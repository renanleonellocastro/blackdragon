import enum
import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ProjectStatus(str, enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    property_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("properties.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[ProjectStatus] = mapped_column(Enum(ProjectStatus), nullable=False, default=ProjectStatus.DRAFT)
    current_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    is_locked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    locked_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    locked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    property = relationship("Property", back_populates="projects")
    diagrams = relationship("Diagram", back_populates="project", cascade="all, delete-orphan")
