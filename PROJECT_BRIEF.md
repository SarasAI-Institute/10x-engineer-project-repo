# PromptLab: Project Brief

## Your 4-Week Engineering Assignment

---

## Overview

You've joined the PromptLab team as a software engineer. Your mission is to take this partially-built backend and transform it into a **production-ready, full-stack application** over the next 4 weeks.

Each week, you'll focus on a different aspect of professional software development:

| Week | Focus | Deliverable | Weight |
|------|-------|-------------|--------|
| 1 | Backend Foundation | Working API (bugs fixed) | 25% |
| 2 | Documentation & Specs | Fully documented codebase | 25% |
| 3 | Testing & DevOps | Production-ready backend | 25% |
| 4 | Full-Stack Integration | Complete application | 25% |

**Grading:** Satisfactory (S) if total ≥ 70%, Unsatisfactory (U) if < 70%

---

# Week 1: Backend Foundation

## Theme: "The Brownfield Challenge"

### Scenario

You've inherited this codebase from a developer who left the company. The basics are there, but there are bugs, missing features, and the documentation is... lacking.

Your first job is to **understand** this code and **fix** what's broken.

### Learning Objectives

- Use AI tools to understand unfamiliar codebases
- Apply debugging strategies with AI assistance
- Implement features following existing patterns

### Tasks

#### Task 1.1: Understand the Codebase
Use AI to explore and understand:
- [ ] What is the overall architecture?
- [ ] What are the main models and their relationships?
- [ ] How does the storage layer work?
- [ ] What API endpoints exist?

**Tip**: Ask your AI assistant questions like:
- "Explain the structure of this codebase"
- "How do prompts and collections relate to each other?"
- "Walk me through the request flow for creating a prompt"

#### Task 1.2: Fix Bug #1 - GET /prompts/{id} Returns 500
**Problem**: When requesting a prompt that doesn't exist, the API returns a 500 Internal Server Error instead of a 404 Not Found.

**Your job**: 
- [ ] Locate the bug in the code
- [ ] Fix it to return proper 404 response
- [ ] Ensure the test passes

#### Task 1.3: Fix Bug #2 - PUT Doesn't Update Timestamp
**Problem**: When updating a prompt via PUT, the `updated_at` field doesn't change.

**Your job**:
- [ ] Find where updates are handled
- [ ] Ensure `updated_at` is set to current time on update
- [ ] Verify with a test

#### Task 1.4: Fix Bug #3 - Sorting is Backwards
**Problem**: `GET /prompts` should return newest prompts first, but it's returning oldest first.

**Your job**:
- [ ] Find the sorting logic
- [ ] Fix the sort order
- [ ] Verify the change works

#### Task 1.5: Fix Bug #4 - Collection Deletion Issue
**Problem**: Deleting a collection doesn't handle the prompts that belong to it. They become orphaned with invalid `collection_id`.

**Your job**:
- [ ] Decide on a strategy (delete prompts? set to null? prevent deletion?)
- [ ] Implement the fix
- [ ] Add appropriate test

#### Task 1.6: Implement Missing Endpoint
**Problem**: There's no `PATCH /prompts/{id}` endpoint for partial updates.

**Your job**:
- [ ] Implement PATCH endpoint that allows partial updates
- [ ] Only update fields that are provided
- [ ] Don't require all fields like PUT does
- [ ] Update `updated_at` timestamp

### Deliverables

1. All bugs fixed
2. Missing endpoint implemented
3. All tests pass (`pytest tests/ -v`)
4. Code committed with meaningful commit messages

### Verification

Run the test suite to verify your fixes:

```bash
cd backend
pytest tests/ -v
```

All tests should pass. ✅

### 🚀 Bonus: Go Beyond (Optional)
Finished early? Want to challenge yourself?
- **Persist Data:** The current storage is in-memory and resets on restart. Try implementing `JSONFileStorage` or `SQLiteStorage` to save data to disk.
- **Better Search:** Improve the `search` parameter in `GET /prompts` to filter by tags or description, not just title.
- **AI-Powered:** Use AI to generate a `seed_data.py` script that populates your API with 50 realistic prompts for testing.

---

