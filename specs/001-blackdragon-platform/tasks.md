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

- [ ] T001 Create monorepo directory structure per plan.md (frontend/, backend/, docker/, docs/)
- [ ] T002 Initialize Vue 3 + TypeScript project with Vite in frontend/ (package.json, tsconfig.json, vite.config.ts, index.html, src/main.ts, src/App.vue)
- [ ] T003 Initialize Python 3.12+ project with FastAPI in backend/ (pyproject.toml with dependencies: fastapi, sqlalchemy, alembic, pydantic, pydantic-settings, python-jose, passlib, pyyaml, asyncpg, cryptography, httpx, uvicorn)
- [ ] T004 [P] Configure ESLint + Prettier for TypeScript strict mode in frontend/ (.eslintrc.cjs, .prettierrc)
- [ ] T005 [P] Configure Ruff + Black + mypy for Python in backend/ (ruff.toml, mypy.ini)
- [ ] T006 [P] Create Docker Compose development configuration with PostgreSQL 16 service in docker/docker-compose.dev.yml and backend Dockerfile in docker/backend/Dockerfile

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Design System & Layout

- [ ] T007 Configure Tailwind CSS with BlackDragon design tokens (colors, shadows, gradients, typography, animations) in frontend/tailwind.config.ts and frontend/src/assets/styles/main.css
- [ ] T008 [P] Create BdButton component with variants (primary, secondary, ghost, danger) in frontend/src/components/ui/BdButton.vue
- [ ] T009 [P] Create BdCard component with metallic embossed styling in frontend/src/components/ui/BdCard.vue
- [ ] T010 [P] Create BdInput component with validation states in frontend/src/components/ui/BdInput.vue
- [ ] T011 [P] Create BdModal component with overlay and focus trap in frontend/src/components/ui/BdModal.vue
- [ ] T012 [P] Create BdTable component with sorting and pagination in frontend/src/components/ui/BdTable.vue
- [ ] T013 [P] Create BdStatusIndicator component with status colors in frontend/src/components/ui/BdStatusIndicator.vue
- [ ] T014 Create AppHeader with navigation and logo in frontend/src/components/layout/AppHeader.vue
- [ ] T015 [P] Create AppFooter component in frontend/src/components/layout/AppFooter.vue
- [ ] T016 [P] Create AppSidebar for portal navigation in frontend/src/components/layout/AppSidebar.vue
- [ ] T017 Create PortalLayout combining sidebar and content area in frontend/src/components/layout/PortalLayout.vue

### Frontend Core

- [ ] T018 Configure Vue Router with public, auth, and portal route groups (lazy-loaded) in frontend/src/router/index.ts
- [ ] T019 Create API HTTP client with auth interceptor and base URL config in frontend/src/services/api.ts
- [ ] T020 Create TypeScript type definitions for API responses in frontend/src/types/api.ts

### Backend Core

- [ ] T021 Create environment configuration with Pydantic Settings (DATABASE_URL, SECRET_KEY, FERNET_KEY, CORS_ORIGINS, token expiry) in backend/app/config.py
- [ ] T022 Create SQLAlchemy async engine, session factory, and Base declarative class in backend/app/database.py
- [ ] T023 Create Tenant model with fields per data-model.md in backend/app/models/tenant.py
- [ ] T024 [P] Create User model with fields per data-model.md in backend/app/models/user.py
- [ ] T025 Implement password hashing (bcrypt via Passlib), JWT creation/verification (python-jose), and Fernet encryption for credentials in backend/app/core/security.py
- [ ] T026 Create tenant context middleware with SQLAlchemy event filter for automatic tenant_id injection on queries in backend/app/core/tenant.py
- [ ] T027 Create custom exception classes (NotFound, Forbidden, Conflict, ValidationError) and FastAPI exception handlers in backend/app/core/exceptions.py
- [ ] T028 Create FastAPI dependency injection functions (get_db, get_current_user, require_role, get_tenant_context) in backend/app/api/deps.py
- [ ] T029 Create FastAPI application factory with CORS middleware, exception handlers, and router mounting in backend/app/main.py
- [ ] T030 Configure Alembic for async with env.py and create initial migration for Tenant and User tables in backend/alembic/
- [ ] T031 Create database seed script with admin user and test client in backend/app/seed.py

### Testing Infrastructure

