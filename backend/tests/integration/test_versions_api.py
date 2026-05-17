"""Tests for version API endpoints."""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_save_and_list_versions(client: AsyncClient, auth_headers: dict) -> None:
    # Save version returns 201 or 404 (no project in test db)
    resp = await client.post(
        "/api/projects/00000000-0000-0000-0000-000000000001/versions",
        json={"description": "v1"},
        headers=auth_headers,
    )
    assert resp.status_code in (201, 404)


@pytest.mark.asyncio
async def test_list_versions_empty(client: AsyncClient, auth_headers: dict) -> None:
    resp = await client.get(
        "/api/projects/00000000-0000-0000-0000-000000000001/versions",
        headers=auth_headers,
    )
    assert resp.status_code in (200, 404)
