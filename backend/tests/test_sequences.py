import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_sequence(client: AsyncClient):
    resp = await client.post("/api/v1/sequences", json={
        "name": "Welcome Series",
        "status": "draft"
    })
    assert resp.status_code in [200, 201]

@pytest.mark.asyncio
async def test_list_sequences(client: AsyncClient):
    resp = await client.get("/api/v1/sequences")
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
