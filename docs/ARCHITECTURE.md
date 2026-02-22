# PromptLab Architecture Documentation

## Overview

PromptLab is built using a modern, layered architecture with clear separation of concerns. This document describes the system architecture, design decisions, and data flow.

---

## Technology Stack

### Backend
- **Framework:** FastAPI 0.104+
- **Language:** Python 3.10+
- **Validation:** Pydantic v2
- **ASGI Server:** Uvicorn
- **Testing:** pytest

### Storage
- **Current:** In-memory storage (development)
- **Future:** PostgreSQL / MongoDB (production)

---

## Architecture Layers

```
┌─────────────────────────────────────┐
│         API Layer (api.py)          │
│  - HTTP endpoints                   │
│  - Request/response handling        │
│  - Input validation                 │
│  - Error handling                   │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│      Models Layer (models.py)       │
│  - Pydantic models                  │
│  - Data validation                  │
│  - Serialization                    │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│    Business Logic (utils.py)        │
│  - Sorting & filtering              │
│  - Search algorithms                │
│  - Data transformations             │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│    Storage Layer (storage.py)       │
│  - Data persistence                 │
│  - CRUD operations                  │
│  - Data retrieval                   │
└─────────────────────────────────────┘
```

---

## Component Details

### 1. API Layer (`app/api.py`)

**Responsibilities:**
- Define HTTP routes and endpoints
- Handle HTTP requests and responses
- Perform input validation via Pydantic
- Return appropriate status codes
- Handle errors and exceptions
- Apply CORS middleware

**Key Design Patterns:**
- RESTful API design
- Dependency injection (FastAPI)
- Middleware pattern (CORS)

**Example Flow:**
```
HTTP Request → FastAPI Router → Endpoint Handler → 
Business Logic → Storage Layer → Response
```

### 2. Models Layer (`app/models.py`)

**Responsibilities:**
- Define data structures using Pydantic
- Validate incoming data
- Serialize/deserialize JSON
- Generate default values (IDs, timestamps)

**Models:**
- `Prompt`: Full prompt with all fields
- `PromptCreate`: Data for creating prompts
- `PromptUpdate`: Data for updating prompts
- `Collection`: Full collection with all fields
- `CollectionCreate`: Data for creating collections
- `PromptList`: Response with list of prompts
- `CollectionList`: Response with list of collections
- `HealthResponse`: Health check response

**Key Features:**
- Automatic UUID generation
- UTC timestamp generation
- Field validation (length, required fields)
- Type safety

### 3. Business Logic Layer (`app/utils.py`)

**Responsibilities:**
- Sort prompts by date
- Filter prompts by collection
- Search prompts by text
- Validate prompt content
- Extract template variables

**Functions:**
- `sort_prompts_by_date()`: Sort with configurable order
- `filter_prompts_by_collection()`: Filter by collection ID
- `search_prompts()`: Case-insensitive text search
- `validate_prompt_content()`: Content validation rules
- `extract_variables()`: Extract `{{variable}}` patterns

### 4. Storage Layer (`app/storage.py`)

**Responsibilities:**
- Persist data (in-memory for now)
- CRUD operations for prompts
- CRUD operations for collections
- Handle data relationships
- Manage orphaned prompts

**Current Implementation:**
- Python dictionaries for O(1) lookups
- Singleton pattern (global `storage` instance)
- Not thread-safe (single-threaded usage only)
- Data lost on restart (in-memory only)

**Future Considerations:**
- Replace with SQLAlchemy/PostgreSQL
- Add connection pooling
- Implement transactions
- Add caching layer (Redis)

---

## Data Flow

### Creating a Prompt

```
1. POST /prompts
   ↓
2. FastAPI validates request body against PromptCreate model
   ↓
3. If collection_id provided, verify collection exists
   ↓
4. Create Prompt object (generates ID and timestamps)
   ↓
5. Storage.create_prompt() stores in dictionary
   ↓
6. Return created prompt (201 Created)
```

### Listing Prompts with Filters

```
1. GET /prompts?collection_id=X&search=Y
   ↓
2. Storage.get_all_prompts() retrieves all prompts
   ↓
3. filter_prompts_by_collection() filters by collection
   ↓
4. search_prompts() filters by search query
   ↓
5. sort_prompts_by_date() sorts newest first
   ↓
6. Return PromptList with prompts and total count
```

### Deleting a Collection

```
1. DELETE /collections/{id}
   ↓
2. Storage.delete_collection() checks if exists
   ↓
3. If exists, delete collection from storage
   ↓
4. Find all prompts with this collection_id
   ↓
5. Set their collection_id to None (orphaned)
   ↓
6. Return 204 No Content
```

---

## Design Decisions

### Why FastAPI?

- **Fast:** Built on Starlette and Pydantic (high performance)
- **Auto-documentation:** Automatic OpenAPI/Swagger UI
- **Type Safety:** Python type hints for validation
- **Modern:** Async support, dependency injection
- **Developer Experience:** Great error messages, easy testing

