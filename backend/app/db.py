"""SQLAlchemy engine, session factory, and FastAPI dependency."""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from .config import settings


class Base(DeclarativeBase):
    """Base class for all future IncidentOps ORM models."""


engine_options: dict[str, object] = {"pool_pre_ping": True}
if make_url(settings.database_url).get_backend_name() == "postgresql":
    engine_options["connect_args"] = {
        "connect_timeout": settings.database_connect_timeout_seconds,
    }

engine = create_engine(settings.database_url, **engine_options)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db() -> Generator[Session, None, None]:
    """Provide a request-scoped database session."""

    with SessionLocal() as session:
        yield session
