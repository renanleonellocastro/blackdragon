# Tasks: BlackDragon SaaS Platform

**Input**: Design documents from `/specs/001-blackdragon-platform/`

**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Included — constitution mandates testing standards as NON-NEGOTIABLE; spec requires automated unit, integration, and e2e tests.

**Organization**: Tasks grouped by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Frontend**: `frontend/src/`
- **Backend**: `backend/app/`
- **Frontend tests**: `frontend/tests/`
- **Backend tests**: `backend/tests/`
- Paths based on plan.md project structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize monorepo, tooling, and containerized development environment

- [X] T001 Create monorepo directory structure per plan.md (frontend/, backend/, docker/, docs/)
- [X] T002 Initialize Vue 3 + TypeScript project with Vite in frontend/ (package.json, tsconfig.json, vite.config.ts, index.html, src/main.ts, src/App.vue)
- [X] T003 Initialize Python 3.12+ project with FastAPI in backend/ (pyproject.toml with dependencies: fastapi, sqlalchemy, alembic, pydantic, pydantic-settings, python-jose, passlib, pyyaml, asyncpg, cryptography, httpx, uvicorn)
- [X] T004 [P] Configure ESLint + Prettier for TypeScript strict mode in frontend/ (.eslintrc.cjs, .prettierrc)
- [X] T005 [P] Configure Ruff + Black + mypy for Python in backend/ (ruff.toml, mypy.ini)
- [X] T006 [P] Create Docker Compose development configuration with PostgreSQL 16 service in docker/docker-compose.dev.yml and backend Dockerfile in docker/backend/Dockerfile

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### BlackDragon Design System & Brand Identity

