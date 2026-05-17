# Data Model: BlackDragon SaaS Platform

**Feature**: 001-blackdragon-platform
**Date**: 2026-05-16
**Database**: PostgreSQL 16
**ORM**: SQLAlchemy 2.0

## Entity Relationship Overview

```
Tenant 1──* User
Tenant 1──* Property
Property 1──* Project
Project 1──* BoardInstance
Project 1──* Diagram
Project 1──* ProjectVersion
Project 1──* Deployment
BoardModel 1──* BoardInstance
BoardModel 1──* BoardModelChannel
BoardInstance 1──* BoardInstanceChannel
Diagram 1──* CompilationArtifact
User 1──* AuditLog
Deployment 1──* AuditLog
```

## Entities

### Tenant

Organizational boundary for multi-tenant data isolation.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, default uuid4 | Unique identifier |
| name | VARCHAR(255) | NOT NULL | Company or individual name |
| slug | VARCHAR(100) | UNIQUE, NOT NULL | URL-safe identifier |
| is_active | BOOLEAN | NOT NULL, default TRUE | Soft-disable tenant access |
| created_at | TIMESTAMP | NOT NULL, default now() | Creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, auto-update | Last modification |

**Relationships**: Has many Users, has many Properties.

---

### User

A person who authenticates and interacts with the platform.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, default uuid4 | Unique identifier |
| tenant_id | UUID | FK → Tenant.id, NOT NULL | Owning tenant |
| email | VARCHAR(255) | UNIQUE, NOT NULL | Login email |
| hashed_password | VARCHAR(255) | NOT NULL | bcrypt hash |
| full_name | VARCHAR(255) | NOT NULL | Display name |
| role | ENUM('client', 'admin') | NOT NULL, default 'client' | Access role |
| is_active | BOOLEAN | NOT NULL, default TRUE | Account active flag |
| last_login_at | TIMESTAMP | NULLABLE | Last successful login |
| created_at | TIMESTAMP | NOT NULL, default now() | Creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, auto-update | Last modification |

**Relationships**: Belongs to Tenant. Has many AuditLogs.
**Indexes**: `idx_user_email` (email), `idx_user_tenant` (tenant_id).

---

### Property

A physical location (home, building) owned by a tenant.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, default uuid4 | Unique identifier |
| tenant_id | UUID | FK → Tenant.id, NOT NULL | Owning tenant |
| name | VARCHAR(255) | NOT NULL | Property name |
| address | TEXT | NULLABLE | Physical address |
| description | TEXT | NULLABLE | Additional details |
| created_at | TIMESTAMP | NOT NULL, default now() | Creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, auto-update | Last modification |

**Relationships**: Belongs to Tenant. Has many Projects.
**Indexes**: `idx_property_tenant` (tenant_id).

---

### Project

An automation design workspace for a property.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, default uuid4 | Unique identifier |
| tenant_id | UUID | FK → Tenant.id, NOT NULL | Owning tenant |
| property_id | UUID | FK → Property.id, NOT NULL | Associated property |
| name | VARCHAR(255) | NOT NULL | Project name |
| description | TEXT | NULLABLE | Project description |
| status | ENUM('draft', 'active', 'archived') | NOT NULL, default 'draft' | Project status |
| current_version | INTEGER | NOT NULL, default 1 | Current version number |
| is_locked | BOOLEAN | NOT NULL, default FALSE | Concurrent editing lock |
| locked_by | UUID | FK → User.id, NULLABLE | User holding the lock |
| locked_at | TIMESTAMP | NULLABLE | Lock acquisition time |
| created_at | TIMESTAMP | NOT NULL, default now() | Creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, auto-update | Last modification |

**Relationships**: Belongs to Tenant, Property. Has many BoardInstances, Diagrams, ProjectVersions, Deployments.
**Indexes**: `idx_project_tenant` (tenant_id), `idx_project_property` (property_id).

---

### ProjectVersion

A snapshot of a project's complete state at a point in time.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, default uuid4 | Unique identifier |
| project_id | UUID | FK → Project.id, NOT NULL | Parent project |
| version_number | INTEGER | NOT NULL | Sequential version |
| description | VARCHAR(500) | NULLABLE | Version description |
| snapshot_data | JSONB | NOT NULL | Full project state (diagrams, boards, config) |
| created_by | UUID | FK → User.id, NOT NULL | User who saved this version |
| created_at | TIMESTAMP | NOT NULL, default now() | Creation timestamp |

