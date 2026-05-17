# API Contract: Projects

**Base path**: `/api/projects`
**Authentication**: Bearer token required
**Tenant isolation**: Automatic — all operations scoped to authenticated user's tenant

---

## GET /api/projects

List all projects for the current tenant.

**Query parameters**:
- `property_id` (uuid, optional): Filter by property
- `status` (string, optional): Filter by status (draft, active, archived)
- `page` (int, optional, default 1): Page number
- `per_page` (int, optional, default 20): Items per page

**Response 200**:
```json
{
  "items": [
    {
      "id": "uuid",
      "name": "string",
      "description": "string | null",
      "status": "draft | active | archived",
      "property": {
        "id": "uuid",
        "name": "string"
      },
      "current_version": 1,
      "board_count": 2,
      "diagram_count": 3,
      "is_locked": false,
      "updated_at": "datetime",
      "created_at": "datetime"
    }
  ],
  "total": 42,
  "page": 1,
  "per_page": 20
}
```

---

## POST /api/projects

Create a new project.

**Request body**:
```json
{
  "name": "string (required)",
  "description": "string (optional)",
  "property_id": "uuid (required)"
}
```

**Response 201**:
```json
{
  "id": "uuid",
  "name": "string",
  "description": "string | null",
  "status": "draft",
  "property_id": "uuid",
  "current_version": 1,
  "created_at": "datetime"
}
```

**Response 404**: `{ "detail": "Property not found" }`

---

## GET /api/projects/{project_id}

Get a project with full details including board instances and diagrams.

**Response 200**:
```json
{
  "id": "uuid",
  "name": "string",
  "description": "string | null",
  "status": "draft | active | archived",
  "property": {
    "id": "uuid",
    "name": "string",
    "address": "string | null"
  },
  "current_version": 1,
  "is_locked": false,
  "locked_by": "uuid | null",
  "board_instances": [
    {
      "id": "uuid",
      "name": "string",
      "board_model": {
        "id": "uuid",
        "name": "string",
        "slug": "string"
      }
    }
  ],
  "diagrams": [
    {
      "id": "uuid",
      "name": "string",
      "layer": "board | home_automation",
      "board_instance_id": "uuid | null",
      "updated_at": "datetime"
    }
  ],
  "updated_at": "datetime",
  "created_at": "datetime"
}
```

**Response 404**: `{ "detail": "Project not found" }`

---

## PATCH /api/projects/{project_id}

Update project metadata.

**Request body**:
```json
{
  "name": "string (optional)",
  "description": "string (optional)",
  "status": "draft | active | archived (optional)"
}
```

**Response 200**: Updated project object (same as GET response)

---

## DELETE /api/projects/{project_id}

Delete a project and all associated data.

**Response 204**: No content

**Response 409**: `{ "detail": "Project has active deployments" }`

---

## POST /api/projects/{project_id}/duplicate

Create a copy of a project with all diagrams and board configurations.

**Request body**:
```json
{
  "name": "string (required, name for the copy)"
}
```

**Response 201**: New project object (same as GET response)

---

## POST /api/projects/{project_id}/lock

Acquire an editing lock on a project.

**Response 200**:
```json
{
  "locked": true,
  "locked_by": "uuid",
  "locked_at": "datetime"
}
```

**Response 409**: `{ "detail": "Project is locked by another user", "locked_by": "uuid" }`

---

## POST /api/projects/{project_id}/unlock

Release an editing lock on a project.

**Response 200**: `{ "locked": false }`

---

## GET /api/projects/{project_id}/versions

List version history for a project.

**Response 200**:
```json
{
  "items": [
    {
      "id": "uuid",
      "version_number": 1,
      "description": "string | null",
      "created_by": {
        "id": "uuid",
        "full_name": "string"
      },
      "created_at": "datetime"
    }
  ]
}
```

---

## POST /api/projects/{project_id}/versions

Save a new version snapshot.

**Request body**:
```json
{
  "description": "string (optional)"
}
```

**Response 201**: Version object

---

## POST /api/projects/{project_id}/versions/{version_number}/rollback

Roll back project to a specific version.

**Response 200**: Updated project object with rolled-back data
