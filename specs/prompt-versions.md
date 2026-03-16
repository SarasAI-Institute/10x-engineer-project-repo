# Prompt Versions Feature Specification

## 1. Plain-Language Overview
- Every time someone edits a prompt, we should keep a frozen copy of the previous version.
- These copies let us answer three simple questions: *When did this change? Who changed it? Can I undo it?*
- Version history must be easy to browse so on-call engineers can recover quickly during an incident review.

## 2. User Stories and What “Done” Means
1. **Capture every edit (PV-1).**
   - PUT and PATCH automatically save the old prompt as a version *before* the new data is stored.
   - Saved version keeps the full prompt payload plus metadata: editor, timestamps, optional change note.
2. **See the history (PV-2).**
   - `GET /prompts/{id}/versions` lists versions newest-first.
   - Each item shows enough info to pick the right version (number, editor, change note, created_at).
3. **Inspect one version (PV-3).**
   - `GET /prompts/{id}/versions/{version_id}` returns the exact snapshot.
   - Return 404 if either the prompt or the version is missing.
4. **Roll back (PV-4).**
   - `POST /prompts/{id}/versions/{version_id}/restore` copies the snapshot into the live prompt.
   - The restore action also stores the pre-restore state as another version and refreshes `updated_at`.
5. **Explain why (PV-5).**
   - PUT and PATCH accept an optional `change_note` (1–255 chars).
   - The note is saved with the new version so readers know the intent of the change.

## 3. Data Model Changes
- **New `PromptVersion` model** with fields: `id`, `prompt_id`, `version_number` (per-prompt counter starting at 1), `title`, `content`, `description`, `collection_id`, `created_at`, `editor` (default "system"), `change_note`.
- **Prompt model update:** add read-only `current_version` that mirrors the latest `version_number`.
- **Storage additions:**
  - `create_prompt_version(prompt_version)`
  - `get_prompt_versions(prompt_id) -> List`
  - `get_prompt_version(prompt_id, version_id)`
  - `get_next_version_number(prompt_id)` to keep numbering in order.

## 4. API Changes
- **List versions:** `GET /prompts/{prompt_id}/versions` → `{ prompt_id, versions: [ {id, version_number, editor, change_note, created_at} ], total }`.
- **Get a version:** `GET /prompts/{prompt_id}/versions/{version_id}` → returns full `PromptVersion` payload.
- **Restore a version:** `POST /prompts/{prompt_id}/versions/{version_id}/restore`
  - Body: `{ "change_note": Optional[str] }`
  - Response: updated `Prompt`.
- **Change note support:** existing PUT/PATCH endpoints accept a `change_note` field and pass it into the version-creation logic.

## 5. Edge Cases to Handle
- Requests against a missing prompt or version must return 404.
- Prompts with no edits return an empty list from the versions endpoint (still HTTP 200).
- Increment `version_number` in a thread-safe way so parallel updates cannot reuse the same number.
- Version rows may be large; store the full content even if long (no truncation now).
- Reject `change_note` values longer than 255 characters with a 422 response.
- Deleting a prompt should also delete or archive its versions to prevent orphans.
- Restoring the currently active version should still record a new version so the audit trail stays intact.