### Why Pydantic?

- **Validation:** Automatic data validation
- **Serialization:** Easy JSON conversion
- **Type Safety:** Runtime type checking
- **Documentation:** Auto-generates schema

### Why In-Memory Storage (for now)?

- **Simplicity:** Easy to understand and test
- **Speed:** Fast for development/prototyping
- **No Dependencies:** No database setup required
- **Easy Migration:** Clear separation allows easy DB replacement

### RESTful API Design

- **Resource-based URLs:** `/prompts`, `/collections`
- **HTTP verbs:** GET (read), POST (create), PUT/PATCH (update), DELETE (delete)
- **Status codes:** 200 (OK), 201 (Created), 204 (No Content), 404 (Not Found)
- **JSON format:** Standard request/response format

---

## Data Model Relationships

```
Collection (1) ──< (N) Prompt
```

- One collection can have many prompts
- One prompt belongs to zero or one collection
- Collections can be deleted (prompts become orphaned)
- Prompts can exist without a collection

---

## Security Considerations

### Current State (Development)

- ❌ No authentication
- ❌ No authorization
- ❌ No rate limiting
- ✅ Input validation via Pydantic
- ✅ CORS enabled (allow all origins)

### Production Requirements

- ✅ Add JWT authentication
- ✅ Add role-based access control
- ✅ Implement rate limiting
- ✅ Restrict CORS to specific domains
- ✅ Add HTTPS/TLS
- ✅ Sanitize user inputs
- ✅ Add request logging
- ✅ Implement API keys for external access

---

## Performance Considerations

### Current Performance

- **In-memory storage:** O(1) lookups, very fast
- **List operations:** O(n) iteration, acceptable for small datasets
- **Search:** O(n) linear search, inefficient for large datasets
- **Sorting:** O(n log n), built-in Python sort

### Scaling Strategies

1. **Database Migration:**
   - PostgreSQL with indexes for fast lookups
   - Full-text search for efficient searching
   - Connection pooling for concurrent requests

2. **Caching:**
   - Redis for frequently accessed data
   - Cache invalidation on updates

3. **Pagination:**
   - Add `limit` and `offset` parameters
   - Reduce response sizes for large datasets

4. **Async Operations:**
   - FastAPI already supports async
   - Use async database drivers (asyncpg)

5. **Horizontal Scaling:**
   - Stateless API (easy to load balance)
   - Multiple app instances behind load balancer

---

## Testing Strategy

### Unit Tests
- Test individual functions in `utils.py`
- Mock storage layer
- Test edge cases and validation

### Integration Tests
- Test API endpoints end-to-end
- Use pytest fixtures for setup/teardown
- Test request/response formats

### Test Coverage Goals
- 80%+ code coverage
- All endpoints tested
- All error cases tested

---

## Future Enhancements

### Short Term
1. Add tags to prompts
2. Implement prompt versioning
3. Add user authentication
4. Export/import functionality

### Medium Term
1. PostgreSQL database migration
2. Full-text search with Elasticsearch
3. Prompt execution/testing
4. Collaborative features (sharing, comments)

### Long Term
1. Multi-tenancy support
2. Analytics and usage tracking
3. AI-powered prompt suggestions
4. Integration with LLM providers (OpenAI, Anthropic)
5. Template marketplace

---

## Maintenance and Operations

### Logging
- Add structured logging (JSON format)
- Log all API requests (method, path, status, duration)
- Log errors with stack traces
- Use different log levels (DEBUG, INFO, WARNING, ERROR)

### Monitoring
- Health check endpoint (`/health`)
- Add metrics endpoint (Prometheus format)
- Monitor response times
- Track error rates

### Deployment
- Docker containerization
- Environment-based configuration
- CI/CD pipeline (GitHub Actions)
- Automated testing before deployment

---

## Developer Onboarding

### Getting Started

1. **Setup:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Run locally:**
   ```bash
   python main.py
   ```

3. **Run tests:**
   ```bash
   pytest tests/ -v
   ```

4. **View API docs:**
   Open `http://localhost:8000/docs`

### Code Organization

- `main.py` - Entry point
- `app/__init__.py` - Package metadata
- `app/api.py` - API routes
- `app/models.py` - Data models
- `app/storage.py` - Data persistence
- `app/utils.py` - Helper functions
- `tests/` - Test suite

### Making Changes

1. Write code following the coding standards
2. Add/update docstrings
3. Write tests for new features
4. Run tests before committing
5. Create meaningful commit messages

---

## Glossary

- **Prompt:** A template text with optional variables for AI model input
- **Collection:** A logical grouping of related prompts
- **Template Variable:** A placeholder in format `{{name}}` that can be replaced
- **Orphaned Prompt:** A prompt whose collection has been deleted
- **CRUD:** Create, Read, Update, Delete operations
- **REST:** Representational State Transfer (API design pattern)
