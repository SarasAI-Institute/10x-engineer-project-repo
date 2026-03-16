"""Utility functions for PromptLab"""

from typing import List
from app.models import Prompt


# def sort_prompts_by_date(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
#     """Sort prompts by creation date.
    
#     Note: There might be a bug here. Check the sort order!
#     """
#     # BUG #3: This sorts ascending (oldest first) when it should sort descending (newest first)
#     # The 'descending' parameter is ignored!
#     return sorted(prompts, key=lambda p: p.created_at)

def sort_prompts_by_date(prompts: list[Prompt], descending: bool = False) -> list[Prompt]:
    """Sort prompts by their ``updated_at`` timestamp.

    Args:
        prompts (list[Prompt]): Collection of prompts to sort.
        descending (bool): Whether to place the newest prompts first. Defaults to False.

    Returns:
        list[Prompt]: Prompts ordered by ``updated_at``.

    Examples:
        >>> from datetime import datetime
        >>> prompts = [
        ...     Prompt(title="Older", updated_at=datetime(2023, 1, 1)),
        ...     Prompt(title="Newer", updated_at=datetime(2023, 6, 1)),
        ... ]
        >>> [p.title for p in sort_prompts_by_date(prompts, descending=True)]
        ['Newer', 'Older']
    """
    # ...existing code...
    # Ensure descending=True gives newest-first
    prompts_sorted = sorted(prompts, key=lambda p: p.updated_at, reverse=descending)
    return prompts_sorted

def filter_prompts_by_collection(prompts: List[Prompt], collection_id: str) -> List[Prompt]:
    """Return prompts that belong to the specified collection.

    Args:
        prompts (List[Prompt]): Prompts to inspect.
        collection_id (str): Identifier of the desired collection.

    Returns:
        List[Prompt]: Prompts whose ``collection_id`` matches ``collection_id``.

    Examples:
        >>> prompts = [
        ...     Prompt(title="Draft", collection_id="alpha"),
        ...     Prompt(title="Final", collection_id="beta"),
        ... ]
        >>> [p.title for p in filter_prompts_by_collection(prompts, "alpha")]
        ['Draft']
    """
    return [p for p in prompts if p.collection_id == collection_id]


def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
    """Search prompts by title or description, case-insensitively.

    Args:
        prompts (List[Prompt]): Prompts to search.
        query (str): Text to match against titles and descriptions.

    Returns:
        List[Prompt]: Prompts whose title or description contains ``query``.

    Examples:
        >>> prompts = [
        ...     Prompt(title="Greeting", description="Says hello"),
        ...     Prompt(title="Farewell", description="Says goodbye"),
        ... ]
        >>> [p.title for p in search_prompts(prompts, "hello")]
        ['Greeting']
    """
    query_lower = query.lower()
    return [
        p for p in prompts 
        if query_lower in p.title.lower() or 
           (p.description and query_lower in p.description.lower())
    ]


def validate_prompt_content(content: str) -> bool:
    """Validate that prompt content is non-empty, non-whitespace, and long enough.

    Args:
        content (str): Proposed prompt body.

    Returns:
        bool: True if the trimmed content is at least 10 characters, False otherwise.

    Examples:
        >>> validate_prompt_content("Hello world")
        True
        >>> validate_prompt_content("   too short ")
        False
    """
    if not content or not content.strip():
        return False
    return len(content.strip()) >= 10


def extract_variables(content: str) -> List[str]:
    """Extract template variables in ``{{variable_name}}`` format from prompt content.

    Args:
        content (str): Prompt text that may contain template placeholders.

    Returns:
        List[str]: All variable names found, in order of appearance.

    Examples:
        >>> extract_variables("Hello {{name}}, welcome to {{place}}!")
        ['name', 'place']
    """
    import re
    pattern = r'\{\{(\w+)\}\}'
    return re.findall(pattern, content)
