# Tagging System (spec)

## Overview

Allow users to attach tags to prompts and filter/search by tags.

## User stories
- As a user I can add multiple tags to a prompt.
- As a user I can filter the prompt list by one or more tags.

## Data model changes
- Add `tags: List[str]` field to `Prompt` (default empty list).

## API endpoints
- PATCH/PUT/POST for creating/updating prompts support `tags` field.
- GET `/prompts?tags=tag1,tag2` - returns prompts that match any/all tags (specify semantics).

## Search/filter requirements
- Support both 'any' and 'all' matching modes (e.g., `tags_mode=any|all`).
