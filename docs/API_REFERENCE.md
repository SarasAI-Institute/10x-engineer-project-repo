# API Reference

This file documents the backend API endpoints for PromptLab (FastAPI).

Base URL: http://127.0.0.1:8000/

## Health

- GET `/health`
  - Response: 200
  - Body: `{ "status": "healthy", "version": "0.1.0" }`

## Prompts

- GET `/prompts`
  - Query parameters:
    - `collection_id` (optional): filter prompts by collection id
    - `search` (optional): text search across title and description
  - Response: 200 `{ prompts: [...], total: <int> }`

- GET `/prompts/{prompt_id}`
  - Path param: `prompt_id` (string)
  - Response: 200 `Prompt` object or 404 if not found

- POST `/prompts`
  - Body: `PromptCreate` (title, content, description?, collection_id?)
  - Response: 201 `Prompt` (created)

- PUT `/prompts/{prompt_id}`
  - Body: `PromptUpdate` (full replacement)
  - Response: 200 `Prompt` or 404 if missing

- PATCH `/prompts/{prompt_id}`
  - Body: partial fields (only provided fields are changed)
  - Response: 200 `Prompt` or 404 if missing

- DELETE `/prompts/{prompt_id}`
  - Response: 204 on success, 404 if not found

## Collections

- GET `/collections`
  - Response: 200 `{ collections: [...], total: <int> }`

- GET `/collections/{collection_id}`
  - Response: 200 `Collection` or 404

- POST `/collections`
  - Body: `CollectionCreate` (name, description)
  - Response: 201 `Collection`

- DELETE `/collections/{collection_id}`
  - Behavior: deletes the collection and nullifies `collection_id` on any
    prompts that referenced it (preserves prompts).
  - Response: 204 or 404 if not found

## Error responses

- 400 Bad Request: invalid input (e.g., collection_id not found on create/update)
- 404 Not Found: resource not found
- 500 Internal Server Error: unexpected server error

For interactive docs point your browser at `/docs` when the server is running.
