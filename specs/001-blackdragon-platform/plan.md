# Implementation Plan: BlackDragon SaaS Platform

**Branch**: `001-blackdragon-platform` | **Date**: 2026-05-17 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/001-blackdragon-platform/spec.md`

## Summary

BlackDragon is a full-stack SaaS web application that serves as the company's public website and a multi-tenant client portal with a visual programming environment for smart home automation. The platform enables clients to design automation logic using a drag-and-drop blocks-and-wires editor, compile visual diagrams into ESPHome YAML and Home Assistant configuration, and deploy generated artifacts to ESP32-based I/O boards via OTA. The BlackDragon brand identity — ultra-dark backgrounds, metallic graphite/silver accents, circuit-board patterns, and futuristic technical typography — is a first-class architectural concern enforced through a comprehensive design token system that permeates every user-facing surface. The implementation uses a Vue 3 + TypeScript frontend with Vue Flow for the visual editor, a FastAPI + Python backend with a modular compiler pipeline, PostgreSQL for persistence, and Docker Compose for infrastructure.

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

**Brand Identity**: Ultra-dark theme derived from `specs/001-blackdragon-platform/blackdragon_logo.png` — all UI surfaces, components, and editor nodes must consume BlackDragon design tokens with zero ad-hoc overrides

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
- E2e tests cover US1 (public website), US2 (auth), US3 (visual editor).
- Performance tests validate SC-004 (100ms editor) and SC-006 (100 concurrent users).

### III. User Experience Consistency — PASS
- BlackDragon design system with Tailwind custom tokens: colors (bd-bg, bd-border, bd-text, bd-accent, bd-chrome), shadows (bd-glow, bd-emboss, bd-node), gradients (bd-metallic, bd-chrome, bd-hero), typography (Exo 2 + JetBrains Mono).
- Reusable Vue component library: BdButton, BdCard, BdInput, BdModal, BdTable, BdStatusIndicator, BdLogo, BdCircuitPattern.
- Error/loading/empty states handled via standard component wrappers.
- WCAG 2.1 AA target: keyboard navigation, screen reader labels, contrast ratios (verified against ultra-dark backgrounds).
- Responsive breakpoints validated for all public pages and portal views.
- Logo (derived from `blackdragon_logo.png`) placed consistently in header, auth pages, dashboard, and landing hero.
- Circuit-board SVG patterns used in hero sections, dividers, card backgrounds, and section separators.
- No ad-hoc CSS overrides — all styling consumes design tokens exclusively.

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
├── blackdragon_logo.png
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
│   ├── logo.svg                # BlackDragon logo (SVG, derived from blackdragon_logo.png)
│   └── circuit-pattern.svg     # SVG circuit-board background pattern
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
│   │   ├── ui/               # BlackDragon design system components
│   │   │   ├── BdButton.vue         # Metallic gradients, glow hover effects
│   │   │   ├── BdCard.vue           # Embossed styling, circuit-pattern bg option
│   │   │   ├── BdInput.vue          # Charcoal surface, validation states
│   │   │   ├── BdModal.vue          # Dark overlay, focus trap
│   │   │   ├── BdTable.vue          # Dark row striping, sort/pagination
│   │   │   ├── BdStatusIndicator.vue
│   │   │   ├── BdLogo.vue           # Logo component (sm/md/lg/xl variants)
│   │   │   └── BdCircuitPattern.vue  # SVG circuit-board decorative pattern
│   │   ├── layout/
│   │   │   ├── AppHeader.vue        # Navigation + BdLogo + metallic border
│   │   │   ├── AppSidebar.vue       # Dark panel + accent highlights
│   │   │   ├── AppFooter.vue        # Circuit-pattern divider
│   │   │   └── PortalLayout.vue     # Ultra-dark background container
│   │   ├── editor/
│   │   │   ├── EditorCanvas.vue     # Vue Flow + circuit-board grid bg
│   │   │   ├── NodePalette.vue
│   │   │   ├── PropertiesPanel.vue
│   │   │   └── nodes/              # All nodes: dark bodies, color-coded ports, glow
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
│   │   │   ├── HomePage.vue         # Hero with bd-hero gradient + BdLogo (xl)
│   │   │   ├── AboutPage.vue        # Circuit-pattern dividers
│   │   │   ├── ProductsPage.vue     # BdCard metallic board catalog
│   │   │   ├── SolutionsPage.vue
│   │   │   ├── ProjectsPage.vue
│   │   │   ├── BlogPage.vue
│   │   │   └── ContactPage.vue
│   │   ├── auth/
│   │   │   ├── LoginPage.vue        # BdLogo + metallic card container
│   │   │   └── RegisterPage.vue     # BdLogo + metallic card container
│   │   └── portal/
│   │       ├── DashboardPage.vue    # BdLogo header + metallic project cards
│   │       ├── ProjectListPage.vue
│   │       ├── ProjectEditorPage.vue
│   │       ├── BoardCatalogPage.vue
│   │       ├── YamlPreviewPage.vue
│   │       ├── DeploymentPage.vue
│   │       ├── ProfilePage.vue
│   │       └── admin/
│   │           ├── UsersPage.vue
│   │           ├── ClientsPage.vue
│   │           ├── BoardManagementPage.vue
│   │           └── BlogManagementPage.vue
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
│           └── main.css      # Tailwind directives + bd-* base styles
└── tests/
    ├── unit/
    │   ├── components/
    │   ├── stores/
    │   └── services/
    └── e2e/
        ├── public-website.spec.ts
        ├── auth.spec.ts
        ├── project-management.spec.ts
        ├── visual-editor.spec.ts
        └── editor-performance.spec.ts

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
    │   │   ├── test_esphome_generator.py
    │   │   ├── test_homeassistant_generator.py
    │   │   └── test_modules.py
    │   ├── test_services/
    │   └── test_models/
    ├── integration/
    │   ├── test_auth_api.py
    │   ├── test_projects_api.py
    │   ├── test_boards_api.py
    │   ├── test_compiler_api.py
    │   ├── test_deployments_api.py
    │   ├── test_versions_api.py
    │   ├── test_admin_api.py
    │   ├── test_leads_api.py
    │   ├── test_tenant_isolation.py
    │   └── test_rls_policies.py
    ├── snapshots/
    │   ├── esphome/           # Expected YAML output snapshots
    │   └── homeassistant/     # Expected HA YAML snapshots
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
```