- [ ] T032 [P] Create backend test conftest.py with async db session, test client, auth token fixtures, and test tenant setup in backend/tests/conftest.py
- [ ] T033 [P] Configure Vitest for frontend unit tests in frontend/vite.config.ts and frontend/package.json
- [ ] T034 [P] Test tenant isolation middleware filters queries correctly in backend/tests/integration/test_tenant_isolation.py

**Checkpoint**: Foundation ready — user story implementation can now begin in parallel

---

## Phase 3: User Story 1 — Public Website (Priority: P1) 🎯 MVP

**Goal**: Public-facing website with BlackDragon branding, product catalog, and lead capture form

**Independent Test**: Navigate all public pages, verify content renders, submit contact form, confirm submission stored

### Tests for User Story 1

- [ ] T035 [P] [US1] Test lead submission API endpoint (create, list, update status) in backend/tests/integration/test_leads_api.py

### Implementation for User Story 1

- [ ] T036 [P] [US1] Create LeadSubmission model with fields per data-model.md in backend/app/models/lead_submission.py
- [ ] T037 [P] [US1] Create lead Pydantic schemas (LeadCreate, LeadResponse, LeadUpdate) in backend/app/schemas/lead.py
- [ ] T038 [US1] Create lead submission API endpoints (POST /api/leads public, GET/PATCH /api/admin/leads admin) in backend/app/api/leads.py
- [ ] T039 [P] [US1] Create HomePage with hero section, features overview, and CTA in frontend/src/views/public/HomePage.vue
- [ ] T040 [P] [US1] Create AboutPage with company overview and mission in frontend/src/views/public/AboutPage.vue
- [ ] T041 [P] [US1] Create ProductsPage displaying board catalog with specs in frontend/src/views/public/ProductsPage.vue
- [ ] T042 [P] [US1] Create SolutionsPage with automation capabilities in frontend/src/views/public/SolutionsPage.vue
- [ ] T043 [P] [US1] Create ProjectsPage with case studies portfolio in frontend/src/views/public/ProjectsPage.vue
- [ ] T044 [P] [US1] Create BlogPage with article listing in frontend/src/views/public/BlogPage.vue
- [ ] T045 [US1] Create ContactPage with validated lead capture form calling POST /api/leads in frontend/src/views/public/ContactPage.vue
- [ ] T046 [US1] Add Alembic migration for LeadSubmission table in backend/alembic/versions/

**Checkpoint**: Public website fully navigable, contact form stores submissions

---

## Phase 4: User Story 2 — Authentication & Project Management (Priority: P1)

**Goal**: User registration, login, multi-tenant dashboard, project CRUD with duplication and locking

**Independent Test**: Register, log in, create project, duplicate, verify tenant isolation

### Tests for User Story 2

- [ ] T047 [P] [US2] Test auth API endpoints (register, login, refresh, me, invalid credentials) in backend/tests/integration/test_auth_api.py
- [ ] T048 [P] [US2] Test projects API endpoints (CRUD, duplicate, lock/unlock, tenant isolation) in backend/tests/integration/test_projects_api.py

### Implementation for User Story 2

