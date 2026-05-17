# Feature Specification: BlackDragon SaaS Platform

**Feature Branch**: `001-blackdragon-platform`

**Created**: 2026-05-16

**Status**: Draft

**Input**: Full-stack SaaS web application serving as BlackDragon's public website and a secure multi-tenant client portal with a visual programming environment for smart home automation using Home Assistant and custom ESP32-based boards.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Public Website Visitor Explores BlackDragon (Priority: P1)

A prospective client visits the BlackDragon public website to learn about the company, browse available hardware boards and automation solutions, view completed project case studies, and submit a contact or lead capture form to request services.

**Why this priority**: The public website is BlackDragon's commercial storefront. Without it, there is no channel for acquiring new clients. It is the lowest-complexity, highest-visibility deliverable and establishes the brand presence.

**Independent Test**: Navigate to each public page (Home, About, Products, Solutions, Projects, Blog, Contact), verify content renders correctly, submit the contact form with valid data, and confirm the submission is recorded.

**Acceptance Scenarios**:

1. **Given** a visitor on the Home page, **When** they navigate to Products, **Then** they see a catalog of BlackDragon hardware boards with descriptions and specifications.
2. **Given** a visitor on the Contact page, **When** they fill out the lead capture form with valid information and submit it, **Then** the system confirms receipt and stores the submission for administrator review.
3. **Given** a visitor on the Solutions page, **When** they browse automation solutions, **Then** they see descriptions of technical capabilities and supported use cases.
4. **Given** a visitor on the Projects page, **When** they view a case study, **Then** they see a summary of the project scope, hardware used, and outcomes achieved.

---

### User Story 2 - Client Authenticates and Manages Projects (Priority: P1)

A registered client logs into the BlackDragon portal, views a dashboard of their properties and automation projects, creates a new project for a property, and manages existing projects (save, load, duplicate, delete).

**Why this priority**: Authentication and project management are prerequisites for every portal feature. Without them, no client work can happen. This story establishes the multi-tenant security boundary.

**Independent Test**: Register a new user, log in, create a project, save it, reload the dashboard, verify the project appears, duplicate it, and confirm both projects exist. Verify that one client cannot see another client's projects.

**Acceptance Scenarios**:

1. **Given** valid credentials, **When** a client logs in, **Then** they see a dashboard listing only their own properties and projects.
2. **Given** a logged-in client, **When** they create a new project for a property, **Then** the project appears in their dashboard and is persisted.
3. **Given** an existing project, **When** the client duplicates it, **Then** a new independent copy is created with all diagram data preserved.
4. **Given** a client session, **When** another client's project ID is accessed directly, **Then** access is denied with a forbidden response.
5. **Given** a client with multiple projects, **When** they open a project, **Then** the most recent saved version loads in the editor.

---

### User Story 3 - Client Designs Automation in Visual Editor (Priority: P1)

A client opens a project and uses the visual programming editor to design automation logic. They drag blocks (Digital Input, Digital Output, AND, OR, NOT, Timer, etc.) onto a canvas, connect them with wires, configure block properties (GPIO assignments, pull-up/pull-down, debounce, inverted logic), and organize their diagram.

**Why this priority**: The visual editor is the core product differentiator. It is the primary reason clients use the platform. Without it, the portal has no functional value.

**Independent Test**: Open the editor, place a Digital Input block and a Digital Output block, connect them with a wire, configure GPIO pin assignments and pull-up settings, save the diagram, reload it, and verify all blocks, connections, and configurations persist correctly.

**Acceptance Scenarios**:

1. **Given** an open project editor, **When** a client drags a Digital Input block onto the canvas, **Then** the block appears at the drop position with default properties.
2. **Given** two blocks on the canvas, **When** the client draws a wire from an output port to an input port, **Then** a connection is established and visually rendered.
3. **Given** a Digital Input block, **When** the client opens its properties panel, **Then** they can configure the GPIO pin, pull-up/pull-down mode, debounce time, inverted logic, and a human-readable name.
4. **Given** a completed diagram, **When** the client saves the project, **Then** all blocks, wires, positions, and configurations are persisted.
5. **Given** a saved diagram, **When** the client reloads the project, **Then** the diagram restores exactly as saved with all connections and configurations intact.
6. **Given** an invalid connection (incompatible port types), **When** the client attempts to draw a wire, **Then** the connection is rejected with a clear error message.

