from fastapi import APIRouter

from sqlalchemy import select

from app.api.deps import AdminUser, DbSession
from app.models.lead_submission import LeadSubmission, LeadStatus
from app.schemas.lead import LeadCreate, LeadResponse, LeadUpdate

router = APIRouter()


@router.post("", response_model=LeadResponse, status_code=201)
async def create_lead(data: LeadCreate, db: DbSession) -> LeadSubmission:
    lead = LeadSubmission(**data.model_dump())
    db.add(lead)
    await db.commit()
    await db.refresh(lead)
    return lead


@router.get("", response_model=list[LeadResponse])
async def list_leads(_admin: AdminUser, db: DbSession) -> list[LeadSubmission]:
    result = await db.execute(select(LeadSubmission).order_by(LeadSubmission.created_at.desc()))
    return list(result.scalars().all())


@router.patch("/{lead_id}", response_model=LeadResponse)
async def update_lead(
    lead_id: str, data: LeadUpdate, admin: AdminUser, db: DbSession
) -> LeadSubmission:
    from uuid import UUID

    from app.core.exceptions import NotFoundError

    result = await db.execute(select(LeadSubmission).where(LeadSubmission.id == UUID(lead_id)))
    lead = result.scalar_one_or_none()
    if not lead:
        raise NotFoundError("Lead not found")
    if data.status:
        lead.status = LeadStatus(data.status)
        lead.reviewed_by = admin.id
    await db.commit()
    await db.refresh(lead)
    return lead
