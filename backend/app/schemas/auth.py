import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., min_length=1, max_length=255)
    company_name: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: "UserResponse"


class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    full_name: str
    role: str
    tenant_id: uuid.UUID
    last_login_at: datetime | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
