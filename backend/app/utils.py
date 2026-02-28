"""Utility functions for PromptLab"""

from typing import List
from app.models import Prompt


def sort_prompts_by_date(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
    """Sort a list of prompts by their creation date.

    Sorts the given list of prompts based on their creation date, either
    in descending (newest first) or ascending (oldest first) order.

    Args:
        prompts (List[Prompt]): The list of prompts to sort.
        descending (bool): Determines the sort order. If True, sorts by date descending.
                           If False, sorts by date ascending. Default is True.

    Returns:
        List[Prompt]: A list of prompts sorted by creation date.

    Note:
        There was a known issue where the 'descending' parameter was ignored, 
        which has been fixed.

    Example Usage:
        >>> sorted_prompts = sort_prompts_by_date(prompts)
    """
    return sorted(prompts, key=lambda p: p.created_at, reverse=descending)


def filter_prompts_by_collection(prompts: List[Prompt], collection_id: str) -> List[Prompt]:
    """Filter prompts by a specific collection ID.

    Filters the provided list of prompts to return only those belonging to the
    specified collection.

    Args:
        prompts (List[Prompt]): The list of prompts to filter.
        collection_id (str): The collection ID to filter prompts by.

    Returns:
        List[Prompt]: A list of prompts that belong to the given collection ID.

    Example Usage:
        >>> filtered_prompts = filter_prompts_by_collection(prompts, "col123")
    """
    return [p for p in prompts if p.collection_id == collection_id]


def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
    """Search for prompts containing a specific query.

    Searches through the list of prompts to find any that contain the query
    in their title or description. The search is case-insensitive.

    Args:
        prompts (List[Prompt]): The list of prompts to search.
        query (str): The search query string.

    Returns:
        List[Prompt]: A list of prompts matching the search query.

    Example Usage:
        >>> matching_prompts = search_prompts(prompts, "example")
    """
    query_lower = query.lower()
    return [
        p for p in prompts 
        if query_lower in p.title.lower() or 
           (p.description and query_lower in p.description.lower())
    ]


def validate_prompt_content(content: str) -> bool:
    """Validate the content of a prompt.

    Ensures that prompt content meets basic validity criteria:
    - Content must not be empty or only whitespace.
    - Content must be at least 10 characters long after trimming whitespace.

    Args:
        content (str): The content string of the prompt to validate.

    Returns:
        bool: True if content is valid, False otherwise.

    Example Usage:
        >>> is_valid = validate_prompt_content("Valid content text.")
    """
    if not content or not content.strip():
        return False
    return len(content.strip()) >= 10


def extract_variables(content: str) -> List[str]:
    """Extract template variables from prompt content.

    Identifies and extracts all template variables from prompt content.
    Variables are expected to be in the format {{variable_name}}.

    Args:
        content (str): The prompt content string containing variables.

    Returns:
        List[str]: A list of all variable names found in the content.

    Example Usage:
        >>> variables = extract_variables("Hello, {{name}}. Your age is {{age}}.")
    """
    import re
    pattern = r'\{\{(\w+)\}\}'
    return re.findall(pattern, content)
