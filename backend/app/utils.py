"""Utility functions for PromptLab.

This module provides helper functions for common operations like:
- Sorting prompts by date
- Filtering prompts by collection
- Searching prompts by text
- Validating prompt content
- Extracting template variables from prompts
"""

from typing import List
from app.models import Prompt


def sort_prompts_by_date(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
    """Sort prompts by creation date.
    
    Args:
        prompts: List of prompts to sort.
        descending: If True, sort newest first. If False, sort oldest first.
                   Defaults to True (newest first).
    
    Returns:
        List[Prompt]: Sorted list of prompts.
        
    Example:
        >>> sorted_prompts = sort_prompts_by_date(prompts, descending=True)
    """
    # Respect the 'descending' flag and sort accordingly
    return sorted(prompts, key=lambda p: p.created_at, reverse=descending)


def filter_prompts_by_collection(prompts: List[Prompt], collection_id: str) -> List[Prompt]:
    """Filter prompts to only those belonging to a specific collection.
    
    Args:
        prompts: List of prompts to filter.
        collection_id: The collection ID to filter by.
        
    Returns:
        List[Prompt]: Prompts that belong to the specified collection.
        
    Example:
        >>> marketing_prompts = filter_prompts_by_collection(all_prompts, "marketing-id")
    """
    return [p for p in prompts if p.collection_id == collection_id]


def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
    """Search prompts by title or description.
    
    Performs a case-insensitive substring search across prompt titles
    and descriptions.
    
    Args:
        prompts: List of prompts to search.
        query: The search query string.
        
    Returns:
        List[Prompt]: Prompts matching the search query.
        
    Example:
        >>> email_prompts = search_prompts(all_prompts, "email")
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
    - Be at least 10 characters (after stripping whitespace)
    
    Args:
        content: The prompt content to validate.
        
    Returns:
        bool: True if the content is valid, False otherwise.
        
    Example:
        >>> validate_prompt_content("Hello {{name}}")
        True
        >>> validate_prompt_content("   ")
        False
    """
    if not content or not content.strip():
        return False
    return len(content.strip()) >= 10


def extract_variables(content: str) -> List[str]:
    """Extract template variables from prompt content.
    
    Variables are expected in the format {{variable_name}}.
    This is useful for identifying what inputs a prompt template requires.
    
    Args:
        content: The prompt content containing template variables.
        
    Returns:
        List[str]: List of variable names found in the content.
        
    Example:
        >>> extract_variables("Hello {{name}}, your order {{order_id}} is ready")
        ['name', 'order_id']
    """
    import re
    pattern = r'\{\{(\w+)\}\}'
    return re.findall(pattern, content)
