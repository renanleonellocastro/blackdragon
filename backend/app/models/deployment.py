import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class DeploymentStatus(str, enum.Enum):
    PENDING = "pending"
    UPLOADING = "uploading"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Deployment(Base):
    __tablename__ = "deployments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False, index=True)
    board_instance_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("board_instances.id"), nullable=False)
    artifact_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("compilation_artifacts.id"), nullable=False)
    deployed_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    status: Mapped[DeploymentStatus] = mapped_column(Enum(DeploymentStatus), nullable=False, default=DeploymentStatus.PENDING)
    progress_percent: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
