# API Contract: Boards

**Base path**: `/api/boards`
**Authentication**: Bearer token required

---

## GET /api/boards/catalog

List all available board models (system-wide catalog).

**Response 200**:
```json
{
  "items": [
    {
      "id": "uuid",
      "name": "string",
      "slug": "string",
      "description": "string | null",
      "platform": "ESP32",
      "board_variant": "string",
      "image_url": "string | null",
      "is_active": true,
      "specifications": {},
      "channels": [
        {
          "id": "uuid",
          "channel_number": 1,
          "direction": "input | output",
          "default_gpio_pin": 14,
          "supports_pullup": true,
          "supports_pulldown": true,
          "label": "string | null"
        }
      ]
    }
  ]
}
```

---

## POST /api/boards/catalog (admin only)

Add a new board model to the catalog.

**Request body**:
```json
{
  "name": "string (required)",
  "slug": "string (required)",
  "description": "string (optional)",
  "platform": "string (default: ESP32)",
  "board_variant": "string (required)",
  "image_url": "string (optional)",
  "channels": [
    {
      "channel_number": 1,
      "direction": "input | output",
      "default_gpio_pin": 14,
      "supports_pullup": true,
      "supports_pulldown": true,
      "label": "string (optional)"
    }
  ]
}
```

**Response 201**: Board model object with channels
**Response 403**: `{ "detail": "Admin access required" }`

---

## PATCH /api/boards/catalog/{board_model_id} (admin only)

Update a board model.

**Request body**: Partial board model fields (same as POST but all optional)
**Response 200**: Updated board model object

---

## DELETE /api/boards/catalog/{board_model_id} (admin only)

Retire a board model (soft delete — sets `is_active = false`).

**Response 200**: `{ "is_active": false }`

---

## GET /api/projects/{project_id}/boards

List board instances in a project.

**Response 200**:
```json
{
  "items": [
    {
      "id": "uuid",
      "name": "string",
      "esphome_name": "string",
      "device_address": "string | null",
      "board_model": {
        "id": "uuid",
        "name": "string",
        "platform": "string"
      },
      "channels": [
        {
          "id": "uuid",
          "channel_number": 1,
          "direction": "input | output",
          "name": "string",
          "gpio_pin": 14,
          "pull_mode": "none | pullup | pulldown",
          "inverted": false,
          "debounce_ms": 0,
          "is_enabled": true
        }
      ],
      "created_at": "datetime"
    }
  ]
}
```

---

## POST /api/projects/{project_id}/boards

Add a board instance to a project.

**Request body**:
```json
{
  "board_model_id": "uuid (required)",
  "name": "string (required)",
  "esphome_name": "string (required, slug format)",
  "device_address": "string (optional)"
}
```

**Response 201**: Board instance with default channel configurations (inherited from board model)

---

## PATCH /api/projects/{project_id}/boards/{board_instance_id}

Update board instance metadata.

**Request body**:
```json
{
  "name": "string (optional)",
  "esphome_name": "string (optional)",
  "device_address": "string (optional)"
}
```

**Response 200**: Updated board instance

---

## PATCH /api/projects/{project_id}/boards/{board_instance_id}/channels/{channel_id}

Update a specific I/O channel configuration.

**Request body**:
```json
{
  "name": "string (optional)",
  "gpio_pin": "int (optional)",
  "pull_mode": "none | pullup | pulldown (optional)",
  "inverted": "boolean (optional)",
  "debounce_ms": "int (optional)",
  "is_enabled": "boolean (optional)"
}
```

**Response 200**: Updated channel object

**Response 409**: `{ "detail": "GPIO pin conflict", "conflicting_channel": "uuid" }`

---

## DELETE /api/projects/{project_id}/boards/{board_instance_id}

Remove a board instance from a project.

**Response 204**: No content
**Response 409**: `{ "detail": "Board is referenced in diagrams", "diagram_ids": ["uuid"] }`
