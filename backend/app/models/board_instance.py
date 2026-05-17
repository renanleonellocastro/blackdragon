import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class BoardInstance(Base):
    __tablename__ = "board_instances"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False, index=True)
    board_model_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("board_models.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    device_address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    esphome_name: Mapped[str] = mapped_column(String(100), nullable=False)
    wifi_credential_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    ota_credential_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    api_credential_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    board_model = relationship("BoardModel")
    channels = relationship("BoardInstanceChannel", back_populates="board_instance", cascade="all, delete-orphan")


class BoardInstanceChannel(Base):
    __tablename__ = "board_instance_channels"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    board_instance_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("board_instances.id"), nullable=False)
    tenant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    channel_number: Mapped[int] = mapped_column(Integer, nullable=False)
    direction: Mapped[str] = mapped_column(String(10), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    gpio_pin: Mapped[int] = mapped_column(Integer, nullable=False)
    pull_mode: Mapped[str] = mapped_column(String(10), nullable=False, default="none")
    inverted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    debounce_ms: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    board_instance = relationship("BoardInstance", back_populates="channels")
