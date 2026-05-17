from uuid import UUID

from fastapi import APIRouter

from app.api.deps import AdminUser, CurrentUser, DbSession
from app.models.board_model import BoardModel, BoardModelChannel
from app.schemas.board import (
    BoardInstanceCreate,
    BoardInstanceResponse,
    BoardModelCreate,
    BoardModelResponse,
    ChannelConfig,
)
from app.services import board_service

router = APIRouter()


# Catalog endpoints
@router.get("/catalog", response_model=list[BoardModelResponse])
async def list_catalog(db: DbSession) -> list:
    return await board_service.list_catalog(db)


@router.post("/catalog", response_model=BoardModelResponse, status_code=201)
async def create_catalog_model(data: BoardModelCreate, _admin: AdminUser, db: DbSession) -> BoardModel:
    import uuid

    model = BoardModel(
        id=uuid.uuid4(),
        name=data.name,
        slug=data.slug,
        description=data.description,
        platform=data.platform,
        board_variant=data.board_variant,
        image_url=data.image_url,
    )
    db.add(model)
    await db.flush()

    for ch in data.channels:
        channel = BoardModelChannel(id=uuid.uuid4(), board_model_id=model.id, **ch.model_dump())
        db.add(channel)

    await db.commit()
    await db.refresh(model)
    return model


# Instance endpoints (project-scoped)
@router.get("/projects/{project_id}/instances", response_model=list[BoardInstanceResponse])
async def list_instances(project_id: str, user: CurrentUser, db: DbSession) -> list:
    return await board_service.list_instances(db, UUID(project_id), user.tenant_id)


@router.post("/projects/{project_id}/instances", response_model=BoardInstanceResponse, status_code=201)
async def create_instance(
    project_id: str, data: BoardInstanceCreate, user: CurrentUser, db: DbSession
) -> BoardInstanceResponse:
    return await board_service.create_instance(db, data, UUID(project_id), user.tenant_id)


@router.patch("/instances/{instance_id}/channels", response_model=dict)
async def update_channel(
    instance_id: str, config: ChannelConfig, user: CurrentUser, db: DbSession
) -> dict:
    channel = await board_service.update_channel(db, UUID(instance_id), config, user.tenant_id)
    return {"status": "updated", "channel_number": channel.channel_number}


@router.delete("/instances/{instance_id}", status_code=204)
async def delete_instance(instance_id: str, user: CurrentUser, db: DbSession) -> None:
    await board_service.delete_instance(db, UUID(instance_id), user.tenant_id)
