# API Documentation

## Health Check Endpoint

### GET /health
- **Description**: Checks the health status of the API.
- **Parameters**: None
- **Response Format**: Application status and version in JSON format.
- **Error Codes**: None

## Prompt Endpoints

### GET /prompts
- **Description**: Retrieves a list of prompts.
- **Parameters**:
  - `collection_id` (Optional): Filter prompts by collection ID.
  - `search` (Optional): Search query for filtering prompts.
- **Response Format**: A JSON object containing the prompts and total count.
- **Error Codes**: None

### GET /prompts/{prompt_id}
- **Description**: Retrieve a specific prompt by ID.
- **Parameters**:
  - `prompt_id`: The ID of the prompt to retrieve.
- **Response Format**: A JSON object representing the prompt.
- **Error Codes**:
  - 404: Prompt not found

### POST /prompts
- **Description**: Create a new prompt.
- **Request Body**: JSON object of `PromptCreate` containing:
  - `title`, `content`, `description`, `collection_id` (Optional)
- **Response Format**: The created prompt in JSON format.
- **Error Codes**:
  - 400: Collection not found
  - 422: Unprocessable Entity for invalid data

### PUT /prompts/{prompt_id}
- **Description**: Update an existing prompt.
- **Parameters**:
  - `prompt_id`: The ID of the prompt to update.
- **Request Body**: JSON object of `PromptUpdate` containing:
  - `title`, `content`, `description`, `collection_id` (Optional)
- **Response Format**: The updated prompt in JSON format.
- **Error Codes**:
  - 404: Prompt not found
  - 400: Collection not found

### PATCH /prompts/{prompt_id}
- **Description**: Partially update an existing prompt.
- **Parameters**:
  - `prompt_id`: The ID of the prompt to update.
- **Request Body**: JSON object of `PromptUpdate` with fields to update.
- **Response Format**: The updated prompt in JSON format.
- **Error Codes**:
  - 404: Prompt not found

### DELETE /prompts/{prompt_id}
- **Description**: Delete a specific prompt by ID.
- **Parameters**:
  - `prompt_id`: The ID of the prompt to delete.
- **Response Format**: No content.
- **Error Codes**:
  - 404: Prompt not found

## Collection Endpoints

### GET /collections
- **Description**: Retrieves a list of collections.
- **Parameters**: None
- **Response Format**: A JSON object containing collections and total count.
- **Error Codes**: None

### GET /collections/{collection_id}
- **Description**: Retrieve a specific collection by ID.
- **Parameters**:
  - `collection_id`: The ID of the collection to retrieve.
- **Response Format**: A JSON object representing the collection.
- **Error Codes**:
  - 404: Collection not found

### POST /collections
- **Description**: Create a new collection.
- **Request Body**: JSON object of `CollectionCreate` containing:
  - `name`, `description`
- **Response Format**: The created collection in JSON format.
- **Error Codes**: None

### DELETE /collections/{collection_id}
- **Description**: Delete a collection and orphan its prompts.
- **Parameters**:
  - `collection_id`: The ID of the collection to delete.
- **Response Format**: No content.
- **Error Codes**:
  - 404: Collection not found
