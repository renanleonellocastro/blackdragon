"""Integration tests for projects API endpoints."""
import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.property import Property


@pytest.mark.asyncio
async def test_create_and_list_projects(client: AsyncClient, auth_headers: dict, db_session: AsyncSession, test_tenant) -> None:
    # Create a property first (projects belong to properties)
    prop = Property(id=uuid.uuid4(), tenant_id=test_tenant.id, name="Test Property", address="123 Test St")
    db_session.add(prop)
    await db_session.commit()

    resp = await client.post("/api/projects", json={
        "name": "My Project",
        "property_id": str(prop.id),
    }, headers=auth_headers)
    assert resp.status_code == 201
    project_id = resp.json()["id"]

    # List projects
    resp = await client.get("/api/projects", headers=auth_headers)
    assert resp.status_code == 200
    assert any(p["id"] == project_id for p in resp.json())


@pytest.mark.asyncio
async def test_get_project(client: AsyncClient, auth_headers: dict, db_session: AsyncSession, test_tenant) -> None:
    prop = Property(id=uuid.uuid4(), tenant_id=test_tenant.id, name="Prop", address="456 St")
    db_session.add(prop)
    await db_session.commit()

    resp = await client.post("/api/projects", json={"name": "Proj", "property_id": str(prop.id)}, headers=auth_headers)
    project_id = resp.json()["id"]

    resp = await client.get(f"/api/projects/{project_id}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["name"] == "Proj"


@pytest.mark.asyncio
async def test_update_project(client: AsyncClient, auth_headers: dict, db_session: AsyncSession, test_tenant) -> None:
    prop = Property(id=uuid.uuid4(), tenant_id=test_tenant.id, name="Prop", address="789 St")
    db_session.add(prop)
    await db_session.commit()

    resp = await client.post("/api/projects", json={"name": "Original", "property_id": str(prop.id)}, headers=auth_headers)
    project_id = resp.json()["id"]

    resp = await client.patch(f"/api/projects/{project_id}", json={"name": "Updated"}, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["name"] == "Updated"


@pytest.mark.asyncio
async def test_delete_project(client: AsyncClient, auth_headers: dict, db_session: AsyncSession, test_tenant) -> None:
    prop = Property(id=uuid.uuid4(), tenant_id=test_tenant.id, name="Prop", address="Del St")
    db_session.add(prop)
    await db_session.commit()

    resp = await client.post("/api/projects", json={"name": "DeleteMe", "property_id": str(prop.id)}, headers=auth_headers)
    project_id = resp.json()["id"]

    resp = await client.delete(f"/api/projects/{project_id}", headers=auth_headers)
    assert resp.status_code == 204


@pytest.mark.asyncio
async def test_duplicate_project(client: AsyncClient, auth_headers: dict, db_session: AsyncSession, test_tenant) -> None:
    prop = Property(id=uuid.uuid4(), tenant_id=test_tenant.id, name="Prop", address="Dup St")
    db_session.add(prop)
    await db_session.commit()

    resp = await client.post("/api/projects", json={"name": "Source", "property_id": str(prop.id)}, headers=auth_headers)
    project_id = resp.json()["id"]

    resp = await client.post(f"/api/projects/{project_id}/duplicate", headers=auth_headers)
    assert resp.status_code == 201
    assert "Copy" in resp.json()["name"]


@pytest.mark.asyncio
async def test_project_not_found(client: AsyncClient, auth_headers: dict) -> None:
    fake_id = str(uuid.uuid4())
    resp = await client.get(f"/api/projects/{fake_id}", headers=auth_headers)
    assert resp.status_code == 404