**Relationships**: Belongs to Project. Belongs to User (creator).
**Indexes**: `idx_version_project` (project_id), UNIQUE (project_id, version_number).

---

### BoardModel

A hardware product definition in the catalog (system-wide, not tenant-scoped).

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, default uuid4 | Unique identifier |
| name | VARCHAR(255) | NOT NULL | Model name (e.g., "BD-IO-16") |
| slug | VARCHAR(100) | UNIQUE, NOT NULL | URL-safe identifier |
| description | TEXT | NULLABLE | Product description |
| platform | VARCHAR(50) | NOT NULL, default 'ESP32' | Hardware platform |
| board_variant | VARCHAR(100) | NOT NULL | ESPHome board identifier |
| image_url | VARCHAR(500) | NULLABLE | Product image URL |
| is_active | BOOLEAN | NOT NULL, default TRUE | Available for new selections |
| specifications | JSONB | NULLABLE | Additional specs (memory, processor, etc.) |
| created_at | TIMESTAMP | NOT NULL, default now() | Creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, auto-update | Last modification |

**Relationships**: Has many BoardModelChannels, has many BoardInstances.
**Note**: NOT tenant-scoped. Managed by administrators.

---

### BoardModelChannel

Defines an I/O channel available on a board model.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, default uuid4 | Unique identifier |
| board_model_id | UUID | FK → BoardModel.id, NOT NULL | Parent board model |
| channel_number | INTEGER | NOT NULL | Channel index on the board |
| direction | ENUM('input', 'output') | NOT NULL | I/O direction |
| default_gpio_pin | INTEGER | NOT NULL | Default GPIO pin assignment |
| supports_pullup | BOOLEAN | NOT NULL, default TRUE | Supports pull-up resistor |
| supports_pulldown | BOOLEAN | NOT NULL, default TRUE | Supports pull-down resistor |
| supports_pwm | BOOLEAN | NOT NULL, default FALSE | Supports PWM output |
| label | VARCHAR(100) | NULLABLE | Default channel label |

**Relationships**: Belongs to BoardModel.
**Indexes**: UNIQUE (board_model_id, channel_number).

---

### BoardInstance

A specific board model assigned to a project with user configuration.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, default uuid4 | Unique identifier |
| tenant_id | UUID | FK → Tenant.id, NOT NULL | Owning tenant |
| project_id | UUID | FK → Project.id, NOT NULL | Parent project |
| board_model_id | UUID | FK → BoardModel.id, NOT NULL | Board model reference |
| name | VARCHAR(255) | NOT NULL | User-assigned board name |
| device_address | VARCHAR(255) | NULLABLE | IP address or hostname for OTA |
| esphome_name | VARCHAR(100) | NOT NULL | ESPHome device name (slug) |
| wifi_credential_id | UUID | FK → Credential.id, NULLABLE | WiFi credentials reference |
| ota_credential_id | UUID | FK → Credential.id, NULLABLE | OTA password reference |
| api_credential_id | UUID | FK → Credential.id, NULLABLE | API password reference |
| created_at | TIMESTAMP | NOT NULL, default now() | Creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, auto-update | Last modification |

**Relationships**: Belongs to Tenant, Project, BoardModel. Has many BoardInstanceChannels.
**Indexes**: `idx_board_instance_project` (project_id), `idx_board_instance_tenant` (tenant_id).

---

### BoardInstanceChannel

User configuration for a specific I/O channel on a board instance.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, default uuid4 | Unique identifier |
| board_instance_id | UUID | FK → BoardInstance.id, NOT NULL | Parent board instance |
| board_model_channel_id | UUID | FK → BoardModelChannel.id, NOT NULL | Channel definition reference |
| name | VARCHAR(255) | NOT NULL | User-assigned channel name |
| gpio_pin | INTEGER | NOT NULL | Configured GPIO pin |
| pull_mode | ENUM('none', 'pullup', 'pulldown') | NOT NULL, default 'none' | Pull resistor mode |
| inverted | BOOLEAN | NOT NULL, default FALSE | Inverted logic |
| debounce_ms | INTEGER | NOT NULL, default 0 | Debounce time in ms |
| is_enabled | BOOLEAN | NOT NULL, default TRUE | Channel enabled flag |

