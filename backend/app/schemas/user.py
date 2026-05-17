import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., min_length=1, max_length=255)
    role: str = "client"


class UserUpdate(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None
    is_active: bool | None = None


class UserList(BaseModel):
    id: uuid.UUID
    email: str
    full_name: str
    role: str
    is_active: bool
    last_login_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}
