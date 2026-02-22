# Developer Guide

## Welcome, Developer! 👋

This guide will help you set up, develop, and contribute to PromptLab. Whether you're new to the project or an experienced contributor, this guide has everything you need.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Getting Started](#getting-started)
3. [Project Structure](#project-structure)
4. [Development Workflow](#development-workflow)
5. [Testing](#testing)
6. [API Development](#api-development)
7. [Debugging](#debugging)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)
10. [Contributing](#contributing)

---

## Prerequisites

### Required Software

- **Python:** 3.10 or higher
- **pip:** Latest version
- **Git:** For version control

### Recommended Tools

- **VS Code:** With Python extension
- **Postman or Insomnia:** For API testing
- **pytest:** For running tests (installed via requirements.txt)

### Check Your Setup

```bash
# Check Python version
python --version  # Should be 3.10+

# Check pip
pip --version

# Check git
git --version
```

---

## Getting Started

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd promptlab
```

### 2. Set Up Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 5. Verify Installation

Open your browser and navigate to:
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

---

## Project Structure

```
promptlab/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Package initialization
│   │   ├── api.py               # FastAPI routes
│   │   ├── models.py            # Pydantic models
│   │   ├── storage.py           # Data storage
│   │   └── utils.py             # Helper functions
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py          # Test fixtures
│   │   └── test_api.py          # API tests
│   ├── main.py                  # Application entry point
│   └── requirements.txt         # Python dependencies
├── docs/                        # Documentation
│   ├── API_REFERENCE.md
│   ├── ARCHITECTURE.md
│   └── DEVELOPER_GUIDE.md
├── specs/                       # Feature specifications
├── frontend/                    # Frontend (Week 4)
├── README.md
├── PROJECT_BRIEF.md
└── GRADING_RUBRIC.md
```

---

## Development Workflow

### Daily Workflow

1. **Pull latest changes:**
   ```bash
   git pull origin main
   ```

2. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**

4. **Run tests:**
   ```bash
   pytest tests/ -v
   ```

5. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Add feature: description"
   ```

6. **Push to remote:**
   ```bash
   git push origin feature/your-feature-name
   ```

### Hot Reload

The development server (`python main.py`) runs with auto-reload enabled. Changes to Python files will automatically restart the server.

**Files watched:**
- `app/*.py`
- `main.py`

**Not watched:**
- Test files
- Documentation

---

## Testing

### Running Tests

**Run all tests:**
```bash
cd backend
pytest tests/ -v
```

**Run specific test file:**
```bash
pytest tests/test_api.py -v
```

**Run specific test:**
```bash
pytest tests/test_api.py::test_create_prompt -v
```

**Run with coverage:**
```bash
pytest tests/ -v --cov=app --cov-report=html
```

### Writing Tests

**Example test:**

```python
def test_create_prompt(client):
    """Test creating a new prompt."""
    response = client.post("/prompts", json={
        "title": "Test Prompt",
        "content": "Hello {{name}}"
    })
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Prompt"
    assert "id" in data
```

**Test structure:**
- Arrange: Set up test data
- Act: Call the function/endpoint
- Assert: Verify the results

### Test Fixtures

Common fixtures (defined in `conftest.py`):

- `client`: FastAPI test client
- `sample_prompt`: Pre-created prompt for testing
- `sample_collection`: Pre-created collection for testing

**Usage:**
```python
def test_get_prompt(client, sample_prompt):
    response = client.get(f"/prompts/{sample_prompt['id']}")
    assert response.status_code == 200
```

### Test Coverage Goals

- **Target:** 80%+ code coverage
- **Focus areas:**
  - All API endpoints
  - Error handling
  - Edge cases
  - Data validation

---

## API Development

### Adding a New Endpoint

**1. Define the route in `api.py`:**

```python
@app.get("/prompts/{prompt_id}/variables")
def get_prompt_variables(prompt_id: str):
    """Extract variables from a prompt."""
    prompt = storage.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    variables = extract_variables(prompt.content)
    return {"variables": variables}
```

**2. Add docstring:**

Include:
- Description of what the endpoint does
- Parameters
- Return value
- Possible errors
- Example usage

**3. Add tests:**

```python
def test_get_prompt_variables(client, sample_prompt):
    response = client.get(f"/prompts/{sample_prompt['id']}/variables")
    assert response.status_code == 200
    assert "variables" in response.json()
```

**4. Update API documentation:**

Add the new endpoint to `docs/API_REFERENCE.md`.

### Request Validation

FastAPI automatically validates requests using Pydantic models:

```python
class PromptCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
```

This ensures:
- Required fields are present
- Types are correct
- Constraints are met (length, format, etc.)

### Error Handling

**Use HTTP exceptions:**

```python
from fastapi import HTTPException

# 404 Not Found
raise HTTPException(status_code=404, detail="Prompt not found")

# 400 Bad Request
raise HTTPException(status_code=400, detail="Collection not found")

# 422 Validation Error (automatic via Pydantic)
```

---

## Debugging

### Using Print Statements

```python
@app.get("/prompts")
def list_prompts():
    prompts = storage.get_all_prompts()
    print(f"Found {len(prompts)} prompts")  # Debug print
    return PromptList(prompts=prompts, total=len(prompts))
```

### Using Python Debugger

**Add breakpoint:**

```python
import pdb

@app.get("/prompts/{prompt_id}")
def get_prompt(prompt_id: str):
    pdb.set_trace()  # Debugger will stop here
    prompt = storage.get_prompt(prompt_id)
    return prompt
```

**VS Code Debugger:**

Create `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "app.api:app",
                "--reload"
            ],
            "jinja": true,
            "justMyCode": true
        }
    ]
}
```

### Logging

**Add logging:**

```python
import logging

logger = logging.getLogger(__name__)

@app.get("/prompts")
def list_prompts():
    logger.info("Listing all prompts")
    prompts = storage.get_all_prompts()
    logger.debug(f"Found {len(prompts)} prompts")
    return PromptList(prompts=prompts, total=len(prompts))
```

### Interactive API Testing

**Using Swagger UI:**

1. Navigate to http://localhost:8000/docs
2. Click on an endpoint
3. Click "Try it out"
4. Fill in parameters
5. Click "Execute"
6. View response

**Using curl:**

```bash
# GET request
curl http://localhost:8000/prompts

# POST request
curl -X POST http://localhost:8000/prompts \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","content":"Hello"}'

# With pretty printing
curl http://localhost:8000/prompts | python -m json.tool
```

---

## Best Practices

### Code Style

- **Follow PEP 8:** Python style guide
- **Use type hints:** For function parameters and returns
- **Write docstrings:** For all functions and classes
- **Keep functions small:** Single responsibility principle
- **Use meaningful names:** Variables, functions, classes

### Docstring Format

```python
def function_name(param1: str, param2: int) -> bool:
    """Brief description of function.
    
    More detailed description if needed. Explain what the
    function does, any important behavior, etc.
    
    Args:
        param1: Description of param1.
        param2: Description of param2.
        
    Returns:
        bool: Description of return value.
        
    Raises:
        ValueError: When this error occurs.
        
    Example:
        >>> function_name("test", 5)
        True
    """
    pass
```

### Error Handling

```python
# Bad
def get_prompt(prompt_id: str):
    return storage._prompts[prompt_id]  # Crashes if not found

# Good
def get_prompt(prompt_id: str):
    prompt = storage.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt
```

### Data Validation

```python
# Bad
def create_prompt(data: dict):
    prompt = Prompt(**data)  # No validation

# Good
def create_prompt(data: PromptCreate):
    # Pydantic validates automatically
    prompt = Prompt(**data.model_dump())
    return storage.create_prompt(prompt)
```

---

## Troubleshooting

### Server won't start

**Error:** `Address already in use`

**Solution:** Another process is using port 8000
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>
```

### Import errors

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Tests failing

**Check:**
1. Are you in the `backend` directory?
2. Is the virtual environment activated?
3. Are dependencies installed?
4. Did you clear storage between tests? (automatic with fixtures)

### Changes not reflecting

**Issue:** Code changes not appearing

**Solution:**
- Server should auto-reload (check terminal for "Reloading" message)
- Manually restart: Ctrl+C, then `python main.py`
- Clear browser cache: Shift+F5

---

## Contributing

### Commit Message Format

```
<type>: <subject>

<body>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding/updating tests
- `refactor`: Code refactoring
- `style`: Code style changes (formatting)
- `chore`: Maintenance tasks

**Examples:**

```
feat: Add PATCH endpoint for partial prompt updates

Implemented PATCH /prompts/{id} to allow updating individual
fields without providing all data. Updates updated_at timestamp.
```

```
fix: Return 404 instead of 500 for missing prompts

Changed get_prompt endpoint to check for None and return
proper HTTPException with 404 status code.
```

### Code Review Checklist

Before submitting code for review:

- [ ] Code follows style guide
- [ ] All functions have docstrings
- [ ] Tests are added/updated
- [ ] All tests pass
- [ ] No debug print statements
- [ ] Error handling is proper
- [ ] Documentation is updated
- [ ] Commit messages are clear

---

## Quick Reference

### Common Commands

```bash
# Start server
python main.py

# Run tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ --cov=app

# Install new package
pip install <package>
pip freeze > requirements.txt

# Format code
black app/
```

### Useful URLs

- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health
- **OpenAPI Schema:** http://localhost:8000/openapi.json

### Getting Help

- **Documentation:** See `docs/` folder
- **API Reference:** `docs/API_REFERENCE.md`
- **Architecture:** `docs/ARCHITECTURE.md`
- **Project Brief:** `PROJECT_BRIEF.md`

---

## Next Steps

1. **Explore the API:** Try out endpoints in Swagger UI
2. **Read the code:** Start with `api.py`, then `models.py`
3. **Run the tests:** See how testing works
4. **Make a change:** Fix a bug or add a small feature
5. **Write a test:** For your change
6. **Read architecture docs:** Understand the big picture

Happy coding! 🚀
