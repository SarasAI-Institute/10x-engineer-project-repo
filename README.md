# PromptLab Incident Management API

FastAPI backend that helps incident response teams capture, index, and reuse proven remediation playbooks ("prompts") so on-call engineers can react consistently during high-pressure events.

---

## Project Overview & Purpose
PromptLab centralizes the organization’s incident knowledge base in one FastAPI service so teams can:

- Standardize remediation steps during outages instead of searching scattered docs.
- Curate collections by severity, product surface, or on-call rotation.
- Power automation (chatbots, paging assistants, ticket bots) with the same structured prompts.

The stack stays lightweight: FastAPI + Pydantic models, an in-memory storage layer, and pytest for regression coverage.

---

## Key Features
- **Incident Prompt Registry** – Create, read, update, patch, and delete structured prompt templates.
- **Collection Management** – Group prompts by incident category, business unit, or escalation tier.
- **Search & Filtering** – Query prompts by free-text search or limit results to a specific collection.
- **Timestamp Tracking** – Automatic `created_at`/`updated_at` fields for auditability.
- **Health Monitoring** – `/health` endpoint exposes service status and semantic version.
- **OpenAPI Docs** – Interactive Swagger UI (`/docs`) and ReDoc (`/redoc`).

---

## Prerequisites & Installation
### Prerequisites
- Python 3.10+ with pip
- Git
- (Optional) Node.js 18+ for future frontend work

### Installation
1. Clone the repository.
   ```bash
   git clone <your-repo-url>
   cd promptlab
   ```
2. Install backend dependencies from the project root.
   ```bash
   pip install -r backend/requirements.txt
   ```

---

## Quick Start Guide
1. **Start the API**
   ```bash
   cd backend
   uvicorn app.api:app --reload --host 0.0.0.0 --port 8000
   ```
   Swagger UI lives at http://localhost:8000/docs and ReDoc at /redoc.

2. **Add sample data (optional)** – Use the `POST /collections` and `POST /prompts` routes from Swagger UI or the curl snippets below.

3. **Run the tests**
   ```bash
   cd backend
   pytest tests/ -v --cov=app --cov-report=term-missing
   ```

---

## Running in GitHub Codespaces
1. **Launch a Codespace** – Open the repository in Codespaces and wait for the dev container to finish installing dependencies.
2. **Install/refresh Python deps** – From the integrated terminal at the repo root, run:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. **Start the API with Python** – Either of the following works; both bind to all interfaces on port 8000 so Codespaces can forward traffic.
   ```bash
   # Option A: run uvicorn explicitly
   cd backend
   uvicorn app.api:app --host 0.0.0.0 --port 8000 --reload

   # Option B: use the provided launcher script from the repo root
   python backend/main.py
   ```
   The terminal will log `Uvicorn running on http://0.0.0.0:8000` once the server is live.
4. **Expose the port publicly** – Open the *Ports* panel in the Codespaces sidebar, locate port `8000`, and change *Visibility* from **Private** to **Public** if you need to share the live preview link. Keeping it private limits access to your session only.
5. **Open the service** – Click the forwarded URL (e.g., `https://8000-<hash>.app.github.dev`) to view Swagger UI. The same URL works for teammates when the port is public.
6. **Stop the server** – Use the terminal where Uvicorn is running and press `Ctrl+C` or terminate the shell tab to stop the process before running tests or restarting.

---

## Data Models
### Prompt
| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` (UUID) | Server-generated identifier for the prompt. |
| `title` | `str` | Human-readable incident prompt title (1–200 chars). |
| `content` | `str` | Full text of the playbook or prompt body (supports template variables like `{{service}}`). |
| `description` | `Optional[str]` | Additional context or usage notes. |
| `collection_id` | `Optional[str]` | References the collection this prompt belongs to. |
| `created_at` | `datetime` | Timestamp of initial creation (UTC). |
| `updated_at` | `datetime` | Timestamp of last modification (UTC). |

### Collection
| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` (UUID) | Server-generated identifier for a collection. |
| `name` | `str` | Collection name (e.g., "SEV-1 Runbooks"). |
| `description` | `Optional[str]` | Details that clarify how the collection should be used. |
| `created_at` | `datetime` | Timestamp when the collection was created. |

