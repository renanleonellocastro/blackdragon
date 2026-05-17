import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class DiagramLayer(str, enum.Enum):
    BOARD = "board"
    HOME_AUTOMATION = "home_automation"


class Diagram(Base):
    __tablename__ = "diagrams"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    layer: Mapped[DiagramLayer] = mapped_column(Enum(DiagramLayer), nullable=False)
    board_instance_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    graph_data: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    draft_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    viewport: Mapped[dict] = mapped_column(JSONB, nullable=False, default=lambda: {"x": 0, "y": 0, "zoom": 1})
    node_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    edge_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    project = relationship("Project", back_populates="diagrams")
