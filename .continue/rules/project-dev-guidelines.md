---
description: PromptLab AI Coding Agent Rules
---

## Project Overview
This is a FastAPI-based AI Prompt Engineering Platform. All code generation and modifications should follow these standards.

---

## Python & FastAPI Standards

### Code Style
- Follow **PEP 8** style guide strictly
- Use **Google-style docstrings** for all functions, classes, and modules
- Maximum line length: **88 characters** (Black formatter standard)
- Use **type hints** for all function parameters and return values
- Prefer **explicit over implicit** code

### Naming Conventions
- **Files**: Use `snake_case` for all Python files (e.g., `prompt_service.py`, `auth_utils.py`)
- **Classes**: Use `PascalCase` (e.g., `PromptService`, `UserAuthentication`)
- **Functions/Methods**: Use `snake_case` (e.g., `get_prompt_by_id`, `validate_input`)
- **Constants**: Use `UPPER_SNAKE_CASE` (e.g., `MAX_PROMPT_LENGTH`, `DEFAULT_PAGE_SIZE`)
- **Private methods/attributes**: Prefix with single underscore (e.g., `_internal_helper`)
- **Pydantic Models**: Use `PascalCase` and descriptive names (e.g., `PromptCreate`, `UserResponse`)

### Type Hints
Always use type hints from `typing` module:
```python
from typing import Optional, List, Dict, Union
from datetime import datetime

def get_prompts(
    collection_id: Optional[str] = None,
    limit: int = 10,
    offset: int = 0
) -> List[Prompt]:
    """Retrieve prompts with optional filtering."""
    pass
```

---

## Project Structure Patterns

### Module Organization
```
backend/app/
├── api/              # API routes (split by domain)
│   ├── prompts.py
│   ├── collections.py
│   └── health.py
├── models/           # Pydantic models
│   ├── prompt.py
│   └── collection.py
├── services/         # Business logic
│   ├── prompt_service.py
│   └── collection_service.py
├── repositories/     # Data access layer
│   ├── prompt_repository.py
│   └── collection_repository.py
├── core/            # Configuration, dependencies
│   ├── config.py
│   └── dependencies.py
└── utils/           # Helper functions
```

### Dependency Injection
Use FastAPI's dependency injection for shared logic:
```python
from fastapi import Depends

def get_storage() -> Storage:
    """Dependency for storage access."""
    return storage

@app.get("/prompts/{prompt_id}")
def get_prompt(
    prompt_id: str,
    storage: Storage = Depends(get_storage)
) -> Prompt:
    """Get prompt by ID using dependency injection."""
    pass
```

---

## Error Handling Standards

### HTTP Exceptions
Use FastAPI's `HTTPException` with appropriate status codes:

```python
from fastapi import HTTPException, status

# 400 - Bad Request (validation errors, invalid input)
if not validate_prompt_content(data.content):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Prompt content must be at least 10 characters"
    )

# 404 - Not Found
prompt = storage.get_prompt(prompt_id)
if not prompt:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Prompt with id '{prompt_id}' not found"
    )

# 409 - Conflict
if storage.collection_exists(name):
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"Collection '{name}' already exists"
    )

# 422 - Unprocessable Entity (Pydantic validation handles this automatically)

# 500 - Internal Server Error (use sparingly, log the error)
try:
    result = external_api_call()
except Exception as e:
    logger.error(f"External API failed: {e}")
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="An unexpected error occurred"
    )
```

### Error Response Format
All errors should return consistent JSON structure:
```python
{
    "detail": "Human-readable error message",
    "error_code": "OPTIONAL_ERROR_CODE",  # For client-side handling
    "field": "field_name"  # For validation errors
}
```

### Logging
Use Python's `logging` module for all errors:
```python
import logging

logger = logging.getLogger(__name__)

try:
    risky_operation()
except ValueError as e:
    logger.warning(f"Invalid value provided: {e}")
    raise HTTPException(status_code=400, detail=str(e))
except Exception as e:
    logger.error(f"Unexpected error in operation: {e}", exc_info=True)
    raise HTTPException(status_code=500, detail="Internal server error")
```

---

## Testing Requirements

