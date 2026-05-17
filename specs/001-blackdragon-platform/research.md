# Research: BlackDragon SaaS Platform

**Feature**: 001-blackdragon-platform
**Date**: 2026-05-16
**Status**: Complete

## R1: Vue Flow for Visual Programming Editor

**Decision**: Use Vue Flow (v1.x) as the foundation for the blocks-and-wires visual editor.

**Rationale**:
- Vue Flow is the Vue 3 port of React Flow, the most widely adopted node-based editor library.
- Provides built-in support for custom nodes, edges, handles (ports), minimap, controls, background grid, and viewport manipulation (zoom, pan).
- Custom node components are standard Vue 3 SFCs — no proprietary abstraction layer.
- Handles (input/output ports) support typed connections via `isValidConnection` callback, enabling port compatibility validation.
- Supports nested groups (used for future module/subprogram support).
- State management integrates cleanly with Pinia via `useVueFlow()` composable.
- Active maintenance, TypeScript support, and growing ecosystem.

**Alternatives considered**:
- **Rete.js**: More framework-agnostic but heavier API surface, less Vue-native. Steeper learning curve for custom node styling.
- **JointJS / mxGraph**: Enterprise-grade but complex, large bundle size, and licensing considerations.
- **Custom canvas implementation**: Maximum control but massive development effort for basic features (zoom, pan, hit testing, drag).

**Key implementation patterns**:
- Define each block type as a custom Vue Flow node component with typed handles.
- Use `Position.Left` for inputs, `Position.Right` for outputs.
- Store graph state as Vue Flow's `Node[]` and `Edge[]` arrays, serialized to JSON for persistence.
- Use `onConnect` event with validation to enforce port type compatibility.
- Implement auto-save via `watch()` on graph changes with debounced API calls.

---

## R2: ESPHome YAML Generation from Visual Graphs

**Decision**: Implement a multi-stage compiler pipeline with an intermediate representation (IR) that decouples visual graph structure from target-specific code generation.

**Rationale**:
- ESPHome configuration is declarative YAML with specific component schemas (binary_sensor, switch, output, lambda, automation).
- A direct graph-to-YAML translation would tightly couple the visual editor's data model to ESPHome's schema, making it impossible to add future generators (Home Assistant, custom platforms).
- An IR provides a normalized representation of automation logic that can be optimized before code generation.
- The IR also enables validation at a semantic level (type checking, cycle detection, resource conflicts) before attempting generation.

**Alternatives considered**:
- **Direct graph-to-YAML**: Simpler for MVP but creates technical debt; rejected due to architectural requirement for multiple generators.
- **AST-based approach**: Too heavyweight; ESPHome YAML is configuration, not code. IR is sufficient.

**Key implementation patterns**:
- **Visual Graph JSON**: Serialized Vue Flow state (nodes with properties, edges with source/target).
- **Validator**: Checks connectivity (no dangling ports), GPIO conflicts, type compatibility, cycle detection for combinational logic.
- **IR**: Normalized graph of `IRNode` objects with resolved types, validated connections, and computed execution order (topological sort).
- **Optimizer**: Dead-node elimination, constant folding (e.g., `AND(TRUE, x) → x`), redundant wire removal.
- **ESPHome Generator**: Walks IR nodes, maps to ESPHome component definitions:
  - `DigitalInput` → `binary_sensor:` with `platform: gpio`, pin config, filters
  - `DigitalOutput` → `switch:` + `output:` with `platform: gpio`, pin config
  - `AND/OR/NOT/XOR` → `lambda:` expressions or `template:` sensors
  - `Timer/Delay` → `on_...:` actions with `delay:` directives
  - `Debounce` → `filters: - delayed_on_off:` on binary sensors
- **PyYAML**: Use `yaml.dump()` with custom representers for clean YAML output (no Python-specific tags).

**ESPHome YAML structure per board**:
```yaml
esphome:
  name: {board_instance_name}
  platform: ESP32
  board: {board_model}

wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password

api:
  password: !secret api_password

ota:
  password: !secret ota_password

binary_sensor:
  - platform: gpio
    pin:
      number: {gpio_pin}
      mode: INPUT_PULLUP
      inverted: {inverted}
    name: "{input_name}"
    filters:
      - delayed_on_off: {debounce_ms}ms

switch:
  - platform: gpio
    pin: {gpio_pin}
    name: "{output_name}"
    id: {output_id}
```

---