**Relationships**: Belongs to BoardInstance, BoardModelChannel.
**Indexes**: UNIQUE (board_instance_id, board_model_channel_id).

---

### Diagram

A visual graph of connected blocks representing automation logic.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, default uuid4 | Unique identifier |
| tenant_id | UUID | FK → Tenant.id, NOT NULL | Owning tenant |
| project_id | UUID | FK → Project.id, NOT NULL | Parent project |
| name | VARCHAR(255) | NOT NULL | Diagram name |
| layer | ENUM('board', 'home_automation') | NOT NULL, default 'board' | Programming layer |
| board_instance_id | UUID | FK → BoardInstance.id, NULLABLE | Associated board (for board layer) |
| graph_data | JSONB | NOT NULL, default '{}' | Vue Flow serialized graph (nodes + edges) |
| draft_data | JSONB | NULLABLE | Auto-saved draft (not yet committed by user) |
| viewport | JSONB | NULLABLE | Canvas position and zoom level |
| created_at | TIMESTAMP | NOT NULL, default now() | Creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, auto-update | Last modification |

**Relationships**: Belongs to Tenant, Project, optionally BoardInstance. Has many CompilationArtifacts.
**Indexes**: `idx_diagram_project` (project_id), `idx_diagram_tenant` (tenant_id).

**graph_data structure** (JSONB):
```json
{
  "nodes": [
    {
      "id": "node-1",
      "type": "digitalInput",
      "position": { "x": 100, "y": 200 },
      "data": {
        "label": "Front Door Sensor",
        "gpio_pin": 14,
        "pull_mode": "pullup",
        "inverted": false,
        "debounce_ms": 50
      }
    }
  ],
  "edges": [
    {
      "id": "edge-1",
      "source": "node-1",
      "sourceHandle": "signal",
      "target": "node-2",
      "targetHandle": "a"
    }
  ]
}
```

---

### CompilationArtifact

Generated output from the compiler pipeline.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, default uuid4 | Unique identifier |
| diagram_id | UUID | FK → Diagram.id, NOT NULL | Source diagram |
| artifact_type | ENUM('esphome_yaml', 'homeassistant_yaml', 'ir_json') | NOT NULL | Output type |
| content | TEXT | NOT NULL | Generated content |
| version | INTEGER | NOT NULL | Compilation version |
| errors | JSONB | NULLABLE | Validation/compilation errors if any |
| is_valid | BOOLEAN | NOT NULL | Whether compilation succeeded |
| compiled_at | TIMESTAMP | NOT NULL, default now() | Compilation timestamp |
| compiled_by | UUID | FK → User.id, NOT NULL | User who triggered compilation |

**Relationships**: Belongs to Diagram.
**Indexes**: `idx_artifact_diagram` (diagram_id).

---

### Deployment

A record of deploying a configuration to a physical device.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, default uuid4 | Unique identifier |
| tenant_id | UUID | FK → Tenant.id, NOT NULL | Owning tenant |
| project_id | UUID | FK → Project.id, NOT NULL | Parent project |
| board_instance_id | UUID | FK → BoardInstance.id, NOT NULL | Target board |
| artifact_id | UUID | FK → CompilationArtifact.id, NOT NULL | Deployed artifact |
| status | ENUM('pending', 'uploading', 'success', 'failed', 'cancelled') | NOT NULL | Deployment status |
| progress_percent | INTEGER | NOT NULL, default 0 | Upload progress (0-100) |
| error_message | TEXT | NULLABLE | Failure reason |
| started_at | TIMESTAMP | NOT NULL, default now() | Deployment start |
| completed_at | TIMESTAMP | NULLABLE | Deployment end |
| deployed_by | UUID | FK → User.id, NOT NULL | User who initiated deployment |

**Relationships**: Belongs to Tenant, Project, BoardInstance, CompilationArtifact.
**Indexes**: `idx_deployment_project` (project_id), `idx_deployment_tenant` (tenant_id).

---

### Credential

Encrypted storage for device credentials (WiFi passwords, OTA secrets, API keys).

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, default uuid4 | Unique identifier |
| tenant_id | UUID | FK → Tenant.id, NOT NULL | Owning tenant |
| name | VARCHAR(255) | NOT NULL | Credential label |
| credential_type | ENUM('wifi', 'ota', 'api', 'homeassistant') | NOT NULL | Credential category |
| encrypted_value | TEXT | NOT NULL | Fernet-encrypted credential data |
| created_at | TIMESTAMP | NOT NULL, default now() | Creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, auto-update | Last modification |

