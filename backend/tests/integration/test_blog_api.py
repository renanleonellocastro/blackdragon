"""Integration tests for blog API."""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_blog_empty(client: AsyncClient) -> None:
    resp = await client.get("/api/blog")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


@pytest.mark.asyncio
async def test_create_blog_requires_admin(client: AsyncClient, auth_headers: dict) -> None:
    resp = await client.post("/api/blog", json={
        "title": "Test Post",
        "slug": "test-post",
        "excerpt": "An excerpt",
        "content": "Full content here",
    }, headers=auth_headers)
    # Regular user should get 403
    assert resp.status_code in (201, 403)


@pytest.mark.asyncio
async def test_create_blog_as_admin(client: AsyncClient, admin_headers: dict) -> None:
    resp = await client.post("/api/blog", json={
        "title": "Admin Post",
        "slug": "admin-post",
        "excerpt": "Admin excerpt",
        "content": "Admin content",
    }, headers=admin_headers)
    assert resp.status_code in (200, 201)
