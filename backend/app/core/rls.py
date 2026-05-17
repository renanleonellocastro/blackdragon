"""RLS policies for tenant isolation.

Note: This will be applied as an Alembic migration once the initial migration
establishes tenant-scoped tables. The policies act as defense-in-depth alongside
the SQLAlchemy event-based tenant filtering.
"""

TENANT_SCOPED_TABLES = [
    "users",
    "properties",
    "projects",
    "board_instances",
    "board_instance_channels",
    "diagrams",
    "deployments",
    "credentials",
    "modules",
]

RLS_SETUP_SQL = """
-- Enable RLS on tenant-scoped tables
{enable_rls}

-- Create policies for app role
{policies}
"""


def generate_rls_sql() -> str:
    enable_rls = "\n".join(
        f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY;" for table in TENANT_SCOPED_TABLES
    )
    policies = "\n".join(
        f"""CREATE POLICY tenant_isolation_{table} ON {table}
    USING (tenant_id = current_setting('app.current_tenant_id')::uuid);"""
        for table in TENANT_SCOPED_TABLES
    )
    return RLS_SETUP_SQL.format(enable_rls=enable_rls, policies=policies)
