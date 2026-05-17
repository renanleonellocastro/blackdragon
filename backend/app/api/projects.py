from uuid import UUID

from fastapi import APIRouter, Query

from app.api.deps import CurrentUser, DbSession
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from app.services import project_service

router = APIRouter()


@router.get("", response_model=list[ProjectResponse])
async def list_projects(
    user: CurrentUser,
    db: DbSession,
    property_id: str | None = Query(None),
    status: str | None = Query(None),
) -> list:
    pid = UUID(property_id) if property_id else None
    return await project_service.list_projects(db, user.tenant_id, pid, status)


@router.post("", response_model=ProjectResponse, status_code=201)
async def create_project(data: ProjectCreate, user: CurrentUser, db: DbSession) -> ProjectResponse:
    return await project_service.create_project(db, data, user.tenant_id)


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str, user: CurrentUser, db: DbSession) -> ProjectResponse:
    return await project_service.get_project(db, UUID(project_id), user.tenant_id)


@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str, data: ProjectUpdate, user: CurrentUser, db: DbSession
) -> ProjectResponse:
    return await project_service.update_project(db, UUID(project_id), data, user.tenant_id)


@router.delete("/{project_id}", status_code=204)
async def delete_project(project_id: str, user: CurrentUser, db: DbSession) -> None:
    await project_service.delete_project(db, UUID(project_id), user.tenant_id)


@router.post("/{project_id}/duplicate", response_model=ProjectResponse, status_code=201)
async def duplicate_project(project_id: str, user: CurrentUser, db: DbSession) -> ProjectResponse:
    return await project_service.duplicate_project(db, UUID(project_id), user.tenant_id)


@router.post("/{project_id}/lock", response_model=ProjectResponse)
async def lock_project(project_id: str, user: CurrentUser, db: DbSession) -> ProjectResponse:
    return await project_service.lock_project(db, UUID(project_id), user.id, user.tenant_id)


@router.post("/{project_id}/unlock", response_model=ProjectResponse)
async def unlock_project(project_id: str, user: CurrentUser, db: DbSession) -> ProjectResponse:
    return await project_service.unlock_project(db, UUID(project_id), user.id, user.tenant_id)


# --- Version Endpoints ---

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Any


class VersionCreate(BaseModel):
    description: str | None = None


class VersionResponse(BaseModel):
    id: str
    version_number: int
    description: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


@router.post("/{project_id}/versions", status_code=201)
async def save_version(project_id: str, data: VersionCreate, user: CurrentUser, db: DbSession) -> dict:
    v = await project_service.save_version(db, UUID(project_id), user.tenant_id, user.id, data.description)
    return {"id": str(v.id), "version_number": v.version_number, "description": v.description, "created_at": v.created_at}


@router.get("/{project_id}/versions")
async def list_versions(project_id: str, user: CurrentUser, db: DbSession) -> list[dict]:
    versions = await project_service.list_versions(db, UUID(project_id), user.tenant_id)
    return [{"id": str(v.id), "version_number": v.version_number, "description": v.description, "created_at": v.created_at} for v in versions]


@router.post("/{project_id}/versions/{version_number}/rollback")
async def rollback_version(project_id: str, version_number: int, user: CurrentUser, db: DbSession) -> dict:
    v = await project_service.rollback_version(db, UUID(project_id), version_number, user.tenant_id)
    return {"message": "Rolled back", "version_number": v.version_number}
