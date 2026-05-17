import uuid

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from app.api.deps import CurrentUser, DbSession
from app.compiler.nodes.registry import get_all_definitions
from app.compiler.pipeline import compile_graph, validate_only
from app.core.exceptions import NotFoundError
from app.models.compilation_artifact import CompilationArtifact
from app.models.diagram import Diagram
from app.schemas.compiler import (
    ArtifactResponse,
    CompileRequest,
    CompileResponse,
    ValidationErrorItem,
    ValidationResultSchema,
)

from sqlalchemy import select

router = APIRouter()


@router.post("/compile", response_model=CompileResponse)
async def compile(data: CompileRequest, user: CurrentUser, db: DbSession) -> CompileResponse:
    # Load diagram
    result = await db.execute(
        select(Diagram).where(Diagram.id == data.diagram_id, Diagram.tenant_id == user.tenant_id)
    )
    diagram = result.scalar_one_or_none()
    if not diagram:
        raise NotFoundError("Diagram not found")

    compile_result = compile_graph(diagram.graph_data, data.context)

    validation = ValidationResultSchema(
        valid=compile_result.validation.valid,
        errors=[ValidationErrorItem(node_id=e.node_id, message=e.message, severity=e.severity) for e in compile_result.validation.errors],
        warnings=[ValidationErrorItem(node_id=e.node_id, message=e.message, severity=e.severity) for e in compile_result.validation.warnings],
    )

    artifact_id = None
    if compile_result.success and compile_result.output:
        artifact = CompilationArtifact(
            id=uuid.uuid4(),
            tenant_id=user.tenant_id,
            diagram_id=diagram.id,
            target=compile_result.target,
            output=compile_result.output,
            node_count=diagram.node_count,
            edge_count=diagram.edge_count,
        )
        db.add(artifact)
        await db.commit()
        artifact_id = artifact.id

    return CompileResponse(
        success=compile_result.success,
        validation=validation,
        output=compile_result.output,
        artifact_id=artifact_id,
    )


@router.post("/validate", response_model=ValidationResultSchema)
async def validate(data: CompileRequest, user: CurrentUser, db: DbSession) -> ValidationResultSchema:
    result = await db.execute(
        select(Diagram).where(Diagram.id == data.diagram_id, Diagram.tenant_id == user.tenant_id)
    )
    diagram = result.scalar_one_or_none()
    if not diagram:
        raise NotFoundError("Diagram not found")

    validation = validate_only(diagram.graph_data)
    return ValidationResultSchema(
        valid=validation.valid,
        errors=[ValidationErrorItem(node_id=e.node_id, message=e.message, severity=e.severity) for e in validation.errors],
        warnings=[ValidationErrorItem(node_id=e.node_id, message=e.message, severity=e.severity) for e in validation.warnings],
    )


@router.get("/artifacts/{artifact_id}", response_model=ArtifactResponse)
async def get_artifact(artifact_id: str, user: CurrentUser, db: DbSession) -> ArtifactResponse:
    result = await db.execute(
        select(CompilationArtifact).where(
            CompilationArtifact.id == uuid.UUID(artifact_id),
            CompilationArtifact.tenant_id == user.tenant_id,
        )
    )
    artifact = result.scalar_one_or_none()
    if not artifact:
        raise NotFoundError("Artifact not found")
    return artifact


@router.get("/artifacts/{artifact_id}/download")
async def download_artifact(artifact_id: str, user: CurrentUser, db: DbSession) -> PlainTextResponse:
    result = await db.execute(
        select(CompilationArtifact).where(
            CompilationArtifact.id == uuid.UUID(artifact_id),
            CompilationArtifact.tenant_id == user.tenant_id,
        )
    )
    artifact = result.scalar_one_or_none()
    if not artifact:
        raise NotFoundError("Artifact not found")
    return PlainTextResponse(
        content=artifact.output,
        media_type="text/yaml",
        headers={"Content-Disposition": f"attachment; filename=esphome_{artifact_id}.yaml"},
    )


@router.get("/node-definitions")
async def get_node_definitions() -> list[dict]:
    defs = get_all_definitions()
    return [
        {
            "type": d.type,
            "label": d.label,
            "category": d.category,
            "inputs": [{"id": p.id, "label": p.label, "type": p.type} for p in d.inputs],
            "outputs": [{"id": p.id, "label": p.label, "type": p.type} for p in d.outputs],
            "properties": [{"key": p.key, "label": p.label, "type": p.type, "default": p.default} for p in d.properties],
        }
        for d in defs
    ]
