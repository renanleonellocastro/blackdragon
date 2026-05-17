import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class BlogPostCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    excerpt: str | None = None
    content: str = Field(..., min_length=1)
    status: str = "draft"


class BlogPostUpdate(BaseModel):
    title: str | None = None
    slug: str | None = None
    excerpt: str | None = None
    content: str | None = None
    status: str | None = None


class BlogPostResponse(BaseModel):
    id: uuid.UUID
    title: str
    slug: str
    excerpt: str | None
    content: str
    author_id: uuid.UUID
    status: str
    published_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class BlogPostList(BaseModel):
    id: uuid.UUID
    title: str
    slug: str
    excerpt: str | None
    status: str
    published_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}
