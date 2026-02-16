# Continue Rules – PromptLab Project

These rules define how AI coding assistants MUST write, modify, and review code
for this repository. Follow them strictly.

---

## 1. Project Overview

Project Name: PromptLab  
Repository: 10x-engineer-project-repo  
Backend: Python + FastAPI-style API  
Frontend: Reserved (currently empty)  
Docs: Markdown-based documentation under /docs

Primary goals:
- Clean, readable Python code
- Minimal but correct API implementation
- Predictable AI-generated code output
- No unnecessary architectural changes

---

## 2. Repository Structure (STRICT)

AI MUST respect this structure and MUST NOT restructure the project.


## 3. Coding Standards

### Python Version & Style
- Use **Python 3.11+**
- Follow **PEP 8**
- Use 4-space indentation
- Prefer explicit, readable code over shortcuts

### Type Hints
- All functions MUST include type annotations
- Prefer standard typing (`list`, `dict`, `Optional`) and dataclasses or Pydantic-style models when applicable

---

## 4. File Responsibilities (IMPORTANT)

- `main.py`
  - App initialization
  - App startup configuration
  - No business logic

- `app/api.py`
  - API route definitions ONLY
  - No storage or computation logic

- `app/models.py`
  - Request/response models
  - Shared data structures

- `app/storage.py`
  - Data persistence logic
  - No API logic

- `app/utils.py`
  - Stateless helper functions
  - Reusable logic only

AI MUST place new code in the correct file.

---

## 5. API Design Rules

- Follow REST-style conventions
- Use JSON-only APIs
- Use appropriate HTTP methods:
  - GET → read
  - POST → create
  - PUT/PATCH → update
  - DELETE → remove

### Responses
- Always return JSON
- Success responses MUST be consistent
- Do not return raw Python exceptions

---

## 6. Error Handling Rules

- Validate all input
- Use explicit error messages
- Error responses MUST follow this format:

```json
{
  "error": {
    "code": "string_identifier",
    "message": "Human readable message"
  }
}
