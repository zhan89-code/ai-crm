import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_deal(client: AsyncClient):
    resp = await client.post("/api/v1/deals", json={
        "name": "Big Deal",
        "stage": "prospecting",
        "value": 50000.0
    })
    assert resp.status_code in [200, 201]

@pytest.mark.asyncio
async def test_update_stage(client: AsyncClient):
    resp = await client.patch("/api/v1/deals/00000000-0000-0000-0000-000000000000/stage", json={
        "stage": "negotiation",
        "probability": 0.75
    })
    assert resp.status_code in [200, 404]