**Relationships**: Belongs to Tenant.
**Indexes**: `idx_credential_tenant` (tenant_id).
**Security**: Values encrypted with Fernet (symmetric, AES-128-CBC). Encryption key stored as environment variable, never in database.

---

### AuditLog

Immutable log of significant actions for accountability and compliance.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, default uuid4 | Unique identifier |
| tenant_id | UUID | FK → Tenant.id, NULLABLE | Tenant context (NULL for system actions) |
| user_id | UUID | FK → User.id, NULLABLE | Acting user (NULL for system actions) |
| action | VARCHAR(100) | NOT NULL | Action identifier (e.g., 'project.create', 'deployment.start') |
| resource_type | VARCHAR(100) | NOT NULL | Entity type affected |
| resource_id | UUID | NOT NULL | Entity ID affected |
| details | JSONB | NULLABLE | Additional context (before/after values, parameters) |
| ip_address | VARCHAR(45) | NULLABLE | Client IP address |
| created_at | TIMESTAMP | NOT NULL, default now() | Event timestamp |

**Relationships**: Belongs to Tenant (optional), User (optional).
**Indexes**: `idx_audit_tenant` (tenant_id), `idx_audit_user` (user_id), `idx_audit_created` (created_at), `idx_audit_resource` (resource_type, resource_id).
**Note**: Append-only table. No UPDATE or DELETE operations.

---

### LeadSubmission

Contact form entries from the public website.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, default uuid4 | Unique identifier |
| name | VARCHAR(255) | NOT NULL | Submitter name |
| email | VARCHAR(255) | NOT NULL | Submitter email |
| company | VARCHAR(255) | NULLABLE | Company name |
| phone | VARCHAR(50) | NULLABLE | Phone number |
| message | TEXT | NOT NULL | Message content |
| status | ENUM('new', 'reviewed', 'contacted', 'archived') | NOT NULL, default 'new' | Processing status |
| reviewed_by | UUID | FK → User.id, NULLABLE | Admin who reviewed |
| created_at | TIMESTAMP | NOT NULL, default now() | Submission timestamp |

**Relationships**: None (not tenant-scoped — public form).
**Indexes**: `idx_lead_status` (status), `idx_lead_created` (created_at).

---

### Module

A reusable group of blocks saved as a template (future enhancement, included in model for forward compatibility).

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, default uuid4 | Unique identifier |
| tenant_id | UUID | FK → Tenant.id, NOT NULL | Owning tenant |
| name | VARCHAR(255) | NOT NULL | Module name |
| description | TEXT | NULLABLE | Module description |
| graph_data | JSONB | NOT NULL | Internal block graph |
| input_ports | JSONB | NOT NULL | Defined input port schema |
| output_ports | JSONB | NOT NULL | Defined output port schema |
| version | INTEGER | NOT NULL, default 1 | Module version |
| created_by | UUID | FK → User.id, NOT NULL | Author |
| created_at | TIMESTAMP | NOT NULL, default now() | Creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, auto-update | Last modification |

**Relationships**: Belongs to Tenant.
**Indexes**: `idx_module_tenant` (tenant_id).

---

## Tenant-Scoped vs System-Scoped Tables

| Table | Scope | tenant_id column |
|-------|-------|-----------------|
| Tenant | System | — (is the tenant) |
| User | Tenant | ✓ |
| Property | Tenant | ✓ |
| Project | Tenant | ✓ |
| ProjectVersion | Tenant | via Project |
| BoardModel | System | — |
| BoardModelChannel | System | via BoardModel |
| BoardInstance | Tenant | ✓ |
| BoardInstanceChannel | Tenant | via BoardInstance |
| Diagram | Tenant | ✓ |
| CompilationArtifact | Tenant | via Diagram |
| Deployment | Tenant | ✓ |
| Credential | Tenant | ✓ |
| AuditLog | Tenant | ✓ (nullable) |
| LeadSubmission | System | — |
| Module | Tenant | ✓ |

## State Transitions

### Project.status
```
draft → active → archived
         ↑         |
         └─────────┘ (unarchive)
```

### Deployment.status
```
pending → uploading → success
                   → failed
          → cancelled
```

### LeadSubmission.status
```
new → reviewed → contacted → archived
```
