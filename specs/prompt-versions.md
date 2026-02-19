# Prompt Version Tracking Specification

## Overview

Prompt version tracking is a feature that allows users to maintain and access historical versions of a prompt. It enables users to track changes, roll back to previous versions, and understand the evolution of the prompt content over time. This feature will introduce a versioning system that assigns unique identifiers to each prompt version, storing metadata about the changes and allowing easy access and management through the API.

## User Stories

1. **Viewing Prompt History**
   - **As a user**, I want to view the history of a prompt, so that I can see all previous versions and changes.
   - **Acceptance Criteria**:
     - Users can request the history of a specific prompt.
     - The response contains a list of all versions with metadata, including version ID, timestamp, and author.
     - If no history is available, return an empty list.

2. **Reverting to a Previous Version**
   - **As a user**, I want to revert a prompt to a specific previous version, so that I can roll back changes if needed.
   - **Acceptance Criteria**:
     - Users can specify a version ID to revert to.
     - The prompt contents are updated to match the specified version.
     - Confirmation of the successful revert is provided.
     - If the version ID does not exist, return an error message.

3. **Updating a Prompt and Creating a New Version**
   - **As a user**, I want a new version to be created every time a prompt is updated, so that the previous states are not lost.
   - **Acceptance Criteria**:
     - A new version is created upon every update with a unique version ID.
     - The updated prompt content and metadata are saved.
     - The new version is recorded in the prompt's history.

4. **Deleting a Prompt Version**
   - **As a user**, I want the ability to delete specific prompt versions, so that I can manage and clean up unnecessary versions.
   - **Acceptance Criteria**:
     - Users can delete a version by providing a version ID.
     - The version is removed from history without affecting other versions.
     - A confirmation message is returned upon successful deletion.
     - Prevent deletion of the current/active version.

## Data Model Changes

The existing Pydantic models will be updated to include version tracking fields.

```python
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class PromptVersion(BaseModel):
    version_id: str
    content: str
    timestamp: datetime
    author: Optional[str]

class Prompt(BaseModel):
    id: str
    current_content: str
    versions: List[PromptVersion] = Field(default_factory=list)

class CreatePromptRequest(BaseModel):
    content: str
    author: Optional[str]

class UpdatePromptRequest(BaseModel):
    prompt_id: str
    new_content: str
    author: Optional[str]

class RevertPromptRequest(BaseModel):
    prompt_id: str
    version_id: str

class DeleteVersionRequest(BaseModel):
    prompt_id: str
    version_id: str
```

## New API Endpoints

1. **Get Prompt History**

   - **Method**: GET
   - **Path**: `/prompts/{prompt_id}/history`
   - **Response Example**:

     ```json
     [
       {
         "version_id": "v1",
         "content": "First version",
         "timestamp": "2023-01-01T12:00:00",
         "author": "user1"
       },
       {
         "version_id": "v2",
         "content": "Second version",
         "timestamp": "2023-01-02T12:00:00",
         "author": "user2"
       }
     ]
     ```

2. **Revert Prompt to Previous Version**

   - **Method**: POST
   - **Path**: `/prompts/revert`
   - **Request Example**:

     ```json
     {
       "prompt_id": "123",
       "version_id": "v1"
     }
     ```

   - **Response Example**:

     ```json
     {
       "message": "Prompt successfully reverted to version v1."
     }
     ```

3. **Update Prompt**

   - **Method**: PUT
   - **Path**: `/prompts`
   - **Request Example**:

     ```json
     {
       "prompt_id": "123",
       "new_content": "Updated prompt content",
       "author": "user1"
     }
     ```

   - **Response Example**:

     ```json
     {
       "version_id": "v3",
       "message": "New version created successfully."
     }
     ```

4. **Delete Prompt Version**

   - **Method**: DELETE
   - **Path**: `/prompts/{prompt_id}/versions/{version_id}`
   - **Response Example**:

     ```json
     {
       "message": "Version v2 successfully deleted."
     }
     ```

## Edge Cases

| Scenario                              | Handling                                                  |
|---------------------------------------|-----------------------------------------------------------|
| Attempting to view history of a non-existent prompt | Return a 404 Not Found error with an appropriate message. |
| Reverting to a non-existent version   | Return a 404 Not Found error indicating the version does not exist. |
| Attempting to delete the current version | Return a 400 Bad Request for invalid operation.           |
| Creating a new version with identical content to the last version | Allow operation, but ensure a new version ID is created to preserve update metadata. |