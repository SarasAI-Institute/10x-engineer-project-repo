# PromptLab API Reference

Comprehensive guide for the PromptLab FastAPI service that manages incident-response prompts and collections.

- **Base URL (local development):** `http://localhost:8000`
- **OpenAPI (Swagger UI):** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

## Authentication
Authentication is **not required** today. All endpoints are open in development. When authentication is introduced, clients should expect to send credentials via the `Authorization` header (e.g., bearer tokens).

## Request & Response Conventions
- **Content type:** Send `application/json` for all request bodies; responses are JSON.
- **Timestamps:** ISO 8601 UTC strings (e.g., `2024-02-12T19:05:13.987654`).
- **IDs:** Prompt and collection identifiers are UUIDv4 strings generated server-side.
- **Sorting:** `GET /prompts` returns prompts ordered by `updated_at` (newest first).
- **Pagination:** Not yet implemented; all records are returned.

## Error Handling
FastAPI error responses follow consistent JSON shapes:

| Status | When it occurs | Payload shape |
|--------|----------------|---------------|
| `400 Bad Request` | Data references invalid resources (e.g., unknown `collection_id`). | `{ "detail": "Collection not found" }` |
| `404 Not Found` | Requested resource is missing. | `{ "detail": "Prompt not found" }` |
| `422 Unprocessable Entity` | Validation failure (missing/invalid fields). | `{ "detail": [ { "loc": [...], "msg": "...", "type": "..." } ] }` |

### Example 400 response (unknown collection)
```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "detail": "Collection not found"
}
```

### Example 422 response (validation error)
```http
HTTP/1.1 422 Unprocessable Entity
Content-Type: application/json

{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "Field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## Health
### `GET /health`
Returns current health status and semantic version.

**Response — 200 OK**
```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

---

## Prompts
Prompts capture reusable incident response guidance.

| Field | Type | Notes |
|-------|------|-------|
| `id` | `string` | Read-only UUID. |
| `title` | `string` | 1–200 chars, required. |
| `content` | `string` | Required prompt body (template variables allowed). |
| `description` | `string \| null` | Optional, ≤500 chars. |
| `collection_id` | `string \| null` | Optional UUID referencing an existing collection. |
| `created_at` | `string` | Read-only ISO timestamp. |
| `updated_at` | `string` | Read-only ISO timestamp, updated on every mutation. |

### List Prompts — `GET /prompts`
Retrieve all prompts with optional filters.

**Query Parameters**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `collection_id` | `string` | No | Restrict results to a specific collection. |
| `search` | `string` | No | Case-insensitive substring search on title + description. |

**Response — 200 OK**
```json
{
  "prompts": [
    {
      "id": "b3f0d80f-3db1-4f5a-a10d-0123456789ab",
      "title": "Escalate PSP Timeout",
      "content": "Investigate PSP latencies > {{latency_threshold}}ms...",
      "description": "Use during PSP timeouts",
      "collection_id": "c2c1d1de-9d7a-4de6-9af1-fa3d73c5b7a5",
      "created_at": "2024-02-12T18:41:31.123456",
      "updated_at": "2024-02-12T18:41:31.123456"
    }
  ],
  "total": 1
}
```

**Example request**
```bash
curl "http://localhost:8000/prompts?collection_id=c2c1d1de-9d7a-4de6-9af1-fa3d73c5b7a5&search=psp"
```

### Retrieve Prompt — `GET /prompts/{prompt_id}`
Fetch a prompt by UUID.

**Path parameter**
| Name | Description |
|------|-------------|
| `prompt_id` | UUID of the prompt to retrieve. |

**Response — 200 OK**
```json
{
  "id": "b3f0d80f-3db1-4f5a-a10d-0123456789ab",
  "title": "Escalate PSP Timeout",
  "content": "Investigate PSP latencies > {{latency_threshold}}ms...",
  "description": "Use during PSP timeouts",
  "collection_id": "c2c1d1de-9d7a-4de6-9af1-fa3d73c5b7a5",
  "created_at": "2024-02-12T18:41:31.123456",
  "updated_at": "2024-02-12T18:41:31.123456"
}
```

**Errors**
- `404 Not Found` if the prompt does not exist.

### Create Prompt — `POST /prompts`
Create a new prompt. `collection_id` must point to an existing collection when present.

**Request body**
| Field | Required | Description |
|-------|----------|-------------|
| `title` | Yes | Prompt name (1–200 chars). |
| `content` | Yes | Prompt body text. |
| `description` | No | Optional summary/notes. |
| `collection_id` | No | UUID of an existing collection. |

**Example request**
```bash
curl -X POST http://localhost:8000/prompts \
  -H "Content-Type: application/json" \
  -d '{
        "title": "Notify leadership channel",
        "content": "Post update to #incident-room with status: {{status}}",
        "description": "Hourly leadership ping",
        "collection_id": "c2c1d1de-9d7a-4de6-9af1-fa3d73c5b7a5"
      }'
```