## R3: Multi-Tenant Architecture with PostgreSQL

**Decision**: Implement tenant isolation using a shared-database, shared-schema approach with a `tenant_id` foreign key on all tenant-scoped tables, enforced at the query layer via SQLAlchemy events.

**Rationale**:
- Shared-schema is the simplest multi-tenant pattern for the expected scale (hundreds of tenants, not thousands).
- A `tenant_id` column on every tenant-scoped table enables row-level filtering.
- SQLAlchemy 2.0 session events (`do_orm_execute`) can automatically inject `WHERE tenant_id = :current_tenant` on all queries, preventing accidental cross-tenant access.
- PostgreSQL Row Level Security (RLS) can be added later as a defense-in-depth layer without schema changes.

**Alternatives considered**:
- **Schema-per-tenant**: Stronger isolation but operationally complex (migration per schema, connection pool per tenant). Overkill for initial scale.
- **Database-per-tenant**: Maximum isolation but extreme operational overhead. Not warranted.

**Key implementation patterns**:
- `TenantMixin` base class adds `tenant_id: UUID` column to all tenant-scoped models.
- `TenantMiddleware` extracts tenant context from the authenticated user's JWT claims.
- SQLAlchemy session event filters all SELECT/UPDATE/DELETE queries by `tenant_id`.
- INSERT operations automatically set `tenant_id` from the current context.
- Admin role bypasses tenant filtering (explicit flag in the dependency injection).
- Integration tests verify cross-tenant isolation with two test tenants.

---

## R4: JWT Authentication with FastAPI

**Decision**: Use JWT bearer tokens with short-lived access tokens and optional refresh tokens, implemented via FastAPI dependency injection.

**Rationale**:
- JWT is stateless and scales horizontally without shared session storage.
- FastAPI's `Depends()` system provides clean middleware for auth extraction.
- python-jose handles JWT encoding/decoding with standard algorithms (HS256 for MVP, RS256 upgrade path).
- Passlib with bcrypt provides secure password hashing.

**Alternatives considered**:
- **Session-based auth**: Requires server-side session storage (Redis). Adds infrastructure complexity for the MVP.
- **OAuth2 / OpenID Connect**: Over-engineered for initial deployment where the platform is the only identity provider.

**Key implementation patterns**:
- `POST /api/auth/login` → validates credentials, returns `{ access_token, token_type }`.
- `POST /api/auth/register` → creates user + tenant, returns tokens.
- Access token contains: `sub` (user_id), `tenant_id`, `role`, `exp`.
- Token expiry: 30 minutes (access), 7 days (refresh).
- `get_current_user` dependency extracts and validates JWT from `Authorization: Bearer` header.
- `require_role("admin")` dependency wraps `get_current_user` with role check.

---

## R5: OTA Deployment via ESPHome

**Decision**: Invoke ESPHome's OTA upload mechanism from the backend to push compiled configurations to ESP32 devices.

