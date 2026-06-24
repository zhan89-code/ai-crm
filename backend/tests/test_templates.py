import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_template(client: AsyncClient):
    resp = await client.post("/api/v1/templates", json={
        "name": "Welcome Email",
        "subject": "Welcome!",
        "body_html": "<h1>Welcome</h1>",
        "category": "onboarding"
    })
    assert resp.status_code in [200, 201]

@pytest.mark.asyncio
async def test_list_templates(client: AsyncClient):
    resp = await client.get("/api/v1/templates")
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