# Week 2: Documentation & Specifications

## Theme: "Spec-Driven Development"

### Scenario

Now that the backend works, we need to document it properly and plan new features. Good documentation is the difference between a "project" and a "product."

### Learning Objectives

- Generate comprehensive documentation with AI
- Write specifications for new features
- Create custom AI coding agents

### Tasks

#### Task 2.1: Create Comprehensive README
Replace the basic README with a professional one including:
- [ ] Project overview and purpose
- [ ] Features list
- [ ] Prerequisites and installation
- [ ] Quick start guide
- [ ] API endpoint summary with examples
- [ ] Development setup
- [ ] Contributing guidelines

#### Task 2.2: Add Docstrings to All Code
Add Google-style docstrings to every function and class:

**In `app/models.py`:**
- [ ] All Pydantic model classes
- [ ] All fields with descriptions

**In `app/api.py`:**
- [ ] All endpoint functions
- [ ] Include Args, Returns, Raises

**In `app/utils.py`:**
- [ ] All utility functions
- [ ] Include examples where helpful

**In `app/storage.py`:**
- [ ] Storage class and all methods

**Example format:**
```python
def get_prompt(prompt_id: str) -> Optional[Prompt]:
    """Retrieve a prompt by its unique identifier.
    
    Args:
        prompt_id: The unique identifier of the prompt to retrieve.
        
    Returns:
        The Prompt object if found, None otherwise.
        
    Raises:
        ValueError: If prompt_id is empty or invalid format.
        
    Example:
        >>> prompt = get_prompt("abc123")
        >>> print(prompt.title)
        "My Prompt"
    """
```

#### Task 2.3: Create API Reference Documentation
Create `docs/API_REFERENCE.md` with:
- [ ] Full endpoint documentation
- [ ] Request/response examples for each endpoint
- [ ] Error response formats
- [ ] Authentication notes (even if "none" for now)

#### Task 2.4: Create Custom AI Coding Agent
Create `.github/copilot-instructions.md` (or `.continuerules`) with:
- [ ] Project coding standards
- [ ] Preferred patterns and conventions
- [ ] File naming conventions
- [ ] Error handling approach
- [ ] Testing requirements

This file tells AI assistants how to write code for THIS project.

#### Task 2.5: Write Feature Specifications
Create specifications for two new features in `specs/` folder:

**`specs/prompt-versions.md`:**
- [ ] Overview of version tracking feature
- [ ] User stories with acceptance criteria
- [ ] Data model changes needed
- [ ] API endpoint specifications
- [ ] Edge cases to handle

**`specs/tagging-system.md`:**
- [ ] Overview of tagging feature
- [ ] User stories with acceptance criteria
- [ ] Data model changes needed
- [ ] API endpoint specifications
- [ ] Search/filter requirements

### Deliverables

1. Updated `README.md`
2. All code has docstrings (100% coverage)
3. `docs/API_REFERENCE.md` created
4. `.github/copilot-instructions.md` created
5. `specs/prompt-versions.md` created
6. `specs/tagging-system.md` created

### Verification

- [ ] README has all required sections
- [ ] Running `python -m pydoc app.models` shows docstrings
- [ ] API reference is complete and accurate
- [ ] Specs are detailed enough to implement from

### 🚀 Bonus: Go Beyond (Optional)
- **Interactive Docs:** Research tools like `MkDocs` or `Swagger UI` extensions to make your documentation interactive.
- **Diagrams:** Use Mermaid.js in your spec files to visualize the data model or request flow. Ask AI: "Generate a Mermaid class diagram for these Pydantic models."
- **Badges:** Add dynamic badges to your README (Build Status, Coverage, etc.).

---

# Week 3: Testing & DevOps

## Theme: "Production-Ready"

### Scenario

We're preparing for launch. That means comprehensive tests, CI/CD, and containerization. No more "it works on my machine."

### Learning Objectives

- Write comprehensive tests using TDD
- Set up CI/CD pipelines with GitHub Actions
- Containerize applications with Docker
- Refactor code for maintainability

### Tasks

#### Task 3.1: Write Comprehensive Test Suite
Achieve **80%+ code coverage**:

