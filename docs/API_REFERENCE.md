# API Reference

## Overview

The PromptLab API is a RESTful API built with FastAPI. All endpoints return JSON responses and follow standard HTTP conventions for status codes and methods.

**Base URL:** `http://localhost:8000`

**API Documentation:** `http://localhost:8000/docs` (Interactive Swagger UI)

**OpenAPI Schema:** `http://localhost:8000/openapi.json`

---

## Table of Contents

- [Authentication](#authentication)
- [Health Check](#health-check)
- [Prompts](#prompts)
  - [List Prompts](#list-prompts)
  - [Get Prompt](#get-prompt)
  - [Create Prompt](#create-prompt)
  - [Update Prompt (PUT)](#update-prompt-put)
  - [Partial Update (PATCH)](#partial-update-patch)
  - [Delete Prompt](#delete-prompt)
- [Collections](#collections)
  - [List Collections](#list-collections)
  - [Get Collection](#get-collection)
  - [Create Collection](#create-collection)
  - [Delete Collection](#delete-collection)
- [Error Responses](#error-responses)
- [Data Models](#data-models)

---

## Authentication

Currently, the API does not require authentication. This will be added in future versions.

---

## Health Check

### GET /health

Check if the API is running and get version information.

**Response:** `200 OK`

```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

---

## Prompts

### List Prompts

**GET** `/prompts`

Retrieve a list of all prompts with optional filtering.

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `collection_id` | string | No | Filter prompts by collection ID |
| `search` | string | No | Search prompts by title or description |

#### Response: `200 OK`

```json
{
  "prompts": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Email Template",
      "content": "Hello {{name}}, this is regarding {{subject}}",
      "description": "Generic email template",
      "collection_id": "123e4567-e89b-12d3-a456-426614174000",
      "created_at": "2026-02-20T10:30:00Z",
      "updated_at": "2026-02-20T10:30:00Z"
    }
  ],
  "total": 1
}
```

#### Example Requests

```bash
# Get all prompts
curl http://localhost:8000/prompts

# Filter by collection
curl http://localhost:8000/prompts?collection_id=123e4567-e89b-12d3-a456-426614174000

# Search prompts
curl http://localhost:8000/prompts?search=email

# Combine filters
curl http://localhost:8000/prompts?collection_id=123&search=template
```

---

### Get Prompt

**GET** `/prompts/{prompt_id}`

Retrieve a single prompt by its ID.

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt_id` | string | Yes | The unique prompt ID |

#### Response: `200 OK`

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Email Template",
  "content": "Hello {{name}}, this is regarding {{subject}}",
  "description": "Generic email template",
  "collection_id": "123e4567-e89b-12d3-a456-426614174000",
  "created_at": "2026-02-20T10:30:00Z",
  "updated_at": "2026-02-20T10:30:00Z"
}
```

#### Error Response: `404 Not Found`

```json
{
  "detail": "Prompt not found"
}
```

---

### Create Prompt

**POST** `/prompts`

Create a new prompt.

#### Request Body

```json
{
  "title": "Email Template",
  "content": "Hello {{name}}, this is regarding {{subject}}",
  "description": "Generic email template",
  "collection_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `title` | string | Yes | 1-200 chars | Prompt title |
| `content` | string | Yes | Min 1 char | Prompt template content |
| `description` | string | No | Max 500 chars | Prompt description |
| `collection_id` | string | No | Valid UUID | Collection this prompt belongs to |

#### Response: `201 Created`

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Email Template",
  "content": "Hello {{name}}, this is regarding {{subject}}",
  "description": "Generic email template",
  "collection_id": "123e4567-e89b-12d3-a456-426614174000",
  "created_at": "2026-02-20T10:30:00Z",
  "updated_at": "2026-02-20T10:30:00Z"
}
```

#### Error Response: `400 Bad Request`

```json
{
  "detail": "Collection not found"
}
```

---

### Update Prompt (PUT)

**PUT** `/prompts/{prompt_id}`

Perform a full update of a prompt. All fields should be provided (unprovided fields will fall back to existing values).

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt_id` | string | Yes | The unique prompt ID |

#### Request Body

```json
{
  "title": "Updated Email Template",
  "content": "Hi {{name}}, regarding {{subject}}...",
  "description": "Updated description",
  "collection_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

#### Response: `200 OK`

The updated prompt with refreshed `updated_at` timestamp.

#### Error Responses

- `404 Not Found` - Prompt does not exist
- `400 Bad Request` - Invalid collection_id

---

### Partial Update (PATCH)

**PATCH** `/prompts/{prompt_id}`

Perform a partial update of a prompt. Only provide the fields you want to update.

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt_id` | string | Yes | The unique prompt ID |

#### Request Body

```json
{
  "title": "New Title Only"
}
```

All fields are optional. Only provided fields will be updated.

#### Response: `200 OK`

The updated prompt with refreshed `updated_at` timestamp.

#### Error Responses

- `404 Not Found` - Prompt does not exist
- `400 Bad Request` - Invalid collection_id

---

### Delete Prompt

**DELETE** `/prompts/{prompt_id}`

Delete a prompt permanently.

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt_id` | string | Yes | The unique prompt ID |

#### Response: `204 No Content`

No response body.

#### Error Response: `404 Not Found`

```json
{
  "detail": "Prompt not found"
}
```

---

## Collections

### List Collections

**GET** `/collections`

Retrieve a list of all collections.

#### Response: `200 OK`

```json
{
  "collections": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "name": "Marketing",
      "description": "Marketing-related prompts",
      "created_at": "2026-02-20T10:00:00Z"
    }
  ],
  "total": 1
}
```

---

### Get Collection

**GET** `/collections/{collection_id}`

Retrieve a single collection by its ID.

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `collection_id` | string | Yes | The unique collection ID |

#### Response: `200 OK`

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Marketing",
  "description": "Marketing-related prompts",
  "created_at": "2026-02-20T10:00:00Z"
}
```

#### Error Response: `404 Not Found`

```json
{
  "detail": "Collection not found"
}
```

---

### Create Collection

**POST** `/collections`

Create a new collection.

#### Request Body

```json
{
  "name": "Marketing",
  "description": "Marketing-related prompts"
}
```

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `name` | string | Yes | 1-100 chars | Collection name |
| `description` | string | No | Max 500 chars | Collection description |

#### Response: `201 Created`

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Marketing",
  "description": "Marketing-related prompts",
  "created_at": "2026-02-20T10:00:00Z"
}
```

---

### Delete Collection

**DELETE** `/collections/{collection_id}`

Delete a collection permanently. All prompts in this collection will have their `collection_id` set to `null` (orphaned).

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `collection_id` | string | Yes | The unique collection ID |

#### Response: `204 No Content`

No response body.

#### Error Response: `404 Not Found`

```json
{
  "detail": "Collection not found"
}
```

---

## Error Responses

The API uses standard HTTP status codes:

| Status Code | Meaning |
|-------------|---------|
| `200` | OK - Request succeeded |
| `201` | Created - Resource created successfully |
| `204` | No Content - Request succeeded, no response body |
| `400` | Bad Request - Invalid input data |
| `404` | Not Found - Resource does not exist |
| `422` | Unprocessable Entity - Validation error |
| `500` | Internal Server Error - Server error |

### Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Validation Errors (422)

```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## Data Models

### Prompt

```typescript
{
  id: string;              // UUID
  title: string;           // 1-200 characters
  content: string;         // Min 1 character
  description?: string;    // Optional, max 500 characters
  collection_id?: string;  // Optional UUID
  created_at: string;      // ISO 8601 datetime
  updated_at: string;      // ISO 8601 datetime
}
```

### Collection

```typescript
{
  id: string;              // UUID
  name: string;            // 1-100 characters
  description?: string;    // Optional, max 500 characters
  created_at: string;      // ISO 8601 datetime
}
```

### Template Variables

Prompts support template variables in the format `{{variable_name}}`. These can be used for dynamic content replacement.

**Example:**

```
Hello {{name}}, your order {{order_id}} is ready for pickup.
```

Variables: `name`, `order_id`

---

## Rate Limiting

Currently, there is no rate limiting. This will be added in future versions.

---

## CORS

The API allows CORS from all origins (`*`). In production, this should be restricted to specific domains.

---

## Versioning

The current API version is `0.1.0`. Future versions may introduce breaking changes with appropriate versioning in the URL path (e.g., `/v2/prompts`).
