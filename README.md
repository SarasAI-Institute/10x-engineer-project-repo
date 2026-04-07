# Incident Management API

## Project Overview

This project is a FastAPI-based application designed for managing incidents. It provides a robust backend for handling prompts and collections, allowing for effective tracking and categorization of various incidents within a given system.

## Setup Instructions

To set up the project locally, follow these steps:

Here is a clarified and structured version, step-by-step:

## Step-by-Step Setup

1. **Clone the Repository**
   - Use the command:
     ```bash
     git clone <repository-url>
     ```
   - Replace `<repository-url>` with the actual URL of the repository.

2. **Navigate to the Project Directory**
   - Move into the directory:
     ```bash
     cd repository-directory
     ```
   - Replace `repository-directory` with the name of your project folder.

3. **Create and Activate a Virtual Environment** (recommended)
   - To create a virtual environment:
     ```bash
     python -m venv env
     ```
   - Activate the virtual environment:
     - On macOS and Linux:
       ```bash
       source env/bin/activate
       ```
     - On Windows:
       ```bash
       env\\Scripts\\activate
       ```

4. **Install Dependencies**
   - Install the necessary packages:
     ```bash
     pip install -r requirements.txt
     ```

5. **Run the Application**
   - Start the application using:
     ```bash
     uvicorn backend.main:app --reload
     ```
   - Access the application at `http://127.0.0.1:8000`.

## API Endpoints

### Health Check
- **GET** `/health`
  - **Description**: Checks if the API is running and healthy.
  - **Response**: Returns a JSON status and version.

### Prompt Endpoints
- **GET** `/prompts`
  - **Parameters**:
    - `collection_id` (optional)
    - `search` (optional)
  - **Response**: A list of prompts matching the filters.

- **GET** `/prompts/{prompt_id}`
  - **Response**: Details for a specific prompt by ID.

- **POST** `/prompts`
  - **Body**: JSON with `title`, `content`, `description`, `collection_id`.
  - **Response**: Newly created prompt object.

- **PUT** `/prompts/{prompt_id}`
  - **Body**: Fields to be updated for a prompt.
  - **Response**: Updated prompt.

- **PATCH** `/prompts/{prompt_id}`
  - **Description**: Partially update a prompt.

- **DELETE** `/prompts/{prompt_id}`
  - **Description**: Deletes a specified prompt.

### Collection Endpoints
- **GET** `/collections`
  - **Response**: Lists all collections.

- **GET** `/collections/{collection_id}`
  - **Response**: Details of a collection by ID.

- **POST** `/collections`
  - **Body**: JSON for new collection details.
  - **Response**: Created collection object.

- **DELETE** `/collections/{collection_id}`
  - **Description**: Deletes a collection and orphans its prompts.


  To ensure comprehensive coverage of models and API endpoints, let's list all potential examples and ensure they are documented. Here's a possible extended view, including all found details:

## Extended API Endpoints

### Health Check

- **GET** `/health`
  - **Description**: Check the service health.
  - **Response**: JSON indicating service status and version.

### Prompt Endpoints

- **GET** `/prompts`
  - **Query Parameters**:
    - **collection_id** (Optional): Filter prompts by specific collection.
    - **search** (Optional): Search query for filtering prompts by title/description.
  - **Response**: List of prompts filtered or all prompts if no query is provided.

- **GET** `/prompts/{prompt_id}`
  - **Path Parameter**: `prompt_id`
  - **Response**: Detailed prompt object by ID.

- **POST** `/prompts`
  - **Body Example**:
    ```json
    {
      "title": "Incident Analysis",
      "content": "Analyze and document incident details.",
      "description": "Documentation for incident analysis",
      "collection_id": "analysis-collection-id"
    }
    ```
  - **Response**: Object of the created prompt.

- **PUT** `/prompts/{prompt_id}`
  - **Body Example**:
    ```json
    {
      "title": "Updated Incident Title"
    }
    ```
  - **Response**: Updated prompt object with new details.

- **PATCH** `/prompts/{prompt_id}`

- **DELETE** `/prompts/{prompt_id}`
  - **Description**: Deletes the prompt and returns no content on success.

### Collection Endpoints

- **GET** `/collections`
  - **Response**: Get all collections data.

- **GET** `/collections/{collection_id}`
  - **Response**: Collection details by its ID.

- **POST** `/collections`
  - **Body Example**:
    ```json
    {
      "name": "New Collection",
      "description": "Collection for incident categorizations"
    }
    ```
  - **Response**: Newly created collection object.

- **DELETE** `/collections/{collection_id}`
  - **Description**: Deletes identified collection and updates corresponding prompts.

## Extended Data Models

### Prompt Models

- **PromptBase**
  ```json
  {
    "title": "Incident Title",
    "content": "Detailed content of the prompt.",
    "description": "Optional description",
    "collection_id": "optional-collection-id"
  }
  ```

- **PromptCreate**: Same fields as `PromptBase`.

- **PromptUpdate**
  ```json
  {
    "title": "Optional new title",
    "content": "Optional new content",
    "description": "Optional new description",
    "collection_id": "Optional new collection ID"
  }
  ```

- **Prompt**: Includes all `PromptBase` fields plus metadata like `id`, `created_at`, and `updated_at`.

- **PromptList**: Represents a paginated list or filtered list of prompts.

### Collection Models

- **CollectionBase**
  ```json
  {
    "name": "Collection Name",
    "description": "Brief description"
  }
  ```

- **CollectionCreate**: Same fields as `CollectionBase`.

- **Collection**: Includes all `CollectionBase` fields plus metadata like `id`, `created_at`.

- **CollectionList**: Represents a list of collections to enable pagination.

### Response Models

- **HealthResponse**
  ```json
  {
    "status": "healthy",
    "version": "1.0.0"
  }
  ```

## Data Models

### Prompt Models
- **PromptBase**: Contains `title`, `content`, and optional `collection_id`.
- **PromptCreate**: Extends `PromptBase` for new prompts.
- **PromptUpdate**: Optional fields for prompt updates.
- **Prompt**: Complete prompt data model.
- **PromptList**: Wrapper for a list of prompts.

### Collection Models
- **CollectionBase**: Common fields for collections.
- **CollectionCreate**: Used when creating collections.
- **Collection**: Full collection data model.
- **CollectionList**: Wrapper for a list of collections.

### Response Models
- **HealthResponse**: Represents the health check results.

## Usage Examples

### Adding a New Prompt
- Send a POST request to `/prompts` with JSON like:
  ```json
  {
    "title": "New Incident",
    "content": "Incident details...",
    "description": "Brief description",
    "collection_id": "example-collection-id"
  }
  ```

### Fetching a Collection
- Use the endpoint `/collections/{collection_id}` to get specific collection data.

I ensured each section is thoroughly detailed to ensure clarity for users setting up and using your API. If more information needs to be included or if specific details should be adjusted, please let me know!

