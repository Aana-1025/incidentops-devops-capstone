"""Database-backed tests for the Service API."""

from httpx import AsyncClient
import pytest

from tests.helpers import create_service

pytestmark = pytest.mark.anyio


async def test_create_list_and_get_service(client: AsyncClient) -> None:
    payments = await create_service(client, "Payments API")
    accounts = await create_service(client, "Accounts API")

    list_response = await client.get("/api/services")
    get_response = await client.get(f"/api/services/{payments['id']}")

    assert list_response.status_code == 200
    assert [item["name"] for item in list_response.json()] == [
        "Accounts API",
        "Payments API",
    ]
    assert get_response.status_code == 200
    assert get_response.json()["id"] == payments["id"]
    assert accounts["id"] != payments["id"]


async def test_update_service_preserves_omitted_fields(client: AsyncClient) -> None:
    service = await create_service(client)

    response = await client.put(
        f"/api/services/{service['id']}",
        json={"status": "Degraded"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "Degraded"
    assert response.json()["name"] == service["name"]
    assert response.json()["description"] == service["description"]


async def test_duplicate_service_name_returns_conflict(client: AsyncClient) -> None:
    await create_service(client)

    response = await client.post(
        "/api/services",
        json={"name": "Payments API"},
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "A service with this name already exists."


async def test_invalid_service_input_returns_validation_error(
    client: AsyncClient,
) -> None:
    invalid_payloads = [
        {"name": "   "},
        {"name": "Invalid Status Service", "status": "Unknown"},
    ]

    for payload in invalid_payloads:
        response = await client.post("/api/services", json=payload)
        assert response.status_code == 422
        assert response.json()["detail"]


async def test_missing_service_returns_not_found(client: AsyncClient) -> None:
    response = await client.get("/api/services/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Service not found."


async def test_delete_unused_service_removes_it(client: AsyncClient) -> None:
    service = await create_service(client)

    delete_response = await client.delete(f"/api/services/{service['id']}")
    get_response = await client.get(f"/api/services/{service['id']}")

    assert delete_response.status_code == 204
    assert delete_response.content == b""
    assert get_response.status_code == 404
