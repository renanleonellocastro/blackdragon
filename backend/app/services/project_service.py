"""Project service — CRUD, duplicate, lock/unlock."""
import uuid
from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, ForbiddenError, NotFoundError
from app.models.project import Project, ProjectStatus
from app.models.property import Property
from app.schemas.project import ProjectCreate, ProjectUpdate


async def list_projects(
    db: AsyncSession,
    tenant_id: uuid.UUID,
    property_id: uuid.UUID | None = None,
    status: str | None = None,
) -> list[Project]:
    query = select(Project).where(Project.tenant_id == tenant_id)
    if property_id:
        query = query.where(Project.property_id == property_id)
    if status:
        query = query.where(Project.status == ProjectStatus(status))
    query = query.order_by(Project.updated_at.desc())
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_project(db: AsyncSession, project_id: uuid.UUID, tenant_id: uuid.UUID) -> Project:
    result = await db.execute(
        select(Project).where(Project.id == project_id, Project.tenant_id == tenant_id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise NotFoundError("Project not found")
    return project


async def create_project(db: AsyncSession, data: ProjectCreate, tenant_id: uuid.UUID) -> Project:
    # Verify property belongs to tenant
    prop_result = await db.execute(
        select(Property).where(Property.id == data.property_id, Property.tenant_id == tenant_id)
    )
    if not prop_result.scalar_one_or_none():
        raise NotFoundError("Property not found")

    project = Project(
        id=uuid.uuid4(),
        tenant_id=tenant_id,
        **data.model_dump(),
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project


async def update_project(
    db: AsyncSession, project_id: uuid.UUID, data: ProjectUpdate, tenant_id: uuid.UUID
) -> Project:
    project = await get_project(db, project_id, tenant_id)
    update_data = data.model_dump(exclude_unset=True)
    if "status" in update_data:
        update_data["status"] = ProjectStatus(update_data["status"])
    for field, value in update_data.items():
        setattr(project, field, value)
    await db.commit()
    await db.refresh(project)
    return project


async def delete_project(db: AsyncSession, project_id: uuid.UUID, tenant_id: uuid.UUID) -> None:
    project = await get_project(db, project_id, tenant_id)
    await db.delete(project)
    await db.commit()


async def duplicate_project(
    db: AsyncSession, project_id: uuid.UUID, tenant_id: uuid.UUID
) -> Project:
    source = await get_project(db, project_id, tenant_id)
    new_project = Project(
        id=uuid.uuid4(),
        tenant_id=tenant_id,
        property_id=source.property_id,
        name=f"{source.name} (Copy)",
        description=source.description,
        status=ProjectStatus.DRAFT,
    )
    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)
    return new_project


async def lock_project(
    db: AsyncSession, project_id: uuid.UUID, user_id: uuid.UUID, tenant_id: uuid.UUID
) -> Project:
    project = await get_project(db, project_id, tenant_id)
    if project.is_locked and project.locked_by != user_id:
        raise ConflictError("Project is locked by another user")
    project.is_locked = True
    project.locked_by = user_id
    project.locked_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(project)
    return project


async def unlock_project(
    db: AsyncSession, project_id: uuid.UUID, user_id: uuid.UUID, tenant_id: uuid.UUID
) -> Project:
    project = await get_project(db, project_id, tenant_id)
    if project.is_locked and project.locked_by != user_id:
        raise ForbiddenError("Cannot unlock project locked by another user")
    project.is_locked = False
    project.locked_by = None
    project.locked_at = None
    await db.commit()
    await db.refresh(project)
    return project


# --- Version Management ---

async def save_version(
    db: AsyncSession,
    project_id: uuid.UUID,
    tenant_id: uuid.UUID,
    user_id: uuid.UUID,
    description: str | None = None,
) -> "ProjectVersion":
    from app.models.diagram import Diagram
    from app.models.project_version import ProjectVersion

    project = await get_project(db, project_id, tenant_id)

    # Get latest version number
    result = await db.execute(
        select(func.coalesce(func.max(ProjectVersion.version_number), 0)).where(
            ProjectVersion.project_id == project_id
        )
    )
    next_version = result.scalar() + 1

    # Snapshot: collect all diagram graph_data for this project
    diagrams_result = await db.execute(
        select(Diagram).where(Diagram.project_id == project_id)
    )
    diagrams = diagrams_result.scalars().all()
    snapshot = {
        "project_name": project.name,
        "diagrams": [
            {"id": str(d.id), "name": d.name, "graph_data": d.graph_data}
            for d in diagrams
        ],
    }

    version = ProjectVersion(
        id=uuid.uuid4(),
        project_id=project_id,
        version_number=next_version,
        description=description,
        snapshot_data=snapshot,
        created_by=user_id,
    )
    db.add(version)
    await db.commit()
    await db.refresh(version)
    return version


async def list_versions(
    db: AsyncSession, project_id: uuid.UUID, tenant_id: uuid.UUID
) -> list["ProjectVersion"]:
    from app.models.project_version import ProjectVersion

    # Ensure tenant owns project
    await get_project(db, project_id, tenant_id)

    result = await db.execute(
        select(ProjectVersion)
        .where(ProjectVersion.project_id == project_id)
        .order_by(ProjectVersion.version_number.desc())
    )
    return list(result.scalars().all())


async def rollback_version(
    db: AsyncSession,
    project_id: uuid.UUID,
    version_number: int,
    tenant_id: uuid.UUID,
) -> "ProjectVersion":
    from app.models.diagram import Diagram
    from app.models.project_version import ProjectVersion

    await get_project(db, project_id, tenant_id)

    result = await db.execute(
        select(ProjectVersion).where(
            ProjectVersion.project_id == project_id,
            ProjectVersion.version_number == version_number,
        )
    )
    version = result.scalar_one_or_none()
    if not version:
        raise NotFoundError("Version not found")

    # Restore diagrams from snapshot
    snapshot = version.snapshot_data
    for diag_data in snapshot.get("diagrams", []):
        diag_result = await db.execute(
            select(Diagram).where(Diagram.id == uuid.UUID(diag_data["id"]))
        )
        diagram = diag_result.scalar_one_or_none()
        if diagram:
            diagram.graph_data = diag_data.get("graph_data")

    await db.commit()
    return version
