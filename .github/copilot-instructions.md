# Copilot Instructions for PromptLab

These guidelines help AI copilots and contributors stay aligned with our coding standards and project goals.

## Project Goals
1. Deliver a stable backend with comprehensive documentation.
2. Respect the in-memory storage abstraction while adding missing features.
3. Enable future frontend and DevOps work through clear APIs and specs.

## Coding Standards
- Follow PEP 8 and prefer expressive, readable Python.
- Use Google-style docstrings for every function, including Args/Returns/Raises when applicable.
- Favor dependency injection via parameters and keep business logic in small, testable units.
- Keep helper modules (e.g., `utils.py`, `storage.py`) focused on a single responsibility.
- Preserve type hints and leverage Pydantic models for validation and serialization.

## API Patterns
- Always validate referenced collection IDs before persisting prompts (or raise HTTP 400).
- Do not mutate existing prompt metadata unless explicitly updating `updated_at`.
- Keep response models consistent by returning the same data shape as defined in `models.py`.

## Documentation & Tests
- Add README sections for overview, installation, API summary, usage, and docs/spec links.
- Update `docs/API_REFERENCE.md` or specs when introducing or modifying endpoints.
- Write tests that exercise new logic and ensure existing ones still pass.
- Run `pytest tests/test_api.py -q` before finalizing changes and mention the command in updates.

## Communication
- When generating code, include brief comments explaining complex sections and mention related docs.
- If unsure about expected behavior, prompt the user before guessing.
- Always keep error messages clear, professional, and friendly.
