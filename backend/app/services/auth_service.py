"""Authentication service — register, login, refresh."""
import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, UnauthorizedError
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.tenant import Tenant
from app.models.user import User, UserRole
from app.schemas.auth import RegisterRequest, TokenResponse, UserResponse


async def register(db: AsyncSession, data: RegisterRequest) -> TokenResponse:
    # Check email uniqueness
    existing = await db.execute(select(User).where(User.email == data.email))
    if existing.scalar_one_or_none():
        raise ConflictError("Email already registered")

    # Create tenant
    tenant_name = data.company_name or data.full_name
    slug = tenant_name.lower().replace(" ", "-")[:100]
    # Ensure slug uniqueness
    slug_check = await db.execute(select(Tenant).where(Tenant.slug == slug))
    if slug_check.scalar_one_or_none():
        slug = f"{slug}-{uuid.uuid4().hex[:6]}"

    tenant = Tenant(id=uuid.uuid4(), name=tenant_name, slug=slug, is_active=True)
    db.add(tenant)
    await db.flush()

    # Create user
    user = User(
        id=uuid.uuid4(),
        tenant_id=tenant.id,
        email=data.email,
        hashed_password=hash_password(data.password),
        full_name=data.full_name,
        role=UserRole.CLIENT,
        is_active=True,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    token = create_access_token(user.id, user.tenant_id, user.role.value)
    return TokenResponse(
        access_token=token,
        user=UserResponse.model_validate(user),
    )


async def login(db: AsyncSession, email: str, password: str) -> TokenResponse:
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(password, user.hashed_password):
        raise UnauthorizedError("Invalid credentials")
    if not user.is_active:
        raise UnauthorizedError("Account deactivated")

    user.last_login_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(user)

    token = create_access_token(user.id, user.tenant_id, user.role.value)
    return TokenResponse(
        access_token=token,
        user=UserResponse.model_validate(user),
    )


async def refresh(db: AsyncSession, token: str) -> dict[str, str]:
    payload = decode_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedError("Invalid token")

    result = await db.execute(select(User).where(User.id == uuid.UUID(user_id)))
    user = result.scalar_one_or_none()
    if not user or not user.is_active:
        raise UnauthorizedError("Invalid token")

    new_token = create_access_token(user.id, user.tenant_id, user.role.value)
    return {"access_token": new_token, "token_type": "bearer"}
