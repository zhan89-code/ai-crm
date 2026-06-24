import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_contact(client: AsyncClient):
    resp = await client.post("/api/v1/contacts", json={
        "email": "test@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "company": "Acme Corp"
    })
    assert resp.status_code in [200, 201]

@pytest.mark.asyncio
async def test_list_contacts(client: AsyncClient):
    resp = await client.get("/api/v1/contacts")
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data

@pytest.mark.asyncio
async def test_get_contact_not_found(client: AsyncClient):
    resp = await client.get("/api/v1/contacts/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404
