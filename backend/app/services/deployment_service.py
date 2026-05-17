"""Deployment service — initiate OTA, track progress, update status."""
import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, NotFoundError, ValidationError
from app.models.board_instance import BoardInstance
from app.models.compilation_artifact import CompilationArtifact
from app.models.deployment import Deployment, DeploymentStatus


async def initiate(
    db: AsyncSession,
    artifact_id: uuid.UUID,
    board_instance_id: uuid.UUID,
    project_id: uuid.UUID,
    user_id: uuid.UUID,
    tenant_id: uuid.UUID,
) -> Deployment:
    # Validate artifact
    artifact = await db.execute(
        select(CompilationArtifact).where(
            CompilationArtifact.id == artifact_id,
            CompilationArtifact.tenant_id == tenant_id,
        )
    )
    if not artifact.scalar_one_or_none():
        raise NotFoundError("Artifact not found")

    # Validate board instance
    board_result = await db.execute(
        select(BoardInstance).where(
            BoardInstance.id == board_instance_id,
            BoardInstance.tenant_id == tenant_id,
        )
    )
    board = board_result.scalar_one_or_none()
    if not board:
        raise NotFoundError("Board instance not found")
    if not board.device_address:
        raise ValidationError("Board has no device address configured")

    # Check no active deployment for this board
    active = await db.execute(
        select(Deployment).where(
            Deployment.board_instance_id == board_instance_id,
            Deployment.status.in_([DeploymentStatus.PENDING, DeploymentStatus.UPLOADING]),
        )
    )
    if active.scalar_one_or_none():
        raise ConflictError("Deployment already in progress for this board")

    deployment = Deployment(
        id=uuid.uuid4(),
        tenant_id=tenant_id,
        project_id=project_id,
        board_instance_id=board_instance_id,
        artifact_id=artifact_id,
        deployed_by=user_id,
        status=DeploymentStatus.PENDING,
    )
    db.add(deployment)
    await db.commit()
    await db.refresh(deployment)

    # In production, this would trigger an async task for OTA upload
    # For now, we just create the deployment record

    return deployment


async def list_deployments(
    db: AsyncSession, project_id: uuid.UUID, tenant_id: uuid.UUID
) -> list[Deployment]:
    result = await db.execute(
        select(Deployment)
        .where(Deployment.project_id == project_id, Deployment.tenant_id == tenant_id)
        .order_by(Deployment.started_at.desc())
    )
    return list(result.scalars().all())


async def get_deployment(
    db: AsyncSession, deployment_id: uuid.UUID, tenant_id: uuid.UUID
) -> Deployment:
    result = await db.execute(
        select(Deployment).where(
            Deployment.id == deployment_id, Deployment.tenant_id == tenant_id
        )
    )
    deployment = result.scalar_one_or_none()
    if not deployment:
        raise NotFoundError("Deployment not found")
    return deployment


async def cancel_deployment(
    db: AsyncSession, deployment_id: uuid.UUID, tenant_id: uuid.UUID
) -> Deployment:
    deployment = await get_deployment(db, deployment_id, tenant_id)
    if deployment.status not in [DeploymentStatus.PENDING, DeploymentStatus.UPLOADING]:
        raise ConflictError("Cannot cancel completed deployment")
    deployment.status = DeploymentStatus.CANCELLED
    deployment.completed_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(deployment)
    return deployment
