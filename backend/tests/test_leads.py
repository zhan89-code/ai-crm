import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_lead(client: AsyncClient):
    resp = await client.post("/api/v1/leads", json={
        "source": "website",
        "status": "new"
    })
    assert resp.status_code in [200, 201]

@pytest.mark.asyncio
async def test_score_lead(client: AsyncClient):
    resp = await client.post("/api/v1/leads/00000000-0000-0000-0000-000000000000/score")
    assert resp.status_code in [200, 404]

@pytest.mark.asyncio
async def test_convert_lead(client: AsyncClient):
    resp = await client.post("/api/v1/leads/00000000-0000-0000-0000-000000000000/convert")
    assert resp.status_code in [200, 404]
