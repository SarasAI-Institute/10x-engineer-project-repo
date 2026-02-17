# API Reference

This document provides details on all API endpoints available in the `api.py` module for the PromptLab application. Each endpoint is described with its HTTP method, path, description, parameters, request body, response format, and possible error codes.

## Endpoints

### Health Check

- **Method**: `GET`
- **Path**: `/health`
- **Description**: Checks the health status of the API and provides the current version of the application.
- **Parameters**: None
- **Request Body**: None
- **Response Format**:
  - **200 OK**: `{'status': 'healthy', 'version': '1.0.0'}`
- **Error Codes**: None

### List Prompts

- **Method**: `GET`
- **Path**: `/prompts`
- **Description**: Retrieves a list of prompts, optionally filtered by collection or search query.
- **Parameters**:
  - `collection_id` (query, optional, `str`): ID of the collection to filter prompts.
  - `search` (query, optional, `str`): Search query to filter prompts by title or content.
- **Request Body**: None
- **Response Format**:
  - **200 OK**: `{ 'prompts': [...], 'total': number }`
- **Error Codes**: None

### Get Prompt

- **Method**: `GET`
- **Path**: `/prompts/{prompt_id}`
- **Description**: Retrieves a specific prompt by its unique identifier.
- **Parameters**:
  - `prompt_id` (path, `str`): The unique identifier of the prompt.
- **Request Body**: None
- **Response Format**:
  - **200 OK**: `{ 'id': '...', 'title': '...', 'content': '...', ... }`
  - **404 Not Found**: `{'detail': 'Prompt not found'}`

### Create Prompt

- **Method**: `POST`
- **Path**: `/prompts`
- **Description**: Creates a new prompt.
- **Parameters**: None
- **Request Body**:
  - **Required Fields**:
    - `title` (`str`): Title of the prompt.
    - `content` (`str`): Content of the prompt.
  - **Optional Fields**:
    - `description` (`str`): Description of the prompt.
    - `collection_id` (`str`): Collection ID to which the prompt belongs.
- **Response Format**:
  - **201 Created**: `{ 'id': '...', 'title': '...', 'content': '...', ... }`
  - **400 Bad Request**: `{'detail': 'Collection not found'}`

### Update Prompt

- **Method**: `PUT`
- **Path**: `/prompts/{prompt_id}`
- **Description**: Updates an existing prompt by its unique identifier.
- **Parameters**:
  - `prompt_id` (path, `str`): The unique identifier of the prompt.
- **Request Body**:
  - **Optional Fields for Update**:
    - `title` (`str`): New title of the prompt.
    - `content` (`str`): New content of the prompt.
    - `description` (`str`): New description of the prompt.
    - `collection_id` (`str`): New collection ID for the prompt.
- **Response Format**:
  - **200 OK**: `{ 'id': '...', 'title': '...', 'content': '...', ... }`
  - **400 Bad Request**: `{'detail': 'Collection not found'}`
  - **404 Not Found**: `{'detail': 'Prompt not found'}`

### Patch Prompt

- **Method**: `PATCH`
- **Path**: `/prompts/{prompt_id}`
- **Description**: Partially updates an existing prompt.
- **Parameters**:
  - `prompt_id` (path, `str`): The unique identifier of the prompt.
- **Request Body**:
  - **Fields for Partial Update**:
    - `title` (`str`): New title of the prompt.
    - `content` (`str`): New content of the prompt.
    - `description` (`str`): New description of the prompt.
    - `collection_id` (`str`): New collection ID for the prompt.
- **Response Format**:
  - **200 OK**: `{ 'id': '...', 'title': '...', 'content': '...', ... }`
  - **400 Bad Request**: `{'detail': 'Collection not found'}`
  - **404 Not Found**: `{'detail': 'Prompt not found'}`

### Delete Prompt

- **Method**: `DELETE`
- **Path**: `/prompts/{prompt_id}`
- **Description**: Deletes a prompt by its unique identifier.
- **Parameters**:
  - `prompt_id` (path, `str`): The unique identifier of the prompt.
- **Request Body**: None
- **Response Format**:
  - **204 No Content**: Successful deletion with no response body.
  - **404 Not Found**: `{'detail': 'Prompt not found'}`

### List Collections

- **Method**: `GET`
- **Path**: `/collections`
- **Description**: Retrieves a list of all collections.
- **Parameters**: None
- **Request Body**: None
- **Response Format**:
  - **200 OK**: `{ 'collections': [...], 'total': number }`
- **Error Codes**: None

### Get Collection

- **Method**: `GET`
- **Path**: `/collections/{collection_id}`
- **Description**: Retrieves a specific collection by its unique identifier.
- **Parameters**:
  - `collection_id` (path, `str`): The unique identifier of the collection.
- **Request Body**: None
- **Response Format**:
  - **200 OK**: `{ 'id': '...', 'name': '...', 'description': '...', ... }`
  - **404 Not Found**: `{'detail': 'Collection not found'}`

### Create Collection

- **Method**: `POST`
- **Path**: `/collections`
- **Description**: Creates a new collection.
- **Parameters**: None
- **Request Body**:
  - **Required Fields**:
    - `name` (`str`): Name of the collection.
  - **Optional Fields**:
    - `description` (`str`): Description of the collection.
- **Response Format**:
  - **201 Created**: `{ 'id': '...', 'name': '...', 'description': '...', ... }`

### Delete Collection

- **Method**: `DELETE`
- **Path**: `/collections/{collection_id}`
- **Description**: Deletes a collection by its unique identifier.
- **Parameters**:
  - `collection_id` (path, `str`): The unique identifier of the collection.
- **Request Body**: None
- **Response Format**:
  - **204 No Content**: Successful deletion with no response body.
  - **404 Not Found**: `{'detail': 'Collection not found'}`
