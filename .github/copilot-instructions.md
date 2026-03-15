# PromptLab Coding Agent Instructions

Use this playbook whenever you generate code for PromptLab. Keep the tone practical, the code safe, and the docs updated.

## Project Coding Standards
1. **Python style.** Follow PEP 8. Use clear names, full type hints, and Google-style docstrings on every public class, function, and FastAPI route. Keep functions short (about 20 lines or fewer).
2. **Pydantic first.** Use the models in `app/models.py` (or new Pydantic models) instead of raw dicts. When you update data, create a fresh model instance rather than mutating an existing one.
3. **Timestamps.** Call `get_current_time()` for all `created_at`/`updated_at` fields. Always store UTC datetimes and return ISO-8601 strings.
4. **Docs stay current.** If behavior changes, update README, specs, and API reference so they match reality. Keep inline comments short and useful.

## Preferred Patterns & Conventions
1. **FastAPI flow.** Each route should: (a) validate input with a Pydantic schema, (b) run guards/lookups, (c) call the storage layer, (d) return the proper response model. Push shared logic into `app/utils.py`.
2. **Storage boundary.** Talk to data through `app.storage.storage` (e.g., `storage.get_prompt`). Never reach into private fields of the backend implementation—this keeps future storage swaps easy.
3. **Collections + prompts.** Any prompt that references a collection must confirm the collection exists. When collections are deleted, clear orphaned `collection_id` fields so nothing points to a missing record.
4. **Filtering helpers.** Reuse helpers such as `sort_prompts_by_date`, `filter_prompts_by_collection`, and `search_prompts`. Add new helpers in `app/utils.py`, cover them with tests, then use them in the API.
5. **Frontend basics.** Component files use PascalCase names (e.g., `PromptList.jsx`). Keep API calls under `frontend/src/api/`, and keep hooks/components focused on one job.

## File Naming Conventions
- Python modules: `snake_case.py` (tests mirror the same name: `tests/test_module.py`).
- Schemas/models: stay in `app/models.py` or split into `app/models/<topic>.py` using snake_case filenames.
- Docs/specs: Markdown files live in `docs/` or `specs/` with kebab-case names (`prompt-versions.md`).
- Frontend: components use PascalCase, hooks use `useThing.ts/tsx`, utilities stay snake_case.
- Tooling: GitHub Actions in `.github/workflows/*.yml`; Docker files at repo root (`docker-compose.yml`) or service root (`backend/Dockerfile`).

## Error Handling Approach
1. **Right status code.** Raise `HTTPException` with the correct status (404 missing prompt, 400 bad request, 409 conflict, etc.) and a helpful `detail`. Don’t let expected errors become 500s.
2. **Validate with Pydantic.** Prefer `field_validator` or `model_validator` for custom rules instead of manual parsing in routes.
3. **Return safe signals.** Storage and utility functions should return `None`/`False` when something is missing; let callers translate that into HTTP responses. Avoid bare `except`; catch specific exceptions and log context before re-raising.
4. **Frontend feedback.** When working on the React app, surface API failures with the shared error components and show user-friendly copy.

## Testing Requirements
1. **Coverage goal.** Keep test coverage at or above 80%. Every feature or bug fix needs matching pytest coverage.
2. **Test placement.** Backend tests live in `backend/tests/` (e.g., `test_api.py`, `test_storage.py`). Frontend tests belong in `frontend/src/__tests__/` or as `*.test.jsx/ts` files.
3. **Test strategy.** Write or update tests *before* fixing bugs. Cover success and failure paths, including edge cases like invalid IDs or empty inputs.
4. **Commands to run.** From `backend/`, run `pytest tests/ -v --cov=app --cov-report=term-missing`. From `frontend/`, run `npm test` or `npm run test -- --coverage` once tests exist.
5. **CI stays green.** Ensure the GitHub Actions workflow passes (lint, tests, coverage). Update the workflow only if tooling changes.

Keep these instructions handy. Clear code, clean tests, and up-to-date docs make PromptLab easy to maintain and extend.