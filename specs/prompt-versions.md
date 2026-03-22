**Prompt Versions Specification**
**Overview**

Prompt versioning enables tracking and managing changes made to a prompt over time. Each update to a prompt results in the creation of a new version, preserving the previous state.

This allows users to review historical changes, compare versions, and restore earlier states when needed.

The feature enhances reliability, traceability, and collaboration, especially as prompts evolve in iterative workflows.

**User Stories and Acceptance Criteria**

User Story 1: Automatically create versions on update

As a user, I want a new version to be created whenever a prompt is updated, so I can track changes over time.

Acceptance Criteria

A new version is created whenever a prompt is updated via PUT (and PATCH, when implemented).

The main prompt record always reflects the latest state.

The version history stores the previous state before the update.

Each version includes:

version number (incremental)

prompt_id

snapshot of title, content, description, collection_id

created_at timestamp

optional change summary (future enhancement)

User Story 2: View version history

As a user, I want to view all versions of a prompt so I can understand how it has evolved.

Acceptance Criteria

An endpoint exists to retrieve all versions for a given prompt.

Versions are returned in descending order (newest first).

Each version entry includes version number and timestamp.

If the prompt does not exist, return 404.

User Story 3: Retrieve a specific version

As a user, I want to view a specific version of a prompt so I can inspect its previous state.

Acceptance Criteria

An endpoint exists to retrieve a version by version number (or version_id).

If the requested version does not exist, return 404.

The response includes the complete snapshot of that version.

User Story 4: Restore a version as current

As a user, I want to restore an older version as the current prompt so I can revert unintended changes.

Acceptance Criteria

A restore endpoint is available.

Restoring a version:

Either creates a new version entry capturing the pre-restore state

Or explicitly records the restore action (must be defined and consistent)

After restoration:

The prompt reflects the restored version’s data

updated_at is refreshed

If prompt or version is not found, return 404.

**Data Model Changes Required**
Option A: Separate Version Model (Recommended)

Introduce a dedicated Pydantic model and storage structure:

PromptVersion

id: str

prompt_id: str

version: int

title: str

content: str

description: Optional[str]

collection_id: Optional[str]

created_at: datetime

Storage changes:

Add _prompt_versions: Dict[str, List[PromptVersion]], keyed by prompt_id

On each prompt update:

Create a version snapshot before applying changes

Append the snapshot to the corresponding version list

Notes

Version numbering starts at 1.

The active (current) prompt remains stored in the existing Prompt model.

Version entries represent immutable historical snapshots.

**API Endpoint Specifications**
List all versions for a prompt

GET /prompts/{prompt_id}/versions

Response (200)

Returns a list of version metadata.

Example response:

versions: [ { version, created_at }, ... ]

total: int

Errors:

404 if prompt not found

Get a specific version

GET /prompts/{prompt_id}/versions/{version}

Response (200)

Returns the full snapshot of the requested version.

Errors:

404 if prompt not found

404 if version not found

Restore a version

POST /prompts/{prompt_id}/versions/{version}/restore

Response (200)

Returns the updated current prompt after restoration.

Errors:

404 if prompt not found

404 if version not found

**Edge Cases to Handle**

Updating a non-existent prompt → return 404 (already handled)

Updating with identical data:

Either always create a version

Or skip version creation

Behavior must be explicitly defined and documented

Deleting prompts:

Decide whether versions should also be deleted (recommended: cascade delete)

No version history:

If a prompt has never been updated, return an empty list with 200

Concurrent updates:

Ensure version numbering remains consistent

For in-memory storage, enforce serialized updates

Collection deletion:

Historical versions may reference deleted collection_ids (acceptable, as versions represent past state)