- [ ] T049 [P] [US2] Create auth Pydantic schemas (LoginRequest, RegisterRequest, TokenResponse, UserResponse) in backend/app/schemas/auth.py
- [ ] T050 [P] [US2] Create user Pydantic schemas (UserCreate, UserUpdate, UserList) in backend/app/schemas/user.py
- [ ] T051 [US2] Create auth service (register with tenant creation, login, refresh token) in backend/app/services/auth_service.py
- [ ] T052 [US2] Create auth API endpoints (POST register, POST login, POST refresh, GET me) per contracts/auth.md in backend/app/api/auth.py
- [ ] T053 [P] [US2] Create Property model with fields per data-model.md in backend/app/models/property.py
- [ ] T054 [P] [US2] Create Project model with fields per data-model.md in backend/app/models/project.py
- [ ] T055 [P] [US2] Create property and project Pydantic schemas in backend/app/schemas/project.py
- [ ] T056 [US2] Create project service (create, list, get, update, delete, duplicate, lock/unlock) in backend/app/services/project_service.py
- [ ] T057 [US2] Create properties API endpoints per contracts/properties.md in backend/app/api/properties.py
- [ ] T058 [US2] Create projects API endpoints per contracts/projects.md in backend/app/api/projects.py
- [ ] T059 [US2] Add Alembic migration for Property and Project tables in backend/alembic/versions/
- [ ] T060 [P] [US2] Create auth frontend service (login, register, refresh, logout API calls) in frontend/src/services/auth.service.ts
- [ ] T061 [P] [US2] Create Pinia auth store with token management and user state in frontend/src/stores/auth.ts
- [ ] T062 [P] [US2] Create useAuth composable for login/logout/register actions in frontend/src/composables/useAuth.ts
- [ ] T063 [US2] Create LoginPage with email/password form and error handling in frontend/src/views/auth/LoginPage.vue
- [ ] T064 [US2] Create RegisterPage with registration form and validation in frontend/src/views/auth/RegisterPage.vue
- [ ] T065 [P] [US2] Create project frontend service (CRUD, duplicate API calls) in frontend/src/services/project.service.ts
- [ ] T066 [P] [US2] Create Pinia project store with project list and current project state in frontend/src/stores/project.ts
- [ ] T067 [P] [US2] Create project TypeScript types in frontend/src/types/project.ts
- [ ] T068 [US2] Create DashboardPage with property list and project cards in frontend/src/views/portal/DashboardPage.vue
- [ ] T069 [US2] Create ProjectListPage with filtering and project actions in frontend/src/views/portal/ProjectListPage.vue
- [ ] T070 [US2] Add route guards for authenticated routes in frontend/src/router/index.ts

**Checkpoint**: Users can register, log in, manage properties and projects. Tenant isolation enforced.

---

## Phase 5: User Story 3 — Visual Programming Editor (Priority: P1)

**Goal**: Drag-and-drop blocks-and-wires editor with 12 MVP node types, property editing, wire validation, and auto-save

**Independent Test**: Place blocks, connect with wires, configure properties, save and reload — all data persists

### Tests for User Story 3

- [ ] T071 [P] [US3] Test diagram API endpoints (CRUD, save graph_data, auto-save draft) in backend/tests/integration/test_diagrams_api.py
- [ ] T072 [P] [US3] Test editor store (add/remove nodes, connect edges, update properties) in frontend/tests/unit/stores/editor.spec.ts

### Implementation for User Story 3

- [ ] T073 [P] [US3] Create Diagram model with fields per data-model.md in backend/app/models/diagram.py
- [ ] T074 [P] [US3] Create diagram Pydantic schemas (DiagramCreate, DiagramUpdate, DiagramResponse, DraftSave) in backend/app/schemas/diagram.py
- [ ] T075 [US3] Create diagram service (CRUD, save graph_data, save draft) in backend/app/services/diagram_service.py
- [ ] T076 [US3] Create diagram API endpoints per contracts/diagrams.md in backend/app/api/diagrams.py
- [ ] T077 [US3] Add Alembic migration for Diagram table in backend/alembic/versions/
- [ ] T078 [P] [US3] Create editor TypeScript types (NodeData, EdgeData, PortDefinition, NodeDefinition) in frontend/src/types/editor.ts
- [ ] T079 [P] [US3] Create Pinia editor store with Vue Flow state management in frontend/src/stores/editor.ts
- [ ] T080 [US3] Create DigitalInputNode custom Vue Flow node with signal output port in frontend/src/components/editor/nodes/DigitalInputNode.vue
- [ ] T081 [P] [US3] Create DigitalOutputNode custom Vue Flow node with signal input port in frontend/src/components/editor/nodes/DigitalOutputNode.vue
- [ ] T082 [P] [US3] Create LogicGateNode (AND, OR, NOT, XOR variants) with typed ports in frontend/src/components/editor/nodes/LogicGateNode.vue
- [ ] T083 [P] [US3] Create TimerNode with trigger input and output ports in frontend/src/components/editor/nodes/TimerNode.vue
- [ ] T084 [P] [US3] Create DelayNode with input and delayed output ports in frontend/src/components/editor/nodes/DelayNode.vue
- [ ] T085 [P] [US3] Create EdgeDetectorNode with rising/falling output ports in frontend/src/components/editor/nodes/EdgeDetectorNode.vue
- [ ] T086 [P] [US3] Create DebounceNode with input and debounced output ports in frontend/src/components/editor/nodes/DebounceNode.vue
- [ ] T087 [P] [US3] Create ConstantNode (True/False variants) with value output port in frontend/src/components/editor/nodes/ConstantNode.vue
- [ ] T088 [US3] Create NodePalette component with categorized draggable node list in frontend/src/components/editor/NodePalette.vue
- [ ] T089 [US3] Create PropertiesPanel component for editing selected node properties in frontend/src/components/editor/PropertiesPanel.vue
- [ ] T090 [US3] Create EditorCanvas component integrating Vue Flow with custom nodes, minimap, controls, background grid, and connection validation in frontend/src/components/editor/EditorCanvas.vue
- [ ] T091 [US3] Create useAutoSave composable with debounced draft save (60s interval) in frontend/src/composables/useAutoSave.ts
- [ ] T092 [US3] Create ProjectEditorPage integrating EditorCanvas, NodePalette, and PropertiesPanel in frontend/src/views/portal/ProjectEditorPage.vue

