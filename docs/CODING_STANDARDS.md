# PromptLab Coding Standards

## Table of Contents

1. [Overview](#overview)
2. [Python Code Standards](#python-code-standards)
3. [API Design Standards](#api-design-standards)
4. [Documentation Standards](#documentation-standards)
5. [Testing Standards](#testing-standards)
6. [Git Workflow](#git-workflow)
7. [Code Review Guidelines](#code-review-guidelines)
8. [AI Coding Assistant Configuration](#ai-coding-assistant-configuration)

---

## Overview

This document defines the coding standards for the PromptLab project. All team members and contributors must follow these guidelines to maintain code quality, consistency, and maintainability.

### Goals

- **Consistency:** Code looks like it was written by one person
- **Readability:** Easy to understand for all team members
- **Maintainability:** Easy to modify and extend
- **Quality:** Minimal bugs, high test coverage

### Enforcement

- Automated linting and formatting tools
- Code review before merging
- CI/CD pipeline checks
- Regular code quality audits

---

## Python Code Standards

### Style Guide

We follow **PEP 8** (Python Enhancement Proposal 8) with minor modifications.

#### Line Length
- **Maximum:** 100 characters (not 79)
- **Reason:** Modern screens are wider, 100 is more practical

#### Indentation
- **4 spaces** (no tabs)
- Configure your editor to convert tabs to spaces

#### Naming Conventions

```python
# Classes: PascalCase
class PromptManager:
    pass

# Functions and methods: snake_case
def create_prompt():
    pass

# Constants: UPPER_SNAKE_CASE
MAX_PROMPT_LENGTH = 10000

# Private methods/attributes: leading underscore
def _internal_helper():
    pass

# Variables: snake_case
user_prompt = "Hello"
prompt_count = 10
```

#### Imports

```python
# Standard library first
import os
import sys
from datetime import datetime

# Third-party libraries second
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Local imports last
from app.models import Prompt, Collection
from app.storage import storage
from app.utils import sort_prompts_by_date
```

**Rules:**
- Group imports: standard lib, third-party, local
- Alphabetical order within each group
- Absolute imports preferred over relative
- One import per line (except `from x import a, b`)

### Type Hints

**Always use type hints** for function parameters and return values.

```python
# Good
def get_prompt(prompt_id: str) -> Optional[Prompt]:
    return storage.get_prompt(prompt_id)

# Bad
def get_prompt(prompt_id):
    return storage.get_prompt(prompt_id)
```

**Type hint examples:**

```python
from typing import List, Dict, Optional, Union, Any

# Basic types
name: str = "John"
age: int = 25
score: float = 95.5
is_active: bool = True

# Optional (can be None)
description: Optional[str] = None
collection_id: Optional[str] = None

# Collections
prompts: List[Prompt] = []
config: Dict[str, Any] = {}

# Multiple types
result: Union[Prompt, str] = get_data()

# Function signatures
def create_prompt(data: PromptCreate) -> Prompt:
    pass

def list_prompts(limit: int = 10) -> List[Prompt]:
    pass
```

### Docstrings

**All** public functions, classes, and modules must have docstrings.

#### Format: Google Style

```python
def function_name(param1: str, param2: int, param3: Optional[bool] = None) -> Dict[str, Any]:
    """Brief one-line description.
    
    More detailed description if needed. Explain what the function does,
    any important behavior, side effects, etc.
    
    Args:
        param1: Description of param1.
        param2: Description of param2.
        param3: Optional description of param3. Defaults to None.
        
    Returns:
        Dict[str, Any]: Description of the return value.
        
    Raises:
        ValueError: When param2 is negative.
        HTTPException: When resource is not found.
        
    Example:
        >>> result = function_name("test", 5)
        >>> print(result)
        {'status': 'success'}
    """
    pass
```

#### Module Docstrings

```python
"""Module for managing AI prompts.

This module provides functionality for creating, updating, and deleting
AI prompt templates. It includes both CRUD operations and search/filter
capabilities.

The module is organized into:
- CRUD endpoints for prompts
- Search and filter utilities
- Validation helpers
"""
```

#### Class Docstrings

```python
class PromptManager:
    """Manage prompt CRUD operations and business logic.
    
    This class handles all prompt-related operations including creation,
    retrieval, updates, and deletion. It acts as an intermediary between
    the API layer and the storage layer.
    
    Attributes:
        storage: The storage instance for data persistence.
        validator: The validation instance for data validation.
        
    Example:
        >>> manager = PromptManager()
        >>> prompt = manager.create_prompt(data)
    """
    pass
```

### Error Handling

#### Use Specific Exceptions

```python
# Good
from fastapi import HTTPException

if not prompt:
    raise HTTPException(status_code=404, detail="Prompt not found")

if not collection:
    raise HTTPException(status_code=400, detail="Collection not found")

# Bad
if not prompt:
    raise Exception("Error!")  # Too generic
```

#### Don't Silently Catch Exceptions

```python
# Good
try:
    result = risky_operation()
except ValueError as e:
    logger.error(f"Invalid value: {e}")
    raise HTTPException(status_code=400, detail=str(e))

# Bad
try:
    result = risky_operation()
except:
    pass  # Silent failure is dangerous
```

### Code Organization

#### Function Length
- **Target:** 10-20 lines
- **Maximum:** 50 lines
- **If longer:** Break into smaller functions

#### File Length
- **Target:** 200-300 lines
- **Maximum:** 500 lines
- **If longer:** Split into multiple modules

#### Single Responsibility
- Each function/class should do ONE thing
- If you use "and" in the function name, it's doing too much

```python
# Good
def validate_prompt_data(data: PromptCreate) -> bool:
    """Validate prompt data."""
    pass

def save_prompt_to_storage(prompt: Prompt) -> Prompt:
    """Save prompt to storage."""
    pass

# Bad
def validate_and_save_prompt(data: PromptCreate) -> Prompt:
    """Validate AND save."""  # Doing two things!
    pass
```

### Code Quality Rules

#### DRY (Don't Repeat Yourself)

```python
# Bad
if prompt_data.title:
    prompt.title = prompt_data.title
if prompt_data.content:
    prompt.content = prompt_data.content
if prompt_data.description:
    prompt.description = prompt_data.description

# Good
fields = ['title', 'content', 'description']
for field in fields:
    if getattr(prompt_data, field, None):
        setattr(prompt, field, getattr(prompt_data, field))
```

#### YAGNI (You Aren't Gonna Need It)

Don't implement features "just in case" - wait until they're actually needed.

#### KISS (Keep It Simple, Stupid)

```python
# Bad (over-engineered)
class PromptFactoryBuilderStrategy:
    def create_abstract_prompt_with_builder_pattern():
        pass

# Good (simple)
def create_prompt(data: PromptCreate) -> Prompt:
    return Prompt(**data.model_dump())
```

---

## API Design Standards

### RESTful Principles

#### Resource-Based URLs

```python
# Good
GET    /prompts           # List prompts
GET    /prompts/{id}      # Get specific prompt
POST   /prompts           # Create prompt
PUT    /prompts/{id}      # Full update
PATCH  /prompts/{id}      # Partial update
DELETE /prompts/{id}      # Delete prompt

# Bad
POST   /createPrompt      # Not RESTful
GET    /getPromptById?id=123
POST   /updatePrompt
```

#### HTTP Verbs

- **GET:** Retrieve resource(s), no side effects
- **POST:** Create new resource
- **PUT:** Full replacement of resource
- **PATCH:** Partial update of resource
- **DELETE:** Remove resource

#### Status Codes

```python
# Success
200 OK              # Successful GET, PUT, PATCH
201 Created         # Successful POST
204 No Content      # Successful DELETE

# Client Errors
400 Bad Request     # Invalid data (e.g., collection doesn't exist)
404 Not Found       # Resource doesn't exist
422 Unprocessable   # Validation error

# Server Errors
500 Internal Error  # Server error (should be rare)
```

#### Response Format

**Always return JSON** with consistent structure:

```python
# Success with data
{
  "id": "uuid",
  "title": "...",
  ...
}

# Success with list
{
  "prompts": [...],
  "total": 10
}

# Error
{
  "detail": "Error message"
}

# Validation error
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### Endpoint Design

#### Naming

- Use **plural nouns** for collections: `/prompts`, `/collections`
- Use **IDs in path** for specific resources: `/prompts/{id}`
- Use **query params** for filters: `/prompts?search=email`

#### Query Parameters

```python
# Filtering
GET /prompts?collection_id=abc123

# Searching
GET /prompts?search=email

# Pagination (future)
GET /prompts?limit=20&offset=40

# Sorting (future)
GET /prompts?sort_by=created_at&order=desc

# Combining
GET /prompts?collection_id=abc&search=email&limit=10
```

---

## Documentation Standards

### Code Comments

#### When to Comment

**DO comment:**
- Complex algorithms
- Business logic that isn't obvious
- Workarounds or hacks
- TODOs and FIXMEs

**DON'T comment:**
- Obvious code
- Instead of good naming

```python
# Bad (obvious)
# Increment counter by 1
counter += 1

# Good (explains WHY)
# Use linear search here because binary search would require
# maintaining sorted order, which is expensive for our use case
result = linear_search(data, target)

# Good (TODO)
# TODO: Replace with database query after migration
prompts = storage.get_all_prompts()
```

#### Comment Style

```python
# Single-line comment

"""
Multi-line comment or docstring.
Used for longer explanations.
"""
```

### README Files

Every directory should have a README explaining its purpose:

```
backend/
  README.md           # Backend overview
  app/
    README.md         # App structure explanation
  tests/
    README.md         # Testing guide
```

### API Documentation

- Use FastAPI's auto-documentation (Swagger/OpenAPI)
- Add descriptions to all endpoints
- Include examples in docstrings
- Maintain separate API reference document

---

## Testing Standards

### Test Coverage

- **Minimum:** 70% code coverage
- **Target:** 80% code coverage
- **Focus:** All API endpoints, business logic, edge cases

### Test Organization

```
tests/
  __init__.py
  conftest.py              # Fixtures
  test_api.py              # API endpoint tests
  test_models.py           # Model validation tests
  test_utils.py            # Utility function tests
  test_storage.py          # Storage layer tests
```

### Test Naming

```python
# Pattern: test_<what>_<condition>_<expected>

def test_create_prompt_valid_data_returns_201():
    pass

def test_get_prompt_nonexistent_id_returns_404():
    pass

def test_delete_collection_with_prompts_orphans_prompts():
    pass
```

### Test Structure (AAA Pattern)

```python
def test_create_prompt():
    # Arrange - Set up test data
    prompt_data = {
        "title": "Test Prompt",
        "content": "Hello {{name}}"
    }
    
    # Act - Perform the action
    response = client.post("/prompts", json=prompt_data)
    
    # Assert - Verify the results
    assert response.status_code == 201
    assert response.json()["title"] == "Test Prompt"
    assert "id" in response.json()
```

### What to Test

```python
# ✅ Test happy path
def test_create_prompt_success():
    pass

# ✅ Test error cases
def test_create_prompt_invalid_collection():
    pass

# ✅ Test edge cases
def test_create_prompt_max_length_title():
    pass

# ✅ Test validation
def test_create_prompt_missing_required_field():
    pass

# ✅ Test business logic
def test_delete_collection_orphans_prompts():
    pass
```

### Fixtures

Use fixtures for common test data:

```python
# conftest.py
import pytest

@pytest.fixture
def sample_prompt():
    """Create a sample prompt for testing."""
    return {
        "id": "test-uuid",
        "title": "Test Prompt",
        "content": "Hello {{name}}",
        "created_at": "2026-02-22T10:00:00Z",
        "updated_at": "2026-02-22T10:00:00Z"
    }

# Usage in tests
def test_something(sample_prompt):
    assert sample_prompt["title"] == "Test Prompt"
```

---

## Git Workflow

### Branch Naming

```bash
# Features
feature/prompt-tagging
feature/user-authentication

# Bug fixes
fix/update-timestamp-bug
fix/collection-deletion-edge-case

# Documentation
docs/api-reference
docs/architecture-diagrams

# Refactoring
refactor/storage-layer
refactor/error-handling
```

### Commit Messages

#### Format

```
<type>: <subject>

<optional body>

<optional footer>
```

#### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `test`: Adding/updating tests
- `refactor`: Code restructuring (no behavior change)
- `style`: Code formatting (no logic change)
- `chore`: Maintenance (dependencies, build, etc.)

#### Examples

```bash
# Good
feat: Add PATCH endpoint for partial prompt updates

Implemented PATCH /prompts/{id} endpoint that allows updating
individual fields without providing all data. The updated_at
timestamp is properly refreshed on updates.

Fixes #42

# Good
fix: Return 404 instead of 500 for missing prompts

Changed get_prompt endpoint to check if prompt exists before
accessing it. Now properly returns HTTPException with 404 status.

# Bad
Update stuff        # Too vague
Fixed bug           # What bug?
WIP                 # Don't commit work in progress to main
```

### Pull Request Guidelines

#### PR Title

Follow commit message format:

```
feat: Add tagging system for prompts
fix: Correct timestamp update bug
docs: Add architecture documentation
```

#### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Changes Made
- Added PATCH endpoint
- Updated timestamp logic
- Added tests

## Testing
- [ ] Unit tests added/updated
- [ ] All tests passing
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guide
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes (or documented)
```

---

## Code Review Guidelines

### For Authors

**Before requesting review:**
- [ ] All tests pass locally
- [ ] Code is self-reviewed
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] PR description is complete

### For Reviewers

**Focus on:**
- Correctness: Does it work?
- Design: Is it well-structured?
- Readability: Is it clear?
- Tests: Are edge cases covered?
- Documentation: Are changes documented?

**Review checklist:**
- [ ] Code follows standards
- [ ] Logic is correct
- [ ] Error handling is proper
- [ ] Tests are comprehensive
- [ ] Documentation is updated
- [ ] No security issues
- [ ] Performance is acceptable

**Providing feedback:**

```markdown
# Good feedback
❌ This function is doing too much. Consider splitting the validation
   logic into a separate `validate_prompt_data()` function.

✅ Good use of type hints here!

💡 Suggestion: We could simplify this with a list comprehension:
   `return [p for p in prompts if p.collection_id == collection_id]`

# Bad feedback
❌ This is wrong        # Too vague
❌ Bad code            # Not constructive
❌ Rewrite this        # No explanation
```

---

## AI Coding Assistant Configuration

### GitHub Copilot Settings

**.copilot.yaml** (project root):

```yaml
# GitHub Copilot configuration for PromptLab

# Suggested code style
style:
  language: python
  version: "3.10"
  max_line_length: 100
  indent: 4 spaces
  
# Project context
context:
  - "This is a FastAPI project"
  - "Follow PEP 8 with 100 char line limit"
  - "Use type hints for all functions"
  - "Write Google-style docstrings"
  - "Prefer explicit over implicit"

# Coding preferences
preferences:
  - "Use Pydantic models for data validation"
  - "Use HTTPException for API errors"
  - "Write comprehensive docstrings"
  - "Include type hints in function signatures"
  - "Use descriptive variable names"
  - "Keep functions under 50 lines"
  
# Testing preferences
testing:
  framework: pytest
  coverage_minimum: 80
  naming_pattern: "test_<what>_<condition>_<expected>"
```

### AI Assistant Prompts

#### Code Generation

```
Generate a FastAPI endpoint that:
- Follows RESTful conventions
- Uses Pydantic models for validation
- Includes comprehensive docstrings
- Has proper error handling
- Returns appropriate status codes
```

#### Test Generation

```
Generate pytest tests for this function that:
- Cover the happy path
- Test error cases
- Test edge cases
- Use AAA pattern (Arrange, Act, Assert)
- Include descriptive test names
```

#### Documentation

```
Write a docstring for this function following Google style:
- Brief one-line description
- Detailed explanation if needed
- Args with types and descriptions
- Returns section
- Raises section if applicable
- Example usage
```

### Custom AI Instructions

Create `.ai-instructions.md` in project root:

```markdown
# AI Coding Assistant Instructions for PromptLab

## Project Overview
- FastAPI REST API for managing AI prompts
- Python 3.10+
- In-memory storage (will migrate to PostgreSQL)

## Code Style
- Follow PEP 8 with 100-char line limit
- Use type hints everywhere
- Write Google-style docstrings
- Name classes PascalCase, functions snake_case

## Patterns to Follow
- RESTful API design
- Pydantic for validation
- Dependency injection (FastAPI)
- Repository pattern for storage

## Testing
- Use pytest
- AAA pattern (Arrange, Act, Assert)
- Descriptive test names
- Aim for 80%+ coverage

## Don't Do
- Don't use `print()` for logging (use `logger`)
- Don't catch exceptions silently
- Don't hardcode values
- Don't create functions over 50 lines
```

---

## Tools and Automation

### Linting

**Install:**
```bash
pip install flake8 black mypy
```

**Run:**
```bash
# Check code style
flake8 app/ tests/

# Format code
black app/ tests/

# Type checking
mypy app/
```

### Configuration Files

**setup.cfg** (flake8 config):
```ini
[flake8]
max-line-length = 100
exclude = .git,__pycache__,venv
ignore = E203, W503
```

**pyproject.toml** (black config):
```toml
[tool.black]
line-length = 100
target-version = ['py310']
```

### Pre-commit Hooks

**.pre-commit-config.yaml**:
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black
  
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
```

---

## Summary

### Key Principles

1. **Consistency** - Follow standards always
2. **Clarity** - Write code others can understand
3. **Quality** - Test thoroughly, handle errors
4. **Documentation** - Document code, APIs, decisions
5. **Simplicity** - Keep it simple and maintainable

### Quick Checklist

Before committing code:

- [ ] Code follows PEP 8
- [ ] Type hints added
- [ ] Docstrings written
- [ ] Tests added/updated
- [ ] Tests passing
- [ ] No debug code
- [ ] Documentation updated
- [ ] Meaningful commit message

---

## Questions?

If you have questions about these standards:

1. Check this document first
2. Ask in team chat
3. Discuss in code review
4. Propose changes via PR to this document
