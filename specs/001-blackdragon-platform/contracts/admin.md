# API Contract: Admin

**Base path**: `/api/admin`
**Authentication**: Bearer token required, admin role only
**Tenant isolation**: Admin bypasses tenant filtering

---

## GET /api/admin/users

List all users across all tenants.

**Query parameters**:
- `tenant_id` (uuid, optional): Filter by tenant
- `role` (string, optional): Filter by role
- `is_active` (boolean, optional): Filter by active status
- `page` (int, optional, default 1)
- `per_page` (int, optional, default 20)

**Response 200**:
```json
{
  "items": [
    {
      "id": "uuid",
      "email": "string",
      "full_name": "string",
      "role": "client | admin",
      "is_active": true,
      "tenant": {
        "id": "uuid",
        "name": "string"
      },
      "last_login_at": "datetime | null",
      "created_at": "datetime"
    }
  ],
  "total": 50,
  "page": 1,
  "per_page": 20
}
```

---

## PATCH /api/admin/users/{user_id}

Update user details (role, active status).

**Request body**:
```json
{
  "role": "client | admin (optional)",
  "is_active": "boolean (optional)",
  "full_name": "string (optional)"
}
```

**Response 200**: Updated user object

---

## GET /api/admin/tenants

List all tenants.

**Response 200**:
```json
{
  "items": [
    {
      "id": "uuid",
      "name": "string",
      "slug": "string",
      "is_active": true,
      "user_count": 3,
      "property_count": 5,
      "created_at": "datetime"
    }
  ]
}
```

---

## GET /api/admin/audit-logs

Query audit logs.

**Query parameters**:
- `tenant_id` (uuid, optional)
- `user_id` (uuid, optional)
- `action` (string, optional)
- `resource_type` (string, optional)
- `from_date` (datetime, optional)
- `to_date` (datetime, optional)
- `page` (int, optional, default 1)
- `per_page` (int, optional, default 50)

**Response 200**:
```json
{
  "items": [
    {
      "id": "uuid",
      "user": {
        "id": "uuid",
        "full_name": "string",
        "email": "string"
      },
      "tenant": {
        "id": "uuid",
        "name": "string"
      },
      "action": "string",
      "resource_type": "string",
      "resource_id": "uuid",
      "details": {},
      "ip_address": "string",
      "created_at": "datetime"
    }
  ],
  "total": 200,
  "page": 1,
  "per_page": 50
}
```