**Checkpoint**: Visual editor fully functional — blocks, wires, properties, save/load, auto-save all working

---

## Phase 6: User Story 4 — Board Configuration (Priority: P2)

**Goal**: Board catalog browsing, board instance creation per project, I/O channel configuration with GPIO/electrical options

**Independent Test**: Add board from catalog, configure I/O channels, verify channels appear as editor blocks

### Tests for User Story 4

- [ ] T093 [P] [US4] Test boards API endpoints (catalog CRUD, instance CRUD, channel config, GPIO conflict detection) in backend/tests/integration/test_boards_api.py

### Implementation for User Story 4

- [ ] T094 [P] [US4] Create BoardModel and BoardModelChannel models per data-model.md in backend/app/models/board_model.py
- [ ] T095 [P] [US4] Create BoardInstance and BoardInstanceChannel models per data-model.md in backend/app/models/board_instance.py
- [ ] T096 [P] [US4] Create board Pydantic schemas (BoardModelResponse, BoardInstanceCreate, ChannelConfig) in backend/app/schemas/board.py
- [ ] T097 [US4] Create board service (catalog listing, instance CRUD, channel update, GPIO conflict check) in backend/app/services/board_service.py
- [ ] T098 [US4] Create boards API endpoints per contracts/boards.md in backend/app/api/boards.py
- [ ] T099 [US4] Add Alembic migration for BoardModel, BoardModelChannel, BoardInstance, BoardInstanceChannel tables in backend/alembic/versions/
- [ ] T100 [US4] Add board model seed data (sample BlackDragon boards with I/O definitions) to backend/app/seed.py
- [ ] T101 [P] [US4] Create board frontend service (catalog, instance CRUD, channel config API calls) in frontend/src/services/board.service.ts
- [ ] T102 [P] [US4] Create board TypeScript types in frontend/src/types/board.ts
- [ ] T103 [P] [US4] Create Pinia board store with catalog and instance state in frontend/src/stores/board.ts
- [ ] T104 [US4] Create BoardSelector component for adding boards from catalog in frontend/src/components/boards/BoardSelector.vue
- [ ] T105 [US4] Create IoChannelEditor component for configuring GPIO, pull mode, debounce, inverted in frontend/src/components/boards/IoChannelEditor.vue
- [ ] T106 [US4] Create BoardConfigurator component combining board metadata and channel editors in frontend/src/components/boards/BoardConfigurator.vue
- [ ] T107 [US4] Create BoardCatalogPage displaying available boards and project board instances in frontend/src/views/portal/BoardCatalogPage.vue

**Checkpoint**: Boards configurable per project, I/O channels mapped to GPIO pins, channels available as editor blocks

---

## Phase 7: User Story 5 — ESPHome YAML Compilation (Priority: P2)

**Goal**: Compiler pipeline (validate → IR → optimize → generate), ESPHome YAML output, preview and download

**Independent Test**: Create diagram with DigitalInput → AND → DigitalOutput, compile, verify valid ESPHome YAML with correct GPIO mappings

### Tests for User Story 5

- [ ] T108 [P] [US5] Test graph validator (unconnected ports, type mismatches, GPIO conflicts, cycles) in backend/tests/unit/test_compiler/test_validator.py
- [ ] T109 [P] [US5] Test IR generation (topological sort, type resolution) in backend/tests/unit/test_compiler/test_ir.py
- [ ] T110 [P] [US5] Test optimizer (dead-node elimination, constant folding) in backend/tests/unit/test_compiler/test_optimizer.py
- [ ] T111 [P] [US5] Test ESPHome generator with YAML snapshot comparisons in backend/tests/unit/test_compiler/test_esphome_generator.py
- [ ] T112 [P] [US5] Test compile API endpoint (success, validation errors, artifact retrieval) in backend/tests/integration/test_compiler_api.py

