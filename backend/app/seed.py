"""Database seed script — creates admin user and test client."""
import asyncio
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.database import async_session_factory
from app.models.tenant import Tenant
from app.models.user import User, UserRole


async def seed() -> None:
    async with async_session_factory() as session:
        await _seed_admin(session)
        await _seed_test_client(session)
        await session.commit()
        print("Seed complete.")


async def _seed_admin(session: AsyncSession) -> None:
    result = await session.execute(select(User).where(User.email == "admin@blackdragon.io"))
    if result.scalar_one_or_none():
        print("Admin user already exists, skipping.")
        return

    tenant = Tenant(
        id=uuid.uuid4(),
        name="BlackDragon",
        slug="blackdragon",
        is_active=True,
    )
    session.add(tenant)
    await session.flush()

    admin = User(
        id=uuid.uuid4(),
        tenant_id=tenant.id,
        email="admin@blackdragon.io",
        hashed_password=hash_password("admin123"),
        full_name="System Administrator",
        role=UserRole.ADMIN,
        is_active=True,
    )
    session.add(admin)
    print(f"Created admin tenant '{tenant.slug}' and user '{admin.email}'")


async def _seed_test_client(session: AsyncSession) -> None:
    result = await session.execute(select(User).where(User.email == "client@test.com"))
    if result.scalar_one_or_none():
        print("Test client already exists, skipping.")
        return

    tenant = Tenant(
        id=uuid.uuid4(),
        name="Test Company",
        slug="test-company",
        is_active=True,
    )
    session.add(tenant)
    await session.flush()

    client = User(
        id=uuid.uuid4(),
        tenant_id=tenant.id,
        email="client@test.com",
        hashed_password=hash_password("client123"),
        full_name="Test Client",
        role=UserRole.CLIENT,
        is_active=True,
    )
    session.add(client)
    print(f"Created test tenant '{tenant.slug}' and user '{client.email}'")


if __name__ == "__main__":
    asyncio.run(seed())
