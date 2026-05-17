# API Contract: Properties

**Base path**: `/api/properties`
**Authentication**: Bearer token required
**Tenant isolation**: Automatic

---

## GET /api/properties

List all properties for the current tenant.

**Response 200**:
```json
{
  "items": [
    {
      "id": "uuid",
      "name": "string",
      "address": "string | null",
      "description": "string | null",
      "project_count": 3,
      "created_at": "datetime"
    }
  ]
}
```

---

## POST /api/properties

Create a new property.

**Request body**:
```json
{
  "name": "string (required)",
  "address": "string (optional)",
  "description": "string (optional)"
}
```

**Response 201**: Property object

---

## GET /api/properties/{property_id}

Get a property with its projects.

**Response 200**:
```json
{
  "id": "uuid",
  "name": "string",
  "address": "string | null",
  "description": "string | null",
  "projects": [
    {
      "id": "uuid",
      "name": "string",
      "status": "string",
      "updated_at": "datetime"
    }
  ],
  "created_at": "datetime"
}
```

---

## PATCH /api/properties/{property_id}

Update a property.

**Request body**:
```json
{
  "name": "string (optional)",
  "address": "string (optional)",
  "description": "string (optional)"
}
```

**Response 200**: Updated property object

---

## DELETE /api/properties/{property_id}

Delete a property (only if it has no projects).

**Response 204**: No content
**Response 409**: `{ "detail": "Property has existing projects" }`
