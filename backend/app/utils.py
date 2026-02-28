"""Utility functions for PromptLab"""

from typing import List
from app.models import Prompt


def sort_prompts_by_date(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
    """Sort prompts by creation date.

    Args:
        prompts: List of Prompt objects to sort.
        descending: When True (default) return newest-first; when False,
            return oldest-first.

    Returns:
        List[Prompt]: The sorted list of prompts.
    """
    # Respect the 'descending' parameter. If descending is True, newest prompts come first.
    return sorted(prompts, key=lambda p: p.created_at, reverse=descending)


def filter_prompts_by_collection(prompts: List[Prompt], collection_id: str) -> List[Prompt]:
    """Filter prompts by `collection_id`.

    Args:
        prompts: List of prompts to filter.
        collection_id: Collection ID to match.

    Returns:
        List[Prompt]: Prompts that belong to the requested collection.
    """
    return [p for p in prompts if p.collection_id == collection_id]


def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
    """Simple case-insensitive search over title and description.

    Args:
        prompts: Prompts to search.
        query: Text to search for.

    Returns:
        List[Prompt]: Prompts that match the query in title or description.
    """
    query_lower = query.lower()
    return [
        p for p in prompts 
        if query_lower in p.title.lower() or 
           (p.description and query_lower in p.description.lower())
    ]


def validate_prompt_content(content: str) -> bool:
    """Validate prompt text content.

    A valid prompt should not be empty, not be only whitespace, and be at
    least 10 characters long after trimming.

    Args:
        content: The prompt text to validate.

    Returns:
        bool: True when valid, False otherwise.
    """
    if not content or not content.strip():
        return False
    return len(content.strip()) >= 10


def extract_variables(content: str) -> List[str]:
    """Extract template variables from prompt content.

    Variables use the Handlebars-like `{{variable_name}}` syntax. This helper
    returns the list of variable names found in the content.

    Args:
        content: The prompt text to scan for variables.

    Returns:
        List[str]: Variable names found (may be empty).
    """
    import re
    pattern = r'\{\{(\w+)\}\}'
    return re.findall(pattern, content)
