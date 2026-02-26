"""Utility functions for PromptLab"""

from typing import List
from app.models import Prompt


def sort_prompts_by_date(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
    """Sort the list of prompts by their creation date.

    Args:
        prompts (List[Prompt]): The list of Prompt objects to be sorted.
        descending (bool): If True, sort the prompts in descending order. Defaults to True.

    Returns:
        List[Prompt]: The sorted list of prompts.

    Example:
        >>> sorted_prompts = sort_prompts_by_date(prompts, descending=False)
        >>> for prompt in sorted_prompts:
        ...     print(prompt.title)
    """
    return sorted(prompts, key=lambda p: p.created_at, reverse=descending)


def filter_prompts_by_collection(prompts: List[Prompt], collection_id: str) -> List[Prompt]:
    """Filter prompts by their collection ID.

    Args:
        prompts (List[Prompt]): The list of Prompt objects to filter.
        collection_id (str): The collection ID to filter prompts by.

    Returns:
        List[Prompt]: A list of prompts that belong to the specified collection.

    Example:
        >>> filtered_prompts = filter_prompts_by_collection(prompts, "12345")
        >>> for prompt in filtered_prompts:
        ...     print(prompt.title)
    """
    return [p for p in prompts if p.collection_id == collection_id]


def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
    """Search for prompts containing the query in their title or description.

    Args:
        prompts (List[Prompt]): The list of Prompt objects to search within.
        query (str): The search string to look for in the prompt titles and descriptions.
    Returns:
        List[Prompt]: A list of prompts where the query is found in the title or description.

    Example:
        >>> search_results = search_prompts(prompts, "welcome")
        >>> for prompt in search_results:
        ...     print(prompt.title)
    """
    query_lower = query.lower()
    return [
        p for p in prompts
        if query_lower in p.title.lower() or
           (p.description and query_lower in p.description.lower())
    ]


def validate_prompt_content(content: str) -> bool:
    """Check if prompt content is valid.
    
    A valid prompt should:
    - Not be empty
    - Not be just whitespace
    - Be at least 10 characters
    """
    if not content or not content.strip():
        return False
    return len(content.strip()) >= 10


def extract_variables(content: str) -> List[str]:
    """Extract template variables from prompt content.
    
    Variables are in the format {{variable_name}}
    """
    import re
    pattern = r'\{\{(\w+)\}\}'
    return re.findall(pattern, content)

