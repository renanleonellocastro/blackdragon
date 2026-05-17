"""Tests for deployment API endpoints."""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_deploy_no_artifact(client: AsyncClient, auth_headers: dict) -> None:
    resp = await client.post(
        "/api/projects/00000000-0000-0000-0000-000000000001/deployments",
        json={"artifact_id": "00000000-0000-0000-0000-000000000099", "board_instance_id": "00000000-0000-0000-0000-000000000099"},
        headers=auth_headers,
    )
    assert resp.status_code in (404, 422)


@pytest.mark.asyncio
async def test_list_deployments_empty(client: AsyncClient, auth_headers: dict) -> None:
    resp = await client.get(
        "/api/projects/00000000-0000-0000-0000-000000000001/deployments",
        headers=auth_headers,
    )
    assert resp.status_code == 200
