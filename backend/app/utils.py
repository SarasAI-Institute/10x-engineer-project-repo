"""Utility functions for PromptLab.

Provides helper functions for sorting, filtering, searching,
validation, and template parsing.
"""

from typing import List
from app.models import Prompt


def sort_prompts_by_date(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
    """
    Sort prompts by creation timestamp.

    Args:
        prompts (List[Prompt]): List of prompt objects.
        descending (bool): If True, sorts newest first. If False, oldest first.

    Returns:
        List[Prompt]: Sorted list of prompts.

    Example:
        >>> sort_prompts_by_date(prompts, descending=True)
        [Prompt(created_at=2025-01-01), Prompt(created_at=2024-01-01)]
    """
    return sorted(prompts, key=lambda p: p.created_at, reverse=descending)


def filter_prompts_by_collection(prompts: List[Prompt], collection_id: str) -> List[Prompt]:
    """
    Filter prompts belonging to a specific collection.

    Args:
        prompts (List[Prompt]): List of prompt objects.
        collection_id (str): Collection identifier.

    Returns:
        List[Prompt]: Prompts that belong to the given collection.

    Example:
        >>> filter_prompts_by_collection(prompts, "col-123")
        [Prompt(...), Prompt(...)]
    """
    return [p for p in prompts if p.collection_id == collection_id]


def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
    """
    Search prompts by title or description.

    Performs a case-insensitive match.

    Args:
        prompts (List[Prompt]): List of prompt objects.
        query (str): Search keyword.

    Returns:
        List[Prompt]: Prompts matching the search query.

    Example:
        >>> search_prompts(prompts, "summarize")
        [Prompt(title="Summarize Text", ...)]
    """
    query_lower = query.lower()
    return [
        p for p in prompts 
        if query_lower in p.title.lower() or 
           (p.description and query_lower in p.description.lower())
    ]


def validate_prompt_content(content: str) -> bool:
    """
    Validate prompt content.

    A valid prompt must:
    - Not be empty
    - Not contain only whitespace
    - Be at least 10 characters long

    Args:
        content (str): Prompt content.

    Returns:
        bool: True if valid, False otherwise.

    Example:
        >>> validate_prompt_content("Summarize this text")
        True

        >>> validate_prompt_content("   ")
        False
    """
    if not content or not content.strip():
        return False
    return len(content.strip()) >= 10


def extract_variables(content: str) -> List[str]:
    """
    Extract template variables from prompt content.

    Variables must follow the format: {{variable_name}}

    Args:
        content (str): Prompt content containing template variables.

    Returns:
        List[str]: List of extracted variable names.

    Example:
        >>> extract_variables("Summarize {{text}} for {{audience}}")
        ["text", "audience"]
    """
    import re
    pattern = r'\{\{(\w+)\}\}'
    return re.findall(pattern, content)
def normalize_tags(tags: list[str]) -> list[str]:
    """
    Normalize tags:
    - lowercase
    - trim whitespace
    - remove duplicates
    """
    cleaned = []

    for tag in tags:
        t = tag.strip().lower()
        if t and t not in cleaned:
            cleaned.append(t)

    return cleaned