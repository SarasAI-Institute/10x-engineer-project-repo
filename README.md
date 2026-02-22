# PromptLab

**Your AI Prompt Engineering Platform**

---

## Welcome to the Team! 👋

Congratulations on joining the PromptLab engineering team! You've been brought on to help us build the next generation of prompt engineering tools.

### What is PromptLab?

PromptLab is an internal tool for AI engineers to **store, organize, and manage their prompts**. Think of it as a "Postman for Prompts" — a professional workspace where teams can:

- 📝 Store prompt templates with variables (`{{input}}`, `{{context}}`)
- 📁 Organize prompts into collections
- 🏷️ Tag and search prompts
- 📜 Track version history
- 🧪 Test prompts with sample inputs

### The Current Situation

The previous developer left us with a *partially working* backend. The core structure is there, but:

- There are **several bugs** that need fixing
- Some **features are incomplete**
- The **documentation is minimal** (you'll fix that)
- There are **no tests** worth mentioning
- **No CI/CD pipeline** exists
- **No frontend** has been built yet

Your job over the next 4 weeks is to transform this into a **production-ready, full-stack application**.

---

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+ (for Week 4)
- Git

### Run Locally

```bash
# Clone the repo
git clone <your-repo-url>
cd promptlab

# Set up backend
cd backend
pip install -r requirements.txt
python main.py
```

API runs at: http://localhost:8000

API docs at: http://localhost:8000/docs

### Run Tests

```bash
cd backend
pytest tests/ -v
```

---

## Project Structure

```
promptlab/
├── README.md                    # You are here
├── PROJECT_BRIEF.md             # Your assignment details
├── GRADING_RUBRIC.md            # How you'll be graded
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── api.py              # FastAPI routes (has bugs!)
│   │   ├── models.py           # Pydantic models
│   │   ├── storage.py          # In-memory storage
│   │   └── utils.py            # Helper functions
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_api.py         # Basic tests
│   │   └── conftest.py         # Test fixtures
│   ├── main.py                 # Entry point
│   └── requirements.txt
│
├── frontend/                    # You'll create this in Week 4
├── specs/                       # You'll create this in Week 2
├── docs/                        # You'll create this in Week 2
└── .github/                     # You'll set up CI/CD in Week 3
```

---

## Your Mission

### 🧪 Experimentation Encouraged!
While we provide guidelines, **you are the engineer**. If you see a better way to solve a problem using AI, do it!
- Want to swap the storage layer for a real database? **Go for it.**
- Want to add Authentication? **Do it.**
- Want to rewrite the API in a different style? **As long as tests pass, you're clear.**

The goal is to learn how to build *better* software *faster* with AI. Don't be afraid to break things and rebuild them better.

### Week 1: Fix the Backend
- Understand this codebase using AI
- Find and fix the bugs
- Implement missing features

### Week 2: Document Everything ✅
- ✅ Write proper documentation
- ✅ Create feature specifications
- ✅ Set up coding standards

### Week 3: Make it Production-Ready
- Write comprehensive tests
- Implement new features with TDD
- Set up CI/CD and Docker

### Week 4: Build the Frontend
- Create a React frontend
- Connect it to the backend
- Polish the user experience

---

## Documentation

Comprehensive documentation has been created for this project:

### 📚 Core Documentation
- **[API Reference](docs/API_REFERENCE.md)** - Complete API documentation with examples
- **[Architecture Guide](docs/ARCHITECTURE.md)** - System design and architecture decisions
- **[Developer Guide](docs/DEVELOPER_GUIDE.md)** - Setup, development workflow, and best practices
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Deploy to various environments
- **[Coding Standards](docs/CODING_STANDARDS.md)** - Code style, conventions, and quality standards

### 📋 Feature Specifications
- **[Prompt Management](specs/PROMPT_MANAGEMENT.md)** - CRUD operations for prompts
- **[Collection Management](specs/COLLECTION_MANAGEMENT.md)** - Organize prompts into collections
- **[Search and Filter](specs/SEARCH_AND_FILTER.md)** - Find prompts efficiently
- **[Specifications Index](specs/README.md)** - All feature specs and roadmap

### 🚀 Quick Links
- **API Docs (Swagger):** http://localhost:8000/docs
- **OpenAPI Schema:** http://localhost:8000/openapi.json
- **Health Check:** http://localhost:8000/health

---

## API Endpoints

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| GET | `/health` | Health check | ✅ Working |
| GET | `/prompts` | List all prompts (with search/filter) | ✅ Working |
| GET | `/prompts/{id}` | Get single prompt | ✅ Working |
| POST | `/prompts` | Create prompt | ✅ Working |
| PUT | `/prompts/{id}` | Update prompt (full) | ✅ Working |
| PATCH | `/prompts/{id}` | Update prompt (partial) | ✅ Working |
| DELETE | `/prompts/{id}` | Delete prompt | ✅ Working |
| GET | `/collections` | List collections | ✅ Working |
| GET | `/collections/{id}` | Get collection | ✅ Working |
| POST | `/collections` | Create collection | ✅ Working |
| DELETE | `/collections/{id}` | Delete collection | ✅ Working |

**Features:**
- 🔍 Search prompts by keyword
- 🗂️ Filter prompts by collection
- 🏷️ Template variables support (`{{variable}}`)
- ⏰ Auto-managed timestamps
- ✅ Full input validation
- 📝 Comprehensive error messages

See [API Reference](docs/API_REFERENCE.md) for detailed documentation.

---

## Tech Stack

### Backend
- **Framework:** FastAPI 0.104+
- **Language:** Python 3.10+
- **Validation:** Pydantic v2
- **Server:** Uvicorn (ASGI)
- **Testing:** pytest

### Storage
- **Current:** In-memory (development)
- **Planned:** PostgreSQL (production)

### Future Additions
- **Frontend:** React + Vite (Week 4)
- **DevOps:** Docker, GitHub Actions (Week 3)
- **Auth:** JWT-based authentication
- **Cache:** Redis

---

## Code Quality

### Documentation Coverage
- ✅ All modules documented
- ✅ All functions have docstrings (Google style)
- ✅ All classes documented
- ✅ API endpoints fully documented
- ✅ Examples provided

### Code Standards
- ✅ PEP 8 compliant (100 char line limit)
- ✅ Type hints on all functions
- ✅ Comprehensive error handling
- ✅ RESTful API design
- ✅ Consistent naming conventions

### Testing
- Current coverage: Check with `pytest --cov=app`
- Target coverage: 80%+
- See [Developer Guide](docs/DEVELOPER_GUIDE.md) for testing details

---

## Contributing

### Getting Started

1. **Read the documentation:**
   - [Developer Guide](docs/DEVELOPER_GUIDE.md) - Setup and workflow
   - [Coding Standards](docs/CODING_STANDARDS.md) - Code conventions

2. **Set up your environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   cd backend
   pip install -r requirements.txt
   ```

3. **Run tests:**
   ```bash
   pytest tests/ -v
   ```

4. **Make your changes:**
   - Follow coding standards
   - Add tests for new features
   - Update documentation

5. **Submit a pull request:**
   - Write clear commit messages
   - Reference related issues
   - Ensure all tests pass

### Code Review Process

All contributions are reviewed for:
- Code quality and standards compliance
- Test coverage
- Documentation updates
- Security considerations

See [Code Review Guidelines](docs/CODING_STANDARDS.md#code-review-guidelines) for details.

---

## Need Help?

### Resources

1. **Project Documentation:**
   - Start with [Developer Guide](docs/DEVELOPER_GUIDE.md)
   - Check [API Reference](docs/API_REFERENCE.md) for endpoint details
   - Review [Architecture](docs/ARCHITECTURE.md) for system design

2. **Assignment Details:**
   - Read `PROJECT_BRIEF.md` for detailed instructions
   - Check `GRADING_RUBRIC.md` to understand expectations

3. **AI Tools:**
   - This is an AI-assisted coding course!
   - See [AI Coding Assistant Configuration](docs/CODING_STANDARDS.md#ai-coding-assistant-configuration)

4. **Community:**
   - Ask questions in the course forum
   - Review existing issues and PRs

---

## Project Status

### Completed (Week 1-2)
- ✅ Backend API implementation
- ✅ Bug fixes (GET 404, timestamps, sorting, collection deletion)
- ✅ PATCH endpoint implementation
- ✅ Comprehensive documentation
- ✅ Feature specifications
- ✅ Coding standards

### In Progress (Week 3)
- ⏳ Comprehensive test suite
- ⏳ CI/CD pipeline
- ⏳ Docker containerization

### Planned (Week 4)
- 📋 React frontend
- 📋 Full-stack integration
- 📋 Production deployment

---

## License

This is an educational project for the 10x Engineer program.

---

**Built with ❤️ and AI assistance**

Good luck, and welcome to the team! 🚀
