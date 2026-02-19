# API Reference

This document provides an overview of the REST API endpoints available in the PromptLab application. Below is the detailed description of each endpoint, including HTTP methods, paths, parameters, request bodies, response formats, and error codes.

---

## Endpoints

### Health Check

**GET** `/health`

- **Description**: Perform a health check on the API.
- **Parameters**: None
- **Request Body**: None
- **Response Format**: 
  ```json
  {
    "status": "healthy",
    "version": "<api_version>"
  }
  ```
- **Error Codes**: None

---

### List Prompts

**GET** `/prompts`

- **Description**: List all prompts with optional filters.
- **Parameters**:
  - `collection_id` (Optional): Filter prompts by collection ID.
  - `search` (Optional): Search term to filter prompts by content.
- **Request Body**: None
- **Response Format**:
  ```json
  {
    "prompts": [<Prompt objects>],
    "total": <total_count>
  }
  ```
- **Error Codes**: None

---

### Get Prompt

**GET** `/prompts/{prompt_id}`

- **Description**: Retrieve a specific prompt by its ID.
- **Parameters**:
  - `prompt_id` (Path): The ID of the prompt to retrieve.
- **Request Body**: None
- **Response Format**:
  ```json
  <Prompt object>
  ```
- **Error Codes**:
  - `404`: Prompt not found.

---

### Create Prompt

**POST** `/prompts`

- **Description**: Create a new prompt with the provided data.
- **Parameters**: None
- **Request Body**:
  ```json
  {
    "title": "<title>",
    "content": "<content>",
    "description": "<description>",
    "collection_id": "<collection_id>"
  }
  ```
- **Response Format**:
  ```json
  <Prompt object>
  ```
- **Error Codes**:
  - `400`: Collection not found.

---

### Update Prompt

**PUT** `/prompts/{prompt_id}`

- **Description**: Update an existing prompt by ID with new data.
- **Parameters**:
  - `prompt_id` (Path): The ID of the prompt to update.
- **Request Body**:
  ```json
  {
    "title": "<title>",
    "content": "<content>",
    "description": "<description>",
    "collection_id": "<collection_id>"
  }
  ```
- **Response Format**:
  ```json
  <Prompt object>
  ```
- **Error Codes**:
  - `404`: Prompt not found.
  - `400`: Collection not found.

---

### Patch Prompt

**PATCH** `/prompts/{prompt_id}`

- **Description**: Partially update a prompt by ID with given data.
- **Parameters**:
  - `prompt_id` (Path): The ID of the prompt to update.
- **Request Body**:
  ```json
  {
    "title": "<title>",
    "content": "<content>",
    "description": "<description>",
    "collection_id": "<collection_id>"
  }
  ```
- **Response Format**:
  ```json
  <Prompt object>
  ```
- **Error Codes**:
  - `404`: Prompt not found.
  - `400`: Collection not found.

---

### Delete Prompt

**DELETE** `/prompts/{prompt_id}`

- **Description**: Delete a specific prompt by its ID.
- **Parameters**:
  - `prompt_id` (Path): The ID of the prompt to delete.
- **Request Body**: None
- **Response Format**: None
- **Error Codes**:
  - `404`: Prompt not found.

---

### List Collections

**GET** `/collections`

- **Description**: List all collections.
- **Parameters**: None
- **Request Body**: None
- **Response Format**:
  ```json
  {
    "collections": [<Collection objects>],
    "total": <total_count>
  }
  ```
- **Error Codes**: None

---

### Get Collection

**GET** `/collections/{collection_id}`

- **Description**: Retrieve a specific collection by its ID.
- **Parameters**:
  - `collection_id` (Path): The ID of the collection to retrieve.
- **Request Body**: None
- **Response Format**:
  ```json
  <Collection object>
  ```
- **Error Codes**:
  - `404`: Collection not found.

---

### Create Collection

**POST** `/collections`

- **Description**: Create a new collection with the provided data.
- **Parameters**: None
- **Request Body**:
  ```json
  {
    "name": "<name>",
    "description": "<description>"
  }
  ```
- **Response Format**:
  ```json
  <Collection object>
  ```
- **Error Codes**: None

---

### Delete Collection

**DELETE** `/collections/{collection_id}`

- **Description**: Delete a collection by its ID, handling associated prompts.
- **Parameters**:
  - `collection_id` (Path): The ID of the collection to delete.
- **Request Body**: None
- **Response Format**: None
- **Error Codes**:
  - `404`: Collection not found.
