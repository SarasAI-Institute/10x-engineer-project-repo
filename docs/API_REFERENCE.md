# API Reference for PromptLab

## Health Check Endpoint

### GET `/health`
- **Description**: Checks the health status of the API.
- **Parameters**: None
- **Request Body**: None
- **Response Format**:
  - `HealthResponse` object containing:
    - `status`: A string indicating the health status (e.g., "healthy").
    - `version`: Current API version.
- **Error Codes**: None
- **Request Example**:
  - `GET /health`
- **Response Example**:
  ```json
  {
    "status": "healthy",
    "version": "1.0.0"
  }
  ```
- **Error Response Format**: None
- **Authentication**: None

## Prompt Endpoints

### GET `/prompts`
- **Description**: Retrieves a list of prompts, optionally filtered by collection or search query.
- **Parameters**:
  - `collection_id` (optional): ID of the collection to filter.
  - `search` (optional): Search query to filter prompts.
- **Request Body**: None
- **Response Format**:
  - `PromptList` object containing:
    - `prompts`: List of `Prompt` objects.
    - `total`: Total count of prompts.
- **Error Codes**: None
- **Request Example**:
  - `GET /prompts`
- **Response Example**:
  ```json
  {
    "prompts": [
      { "id": "1", "title": "Example Prompt", "content": "Sample content" },
      // ... other prompts ...
    ],
    "total": 1
  }
  ```
- **Error Response Format**: None
- **Authentication**: None

### GET `/prompts/{prompt_id}`
- **Description**: Retrieves a prompt by its ID.
- **Parameters**:
  - `prompt_id`: Unique identifier for the prompt.
- **Request Body**: None
- **Response Format**:
  - `Prompt` object containing prompt details.
- **Error Codes**:
  - `404`: Prompt not found
- **Request Example**:
  - `GET /prompts/example_prompt_id`
- **Response Example**:
  ```json
  {
    "id": "example_prompt_id",
    "title": "Example Prompt",
    "content": "Sample content"
  }
  ```
- **Error Response Format**:
  ```json
  {
    "detail": "Prompt not found"
  }
  ```
- **Authentication**: None

### POST `/prompts`
- **Description**: Creates a new prompt.
- **Parameters**: None
- **Request Body**:
  - `PromptCreate` object:
    - `text`: Text of the prompt.
    - `collection_id` (optional): Collection ID if applicable.
- **Response Format**:
  - `Prompt` object of the created prompt.
- **Error Codes**:
  - `400`: Collection not found
- **Request Example**:
  ```json
  {
    "text": "What is the capital of France?",
    "collection_id": "1"
  }
  ```
- **Response Example**:
  ```json
  {
    "id": "new_prompt_id",
    "title": "New Prompt",
    "content": "Sample content"
  }
  ```
- **Error Response Format**:
  ```json
  {
    "detail": "Collection not found"
  }
  ```
- **Authentication**: None

### PUT `/prompts/{prompt_id}`
- **Description**: Updates an existing prompt.
- **Parameters**:
  - `prompt_id`: Unique identifier for the prompt.
- **Request Body**:
  - `PromptUpdate` object with fields to update.
- **Response Format**:
  - `Prompt` object of the updated prompt.
- **Error Codes**:
  - `404`: Prompt not found
  - `400`: Collection not found
- **Request Example**:
  ```json
  {
    "title": "Updated Prompt",
    "content": "Updated content"
  }
  ```
- **Response Example**:
  ```json
  {
    "id": "example_prompt_id",
    "title": "Updated Prompt",
    "content": "Updated content"
  }
  ```
- **Error Response Format**:
  ```json
  {
    "detail": "Prompt not found"
  }
  ```
- **Authentication**: None

### PATCH `/prompts/{prompt_id}`
- **Description**: Partially updates an existing prompt.
- **Parameters**:
  - `prompt_id`: Unique identifier for the prompt.
- **Request Body**:
  - Fields to be updated within a `PromptUpdate` object.
- **Response Format**:
  - `Prompt` object of the updated prompt.
- **Error Codes**:
  - `404`: Prompt not found
- **Request Example**:
  ```json
  {
    "title": "Partially Updated Prompt"
  }
  ```
- **Response Example**:
  ```json
  {
    "id": "example_prompt_id",
    "title": "Partially Updated Prompt",
    "content": "Original content"
  }
  ```
- **Error Response Format**:
  ```json
  {
    "detail": "Prompt not found"
  }
  ```
- **Authentication**: None

### DELETE `/prompts/{prompt_id}`
- **Description**: Deletes a prompt by ID.
- **Parameters**:
  - `prompt_id`: Unique identifier for the prompt.
- **Request Body**: None
- **Response Format**: None (if deleted successfully)
- **Error Codes**:
  - `404`: Prompt not found
- **Request Example**:
  - `DELETE /prompts/example_prompt_id`
- **Error Response Format**:
  ```json
  {
    "detail": "Prompt not found"
  }
  ```
- **Authentication**: None

## Collection Endpoints

### GET `/collections`
- **Description**: Retrieves all collections.
- **Parameters**: None
- **Request Body**: None
- **Response Format**:
  - `CollectionList` object containing:
    - `collections`: List of `Collection` objects.
    - `total`: Total count of collections.
- **Error Codes**: None
- **Request Example**:
  - `GET /collections`
- **Response Example**:
  ```json
  {
    "collections": [
      { "id": "1", "name": "Example Collection" },
      // ... other collections ...
    ],
    "total": 1
  }
  ```
- **Authentication**: None

### GET `/collections/{collection_id}`
- **Description**: Retrieves a specific collection by ID.
- **Parameters**:
  - `collection_id`: Unique identifier for the collection.
- **Request Body**: None
- **Response Format**:
  - `Collection` object detailing the collection.
- **Error Codes**:
  - `404`: Collection not found
- **Request Example**:
  - `GET /collections/example_collection_id`
- **Response Example**:
  ```json
  {
    "id": "example_collection_id",
    "name": "Example Collection"
  }
  ```
- **Error Response Format**:
  ```json
  {
    "detail": "Collection not found"
  }
  ```
- **Authentication**: None

### POST `/collections`
- **Description**: Creates a new collection.
- **Parameters**: None
- **Request Body**:
  - `CollectionCreate` object:
    - `name`: Name of the collection.
    - `description`: Description of the collection.
- **Response Format**:
  - `Collection` object of the newly created collection.
- **Error Codes**: None
- **Request Example**:
  ```json
  {
    "name": "New Collection",
    "description": "Description of new collection"
  }
  ```
- **Response Example**:
  ```json
  {
    "id": "new_collection_id",
    "name": "New Collection",
    "description": "Description of new collection"
  }
  ```
- **Authentication**: None

### DELETE `/collections/{collection_id}`
- **Description**: Deletes a collection and its orphaned prompts.
- **Parameters**:
  - `collection_id`: Unique identifier for the collection.
- **Request Body**: None
- **Response Format**: None (if deleted successfully)
- **Error Codes**:
  - `404`: Collection not found
- **Request Example**:
  - `DELETE /collections/example_collection_id`
- **Error Response Format**:
  ```json
  {
    "detail": "Collection not found"
  }
  ```
- **Authentication**: None