---

## Usage Examples
> Replace placeholder IDs with the UUIDs returned by your API.

### 1. Create a collection
```bash
curl -X POST http://localhost:8000/collections \
  -H "Content-Type: application/json" \
  -d '{
        "name": "Payments - SEV",
        "description": "Incident runbooks for payment outages"
      }'
```

### 2. Create an incident prompt within that collection
```bash
curl -X POST http://localhost:8000/prompts \
  -H "Content-Type: application/json" \
  -d '{
        "title": "Escalate PSP Timeout",
        "content": "Investigate PSP latencies > {{latency_threshold}}ms...",
        "description": "Use during PSP timeouts",
        "collection_id": "<collection-id>"
      }'
```

### 3. Search prompts within a collection
```bash
curl "http://localhost:8000/prompts?collection_id=<collection-id>&search=psp"
```

---

## API Endpoint Summary
| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Service health and version metadata. |
| GET | `/prompts` | List prompts (supports `collection_id` and `search` query params). |
| GET | `/prompts/{prompt_id}` | Retrieve a single prompt by ID. |
| POST | `/prompts` | Create a new prompt. |
| PUT | `/prompts/{prompt_id}` | Replace an entire prompt document. |
| PATCH | `/prompts/{prompt_id}` | Partially update select prompt fields. |
| DELETE | `/prompts/{prompt_id}` | Remove a prompt permanently. |
| GET | `/collections` | List all collections. |
| GET | `/collections/{collection_id}` | Retrieve a collection. |
| POST | `/collections` | Create a collection. |
| DELETE | `/collections/{collection_id}` | Delete a collection (prompts are retained but their `collection_id` is cleared). |

### Example Request/Response: `POST /prompts`
```http
POST /prompts
Content-Type: application/json

{
  "title": "Notify leadership channel",
  "content": "Post update to #incident-room with status: {{status}}",
  "description": "Template for hourly leadership ping",
  "collection_id": "<collection-id>"
}
```
```http
201 Created
Content-Type: application/json

{
  "id": "2f23d8b9-9373-4e10-8fd1-5f4aa251c7a9",
  "title": "Notify leadership channel",
  "content": "Post update to #incident-room with status: {{status}}",
  "description": "Template for hourly leadership ping",
  "collection_id": "<collection-id>",
  "created_at": "2024-01-22T18:41:31.123456",
  "updated_at": "2024-01-22T18:41:31.123456"
}
```
For full request/response documentation, see [`docs/API_REFERENCE.md`](docs/API_REFERENCE.md).

---

## Development Setup
- **Env vars:** None required today; add a `.env` only when new settings appear.
- **Live reload:** `uvicorn app.api:app --reload` restarts the server on each file save.
- **Testing:** `pytest tests/ -v --cov=app` from `backend/` keeps regressions out.
- **Style:** Follow PEP 8, keep functions concise, and include descriptive type-hinted docstrings.
- **Data reset:** Storage is in-memory, so restarting the API wipes data; plan persistence accordingly.

---

## Contributing Guidelines
1. **Fork & Branch** – Work from a feature branch (`feature/short-description`).
2. **Plan with Specs** – Capture significant enhancements in the `specs/` directory before coding.
3. **Tests First** – Add or update pytest coverage for any new logic or bug fix.
4. **Keep Commits Focused** – Write descriptive commit messages and avoid mixing unrelated changes.
5. **Lint & Verify** – Ensure `pytest` succeeds and the API boots locally before opening a PR.
6. **Pull Request Template** – Describe context, testing evidence, and any follow-up tasks. Request at least one review.

---

## Additional Resources
- [`PROJECT_BRIEF.md`](PROJECT_BRIEF.md) – 4-week roadmap and grading rubric.
- [`docs/API_REFERENCE.md`](docs/API_REFERENCE.md) – Detailed endpoint specification.
- [`specs/`](specs/) – Product specs for upcoming roadmap items.

Have questions? File an issue, open a discussion, or reach out to the incident engineering team. Happy shipping! 🚀
