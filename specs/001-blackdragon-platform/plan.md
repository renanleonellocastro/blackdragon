# Implementation Plan: BlackDragon SaaS Platform

**Branch**: `001-blackdragon-platform` | **Date**: 2026-05-16 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/001-blackdragon-platform/spec.md`

## Summary

BlackDragon is a full-stack SaaS web application that serves as the company's public website and a multi-tenant client portal with a visual programming environment for smart home automation. The platform enables clients to design automation logic using a drag-and-drop blocks-and-wires editor, compile visual diagrams into ESPHome YAML and Home Assistant configuration, and deploy generated artifacts to ESP32-based I/O boards via OTA. The implementation uses a Vue 3 + TypeScript frontend with Vue Flow for the visual editor, a FastAPI + Python backend with a modular compiler pipeline, PostgreSQL for persistence, and Docker Compose for infrastructure.

## Technical Context

**Language/Version**: Python 3.12+ (backend), TypeScript 5.x (frontend)

**Primary Dependencies**:
- Frontend: Vue 3, Vite, Vue Flow, Pinia, Vue Router, Tailwind CSS, Lucide Icons
- Backend: FastAPI, Pydantic, SQLAlchemy 2.0, Alembic, PyYAML, Passlib, python-jose (JWT)

**Storage**: PostgreSQL 16 with Alembic migrations

**Testing**:
- Frontend: Vitest (unit), Playwright (e2e)
- Backend: pytest, pytest-asyncio, httpx (integration)
- Compiler: pytest with YAML snapshot tests

**Target Platform**: Web application (modern browsers), Linux containers (Docker)

**Project Type**: Web application (frontend + backend + compiler)

**Performance Goals**: <2s page load, <100ms editor interactions, <500ms API p95, <3s compilation for 50 blocks, 100 concurrent users

**Constraints**: Multi-tenant data isolation, RBAC enforcement, <2s save/load for 200-block projects, auto-save every 60s

**Scale/Scope**: 100 concurrent users, 50 properties per tenant, 20 projects per property, ~15 public pages + ~10 portal views

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Code Quality — PASS
- ESLint + Prettier enforced for frontend TypeScript; Ruff + Black for backend Python.
- TypeScript strict mode enabled. Python type hints mandatory with mypy.
- Single-responsibility enforced through modular architecture: separate packages for API, services, compiler, models.
- No dead code tolerance enforced via linter configs.

### II. Testing Standards (NON-NEGOTIABLE) — PASS
- Unit tests: Vitest (frontend), pytest (backend). 80%+ coverage target per module.
- Integration tests: httpx TestClient for API endpoints, Playwright for e2e flows.
- Compiler snapshot tests: deterministic YAML output comparison.
- Test naming convention: `test_[unit]_[scenario]_[expected_result]` (Python), `describe/it` (TypeScript).
- No flaky tests — all deterministic, no network calls in unit tests.

### III. User Experience Consistency — PASS
- BlackDragon design system with Tailwind custom tokens: colors, shadows, gradients, typography.
- Reusable Vue component library: buttons, cards, inputs, modals, tables, navigation.
- Error/loading/empty states handled via standard component wrappers.
- WCAG 2.1 AA target: keyboard navigation, screen reader labels, contrast ratios.
- Responsive breakpoints validated for all public pages and portal views.

### IV. Performance Requirements — PASS
- Page load <2s: Vite code splitting, lazy-loaded routes, optimized assets.
- Editor interactions <100ms: Vue Flow handles canvas operations natively.
- API p95 <500ms: async FastAPI handlers, indexed queries, connection pooling.
- Bundle size tracked via Vite build analysis.
- Database queries reviewed for N+1 via SQLAlchemy eager loading strategies.

### Quality Gates — PASS
All six gates (Lint, Type, Test, Performance, UX, Code Review) mapped to CI pipeline steps.

### Development Workflow — PASS
Feature branch workflow, conventional commits, PR references to tasks/issues.

**GATE RESULT: ALL PASS — Proceed to Phase 0**

## Project Structure

### Documentation (this feature)

```text
specs/001-blackdragon-platform/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
└── tasks.md
```

### Source Code (repository root)

```text
frontend/
├── index.html
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── vite.config.ts
├── public/
│   ├── favicon.ico
│   └── logo.svg
├── src/
│   ├── main.ts
│   ├── App.vue
│   ├── router/
│   │   └── index.ts
│   ├── stores/
│   │   ├── auth.ts
│   │   ├── project.ts
│   │   ├── editor.ts
│   │   └── board.ts
│   ├── composables/
│   │   ├── useAuth.ts
│   │   └── useAutoSave.ts
│   ├── components/
│   │   ├── ui/               # Design system components
│   │   │   ├── BdButton.vue
│   │   │   ├── BdCard.vue
│   │   │   ├── BdInput.vue
│   │   │   ├── BdModal.vue
│   │   │   ├── BdTable.vue
│   │   │   ├── BdStatusIndicator.vue
│   │   │   ├── BdLogo.vue           # Logo component with size variants
│   │   │   └── BdCircuitPattern.vue  # SVG circuit-board decorative pattern
│   │   ├── layout/
│   │   │   ├── AppHeader.vue
│   │   │   ├── AppSidebar.vue
│   │   │   ├── AppFooter.vue
│   │   │   └── PortalLayout.vue
│   │   ├── editor/
│   │   │   ├── EditorCanvas.vue
│   │   │   ├── NodePalette.vue
│   │   │   ├── PropertiesPanel.vue
│   │   │   └── nodes/
│   │   │       ├── DigitalInputNode.vue
│   │   │       ├── DigitalOutputNode.vue
│   │   │       ├── LogicGateNode.vue
│   │   │       ├── TimerNode.vue
│   │   │       ├── DelayNode.vue
│   │   │       ├── EdgeDetectorNode.vue
│   │   │       ├── DebounceNode.vue
│   │   │       └── ConstantNode.vue
│   │   └── boards/
│   │       ├── BoardSelector.vue
│   │       ├── BoardConfigurator.vue
│   │       └── IoChannelEditor.vue
│   ├── views/
│   │   ├── public/
│   │   │   ├── HomePage.vue
│   │   │   ├── AboutPage.vue
│   │   │   ├── ProductsPage.vue
│   │   │   ├── SolutionsPage.vue
│   │   │   ├── ProjectsPage.vue
│   │   │   ├── BlogPage.vue
│   │   │   └── ContactPage.vue
│   │   ├── auth/
│   │   │   ├── LoginPage.vue
│   │   │   └── RegisterPage.vue
│   │   └── portal/
│   │       ├── DashboardPage.vue
│   │       ├── ProjectListPage.vue
│   │       ├── ProjectEditorPage.vue
│   │       ├── BoardCatalogPage.vue
│   │       ├── YamlPreviewPage.vue
│   │       ├── DeploymentPage.vue
│   │       ├── ProfilePage.vue
│   │       └── admin/
│   │           ├── UsersPage.vue
│   │           ├── ClientsPage.vue
│   │           └── BoardManagementPage.vue
│   ├── services/
│   │   ├── api.ts            # HTTP client
│   │   ├── auth.service.ts
│   │   ├── project.service.ts
│   │   ├── board.service.ts
│   │   ├── compiler.service.ts
│   │   └── deployment.service.ts
│   ├── types/
│   │   ├── api.ts
│   │   ├── editor.ts
│   │   ├── board.ts
│   │   └── project.ts
│   └── assets/
│       └── styles/
│           └── main.css
└── tests/
    ├── unit/
    │   ├── components/
    │   ├── stores/
    │   └── services/
    └── e2e/
        ├── public-website.spec.ts
        ├── auth.spec.ts
        ├── project-management.spec.ts
        └── visual-editor.spec.ts