---

### User Story 4 - Client Configures Boards for a Property (Priority: P2)

A client selects which BlackDragon hardware board models are installed in their property, assigns names and metadata to each board instance, and configures the inputs and outputs available on each board (naming, GPIO mapping, electrical options).

**Why this priority**: Board configuration provides the hardware context required by the visual editor and the compiler. It bridges the gap between physical installation and software design. It depends on authentication (US2) but is a prerequisite for meaningful compilation (US5).

**Independent Test**: Open a project, add a board from the catalog, name it, configure its I/O channels with GPIO assignments and options, save, and verify the configuration persists. Confirm that the configured I/O entities appear as available blocks in the visual editor.

**Acceptance Scenarios**:

1. **Given** a project, **When** the client adds a board model from the catalog, **Then** a new board instance is created with default I/O configuration.
2. **Given** a board instance, **When** the client assigns names and GPIO pins to inputs and outputs, **Then** the configuration is saved and reflected in the editor's available blocks.
3. **Given** a board instance, **When** the client configures electrical options (pull-up, pull-down, inverted logic, debounce), **Then** the options are persisted per I/O channel.
4. **Given** a board with configured I/O, **When** the client opens the visual editor, **Then** the board's named inputs and outputs appear as draggable blocks.

---

### User Story 5 - Client Compiles Diagrams to ESPHome YAML (Priority: P2)

A client completes an automation diagram and triggers compilation. The system validates the diagram, generates ESPHome YAML configuration files for each configured board, and presents a preview. The client can download the generated YAML files.

**Why this priority**: Compilation transforms visual designs into deployable artifacts. Without it, the visual editor produces nothing actionable. This story delivers the first tangible output of the platform.

**Independent Test**: Create a diagram with a Digital Input connected through an AND gate to a Digital Output, assign it to a configured board, compile, verify the generated ESPHome YAML is syntactically valid and contains the correct GPIO mappings and logic, and download the file.

**Acceptance Scenarios**:

1. **Given** a valid diagram assigned to configured boards, **When** the client triggers compilation, **Then** the system produces ESPHome YAML files — one per board.
2. **Given** a diagram with validation errors (unconnected ports, missing GPIO assignments), **When** the client triggers compilation, **Then** the system displays specific error messages identifying each problem and its location in the diagram.
3. **Given** successfully generated YAML, **When** the client opens the preview, **Then** they see the complete ESPHome configuration with correct pin mappings, binary sensor definitions, switch definitions, and automation logic.
4. **Given** a YAML preview, **When** the client downloads the file, **Then** a correctly formatted YAML file is saved to their device.

---

### User Story 6 - Client Deploys to ESP32 Boards via OTA (Priority: P3)

After successful compilation, a client initiates deployment of the generated ESPHome configuration to a target ESP32 board via Over-The-Air (OTA) update. The system shows deployment progress and reports success or failure.

**Why this priority**: Deployment closes the loop from design to running hardware. It is high-value but depends on compilation (US5) and board configuration (US4). It also requires network access to target devices, adding complexity.

**Independent Test**: Compile a valid diagram for a board, initiate OTA deployment to a test ESP32 device, monitor the progress indicator, and verify the device receives and applies the new firmware configuration.

**Acceptance Scenarios**:

1. **Given** a compiled ESPHome configuration and a reachable ESP32 device, **When** the client initiates deployment, **Then** the system begins OTA upload and displays progress.
2. **Given** an ongoing deployment, **When** the upload completes successfully, **Then** the system confirms successful deployment and the device restarts with the new configuration.
3. **Given** an unreachable device, **When** the client initiates deployment, **Then** the system reports a connection error within a reasonable timeout period.
4. **Given** a deployment failure mid-upload, **When** the error occurs, **Then** the system reports the failure reason and the device remains on its previous configuration.

