# PromptLab

**Your AI Prompt Engineering Platform**

---

## Project Overview

PromptLab is an internal tool designed for AI engineers to store, organize, and manage their prompts effectively. It's akin to a "Postman for Prompts" — providing a professional environment for managing prompt templates, enabling tagging, searching, version tracking, and prompt testing.

### Features
- 📝 **Store Prompts**: Save templates with variables (e.g., `{{input}}`, `{{context}}`).
- 📁 **Collections**: Organize prompts into searchable collections.
- 🏷️ **Tagging & Search**: Easily find and categorize prompts.
- 📜 **Version Tracking**: Keep history of prompt changes.
- 🧪 **Testing**: Test prompts against various inputs.

---

## Setup Instructions

### Prerequisites
- **Python**: 3.10+
- **Node.js**: 18+ (needed for frontend development)
- **Git**: Version Control System

### Installation

1. **Clone the Repository**
   ```bash
   git clone <your-repo-url>
   cd promptlab
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   python main.py
   ```
   The API will be running at: [http://localhost:8000](http://localhost:8000)

3. **API Documentation**
   Access Swagger UI for API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

4. **Running Tests**
   ```bash
   cd backend
   pytest tests/ -v
   ```

---

## API Endpoints

| Method | Endpoint            | Description       | Status   |
|--------|---------------------|-------------------|----------|
| GET    | `/health`           | Health check      | ✅ Works |
| GET    | `/prompts`          | List all prompts  | ✅ Works |
| GET    | `/prompts/{id}`     | Get single prompt | ✅ Works |
| POST   | `/prompts`          | Create prompt     | ✅ Works |
| PUT    | `/prompts/{id}`     | Update prompt     | ✅ Works |
| DELETE | `/prompts/{id}`     | Delete prompt     | ✅ Works |
| GET    | `/collections`      | List collections  | ✅ Works |
| GET    | `/collections/{id}` | Get collection    | ✅ Works |
| POST   | `/collections`      | Create collection | ✅ Works |
| DELETE | `/collections/{id}` | Delete collection | ✅ Works |

---

## Data Models

### Prompt Models

- `PromptBase`: Shared attributes for prompts such as title, content, description, and collection ID.
- `PromptCreate`: Used when creating a new prompt, extending `PromptBase`.
- `PromptUpdate`: Inherits from `PromptBase` for updating prompts.
- `PromptPatch`: Handles partial updates to a prompt.
- `Prompt`: Represents a stored prompt with metadata including ID and timestamps.

### Collection Models

- `CollectionBase`: Contains common attributes for collections like name and description.
- `CollectionCreate`: Used for creating new collections.
- `Collection`: A fully defined collection with metadata.

### Other Models

- `PromptList`: Represents a list of prompts.
- `CollectionList`: Represents a list of collections.
- `HealthResponse`: Provides API health status and version.

---

## Usage Examples

**Adding a New Prompt:**

To add a new prompt, make a POST request to `/prompts` with a JSON payload containing the title and content.

**Fetching All Prompts:**

To retrieve all stored prompts, use a GET request to `/prompts`.

**Managing Collections:**

Collections can be created, listed, and fetched using respective endpoints for organization purposes.

---


## Project Structure

promptlab/
├── README.md                      # Documentation for project overview
├── PROJECT_BRIEF.md               # Assignment details for the project
├── GRADING_RUBRIC.md              # Grading criteria for the project
│
├── backend/                       # Backend directory using FastAPI
│   ├── app/                       # Application code
│   │   ├── __init__.py            # Package initialization
│   │   ├── api.py                 # FastAPI routes (contains some bugs)
│   │   ├── models.py              # Pydantic data validation models
│   │   ├── storage.py             # In-memory data storage
│   │   └── utils.py               # Utility/helper functions
│   ├── tests/                     # Testing directory
│   │   ├── __init__.py            # Package initialization for tests
│   │   ├── test_api.py            # Basic FastAPI route tests
│   │   └── conftest.py            # Test fixtures setup
│   ├── main.py                    # Application entry point
│   └── requirements.txt           # Python dependencies
│
├── frontend/                      # Placeholder for future frontend development
├── specs/                         # Specifications for features
│   ├── prompt-versions.md         # Feature specification for Prompt Versions
│   └── tagging-system.md          # Feature specification for Tagging System
├── docs/                          # Documentation directory
│   ├── .gitkeep                   # Placeholder for git
│   └── API_REFERENCE.md           # API reference documentation
└── .github/                       # To be developed in Week 3 for CI/CD setup

---
## Test Cases Implementation

We employ `pytest` along with `pytest-cov` for testing our application. Our test suite ensures robust validation of API endpoints and logic.

### Running Tests with Coverage
To run the tests and check code coverage, execute the following:

```bash
pytest --cov=backend --cov-report=term-missing
```

### Coverage Threshold
The test suite is configured to fail if code coverage falls below 80%, ensuring consistent quality.

---

## Continuous Integration via GitHub Actions

We have a CI/CD pipeline set up using GitHub Actions to automate testing and deployment tasks:

- **Trigger**: The workflow triggers on pushes and pull requests to the `main` branch.
- **Steps**:
  - Set up the Python environment.
  - Install dependencies.
  - Run tests with coverage check.

This integration ensures continuous quality and integrates seamlessly with GitHub for streamlined collaboration.

---

## Docker Implementation

The project is containerized to facilitate easy setup and deployment using Docker:

### Docker Configuration

- **Dockerfile**: Builds a lightweight image using a multi-stage build to optimize dependencies.
- **Docker Compose**: Defined to set up and run the application easily.

#### Running with Docker

1. **Build the Docker Image**:
   ```bash
   docker-compose build
   ```

2. **Run the Docker Container**:
   ```bash
   docker-compose up
   ```

Access the application on [http://localhost:8000]

---

## Development Workflow

- **Week 1**: Fix backend issues, understand codebase, and feature implementation.
- **Week 2**: Write documentation, create feature specs, and set up coding standards.
- **Week 3**: Implement a test suite, use Test-Driven Development (TDD), and set up CI/CD via Docker and GitHub Actions.
- **Week 4**: Develop the frontend using React and Vite, connecting it to the backend.

---

## Tech Stack

- **Backend**: Python 3.10+, FastAPI, Pydantic
- **Frontend**: React, Vite (development planned)
- **Testing**: Pytest
- **DevOps**: Docker, GitHub Actions

---

## Need Help?

1. Utilize AI coding tools as this is an AI-assisted learning project.
2. Refer to `PROJECT_BRIEF.md` for comprehensive instructions.
3. Consult `GRADING_RUBRIC.md` for evaluation criteria.
4. Engage in the course forum for any questions.

---

Good luck, and welcome to the team! 🚀
