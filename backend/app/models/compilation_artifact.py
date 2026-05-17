import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class CompilationArtifact(Base):
    __tablename__ = "compilation_artifacts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    diagram_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("diagrams.id"), nullable=False, index=True)
    target: Mapped[str] = mapped_column(String(50), nullable=False, default="esphome")
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    output: Mapped[str] = mapped_column(Text, nullable=False)
    node_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    edge_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
