# Project AI/Coding Instructions

These instructions describe coding patterns, expectations, and conventions for
automated coding assistants working on PromptLab.

Guidelines
- Language: Python 3.11, FastAPI for backend, Pydantic for models.
- Tests: Use pytest and fastapi.testclient. All endpoints must have tests.
- Style: Follow existing project style (concise functions, clear names). Add
  Google-style docstrings to public functions and classes.
- Error handling: Return HTTPException with appropriate status codes. Validate
  external references (e.g. collection_id) and return 400 when invalid.
- Storage: Use the `storage` instance in `app.storage`. When adding persistence,
  preserve current Storage API (create/get/update/delete) and keep it replaceable.

Commit messages
- Use conventional commit style (feat:, fix:, docs:, test:, chore:).

Testing requirements
- Add at least one unit/integration test per new API behavior.
- Clear storage in tests using the existing autouse fixture.

PRs
- Keep changes small and focused. Add tests and update docs when behavior
  changes.
