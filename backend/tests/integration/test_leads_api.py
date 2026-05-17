"""Integration tests for leads API."""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_lead(client: AsyncClient) -> None:
    resp = await client.post("/api/leads", json={
        "name": "John Doe",
        "email": "john@example.com",
        "company": "TestCo",
        "message": "Interested in the platform",
    })
    assert resp.status_code in (200, 201)
    data = resp.json()
    assert data["email"] == "john@example.com"


@pytest.mark.asyncio
async def test_list_leads_requires_auth(client: AsyncClient) -> None:
    resp = await client.get("/api/leads")
    assert resp.status_code in (401, 403)


@pytest.mark.asyncio
async def test_list_leads_as_admin(client: AsyncClient, admin_headers: dict) -> None:
    # Create a lead first
    await client.post("/api/leads", json={
        "name": "Jane", "email": "jane@example.com", "company": "Co", "message": "Hi",
    })
    resp = await client.get("/api/leads", headers=admin_headers)
    assert resp.status_code == 200
