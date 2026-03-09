"""Utility functions for PromptLab"""

from typing import List
from app.models import Prompt


def sort_prompts_by_date(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
    """Order prompts by creation date.

    Args:
        prompts: List of prompts to sort.
        descending: Whether to order newest-first (default) or oldest-first.

    Returns:
        The prompts sorted by their creation timestamp.
    """
    return sorted(prompts, key=lambda p: p.created_at, reverse=descending)


def filter_prompts_by_collection(prompts: List[Prompt], collection_id: str) -> List[Prompt]:
    """Return prompts that are assigned to a specific collection.

    Args:
        prompts: List of prompts to filter.
        collection_id: Identifier of the collection to match.

    Returns:
        Prompts belonging to the requested collection.
    """
    return [p for p in prompts if p.collection_id == collection_id]


def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
    """Search prompts by title or description text.

    Args:
        prompts: Collection of prompts to search through.
        query: Case-insensitive search term.

    Returns:
        Prompts where the title or description contains the query.
    """
    query_lower = query.lower()
    return [
        p for p in prompts 
        if query_lower in p.title.lower() or 
           (p.description and query_lower in p.description.lower())
    ]


def validate_prompt_content(content: str) -> bool:
    """Determine if prompt content meets basic quality rules.

    Args:
        content: Raw prompt text to validate.

    Returns:
        True if content is non-empty, not whitespace, and at least 10 characters long.
    """
    if not content or not content.strip():
        return False
    return len(content.strip()) >= 10


def extract_variables(content: str) -> List[str]:
    """Extract template variable placeholders from prompt content.

    Args:
        content: Prompt body containing optional {{placeholders}}.

    Returns:
        List of variable names without curly braces.
    """
    import re
    pattern = r'\{\{(\w+)\}\}'
    return re.findall(pattern, content)
