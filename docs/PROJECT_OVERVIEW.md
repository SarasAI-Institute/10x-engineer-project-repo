# PROJECT_OVERVIEW.md

## 1. Project Overview and Purpose
PromptLab is an internal tool crafted for AI engineers to store, organize, and manage AI prompts efficiently. It serves as a "Postman for Prompts," allowing teams to store, organize, and version their prompt workflows for consistent and reliable AI tasks.

## 2. Features List
- Store prompt templates with variables like `{{input}}`, `{{context}}`.
- Organize prompts into collections.
- Tagging and search for easy prompt retrieval.
- Track version histories of different prompt drafts.
- Test prompts with various sample inputs.

## 3. Prerequisites and Installation
### Prerequisites
- Python 3.10+
- Node.js 18+ (for frontend setup)
- Git

### Installation
1. **Clone the Repository:**
    ```bash
    git clone <your-repo-url>
    cd promptlab
    ```

2. **Set up the Backend:**
    Navigate to the backend directory, install the required packages, and start the server:
    ```bash
    cd backend
    pip install -r requirements.txt
    python main.py
    ```
3. **Run Tests:**
   Use the following command to execute the test suite and ensure everything is functioning as expected:
   ```bash
   pytest tests/ -v
   ```
4. **Access the API:**
   Once running, access the API at: http://localhost:8000, with documentation available at http://localhost:8000/docs.

## 4. Quick Start Guide
1. **Clone the Repository:** Start by cloning the PromptLab repository.
2. **Backend Setup:** Navigate to the backend directory, install requirements, and run the server.
3. **Access the API:** Your API will be running at http://localhost:8000, with documentation available at http://localhost:8000/docs.

## 5. API Endpoint Summary with Examples
- **GET /health**: Check the health of the API.
- **GET /prompts**: List all prompts. *(Status: Has issues)*
- **GET /prompts/{id}**: Retrieve a single prompt. *(Status: Bug)*
- **POST /prompts**: Create a new prompt. *(Status: Works)*
- **PUT /prompts/{id}**: Update a prompt. *(Status: Has issues)*
- **DELETE /prompts/{id}**: Delete a prompt. *(Status: Works)*
- **GET /collections** and **/collections/{id}**: Manage prompt collections. *(Status: Works except for deletion bug)*

## 6. Development Setup
- Set up a Python virtual environment for dependency management.
- Use `pytest` for running the test suite:
  ```bash
  cd backend
  pytest tests/ -v
  ```
- Run Docker containers using the provided Docker configuration for an isolated development environment.

## 7. Contributing Guidelines
PromptLab encourages experimentation and offers flexibility for implementing improvements:
- **Fork the repository** and create a new branch for your feature or bug fix.
- **Commit changes** with meaningful messages to maintain a clean project history.
- **Run tests** before pushing changes to ensure stability.
- **Create pull requests** for incorporating your work into the main branch.

The focus is on learning how to build robust software quickly with AI, promoting a culture that embraces breaking things and rebuilding them better.
