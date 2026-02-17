# CONTINUE.md

## Project Overview
PromptLab is an internal tool for AI engineers designed to manage AI-prompt incidents efficiently. Utilizing FastAPI, it serves as a backend solution emulating a "Postman for Prompts" to streamline prompt management.

### Key Technologies
- **Backend**: FastAPI, Python 3.10
- **Testing**: Pytest
- **Frontend** (to be developed): React

### High-Level Architecture
PromptLab's architecture revolves around a FastAPI backend service handling prompt storage, retrieval, and management operations. The frontend, to be developed, will interface with this API to provide a user-friendly interaction layer.

---

## Getting Started

### Prerequisites
- Python 3.10+
- Git

### Installation Instructions
1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd promptlab
   ```
2. Set up the backend:
   ```bash
   cd backend
   pip install -r requirements.txt
   python main.py
   ```
3. The API is now running at http://localhost:8000.

### Usage Examples
- Access the API documentation at http://localhost:8000/docs.
- Run tests via:
  ```bash
  cd backend
  pytest tests/ -v
  ```

---

## Project Structure

### Main Directories
- **backend/**: Contains all FastAPI application code and tests.
- **frontend/**: Reserved for future frontend development.
- **docs/**: Documentation and API references.

### Key Files
- **backend/app/api.py**: FastAPI routes implementation.
- **backend/app/models.py**: Pydantic data models.
- **backend/main.py**: Application entry point.

---

## Development Workflow

### Coding Standards
- Follow PEP 8 for Python code.
- Document code with clear docstrings.

### Testing Approach
- Write tests using Pytest.
- Ensure tests cover all API endpoints and critical logic.

### Build & Deployment
- Use Docker for containerization (planned).
- Integrate CI/CD via GitHub Actions (planned).

### Contribution Guidelines
- Fork repository and create feature branches for changes.
- Submit pull requests for review.

---

## Key Concepts
- **Prompt**: A template containing variables like `{{input}}` and `{{context}}`.
- **Collection**: A grouping of prompts for organization.

---

## Common Tasks

### Adding a New Prompt
Use the POST `/prompts` endpoint with JSON payload.

### Fetching All Prompts
Use GET `/prompts` to retrieve and review all stored prompts.

### Troubleshooting
- Verify environment variables if the application fails to start.
- Check the console output for specific error messages.

---

## References
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)