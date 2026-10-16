"""Isolated PostgreSQL fixtures for the IncidentOps API test suite."""

from collections.abc import AsyncIterator, Generator
import os
from pathlib import Path
import re

from alembic import command
from alembic.config import Config
from httpx import ASGITransport, AsyncClient
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session, sessionmaker

BACKEND_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEST_DATABASE_URL = (
    "postgresql+psycopg://incidentops:incidentops@localhost:5433/incidentops_test"
)
TEST_DATABASE_URL = os.environ.get(
    "INCIDENTOPS_TEST_DATABASE_URL",
    DEFAULT_TEST_DATABASE_URL,
)
test_url = make_url(TEST_DATABASE_URL)
test_database_name = test_url.database or ""

if test_database_name == "incidentops" or not test_database_name.endswith("_test"):
    raise RuntimeError(
        "Tests require a dedicated database whose name ends with '_test'."
    )
if not re.fullmatch(r"[A-Za-z0-9_]+", test_database_name):
    raise RuntimeError("Test database name contains unsupported characters.")

# The application creates its engine at import time, so force isolation first.
os.environ["DATABASE_URL"] = TEST_DATABASE_URL

from app.db import get_db  # noqa: E402
from app.main import app  # noqa: E402

test_engine = create_engine(TEST_DATABASE_URL, pool_pre_ping=True)
TestSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    expire_on_commit=False,
)


def create_test_database_if_missing() -> None:
    """Create only the validated dedicated test database when necessary."""

    admin_url = test_url.set(database="postgres")
    admin_engine = create_engine(admin_url, isolation_level="AUTOCOMMIT")
    try:
        with admin_engine.connect() as connection:
            exists = connection.scalar(
                text("SELECT 1 FROM pg_database WHERE datname = :database_name"),
                {"database_name": test_database_name},
            )
            if exists is None:
                connection.exec_driver_sql(
                    f'CREATE DATABASE "{test_database_name}"'
                )
    finally:
        admin_engine.dispose()


def migrate_test_database() -> None:
    """Apply the real Alembic migration chain to the test database."""

    config = Config(str(BACKEND_ROOT / "alembic.ini"))
    config.set_main_option("script_location", str(BACKEND_ROOT / "alembic"))
    config.set_main_option("sqlalchemy.url", TEST_DATABASE_URL.replace("%", "%%"))
    command.upgrade(config, "head")


def clear_test_data() -> None:
    """Remove test rows and reset identifiers without dropping the schema."""

    with test_engine.begin() as connection:
        connection.execute(
            text("TRUNCATE TABLE incidents, services RESTART IDENTITY CASCADE")
        )


def override_get_db() -> Generator[Session, None, None]:
    """Provide request sessions bound only to incidentops_test."""

    with TestSessionLocal() as session:
        yield session


@pytest.fixture(scope="session", autouse=True)
def prepared_test_database() -> Generator[None, None, None]:
    """Create, migrate, and register the isolated database for this run."""

    create_test_database_if_missing()
    migrate_test_database()
    app.dependency_overrides[get_db] = override_get_db
    clear_test_data()
    yield
    clear_test_data()
    app.dependency_overrides.pop(get_db, None)
    test_engine.dispose()


@pytest.fixture(autouse=True)
def isolated_test_data(
    prepared_test_database: None,
) -> Generator[None, None, None]:
    """Give every test an empty database and clean up afterward."""

    clear_test_data()
    yield
    clear_test_data()


@pytest.fixture
def anyio_backend() -> str:
    """Use asyncio only; Trio is not required by the application."""

    return "asyncio"


@pytest.fixture
async def client(
    prepared_test_database: None,
) -> AsyncIterator[AsyncClient]:
    """Call FastAPI in-process through httpx's non-blocking ASGI transport."""

    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as api_client:
        yield api_client
