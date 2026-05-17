import uuid

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Any

from sqlalchemy import select

from app.api.deps import CurrentUser, DbSession
from app.core.exceptions import NotFoundError
from app.models.module import Module

router = APIRouter()


class ModuleCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    graph_data: dict[str, Any]
    input_ports: list[dict[str, Any]] = []
    output_ports: list[dict[str, Any]] = []


class ModuleResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    graph_data: dict[str, Any]
    input_ports: list[dict[str, Any]]
    output_ports: list[dict[str, Any]]
    created_at: str

    model_config = {"from_attributes": True}


@router.get("", response_model=list[ModuleResponse])
async def list_modules(user: CurrentUser, db: DbSession) -> list:
    result = await db.execute(
        select(Module).where(Module.tenant_id == user.tenant_id).order_by(Module.name)
    )
    return list(result.scalars().all())


@router.post("", response_model=ModuleResponse, status_code=201)
async def create_module(data: ModuleCreate, user: CurrentUser, db: DbSession) -> Module:
    module = Module(
        id=uuid.uuid4(),
        tenant_id=user.tenant_id,
        created_by=user.id,
        **data.model_dump(),
    )
    db.add(module)
    await db.commit()
    await db.refresh(module)
    return module


@router.delete("/{module_id}", status_code=204)
async def delete_module(module_id: str, user: CurrentUser, db: DbSession) -> None:
    result = await db.execute(
        select(Module).where(Module.id == uuid.UUID(module_id), Module.tenant_id == user.tenant_id)
    )
    module = result.scalar_one_or_none()
    if not module:
        raise NotFoundError("Module not found")
    await db.delete(module)
    await db.commit()
