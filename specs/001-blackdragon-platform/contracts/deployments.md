# API Contract: Deployments

**Base path**: `/api/projects/{project_id}/deployments`
**Authentication**: Bearer token required
**Tenant isolation**: Automatic

---

## POST /api/projects/{project_id}/deployments

Initiate a deployment of a compiled artifact to a board.

**Request body**:
```json
{
  "artifact_id": "uuid (required)",
  "board_instance_id": "uuid (required)"
}
```

**Response 202** (accepted — deployment runs asynchronously):
```json
{
  "id": "uuid",
  "status": "pending",
  "board_instance": {
    "id": "uuid",
    "name": "string",
    "device_address": "string"
  },
  "artifact_id": "uuid",
  "progress_percent": 0,
  "started_at": "datetime"
}
```

**Response 400**: `{ "detail": "Board has no device address configured" }`
**Response 404**: `{ "detail": "Artifact not found or invalid" }`
**Response 409**: `{ "detail": "Deployment already in progress for this board" }`

---

## GET /api/projects/{project_id}/deployments

List deployment history for a project.

**Query parameters**:
- `board_instance_id` (uuid, optional): Filter by board
- `status` (string, optional): Filter by status
- `page` (int, optional, default 1)
- `per_page` (int, optional, default 20)

**Response 200**:
```json
{
  "items": [
    {
      "id": "uuid",
      "board_instance": {
        "id": "uuid",
        "name": "string"
      },
      "status": "pending | uploading | success | failed | cancelled",
      "progress_percent": 100,
      "error_message": "string | null",
      "deployed_by": {
        "id": "uuid",
        "full_name": "string"
      },
      "started_at": "datetime",
      "completed_at": "datetime | null"
    }
  ],
  "total": 10,
  "page": 1,
  "per_page": 20
}
```

---

## GET /api/projects/{project_id}/deployments/{deployment_id}

Get deployment details and current status.

**Response 200**:
```json
{
  "id": "uuid",
  "board_instance": {
    "id": "uuid",
    "name": "string",
    "device_address": "string"
  },
  "artifact_id": "uuid",
  "status": "string",
  "progress_percent": 65,
  "error_message": "string | null",
  "deployed_by": {
    "id": "uuid",
    "full_name": "string"
  },
  "started_at": "datetime",
  "completed_at": "datetime | null"
}
```

---

## POST /api/projects/{project_id}/deployments/{deployment_id}/cancel

Cancel a pending or in-progress deployment.

**Response 200**: `{ "status": "cancelled" }`
**Response 409**: `{ "detail": "Deployment already completed" }`