### Test Organization
```
tests/
├── unit/              # Unit tests (fast, isolated)
│   ├── test_utils.py
│   ├── test_models.py
│   └── test_services.py
├── integration/       # Integration tests (API + storage)
│   ├── test_api_prompts.py
│   └── test_api_collections.py
└── conftest.py       # Shared fixtures
```

### Test Naming Convention
- Test files: `test_<module_name>.py`
- Test classes: `Test<FeatureName>` (e.g., `TestPromptCreation`)
- Test functions: `test_<what>_<condition>_<expected>` (e.g., `test_get_prompt_nonexistent_returns_404`)

### Test Structure (AAA Pattern)
```python
def test_create_prompt_valid_data_returns_201(client: TestClient):
    """Test that creating a prompt with valid data returns 201."""
    # Arrange
    prompt_data = {
        "title": "Test Prompt",
        "content": "This is a test prompt with enough content"
    }
    
    # Act
    response = client.post("/prompts", json=prompt_data)
    
    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == prompt_data["title"]
    assert "id" in data
    assert "created_at" in data
```

### Coverage Requirements
- **Minimum coverage**: 80%
- **Target coverage**: 90%+
- All edge cases must be tested
- All error paths must be tested

### Fixtures Best Practices
```python
@pytest.fixture
def sample_prompt() -> Prompt:
    """Create a sample prompt for testing.
    
    Returns:
        Prompt: A valid prompt instance.
    """
    return Prompt(
        title="Sample Prompt",
        content="This is sample content for testing purposes"
    )

@pytest.fixture(autouse=True)
def reset_storage():
    """Reset storage before each test."""
    storage.clear()
    yield
    storage.clear()
```

---

## FastAPI-Specific Patterns

### Endpoint Structure
```python
@app.post("/prompts", response_model=Prompt, status_code=status.HTTP_201_CREATED)
def create_prompt(
    prompt_data: PromptCreate,
    storage: Storage = Depends(get_storage)
) -> Prompt:
    """Create a new prompt.
    
    Args:
        prompt_data: The prompt data to create.
        storage: Storage dependency.
        
    Returns:
        The created prompt.
        
    Raises:
        HTTPException: 400 if collection_id is invalid.
    """
    # Validate dependencies
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Collection not found"
            )
    
    # Create and return
    prompt = Prompt(**prompt_data.model_dump())
    return storage.create_prompt(prompt)
```

### Response Models
Always define response models for documentation:
```python
class PromptResponse(BaseModel):
    """Response model for a single prompt."""
    id: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "abc123",
                "title": "Code Review Prompt",
                "content": "Review the following code...",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        }
```

### Validation
Use Pydantic validators for complex validation:
```python
from pydantic import BaseModel, Field, field_validator

class PromptCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=10)
    
    @field_validator('content')
    @classmethod
    def validate_content(cls, v: str) -> str:
        """Validate prompt content has meaningful text."""
        if not v.strip():
            raise ValueError("Content cannot be only whitespace")
        return v.strip()
```

---

## Code Quality Standards

### DRY Principle
Never repeat code. Extract common logic:
```python
# Bad
def get_prompt(prompt_id: str):
    prompt = storage.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt

def delete_prompt(prompt_id: str):
    prompt = storage.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    storage.delete_prompt(prompt_id)

# Good
def get_prompt_or_404(prompt_id: str) -> Prompt:
    """Get prompt or raise 404."""
    prompt = storage.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt

def get_prompt(prompt_id: str):
    return get_prompt_or_404(prompt_id)

def delete_prompt(prompt_id: str):
    get_prompt_or_404(prompt_id)  # Validate existence
    storage.delete_prompt(prompt_id)
```

### Single Responsibility Principle
Each function should do ONE thing:
```python
# Bad - does too much
def create_and_notify_prompt(data: PromptCreate):
    prompt = Prompt(**data.model_dump())
    storage.create_prompt(prompt)
    send_email_notification(prompt)
    log_audit_trail(prompt)
    return prompt

# Good - separated concerns
def create_prompt(data: PromptCreate) -> Prompt:
    """Create a prompt."""
    prompt = Prompt(**data.model_dump())
    return storage.create_prompt(prompt)

def notify_prompt_created(prompt: Prompt):
    """Send notification for new prompt."""
    send_email_notification(prompt)
    log_audit_trail(prompt)
```

