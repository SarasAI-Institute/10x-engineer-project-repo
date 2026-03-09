# API Reference

This document summarizes every backend endpoint with payload examples and expected error formats.

## Health Check

- **Endpoint:** `GET /health`
- **Description:** Verifies the service is running and reports the current version.

<details>
<summary>Response (200)</summary>

```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```
</details>

## Prompt Endpoints

### List Prompts
- **Endpoint:** `GET /prompts`
- **Query Parameters:**
  - `collection_id` (optional) – filters prompts by the owning collection.
  - `search` (optional) – case-insensitive search term that matches titles or descriptions.

<details>
<summary>Response (200)</summary>

```json
{
  "prompts": [
    {
      "id": "abc123",
      "title": "Review Code",
      "content": "Review {{code}}",
      "description": "A code review prompt",
      "collection_id": null,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1
}
```
</details>

### Get Prompt by ID
- **Endpoint:** `GET /prompts/{prompt_id}`
- **Description:** Returns the full prompt data for the specified identifier.

<details>
<summary>Response (200)</summary>

```json
{
  "id": "abc123",
  "title": "Review Code",
  "content": "Review {{code}}",
  "description": "A code review prompt",
  "collection_id": null,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```
</details>

<details>
<summary>Error (404)</summary>

```json
{
  "detail": "Prompt not found"
}
```
</details>

### Create Prompt
- **Endpoint:** `POST /prompts`
- **Request Body:**

```json
{
  "title": "Review Code",
  "content": "Review {{code}}",
  "description": "Audit request",
  "collection_id": "col123"
}
```

<details>
<summary>Response (201)</summary>

```json
{
  "id": "abc123",
  "title": "Review Code",
  "content": "Review {{code}}",
  "description": "Audit request",
  "collection_id": "col123",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```
</details>

<details>
<summary>Error (400)</summary>

```json
{
  "detail": "Collection not found"
}
```
</details>

### Replace Prompt (PUT)
- **Endpoint:** `PUT /prompts/{prompt_id}`
- **Request Body:** same shape as create, except optional fields can be omitted to retain existing value during merge.

<details>
<summary>Response (200)</summary>

```json
{
  "id": "abc123",
  "title": "Updated Title",
  "content": "Updated content",
  "description": "Updated description",
  "collection_id": null,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-02T00:00:00Z"
}
```
</details>

<details>
<summary>Error (404)</summary>

```json
{
  "detail": "Prompt not found"
}
```
</details>

### Partial Update (PATCH)
- **Endpoint:** `PATCH /prompts/{prompt_id}`
- **Description:** Only the fields present in the body are updated; `updated_at` is refreshed automatically.
- **Request Body:** Provide any combination of `title`, `content`, `description`, and `collection_id`.

```json
{
  "description": "Clarified guidance"
}
```

<details>
<summary>Response (200)</summary>

```json
{
  "description": "Clarified guidance",
  "updated_at": "2024-01-02T00:00:00Z",
  "title": "Review Code",
  "content": "Review {{code}}",
  "collection_id": null,
  "id": "abc123",
  "created_at": "2024-01-01T00:00:00Z"
}
```
</details>

<details>
<summary>Error (400 - empty payload)</summary>

```json
{
  "detail": "Provide at least one field to update for a PATCH request."
}
```
</details>

<details>
<summary>Error (404)</summary>

```json
{
  "detail": "Prompt with id 'abc123' was not found."
}
```
</details>

### Delete Prompt
- **Endpoint:** `DELETE /prompts/{prompt_id}`
- **Response:** HTTP 204 with no body.

<details>
<summary>Error (404)</summary>

```json
{
  "detail": "Prompt not found"
}
```
</details>

## Collection Endpoints

### List Collections
- **Endpoint:** `GET /collections`

<details>
<summary>Response (200)</summary>

```json
{
  "collections": [
    {
      "id": "col123",
      "name": "Engineering",
      "description": "Developer prompts",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1
}
```
</details>

### Get Collection
- **Endpoint:** `GET /collections/{collection_id}`

<details>
<summary>Response (200)</summary>

```json
{
  "id": "col123",
  "name": "Engineering",
  "description": "Developer prompts",
  "created_at": "2024-01-01T00:00:00Z"
}
```
</details>

<details>
<summary>Error (404)</summary>

```json
{
  "detail": "Collection not found"
}
```
</details>

### Create Collection
- **Endpoint:** `POST /collections`
- **Request Body:**

```json
{
  "name": "Engineering",
  "description": "Developer-focused prompts"
}
```

<details>
<summary>Response (201)</summary>

```json
{
  "id": "col123",
  "name": "Engineering",
  "description": "Developer-focused prompts",
  "created_at": "2024-01-01T00:00:00Z"
}
```
</details>

### Delete Collection
- **Endpoint:** `DELETE /collections/{collection_id}`
- **Behavior:** Removes the collection but leaves prompts untouched (they retain their `collection_id` unless manually cleared).
- **Response:** HTTP 204 with no body.

<details>
<summary>Error (404)</summary>

```json
{
  "detail": "Collection not found"
}
```
</details>