---

### User Story 7 - Client Manages Project Versions (Priority: P3)

A client saves versions of their project over time. They can view version history, compare versions, and roll back to a previous version if needed.

**Why this priority**: Versioning provides safety and auditability. Clients can experiment with changes knowing they can revert. It builds on save/load (US2) and is important for professional use but not critical for initial functionality.

**Independent Test**: Open a project, make changes, save a new version, make more changes, save again, view version history showing both versions with timestamps, and roll back to the first version confirming the diagram reverts.

**Acceptance Scenarios**:

1. **Given** a project with unsaved changes, **When** the client saves, **Then** a new version is created with a timestamp and the previous version is preserved.
2. **Given** a project with multiple versions, **When** the client views version history, **Then** they see a chronological list of versions with timestamps and optional descriptions.
3. **Given** a version history entry, **When** the client selects rollback, **Then** the project reverts to that version's state and a confirmation is displayed.
4. **Given** a rollback, **When** the client saves after rolling back, **Then** a new version is created (history is not rewritten).

---

### User Story 8 - Administrator Manages Users and Boards (Priority: P3)

An administrator logs into the portal with elevated permissions. They can view and manage all client accounts, access any client's projects for support purposes, and manage the board catalog (add, edit, retire board models and their I/O definitions).

**Why this priority**: Administrative capabilities are essential for operations but are not needed for the initial client-facing workflow. Client self-service (US2–US7) delivers value independently.

**Independent Test**: Log in as an administrator, view the list of all clients, open a client's project, verify full access. Add a new board model to the catalog with I/O definitions, and verify it becomes available for client project configuration.

**Acceptance Scenarios**:

1. **Given** an administrator login, **When** they access the dashboard, **Then** they see all clients and all projects across the platform.
2. **Given** an administrator viewing a client's project, **When** they open the editor, **Then** they can view and edit the client's diagrams.
3. **Given** the board catalog, **When** an administrator adds a new board model with defined inputs and outputs, **Then** the board becomes available in the board selection step for all client projects.
4. **Given** an existing board model, **When** an administrator retires it, **Then** it no longer appears for new board selections but remains in existing projects that use it.
5. **Given** a client user, **When** they attempt to access administrator functions, **Then** access is denied.

---

### User Story 9 - Client Programs Home Automation Logic (Priority: P4)

A client creates system-wide automation rules that run on Home Assistant. They use the visual editor with entities from all installed boards and Home Assistant integrations to define automations, scripts, and helpers. The compiler generates Home Assistant configuration.

**Why this priority**: Home Assistant automation expands the platform beyond board-level logic to full home automation. It depends on board configuration (US4) and the visual editor (US3). It is a significant feature expansion beyond the core ESP32 workflow.

**Independent Test**: Open a project with configured boards, switch to the Home Automation layer, create an automation using board entities and a Timer block, compile, and verify the generated Home Assistant YAML contains correct automation definitions with triggers, conditions, and actions.

**Acceptance Scenarios**:

1. **Given** a project with configured boards, **When** the client switches to the Home Automation programming layer, **Then** they see all board entities and Home Assistant integration entities as available blocks.
2. **Given** a Home Automation diagram, **When** the client compiles, **Then** the system generates Home Assistant automation YAML with correct trigger, condition, and action definitions.
3. **Given** both board-level and home-level diagrams, **When** the client compiles the full project, **Then** the system generates both ESPHome YAML and Home Assistant YAML as separate artifacts.

---

### User Story 10 - Client Creates Reusable Modules (Priority: P4)

A client creates reusable automation modules (custom blocks) from existing diagram sections. These modules can be instantiated multiple times across projects, promoting consistency and reducing duplication.

**Why this priority**: Reusable modules are a productivity enhancement for power users. They depend on a mature visual editor (US3) and are not required for basic automation workflows.

**Independent Test**: Select a group of connected blocks in a diagram, save them as a reusable module with defined input and output ports, instantiate the module in another location, and verify it behaves identically to the original block group.

