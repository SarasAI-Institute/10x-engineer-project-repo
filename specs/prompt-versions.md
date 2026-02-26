# PromptLab: Prompt Versions Feature Specification

## Overview

The Prompt Versions feature allows users to manage different iterations of prompts. 
This helps in tracking changes, reverting to previous versions when needed, 
and experimenting with new prompt ideas without losing previous work.

## Goals

- Enable version control for prompts.
- Allow users to revert to previous versions of a prompt.
- Provide a history view of changes made to prompts.
- Ensure prompt data integrity and auditability.

## Key Features

1. **Version Creation**: Automatically create a new version each time a prompt is saved.
2. **Version Retrieval**: Retrieve any previous version of a prompt for viewing.
3. **Version Comparison**: Compare changes between different versions of a prompt.
4. **Version Reversion**: Restore a prompt to any selected previous version.
5. **Change Summary Support**: Allow users to optionally describe changes.

## User Stories

### 1. Automatic Versioning
As a user, when I update a prompt and save it, a new version should be created automatically.

**Acceptance Criteria:**
- Saving updates creates a new version entry.
- Version numbers increment sequentially (v1, v2, v3…).
- Previous versions remain unchanged.
- Metadata (author, timestamp) is stored.

### 2. View Version History
As a user, I want to view all past versions of a prompt.

**Acceptance Criteria:**
- Versions are displayed in descending order (latest first).
- Each version shows:
  - Version number
  - Author
  - Timestamp
  - Change summary (if available)
- Pagination is supported.

### 3. Compare Versions
As a user, I want to compare two versions to see differences.

**Acceptance Criteria:**
- User can select any two versions.
- System displays structured diff (added, removed, modified content).
- Works efficiently for large prompts.

### 4. Restore Previous Version
As a user, I want to restore an older version of a prompt.

**Acceptance Criteria:**
- Restoring creates a new version entry.
- History remains intact.
- Confirmation is required before restore.

## Data Model Changes

### Prompt (Updated)

- id (UUID)
- title (string)
- current_version_id (UUID)
- created_at (timestamp)
- updated_at (timestamp)
- created_by (UUID)

### PromptVersion (New Table)

- id (UUID)
- prompt_id (UUID, FK -> Prompt.id)
- version_number (integer)
- content (text)
- metadata (json)
- change_summary (text, optional)
- created_by (UUID)
- created_at (timestamp)

### Constraints

- version_number must be unique per prompt.
- Historical versions are immutable.
- Composite index on (prompt_id, version_number).

## API Endpoints

### GET /prompts/{prompt_id}/versions
Retrieve all versions of a prompt.

### GET /prompts/{prompt_id}/versions/{version_number}
Retrieve a specific version.

### PUT /prompts/{prompt_id}
Update prompt and automatically create new version.

Request:
{
  "title": "Updated Title",
  "content": "Updated content",
  "change_summary": "Refined instructions"
}

### GET /prompts/{prompt_id}/compare?from=1&to=3
Compare two versions.

### POST /prompts/{prompt_id}/versions/revert
Revert to a specific version.

Request:
{
  "version_number": 2
}

## Edge Cases to Handle

- Concurrent edits (use optimistic locking).
- Duplicate version numbers during parallel saves.
- Very large prompt content (efficient diff handling).
- Soft deletion of prompts while keeping version history.
- Permission restrictions (view vs edit vs restore).
- Restoring while another update is in progress.
- Metadata schema changes over time.

## Non-Functional Requirements

- Version creation should complete within 200ms for normal prompt size.
- Must support at least 1,000 versions per prompt.
- Ensure audit logging for compliance.
- Scalable storage for version history.

