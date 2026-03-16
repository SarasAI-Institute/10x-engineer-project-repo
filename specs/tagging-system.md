# Tagging System Feature Specification

## 1. Plain-Language Overview
- Tags are short labels like `database`, `sev-1`, or `customer-impact`.
- A prompt can have up to ten tags, and each tag can live on many prompts.
- Tags make search, filtering, and reporting easier without forcing more collections.

## 2. User Stories and What “Done” Means
1. **Add tags while editing prompts (TG-1).**
   - POST/PUT/PATCH accept `tags: List[str]`.
   - We trim whitespace, lowercase the value, and drop duplicates before storing.
   - Empty tags or tags over 30 characters return a 422 error.
2. **See every tag in the system (TG-2).**
   - `GET /tags` lists each unique tag plus how many prompts use it.
   - List is sorted alphabetically so people can scan it fast.
3. **Filter prompts by tag (TG-3).**
   - `GET /prompts?tags=database,sev-1` only returns prompts that include *all* requested tags.
   - Tag filters must work alongside `collection_id` and `search` filters.
4. **Remove stale tags everywhere (TG-4).**
   - `DELETE /tags/{tag_name}` strips that tag from every prompt.
   - If the tag does not exist we send 404.
5. **Prevent accidental duplicates (TG-5).**
   - Input like `" Database "` becomes `"database"`.
   - Re-sending an existing tag list keeps only the unique values.

## 3. Data Model Changes
- **Prompt models:** add `tags: List[str] = []` to `Prompt`, `PromptCreate`, `PromptUpdate`, and `PromptPatch`.
- **Validators:** shared validator ensures each tag is 1–30 chars, only letters/numbers/hyphen/underscore, and no prompt has more than ten tags.
- **Derived tag list:** we can compute the global tag catalog by scanning prompts; no new table is required right now.

## 4. API Changes
- **Prompt create/update:** payloads already described above now include optional `tags`.
- **List tags:** `GET /tags` → `{ tags: [ { name, usage_count } ], total }`.
- **Delete tag:** `DELETE /tags/{tag_name}` → `{ tag, removed_from }` after removing the normalized tag from each prompt.
- **Filter prompts:** `GET /prompts?tags=foo,bar` uses AND logic and can combine with other query params.

## 5. Search and Filter Behavior
- Parse the `tags` query value by splitting on commas, trimming spaces, lowercasing, then deduplicating before filtering.
- Current release only supports AND logic (prompt must contain every requested tag). Document a possible future `tag_match=any` flag for OR behavior.
- If prompt pagination is added later, tag filters must work with it.
- Text search (`search` param) still runs and the final result set must satisfy both the text query and the tag filters.

## 6. Edge Cases to Cover
- Sending an empty `tags` list clears all tags from the prompt.
- More than ten tags or invalid characters return 422 with a clear error message.
- Reject tags with spaces or emoji so URLs stay clean (only letters, numbers, `-`, `_`).
- Deleting a popular tag should still be fast—consider batching writes inside the storage layer.
- Normalize and deduplicate tags server-side to avoid race conditions during concurrent updates.
- Older prompts without tags should continue working; they just return `tags: []` in every response.