**Rationale**:
- ESPHome natively supports OTA updates over WiFi. Devices running ESPHome firmware listen for upload connections on a configurable port.
- The platform can compile YAML, invoke `esphome run` (or use ESPHome's Python API) to compile firmware and upload it to the target device.
- This requires the backend to have network access to the target ESP32 devices (directly or via VPN/tunnel).

**Alternatives considered**:
- **Client-side deployment**: User downloads YAML and runs ESPHome locally. Simpler but defeats the purpose of an integrated platform.
- **MQTT-based OTA**: Custom protocol. Unnecessary when ESPHome's native OTA works.

**Key implementation patterns**:
- Backend stores device network addresses (IP/hostname) as encrypted credentials per board instance.
- Deployment service writes compiled YAML to a temporary directory, invokes ESPHome CLI subprocess.
- Deployment runs asynchronously (background task via FastAPI BackgroundTasks or Celery for production).
- WebSocket or polling endpoint provides deployment progress to the frontend.
- Deployment status and logs stored in `deployment` table for audit.

---

## R6: BlackDragon Design System with Tailwind CSS

**Decision**: Extend Tailwind CSS with custom design tokens matching the BlackDragon brand identity (ultra-dark, metallic, industrial aesthetic) and build a reusable Vue component library.

**Rationale**:
- Tailwind's configuration system (`tailwind.config.ts`) supports custom colors, shadows, fonts, and animations as first-class tokens.
- Building a component library (BdButton, BdCard, BdInput, etc.) ensures consistency across all views and enforces the constitution's UX consistency principle.
- The dark-mode-only constraint simplifies the design system (no light/dark toggle needed).

**Key implementation patterns**:
- Custom Tailwind theme extends `colors` with BlackDragon palette (`bd-bg-primary: #050505`, etc.).
- Custom shadows: `bd-glow` for subtle metallic glow effects, `bd-emboss` for raised card surfaces.
- Custom gradients: `bd-metallic` for linear gradients simulating brushed metal.
- All components use `Bd` prefix (e.g., `BdButton`, `BdCard`) to distinguish from third-party components.
- Component props standardize variants: `variant="primary" | "secondary" | "ghost" | "danger"`.
- Visual editor nodes use a distinct `BdNode` base component with colored port indicators and selection glow.

**Color tokens**:
```typescript
colors: {
  'bd-bg': { primary: '#050505', secondary: '#0A0A0A', panel: '#111111', surface: '#181818' },
  'bd-border': '#2A2A2A',
  'bd-text': { primary: '#E5E5E5', secondary: '#9CA3AF' },
  'bd-accent': { DEFAULT: '#6B7280', highlight: '#D1D5DB' },
  'bd-success': '#10B981',
  'bd-warning': '#F59E0B',
  'bd-error': '#EF4444',
}
```

---

## R7: SQLAlchemy 2.0 with Alembic Migrations

**Decision**: Use SQLAlchemy 2.0 ORM with the new 2.0-style query API and Alembic for schema migrations.

**Rationale**:
- SQLAlchemy 2.0 provides full type annotation support, async session support, and cleaner query patterns.
- Alembic auto-generates migration scripts from model changes, reducing manual SQL.
- Mapped columns with `Mapped[type]` provide IDE autocompletion and mypy compatibility.

**Alternatives considered**:
- **Tortoise ORM / SQLModel**: Less mature, smaller ecosystem. SQLAlchemy is the standard for production Python.
- **Raw SQL with asyncpg**: Maximum performance but sacrifices ORM benefits (migrations, relationships, validation).

**Key implementation patterns**:
- `DeclarativeBase` with `MappedAsDataclass` for model definitions.
- Async session factory via `create_async_engine` + `async_sessionmaker`.
- Repository pattern not used — services query via session directly (per constitution: no unnecessary abstractions).
- Alembic configured for async with `run_async()` in `env.py`.

---

## R8: Compiler Node Type System

**Decision**: Implement a type-safe node registry where each node type defines its ports (name, direction, data type), default properties, and validation rules.

**Rationale**:
- The visual editor and compiler both need to know the port schema for each node type.
- A shared registry ensures the frontend palette, the editor's connection validation, and the compiler's semantic analysis all agree on node definitions.
- The registry is extensible — future node types (analog I/O, PID controllers, schedulers) register via the same interface.

**Key implementation patterns**:
- `NodeDefinition` dataclass: `type`, `category`, `ports: list[PortDefinition]`, `properties: list[PropertyDefinition]`, `icon`, `color`.
- `PortDefinition`: `name`, `direction` (input/output), `data_type` (boolean/number/trigger), `required`.
- `PropertyDefinition`: `name`, `type`, `default`, `validation` (min/max/enum).
- Node registry exposed via API endpoint (`GET /api/nodes/definitions`) so frontend dynamically builds the palette.
- Compiler validates connections by checking `source.port.data_type == target.port.data_type`.

**MVP node definitions**:

| Node | Category | Inputs | Outputs | Properties |
|------|----------|--------|---------|------------|
| Digital Input | Hardware | — | signal (bool) | gpio_pin, pull_mode, inverted, debounce_ms, name |
| Digital Output | Hardware | signal (bool) | — | gpio_pin, inverted, name |
| Constant True | Constant | — | value (bool) | — |
| Constant False | Constant | — | value (bool) | — |
| AND | Logic | a (bool), b (bool) | out (bool) | — |
| OR | Logic | a (bool), b (bool) | out (bool) | — |
| NOT | Logic | in (bool) | out (bool) | — |
| XOR | Logic | a (bool), b (bool) | out (bool) | — |
| Timer | Timing | trigger (bool) | out (bool) | duration_ms |
| Delay | Timing | in (bool) | out (bool) | delay_ms |
| Edge Detector | Timing | in (bool) | rising (bool), falling (bool) | edge_type |
| Debounce | Timing | in (bool) | out (bool) | delay_ms |
