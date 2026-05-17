# API Contract: Leads (Public Contact Form)

**Base path**: `/api/leads`

---

## POST /api/leads (public — no auth)

Submit a contact form from the public website.

**Request body**:
```json
{
  "name": "string (required)",
  "email": "string (required, valid email)",
  "company": "string (optional)",
  "phone": "string (optional)",
  "message": "string (required, max 5000 chars)"
}
```

**Response 201**:
```json
{
  "id": "uuid",
  "message": "Thank you for contacting us. We will respond shortly.",
  "created_at": "datetime"
}
```

**Response 422**: Validation errors
**Response 429**: Rate limit exceeded (max 5 submissions per IP per hour)

---

## GET /api/admin/leads (admin only)

List all lead submissions.

**Query parameters**:
- `status` (string, optional): new, reviewed, contacted, archived
- `page` (int, optional, default 1)
- `per_page` (int, optional, default 20)

**Response 200**:
```json
{
  "items": [
    {
      "id": "uuid",
      "name": "string",
      "email": "string",
      "company": "string | null",
      "phone": "string | null",
      "message": "string",
      "status": "new | reviewed | contacted | archived",
      "reviewed_by": {
        "id": "uuid",
        "full_name": "string"
      },
      "created_at": "datetime"
    }
  ],
  "total": 15,
  "page": 1,
  "per_page": 20
}
```

---

## PATCH /api/admin/leads/{lead_id} (admin only)

Update lead status.

**Request body**:
```json
{
  "status": "reviewed | contacted | archived"
}
```

**Response 200**: Updated lead object
