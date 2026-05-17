from uuid import UUID

from fastapi import APIRouter

from app.api.deps import CurrentUser, DbSession
from app.core.exceptions import ConflictError, NotFoundError
from app.models.property import Property
from app.schemas.project import PropertyCreate, PropertyDetail, PropertyResponse, PropertyUpdate

from sqlalchemy import func, select

router = APIRouter()


@router.get("", response_model=list[PropertyResponse])
async def list_properties(user: CurrentUser, db: DbSession) -> list[Property]:
    result = await db.execute(
        select(Property)
        .where(Property.tenant_id == user.tenant_id)
        .order_by(Property.name)
    )
    return list(result.scalars().all())


@router.post("", response_model=PropertyResponse, status_code=201)
async def create_property(data: PropertyCreate, user: CurrentUser, db: DbSession) -> Property:
    import uuid

    prop = Property(id=uuid.uuid4(), tenant_id=user.tenant_id, **data.model_dump())
    db.add(prop)
    await db.commit()
    await db.refresh(prop)
    return prop


@router.get("/{property_id}", response_model=PropertyDetail)
async def get_property(property_id: str, user: CurrentUser, db: DbSession) -> Property:
    result = await db.execute(
        select(Property).where(
            Property.id == UUID(property_id), Property.tenant_id == user.tenant_id
        )
    )
    prop = result.scalar_one_or_none()
    if not prop:
        raise NotFoundError("Property not found")
    return prop


@router.patch("/{property_id}", response_model=PropertyResponse)
async def update_property(
    property_id: str, data: PropertyUpdate, user: CurrentUser, db: DbSession
) -> Property:
    result = await db.execute(
        select(Property).where(
            Property.id == UUID(property_id), Property.tenant_id == user.tenant_id
        )
    )
    prop = result.scalar_one_or_none()
    if not prop:
        raise NotFoundError("Property not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(prop, field, value)
    await db.commit()
    await db.refresh(prop)
    return prop


@router.delete("/{property_id}", status_code=204)
async def delete_property(property_id: str, user: CurrentUser, db: DbSession) -> None:
    result = await db.execute(
        select(Property).where(
            Property.id == UUID(property_id), Property.tenant_id == user.tenant_id
        )
    )
    prop = result.scalar_one_or_none()
    if not prop:
        raise NotFoundError("Property not found")
    if prop.projects:
        raise ConflictError("Property has existing projects")
    await db.delete(prop)
    await db.commit()
