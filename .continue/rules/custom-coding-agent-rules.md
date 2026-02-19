---
description: Coding agent Assitant
---
# Continue Rules

These rules define mandatory constraints for AI coding assistants when writing,
modifying, or reviewing code.

---

## 1. Project Overview

Project Name: PromptLab 
Backend: Python-based FastAPI-style service 
Docs: Markdown-based documentation under `/docs`

Primary goals:
- Clean and maintainable code
- Correct API implementation
- Predictable and deterministic AI-generated output
- No unnecessary refactors or architectural changes
- Easy handoff between AI-generated and human-written code

---

## 2. Structure

The repository structure is fixed.

AI MUST:
- Respect the existing layout
- Add new code only to appropriate existing files

AI MUST NOT:
- Rename or move files
- Introduce new directories or layers
- Restructure the project for stylistic reasons

---

## 3. Coding Standards

### Python Version & Style
- Use **Python 3.11+**
- Follow **PEP 8**

### Type Hints
- All functions MUST include parameter and return type annotations
- Avoid `Any` unless absolutely required
- Prefer built-in typing (`list`, `dict`, `Optional`)
- Use dataclasses or Pydantic-style models for structured data

---

## 4. File Responsibilities (IMPORTANT)

Each file has a single, enforced responsibility.

- `main.py`
  - Application initialization
  - Framework and startup configuration
  - Lifecycle hooks
  - ❌ No business logic
  - ❌ No data access

- `app/api.py`
  - HTTP route definitions only
  - Request validation and response formatting
  - HTTP status codes and error mapping
  - ❌ No computation logic
  - ❌ No persistence logic

- `app/models.py`
  - Request and response models
  - Shared domain data structures
  - Type-safe schemas
  - ❌ No API logic
  - ❌ No storage logic

- `app/storage.py`
  - Data persistence operations
  - CRUD behavior
  - Storage abstraction layer
  - ❌ No HTTP concepts
  - ❌ No business rules

- `app/utils.py`
  - Stateless helper functions
  - Reusable, pure logic
  - ❌ No I/O
  - ❌ No storage access
  - ❌ No API awareness

---

## 5. API Design and Response Rules

### HTTP Methods
- Follow **RESTful conventions**.
- Use JSON for all requests and responses.
- Select methods strictly according to intent:
  - **GET** → Retrieve data
  - **POST** → Create new resources
  - **PUT / PATCH** → Update existing resources
  - **DELETE** → Remove resources

### Response Guidelines
- Always return **JSON** objects.
- Success responses must be **consistent** in structure.
- Never return raw Python objects or internal exceptions.
- Include only relevant data; avoid exposing internal implementation details.

**Example – Success Response**
```json
{
  "id": "123",
  "title": "Sample Prompt",
  "content": "This is a sample."
}
```
----

## 6. Naming Conventions

Consistent naming ensures readability and maintainability.

- **Files:** `snake_case.py`  
  *Example:* `storage_utils.py`
- **Tests:** `test_<module>.py`  
  *Example:* `test_storage.py`
- **Classes:** `PascalCase`  
  *Example:* `PromptManager`
- **Functions / Methods:** `snake_case`  
  *Example:* `get_prompt_by_id`
- **Constants:** `UPPER_SNAKE_CASE`  
  *Example:* `MAX_PROMPT_LENGTH`