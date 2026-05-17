import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class DiagramCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    layer: str = Field(..., pattern=r"^(board|home_automation)$")
    board_instance_id: uuid.UUID | None = None


class DiagramUpdate(BaseModel):
    name: str | None = None
    graph_data: dict[str, Any] | None = None
    viewport: dict[str, Any] | None = None


class DraftSave(BaseModel):
    draft_data: dict[str, Any]
    viewport: dict[str, Any] | None = None


class DiagramResponse(BaseModel):
    id: uuid.UUID
    name: str
    layer: str
    board_instance_id: uuid.UUID | None
    graph_data: dict[str, Any]
    draft_data: dict[str, Any] | None
    viewport: dict[str, Any]
    node_count: int
    edge_count: int
    updated_at: datetime
    created_at: datetime

    model_config = {"from_attributes": True}


class DiagramSummary(BaseModel):
    id: uuid.UUID
    name: str
    layer: str
    board_instance_id: uuid.UUID | None
    has_draft: bool = False
    node_count: int
    edge_count: int
    updated_at: datetime
    created_at: datetime

    model_config = {"from_attributes": True}
