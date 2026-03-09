# PromptLab

**Your AI prompt engineering workspace**

PromptLab is an API-first platform for AI engineers to craft, organize, and version prompt templates with the same rigor as traditional software artifacts. The current repository ships a FastAPI backend with CRUD endpoints for prompts and collections. Your mission is to stabilize the backend, document it thoroughly, and prepare for frontend, testing, and DevOps enhancements over the four-week assignment.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Getting Started](#getting-started)
3. [API Summary](#api-summary)
4. [Usage Examples](#usage-examples)
5. [Project Structure](#project-structure)
6. [Documentation & Specs](#documentation--specs)
7. [Need Help?](#need-help)

## Project Overview
PromptLab centralizes prompt templates in collections, supports metadata such as descriptions and timestamps, and enables curated retrieval via search or collection filters. The week-by-week plan emphasizes:

- Week 1: Stabilize backend bugs, add PATCH support, and refresh documentation.
- Week 2: Write Google-style docstrings, produce API references, and author feature specs.
- Week 3: Expand automated tests, implement a priority feature, and configure CI/CD plus Docker.
- Week 4: Deliver a React + Vite frontend that consumes the API.

## Getting Started
### Prerequisites
- Python 3.10 or later
- Node.js 18+ (for future frontend work)
- Git configured with your editor of choice

### Installation
```bash
git clone <your-repo-url>
cd promptlab/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Running the Backend
```bash
python main.py
```
The API listens on http://localhost:8000 and exposes interactive Swagger docs at http://localhost:8000/docs.

### Running Tests
```bash
cd backend
pytest tests/ -v
```

## API Summary
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Returns service health and version metadata |
| GET | `/prompts` | Lists prompts with optional `collection_id` and `search` filters |
| GET | `/prompts/{id}` | Retrieves a prompt by id |
| POST | `/prompts` | Creates a prompt with title, content, and optional description/collection linkage |
| PUT | `/prompts/{id}` | Replaces a prompt’s mutable fields and refreshes `updated_at` |
| PATCH | `/prompts/{id}` | Partially updates provided prompt fields and refreshes `updated_at` |
| DELETE | `/prompts/{id}` | Deletes a prompt and returns HTTP 204 |
| GET | `/collections` | Lists all collections |
| GET | `/collections/{id}` | Retrieves a collection by id |
| POST | `/collections` | Creates a new collection bucket |
| DELETE | `/collections/{id}` | Deletes a collection (prompts remain but lose association) |

Refer to [`docs/API_REFERENCE.md`](docs/API_REFERENCE.md) for full payload samples and error codes.

## Usage Examples
### Health Check
```bash
curl http://localhost:8000/health
```
Response:
```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

### Create a Prompt
```bash
curl -X POST http://localhost:8000/prompts \
  -H "Content-Type: application/json" \
  -d '{"title": "Review Code", "content": "Please review {{code}}"}'
```

### Partial Update via PATCH
```bash
curl -X PATCH http://localhost:8000/prompts/<prompt_id> \
  -H "Content-Type: application/json" \
  -d '{"description": "Add extra guidance"}'
```

### Filter Prompts by Collection
```bash
curl "http://localhost:8000/prompts?collection_id=<collection_id>"
```

## Project Structure
```
promptlab/
├── backend/        # FastAPI service with models, storage, utils, and tests
├── frontend/        # Week 4: React + Vite UI (pending)
├── docs/            # API reference and documentation artifacts
├── specs/           # Feature specifications for prompt versions and tagging
├── .github/         # CI/CD and AI agent instructions
├── README.md        # This overview
├── PROJECT_BRIEF.md # Week-by-week goals and tasks
└── GRADING_RUBRIC.md# Evaluation criteria
```

## Documentation & Specs
- `docs/API_REFERENCE.md`: Endpoint details with request/response samples and error codes
- `.github/copilot-instructions.md`: Coding standards, testing expectations, and patterns for AI-assisted editing
- `specs/prompt-versions.md` and `specs/tagging-system.md`: Feature briefs with goals, user stories, data model changes, API endpoints, and edge case guidance

## Need Help?
1. Review `PROJECT_BRIEF.md` and `GRADING_RUBRIC.md` for requirements and expectations.
2. Use the FastAPI auto-generated docs at `/docs` while iterating.
3. Consult `.github/copilot-instructions.md` before asking AI assistants to write code.
4. Ask clarifying questions early in the forum to avoid rework.

Happy hacking! 🚀