## BlackDragon Design System Architecture

The design system is a first-class architectural layer, not an afterthought. It is the authoritative source for all visual presentation across the platform.

### Brand Foundation

The BlackDragon brand identity is derived from the logo at `specs/001-blackdragon-platform/blackdragon_logo.png`. The logo features a dragon motif rendered in metallic silver/graphite tones on a pure black background, evoking industrial precision, circuit-board aesthetics, and premium engineering.

**All brand imagery (favicon, SVG logo variants, and social/OG images) MUST be closely derived from the original `blackdragon_logo.png`**. Variations are acceptable (e.g., monochrome, simplified icon, SVG trace) but the dragon silhouette, metallic tone, and dark background must remain recognizable and faithful to the source.

### Design Token Hierarchy

```
tailwind.config.ts (source of truth)
  ├── colors: bd-bg, bd-border, bd-text, bd-accent, bd-chrome, bd-success, bd-warning, bd-error
  ├── boxShadow: bd-glow, bd-glow-accent, bd-emboss, bd-node
  ├── backgroundImage: bd-metallic, bd-chrome, bd-hero
  ├── fontFamily: bd-sans (Exo 2), bd-mono (JetBrains Mono)
  └── extends: animation, spacing
        │
        ▼
  main.css (@layer base: global dark bg, body fonts, scrollbar styling)
        │
        ▼
  Bd* Components (BdButton, BdCard, BdInput, BdLogo, BdCircuitPattern, ...)
        │
        ▼
  Page Views (consume Bd* components exclusively — no raw HTML styling)
        │
        ▼
  Editor Nodes (BdNode base styling: dark body, bd-node shadow, port colors)
```

### Color Palette

| Token | Value | Usage |
|-------|-------|-------|
| `bd-bg-primary` | `#050505` | Page backgrounds, editor canvas |
| `bd-bg-secondary` | `#0A0A0A` | Alternate section backgrounds |
| `bd-bg-panel` | `#111111` | Sidebars, panels, card backgrounds |
| `bd-bg-surface` | `#181818` | Elevated surfaces, dropdowns |
| `bd-border` | `#2A2A2A` | Default borders |
| `bd-border-accent` | `#3A3A3A` | Hover/focus borders |
| `bd-text-primary` | `#E5E5E5` | Primary text |
| `bd-text-secondary` | `#9CA3AF` | Secondary/descriptive text |
| `bd-text-muted` | `#6B7280` | Disabled/placeholder text |
| `bd-accent` | `#6B7280` | Default accent elements |
| `bd-accent-highlight` | `#D1D5DB` | Highlighted/hover accents |
| `bd-accent-metallic` | `#8B8B8B` | Metallic shine highlights |
| `bd-chrome-light` | `#C0C0C0` | Chrome accent (bright) |
| `bd-chrome-mid` | `#808080` | Chrome accent (mid) |
| `bd-chrome-dark` | `#404040` | Chrome accent (shadow) |
| `bd-success` | `#10B981` | Success states |
| `bd-warning` | `#F59E0B` | Warning states |
| `bd-error` | `#EF4444` | Error states |

### Typography

| Token | Font | Usage |
|-------|------|-------|
| `bd-sans` | Exo 2 | All UI text: headings, body, labels, buttons |
| `bd-mono` | JetBrains Mono | Code blocks, YAML preview, technical data, port labels |

### Visual Rules (enforced by design system)

1. **No white or light backgrounds** — every surface uses `bd-bg-*` tokens.
2. **All borders** use `bd-border` or `bd-border-accent` — no raw gray values.
3. **Interactive elements** (buttons, links, inputs) show `bd-glow` or `bd-glow-accent` on hover/focus.
4. **Cards and panels** use `bd-emboss` shadow for the raised metallic look.
5. **Circuit-board SVG pattern** (`BdCircuitPattern`) used in: HomePage hero, page section dividers, card decorative backgrounds, and footer.
6. **Logo placement** (`BdLogo`) required at: AppHeader (md), LoginPage (lg), RegisterPage (lg), DashboardPage (md), HomePage hero (xl).
7. **Editor nodes** use `bd-node` shadow, `bd-bg-surface` body, color-coded handle dots, and `bd-accent-highlight` selection glow.
8. **No ad-hoc CSS** — all styling through Tailwind utility classes consuming `bd-*` tokens or `@apply` in component `<style>` blocks.