**`tests/test_api.py`:**
- [ ] Test all endpoints (happy path)
- [ ] Test error cases (404, 400, etc.)
- [ ] Test edge cases (empty strings, special characters)
- [ ] Test query parameters (sorting, filtering)

**`tests/test_storage.py`:**
- [ ] Test CRUD operations
- [ ] Test data persistence within session
- [ ] Test edge cases

**`tests/test_utils.py`:**
- [ ] Test all utility functions
- [ ] Test edge cases and error conditions

**`tests/test_models.py`:**
- [ ] Test model validation
- [ ] Test default values
- [ ] Test serialization

#### Task 3.2: Implement Feature Using TDD
Choose ONE feature from your Week 2 specs:
- Option A: **Prompt Versioning**
- Option B: **Tagging System**

Follow TDD approach:
1. [ ] Write failing tests first
2. [ ] Implement minimum code to pass
3. [ ] Refactor while keeping tests green
4. [ ] Repeat until feature complete

#### Task 3.3: Set Up GitHub Actions CI
Create `.github/workflows/ci.yml`:
- [ ] Trigger on push and pull request
- [ ] Set up Python environment
- [ ] Install dependencies
- [ ] Run linting (flake8 or ruff)
- [ ] Run tests with coverage
- [ ] Fail if coverage < 80%

**Example workflow structure:**
```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      # ... more steps
```

#### Task 3.4: Create Docker Configuration
Create containerization files:

**`backend/Dockerfile`:**
- [ ] Use appropriate Python base image
- [ ] Install dependencies
- [ ] Copy application code
- [ ] Expose correct port
- [ ] Set proper CMD

**`docker-compose.yml`** (in project root):
- [ ] Define backend service
- [ ] Map ports
- [ ] Set up environment variables
- [ ] Enable hot reload for development

#### Task 3.5: Refactor Code Smells
Review and improve code quality:
- [ ] Eliminate any DRY violations
- [ ] Break up functions longer than 20 lines
- [ ] Improve variable/function names
- [ ] Add type hints where missing
- [ ] Remove dead code

### Deliverables

1. Test coverage ≥ 80%
2. New feature implemented with tests
3. `.github/workflows/ci.yml` working
4. `Dockerfile` and `docker-compose.yml` working
5. Code refactored and clean

### Verification

```bash
# Run tests with coverage
pytest tests/ -v --cov=app --cov-report=term-missing

# Build and run Docker
docker-compose up --build

# Verify CI passes on GitHub
git push origin main
# Check Actions tab on GitHub
```

### 🚀 Bonus: Go Beyond (Optional)
- **Pre-commit Hooks:** Set up `pre-commit` to run linting automatically before every git commit.
- **Production DB:** Switch your Docker Compose setup to use a real PostgreSQL container instead of in-memory storage.
- **Mutation Testing:** Research "Mutation Testing" and try running `mutmut` on your codebase to find gaps in your tests.

---

# Week 4: Full-Stack Integration

## Theme: "Vibe Code the Frontend"

### Scenario

Time to make PromptLab usable! We need a beautiful, functional React frontend that connects to our API.

### Learning Objectives

- Generate frontend code with AI ("vibe coding")
- Build responsive, modern UIs
- Integrate frontend with backend APIs
- Handle loading states and errors gracefully

### Tasks

#### Task 4.1: Set Up React Project
Create the frontend application:
- [ ] Initialize React project with Vite
- [ ] Set up project structure
- [ ] Configure for API integration
- [ ] Add styling solution (CSS modules, Tailwind, etc.)

```bash
cd frontend
npm create vite@latest . -- --template react
npm install
```

#### Task 4.2: Create Core Components
Build the main UI components:

**Layout Components:**
- [ ] `Layout.jsx` - Main app layout with header/sidebar
- [ ] `Header.jsx` - App header with logo/navigation
- [ ] `Sidebar.jsx` - Collections navigation

**Prompt Components:**
- [ ] `PromptList.jsx` - Grid/list of prompts
- [ ] `PromptCard.jsx` - Individual prompt display
- [ ] `PromptForm.jsx` - Create/edit prompt form
- [ ] `PromptDetail.jsx` - Full prompt view