### Implementation for User Story 5

- [ ] T113 [P] [US5] Create node type definitions (DigitalInput, DigitalOutput, AND, OR, NOT, XOR, Timer, Delay, EdgeDetector, Debounce, ConstantTrue, ConstantFalse) in backend/app/compiler/nodes/digital_io.py, logic_gates.py, timing.py, constants.py
- [ ] T114 [P] [US5] Create node type registry with port definitions and property schemas in backend/app/compiler/nodes/registry.py
- [ ] T115 [US5] Create semantic validator (connectivity, type compatibility, GPIO conflicts, cycle detection) in backend/app/compiler/validator.py
- [ ] T116 [US5] Create Intermediate Representation with IRNode, IREdge, and topological sort in backend/app/compiler/ir.py
- [ ] T117 [US5] Create IR optimizer (dead-node elimination, constant folding) in backend/app/compiler/optimizer.py
- [ ] T118 [US5] Create abstract base generator interface in backend/app/compiler/generators/base.py
- [ ] T119 [US5] Create ESPHome YAML generator mapping IR nodes to ESPHome components (binary_sensor, switch, output, lambda, filters) in backend/app/compiler/generators/esphome.py
- [ ] T120 [US5] Create compiler pipeline orchestrator (validate → IR → optimize → generate) in backend/app/compiler/pipeline.py
- [ ] T121 [P] [US5] Create CompilationArtifact model per data-model.md in backend/app/models/compilation_artifact.py
- [ ] T122 [P] [US5] Create compiler Pydantic schemas (CompileRequest, CompileResponse, ArtifactResponse, ValidationResult) in backend/app/schemas/compiler.py
- [ ] T123 [US5] Create compiler API endpoints (POST compile, GET artifacts, GET download, POST validate, GET node definitions) per contracts/compiler.md in backend/app/api/compiler.py
- [ ] T124 [US5] Add Alembic migration for CompilationArtifact table in backend/alembic/versions/
- [ ] T125 [P] [US5] Create compiler frontend service (compile, validate, get artifacts, download API calls) in frontend/src/services/compiler.service.ts
- [ ] T126 [US5] Create YamlPreviewPage with syntax-highlighted YAML display and download button in frontend/src/views/portal/YamlPreviewPage.vue
- [ ] T127 [US5] Add compile and validate buttons to ProjectEditorPage with error highlighting on diagram nodes in frontend/src/views/portal/ProjectEditorPage.vue
- [ ] T128 [US5] Create YAML snapshot test fixtures (expected ESPHome output for standard diagrams) in backend/tests/snapshots/esphome/

**Checkpoint**: Diagrams compile to valid ESPHome YAML, preview renders, files downloadable

---

## Phase 8: User Story 6 — OTA Deployment (Priority: P3)

**Goal**: Deploy compiled ESPHome configurations to ESP32 boards via OTA, track progress and status

**Independent Test**: Compile diagram, initiate OTA deployment, monitor progress, verify success/failure reporting

### Tests for User Story 6

- [ ] T129 [P] [US6] Test deployment API endpoints (create, list, status, cancel) in backend/tests/integration/test_deployments_api.py

### Implementation for User Story 6

- [ ] T130 [P] [US6] Create Deployment model per data-model.md in backend/app/models/deployment.py
- [ ] T131 [P] [US6] Create Credential model per data-model.md in backend/app/models/credential.py
- [ ] T132 [P] [US6] Create deployment Pydantic schemas (DeployRequest, DeployResponse, DeploymentStatus) in backend/app/schemas/deployment.py
- [ ] T133 [US6] Create deployment service (initiate OTA via ESPHome subprocess, track progress, update status) in backend/app/services/deployment_service.py
- [ ] T134 [US6] Create deployment API endpoints per contracts/deployments.md in backend/app/api/deployments.py
- [ ] T135 [US6] Add Alembic migration for Deployment and Credential tables in backend/alembic/versions/
- [ ] T136 [P] [US6] Create deployment frontend service (deploy, list, status, cancel API calls) in frontend/src/services/deployment.service.ts
- [ ] T137 [US6] Create DeploymentPage with board selection, deploy button, progress indicator, and history table in frontend/src/views/portal/DeploymentPage.vue