**Acceptance Scenarios**:

1. **Given** a group of connected blocks, **When** the client saves them as a module, **Then** a reusable module is created with named input and output ports.
2. **Given** a saved module, **When** the client drags it onto a canvas, **Then** it appears as a single block with the defined ports.
3. **Given** an instantiated module, **When** the client compiles, **Then** the module's internal logic is expanded correctly in the generated output.
4. **Given** a module definition update, **When** the client updates the module, **Then** existing instances can be updated to the new definition or kept at the previous version.

---

### Edge Cases

- What happens when a client deletes a board that is referenced in existing diagrams? The system MUST warn the client and identify all affected diagrams before allowing deletion.
- What happens when two users edit the same project simultaneously? The system MUST prevent concurrent editing conflicts by locking the project for the active editor or providing conflict resolution.
- What happens when a diagram references a GPIO pin that conflicts with another assignment on the same board? The system MUST detect duplicate GPIO assignments during validation and report specific conflicts.
- What happens when deployment fails partway through an OTA update? The device MUST remain on its previous working configuration. The system MUST report the failure and allow retry.
- What happens when a compiled YAML file exceeds ESPHome size limits for a board? The system MUST report the constraint violation during compilation with guidance on reducing complexity.
- What happens when a client's session expires while editing? The system MUST auto-save draft state periodically so no more than 60 seconds of work is lost.
- What happens when the board catalog is updated and existing projects reference outdated board definitions? Existing projects MUST continue to function with their original board definitions. Migration to updated definitions MUST be explicit and optional.

## Requirements *(mandatory)*

### Functional Requirements

**Public Website**

- **FR-001**: System MUST present a public website with pages for Home, About, Products, Solutions, Projects, Blog, and Contact.
- **FR-002**: System MUST display a catalog of BlackDragon hardware boards with specifications, descriptions, and images on the Products page.
- **FR-003**: System MUST provide a lead capture form on the Contact page that validates input, confirms submission, and stores entries for administrator review.
- **FR-004**: System MUST support a blog section backed by a database-stored content model with published articles manageable by administrators. An optional documentation section MAY be added as a future enhancement.

**Authentication and Authorization**

- **FR-005**: System MUST support user registration and login with email and password credentials.
- **FR-006**: System MUST enforce role-based access control with at least two roles: Client User and Administrator.
- **FR-007**: System MUST issue session tokens upon successful authentication and require valid tokens for all portal operations.
- **FR-008**: System MUST enforce multi-tenant data isolation so that client users can only access their own properties and projects.

**Project Management**

- **FR-009**: Client users MUST be able to create, open, save, duplicate, and delete automation projects.
- **FR-010**: Each project MUST be associated with a property and a client account.
- **FR-011**: System MUST persist all project data including diagrams, board configurations, and metadata.
- **FR-012**: System MUST support project versioning with the ability to view history and roll back to previous versions.

**Board Configuration**

- **FR-013**: System MUST maintain a catalog of BlackDragon hardware board models with predefined I/O specifications.
- **FR-014**: Client users MUST be able to add board instances to a project from the catalog.
- **FR-015**: Client users MUST be able to configure each board instance's I/O channels with names, GPIO pin assignments, pull-up/pull-down mode, debounce time, and inverted logic.
- **FR-016**: Configured board I/O entities MUST appear as available blocks in the visual editor.

**Visual Programming Editor**

- **FR-017**: System MUST provide a drag-and-drop visual editor with a blocks-and-wires paradigm.
- **FR-018**: System MUST support the following block types in the MVP: Digital Input, Digital Output, Constant True, Constant False, AND, OR, NOT, XOR, Timer, Delay, Edge Detector, and Debounce.
- **FR-019**: Users MUST be able to connect blocks by drawing wires between compatible output and input ports.
- **FR-020**: Users MUST be able to configure block properties including name, GPIO assignment, timing parameters, and electrical options via a properties panel.
- **FR-021**: System MUST validate connections for type compatibility and reject invalid wires with clear feedback.
- **FR-022**: System MUST auto-save diagram drafts periodically (at most every 60 seconds) to prevent data loss.

