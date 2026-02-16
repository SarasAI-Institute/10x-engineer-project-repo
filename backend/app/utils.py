"""Utility functions for PromptLab"""

from typing import List
from app.models import Prompt


def sort_prompts_by_date(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
    """Sorts a list of prompts by their creation date.

    Args:
        prompts (List[Prompt]): The list of Prompt objects to sort.
        descending (bool): If True, sorts in descending order; otherwise, 
            sorts in ascending order. Defaults to True.

    Returns:
        List[Prompt]: The sorted list of prompts.

    Example:
        prompts = [Prompt(created_at=datetime(2023, 1, 15)), 
                   Prompt(created_at=datetime(2021, 7, 10))]
        sorted_prompts = sort_prompts_by_date(prompts)
    """
    # Fixed the below code by using reverse as descending which sorts the new prompt as first
    return sorted(prompts, key=lambda p: p.created_at, reverse=descending)


def filter_prompts_by_collection(prompts: List[Prompt], collection_id: str) -> List[Prompt]:
    """Filters a list of prompts by a specific collection ID.

    Args:
        prompts (List[Prompt]): A list of Prompt objects to filter.
        collection_id (str): The collection ID to filter prompts by.

    Returns:
        List[Prompt]: A list of prompts that belong to the specified collection.

    Example usage:
        filtered_prompts = filter_prompts_by_collection(all_prompts, "collection123")
    """
    return [p for p in prompts if p.collection_id == collection_id]


def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
    """Searches for prompts that contain the query in their title or description.

    Args:
        prompts (List[Prompt]): A list of Prompt objects to search within.
        query (str): The search query string.

    Returns:
        List[Prompt]: A list of prompts that match the search criteria.

    Example:
        >>> search_prompts([Prompt(title="Example", description="Sample description")], "Example")
        [Prompt(title="Example", description="Sample description")]
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

    Args:
        content (str): The prompt content to be validated.

    Returns:
        bool: `True` if the content is valid, `False` otherwise.

    Example usage:
        content = "This is a valid prompt"
        is_valid = validate_prompt_content(content)
        print(is_valid)  # Output: True
    """
    if not content or not content.strip():
        return False
    return len(content.strip()) >= 10


def extract_variables(content: str) -> List[str]:
    """Extract template variables from prompt content.
    
    Variables are in the format {{variable_name}}.

    Args:
        content (str): The string content containing template variables.

    Returns:
        List[str]: A list of variable names found in the content.

    Example usage:
        >>> extract_variables("Hello, {{name}}! Your account number is {{account_number}}.")
        ['name', 'account_number']
    """
    import re
    pattern = r'\{\{(\w+)\}\}'
    return re.findall(pattern, content)

