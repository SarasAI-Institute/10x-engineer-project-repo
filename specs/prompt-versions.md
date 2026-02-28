# Prompt Versions (spec)

## Overview

Track versions of prompts so users can view and revert previous prompt states.

## User stories
- As a user I can see a list of previous versions for a prompt.
- As a user I can revert a prompt to a previous version.

## Data model changes
- Add `versions` list to `Prompt` (or separate `PromptVersion` records).
- `PromptVersion` fields: id, prompt_id, title, content, description, collection_id, created_at

## API endpoints
- GET `/prompts/{id}/versions` - list versions
- POST `/prompts/{id}/versions/revert` - revert to a version id

## Edge cases
- Reverting should create a new version representing the revert action.
- Limit number of stored versions or provide pruning/retention policy.
