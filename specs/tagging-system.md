# PromptLab: Tagging System Feature Specification

## Overview

The Tagging System allows users to organize and categorize prompts using tags. 
This improves discoverability, enables filtering and searching, 
and helps structure large collections of prompts efficiently.

## Goals

- Provide a flexible and user-friendly method to categorize prompts.
- Improve searchability and filtering within the application.
- Support scalable tag management.
- Enable multi-tag assignment per prompt.

## Key Features

1. **Tag Creation**: Users can create new tags.
2. **Tag Assignment**: Users can assign one or multiple tags to a prompt.
3. **Tag Editing**: Users can rename or update existing tags.
4. **Tag Removal**: Users can remove tags from prompts.
5. **Tag Filtering/Search**: Users can filter prompts based on one or more tags.

## User Stories

### 1. Create Tag
As a user, I want to create a new tag to categorize prompts.

**Acceptance Criteria:**
- User can create a tag with a unique name.
- Duplicate tag names are prevented (case-insensitive).
- Tag name validation (min/max length).
- Tag is immediately available for assignment.

### 2. Assign Tag to Prompt
As a user, I want to assign one or more tags to a prompt.

**Acceptance Criteria:**
- A prompt can have multiple tags.
- A tag can belong to multiple prompts.
- Assignment is reflected immediately in UI.
- Duplicate assignments are prevented.

### 3. Edit Tag
As a user, I want to rename or modify an existing tag.

**Acceptance Criteria:**
- Tag name updates across all associated prompts.
- Renaming does not break associations.
- Duplicate names are not allowed.

### 4. Remove Tag from Prompt
As a user, I want to remove a tag from a specific prompt.

**Acceptance Criteria:**
- Removing a tag only affects the selected prompt.
- The tag entity remains if used elsewhere.
- If unused globally, optional auto-cleanup may occur.

### 5. Filter Prompts by Tag
As a user, I want to filter prompts using one or more tags.

**Acceptance Criteria:**
- Supports single-tag filtering.
- Supports multi-tag filtering (AND logic).
- Filtering is performant.
- Works with pagination and search.

## Data Model Changes

### Tag (New Table)

- id (UUID)
- name (string, unique)
- created_by (UUID)
- created_at (timestamp)
- updated_at (timestamp)

### PromptTag (Join Table)

- id (UUID)
- prompt_id (UUID, FK -> Prompt.id)
- tag_id (UUID, FK -> Tag.id)
- created_at (timestamp)

### Relationships

- Many-to-Many relationship between Prompt and Tag.
- Unique constraint on (prompt_id, tag_id).

### Indexing

- Index on tag.name
- Composite index on (prompt_id, tag_id)
- Index on tag_id for filtering performance

## API Endpoints

### POST /tags
Create a new tag.

Request:
{
  "name": "marketing"
}

Response:
{
  "id": "uuid",
  "name": "marketing"
}

### GET /tags
Retrieve all tags.

### PUT /tags/{tag_id}
Update a tag name.

Request:
{
  "name": "growth-marketing"
}

### DELETE /tags/{tag_id}
Delete a tag (if not restricted).

### POST /prompts/{prompt_id}/tags
Assign a tag to a prompt.

Request:
{
  "tag_id": "uuid"
}

### DELETE /prompts/{prompt_id}/tags/{tag_id}
Remove tag from a prompt.

### GET /prompts?tags=marketing,growth
Filter prompts by tags.

## Search & Filter Requirements

- Support filtering by multiple tags (AND logic).
- Support future OR logic enhancement.
- Combine tag filtering with:
  - Keyword search
  - Pagination
  - Sorting (created_at, updated_at)
- Filtering must be indexed and optimized.
- API response times under 200ms for typical dataset.

## Edge Cases to Handle

- Duplicate tag names (case-insensitive check).
- Renaming tag to an existing name.
- Deleting tag that is associated with prompts.
- Concurrent tag creation requests.
- Large number of tags (10k+).
- Special characters in tag names.
- Preventing orphaned join records.
- Permission control (who can create/edit/delete tags).

## Non-Functional Requirements

- Must support thousands of tags without performance degradation.
- Tag lookup should be indexed.
- Consistent behavior across UI and API.
- Audit logging for tag creation, update, and deletion.

