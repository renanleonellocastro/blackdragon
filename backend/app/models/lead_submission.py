import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class LeadStatus(str, enum.Enum):
    NEW = "new"
    REVIEWED = "reviewed"
    CONTACTED = "contacted"
    ARCHIVED = "archived"


class LeadSubmission(Base):
    __tablename__ = "lead_submissions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    company: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[LeadStatus] = mapped_column(Enum(LeadStatus), nullable=False, default=LeadStatus.NEW, index=True)
    reviewed_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), index=True)
