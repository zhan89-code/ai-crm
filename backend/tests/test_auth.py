
import pytest
from httpx import AsyncClient, ASGITransport
from app.app import app


@pytest.mark.asyncio
async def test_health():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_register_and_login():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        reg = await client.post("/api/v1/auth/register", json={
            "name": "Test Corp", "slug": "test-corp-123", "plan": "free"
        })
        assert reg.status_code == 201

        login = await client.post("/api/v1/auth/login", json={
            "email": "admin@test-corp-123.local", "password": "changeme123"
        })
        assert login.status_code == 200
        data = login.json()
        assert "access_token" in data
        assert "refresh_token" in data


@pytest.mark.asyncio
async def test_rate_limit():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        for _ in range(105):
            await client.get("/health")
        response = await client.get("/health")
    assert response.status_code == 429