### Function Length
- Keep functions under **20 lines** when possible
- If a function is long, break it into smaller helper functions
- Each function should have a single, clear purpose

---

## Documentation Standards

### Module Docstrings
Every module must have a docstring:
```python
"""Prompt management API endpoints.

This module contains all HTTP endpoints for CRUD operations on prompts,
including creation, retrieval, updating, and deletion.
"""
```

### Function Docstrings (Google Style)
```python
def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
    """Search through prompts by title and description.
    
    Performs case-insensitive search on both the title and description
    fields of prompts. Returns all prompts that match the query string.
    
    Args:
        prompts: List of Prompt objects to search through.
        query: Search string to match against titles and descriptions.
        
    Returns:
        List of Prompt objects that match the search query. Returns
        empty list if no matches found.
        
    Example:
        >>> prompts = [
        ...     Prompt(title="Code Review", description="Review code"),
        ...     Prompt(title="Documentation", description="Write docs")
        ... ]
        >>> results = search_prompts(prompts, "review")
        >>> len(results)
        1
    """
    query_lower = query.lower()
    return [
        p for p in prompts
        if query_lower in p.title.lower() or
           (p.description and query_lower in p.description.lower())
    ]
```

### Class Docstrings
```python
class PromptService:
    """Service layer for prompt business logic.
    
    This class handles all business logic related to prompts, including
    validation, transformation, and orchestration of storage operations.
    
    Attributes:
        storage: Storage instance for data persistence.
        
    Example:
        >>> service = PromptService(storage)
        >>> prompt = service.create_prompt(prompt_data)
    """
    
    def __init__(self, storage: Storage):
        """Initialize the prompt service.
        
        Args:
            storage: Storage instance for data operations.
        """
        self.storage = storage
```

---

## Performance & Best Practices

### Async/Await
Use async for I/O-bound operations:
```python
@app.get("/prompts/{prompt_id}")
async def get_prompt(prompt_id: str) -> Prompt:
    """Get prompt asynchronously."""
    prompt = await storage.get_prompt_async(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt
```

### Database Queries
- Use indexing for frequently queried fields
- Avoid N+1 query problems
- Use bulk operations when possible

### Caching
For expensive operations, consider caching:
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_collection_prompt_count(collection_id: str) -> int:
    """Get prompt count for a collection (cached)."""
    return len(storage.get_prompts_by_collection(collection_id))
```

---

## Security Standards

### Input Validation
- Always validate user input through Pydantic models
- Sanitize strings to prevent injection attacks
- Use parameterized queries (when using SQL)

### Authentication
```python
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.get("/prompts")
async def get_prompts(
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    """Protected endpoint requiring authentication."""
    pass
```

---

## Git Commit Standards

### Commit Message Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples
```
feat(prompts): add PATCH endpoint for partial updates

Implement PATCH /prompts/{id} endpoint that allows updating
only specified fields without requiring all fields like PUT.

Closes #42

---

fix(collections): handle orphaned prompts on deletion

When deleting a collection, now properly deletes associated
prompts to prevent orphaned records.

Fixes #38

---

test(api): add edge case tests for prompt creation

Add tests for:
- Empty content
- Special characters in title
- Missing required fields
```

---

## When to Refactor

Refactor code when you see:
- Functions longer than 20 lines
- Repeated code patterns (DRY violation)
- Unclear variable/function names
- Missing type hints or docstrings
- Complex conditionals (more than 3 levels deep)
- Large classes (more than 300 lines)

---

## AI-Specific Guidelines

When generating code:
1. **Always include type hints**
2. **Always include Google-style docstrings**
3. **Follow the file naming conventions above**
4. **Use the project's existing patterns** (check similar files first)
5. **Include tests** when adding new features
6. **Handle errors** according to the error handling standards
7. **Keep functions small and focused**
8. **Add examples** in docstrings for complex functions

---

## Quick Reference Checklist

Before committing code, verify:
- [ ] All functions have type hints
- [ ] All functions have Google-style docstrings
- [ ] All tests pass (`pytest tests/ -v`)
- [ ] Code coverage is maintained (>80%)
- [ ] No PEP 8 violations (`ruff check .`)
- [ ] Error handling follows standards
- [ ] No repeated code (DRY principle)
- [ ] Functions are under 20 lines when possible
- [ ] Commit message follows format