**Checkpoint**: End-to-end flow from design to deployed firmware on ESP32 boards

---

## Phase 9: User Story 7 — Project Versioning (Priority: P3)

**Goal**: Save named versions, view history, roll back to previous versions

**Independent Test**: Save version, make changes, save again, view history, roll back to first version

### Tests for User Story 7

- [ ] T138 [P] [US7] Test version API endpoints (save version, list history, rollback) in backend/tests/integration/test_versions_api.py

### Implementation for User Story 7

- [ ] T139 [P] [US7] Create ProjectVersion model per data-model.md in backend/app/models/project_version.py
- [ ] T140 [US7] Add version save, list history, and rollback methods to project service in backend/app/services/project_service.py
- [ ] T141 [US7] Add version API endpoints (POST save, GET list, POST rollback) to projects router per contracts/projects.md in backend/app/api/projects.py
- [ ] T142 [US7] Add Alembic migration for ProjectVersion table in backend/alembic/versions/
- [ ] T143 [US7] Add version history panel with rollback action to ProjectEditorPage in frontend/src/views/portal/ProjectEditorPage.vue

**Checkpoint**: Project versioning with save, history, and rollback fully functional

---

## Phase 10: User Story 8 — Administrator Management (Priority: P3)

**Goal**: Admin dashboard with user management, cross-tenant project access, board catalog management, audit logs

**Independent Test**: Log in as admin, view all clients, access client project, add board to catalog, view audit logs

### Tests for User Story 8

- [ ] T144 [P] [US8] Test admin API endpoints (list users, update user, list tenants, list audit logs, RBAC enforcement) in backend/tests/integration/test_admin_api.py

### Implementation for User Story 8

- [ ] T145 [P] [US8] Create AuditLog model per data-model.md in backend/app/models/audit_log.py
- [ ] T146 [US8] Create audit service (log action, query logs) in backend/app/services/audit_service.py
- [ ] T147 [US8] Create user service (list, update, deactivate) in backend/app/services/user_service.py
- [ ] T148 [US8] Create admin API endpoints (users, tenants, audit logs) per contracts/admin.md in backend/app/api/admin.py
- [ ] T149 [US8] Add Alembic migration for AuditLog table in backend/alembic/versions/
- [ ] T150 [US8] Integrate audit logging into project, deployment, and auth services in backend/app/services/
- [ ] T151 [P] [US8] Create UsersPage with user list, role editing, and active/deactivate toggle in frontend/src/views/portal/admin/UsersPage.vue
- [ ] T152 [P] [US8] Create ClientsPage with tenant list and cross-tenant project access in frontend/src/views/portal/admin/ClientsPage.vue
- [ ] T153 [US8] Create BoardManagementPage with board model CRUD and I/O channel definition editor in frontend/src/views/portal/admin/BoardManagementPage.vue
- [ ] T154 [US8] Create ProfilePage with user profile display and password change in frontend/src/views/portal/ProfilePage.vue

**Checkpoint**: Administrators can manage users, boards, and view audit logs

---

## Phase 11: User Story 9 — Home Automation Logic (Priority: P4)

**Goal**: Home Automation programming layer with board entities and Home Assistant YAML generation

**Independent Test**: Switch to Home Automation layer, create automation with board entities and Timer, compile, verify Home Assistant YAML

### Tests for User Story 9

- [ ] T155 [P] [US9] Test Home Assistant generator with YAML snapshot comparisons in backend/tests/unit/test_compiler/test_homeassistant_generator.py

### Implementation for User Story 9

- [ ] T156 [US9] Create Home Assistant YAML generator mapping IR nodes to HA automations, scripts, and helpers in backend/app/compiler/generators/homeassistant.py
- [ ] T157 [US9] Add Home Automation layer support to compiler pipeline (detect layer, route to appropriate generator) in backend/app/compiler/pipeline.py
- [ ] T158 [US9] Add layer selector (Board / Home Automation) to ProjectEditorPage in frontend/src/views/portal/ProjectEditorPage.vue
- [ ] T159 [US9] Update NodePalette to show Home Assistant entity blocks when Home Automation layer is selected in frontend/src/components/editor/NodePalette.vue
- [ ] T160 [US9] Create HA YAML snapshot test fixtures in backend/tests/snapshots/homeassistant/

**Checkpoint**: Full-stack compilation for both ESPHome and Home Assistant targets

---