**Multi-Layer Programming**

- **FR-023**: System MUST support a Board Internal Logic programming layer for logic that executes on the ESP32 via ESPHome.
- **FR-024**: System MUST support a Home Automation Logic programming layer for automations that execute on Home Assistant.
- **FR-025**: The Home Automation layer MUST expose entities from all configured boards and supported Home Assistant integrations.

**Compilation**

- **FR-026**: System MUST validate diagrams before compilation, reporting all errors with specific locations and descriptions.
- **FR-027**: System MUST compile valid Board Internal Logic diagrams into ESPHome YAML configuration files, one per board.
- **FR-028**: System MUST compile valid Home Automation diagrams into Home Assistant automation, script, and helper YAML configurations.
- **FR-029**: The compiler MUST use a modular pipeline: Visual Graph JSON → Semantic Validation → Intermediate Representation → Optimization → Target Code Generators.
- **FR-030**: System MUST allow users to preview generated YAML before deployment or download.
- **FR-031**: System MUST allow users to download generated YAML files.

**Deployment**

- **FR-032**: System MUST support OTA deployment of compiled ESPHome configurations to ESP32 boards.
- **FR-033**: System MUST display deployment progress and report success or failure.
- **FR-034**: System MUST handle deployment failures gracefully, ensuring target devices remain on their previous working configuration.

**Reusable Modules**

- **FR-035**: Users MUST be able to create reusable modules from groups of connected blocks.
- **FR-036**: Reusable modules MUST be instantiable as single blocks with defined input and output ports.

**Administration**

- **FR-037**: Administrators MUST be able to view and manage all client accounts.
- **FR-038**: Administrators MUST be able to access and edit any client's projects.
- **FR-039**: Administrators MUST be able to manage the board catalog (add, edit, retire board models).
- **FR-040**: System MUST maintain audit logs for deployments, project changes, and administrative actions.

**Security**

- **FR-041**: System MUST store credentials for Home Assistant and ESPHome devices securely using encryption at rest.
- **FR-042**: System MUST enforce tenant data isolation at the data layer, preventing cross-tenant data access regardless of application logic.

**Brand Identity & Design System**

