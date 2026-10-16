"""FastAPI entry point and reliability endpoints for IncidentOps."""

import logging

from fastapi import FastAPI, HTTPException, status
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from .api import incidents_router, services_router
from .config import settings
from .db import engine

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    description="Database-backed API for the IncidentOps reliability platform.",
    version="0.2.0",
)

app.include_router(services_router)
app.include_router(incidents_router)


@app.get("/", tags=["system"])
def root() -> dict[str, str]:
    """Return service metadata and discovery links."""

    return {
        "name": settings.app_name,
        "product": "IncidentOps",
        "environment": settings.app_env,
        "version": app.version,
        "docs": app.docs_url or "/docs",
    }


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    """Report process liveness without depending on external services."""

    return {"status": "UP", "service": "incidentops-api"}


@app.get("/ready", tags=["system"])
def readiness() -> dict[str, str]:
    """Report readiness only when the PostgreSQL connection succeeds."""

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        logger.warning("Readiness check failed because the database is unavailable")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"status": "NOT_READY", "database": "unavailable"},
        ) from exc

    return {"status": "READY", "database": "available"}


Instrumentator(excluded_handlers=["/metrics"]).instrument(app).expose(
    app,
    endpoint="/metrics",
)
