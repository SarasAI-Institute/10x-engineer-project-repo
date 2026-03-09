# Prompt Versioning Specification

## Project Goals
- Preserve each prompt change so engineers can audit modifications and roll back when needed.
- Provide a lightweight version history that integrates with the existing in-memory storage.
- Keep the API consistent with FastAPI best practices and enable frontend clients to inspect and restore historical states.

## User Stories
1. **As an AI engineer, I want to view a prompt's history so I can understand who changed it and why.**
   - **Given** a prompt exists
   - **When** I request `/prompts/{id}/versions`
   - **Then** I receive a list of timestamped versions sorted newest-first with author metadata (if available).

2. **As an engineer, I want to restore a previous prompt version so I can undo accidental changes.**
   - **Given** I am viewing a version history entry
   - **When** I POST to `/prompts/{id}/versions/{version_id}/restore`
   - **Then** the prompt is updated to match the archived payload and `updated_at` is refreshed.

3. **As a developer, I want each version record to include the changed fields so I can highlight differences.**
   - **Given** a version entry
   - **Then** the payload records the delta between versions (title, content, etc.) along with timestamps.

## Data Model Changes
- Introduce `PromptVersion` model with:
  - `id`: uuid
  - `prompt_id`: reference to the original prompt
  - `snapshot`: full `Prompt` payload at the time of change
  - `created_at`: timestamp
  - `author`: optional string (e.g., API user email)

- Update storage to keep a `Dict[str, List[PromptVersion]]` mapping prompt IDs to history.
- Each `create_prompt`, `update_prompt`, and `patch_prompt` call appends a new version entry before persisting.

## API Endpoints
### GET `/prompts/{id}/versions`
- **Description:** List all stored versions for a prompt.
- **Response (200):**
```json
{
  "versions": [
    {
      "id": "ver-1",
      "prompt_id": "abc123",
      "created_at": "2024-01-02T10:00:00Z",
      "author": "alice@example.com",
      "snapshot": {
        "title": "Review Code",
        "content": "Review {{code}}",
        "description": "Initial version",
        "collection_id": null
      }
    }
  ],
  "total": 1
}
```
- **Query Params:** `limit`, `cursor` (future paging)
- **Errors:** 404 if prompt not found.

### POST `/prompts/{id}/versions/{version_id}/restore`
- **Description:** Replace the active prompt with the archived snapshot.
- **Response (200):** Returns the restored prompt (same shape as `Prompt`).
- **Errors:** 404 if prompt or version missing; 400 if restoration would violate validation (e.g., missing title).

### GET `/prompts/{id}/versions/{version_id}` (Optional)
- Could be used to inspect a single snapshot; returns the `PromptVersion` payload.

## Edge Cases
- **Concurrent updates:** Only the latest prompt state is snapshotted; last-write-wins.
- **Deleted prompts:** Clearing a prompt should also prune its versions to avoid dangling data.
- **Large histories:** Keep only the last N versions per prompt (e.g., 20) or provide a TTL.
- **Missing collection:** If a past version references a deleted collection, the snapshot still captures the `collection_id`, but restoring it leaves the prompt collection unset unless the collection is re-created.
