"""Audit service — log and query actions."""
import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit_log import AuditLog


async def log_action(
    db: AsyncSession,
    action: str,
    resource_type: str,
    resource_id: str | None = None,
    user_id: uuid.UUID | None = None,
    tenant_id: uuid.UUID | None = None,
    details: dict[str, Any] | None = None,
    ip_address: str | None = None,
) -> AuditLog:
    entry = AuditLog(
        id=uuid.uuid4(),
        tenant_id=tenant_id,
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details,
        ip_address=ip_address,
    )
    db.add(entry)
    await db.flush()
    return entry


async def query_logs(
    db: AsyncSession,
    tenant_id: uuid.UUID | None = None,
    action: str | None = None,
    limit: int = 100,
) -> list[AuditLog]:
    query = select(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit)
    if tenant_id:
        query = query.where(AuditLog.tenant_id == tenant_id)
    if action:
        query = query.where(AuditLog.action == action)
    result = await db.execute(query)
    return list(result.scalars().all())
