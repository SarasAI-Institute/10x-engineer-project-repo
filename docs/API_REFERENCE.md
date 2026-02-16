# PromptLab API Reference Documentation

## Authentication
Currently, no authentication is required to access the API endpoints.

## Endpoints

### Health Check

- **Endpoint**: `GET /health`
- **Description**: Checks the health status of the application.
- **Response Example**:
  ```json
  {
    "status": "healthy",
    "version": "1.0.0"
  }
  ```
- **Error Responses**: N/A

### Prompt Endpoints

#### List Prompts

- **Endpoint**: `GET /prompts`
- **Description**: Retrieve a list of prompts with optional filtering and searching.
- **Query Parameters**:
  - `collection_id` (optional): Filter prompts by collection ID.
  - `search` (optional): Search prompts by content.
- **Response Example**:
  ```json
  {
    "prompts": [
      {
        "id": "1",
        "text": "Example text."
      }
    ],
    "total": 1
  }
  ```
- **Error Responses**: If an error occurs during retrieval, an internal server error is returned.

#### Get Prompt

- **Endpoint**: `GET /prompts/{prompt_id}`
- **Description**: Retrieve a prompt by its identifier.
- **Response Example**: 
  ```json
  {
    "id": "example_id",
    "title": "Sample Prompt"
  }
  ```
- **Error Responses**:
  - `404`: Prompt not found.

#### Create Prompt

- **Endpoint**: `POST /prompts`
- **Description**: Create a new prompt.
- **Request Example**:
  ```json
  {
    "title": "Sample Prompt",
    "collection_id": "1"
  }
  ```
- **Response Example**: 
  ```json
  {
    "id": "123",
    "title": "Sample Prompt"
  }
  ```
- **Error Responses**:
  - `400`: Collection not found.

#### Update Prompt

- **Endpoint**: `PUT /prompts/{prompt_id}`
- **Description**: Update an existing prompt by its ID.
- **Request Example**:
  ```json
  {
    "title": "Updated Title",
    "content": "Updated Content"
  }
  ```
- **Response Example**: 
  ```json
  {
    "id": "12345",
    "title": "Updated Title"
  }
  ```
- **Error Responses**:
  - `404`: Prompt not found.
  - `400`: Collection not found.

#### Partial Update Prompt

- **Endpoint**: `PATCH /prompts/{prompt_id}`
- **Description**: Update an existing prompt with the provided data.
- **Request Example**:
  ```json
  {
    "title": "New Title"
  }
  ```
- **Response Example**:
  ```json
  {
    "id": "1234",
    "title": "New Title"
  }
  ```
- **Error Responses**:
  - `404`: Prompt not found.
  - `400`: Collection not found.

#### Delete Prompt

- **Endpoint**: `DELETE /prompts/{prompt_id}`
- **Description**: Deletes a prompt with the specified ID.
- **Error Responses**:
  - `404`: Prompt not found.

### Collection Endpoints

#### List Collections

- **Endpoint**: `GET /collections`
- **Description**: Retrieve a list of all collections.
- **Response Example**:
  ```json
  {
    "collections": [
      {
        "id": "123",
        "name": "Sample Collection"
      }
    ],
    "total": 1
  }
  ```
- **Error Responses**: If an error occurs during retrieval, an internal server error is returned.

#### Get Collection

- **Endpoint**: `GET /collections/{collection_id}`
- **Description**: Retrieves a collection by its ID.
- **Response Example**:
  ```json
  {
    "id": "12345",
    "name": "Sample Collection"
  }
  ```
- **Error Responses**:
  - `404`: Collection not found.

#### Create Collection

- **Endpoint**: `POST /collections`
- **Description**: Creates a new collection.
- **Request Example**:
  ```json
  {
    "name": "New Collection"
  }
  ```
- **Response Example**:
  ```json
  {
    "id": "123",
    "name": "New Collection"
  }
  ```
- **Error Responses**: Validation errors if input data is incorrect.

#### Delete Collection

- **Endpoint**: `DELETE /collections/{collection_id}`
- **Description**: Deletes a collection and all its associated prompts.
- **Error Responses**:
  - `404`: Collection not found.
