"""Integration tests for auth API endpoints."""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient) -> None:
    resp = await client.post("/api/auth/register", json={
        "email": "new@test.com",
        "password": "password123",
        "full_name": "New User",
    })
    assert resp.status_code in (201, 200)
    data = resp.json()
    assert "access_token" in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient) -> None:
    payload = {"email": "dup@test.com", "password": "password123", "full_name": "Dup User"}
    await client.post("/api/auth/register", json=payload)
    resp = await client.post("/api/auth/register", json=payload)
    assert resp.status_code == 409


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient) -> None:
    await client.post("/api/auth/register", json={
        "email": "login@test.com", "password": "password123", "full_name": "Login User",
    })
    resp = await client.post("/api/auth/login", json={
        "email": "login@test.com", "password": "password123",
    })
    assert resp.status_code == 200
    assert "access_token" in resp.json()


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient) -> None:
    await client.post("/api/auth/register", json={
        "email": "wrong@test.com", "password": "password123", "full_name": "Wrong",
    })
    resp = await client.post("/api/auth/login", json={
        "email": "wrong@test.com", "password": "bad_password",
    })
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_me_endpoint(client: AsyncClient, auth_headers: dict) -> None:
    resp = await client.get("/api/auth/me", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "email" in data


@pytest.mark.asyncio
async def test_me_no_auth(client: AsyncClient) -> None:
    resp = await client.get("/api/auth/me")
    assert resp.status_code in (401, 403)
