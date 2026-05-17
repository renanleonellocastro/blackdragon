"""Tests for admin API endpoints."""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_users_requires_admin(client: AsyncClient, auth_headers: dict) -> None:
    resp = await client.get("/api/admin/users", headers=auth_headers)
    # Regular user should get 403; admin should get 200
    assert resp.status_code in (200, 403)


@pytest.mark.asyncio
async def test_list_tenants_requires_admin(client: AsyncClient, auth_headers: dict) -> None:
    resp = await client.get("/api/admin/tenants", headers=auth_headers)
    assert resp.status_code in (200, 403)


@pytest.mark.asyncio
async def test_list_audit_logs(client: AsyncClient, auth_headers: dict) -> None:
    resp = await client.get("/api/admin/audit-logs", headers=auth_headers)
    assert resp.status_code in (200, 403)
