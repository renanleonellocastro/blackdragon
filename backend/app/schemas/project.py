import uuid
from datetime import datetime

from pydantic import BaseModel, Field


# Property schemas
class PropertyCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    address: str | None = None
    description: str | None = None


class PropertyUpdate(BaseModel):
    name: str | None = None
    address: str | None = None
    description: str | None = None


class PropertyResponse(BaseModel):
    id: uuid.UUID
    name: str
    address: str | None
    description: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PropertyDetail(PropertyResponse):
    projects: list["ProjectSummary"] = []


# Project schemas
class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    property_id: uuid.UUID


class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    status: str | None = None


class ProjectSummary(BaseModel):
    id: uuid.UUID
    name: str
    status: str
    updated_at: datetime

    model_config = {"from_attributes": True}


class ProjectResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    status: str
    property_id: uuid.UUID
    current_version: int
    is_locked: bool
    locked_by: uuid.UUID | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
