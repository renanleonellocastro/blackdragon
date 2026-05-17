import uuid
from datetime import datetime

from pydantic import BaseModel


class DeployRequest(BaseModel):
    artifact_id: uuid.UUID
    board_instance_id: uuid.UUID


class DeployResponse(BaseModel):
    id: uuid.UUID
    status: str
    board_instance_id: uuid.UUID
    artifact_id: uuid.UUID
    progress_percent: int
    started_at: datetime

    model_config = {"from_attributes": True}


class DeploymentStatus(BaseModel):
    id: uuid.UUID
    status: str
    progress_percent: int
    error_message: str | None
    started_at: datetime
    completed_at: datetime | None

    model_config = {"from_attributes": True}