- **FR-043**: All frontend pages and components MUST strictly follow the BlackDragon brand identity, using ultra-dark backgrounds (#050505 primary, #0A0A0A secondary), matte black and charcoal surfaces, and metallic graphite/silver accents throughout the application.
- **FR-044**: The design system MUST incorporate circuit-board-inspired patterns and details as decorative elements in backgrounds, dividers, card borders, and section separators across both public and portal views.
- **FR-045**: All typography MUST use a futuristic technical typeface consistent with premium engineering software aesthetics. Font weights, sizes, and spacing MUST be defined as design tokens and applied uniformly.
- **FR-046**: The BlackDragon logo MUST be displayed consistently in the main navigation header, authentication pages (login, register), the portal dashboard, and the public website landing page.
- **FR-047**: All reusable UI components (buttons, cards, inputs, modals, tables, status indicators) MUST use the BlackDragon metallic embossed styling with subtle glow effects and brushed-metal gradients as defined in the design token system.
- **FR-048**: All visual programming editor nodes MUST conform to the BlackDragon design system with dark node bodies, color-coded port indicators by data type, selection glow effects, and consistent node header styling.
- **FR-049**: The public website MUST convey a premium engineering brand presence through hero sections, product showcases, and marketing pages that use the full BlackDragon visual vocabulary (dark backgrounds, metallic accents, circuit patterns, technical typography).
- **FR-050**: The design system MUST define and enforce a complete set of Tailwind CSS design tokens (colors, shadows, gradients, animations, spacing, typography) that all components and pages consume, ensuring no ad-hoc styling overrides occur.

### Key Entities

- **User**: A person who accesses the platform. Has a role (Client or Administrator), email, credentials, and belongs to one organization/tenant.
- **Tenant**: An organizational boundary for data isolation. Each client company or individual is a tenant. All data belongs to exactly one tenant.
- **Property**: A physical location (home, building) owned by a tenant. Contains one or more projects. Has address and descriptive metadata.
- **Project**: An automation design workspace for a property. Contains board configurations, diagrams, compilation artifacts, and version history.
- **Board Model**: A hardware product definition in the catalog. Specifies model name, available I/O channels, GPIO mapping constraints, and supported features.
- **Board Instance**: A specific board model assigned to a project with user-configured I/O channels (names, GPIO pins, electrical options).
- **Diagram**: A visual graph of connected blocks representing automation logic. Belongs to a project and a programming layer (Board or Home Automation).
- **Block**: A node in a diagram representing a hardware component, logic gate, timer, or automation construct. Has typed input/output ports and configurable properties.
- **Wire**: A connection between an output port of one block and an input port of another. Represents data or signal flow.
- **Module**: A reusable group of blocks saved as a template with defined input and output ports.
- **Project Version**: A snapshot of a project's complete state at a point in time. Includes diagram data, board configurations, and metadata.
- **Compilation Artifact**: Generated output from the compiler pipeline (ESPHome YAML, Home Assistant YAML, Intermediate Representation).
- **Deployment Record**: A log entry recording when a configuration was deployed to a device, by whom, with what result.
- **Lead Submission**: A contact form entry from the public website, with submitter information and message content.
- **Blog Post**: A content article authored by an administrator, with title, slug, excerpt, body content, publication status, and timestamps.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Visitors can navigate all public website pages and submit a contact form in under 2 minutes.
- **SC-002**: New clients can register, log in, and create their first project in under 3 minutes.
- **SC-003**: A client can design a basic automation (one input, one logic gate, one output), compile it, and preview the YAML in under 5 minutes on their first use.
- **SC-004**: 95% of visual editor interactions (drag, drop, connect, configure) respond within 100 milliseconds.
- **SC-005**: Compilation of a diagram with up to 50 blocks completes within 3 seconds.
- **SC-006**: The system supports at least 100 concurrent authenticated users without performance degradation.
- **SC-007**: Zero cross-tenant data leakage — tenant isolation passes all security test scenarios.
- **SC-008**: 90% of first-time users can complete a basic automation workflow (board setup → diagram → compile → preview) without external documentation or support.
- **SC-009**: OTA deployment to an ESP32 board completes within 2 minutes for standard configurations.
- **SC-010**: All generated ESPHome YAML files are syntactically valid and pass ESPHome config validation.
- **SC-011**: Project save and load operations complete within 2 seconds for projects with up to 200 blocks.
- **SC-012**: Every deployment and project modification is recorded in the audit log with actor, action, timestamp, and outcome.
- **SC-013**: 100% of user-facing pages and components pass a visual design audit confirming adherence to the BlackDragon brand identity — ultra-dark backgrounds, metallic accents, circuit-board patterns, logo placement, and consistent design token usage with zero ad-hoc style overrides.

## Assumptions

- Users have modern web browsers (latest two major versions of Chrome, Firefox, Safari, or Edge) with JavaScript enabled.
- Client users have a stable internet connection when using the portal and deploying configurations.
- ESP32 boards are pre-flashed with an ESPHome base firmware that supports OTA updates before first deployment from the platform.
- Home Assistant instances are accessible over the network from the BlackDragon platform (direct connection or VPN).
- Each tenant manages a reasonable number of properties and projects (up to 50 properties with up to 20 projects each for initial scale).
- Board models have a fixed set of I/O channels defined at the hardware level; the platform configures software behavior, not hardware topology.
- The MVP targets English language only; internationalization is a future enhancement.
- Mobile application support is out of scope for the MVP; the web application is responsive but not a native app.
- Real-time simulation, live signal monitoring, and device auto-discovery are future enhancements, not MVP requirements.
- The platform runs in a containerized environment for the initial deployment target.
- Email delivery for registration and notifications uses a standard transactional email service; specific provider choice is an implementation detail.
