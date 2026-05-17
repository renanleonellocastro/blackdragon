import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel


class CompileRequest(BaseModel):
    diagram_id: uuid.UUID
    context: dict[str, Any] = {}


class ValidationErrorItem(BaseModel):
    node_id: str | None
    message: str
    severity: str


class ValidationResultSchema(BaseModel):
    valid: bool
    errors: list[ValidationErrorItem]
    warnings: list[ValidationErrorItem]


class CompileResponse(BaseModel):
    success: bool
    validation: ValidationResultSchema
    output: str | None = None
    artifact_id: uuid.UUID | None = None


class ArtifactResponse(BaseModel):
    id: uuid.UUID
    diagram_id: uuid.UUID
    target: str
    version: int
    output: str
    node_count: int
    edge_count: int
    created_at: datetime

    model_config = {"from_attributes": True}
