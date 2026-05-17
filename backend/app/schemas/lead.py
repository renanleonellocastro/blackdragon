import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class LeadCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    company: str | None = None
    phone: str | None = Field(None, max_length=50)
    message: str = Field(..., min_length=10, max_length=5000)


class LeadResponse(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    company: str | None
    phone: str | None
    message: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class LeadUpdate(BaseModel):
    status: str | None = None
