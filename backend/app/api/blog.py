from fastapi import APIRouter

from app.api.deps import AdminUser, DbSession
from app.models.blog_post import BlogPost
from app.schemas.blog import BlogPostCreate, BlogPostList, BlogPostResponse, BlogPostUpdate
from app.services import blog_service

router = APIRouter()


@router.get("", response_model=list[BlogPostList])
async def list_published_posts(db: DbSession) -> list[BlogPost]:
    return await blog_service.list_published(db)


@router.get("/{slug}", response_model=BlogPostResponse)
async def get_post_by_slug(slug: str, db: DbSession) -> BlogPost:
    return await blog_service.get_by_slug(db, slug)


@router.post("", response_model=BlogPostResponse, status_code=201)
async def create_post(data: BlogPostCreate, admin: AdminUser, db: DbSession) -> BlogPost:
    return await blog_service.create_post(db, data, admin.id)


@router.patch("/{post_id}", response_model=BlogPostResponse)
async def update_post(post_id: str, data: BlogPostUpdate, _admin: AdminUser, db: DbSession) -> BlogPost:
    from uuid import UUID

    return await blog_service.update_post(db, UUID(post_id), data)


@router.delete("/{post_id}", status_code=204)
async def delete_post(post_id: str, _admin: AdminUser, db: DbSession) -> None:
    from uuid import UUID

    await blog_service.delete_post(db, UUID(post_id))
