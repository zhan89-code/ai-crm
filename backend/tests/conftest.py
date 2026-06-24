import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from app.app import app
from app.core.database import Base, engine

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest.fixture
def auth_headers():
    return {"Authorization": "Bearer test-token"}
