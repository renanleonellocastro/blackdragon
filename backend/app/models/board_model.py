import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class BoardModel(Base):
    __tablename__ = "board_models"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    platform: Mapped[str] = mapped_column(String(50), nullable=False, default="ESP32")
    board_variant: Mapped[str] = mapped_column(String(100), nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    specifications: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    channels = relationship("BoardModelChannel", back_populates="board_model", cascade="all, delete-orphan")


class BoardModelChannel(Base):
    __tablename__ = "board_model_channels"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    board_model_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("board_models.id"), nullable=False)
    channel_number: Mapped[int] = mapped_column(Integer, nullable=False)
    direction: Mapped[str] = mapped_column(String(10), nullable=False)  # input | output
    default_gpio_pin: Mapped[int] = mapped_column(Integer, nullable=False)
    supports_pullup: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    supports_pulldown: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    supports_pwm: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    label: Mapped[str | None] = mapped_column(String(100), nullable=True)

    board_model = relationship("BoardModel", back_populates="channels")
