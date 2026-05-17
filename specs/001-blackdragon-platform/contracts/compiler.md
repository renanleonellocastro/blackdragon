# API Contract: Compiler

**Base path**: `/api/projects/{project_id}/compile`
**Authentication**: Bearer token required
**Tenant isolation**: Automatic

---

## POST /api/projects/{project_id}/compile

Compile one or more diagrams in a project. Runs the full pipeline: validation → IR → optimization → code generation.

**Request body**:
```json
{
  "diagram_ids": ["uuid (optional, compile specific diagrams)"],
  "targets": ["esphome", "homeassistant (optional, default: all applicable)"]
}
```

If `diagram_ids` is omitted, all diagrams in the project are compiled.

**Response 200** (success):
```json
{
  "success": true,
  "artifacts": [
    {
      "id": "uuid",
      "diagram_id": "uuid",
      "diagram_name": "string",
      "artifact_type": "esphome_yaml",
      "board_instance_name": "string",
      "is_valid": true,
      "content": "string (generated YAML)",
      "compiled_at": "datetime"
    }
  ],
  "warnings": [
    {
      "diagram_id": "uuid",
      "node_id": "string",
      "message": "string"
    }
  ]
}
```

**Response 200** (validation errors):
```json
{
  "success": false,
  "errors": [
    {
      "diagram_id": "uuid",
      "node_id": "string | null",
      "edge_id": "string | null",
      "error_type": "unconnected_port | type_mismatch | gpio_conflict | cycle_detected | missing_config",
      "message": "string",
      "location": {
        "node_label": "string",
        "port_name": "string | null"
      }
    }
  ],
  "artifacts": []
}
```

---

## GET /api/projects/{project_id}/compile/artifacts

List all compilation artifacts for a project.

**Query parameters**:
- `diagram_id` (uuid, optional): Filter by diagram
- `artifact_type` (string, optional): Filter by type

**Response 200**:
```json
{
  "items": [
    {
      "id": "uuid",
      "diagram_id": "uuid",
      "artifact_type": "esphome_yaml | homeassistant_yaml | ir_json",
      "is_valid": true,
      "version": 1,
      "compiled_at": "datetime",
      "compiled_by": {
        "id": "uuid",
        "full_name": "string"
      }
    }
  ]
}
```

---

## GET /api/projects/{project_id}/compile/artifacts/{artifact_id}

Get a specific compilation artifact with full content.

**Response 200**:
```json
{
  "id": "uuid",
  "diagram_id": "uuid",
  "artifact_type": "string",
  "content": "string (full generated content)",
  "is_valid": true,
  "errors": null,
  "version": 1,
  "compiled_at": "datetime"
}
```

---

## GET /api/projects/{project_id}/compile/artifacts/{artifact_id}/download

Download a compilation artifact as a file.

**Response 200**: File download
- Content-Type: `application/x-yaml`
- Content-Disposition: `attachment; filename="{board_name}.yaml"`

---

## POST /api/projects/{project_id}/compile/validate

Validate diagrams without generating code (faster — stops after semantic analysis).

**Request body**:
```json
{
  "diagram_ids": ["uuid (optional)"]
}
```

**Response 200**:
```json
{
  "valid": true,
  "errors": [],
  "warnings": []
}
```

---

## GET /api/nodes/definitions

Get all available node type definitions (used by frontend to build the palette).

**Response 200**:
```json
{
  "nodes": [
    {
      "type": "digitalInput",
      "label": "Digital Input",
      "category": "hardware",
      "icon": "string",
      "color": "#10B981",
      "ports": [
        {
          "name": "signal",
          "direction": "output",
          "data_type": "boolean",
          "required": false
        }
      ],
      "properties": [
        {
          "name": "gpio_pin",
          "type": "number",
          "required": true,
          "default": null,
          "validation": { "min": 0, "max": 39 }
        },
        {
          "name": "pull_mode",
          "type": "enum",
          "required": true,
          "default": "none",
          "validation": { "values": ["none", "pullup", "pulldown"] }
        },
        {
          "name": "inverted",
          "type": "boolean",
          "required": true,
          "default": false
        },
        {
          "name": "debounce_ms",
          "type": "number",
          "required": true,
          "default": 0,
          "validation": { "min": 0, "max": 5000 }
        },
        {
          "name": "name",
          "type": "string",
          "required": true,
          "default": ""
        }
      ]
    }
  ]
}
```
