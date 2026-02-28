# Guide to PromptLab Project

## Overview

PromptLab is an AI Prompt Engineering Platform designed to manage AI prompts and collections. This guide provides a comprehensive overview of the main components of the application, including the API routes, data models, storage mechanism, and utility functions.

## Contents
- FastAPI Application and Routes (app/api.py)
- Data Models (app/models.py)
- In-Memory Storage (app/storage.py)
- Utility Functions (app/utils.py)

## FastAPI Application and Routes (app/api.py)

The FastAPI application is defined in this module. It includes various endpoints for managing prompts and collections, alongside a health check endpoint.

### Health Check Endpoint
- **Route:** `/health`
- **Method:** `GET`
- **Response:** `HealthResponse`
- **Details:** Returns the health status and version of the API.

### Prompt Endpoints
- **List Prompts**
  - **Route:** `/prompts`
  - **Method:** `GET`
  - **Response:** `PromptList`
  - **Parameters:** `collection_id` (optional), `search` (optional)
  - **Details:** Retrieves all prompts, optionally filtering by collection and/or search query.

- **Get Prompt by ID**
  - **Route:** `/prompts/{prompt_id}`
  - **Method:** `GET`
  - **Response:** `Prompt`
  - **Details:** Retrieves a specific prompt by its ID. Raises 404 error if not found.
  - **Bug Fix:** Handle non-existent prompts by checking if `prompt.id` exists.

- **Create Prompt**
  - **Route:** `/prompts`
  - **Method:** `POST`
  - **Response:** `Prompt`
  - **Status Code:** 201
  - **Details:** Creates a new prompt. Validates collection existence if provided.

- **Update Prompt**
  - **Route:** `/prompts/{prompt_id}`
  - **Method:** `PUT`
  - **Response:** `Prompt`
  - **Details:** Updates an existing prompt. Validates collection existence. Updates `updated_at` timestamp.

- **Delete Prompt**
  - **Route:** `/prompts/{prompt_id}`
  - **Method:** `DELETE`
  - **Status Code:** 204
  - **Details:** Deletes a specific prompt, with validation.

### Collection Endpoints
- **List Collections**
  - **Route:** `/collections`
  - **Method:** `GET`
  - **Response:** `CollectionList`
  - **Details:** Retrieves all collections.

- **Get Collection by ID**
  - **Route:** `/collections/{collection_id}`
  - **Method:** `GET`
  - **Response:** `Collection`
  - **Details:** Retrieves a specific collection by its ID. Raises 404 error if not found.

- **Create Collection**
  - **Route:** `/collections`
  - **Method:** `POST`
  - **Response:** `Collection`
  - **Status Code:** 201
  - **Details:** Creates a new collection.

- **Delete Collection**
  - **Route:** `/collections/{collection_id}`
  - **Method:** `DELETE`
  - **Status Code:** 204
  - **Details:** Deletes a specific collection. Prompts under this collection need handling to avoid orphaning.

## Data Models (app/models.py)

This module defines the Pydantic models used throughout PromptLab. It distinguishes between prompts and collections, each with create, update, and base classes.

### Prompt Models
- **PromptBase:** Contains shared fields for prompts, including title, content, description, and collection ID.
- **Prompt:** Extends `PromptBase` with an ID, creation, and update timestamps.

### Collection Models
- **CollectionBase:** Contains fields for collections, including name and description.
- **Collection:** Includes an ID and creation timestamp.

### Response Models
- **PromptList** and **CollectionList** hold lists of prompts and collections, respectively, with total counts.
- **HealthResponse** provides the API health status and version.

## In-Memory Storage (app/storage.py)

A simple in-memory storage mechanism simulating a database for storing prompts and collections.

### Methods
- **create_prompt** / **create_collection**: Adds a prompt or collection to storage.
- **get_prompt** / **get_collection**: Retrieves an item by ID.
- **get_all_prompts** / **get_all_collections**: Retrieves all items as lists.
- **update_prompt**: Updates a prompt in storage.
- **delete_prompt** / **delete_collection**: Removes an item by ID.
- **get_prompts_by_collection**: Retrieves prompts under a specific collection.
- **clear**: Clears all data from storage.

## Utility Functions (app/utils.py)

Helper functions facilitating the functionality within PromptLab.

### Main Functions
- **sort_prompts_by_date**: Sorts a list of prompts by date. Known issue: Sorts in ascending order by default.
- **filter_prompts_by_collection**: Filters prompts by a given collection ID.
- **search_prompts**: Searches prompts based on a query string.
- **validate_prompt_content**: Ensures prompt content meets specified criteria.
- **extract_variables**: Parses and extracts template variables from prompt content.

---

This guide serves to aid developers and users of PromptLab in understanding its structure and functionalities. For further details, refer to the specific files in the project.