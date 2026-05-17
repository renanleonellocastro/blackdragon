"""Diagram service — CRUD, save graph_data, save draft."""
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.diagram import Diagram, DiagramLayer
from app.schemas.diagram import DiagramCreate, DiagramUpdate, DraftSave


async def list_diagrams(db: AsyncSession, project_id: uuid.UUID, tenant_id: uuid.UUID) -> list[Diagram]:
    result = await db.execute(
        select(Diagram)
        .where(Diagram.project_id == project_id, Diagram.tenant_id == tenant_id)
        .order_by(Diagram.name)
    )
    return list(result.scalars().all())


async def get_diagram(
    db: AsyncSession, diagram_id: uuid.UUID, project_id: uuid.UUID, tenant_id: uuid.UUID
) -> Diagram:
    result = await db.execute(
        select(Diagram).where(
            Diagram.id == diagram_id,
            Diagram.project_id == project_id,
            Diagram.tenant_id == tenant_id,
        )
    )
    diagram = result.scalar_one_or_none()
    if not diagram:
        raise NotFoundError("Diagram not found")
    return diagram


async def create_diagram(
    db: AsyncSession, data: DiagramCreate, project_id: uuid.UUID, tenant_id: uuid.UUID
) -> Diagram:
    diagram = Diagram(
        id=uuid.uuid4(),
        tenant_id=tenant_id,
        project_id=project_id,
        name=data.name,
        layer=DiagramLayer(data.layer),
        board_instance_id=data.board_instance_id,
        graph_data={"nodes": [], "edges": []},
    )
    db.add(diagram)
    await db.commit()
    await db.refresh(diagram)
    return diagram


async def save_diagram(
    db: AsyncSession, diagram_id: uuid.UUID, data: DiagramUpdate,
    project_id: uuid.UUID, tenant_id: uuid.UUID,
) -> Diagram:
    diagram = await get_diagram(db, diagram_id, project_id, tenant_id)
    if data.name is not None:
        diagram.name = data.name
    if data.graph_data is not None:
        diagram.graph_data = data.graph_data
        diagram.draft_data = None  # Clear draft on full save
        nodes = data.graph_data.get("nodes", [])
        edges = data.graph_data.get("edges", [])
        diagram.node_count = len(nodes)
        diagram.edge_count = len(edges)
    if data.viewport is not None:
        diagram.viewport = data.viewport
    await db.commit()
    await db.refresh(diagram)
    return diagram


async def save_draft(
    db: AsyncSession, diagram_id: uuid.UUID, data: DraftSave,
    project_id: uuid.UUID, tenant_id: uuid.UUID,
) -> Diagram:
    diagram = await get_diagram(db, diagram_id, project_id, tenant_id)
    diagram.draft_data = data.draft_data
    if data.viewport is not None:
        diagram.viewport = data.viewport
    await db.commit()
    await db.refresh(diagram)
    return diagram


async def delete_diagram(
    db: AsyncSession, diagram_id: uuid.UUID, project_id: uuid.UUID, tenant_id: uuid.UUID
) -> None:
    diagram = await get_diagram(db, diagram_id, project_id, tenant_id)
    await db.delete(diagram)
    await db.commit()
