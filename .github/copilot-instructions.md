**PromptLab – AI Coding Agent Instructions (Copilot)**

These instructions define coding standards, architectural guidelines, and development practices for contributing to the PromptLab codebase. Follow them for all implementations, enhancements, and refactors.

**1) Project Coding Standards**
Language and Style

Use Python 3.10+ features consistently.

Follow PEP 8 for formatting and naming.

Use type hints for all public functions and methods.

Keep functions small and focused (prefer under 30 lines).

Prioritize clarity and maintainability over clever or compact code.

Docstrings

Use Google-style docstrings for every function, method, and class.

Each docstring must include:

A concise summary line

Args / Returns

Raises (if applicable)

Example (where it improves clarity)

Ensure docstrings remain accurate and updated with code changes.

Imports

Follow standard import grouping:

Standard library

Third-party libraries

Local application imports (app.*)

Avoid wildcard imports (import *).

Prefer explicit and readable imports.

**2) Preferred Patterns and Conventions**
FastAPI Endpoints

Keep endpoints thin and focused:

Validate input

Delegate logic to storage or service layer

Return structured response models

Use HTTPException for expected error scenarios (e.g., not found, invalid input).

Always return Pydantic response models for consistency.

Data Models (Pydantic)

Define all fields using Field(..., description="...").

Separate request and response models:

Request: PromptCreate, PromptUpdate

Response: Prompt (includes id, timestamps)

Avoid mixing input validation and response representation.

Storage Layer

Encapsulate all storage logic within app/storage.py.

Do not introduce global mutable state outside the Storage class (except the storage singleton).

Return:

None when an object is not found

False for failed delete operations

Do not raise exceptions in the storage layer; delegate error handling to the API layer.

Utility Functions

Place reusable, generic logic in app/utils.py.

Keep utilities independent of FastAPI or framework-specific code.

Ensure functions are side-effect free unless explicitly required.

**3) File Naming Conventions**

Follow the established project structure:

backend/app/api.py → FastAPI routes

backend/app/models.py → Pydantic models

backend/app/storage.py → in-memory storage

backend/app/utils.py → helper utilities

backend/tests/ → pytest test cases

docs/ → Markdown documentation

specs/ → feature specifications

.github/ → workflows and development instructions

Naming rules:

Python files: snake_case.py

Classes: PascalCase

Functions and variables: snake_case

Constants: UPPER_SNAKE_CASE

**4) Error Handling Approach**
API Layer (FastAPI)

Use HTTPException with clear, actionable error messages:

404 for missing resources (prompt/collection)

400 for invalid references (e.g., non-existent collection_id)

Do not return raw dictionaries for errors.

Always rely on HTTPException(detail="...") for consistency.

Storage Layer

Do not raise exceptions for missing or invalid data.

Return:

None when a resource is not found

False when deletion fails

Let the API layer translate these outcomes into HTTP responses.

Validation

Use Pydantic models for request validation.

Allow FastAPI to handle schema validation errors (422 Unprocessable Entity).

**5) Testing Requirements**
General Rules

Every new feature must include corresponding tests.

Every bug fix must include a test that fails before the fix and passes after.

Prefer:

Unit tests for utilities and storage

API tests for endpoint behavior

Avoid redundant or low-value tests.

Tools

Use pytest.

Place all tests under backend/tests/.

Test names must clearly describe behavior:

test_create_prompt_returns_201

test_get_prompt_returns_404_when_missing

Expectations

Run tests locally before committing:

pytest -v

Ensure tests are deterministic and order-independent.

Maintain consistent and predictable behavior across test runs.

**Implementation Notes (Project-Specific)**

Prompts include timestamps: created_at, updated_at.

All update operations must refresh updated_at.

When deleting a collection, associated prompts must be unassigned (collection_id = None) to avoid orphaned references.

Authentication is not part of the current scope; do not introduce auth unless explicitly required by a feature specification.

**Output Quality Requirements**

When generating code changes:

Provide clean and minimal diffs.

Avoid unnecessary refactoring unless explicitly requested.

Keep documentation (README, API_REFERENCE.md) aligned with any changes to endpoints or data models.

Ensure changes are consistent with existing patterns and conventions.