**Response — 201 Created**
```json
{
  "id": "2f23d8b9-9373-4e10-8fd1-5f4aa251c7a9",
  "title": "Notify leadership channel",
  "content": "Post update to #incident-room with status: {{status}}",
  "description": "Hourly leadership ping",
  "collection_id": "c2c1d1de-9d7a-4de6-9af1-fa3d73c5b7a5",
  "created_at": "2024-02-12T19:05:13.987654",
  "updated_at": "2024-02-12T19:05:13.987654"
}
```

**Errors**
- `400 Bad Request` when `collection_id` does not exist.

### Replace Prompt — `PUT /prompts/{prompt_id}`
Replace the full prompt document. All mutable fields (title, content, description, collection_id) must be supplied.

**Example request**
```bash
curl -X PUT http://localhost:8000/prompts/b3f0d80f-3db1-4f5a-a10d-0123456789ab \
  -H "Content-Type: application/json" \
  -d '{
        "title": "Escalate PSP Timeout (Updated)",
        "content": "Updated runbook content",
        "description": "Revised after retro",
        "collection_id": "c2c1d1de-9d7a-4de6-9af1-fa3d73c5b7a5"
      }'
```

**Response — 200 OK**
```json
{
  "id": "b3f0d80f-3db1-4f5a-a10d-0123456789ab",
  "title": "Escalate PSP Timeout (Updated)",
  "content": "Updated runbook content",
  "description": "Revised after retro",
  "collection_id": "c2c1d1de-9d7a-4de6-9af1-fa3d73c5b7a5",
  "created_at": "2024-02-12T18:41:31.123456",
  "updated_at": "2024-02-12T19:10:00.000000"
}
```

**Errors**
- `404 Not Found` when the prompt does not exist.
- `400 Bad Request` if `collection_id` references a missing collection.

### Patch Prompt — `PATCH /prompts/{prompt_id}`
Partially update selected fields. Only provided keys change. `updated_at` refreshes automatically.

**Example request**
```bash
curl -X PATCH http://localhost:8000/prompts/b3f0d80f-3db1-4f5a-a10d-0123456789ab \
  -H "Content-Type: application/json" \
  -d '{
        "title": "Escalate PSP Timeout (Short name)",
        "description": "Short summary"
      }'
```

**Response — 200 OK**
```json
{
  "id": "b3f0d80f-3db1-4f5a-a10d-0123456789ab",
  "title": "Escalate PSP Timeout (Short name)",
  "content": "Investigate PSP latencies > {{latency_threshold}}ms...",
  "description": "Short summary",
  "collection_id": "c2c1d1de-9d7a-4de6-9af1-fa3d73c5b7a5",
  "created_at": "2024-02-12T18:41:31.123456",
  "updated_at": "2024-02-12T19:15:44.000000"
}
```

**Errors**
- `404 Not Found` when the prompt does not exist.
- `400 Bad Request` if a patched `collection_id` is unknown.

### Delete Prompt — `DELETE /prompts/{prompt_id}`
Permanently remove a prompt.

**Response — 204 No Content**
Empty body.

**Error**
- `404 Not Found` if the prompt does not exist.

---

## Collections
Collections group related prompts.

| Field | Type | Notes |
|-------|------|-------|
| `id` | `string` | Read-only UUID. |
| `name` | `string` | Required, 1–100 chars. |
| `description` | `string \| null` | Optional, ≤500 chars. |
| `created_at` | `string` | Read-only ISO timestamp. |

### List Collections — `GET /collections`
Retrieve all collections.

**Response — 200 OK**
```json
{
  "collections": [
    {
      "id": "c2c1d1de-9d7a-4de6-9af1-fa3d73c5b7a5",
      "name": "Payments - SEV",
      "description": "Incident runbooks for payment outages",
      "created_at": "2024-02-12T18:35:10.000001"
    }
  ],
  "total": 1
}
```

### Retrieve Collection — `GET /collections/{collection_id}`
Fetch a collection by UUID.

**Response — 200 OK**
```json
{
  "id": "c2c1d1de-9d7a-4de6-9af1-fa3d73c5b7a5",
  "name": "Payments - SEV",
  "description": "Incident runbooks for payment outages",
  "created_at": "2024-02-12T18:35:10.000001"
}
```

**Error**
- `404 Not Found` if the collection does not exist.

### Create Collection — `POST /collections`
Create a new collection.

**Request body**
| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Collection title (1–100 chars). |
| `description` | No | Optional summary/criteria. |

**Example request**
```bash
curl -X POST http://localhost:8000/collections \
  -H "Content-Type: application/json" \
  -d '{
        "name": "Payments - SEV",
        "description": "Incident runbooks for payment outages"
      }'
```

**Response — 201 Created**
```json
{
  "id": "c2c1d1de-9d7a-4de6-9af1-fa3d73c5b7a5",
  "name": "Payments - SEV",
  "description": "Incident runbooks for payment outages",
  "created_at": "2024-02-12T18:35:10.000001"
}
```

### Delete Collection — `DELETE /collections/{collection_id}`
Delete a collection. Existing prompts are retained, but their `collection_id` is automatically set to `null` so they become unassigned.

**Response — 204 No Content**
Empty body.

**Errors**
- `404 Not Found` if the collection does not exist.

---

## Change Log
| Date | Update |
|------|--------|
| 2024-02-12 | Initial publication of comprehensive API reference, including endpoint examples, error formats, and authentication notes. |
