# API Contract: Authentication

**Base path**: `/api/auth`
**Authentication**: Public (no token required)

---

## POST /api/auth/register

Create a new user account and tenant.

**Request body**:
```json
{
  "email": "string (required, valid email)",
  "password": "string (required, min 8 chars)",
  "full_name": "string (required)",
  "company_name": "string (optional, used as tenant name)"
}
```

**Response 201**:
```json
{
  "access_token": "string (JWT)",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "email": "string",
    "full_name": "string",
    "role": "client",
    "tenant_id": "uuid"
  }
}
```

**Response 409**: `{ "detail": "Email already registered" }`
**Response 422**: Validation errors

---

## POST /api/auth/login

Authenticate and obtain a JWT token.

**Request body**:
```json
{
  "email": "string (required)",
  "password": "string (required)"
}
```

**Response 200**:
```json
{
  "access_token": "string (JWT)",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "email": "string",
    "full_name": "string",
    "role": "client | admin",
    "tenant_id": "uuid"
  }
}
```

**Response 401**: `{ "detail": "Invalid credentials" }`

---

## POST /api/auth/refresh

Refresh an expiring access token.

**Headers**: `Authorization: Bearer <token>`

**Response 200**:
```json
{
  "access_token": "string (JWT)",
  "token_type": "bearer"
}
```

**Response 401**: `{ "detail": "Token expired or invalid" }`

---

## GET /api/auth/me

Get the current authenticated user's profile.

**Headers**: `Authorization: Bearer <token>`

**Response 200**:
```json
{
  "id": "uuid",
  "email": "string",
  "full_name": "string",
  "role": "client | admin",
  "tenant_id": "uuid",
  "last_login_at": "datetime | null",
  "created_at": "datetime"
}
```
