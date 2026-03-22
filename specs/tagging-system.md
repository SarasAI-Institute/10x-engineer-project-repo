**Tagging System Specification** 

**Overview**

The tagging system enables users to assign labels to prompts for better organization, discovery, and filtering. Tags are lightweight identifiers such as "marketing", "summarization", or "customer-support".

This feature allows teams to quickly locate prompts based on categories, use cases, or custom groupings, improving usability as the number of prompts grows.

**User Stories and Acceptance Criteria**

User Story 1: Add tags to a prompt

As a user, I want to assign tags to a prompt so I can categorize it effectively.

Acceptance Criteria

Prompt creation and update operations support a list of tags.

Tags are persisted and returned in the prompt response.

Duplicate tags are automatically removed (case-insensitive).

Tag length is validated (e.g., 1–30 characters).

Tags are normalized (e.g., trimmed and lowercased).

User Story 2: Remove tags from a prompt

As a user, I want to remove tags from a prompt so I can keep classifications accurate.

Acceptance Criteria

Tags can be removed by updating the prompt with a new tags list.

The response reflects the updated set of tags.

User Story 3: List prompts by tag

As a user, I want to filter prompts by tag so I can quickly find relevant prompts.

Acceptance Criteria

GET /prompts supports filtering via a tag query parameter.

Only prompts containing the specified tag are returned.

If no prompts match the tag, return an empty list with total=0 (200).

User Story 4: List all available tags

As a user, I want to view all tags used in the system so I can maintain consistency.

Acceptance Criteria

A new endpoint returns all distinct tags.

Tags are returned in sorted order.

Total count is included in the response.

**Data Model Changes Needed**

Update Prompt models to include tags.

PromptBase changes

Add:

tags: List[str] = Field(default_factory=list)

Rules:

Tags must be a list of strings

Each tag should be trimmed and normalized to lowercase

Maximum tags per prompt (e.g., 20)

Maximum tag length (e.g., 30 characters)

Storage changes:

Existing in-memory Prompt objects can store tags directly; no new top-level model is required.

Optionally introduce a tag index for faster lookups:

_tag_index: Dict[str, List[str]] where key is tag and value is a list of prompt_ids

**API Endpoint Specifications**

Add/Update tags (via existing prompt endpoints)

POST /prompts (include tags)

PUT /prompts/{prompt_id} (include tags)

Example request body:

tags: ["summarization", "marketing"]

Errors:

422 for invalid tag schema (e.g., non-string values, excessive length)

Filter prompts by tag

GET /prompts?tag={tag_name}

Response (200)

PromptList response (prompts and total count)

Behavior:

Matching should be case-insensitive

Tags must match exactly after normalization

List all tags

GET /tags

Response (200)

tags: List[str]

total: int

**Search and Filter Requirements**

Enhance GET /prompts to support combined filtering:

collection_id (optional)

search (optional)

tag (optional)

Rules:

Filters are applied using AND logic:

Example: collection_id=1 AND tag=marketing AND search=summarize

Results should be sorted by most recently updated (updated_at descending)

**Edge Cases to Handle (Recommended)**

Tags with spaces:

Decide whether to allow multi-word tags ("customer support") or enforce a format like "customer-support"

Case sensitivity:

Normalize all tags to lowercase to ensure consistency

Duplicate tags in input:

Remove duplicates automatically

Empty tag list:

Allowed; represents no tags assigned

Large datasets:

Consider implementing a tag index for efficient filtering (optional)