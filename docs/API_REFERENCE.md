# API Reference

This file documents the backend API endpoints for PromptLab (FastAPI).

Base URL: http://127.0.0.1:8000/

## Health

- GET `/health`
  - Response: 200
  - Body: `{ "status": "healthy", "version": "0.1.0" }`

  Example (curl):

```bash
curl -s http://127.0.0.1:8000/health | jq
```

## Prompts

- GET `/prompts`
  - Query parameters:
    - `collection_id` (optional): filter prompts by collection id
    - `search` (optional): text search across title and description
  - Response: 200 `{ "prompts": [...], "total": <int> }`

  Example (list prompts):

```bash
curl -s "http://127.0.0.1:8000/prompts?search=template" | jq
```

- GET `/prompts/{prompt_id}`
  - Path param: `prompt_id` (string)
  - Response: 200 `Prompt` object or 404 if not found

  Example (get a single prompt):

```bash
curl -s http://127.0.0.1:8000/prompts/abcd-1234 | jq
```

- POST `/prompts`
  - Body: `PromptCreate` (title, content, description?, collection_id?)
  - Response: 201 `Prompt` (created)

  Example (create):

```bash
curl -s -X POST http://127.0.0.1:8000/prompts \
  -H "Content-Type: application/json" \
  -d '{"title":"Hello","content":"Write a short poem about AI.","description":"Poem generator"}' | jq
```

  Sample response (201):

```json
{
  "id": "abcd-1234",
  "title": "Hello",
  "content": "Write a short poem about AI.",
  "description": "Poem generator",
  "collection_id": null,
  "created_at": "2026-02-28T12:34:56.789Z",
  "updated_at": "2026-02-28T12:34:56.789Z"
}
```

- PUT `/prompts/{prompt_id}`
  - Body: `PromptUpdate` (full replacement)
  - Response: 200 `Prompt` or 404 if missing

  Example (replace):

```bash
curl -s -X PUT http://127.0.0.1:8000/prompts/abcd-1234 \
  -H "Content-Type: application/json" \
  -d '{"title":"Hello v2","content":"Updated content","description":"Updated"}' | jq
```

- PATCH `/prompts/{prompt_id}`
  - Body: partial fields (only provided fields are changed)
  - Response: 200 `Prompt` or 404 if missing

  Example (partial update):

```bash
curl -s -X PATCH http://127.0.0.1:8000/prompts/abcd-1234 \
  -H "Content-Type: application/json" \
  -d '{"description":"Add a tone: humorous"}' | jq
```

- DELETE `/prompts/{prompt_id}`
  - Response: 204 on success, 404 if not found

  Example (delete):

```bash
curl -s -X DELETE http://127.0.0.1:8000/prompts/abcd-1234 -I
```

## Collections

- GET `/collections`
  - Response: 200 `{ "collections": [...], "total": <int> }`

  Example:

```bash
curl -s http://127.0.0.1:8000/collections | jq
```

- GET `/collections/{collection_id}`
  - Response: 200 `Collection` or 404

- POST `/collections`
  - Body: `CollectionCreate` (name, description)
  - Response: 201 `Collection`

  Example (create collection):

```bash
curl -s -X POST http://127.0.0.1:8000/collections \
  -H "Content-Type: application/json" \
  -d '{"name":"Poems","description":"Short poem templates"}' | jq
```

- DELETE `/collections/{collection_id}`
  - Behavior: deletes the collection and nullifies `collection_id` on any
    prompts that referenced it (preserves the prompts and updates their
    `updated_at`).
  - Response: 204 or 404 if not found

## Error responses

- 400 Bad Request: invalid input (e.g., `collection_id` not found on create/update)
- 404 Not Found: resource not found
- 500 Internal Server Error: unexpected server error

For interactive docs point your browser at `/docs` when the server is running.
