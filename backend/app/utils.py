"""Utility functions for PromptLab"""

from typing import List
from app.models import Prompt, PromptUpdate
from datetime import datetime

def sort_prompts_by_date(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
    """Sort prompts by their creation date.

    This function takes a list of `Prompt` objects and sorts them by the `created_at` attribute. By default, the sorting is in descending order, but it can be toggled to ascending order by setting the `descending` parameter to `False`.

    Args:
        prompts (List[Prompt]): A list of prompt objects containing the `created_at` attribute.
        descending (bool, optional): A flag indicating whether sorting should be in descending order. Defaults to True.

    Returns:
        List[Prompt]: A list of prompts sorted by their creation date in the specified order.

    Usage Examples:
        >>> from datetime import datetime
        >>> prompts = [Prompt(created_at=datetime(2023, 1, 1)), Prompt(created_at=datetime(2022, 1, 1))]
        >>> sorted_prompts = sort_prompts_by_date(prompts)
        >>> sorted_prompts[0].created_at  # datetime(2023, 1, 1)

        >>> sorted_prompts_asc = sort_prompts_by_date(prompts, descending=False)
        >>> sorted_prompts_asc[0].created_at  # datetime(2022, 1, 1)
    """
    # Use the 'reverse' parameter to control descending order sort
    return sorted(prompts, key=lambda p: p.created_at, reverse=descending)


def filter_prompts_by_collection(prompts: List[Prompt], collection_id: str) -> List[Prompt]:
    """Filter prompts by collection ID.

    This function filters a list of `Prompt` objects, returning only those that belong to
    the specified collection.

    Args:
        prompts (List[Prompt]): A list of prompt objects to be filtered.
        collection_id (str): The collection ID to filter prompts by.

    Returns:
        List[Prompt]: A list of prompts belonging to the specified collection ID.

    Usage Examples:
        >>> prompts = [Prompt(collection_id='123'), Prompt(collection_id='456')]
        >>> filtered_prompts = filter_prompts_by_collection(prompts, '123')
        >>> len(filtered_prompts)  # 1
        >>> filtered_prompts[0].collection_id  # '123'
    """
    return [p for p in prompts if p.collection_id == collection_id]


def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
    """Searches through a list of prompts and returns those that match the query.

    This function filters a list of Prompt objects, returning only those where the
    query string is found in the prompt's title or description, case insensitive.

    Args:
        prompts (List[Prompt]): A list of Prompt objects to search through.
        query (str): A string query to search for within each prompt's title and description.
    Returns:
        List[Prompt]: A list of prompts that match the query, based on title or description.

    Usage Example:
        prompts = [
            Prompt(title="Daily Standup", description="Discuss daily progress"),
            Prompt(title="Project Planning", description="Plan the next milestones"),
        ]
        query = "daily"
        matching_prompts = search_prompts(prompts, query)
        # matching_prompts will contain only the "Daily Standup" prompt
    """
    query_lower = query.lower()
    return [
        p for p in prompts
        if query_lower in p.title.lower() or
           (p.description and query_lower in p.description.lower())
    ]


def validate_prompt_content(content: str) -> bool:
    """Validates the content of a prompt to ensure it meets certain criteria.
    A valid prompt should:
    - Not be empty
    - Not be just whitespace
    - Be at least 10 characters

    This function checks if the provided prompt content is valid. A valid prompt:
    - Is not empty
    - Is not just whitespace
    - Has a length of at least 10 characters

    Args:
        content (str): The prompt content to validate.

    Returns:
        bool: True if the content is valid, False otherwise.

    Usage examples:
        >>> validate_prompt_content("Hello, world!")
        True
        >>> validate_prompt_content("   ")
        False
        >>> validate_prompt_content("Short")
        False
    """
    if not content or not content.strip():
        return False
    return len(content.strip()) >= 10


def extract_variables(content: str) -> List[str]:
    """Extract template variables from prompt content.
    
    This function scans the given string for template variables that are enclosed in double curly braces (`{{variable_name}}`). It returns a list of all variable names found within the string.

    Args:
        content (str): The string content to search for template variables.

    Returns:
        List[str]: A list of variable names extracted from the content.

    Usage:
        >>> extract_variables("Hello {{user}}, you have {{count}} new messages.")
        ['user', 'count']

        >>> extract_variables("No variables here.")
        []
    """
    import re
    pattern = r'\{\{(\w+)\}\}'
    return re.findall(pattern, content)

def apply_partial_updates(existing_data: Prompt, update_data: PromptUpdate) -> Prompt:
    """Apply partial updates to a prompt, updating only provided fields.

    This function takes an existing prompt and a set of updates, and applies
    only the fields that are set in the update data. The `updated_at` field
    of the prompt is also updated to the current time.

    Args:
        existing_data (Prompt): The original prompt data that needs updates.
        update_data (PromptUpdate): An object containing fields to update.
                                    Only the fields that are set in this object
                                    will be updated in `existing_data`.

    Returns:
        Prompt: A new `Prompt` object with the updates applied.

    Usage Examples:
        existing_prompt = Prompt(title="Old Title", content="Old Content", updated_at=some_date)
        updates = PromptUpdate(title="New Title")

        updated_prompt = apply_partial_updates(existing_prompt, updates)
        print(updated_prompt.title)  # Output: "New Title"
    """
    updated_data = existing_data.dict()
    update_fields = update_data.dict(exclude_unset=True)

    for key, value in update_fields.items():
        if key in updated_data:
            updated_data[key] = value

    updated_data['updated_at'] = datetime.utcnow()
    return Prompt(**updated_data)