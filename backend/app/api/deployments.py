from uuid import UUID

from fastapi import APIRouter

from app.api.deps import CurrentUser, DbSession
from app.schemas.deployment import DeployRequest, DeployResponse, DeploymentStatus
from app.services import deployment_service

router = APIRouter()


@router.post("/{project_id}/deployments", response_model=DeployResponse, status_code=202)
async def create_deployment(
    project_id: str, data: DeployRequest, user: CurrentUser, db: DbSession
) -> DeployResponse:
    return await deployment_service.initiate(
        db, data.artifact_id, data.board_instance_id, UUID(project_id), user.id, user.tenant_id
    )


@router.get("/{project_id}/deployments", response_model=list[DeploymentStatus])
async def list_deployments(project_id: str, user: CurrentUser, db: DbSession) -> list:
    return await deployment_service.list_deployments(db, UUID(project_id), user.tenant_id)


@router.get("/{project_id}/deployments/{deployment_id}", response_model=DeploymentStatus)
async def get_deployment(
    project_id: str, deployment_id: str, user: CurrentUser, db: DbSession
) -> DeploymentStatus:
    return await deployment_service.get_deployment(db, UUID(deployment_id), user.tenant_id)


@router.post("/{project_id}/deployments/{deployment_id}/cancel", response_model=DeploymentStatus)
async def cancel_deployment(
    project_id: str, deployment_id: str, user: CurrentUser, db: DbSession
) -> DeploymentStatus:
    return await deployment_service.cancel_deployment(db, UUID(deployment_id), user.tenant_id)
