import uuid
from datetime import datetime

from pydantic import BaseModel

from fastapi import APIRouter

from app.api.deps import AdminUser, DbSession
from app.schemas.user import UserList, UserUpdate
from app.services import audit_service, user_service

from sqlalchemy import select

router = APIRouter()


class AuditLogResponse(BaseModel):
    id: uuid.UUID
    action: str
    resource_type: str
    resource_id: str | None
    user_id: uuid.UUID | None
    tenant_id: uuid.UUID | None
    created_at: datetime

    model_config = {"from_attributes": True}


class TenantResponse(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


@router.get("/users", response_model=list[UserList])
async def list_users(_admin: AdminUser, db: DbSession) -> list:
    return await user_service.list_users(db)


@router.patch("/users/{user_id}", response_model=UserList)
async def update_user(user_id: str, data: UserUpdate, _admin: AdminUser, db: DbSession) -> UserList:
    return await user_service.update_user(db, uuid.UUID(user_id), data)


@router.post("/users/{user_id}/deactivate", response_model=UserList)
async def deactivate_user(user_id: str, _admin: AdminUser, db: DbSession) -> UserList:
    return await user_service.deactivate_user(db, uuid.UUID(user_id))


@router.get("/tenants", response_model=list[TenantResponse])
async def list_tenants(_admin: AdminUser, db: DbSession) -> list:
    from app.models.tenant import Tenant

    result = await db.execute(select(Tenant).order_by(Tenant.name))
    return list(result.scalars().all())


@router.get("/audit-logs", response_model=list[AuditLogResponse])
async def list_audit_logs(_admin: AdminUser, db: DbSession) -> list:
    return await audit_service.query_logs(db)
