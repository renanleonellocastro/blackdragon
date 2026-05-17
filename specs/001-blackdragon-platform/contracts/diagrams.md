# API Contract: Diagrams

**Base path**: `/api/projects/{project_id}/diagrams`
**Authentication**: Bearer token required
**Tenant isolation**: Automatic

---

## GET /api/projects/{project_id}/diagrams

List all diagrams in a project.

**Response 200**:
```json
{
  "items": [
    {
      "id": "uuid",
      "name": "string",
      "layer": "board | home_automation",
      "board_instance_id": "uuid | null",
      "has_draft": true,
      "node_count": 12,
      "edge_count": 8,
      "updated_at": "datetime",
      "created_at": "datetime"
    }
  ]
}
```

---

## POST /api/projects/{project_id}/diagrams

Create a new diagram.

**Request body**:
```json
{
  "name": "string (required)",
  "layer": "board | home_automation (required)",
  "board_instance_id": "uuid (required if layer is 'board')"
}
```

**Response 201**: Diagram object with empty graph_data

---

## GET /api/projects/{project_id}/diagrams/{diagram_id}

Get a diagram with full graph data.

**Response 200**:
```json
{
  "id": "uuid",
  "name": "string",
  "layer": "board | home_automation",
  "board_instance_id": "uuid | null",
  "graph_data": {
    "nodes": [],
    "edges": []
  },
  "draft_data": null,
  "viewport": { "x": 0, "y": 0, "zoom": 1 },
  "updated_at": "datetime",
  "created_at": "datetime"
}
```

---

## PUT /api/projects/{project_id}/diagrams/{diagram_id}

Save diagram graph data (full save — updates graph_data, clears draft_data).

**Request body**:
```json
{
  "graph_data": {
    "nodes": [
      {
        "id": "string",
        "type": "string",
        "position": { "x": 0, "y": 0 },
        "data": {}
      }
    ],
    "edges": [
      {
        "id": "string",
        "source": "string",
        "sourceHandle": "string",
        "target": "string",
        "targetHandle": "string"
      }
    ]
  },
  "viewport": { "x": 0, "y": 0, "zoom": 1 }
}
```

**Response 200**: Updated diagram object

---

## PATCH /api/projects/{project_id}/diagrams/{diagram_id}/draft

Auto-save draft data (does not overwrite committed graph_data).

**Request body**:
```json
{
  "draft_data": {
    "nodes": [],
    "edges": []
  },
  "viewport": { "x": 0, "y": 0, "zoom": 1 }
}
```

**Response 200**: `{ "saved": true, "saved_at": "datetime" }`

---

## DELETE /api/projects/{project_id}/diagrams/{diagram_id}

Delete a diagram.

**Response 204**: No content

---

## PATCH /api/projects/{project_id}/diagrams/{diagram_id}

Update diagram metadata (name, board association).

**Request body**:
```json
{
  "name": "string (optional)",
  "board_instance_id": "uuid (optional)"
}
```

**Response 200**: Updated diagram object
