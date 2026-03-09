# Tagging System Specification

## Project Goals
- Enable prompts to be labeled with descriptive tags for faster discovery.
- Provide tag CRUD operations and allow filtering prompts by tag names.
- Keep the tagging system lightweight so it can plug into the existing storage layer without a database migration.

## User Stories
1. **As an engineer, I want to tag a prompt so it surfaces under relevant categories.**
   - **Given** a prompt exists
   - **When** I POST to `/prompts/{id}/tags` with a tag name
   - **Then** the prompt includes the tag in future responses and queries.

2. **As a user, I want to list prompts for a tag so I can focus on a topic.**
   - **Given** a tag exists
   - **When** I GET `/prompts?tag=review`
   - **Then** I receive prompts that include the `review` tag.

3. **As an admin, I want to manage the tag catalog so I can rename or retire tags cleanly.**
   - **Given** tags may evolve over time
   - **When** I PUT `/tags/{tag_id}` or DELETE `/tags/{tag_id}`
   - **Then** all prompt associations adjust accordingly (rename or removal).

## Data Model Changes
- Add `Tag` model:
  - `id`: uuid
  - `name`: string (unique, case-insensitive)
  - `description`: optional string
  - `created_at`: datetime

- Extend `Prompt` model with `tags: List[str]` (list of tag IDs or names depending on implementation) and `tags_details: Optional[List[Tag]]` for optional expansions.
- Storage updates:
  - `Storage._tags: Dict[str, Tag]`
  - Index prompts by tag for efficient reverse lookups (e.g., `Dict[str, Set[str]]`).

## API Endpoints
### Tag Catalog
- **GET `/tags`**: List all tags with metadata.
  - Response sample:
    ```json
    {
      "tags": [
        {"id": "tag-1", "name": "review", "description": "Code review prompts"}
      ],
      "total": 1
    }
    ```
- **POST `/tags`**
  - Request:
    ```json
    {"name": "review", "description": "Code review"}
    ```
  - Response (201) returns tag.
  - Error (400) if the tag name already exists.
- **PUT `/tags/{tag_id}`**
  - Request can rename the tag or update description.
  - All prompts referencing the tag should also update their tag entries to avoid stale references.
- **DELETE `/tags/{tag_id}`**
  - Removes the tag and unlinks it from every prompt (prompts keep remaining tags).
  - Returns 204 with no body.

### Prompt Tagging
- **POST `/prompts/{id}/tags`**
  - Request example:
    ```json
    {"tag_id": "tag-1"}
    ```
  - Response returns updated prompt with tag list.
  - Errors: 404 if prompt or tag missing, 400 if tag already assigned.
- **DELETE `/prompts/{id}/tags/{tag_id}`**
  - Removes a specific tag from the prompt; returns 204.

### Filtering by Tag
- Clients can call `GET /prompts?tag=review` (or `tag_id`) to limit results to prompts containing that tag.
- The query param is optional and combinable with `collection_id` and `search`.
- If the tag does not exist, returns an empty list rather than an error.

## Edge Cases
- **Duplicate tag names:** Names are case-insensitive; return 400 on duplicates.
- **Missing tags on deletion:** Deleting a tag should not prevent prompt responses; they simply lose that tag ID.
- **Nonexistent filters:** Filtering by a tag that does not exist returns an empty `prompts` array (200 OK).
- **Tag renames:** Renaming a tag should propagate to prompts for consistency.
- **Tag limits:** Consider limiting the number of tags per prompt (e.g., max 10) to avoid UI clutter.
