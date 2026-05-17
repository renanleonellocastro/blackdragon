from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, NotFoundError
from app.models.blog_post import BlogPost, BlogStatus
from app.schemas.blog import BlogPostCreate, BlogPostUpdate


async def list_published(db: AsyncSession) -> list[BlogPost]:
    result = await db.execute(
        select(BlogPost)
        .where(BlogPost.status == BlogStatus.PUBLISHED)
        .order_by(BlogPost.published_at.desc())
    )
    return list(result.scalars().all())


async def get_by_slug(db: AsyncSession, slug: str) -> BlogPost:
    result = await db.execute(
        select(BlogPost).where(BlogPost.slug == slug, BlogPost.status == BlogStatus.PUBLISHED)
    )
    post = result.scalar_one_or_none()
    if not post:
        raise NotFoundError("Blog post not found")
    return post


async def create_post(db: AsyncSession, data: BlogPostCreate, author_id: UUID) -> BlogPost:
    # Check slug uniqueness
    existing = await db.execute(select(BlogPost).where(BlogPost.slug == data.slug))
    if existing.scalar_one_or_none():
        raise ConflictError("Slug already exists")

    post = BlogPost(**data.model_dump(), author_id=author_id)
    if post.status == BlogStatus.PUBLISHED:
        post.published_at = datetime.now(timezone.utc)
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post


async def update_post(db: AsyncSession, post_id: UUID, data: BlogPostUpdate) -> BlogPost:
    result = await db.execute(select(BlogPost).where(BlogPost.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise NotFoundError("Blog post not found")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(post, field, value)

    # Set published_at on first publish
    if data.status == "published" and not post.published_at:
        post.published_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(post)
    return post


async def delete_post(db: AsyncSession, post_id: UUID) -> None:
    result = await db.execute(select(BlogPost).where(BlogPost.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise NotFoundError("Blog post not found")
    await db.delete(post)
    await db.commit()
