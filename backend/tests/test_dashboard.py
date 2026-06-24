import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_dashboard_summary(client: AsyncClient):
    resp = await client.get("/api/v1/dashboard/summary")
    assert resp.status_code == 200
    data = resp.json()
    assert "total_contacts" in data or "contacts" in data
