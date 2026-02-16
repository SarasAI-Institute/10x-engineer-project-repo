"""Pydantic models for PromptLab"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import uuid4


def generate_id() -> str:
    """Generates a unique identifier string.

    This function uses the `uuid4` method to generate a random UUID (Universally Unique Identifier).

    Returns:
        str: A string representation of a random UUID.

    Example:
        >>> unique_id = generate_id()
        >>> print(unique_id)  # Outputs a unique identifier, e.g., '123e4567-e89b-12d3-a456-426614174000'
    """
    return str(uuid4())


def get_current_time() -> datetime:
    """Gets the current UTC time.

    Returns:
        datetime: The current time in UTC.

    Example:
        >>> current_time = get_current_time()
        >>> print(current_time)
    """
    return datetime.utcnow()

# ============== Prompt Models ==============

class PromptBase(BaseModel):
    """Base model for a prompt.

    Attributes:
        title (str): The title of the prompt. Must be between 1 and 200 characters.
        content (str): The main content of the prompt. Cannot be empty.
        description (Optional[str]): An optional description of the prompt, maximum 500 characters.
        collection_id (Optional[str]): An optional identifier for the collection to which the prompt belongs.
    """
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None


class PromptCreate(PromptBase):
    """Model for creating a prompt based on PromptBase."""
class PromptUpdate(PromptBase):
    """Model for updating a prompt based on PromptBase."""
class Prompt(PromptBase):
    """Model for a complete prompt with additional meta information.

    Attributes:
        id (str): Unique identifier for the prompt, generated automatically.
        created_at (datetime): Timestamp when the prompt was created, generated automatically.
        updated_at (datetime): Timestamp when the prompt was last updated.
    """
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)

    class Config:
        from_attributes = True


# ============== Collection Models ==============

class CollectionBase(BaseModel):
    """Base model for a collection.

    Attributes:
        name (str): The name of the collection. Must be between 1 and 100 characters.
        description (Optional[str]): An optional description of the collection, maximum 500 characters.
    """
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class CollectionCreate(CollectionBase):
    """Model for creating a collection based on CollectionBase."""
class Collection(CollectionBase):
    """Model for a complete collection with additional meta information.

    Attributes:
        id (str): Unique identifier for the collection, generated automatically.
        created_at (datetime): Timestamp when the collection was created, generated automatically.
    """
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)

    class Config:
        from_attributes = True


# ============== Response Models ==============

class PromptList(BaseModel):
    """Model representing a list of prompts.

    Attributes:
        prompts (List[Prompt]): A list of prompt objects.
        total (int): The total number of prompts.
    """
    prompts: List[Prompt]
    total: int


class CollectionList(BaseModel):
    """Model representing a list of collections.

    Attributes:
        collections (List[Collection]): A list of collection objects.
        total (int): The total number of collections.
    """
    collections: List[Collection]
    total: int


class HealthResponse(BaseModel):
    """Model for health check responses.

    Attributes:
        status (str): The current status of the application.
        version (str): The current version of the application.
    """
    status: str
    version: str

