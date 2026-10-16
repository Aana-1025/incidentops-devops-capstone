"""Small API setup helpers shared by IncidentOps tests."""

from httpx import AsyncClient


async def create_service(
    client: AsyncClient,
    name: str = "Payments API",
) -> dict[str, object]:
    """Create one service and return its response body."""

    response = await client.post(
        "/api/services",
        json={
            "name": name,
            "description": f"Test service: {name}",
            "status": "Operational",
        },
    )
    assert response.status_code == 201, response.text
    return response.json()


async def create_incident(
    client: AsyncClient,
    service_id: int,
    *,
    title: str = "Elevated error rate",
    severity: str = "P1 Critical",
    status: str = "Open",
    assignee: str | None = "on-call@example.test",
) -> dict[str, object]:
    """Create one incident and return its response body."""

    response = await client.post(
        "/api/incidents",
        json={
            "title": title,
            "description": f"Test incident: {title}",
            "severity": severity,
            "status": status,
            "service_id": service_id,
            "assignee": assignee,
        },
    )
    assert response.status_code == 201, response.text
    return response.json()
