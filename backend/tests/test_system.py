"""Tests for liveness and database-aware readiness."""

from httpx import AsyncClient
import pytest

pytestmark = pytest.mark.anyio


async def test_health_endpoint_reports_process_liveness(
    client: AsyncClient,
) -> None:
    response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "UP",
        "service": "incidentops-api",
    }


async def test_readiness_endpoint_queries_test_database(
    client: AsyncClient,
) -> None:
    response = await client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {
        "status": "READY",
        "database": "available",
    }
