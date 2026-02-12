"""Utility functions for PromptLab"""

from typing import List
from app.models import Prompt
from datetime import datetime

def sort_prompts_by_date(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
    """Sort prompts by creation date.
    
    Note: There might be a bug here. Check the sort order!
    """
    # Use the 'reverse' parameter to control descending order sort
    return sorted(prompts, key=lambda p: p.created_at, reverse=descending)


def filter_prompts_by_collection(prompts: List[Prompt], collection_id: str) -> List[Prompt]:
    return [p for p in prompts if p.collection_id == collection_id]


def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
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

def apply_partial_updates(existing_data: Prompt, update_data: PromptUpdate) -> Prompt:
    """Apply partial updates to a prompt, updating only provided fields."""
    updated_data = existing_data.dict()
    update_fields = update_data.dict(exclude_unset=True)

    for key, value in update_fields.items():
        if key in updated_data:
            updated_data[key] = value

    updated_data['updated_at'] = datetime.utcnow()
    return Prompt(**updated_data)