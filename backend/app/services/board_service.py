"""Board service — catalog listing, instance CRUD, channel update, GPIO conflict check."""
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import ConflictError, NotFoundError
from app.models.board_instance import BoardInstance, BoardInstanceChannel
from app.models.board_model import BoardModel, BoardModelChannel
from app.schemas.board import BoardInstanceCreate, ChannelConfig


async def list_catalog(db: AsyncSession) -> list[BoardModel]:
    result = await db.execute(
        select(BoardModel)
        .where(BoardModel.is_active.is_(True))
        .options(selectinload(BoardModel.channels))
        .order_by(BoardModel.name)
    )
    return list(result.scalars().unique().all())


async def get_catalog_model(db: AsyncSession, model_id: uuid.UUID) -> BoardModel:
    result = await db.execute(
        select(BoardModel)
        .where(BoardModel.id == model_id)
        .options(selectinload(BoardModel.channels))
    )
    model = result.scalar_one_or_none()
    if not model:
        raise NotFoundError("Board model not found")
    return model


async def list_instances(
    db: AsyncSession, project_id: uuid.UUID, tenant_id: uuid.UUID
) -> list[BoardInstance]:
    result = await db.execute(
        select(BoardInstance)
        .where(BoardInstance.project_id == project_id, BoardInstance.tenant_id == tenant_id)
        .options(selectinload(BoardInstance.channels), selectinload(BoardInstance.board_model))
        .order_by(BoardInstance.name)
    )
    return list(result.scalars().unique().all())


async def create_instance(
    db: AsyncSession, data: BoardInstanceCreate, project_id: uuid.UUID, tenant_id: uuid.UUID
) -> BoardInstance:
    # Get board model to seed channels
    model = await get_catalog_model(db, data.board_model_id)

    instance = BoardInstance(
        id=uuid.uuid4(),
        tenant_id=tenant_id,
        project_id=project_id,
        board_model_id=data.board_model_id,
        name=data.name,
        esphome_name=data.esphome_name,
        device_address=data.device_address,
    )
    db.add(instance)
    await db.flush()

    # Create channels from model defaults
    for ch in model.channels:
        channel = BoardInstanceChannel(
            id=uuid.uuid4(),
            board_instance_id=instance.id,
            tenant_id=tenant_id,
            channel_number=ch.channel_number,
            direction=ch.direction,
            name=ch.label or f"Channel {ch.channel_number}",
            gpio_pin=ch.default_gpio_pin,
        )
        db.add(channel)

    await db.commit()
    await db.refresh(instance)
    return instance


async def update_channel(
    db: AsyncSession, instance_id: uuid.UUID, config: ChannelConfig, tenant_id: uuid.UUID
) -> BoardInstanceChannel:
    result = await db.execute(
        select(BoardInstanceChannel).where(
            BoardInstanceChannel.board_instance_id == instance_id,
            BoardInstanceChannel.channel_number == config.channel_number,
            BoardInstanceChannel.tenant_id == tenant_id,
        )
    )
    channel = result.scalar_one_or_none()
    if not channel:
        raise NotFoundError("Channel not found")

    if config.name:
        channel.name = config.name
    if config.gpio_pin is not None:
        # Check GPIO conflict
        conflict = await db.execute(
            select(BoardInstanceChannel).where(
                BoardInstanceChannel.board_instance_id == instance_id,
                BoardInstanceChannel.gpio_pin == config.gpio_pin,
                BoardInstanceChannel.channel_number != config.channel_number,
                BoardInstanceChannel.is_enabled.is_(True),
            )
        )
        if conflict.scalar_one_or_none():
            raise ConflictError(f"GPIO pin {config.gpio_pin} already in use")
        channel.gpio_pin = config.gpio_pin

    channel.pull_mode = config.pull_mode
    channel.inverted = config.inverted
    channel.debounce_ms = config.debounce_ms
    channel.is_enabled = config.is_enabled

    await db.commit()
    await db.refresh(channel)
    return channel


async def delete_instance(
    db: AsyncSession, instance_id: uuid.UUID, tenant_id: uuid.UUID
) -> None:
    result = await db.execute(
        select(BoardInstance).where(
            BoardInstance.id == instance_id, BoardInstance.tenant_id == tenant_id
        )
    )
    instance = result.scalar_one_or_none()
    if not instance:
        raise NotFoundError("Board instance not found")
    await db.delete(instance)
    await db.commit()
