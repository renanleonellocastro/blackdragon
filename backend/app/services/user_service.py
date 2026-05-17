"""User management service — list, update, deactivate."""
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.user import User
from app.schemas.user import UserUpdate


async def list_users(db: AsyncSession, tenant_id: uuid.UUID | None = None) -> list[User]:
    query = select(User).order_by(User.email)
    if tenant_id:
        query = query.where(User.tenant_id == tenant_id)
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_user(db: AsyncSession, user_id: uuid.UUID) -> User:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise NotFoundError("User not found")
    return user


async def update_user(db: AsyncSession, user_id: uuid.UUID, data: UserUpdate) -> User:
    user = await get_user(db, user_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    await db.commit()
    await db.refresh(user)
    return user


async def deactivate_user(db: AsyncSession, user_id: uuid.UUID) -> User:
    user = await get_user(db, user_id)
    user.is_active = False
    await db.commit()
    await db.refresh(user)
    return user