## Phase 12: User Story 10 — Reusable Modules (Priority: P4)

**Goal**: Create, save, and instantiate reusable block groups as custom modules

**Independent Test**: Select blocks, save as module, instantiate in new location, compile and verify expanded output

### Tests for User Story 10

- [ ] T161 [P] [US10] Test module creation, instantiation, and compilation expansion in backend/tests/unit/test_compiler/test_modules.py

### Implementation for User Story 10

- [ ] T162 [P] [US10] Create Module model per data-model.md in backend/app/models/module.py
- [ ] T163 [US10] Add module CRUD API endpoints in backend/app/api/modules.py
- [ ] T164 [US10] Add Alembic migration for Module table in backend/alembic/versions/
- [ ] T165 [US10] Add module expansion support to compiler pipeline (expand module instances to sub-graph before IR generation) in backend/app/compiler/pipeline.py
- [ ] T166 [US10] Add module creation flow (select blocks, define ports, save) to EditorCanvas in frontend/src/components/editor/EditorCanvas.vue
- [ ] T167 [US10] Add saved modules section to NodePalette for drag-and-drop instantiation in frontend/src/components/editor/NodePalette.vue

**Checkpoint**: Reusable modules can be created, instantiated, and correctly compiled

---

## Phase 13: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T168 [P] Run quickstart.md validation — verify complete setup and first-use workflow end-to-end
- [ ] T169 [P] Add rate limiting to public endpoints (leads, auth) in backend/app/main.py
- [ ] T170 [P] Add request/response logging middleware in backend/app/main.py
- [ ] T171 Create .env.example files for both frontend/ and backend/ with documented variables
- [ ] T172 Create production Docker Compose (frontend nginx, backend uvicorn, postgres) in docker/docker-compose.yml with frontend Dockerfile in docker/frontend/Dockerfile
- [ ] T173 Add CSRF protection headers and security hardening to backend middleware in backend/app/main.py

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
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
- All design system components marked [P] can run in parallel (T008–T013)
- All backend models within a phase marked [P] can run in parallel
- US1 and US2 can proceed in parallel after Foundational
- US7 and US8 can proceed in parallel (both only need US2)
- Frontend node components (T080–T087) can all run in parallel
- All compiler node definitions (T113) can run in parallel with registry (T114)
- All compiler unit tests (T108–T112) can run in parallel

---

## Parallel Example: User Story 1

```
After Foundational Phase completes:

Parallel group A:
  T036 (LeadSubmission model) ─┐
  T037 (Lead schemas)         ─┼── then T038 (Lead API) ── then T045 (ContactPage)
                               │
Parallel group B (independent):
  T039 (HomePage)
  T040 (AboutPage)
  T041 (ProductsPage)
  T042 (SolutionsPage)
  T043 (ProjectsPage)
  T044 (BlogPage)

All converge at T046 (migration) and T035 (integration test)
```

## Parallel Example: User Story 5

```
After US3 + US4 complete:

Parallel group A (node definitions):
  T113 (node type files) ── T114 (registry)

Parallel group B (tests — write first, fail):
  T108 (test_validator)
  T109 (test_ir)
  T110 (test_optimizer)
  T111 (test_esphome_generator)

Then sequential pipeline:
  T115 (validator) → T116 (IR) → T117 (optimizer) → T118 (base generator) → T119 (ESPHome generator) → T120 (pipeline)

Then API + frontend:
  T121 (model) + T122 (schemas) → T123 (API) → T125 (frontend service) → T126 (preview page) + T127 (editor integration)

  T112 (API integration test) runs after T123
  T128 (snapshot fixtures) after T119
```

---

## Implementation Strategy

### MVP Scope (Suggested)

**Minimum viable product = Phase 1 + Phase 2 + US1 + US2 + US3 + US4 + US5**

This delivers:
- Public website with branding and lead capture
- User auth with multi-tenant isolation
- Visual editor with 12 node types
- Board configuration with I/O channel setup
- ESPHome YAML compilation and preview

**Tasks**: T001–T128 (128 tasks)

### Incremental Delivery

1. **MVP** (Phases 1–7): Core platform with visual editor and ESPHome compilation
2. **Operations** (Phases 8–10): OTA deployment, versioning, admin tools
3. **Expansion** (Phases 11–12): Home Assistant integration, reusable modules
4. **Hardening** (Phase 13): Polish, security, production readiness