- [X] T007 Configure Tailwind CSS with full BlackDragon design token system in frontend/tailwind.config.ts — colors (bd-bg primary/secondary/panel/surface, bd-border/accent, bd-text primary/secondary/muted, bd-accent/highlight/metallic, bd-chrome light/mid/dark, bd-success/warning/error), shadows (bd-glow, bd-glow-accent, bd-emboss, bd-node), gradients (bd-metallic, bd-chrome, bd-hero), and font families (bd-sans: Exo 2, bd-mono: JetBrains Mono) per plan.md color palette table
- [X] T008 Add Exo 2 and JetBrains Mono web fonts to frontend/index.html (Google Fonts or self-hosted) and wire into Tailwind fontFamily tokens in frontend/tailwind.config.ts
- [X] T009 Create global base styles in frontend/src/assets/styles/main.css — Tailwind directives (@tailwind base/components/utilities), @layer base rules for body bg (#050505), font-family (bd-sans), text color (bd-text-primary), custom scrollbar styling with bd-bg-panel/bd-accent, and selection highlight colors
- [X] T010 Create SVG logo file (derived from specs/001-blackdragon-platform/blackdragon_logo.png, faithful to dragon silhouette and metallic tone) in frontend/public/logo.svg and generate matching favicon.ico in frontend/public/favicon.ico
- [X] T011 Create SVG circuit-board decorative pattern tile in frontend/public/circuit-pattern.svg — repeating traces, vias, and pads in bd-border color on transparent background for use as background-image
- [X] T012 Create BdLogo component with size variants (sm: 24px, md: 32px, lg: 48px, xl: 80px) rendering logo.svg in frontend/src/components/ui/BdLogo.vue
- [X] T013 [P] Create BdCircuitPattern component rendering circuit-pattern.svg as a decorative overlay with configurable opacity and position in frontend/src/components/ui/BdCircuitPattern.vue
- [X] T014 [P] Create BdButton component with variants (primary: bd-metallic gradient + bd-glow hover, secondary: bd-bg-surface + bd-border, ghost: transparent + bd-text-secondary, danger: bd-error) in frontend/src/components/ui/BdButton.vue
- [X] T015 [P] Create BdCard component with bd-emboss shadow, bd-bg-panel background, bd-border, optional circuit-pattern background slot, and hover glow effect in frontend/src/components/ui/BdCard.vue
- [X] T016 [P] Create BdInput component with bd-bg-surface background, bd-border, focus ring (bd-border-accent + bd-glow), validation error state (bd-error), and placeholder text (bd-text-muted) in frontend/src/components/ui/BdInput.vue
- [X] T017 [P] Create BdModal component with bd-bg-primary/80 overlay, bd-bg-panel content surface, bd-emboss shadow, focus trap, and close button in frontend/src/components/ui/BdModal.vue
- [X] T018 [P] Create BdTable component with bd-bg-panel header, alternating bd-bg-primary/bd-bg-secondary rows, bd-border dividers, sort indicators, and pagination in frontend/src/components/ui/BdTable.vue
- [X] T019 [P] Create BdStatusIndicator component with dot/badge variants using bd-success/bd-warning/bd-error/bd-accent colors in frontend/src/components/ui/BdStatusIndicator.vue

### Layout Components

- [X] T020 Create AppHeader with BdLogo (md), navigation links (bd-text-secondary, hover bd-text-primary), metallic bottom border (bd-chrome-dark), and responsive mobile menu in frontend/src/components/layout/AppHeader.vue
- [X] T021 [P] Create AppFooter with BdCircuitPattern divider, bd-bg-secondary background, copyright text (bd-text-muted), and footer links in frontend/src/components/layout/AppFooter.vue
- [X] T022 [P] Create AppSidebar for portal navigation with bd-bg-panel background, active item highlight (bd-accent-highlight left border), icon + label nav items, and collapsible toggle in frontend/src/components/layout/AppSidebar.vue
- [X] T023 Create PortalLayout combining AppSidebar + content area with bd-bg-primary background, responsive sidebar collapse, and breadcrumb slot in frontend/src/components/layout/PortalLayout.vue

### Frontend Core

- [X] T024 Configure Vue Router with public, auth, and portal route groups (lazy-loaded) in frontend/src/router/index.ts
- [X] T025 Create API HTTP client with auth interceptor, base URL config, and 401 session-expiry detection in frontend/src/services/api.ts
- [X] T026 Create TypeScript type definitions for API responses in frontend/src/types/api.ts

### Backend Core

- [X] T027 Create environment configuration with Pydantic Settings (DATABASE_URL, SECRET_KEY, FERNET_KEY, CORS_ORIGINS, token expiry) in backend/app/config.py
- [X] T028 Create SQLAlchemy async engine, session factory, and Base declarative class in backend/app/database.py
- [X] T029 Create Tenant model with fields per data-model.md in backend/app/models/tenant.py
- [X] T030 [P] Create User model with fields per data-model.md in backend/app/models/user.py
- [X] T031 Implement password hashing (bcrypt via Passlib), JWT creation/verification (python-jose), and Fernet encryption for credentials in backend/app/core/security.py
- [X] T032 Create tenant context middleware with SQLAlchemy event filter for automatic tenant_id injection on queries in backend/app/core/tenant.py
- [X] T033 Create custom exception classes (NotFound, Forbidden, Conflict, ValidationError) and FastAPI exception handlers in backend/app/core/exceptions.py
- [X] T034 Create FastAPI dependency injection functions (get_db, get_current_user, require_role, get_tenant_context) in backend/app/api/deps.py
- [X] T035 Create FastAPI application factory with CORS middleware, exception handlers, and router mounting in backend/app/main.py
- [X] T036 Configure Alembic for async with env.py and create initial migration for Tenant and User tables in backend/alembic/
- [X] T037 Create database seed script with admin user and test client in backend/app/seed.py
- [X] T038 Create PostgreSQL Row Level Security (RLS) policies for all tenant-scoped tables as defense-in-depth isolation layer, with migration in backend/alembic/versions/ and verification test in backend/tests/integration/test_rls_policies.py

### Testing Infrastructure

- [X] T039 [P] Create backend test conftest.py with async db session, test client, auth token fixtures, and test tenant setup in backend/tests/conftest.py
- [X] T040 [P] Configure Vitest for frontend unit tests in frontend/vite.config.ts and frontend/package.json
- [X] T041 [P] Test tenant isolation middleware filters queries correctly in backend/tests/integration/test_tenant_isolation.py

**Checkpoint**: Foundation ready — design system complete, backend core operational, user story implementation can begin

---

## Phase 3: User Story 1 — Public Website (Priority: P1) 🎯 MVP

**Goal**: Public-facing website with BlackDragon premium brand presence, product catalog, blog, and lead capture form

**Independent Test**: Navigate all public pages, verify BlackDragon brand identity (dark backgrounds, metallic accents, circuit patterns, logo), submit contact form, confirm submission stored

### Tests for User Story 1

- [X] T042 [P] [US1] Test lead submission API endpoint (create, list, update status) in backend/tests/integration/test_leads_api.py
- [X] T043 [P] [US1] Test blog API endpoints (public list, public detail, admin CRUD) in backend/tests/integration/test_blog_api.py

### Implementation for User Story 1

- [X] T044 [P] [US1] Create LeadSubmission model with fields per data-model.md in backend/app/models/lead_submission.py
- [X] T045 [P] [US1] Create BlogPost model with fields per data-model.md in backend/app/models/blog_post.py
- [X] T046 [P] [US1] Create lead Pydantic schemas (LeadCreate, LeadResponse, LeadUpdate) in backend/app/schemas/lead.py
- [X] T047 [P] [US1] Create blog Pydantic schemas (BlogPostCreate, BlogPostUpdate, BlogPostResponse, BlogPostList) in backend/app/schemas/blog.py
- [X] T048 [US1] Create lead submission API endpoints (POST /api/leads public, GET/PATCH /api/admin/leads admin) in backend/app/api/leads.py
- [X] T049 [US1] Create blog service (list published, get by slug, admin CRUD) in backend/app/services/blog_service.py
- [X] T050 [US1] Create blog API endpoints (GET /api/blog public listing, GET /api/blog/:slug public detail, POST/PATCH/DELETE /api/admin/blog admin CRUD) in backend/app/api/blog.py
- [X] T051 [US1] Add Alembic migration for LeadSubmission and BlogPost tables in backend/alembic/versions/
- [X] T052 [P] [US1] Create HomePage with bd-hero radial gradient background, BdLogo (xl) in hero, BdCircuitPattern overlay, feature cards using BdCard with metallic styling, and CTA with BdButton primary glow in frontend/src/views/public/HomePage.vue
- [X] T053 [P] [US1] Create AboutPage with company overview, mission section with BdCircuitPattern dividers, team grid using BdCard, and bd-metallic gradient section headers in frontend/src/views/public/AboutPage.vue
- [X] T054 [P] [US1] Create ProductsPage displaying board catalog with BdCard metallic emboss styling, board images, specifications tables using BdTable, and bd-chrome accents in frontend/src/views/public/ProductsPage.vue
- [X] T055 [P] [US1] Create SolutionsPage with automation capability cards using BdCard, use case sections with circuit-pattern backgrounds, and technical typography in frontend/src/views/public/SolutionsPage.vue
- [X] T056 [P] [US1] Create ProjectsPage with case study portfolio using BdCard grid, project scope/hardware/outcome details, and metallic accent dividers in frontend/src/views/public/ProjectsPage.vue
- [X] T057 [P] [US1] Create BlogPage with article listing using BdCard, excerpt display, author/date metadata in bd-text-secondary, and pagination in frontend/src/views/public/BlogPage.vue
- [X] T058 [US1] Create ContactPage with BdCircuitPattern background, validated lead capture form using BdInput/BdButton, success confirmation with BdStatusIndicator, calling POST /api/leads in frontend/src/views/public/ContactPage.vue

**Checkpoint**: Public website fully navigable with full BlackDragon brand presence, blog operational, contact form stores submissions

---

## Phase 4: User Story 2 — Authentication & Project Management (Priority: P1)

**Goal**: User registration, login with branded auth pages, multi-tenant dashboard, project CRUD with duplication and locking

**Independent Test**: Register, log in (verify BdLogo on auth pages), create project, duplicate, verify tenant isolation

### Tests for User Story 2

- [X] T059 [P] [US2] Test auth API endpoints (register, login, refresh, me, invalid credentials) in backend/tests/integration/test_auth_api.py
- [X] T060 [P] [US2] Test projects API endpoints (CRUD, duplicate, lock/unlock, tenant isolation) in backend/tests/integration/test_projects_api.py

### Implementation for User Story 2

- [X] T061 [P] [US2] Create auth Pydantic schemas (LoginRequest, RegisterRequest, TokenResponse, UserResponse) in backend/app/schemas/auth.py
- [X] T062 [P] [US2] Create user Pydantic schemas (UserCreate, UserUpdate, UserList) in backend/app/schemas/user.py
- [X] T063 [US2] Create auth service (register with tenant creation, login, refresh token) in backend/app/services/auth_service.py
- [X] T064 [US2] Create auth API endpoints (POST register, POST login, POST refresh, GET me) per contracts/auth.md in backend/app/api/auth.py
- [X] T065 [P] [US2] Create Property model with fields per data-model.md in backend/app/models/property.py
- [X] T066 [P] [US2] Create Project model with fields per data-model.md in backend/app/models/project.py
- [X] T067 [P] [US2] Create property and project Pydantic schemas in backend/app/schemas/project.py
- [X] T068 [US2] Create project service (create, list, get, update, delete, duplicate, lock/unlock) in backend/app/services/project_service.py
- [X] T069 [US2] Create properties API endpoints per contracts/properties.md in backend/app/api/properties.py
- [X] T070 [US2] Create projects API endpoints per contracts/projects.md in backend/app/api/projects.py
- [X] T071 [US2] Add Alembic migration for Property and Project tables in backend/alembic/versions/
- [X] T072 [P] [US2] Create auth frontend service (login, register, refresh, logout API calls) in frontend/src/services/auth.service.ts
- [X] T073 [P] [US2] Create Pinia auth store with token management, user state, and automatic session expiry detection with re-authentication prompt (intercept 401 during editing to prevent data loss) in frontend/src/stores/auth.ts
- [X] T074 [P] [US2] Create useAuth composable for login/logout/register actions in frontend/src/composables/useAuth.ts
- [X] T075 [US2] Create LoginPage with BdLogo (lg) centered above metallic BdCard container, email/password BdInput fields, BdButton primary submit, bd-bg-primary full-page background, and BdCircuitPattern subtle overlay in frontend/src/views/auth/LoginPage.vue
- [X] T076 [US2] Create RegisterPage with BdLogo (lg), registration form using BdInput/BdButton within metallic BdCard, validation feedback, and matching branded styling in frontend/src/views/auth/RegisterPage.vue
- [X] T077 [P] [US2] Create project frontend service (CRUD, duplicate API calls) in frontend/src/services/project.service.ts
- [X] T078 [P] [US2] Create Pinia project store with project list and current project state in frontend/src/stores/project.ts
- [X] T079 [P] [US2] Create project TypeScript types in frontend/src/types/project.ts
- [X] T080 [US2] Create DashboardPage with BdLogo (md) in page header, property list sidebar, project cards using BdCard metallic emboss with status indicators, BdCircuitPattern section dividers, and quick-action BdButtons in frontend/src/views/portal/DashboardPage.vue
- [X] T081 [US2] Create ProjectListPage with BdTable for project listing, BdStatusIndicator for project status, filtering, and BdButton project actions in frontend/src/views/portal/ProjectListPage.vue
- [X] T082 [US2] Add route guards for authenticated routes in frontend/src/router/index.ts

**Checkpoint**: Users can register, log in with branded auth flow, manage properties and projects. Tenant isolation enforced.

---

## Phase 5: User Story 3 — Visual Programming Editor (Priority: P1)

**Goal**: Drag-and-drop blocks-and-wires editor with 12 MVP node types using BlackDragon node styling, property editing, wire validation, and auto-save

**Independent Test**: Place blocks (verify dark node bodies, color-coded ports), connect with wires, configure properties, save and reload — all data persists

### Tests for User Story 3

- [X] T083 [P] [US3] Test diagram API endpoints (CRUD, save graph_data, auto-save draft) in backend/tests/integration/test_diagrams_api.py
- [X] T084 [P] [US3] Test editor store (add/remove nodes, connect edges, update properties) in frontend/tests/unit/stores/editor.spec.ts

### Implementation for User Story 3

- [X] T085 [P] [US3] Create Diagram model with fields per data-model.md in backend/app/models/diagram.py
- [X] T086 [P] [US3] Create diagram Pydantic schemas (DiagramCreate, DiagramUpdate, DiagramResponse, DraftSave) in backend/app/schemas/diagram.py
- [X] T087 [US3] Create diagram service (CRUD, save graph_data, save draft) in backend/app/services/diagram_service.py
- [X] T088 [US3] Create diagram API endpoints per contracts/diagrams.md in backend/app/api/diagrams.py
- [X] T089 [US3] Add Alembic migration for Diagram table in backend/alembic/versions/
- [X] T090 [P] [US3] Create editor TypeScript types (NodeData, EdgeData, PortDefinition, NodeDefinition) in frontend/src/types/editor.ts
- [X] T091 [P] [US3] Create Pinia editor store with Vue Flow state management in frontend/src/stores/editor.ts
- [X] T092 [US3] Create DigitalInputNode custom Vue Flow node with bd-bg-surface body, bd-node shadow, bd-success colored signal output handle, node header with bd-chrome-dark gradient and Exo 2 label, GPIO/pull config display in frontend/src/components/editor/nodes/DigitalInputNode.vue
- [X] T093 [P] [US3] Create DigitalOutputNode custom Vue Flow node with bd-bg-surface body, bd-node shadow, bd-warning colored signal input handle, chrome header gradient, and pin config display in frontend/src/components/editor/nodes/DigitalOutputNode.vue
- [X] T094 [P] [US3] Create LogicGateNode (AND, OR, NOT, XOR variants) with bd-bg-surface body, bd-node shadow, bd-accent-highlight port handles, gate symbol in bd-chrome-light, and variant label in frontend/src/components/editor/nodes/LogicGateNode.vue
- [X] T095 [P] [US3] Create TimerNode with bd-bg-surface body, bd-node shadow, trigger input (bd-accent) and output (bd-success) handles, duration display in bd-mono font in frontend/src/components/editor/nodes/TimerNode.vue
- [X] T096 [P] [US3] Create DelayNode with bd-bg-surface body, bd-node shadow, input/output handles, delay_ms display in frontend/src/components/editor/nodes/DelayNode.vue
- [X] T097 [P] [US3] Create EdgeDetectorNode with bd-bg-surface body, bd-node shadow, rising (bd-success) and falling (bd-error) output handles in frontend/src/components/editor/nodes/EdgeDetectorNode.vue
- [X] T098 [P] [US3] Create DebounceNode with bd-bg-surface body, bd-node shadow, input/output handles, delay display in frontend/src/components/editor/nodes/DebounceNode.vue
- [X] T099 [P] [US3] Create ConstantNode (True/False variants) with bd-bg-surface body, bd-node shadow, bd-success (True) or bd-error (False) value indicator, output handle in frontend/src/components/editor/nodes/ConstantNode.vue
- [X] T100 [US3] Create NodePalette component with categorized draggable node list (Hardware, Logic, Timing, Constants), bd-bg-panel background, search filter, category headers in bd-text-secondary, and node preview cards in frontend/src/components/editor/NodePalette.vue
- [X] T101 [US3] Create PropertiesPanel component with bd-bg-panel background, BdInput fields for selected node properties, section headers in bd-chrome-mid, and real-time property update in frontend/src/components/editor/PropertiesPanel.vue
- [X] T102 [US3] Create EditorCanvas component integrating Vue Flow with custom nodes, minimap (bd-bg-panel), controls (bd-chrome-dark), bd-bg-primary canvas background with circuit-pattern.svg grid overlay, bd-accent-highlight selection glow, connection validation, and custom edge styling (bd-border-accent) in frontend/src/components/editor/EditorCanvas.vue
- [X] T103 [US3] Create useAutoSave composable with debounced draft save (60s interval) in frontend/src/composables/useAutoSave.ts
- [X] T104 [US3] Create ProjectEditorPage integrating EditorCanvas, NodePalette, and PropertiesPanel with resizable panels, bd-bg-primary background, and toolbar with compile/save BdButtons in frontend/src/views/portal/ProjectEditorPage.vue

**Checkpoint**: Visual editor fully functional with BlackDragon branded nodes — dark bodies, color-coded ports, metallic headers, selection glow. Save/load and auto-save working.

---

## Phase 6: User Story 4 — Board Configuration (Priority: P2)

**Goal**: Board catalog browsing, board instance creation per project, I/O channel configuration with GPIO/electrical options

**Independent Test**: Add board from catalog, configure I/O channels, verify channels appear as editor blocks with BlackDragon node styling

### Tests for User Story 4

- [X] T105 [P] [US4] Test boards API endpoints (catalog CRUD, instance CRUD, channel config, GPIO conflict detection) in backend/tests/integration/test_boards_api.py

### Implementation for User Story 4

- [X] T106 [P] [US4] Create BoardModel and BoardModelChannel models per data-model.md in backend/app/models/board_model.py
- [X] T107 [P] [US4] Create BoardInstance and BoardInstanceChannel models per data-model.md in backend/app/models/board_instance.py
- [X] T108 [P] [US4] Create board Pydantic schemas (BoardModelResponse, BoardInstanceCreate, ChannelConfig) in backend/app/schemas/board.py
- [X] T109 [US4] Create board service (catalog listing, instance CRUD, channel update, GPIO conflict check) in backend/app/services/board_service.py
- [X] T110 [US4] Create boards API endpoints per contracts/boards.md in backend/app/api/boards.py
- [X] T111 [US4] Add Alembic migration for BoardModel, BoardModelChannel, BoardInstance, BoardInstanceChannel tables in backend/alembic/versions/
- [X] T112 [US4] Add board model seed data (sample BlackDragon boards with I/O definitions) to backend/app/seed.py
- [X] T113 [P] [US4] Create board frontend service (catalog, instance CRUD, channel config API calls) in frontend/src/services/board.service.ts
- [X] T114 [P] [US4] Create board TypeScript types in frontend/src/types/board.ts
- [X] T115 [P] [US4] Create Pinia board store with catalog and instance state in frontend/src/stores/board.ts
- [X] T116 [US4] Create BoardSelector component with BdCard catalog grid, board images, spec summaries, and BdButton add action in frontend/src/components/boards/BoardSelector.vue
- [X] T117 [US4] Create IoChannelEditor component with BdInput for GPIO/pull/debounce/inverted config, channel name field, and bd-border row dividers in frontend/src/components/boards/IoChannelEditor.vue
- [X] T118 [US4] Create BoardConfigurator component combining board metadata header (BdCard), IoChannelEditor list, and save BdButton in frontend/src/components/boards/BoardConfigurator.vue
- [X] T119 [US4] Create BoardCatalogPage displaying available boards and project board instances with BdCard styling and board management actions in frontend/src/views/portal/BoardCatalogPage.vue

**Checkpoint**: Boards configurable per project with BlackDragon UI, I/O channels mapped to GPIO pins, channels available as editor blocks

---

## Phase 7: User Story 5 — ESPHome YAML Compilation (Priority: P2)

**Goal**: Compiler pipeline (validate → IR → optimize → generate), ESPHome YAML output, preview and download

**Independent Test**: Create diagram with DigitalInput → AND → DigitalOutput, compile, verify valid ESPHome YAML with correct GPIO mappings

### Tests for User Story 5

- [X] T120 [P] [US5] Test graph validator (unconnected ports, type mismatches, GPIO conflicts, cycles) in backend/tests/unit/test_compiler/test_validator.py
- [X] T121 [P] [US5] Test IR generation (topological sort, type resolution) in backend/tests/unit/test_compiler/test_ir.py
- [X] T122 [P] [US5] Test optimizer (dead-node elimination, constant folding) in backend/tests/unit/test_compiler/test_optimizer.py
- [X] T123 [P] [US5] Test ESPHome generator with YAML snapshot comparisons in backend/tests/unit/test_compiler/test_esphome_generator.py
- [X] T124 [P] [US5] Test compile API endpoint (success, validation errors, artifact retrieval) in backend/tests/integration/test_compiler_api.py

### Implementation for User Story 5

- [X] T125 [P] [US5] Create node type definitions (DigitalInput, DigitalOutput, AND, OR, NOT, XOR, Timer, Delay, EdgeDetector, Debounce, ConstantTrue, ConstantFalse) in backend/app/compiler/nodes/digital_io.py, logic_gates.py, timing.py, constants.py
- [X] T126 [P] [US5] Create node type registry with port definitions and property schemas in backend/app/compiler/nodes/registry.py
- [X] T127 [US5] Create semantic validator (connectivity, type compatibility, GPIO conflicts, cycle detection) in backend/app/compiler/validator.py
- [X] T128 [US5] Create Intermediate Representation with IRNode, IREdge, and topological sort in backend/app/compiler/ir.py
- [X] T129 [US5] Create IR optimizer (dead-node elimination, constant folding) in backend/app/compiler/optimizer.py
- [X] T130 [US5] Create abstract base generator interface in backend/app/compiler/generators/base.py
- [X] T131 [US5] Create ESPHome YAML generator mapping IR nodes to ESPHome components (binary_sensor, switch, output, lambda, filters) in backend/app/compiler/generators/esphome.py
- [X] T132 [US5] Create compiler pipeline orchestrator (validate → IR → optimize → generate) in backend/app/compiler/pipeline.py
- [X] T133 [P] [US5] Create CompilationArtifact model per data-model.md in backend/app/models/compilation_artifact.py
- [X] T134 [P] [US5] Create compiler Pydantic schemas (CompileRequest, CompileResponse, ArtifactResponse, ValidationResult) in backend/app/schemas/compiler.py
- [X] T135 [US5] Create compiler API endpoints (POST compile, GET artifacts, GET download, POST validate, GET node definitions) per contracts/compiler.md in backend/app/api/compiler.py
- [X] T136 [US5] Add Alembic migration for CompilationArtifact table in backend/alembic/versions/
- [X] T137 [P] [US5] Create compiler frontend service (compile, validate, get artifacts, download API calls) in frontend/src/services/compiler.service.ts
- [X] T138 [US5] Create YamlPreviewPage with bd-bg-panel code container, JetBrains Mono (bd-mono) syntax-highlighted YAML display, BdButton download action, and line numbers in bd-text-muted in frontend/src/views/portal/YamlPreviewPage.vue
- [X] T139 [US5] Add compile and validate BdButtons to ProjectEditorPage toolbar with bd-error node highlighting on validation failures and bd-success glow on compile success in frontend/src/views/portal/ProjectEditorPage.vue
- [X] T140 [US5] Create YAML snapshot test fixtures (expected ESPHome output for standard diagrams) in backend/tests/snapshots/esphome/

**Checkpoint**: Diagrams compile to valid ESPHome YAML, preview renders with branded YAML viewer, files downloadable

---

## Phase 8: User Story 6 — OTA Deployment (Priority: P3)

**Goal**: Deploy compiled ESPHome configurations to ESP32 boards via OTA, track progress and status

**Independent Test**: Compile diagram, initiate OTA deployment, monitor progress, verify success/failure reporting

### Tests for User Story 6

- [X] T141 [P] [US6] Test deployment API endpoints (create, list, status, cancel) in backend/tests/integration/test_deployments_api.py

### Implementation for User Story 6

- [X] T142 [P] [US6] Create Deployment model per data-model.md in backend/app/models/deployment.py
- [X] T143 [P] [US6] Create Credential model per data-model.md in backend/app/models/credential.py
- [X] T144 [P] [US6] Create deployment Pydantic schemas (DeployRequest, DeployResponse, DeploymentStatus) in backend/app/schemas/deployment.py
- [X] T145 [US6] Create deployment service (initiate OTA via ESPHome subprocess, track progress, update status) in backend/app/services/deployment_service.py
- [X] T146 [US6] Create deployment API endpoints per contracts/deployments.md in backend/app/api/deployments.py
- [X] T147 [US6] Add Alembic migration for Deployment and Credential tables in backend/alembic/versions/
- [X] T148 [P] [US6] Create deployment frontend service (deploy, list, status, cancel API calls) in frontend/src/services/deployment.service.ts
- [X] T149 [US6] Create DeploymentPage with board selection using BdCard, BdButton deploy action, progress bar with bd-accent-highlight fill, BdStatusIndicator for status, and history BdTable in frontend/src/views/portal/DeploymentPage.vue

**Checkpoint**: End-to-end flow from design to deployed firmware on ESP32 boards

---

## Phase 9: User Story 7 — Project Versioning (Priority: P3)

**Goal**: Save named versions, view history, compare versions, roll back to previous versions

**Independent Test**: Save version, make changes, save again, view history, compare versions, roll back to first version

### Tests for User Story 7

- [X] T150 [P] [US7] Test version API endpoints (save version, list history, rollback, diff) in backend/tests/integration/test_versions_api.py

### Implementation for User Story 7

- [X] T151 [P] [US7] Create ProjectVersion model per data-model.md in backend/app/models/project_version.py
- [X] T152 [US7] Add version save, list history, rollback, and diff methods to project service in backend/app/services/project_service.py
- [X] T153 [US7] Add version API endpoints (POST save, GET list, POST rollback, GET diff) to projects router per contracts/projects.md in backend/app/api/projects.py
- [X] T154 [US7] Add Alembic migration for ProjectVersion table in backend/alembic/versions/
- [X] T155 [US7] Add version history panel with BdTable listing, BdButton rollback action, and side-by-side diff comparison view to ProjectEditorPage in frontend/src/views/portal/ProjectEditorPage.vue

**Checkpoint**: Project versioning with save, history, rollback, and diff comparison fully functional

---

## Phase 10: User Story 8 — Administrator Management (Priority: P3)

**Goal**: Admin dashboard with user management, cross-tenant project access, board catalog management, blog management, audit logs

**Independent Test**: Log in as admin, view all clients, access client project, add board to catalog, manage blog posts, view audit logs

### Tests for User Story 8

- [X] T156 [P] [US8] Test admin API endpoints (list users, update user, list tenants, list audit logs, RBAC enforcement) in backend/tests/integration/test_admin_api.py

### Implementation for User Story 8

- [X] T157 [P] [US8] Create AuditLog model per data-model.md in backend/app/models/audit_log.py
- [X] T158 [US8] Create audit service (log action, query logs) in backend/app/services/audit_service.py
- [X] T159 [US8] Create user service (list, update, deactivate) in backend/app/services/user_service.py
- [X] T160 [US8] Create admin API endpoints (users, tenants, audit logs) per contracts/admin.md in backend/app/api/admin.py
- [X] T161 [US8] Add Alembic migration for AuditLog table in backend/alembic/versions/
- [X] T162 [US8] Integrate audit logging into project, deployment, and auth services in backend/app/services/
- [X] T163 [P] [US8] Create UsersPage with BdTable user list, role editing with BdInput, active/deactivate toggle with BdButton in frontend/src/views/portal/admin/UsersPage.vue
- [X] T164 [P] [US8] Create ClientsPage with BdTable tenant list and cross-tenant project access using BdCard in frontend/src/views/portal/admin/ClientsPage.vue
- [X] T165 [US8] Create BoardManagementPage with BdTable board model CRUD, BdInput I/O channel definition editor, and BdButton actions in frontend/src/views/portal/admin/BoardManagementPage.vue
- [X] T166 [US8] Create BlogManagementPage with BdTable post list, BdInput/BdModal post editor, publish toggle, and Markdown preview in frontend/src/views/portal/admin/BlogManagementPage.vue
- [X] T167 [US8] Create ProfilePage with BdCard user profile display, BdInput password change form, and BdButton save action in frontend/src/views/portal/ProfilePage.vue

**Checkpoint**: Administrators can manage users, boards, blog, and view audit logs — all with BlackDragon branded UI

---

## Phase 11: User Story 9 — Home Automation Logic (Priority: P4)

**Goal**: Home Automation programming layer with board entities and Home Assistant YAML generation

**Independent Test**: Switch to Home Automation layer, create automation with board entities and Timer, compile, verify Home Assistant YAML

### Tests for User Story 9

- [X] T168 [P] [US9] Test Home Assistant generator with YAML snapshot comparisons in backend/tests/unit/test_compiler/test_homeassistant_generator.py

### Implementation for User Story 9

- [X] T169 [US9] Create Home Assistant YAML generator mapping IR nodes to HA automations, scripts, and helpers in backend/app/compiler/generators/homeassistant.py
- [X] T170 [US9] Add Home Automation layer support to compiler pipeline (detect layer, route to appropriate generator) in backend/app/compiler/pipeline.py
- [X] T171 [US9] Add layer selector (Board / Home Automation) with BdButton toggle group to ProjectEditorPage in frontend/src/views/portal/ProjectEditorPage.vue
- [X] T172 [US9] Update NodePalette to show Home Assistant entity blocks when Home Automation layer is selected in frontend/src/components/editor/NodePalette.vue
- [X] T173 [US9] Create HA YAML snapshot test fixtures in backend/tests/snapshots/homeassistant/

**Checkpoint**: Full-stack compilation for both ESPHome and Home Assistant targets

---

## Phase 12: User Story 10 — Reusable Modules (Priority: P4)

**Goal**: Create, save, and instantiate reusable block groups as custom modules

**Independent Test**: Select blocks, save as module, instantiate in new location, compile and verify expanded output

### Tests for User Story 10

- [X] T174 [P] [US10] Test module creation, instantiation, and compilation expansion in backend/tests/unit/test_compiler/test_modules.py

### Implementation for User Story 10

- [X] T175 [P] [US10] Create Module model per data-model.md in backend/app/models/module.py
- [X] T176 [US10] Add module CRUD API endpoints in backend/app/api/modules.py
- [X] T177 [US10] Add Alembic migration for Module table in backend/alembic/versions/
- [X] T178 [US10] Add module expansion support to compiler pipeline (expand module instances to sub-graph before IR generation) in backend/app/compiler/pipeline.py
- [X] T179 [US10] Add module creation flow (select blocks, define ports, save) with BdModal and BdInput to EditorCanvas in frontend/src/components/editor/EditorCanvas.vue
- [X] T180 [US10] Add saved modules section with BdCard module preview to NodePalette for drag-and-drop instantiation in frontend/src/components/editor/NodePalette.vue

**Checkpoint**: Reusable modules can be created, instantiated, and correctly compiled

---

## Phase 13: Polish & Cross-Cutting Concerns

**Purpose**: E2e tests, performance tests, security hardening, and production configuration

- [X] T181 [P] Run quickstart.md validation — verify complete setup and first-use workflow end-to-end
- [X] T182 [P] Add rate limiting to public endpoints (leads, auth, blog) in backend/app/main.py
- [X] T183 [P] Add request/response logging middleware in backend/app/main.py
- [X] T184 Create .env.example files for both frontend/ and backend/ with documented variables
- [X] T185 Create production Docker Compose (frontend nginx, backend uvicorn, postgres) in docker/docker-compose.yml with frontend Dockerfile in docker/frontend/Dockerfile
- [X] T186 Add CSRF protection headers and security hardening to backend middleware in backend/app/main.py
- [X] T187 [P] Create Playwright e2e test for US1: navigate all public pages (verify BlackDragon brand presence), submit contact form, verify submission stored in frontend/tests/e2e/public-website.spec.ts
- [X] T188 [P] Create Playwright e2e test for US2: register, login (verify BdLogo on auth pages), create project, duplicate, verify tenant isolation in frontend/tests/e2e/auth.spec.ts
- [X] T189 [P] Create Playwright e2e test for US3: open editor, place blocks (verify branded node styling), connect wires, configure properties, save and reload in frontend/tests/e2e/visual-editor.spec.ts
- [X] T190 Create API load test script validating SC-006 (100 concurrent users) with k6 or locust targeting auth, project CRUD, and compile endpoints in backend/tests/performance/load_test.py
- [X] T191 [P] Create frontend performance test validating SC-004 (100ms editor interactions) using Playwright performance tracing in frontend/tests/e2e/editor-performance.spec.ts

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion (including complete design system)
  - US1 (Phase 3) and US2 (Phase 4) can proceed in parallel
  - US3 (Phase 5) depends on US2 (needs project context for editor)
  - US4 (Phase 6) depends on US2 (needs project context for board config)
  - US5 (Phase 7) depends on US3 + US4 (needs editor diagrams + board config)
  - US6 (Phase 8) depends on US5 (needs compiled artifacts)
  - US7 (Phase 9) depends on US2 (needs project save)
  - US8 (Phase 10) depends on US2 (needs users and projects)
  - US9 (Phase 11) depends on US5 (needs compiler pipeline)
  - US10 (Phase 12) depends on US3 + US5 (needs editor + compiler)
- **Polish (Phase 13)**: Depends on all desired user stories being complete

### User Story Dependencies

- **US1 (P1)**: Can start after Foundational — No dependencies on other stories
- **US2 (P1)**: Can start after Foundational — No dependencies on other stories
- **US3 (P1)**: Depends on US2 (project context for editor)
- **US4 (P2)**: Depends on US2 (project context for board instances)
- **US5 (P2)**: Depends on US3 (diagrams) + US4 (board config)
- **US6 (P3)**: Depends on US5 (compiled artifacts to deploy)
- **US7 (P3)**: Depends on US2 (project save infrastructure) — can run parallel with US3-US6
- **US8 (P3)**: Depends on US2 (user/project data) — can run parallel with US3-US7
- **US9 (P4)**: Depends on US5 (compiler pipeline to extend)
- **US10 (P4)**: Depends on US3 + US5 (editor + compiler for module support)

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Models before schemas
- Schemas before services
- Services before API endpoints
- Backend before frontend (API must exist for frontend to call)
- Migrations after models
- Core implementation before integration

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T004, T005, T006)
- All design system Bd* components (T012–T019) can run in parallel after T007–T011
- US1 and US2 can proceed in parallel after Foundational
- US7 and US8 can proceed in parallel (both only need US2)
- Frontend node components (T092–T099) can all run in parallel
- All compiler node definitions (T125) can run in parallel with registry (T126)
- All compiler unit tests (T120–T124) can run in parallel
- All e2e tests (T187–T191) can run in parallel

