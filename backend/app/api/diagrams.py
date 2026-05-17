from uuid import UUID

from fastapi import APIRouter

from app.api.deps import CurrentUser, DbSession
from app.schemas.diagram import DiagramCreate, DiagramResponse, DiagramSummary, DiagramUpdate, DraftSave
from app.services import diagram_service

router = APIRouter()


@router.get("/{project_id}/diagrams", response_model=list[DiagramSummary])
async def list_diagrams(project_id: str, user: CurrentUser, db: DbSession) -> list:
    diagrams = await diagram_service.list_diagrams(db, UUID(project_id), user.tenant_id)
    result = []
    for d in diagrams:
        summary = DiagramSummary.model_validate(d)
        summary.has_draft = d.draft_data is not None
        result.append(summary)
    return result


@router.post("/{project_id}/diagrams", response_model=DiagramResponse, status_code=201)
async def create_diagram(project_id: str, data: DiagramCreate, user: CurrentUser, db: DbSession) -> DiagramResponse:
    return await diagram_service.create_diagram(db, data, UUID(project_id), user.tenant_id)


@router.get("/{project_id}/diagrams/{diagram_id}", response_model=DiagramResponse)
async def get_diagram(project_id: str, diagram_id: str, user: CurrentUser, db: DbSession) -> DiagramResponse:
    return await diagram_service.get_diagram(db, UUID(diagram_id), UUID(project_id), user.tenant_id)


@router.put("/{project_id}/diagrams/{diagram_id}", response_model=DiagramResponse)
async def save_diagram(
    project_id: str, diagram_id: str, data: DiagramUpdate, user: CurrentUser, db: DbSession
) -> DiagramResponse:
    return await diagram_service.save_diagram(db, UUID(diagram_id), data, UUID(project_id), user.tenant_id)


@router.post("/{project_id}/diagrams/{diagram_id}/draft", response_model=DiagramResponse)
async def save_draft(
    project_id: str, diagram_id: str, data: DraftSave, user: CurrentUser, db: DbSession
) -> DiagramResponse:
    return await diagram_service.save_draft(db, UUID(diagram_id), data, UUID(project_id), user.tenant_id)


@router.delete("/{project_id}/diagrams/{diagram_id}", status_code=204)
async def delete_diagram(project_id: str, diagram_id: str, user: CurrentUser, db: DbSession) -> None:
    await diagram_service.delete_diagram(db, UUID(diagram_id), UUID(project_id), user.tenant_id)
