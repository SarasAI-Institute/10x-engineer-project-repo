**PromptLab API Reference**

This document provides detailed documentation for the PromptLab REST API.

The API enables users to create, manage, search, and organize AI prompts into collections through a structured interface.

**Base URL**

When running locally:

http://localhost:8000

Authentication

The current version of the PromptLab API does not implement authentication.

All endpoints are publicly accessible.

Planned enhancements include:

API key-based authentication

User account support

Role-based access control (RBAC)

**Content Type**

All requests and responses are formatted in JSON.

Required request header:

Content-Type: application/json

Error Response Format

On failure, the API returns an appropriate HTTP status code along with a JSON response describing the error.

Example error response:

{
"detail": "Prompt not found"
}

Common status codes:

Status Code	Meaning
200	Request successful
201	Resource created successfully
204	Resource deleted successfully
400	Invalid request
404	Resource not found
422	Validation error


**Health Endpoint**
GET /health

Returns the current health status and version of the API.

Example request:

GET /health

Example response:

{
"status": "healthy",
"version": "1.0.0"
}

**Prompt Endpoints**

Prompts represent reusable templates used in AI-driven workflows.

Example Prompt Object:

{
"id": "123",
"title": "Summarize Text",
"content": "Summarize the following: {{input}}",
"description": "Summarizes text input",
"collection_id": "1",
"created_at": "2024-01-01T10:00:00",
"updated_at": "2024-01-01T10:00:00"
}

GET /prompts

Retrieve all prompts.

Supports optional filtering and search via query parameters (if implemented).

Example request:

GET /prompts

Example response:

{
"prompts": [
{
"id": "123",
"title": "Summarize Text",
"content": "Summarize the following: {{input}}",
"description": "Summarizes text input",
"collection_id": "1",
"created_at": "2024-01-01T10:00:00",
"updated_at": "2024-01-01T10:00:00"
}
],
"total": 1
}

GET /prompts/{prompt_id}

Retrieve a specific prompt by its unique ID.

Example request:

GET /prompts/123

Example response:

{
"id": "123",
"title": "Summarize Text",
"content": "Summarize the following: {{input}}",
"description": "Summarizes text input",
"collection_id": "1",
"created_at": "2024-01-01T10:00:00",
"updated_at": "2024-01-01T10:00:00"
}

Error example:

{
"detail": "Prompt not found"
}

POST /prompts

Create a new prompt.

Example request:

{
"title": "Translate Text",
"content": "Translate this text: {{input}}",
"description": "Translates input text",
"collection_id": "1"
}

Example response:

{
"id": "456",
"title": "Translate Text",
"content": "Translate this text: {{input}}",
"description": "Translates input text",
"collection_id": "1",
"created_at": "2024-01-01T11:00:00",
"updated_at": "2024-01-01T11:00:00"
}

Error example:

{
"detail": "Collection not found"
}

PUT /prompts/{prompt_id}

Update an existing prompt.

This operation replaces all fields of the prompt.

Example request:

{
"title": "Updated Prompt",
"content": "Updated prompt content",
"description": "Updated description",
"collection_id": "1"
}

Example response:

{
"id": "456",
"title": "Updated Prompt",
"content": "Updated prompt content",
"description": "Updated description",
"collection_id": "1",
"created_at": "2024-01-01T11:00:00",
"updated_at": "2024-01-01T12:00:00"
}

DELETE /prompts/{prompt_id}

Delete a prompt by ID.

Example request:

DELETE /prompts/456

Response:

204 No Content

Error example:

{
"detail": "Prompt not found"
}

**Collection Endpoints**

Collections are used to logically group related prompts.

Example Collection Object:

{
"id": "1",
"name": "General Prompts",
"description": "Common prompt templates",
"created_at": "2024-01-01T09:00:00"
}

GET /collections

Retrieve all collections.

Example request:

GET /collections

Example response:

{
"collections": [
{
"id": "1",
"name": "General Prompts",
"description": "Common prompt templates",
"created_at": "2024-01-01T09:00:00"
}
],
"total": 1
}

GET /collections/{collection_id}

Retrieve a specific collection by ID.

Example request:

GET /collections/1

Example response:

{
"id": "1",
"name": "General Prompts",
"description": "Common prompt templates",
"created_at": "2024-01-01T09:00:00"
}

Error example:

{
"detail": "Collection not found"
}

POST /collections

**Create a new collection.

Example request:

{
"name": "Marketing Prompts",
"description": "Prompts used for marketing workflows"
}

Example response:

{
"id": "2",
"name": "Marketing Prompts",
"description": "Prompts used for marketing workflows",
"created_at": "2024-01-01T13:00:00"
}

DELETE /collections/{collection_id}

Delete a collection by ID.

Example request:

DELETE /collections/2

Response:

204 No Content

Error example:

{
"detail": "Collection not found"
}