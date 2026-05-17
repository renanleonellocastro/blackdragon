"""Test tenant isolation middleware filters queries correctly."""
import uuid

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.tenant import current_tenant_id
from app.models.tenant import Tenant
from app.models.user import User, UserRole


@pytest.mark.asyncio
async def test_tenant_filtering_returns_only_own_users(db_session: AsyncSession) -> None:
    """Users from one tenant should not be visible when querying with another tenant's context."""
    # Create two tenants
    tenant_a = Tenant(id=uuid.uuid4(), name="Tenant A", slug="tenant-a")
    tenant_b = Tenant(id=uuid.uuid4(), name="Tenant B", slug="tenant-b")
    db_session.add_all([tenant_a, tenant_b])
    await db_session.flush()

    # Create users in each tenant
    user_a = User(
        id=uuid.uuid4(), tenant_id=tenant_a.id, email="a@a.com",
        hashed_password="hash", full_name="User A", role=UserRole.CLIENT,
    )
    user_b = User(
        id=uuid.uuid4(), tenant_id=tenant_b.id, email="b@b.com",
        hashed_password="hash", full_name="User B", role=UserRole.CLIENT,
    )
    db_session.add_all([user_a, user_b])
    await db_session.flush()

    # Query with tenant A context
    token = current_tenant_id.set(tenant_a.id)
    try:
        result = await db_session.execute(select(User))
        users = result.scalars().all()
        assert len(users) == 1
        assert users[0].email == "a@a.com"
    finally:
        current_tenant_id.reset(token)


@pytest.mark.asyncio
async def test_no_tenant_context_returns_all(db_session: AsyncSession) -> None:
    """Without tenant context, all users are visible (for admin operations)."""
    tenant = Tenant(id=uuid.uuid4(), name="Tenant", slug="tenant-no-ctx")
    db_session.add(tenant)
    await db_session.flush()

    user = User(
        id=uuid.uuid4(), tenant_id=tenant.id, email="nocontext@test.com",
        hashed_password="hash", full_name="User", role=UserRole.CLIENT,
    )
    db_session.add(user)
    await db_session.flush()

    # No tenant context set
    result = await db_session.execute(select(User).where(User.email == "nocontext@test.com"))
    users = result.scalars().all()
    assert len(users) == 1
