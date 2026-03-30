# PromptLab

PromptLab is a comprehensive API platform designed for managing AI prompts effectively. By utilizing FastAPI, PromptLab enables developers to efficiently store, organize, and handle AI prompt templates, providing a structured workflow that enhances AI and machine learning development activities.

---

## Project Overview

PromptLab serves as a robust tool for AI engineers, allowing for the management and organization of AI prompts through:

- **Centralized Management**: Store prompts with advanced template capabilities using variables.
- **Organizational Structure**: Group prompts into thematic collections.
- **Efficient Retrieval**: Utilize search and tag functionalities for quick access.
- **Version Management**: Keep track of prompt revisions.
- **Testing Environment**: Validate and test prompts with sample data before deployment.

---

## Setup Instructions

### Prerequisites

Ensure your environment includes the following:

- **Python**: >= 3.10
- **Node.js**: >= 18 (for future frontend development)
- **Git**: For version control operations

### Installation

Set up PromptLab by following these steps:

1. **Clone the Repository**:

   ```bash
   git clone <repository-url>
   cd promptlab
   ```

2. **Backend Initialization**:

   Navigate to the backend directory and install dependencies:

   ```bash
   cd backend
   pip install -r requirements.txt
   ```

---

## Running the Application

### Startup

To initiate the backend server:

```bash
python main.py
```

- **API Base URL**: Accessible at [http://localhost:8000](http://localhost:8000)
- The API server is immediately available to serve requests and interact with your prompt data.

---

## API Endpoints

Below, you will find detailed descriptions and usage examples for key endpoints:

### Health Check Endpoint

- **GET** `/health`
  - **Purpose**: Check server health and current version status.
  - **Example Command**:
    ```bash
    curl http://localhost:8000/health
    ```

### Prompt Management Endpoints

- **List All Prompts**
  - **GET** `/prompts`
  - **Description**: Retrieve a comprehensive list of all saved prompts.
  - **Example**:
    ```bash
    curl http://localhost:8000/prompts
    ```

- **Create a New Prompt**
  - **POST** `/prompts`
  - **Description**: Add a new prompt to the database.
  - **Example**:
    ```bash
    curl -X POST "http://localhost:8000/prompts" \
         -H "Content-Type: application/json" \
         -d '{"title": "Creative Writing", "content": "Write a story about...", "description": "Story prompt"}'
    ```

- **Retrieve a Specific Prompt**
  - **GET** `/prompts/{prompt_id}`
  - **Description**: Access details of a specific prompt by ID.
  - **Example**:
    ```bash
    curl http://localhost:8000/prompts/your_prompt_id
    ```

- **Update Prompt Details**
  - **PUT** `/prompts/{prompt_id}`
  - **Description**: Modify an existing prompt's details.
  - **Example**:
    ```bash
    curl -X PUT "http://localhost:8000/prompts/your_prompt_id" \
         -H "Content-Type: application/json" \
         -d '{"title": "Updated Title", "content": "New prompt content", "description": "Updated description"}'
    ```

- **Delete a Prompt**
  - **DELETE** `/prompts/{prompt_id}`
  - **Description**: Permanently remove a prompt.
  - **Example**:
    ```bash
    curl -X DELETE http://localhost:8000/prompts/your_prompt_id
    ```

### Collection Management Endpoints

- **List Collections**
  - **GET** `/collections`
  - **Description**: Retrieve all collections available in the system.
  - **Example**:
    ```bash
    curl http://localhost:8000/collections
    ```

- **Create a Collection**
  - **POST** `/collections`
  - **Description**: Add a new collection for organizing prompts.
  - **Example**:
    ```bash
    curl -X POST "http://localhost:8000/collections" \
         -H "Content-Type: application/json" \
         -d '{"name": "Inspiration", "description": "Prompts for inspiration"}'
    ```

- **Delete a Collection**
  - **DELETE** `/collections/{collection_id}`
  - **Description**: Delete a specified collection.
  - **Example**:
    ```bash
    curl -X DELETE http://localhost:8000/collections/your_collection_id
    ```

---

## Data Models

### Prompt Model Schema

- **Attributes**:
  - `id`: Unique identifier (UUID format)
  - `title`: String, represents the prompt's title
  - `content`: String, the main content of the prompt
  - `description`: Optional description of the prompt
  - `collection_id`: ID of the collection to which the prompt belongs
  - `created_at`: Timestamp of creation
  - `updated_at`: Timestamp of the last update

### Collection Model Schema

- **Attributes**:
  - `id`: Unique identifier (UUID format)
  - `name`: String, the name of the collection
  - `description`: Optional description of the collection
  - `created_at`: Timestamp indicating when the collection was created

---

## Usage Examples

### Python Usage: Fetch All Prompts

To integrate PromptLab within a Python application or script:

```python
import requests

response = requests.get("http://localhost:8000/prompts")
prompts = response.json()
print(prompts)
```

### Command-Line: Add a New Prompt

Use curl for directly interfacing with the PromptLab API:

```bash
curl -X POST "http://localhost:8000/prompts" \
     -H "Content-Type: application/json" \
     -d '{"title": "Quick Brainstorm", "content": "Think of a new idea...", "description": "Brainstorming session"}'
```

---

## Development Setup

### Forking and Cloning

1. **Fork the Repository**: Create your copy of the project repository on GitHub.
2. **Clone to Local Machine**:

   ```bash
   git clone <your-fork-url>
   cd promptlab
   ```

3. **Backend Preparation**:
   - Install backend requirements and start the development server using the setup instructions provided earlier.

---
## Docker Setup

You can run the PromptLab application using Docker for a consistent and isolated environment.

### Prerequisites

- **Docker**: Ensure Docker is installed on your machine.
- **Docker Compose**: Ensure Docker Compose is installed.

### Build and Run with Docker

1. **Build and Run the Container**:

   From the project root, you can build the Docker image and start the container with Docker Compose:

   ```bash
   docker-compose up --build
   ```

   This command will build the Docker image and start the application, making it accessible at [http://localhost:8000](http://localhost:8000).

2. **Stop the Container**:

   To stop the running container, run:

   ```bash
   docker-compose down
   ```

3. **Rebuild the Container**:

   If you make changes to dependencies or the Docker configuration, rebuild the container with:

   ```bash
   docker-compose up --build
   ```

Using Docker ensures that you are working within a contained environment that mimics production, improving reliability and ease of deployment.

---
## Contributions

For contributions, enhancements, or bug reports, please open an issue or pull request on GitHub. We appreciate community input to drive the project forward.