backend/
├── pyproject.toml
├── alembic.ini
├── alembic/
│   ├── env.py
│   └── versions/
├── app/
│   ├── __init__.py
│   ├── main.py               # FastAPI app factory
│   ├── config.py              # Environment config
│   ├── database.py            # SQLAlchemy engine + session
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── tenant.py
│   │   ├── property.py
│   │   ├── project.py
│   │   ├── project_version.py
│   │   ├── board_model.py
│   │   ├── board_instance.py
│   │   ├── diagram.py
│   │   ├── compilation_artifact.py
│   │   ├── deployment.py
│   │   ├── credential.py
│   │   ├── audit_log.py
│   │   ├── blog_post.py
│   │   ├── module.py
│   │   └── lead_submission.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── board.py
│   │   ├── diagram.py
│   │   ├── compiler.py
│   │   ├── deployment.py
│   │   ├── blog.py
│   │   └── lead.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py            # Dependency injection (auth, db session, tenant)
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── properties.py
│   │   ├── projects.py
│   │   ├── boards.py
│   │   ├── diagrams.py
│   │   ├── compiler.py
│   │   ├── deployments.py
│   │   ├── leads.py
│   │   ├── blog.py
│   │   └── admin.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── project_service.py
│   │   ├── board_service.py
│   │   ├── diagram_service.py
│   │   ├── deployment_service.py
│   │   ├── blog_service.py
│   │   └── audit_service.py
│   ├── compiler/
│   │   ├── __init__.py
│   │   ├── pipeline.py        # Orchestrates compilation stages
│   │   ├── validator.py       # Semantic validation
│   │   ├── ir.py              # Intermediate Representation
│   │   ├── optimizer.py       # IR optimization passes
│   │   ├── generators/
│   │   │   ├── __init__.py
│   │   │   ├── base.py        # Abstract generator interface
│   │   │   ├── esphome.py     # ESPHome YAML generator
│   │   │   └── homeassistant.py  # Home Assistant generator
│   │   └── nodes/
│   │       ├── __init__.py
│   │       ├── registry.py    # Node type registry
│   │       ├── digital_io.py
│   │       ├── logic_gates.py
│   │       ├── timing.py
│   │       └── constants.py
│   └── core/
│       ├── __init__.py
│       ├── security.py        # Password hashing, JWT, encryption
│       ├── tenant.py          # Tenant context middleware
│       └── exceptions.py
└── tests/
    ├── conftest.py
    ├── unit/
    │   ├── test_compiler/
    │   │   ├── test_validator.py
    │   │   ├── test_ir.py
    │   │   ├── test_optimizer.py
    │   │   └── test_esphome_generator.py
    │   ├── test_services/
    │   └── test_models/
    ├── integration/
    │   ├── test_auth_api.py
    │   ├── test_projects_api.py
    │   ├── test_boards_api.py
    │   ├── test_compiler_api.py
    │   └── test_tenant_isolation.py
    └── snapshots/
        └── esphome/           # Expected YAML output snapshots
        └── homeassistant/     # Expected HA YAML snapshots
    └── performance/
        └── load_test.py       # k6/locust load test scripts

docker/
├── docker-compose.yml
├── docker-compose.dev.yml
├── frontend/
│   └── Dockerfile
├── backend/
│   └── Dockerfile
└── postgres/
    └── init.sql

docs/
└── design-system.md
```

**Structure Decision**: Web application structure selected (Option 2 from template). The monorepo contains separate `frontend/` and `backend/` directories with shared `docker/` infrastructure. The compiler is embedded within the backend as `app/compiler/` since it runs server-side and shares models/schemas with the API layer. This avoids a separate compiler service while keeping the pipeline modular and independently testable.

## Complexity Tracking

No constitution violations detected. No complexity justifications required.
