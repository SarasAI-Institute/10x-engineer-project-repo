"""Utility functions for PromptLab"""

from typing import List
from app.models import Prompt


def sort_prompts_by_date(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
    """Sort prompts by creation date.
    
    This function sorts a list of Prompt objects by their creation date.
    By default, it sorts in descending order, so that the newest prompts appear first.

    Args:
        prompts (List[Prompt]): A list of Prompt objects to be sorted.
        descending (bool): Determines the order of sorting. 
            If True, sorts in descending order (newest first). Defaults to True.

    Returns:
        List[Prompt]: A list of Prompt objects sorted by their creation date.

    Example usage:
        prompts = [Prompt1, Prompt2, Prompt3]
        sorted_prompts = sort_prompts_by_date(prompts, descending=False)
    """
    return sorted(prompts, key=lambda p: p.created_at, reverse=descending)


def filter_prompts_by_collection(prompts: List[Prompt], collection_id: str) -> List[Prompt]:
    """Filter prompts by collection ID.
    
    This function filters a list of Prompt objects, returning only those
    that belong to a specified collection ID.

    Args:
        prompts (List[Prompt]): A list of Prompt objects to be filtered.
        collection_id (str): The collection ID to filter prompts by.

    Returns:
        List[Prompt]: A list of Prompt objects with the specified collection ID.

    Example usage:
        filtered_prompts = filter_prompts_by_collection(prompts, "collection123")
    """
    return [p for p in prompts if p.collection_id == collection_id]


def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
    """Search prompts by a text query.
    
    This function searches through a list of Prompt objects, returning those
    whose title or description contains the specified query string.

    Args:
        prompts (List[Prompt]): A list of Prompt objects to be searched.
        query (str): The text query to search for within prompt titles and descriptions.

    Returns:
        List[Prompt]: A list of Prompt objects that match the search query.

    Example usage:
        search_results = search_prompts(prompts, "example query")
    """
    query_lower = query.lower()
    return [
        p for p in prompts 
        if query_lower in p.title.lower() or 
           (p.description and query_lower in p.description.lower())
    ]


def validate_prompt_content(content: str) -> bool:
    """Check if prompt content is valid.
    
    This function validates the content of a prompt to ensure it meets
    certain criteria such as minimum length and non-whitespace content.

    Args:
        content (str): The content of the prompt to be validated.

    Returns:
        bool: True if the content is valid, False otherwise.

    Example usage:
        is_valid = validate_prompt_content("This is a valid prompt.")
    """
    if not content or not content.strip():
        return False
    return len(content.strip()) >= 10


def extract_variables(content: str) -> List[str]:
    """Extract template variables from prompt content.
    
    This function extracts variables from a string where variables are
    defined in the format {{variable_name}}.

    Args:
        content (str): The content from which to extract variables.

    Returns:
        List[str]: A list of variable names extracted from the content.

    Example usage:
        variables = extract_variables("Hello, {{name}}!")
    """
    import re
    pattern = r'\{\{(\w+)\}\}'
    return re.findall(pattern, content)