**Collection Components:**
- [ ] `CollectionList.jsx` - List of collections
- [ ] `CollectionForm.jsx` - Create collection form

**Shared Components:**
- [ ] `Button.jsx` - Reusable button
- [ ] `Modal.jsx` - Modal dialog
- [ ] `SearchBar.jsx` - Search input
- [ ] `LoadingSpinner.jsx` - Loading state
- [ ] `ErrorMessage.jsx` - Error display

#### Task 4.3: Implement API Integration
Create API layer and connect to backend:

**`src/api/client.js`:**
- [ ] Configure base URL
- [ ] Set up fetch wrapper
- [ ] Handle errors consistently

**`src/api/prompts.js`:**
- [ ] `getPrompts()` - List all prompts
- [ ] `getPrompt(id)` - Get single prompt
- [ ] `createPrompt(data)` - Create prompt
- [ ] `updatePrompt(id, data)` - Update prompt
- [ ] `deletePrompt(id)` - Delete prompt

**`src/api/collections.js`:**
- [ ] `getCollections()` - List collections
- [ ] `createCollection(data)` - Create collection
- [ ] `deleteCollection(id)` - Delete collection

#### Task 4.4: Implement Full CRUD Flow
Make everything work end-to-end:
- [ ] View all prompts on dashboard
- [ ] Click prompt to see details
- [ ] Create new prompt via form
- [ ] Edit existing prompt
- [ ] Delete prompt with confirmation
- [ ] Create and manage collections
- [ ] Filter prompts by collection

#### Task 4.5: Polish the UX
Make it production-quality:
- [ ] Loading states for all async operations
- [ ] Error handling with user-friendly messages
- [ ] Empty states (no prompts yet, etc.)
- [ ] Responsive design (mobile-friendly)
- [ ] Keyboard accessibility
- [ ] Form validation with feedback

#### Task 4.6: Connect Frontend to Backend
Ensure everything works together:
- [ ] Configure CORS on backend (if not already)
- [ ] Set up proxy or environment variables
- [ ] Test all operations end-to-end
- [ ] Handle network errors gracefully

### Deliverables

1. Working React frontend
2. All CRUD operations functional
3. Connected to backend API
4. Clean, professional UI/UX
5. Responsive design
6. Error and loading states handled

### Verification

```bash
# Terminal 1: Run backend
cd backend
python main.py

# Terminal 2: Run frontend
cd frontend
npm run dev
```

Open http://localhost:5173 and verify:
- [ ] Prompts display correctly
- [ ] Can create new prompt
- [ ] Can edit existing prompt
- [ ] Can delete prompt
- [ ] Collections work
- [ ] Search/filter works
- [ ] Looks professional

### 🚀 Bonus: Go Beyond (Optional)
- **Real AI Integration:** Add a "Run" button to your Prompt Detail page. Connect it to the OpenAI API (via your backend) to actually execute the prompts!
- **Dark/Light Mode:** Use AI to generate a theme switcher for your frontend.
- **Drag & Drop:** Implement drag-and-drop reordering for your Prompt List.

---

## Final Submission Checklist

Before submitting, ensure:

### Week 1 ✓
- [ ] All bugs fixed
- [ ] PATCH endpoint implemented
- [ ] All tests pass

### Week 2 ✓
- [ ] README is comprehensive
- [ ] All code has docstrings
- [ ] API reference complete
- [ ] Coding agent configured
- [ ] Feature specs written

### Week 3 ✓
- [ ] 80%+ test coverage
- [ ] New feature implemented with TDD
- [ ] CI/CD pipeline works
- [ ] Docker setup works

### Week 4 ✓
- [ ] React frontend complete
- [ ] All CRUD operations work
- [ ] API integration complete
- [ ] UI is polished

---

## Tips for Success

1. **Use AI extensively** — This is what you're learning!
2. **Commit often** — Small, meaningful commits
3. **Test as you go** — Don't leave testing for the end
4. **Read error messages** — They usually tell you what's wrong
5. **Ask for help** — In forums, from AI, from instructors

---

Good luck! Build something you're proud of. 🚀
