"""Utility functions for PromptLab"""

from app.models import Prompt


def sort_prompts_by_date(prompts: list[Prompt], descending: bool = True) -> list[Prompt]:
    """Sort the list of prompts by their creation date.

    Args:
        prompts (list[Prompt]): The list of Prompt objects to be sorted.
        descending (bool): If True, sort the prompts in descending order. Defaults to True.

    Returns:
        list[Prompt]: The sorted list of prompts.

    Example:
        >>> sorted_prompts = sort_prompts_by_date(prompts, descending=False)
        >>> for prompt in sorted_prompts:
        ...     print(prompt.title)
    """
    return sorted(prompts, key=lambda prompt: prompt.created_at, reverse=descending)


def filter_prompts_by_collection(prompts: list[Prompt], collection_id: str) -> list[Prompt]:
    """Filter prompts by their collection ID.

    Args:
        prompts (list[Prompt]): The list of Prompt objects to filter.
        collection_id (str): The collection ID to filter prompts by.

    Returns:
        list[Prompt]: A list of prompts that belong to the specified collection.

    Example:
        >>> filtered_prompts = filter_prompts_by_collection(prompts, "12345")
        >>> for prompt in filtered_prompts:
        ...     print(prompt.title)
    """
    return [prompt for prompt in prompts if prompt.collection_id == collection_id]


def search_prompts(prompts: list[Prompt], query: str) -> list[Prompt]:
    """Search for prompts containing the query in their title or description.

    Args:
        prompts (list[Prompt]): The list of Prompt objects to search within.
        query (str): The search string to look for in the prompt titles and descriptions.
    Returns:
        list[Prompt]: A list of prompts where the query is found in the title or description.

    Example:
        >>> search_results = search_prompts(prompts, "welcome")
        >>> for prompt in search_results:
        ...     print(prompt.title)
    """
    normalized_query = query.lower()
    return [
        prompt for prompt in prompts
        if normalized_query in prompt.title.lower() or
           (prompt.description and normalized_query in prompt.description.lower())
    ]


