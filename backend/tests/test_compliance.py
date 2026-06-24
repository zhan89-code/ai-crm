import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_dsar(client: AsyncClient):
    resp = await client.post("/api/v1/compliance/dsar", json={
        "request_type": "access",
        "requester_email": "user@example.com",
        "requester_name": "Test User"
    })
    assert resp.status_code in [200, 201]

@pytest.mark.asyncio
async def test_list_dsar(client: AsyncClient):
    resp = await client.get("/api/v1/compliance/dsar")
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