---

## Parallel Example: User Story 1

```
After Foundational Phase completes:

Parallel group A:
  T044 (LeadSubmission model) ─┐
  T045 (BlogPost model)       ─┼── T046-T047 (schemas) ── T048-T050 (API) ── T051 (migration)
  T046 (Lead schemas)         ─┘
  T047 (Blog schemas)         ─┘

Parallel group B (independent frontend — consume design system):
  T052 (HomePage)
  T053 (AboutPage)
  T054 (ProductsPage)
  T055 (SolutionsPage)
  T056 (ProjectsPage)
  T057 (BlogPage)

Converge at T058 (ContactPage — needs API) and T042-T043 (integration tests)
```

## Parallel Example: User Story 3

```
After US2 completes:

Backend group:
  T085 (Diagram model) ── T086 (schemas) ── T087 (service) ── T088 (API) ── T089 (migration)

Frontend parallel (after T090-T091):
  T092 (DigitalInputNode)
  T093 (DigitalOutputNode)
  T094 (LogicGateNode)
  T095 (TimerNode)
  T096 (DelayNode)
  T097 (EdgeDetectorNode)
  T098 (DebounceNode)
  T099 (ConstantNode)

Converge at:
  T100 (NodePalette) ── T101 (PropertiesPanel) ── T102 (EditorCanvas) ── T104 (ProjectEditorPage)
```

---

## Implementation Strategy

### MVP Scope (Phases 1–7)

The minimum viable product covers Setup + Foundational + US1 + US2 + US3 + US4 + US5, totaling **T001–T140** (140 tasks). This delivers:
- Full BlackDragon branded public website with blog
- Authenticated multi-tenant portal with branded auth pages
- Visual editor with 12 branded node types
- Board configuration per project
- ESPHome YAML compilation with preview and download

### Incremental Delivery

1. **Sprint 1**: Phase 1 + Phase 2 (Setup + Foundation with complete design system)
2. **Sprint 2**: Phase 3 + Phase 4 in parallel (Public website + Auth/Projects)
3. **Sprint 3**: Phase 5 (Visual editor — largest phase)
4. **Sprint 4**: Phase 6 + Phase 7 (Board config + Compiler)
5. **Sprint 5+**: Phases 8–13 (Deployment, Versioning, Admin, HA, Modules, Polish)
