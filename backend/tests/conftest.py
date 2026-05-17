import asyncio
import uuid
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.security import create_access_token, hash_password
from app.database import Base, get_async_session
from app.main import app
from app.models.tenant import Tenant
from app.models.user import User, UserRole

TEST_DATABASE_URL = "postgresql+asyncpg://blackdragon:blackdragon_dev@localhost:5432/blackdragon_test"

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
test_session_factory = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with test_session_factory() as session:
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def _get_test_session() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    app.dependency_overrides[get_async_session] = _get_test_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_tenant(db_session: AsyncSession) -> Tenant:
    tenant = Tenant(
        id=uuid.uuid4(),
        name="Test Tenant",
        slug="test-tenant",
        is_active=True,
    )
    db_session.add(tenant)
    await db_session.flush()
    return tenant


@pytest_asyncio.fixture
async def test_user(db_session: AsyncSession, test_tenant: Tenant) -> User:
    user = User(
        id=uuid.uuid4(),
        tenant_id=test_tenant.id,
        email="user@test.com",
        hashed_password=hash_password("password123"),
        full_name="Test User",
        role=UserRole.CLIENT,
        is_active=True,
    )
    db_session.add(user)
    await db_session.flush()
    return user


@pytest_asyncio.fixture
async def admin_user(db_session: AsyncSession, test_tenant: Tenant) -> User:
    user = User(
        id=uuid.uuid4(),
        tenant_id=test_tenant.id,
        email="admin@test.com",
        hashed_password=hash_password("admin123"),
        full_name="Admin User",
        role=UserRole.ADMIN,
        is_active=True,
    )
    db_session.add(user)
    await db_session.flush()
    return user


@pytest_asyncio.fixture
async def auth_headers(test_user: User) -> dict[str, str]:
    token = create_access_token(test_user.id, test_user.tenant_id, test_user.role.value)
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture
async def admin_headers(admin_user: User) -> dict[str, str]:
    token = create_access_token(admin_user.id, admin_user.tenant_id, admin_user.role.value)
    return {"Authorization": f"Bearer {token}"}
