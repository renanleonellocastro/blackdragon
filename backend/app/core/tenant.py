import uuid
from contextvars import ContextVar

from sqlalchemy import event
from sqlalchemy.orm import Session

from app.database import Base

current_tenant_id: ContextVar[uuid.UUID | None] = ContextVar("current_tenant_id", default=None)

# Tables that require tenant filtering
TENANT_SCOPED_TABLES = {
    "users", "properties", "projects", "board_instances",
    "board_instance_channels", "diagrams", "deployments",
    "credentials", "modules",
}


def _has_tenant_id(mapper_class: type) -> bool:
    table_name = getattr(mapper_class, "__tablename__", "")
    return table_name in TENANT_SCOPED_TABLES


@event.listens_for(Session, "do_orm_execute")
def _filter_by_tenant(execute_state):  # type: ignore[no-untyped-def]
    tenant_id = current_tenant_id.get()
    if tenant_id is None:
        return

    if execute_state.is_select:
        for mapper in execute_state.all_mappers:
            if _has_tenant_id(mapper.class_):
                execute_state.statement = execute_state.statement.filter_by(tenant_id=tenant_id)
