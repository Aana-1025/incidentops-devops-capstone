"""Database-backed tests for Incident lifecycle and statistics."""

from httpx import AsyncClient
import pytest

from tests.helpers import create_incident, create_service

pytestmark = pytest.mark.anyio


async def test_create_list_get_and_filter_incident(client: AsyncClient) -> None:
    service = await create_service(client)
    incident = await create_incident(client, int(service["id"]))

    list_response = await client.get(
        "/api/incidents",
        params={
            "status": "Open",
            "severity": "P1 Critical",
            "service_id": service["id"],
            "assignee": "on-call@example.test",
        },
    )
    get_response = await client.get(f"/api/incidents/{incident['id']}")

    assert list_response.status_code == 200
    assert [item["id"] for item in list_response.json()] == [incident["id"]]
    assert get_response.status_code == 200
    assert get_response.json()["service"]["name"] == "Payments API"
    assert get_response.json()["sla_target_minutes"] == 30
    assert get_response.json()["sla_status"] == "ON_TRACK"


async def test_resolve_and_reopen_incident_updates_timestamp(
    client: AsyncClient,
) -> None:
    service = await create_service(client)
    incident = await create_incident(client, int(service["id"]))

    resolved_response = await client.put(
        f"/api/incidents/{incident['id']}",
        json={"status": "Resolved"},
    )
    reopened_response = await client.put(
        f"/api/incidents/{incident['id']}",
        json={"status": "Acknowledged"},
    )

    assert resolved_response.status_code == 200
    assert resolved_response.json()["resolved_at"] is not None
    assert resolved_response.json()["sla_status"] == "MET"
    assert reopened_response.status_code == 200
    assert reopened_response.json()["resolved_at"] is None
    assert reopened_response.json()["status"] == "Acknowledged"


async def test_delete_incident_removes_it(client: AsyncClient) -> None:
    service = await create_service(client)
    incident = await create_incident(client, int(service["id"]))

    delete_response = await client.delete(f"/api/incidents/{incident['id']}")
    get_response = await client.get(f"/api/incidents/{incident['id']}")

    assert delete_response.status_code == 204
    assert get_response.status_code == 404


async def test_invalid_incident_input_returns_validation_error(
    client: AsyncClient,
) -> None:
    service = await create_service(client)
    invalid_payloads = [
        {
            "title": "Invalid severity",
            "severity": "P0 Impossible",
            "service_id": service["id"],
        },
        {
            "title": "Invalid status",
            "severity": "P3 Medium",
            "status": "Unknown",
            "service_id": service["id"],
        },
    ]

    for payload in invalid_payloads:
        response = await client.post("/api/incidents", json=payload)
        assert response.status_code == 422
        assert response.json()["detail"]


async def test_missing_incident_and_service_references_return_not_found(
    client: AsyncClient,
) -> None:
    create_response = await client.post(
        "/api/incidents",
        json={
            "title": "Missing service",
            "severity": "P2 High",
            "service_id": 999999,
        },
    )
    get_response = await client.get("/api/incidents/999999")

    assert create_response.status_code == 404
    assert create_response.json()["detail"] == "Referenced service not found."
    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "Incident not found."


async def test_service_with_incident_cannot_be_deleted(
    client: AsyncClient,
) -> None:
    service = await create_service(client)
    await create_incident(client, int(service["id"]))

    response = await client.delete(f"/api/services/{service['id']}")

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "Service cannot be deleted while incidents reference it."
    )


async def test_incident_statistics_are_database_derived(
    client: AsyncClient,
) -> None:
    payments = await create_service(client, "Payments API")
    accounts = await create_service(client, "Accounts API")
    await create_incident(client, int(payments["id"]), severity="P1 Critical")
    await create_incident(
        client,
        int(accounts["id"]),
        title="Account latency",
        severity="P2 High",
        status="Investigating",
    )
    await create_incident(
        client,
        int(accounts["id"]),
        title="Resolved dependency",
        severity="P3 Medium",
        status="Resolved",
    )

    response = await client.get("/api/incidents/stats")

    assert response.status_code == 200
    assert response.json() == {
        "total_incidents": 3,
        "open_incidents": 2,
        "critical_incidents": 1,
        "resolved_incidents": 1,
        "investigating_incidents": 1,
        "acknowledged_incidents": 0,
        "resolved_today": 1,
        "service_count": 2,
    }
