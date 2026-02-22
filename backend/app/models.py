"""Pydantic models for PromptLab"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import uuid4


def generate_id() -> str:
    """Generates a unique identifier.

    This function creates a unique string identifier using the
    version 4 of the UUID standard.

    Returns:
        str: A string representation of a UUID4, which is universally unique.

    Usage Example:
        >>> unique_id = generate_id()
        >>> print(unique_id)  # Example output: 'f47ac10b-58cc-4372-a567-0e02b2c3d479'
    """
    return str(uuid4())


def get_current_time() -> datetime:
    """Returns the current UTC date and time.

    This function retrieves the current date and time in UTC (Coordinated Universal Time) using
    the `datetime` module.

    Returns:
        datetime: The current UTC date and time.

    Usage Example:
        current_time = get_current_time()
        print(f"The current UTC time is: {current_time}")
    """
    return datetime.utcnow()


# ============== Prompt Models ==============

class PromptBase(BaseModel):
    """Base model for creating a prompt.

    This model serves as the blueprint for creating a prompt, validating necessary fields, and
    offering optional fields with constraints.

    Attributes:
        title (str): The title of the prompt. Must be between 1 and 200 characters.
        content (str): The content of the prompt. Must be at least 1 character.
        description (Optional[str]): An optional description of the prompt with a maximum of 500 characters.
        collection_id (Optional[str]): An optional field to associate the prompt with a collection.

    Usage Example:
        prompt = PromptBase(title="Sample Title", content="This is a sample prompt.")
    """

    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None


class PromptCreate(PromptBase):
    """Model for creating a new prompt.

    Inherits from `PromptBase` and provides validation for prompt creation.

    Since this class does not add additional attributes or methods, its functionality and usage
    are identical to the `PromptBase`.

    Usage Example:
        new_prompt = PromptCreate(title="New Title", content="This is the content for the new prompt.")
    """
    pass


class PromptUpdate(PromptBase):
    """Model for updating an existing prompt.

    Inherits from `PromptBase` and provides validation for updating prompts.

    Like `PromptCreate`, this class does not add any new attributes or methods, thus its functionality
    matches that of the `PromptBase`.

    Usage Example:
        updated_prompt = PromptUpdate(title="Updated Title", content="Updated content of the prompt.")
    """
    pass


class Prompt(PromptBase):
    """Represents a Prompt entity with additional metadata fields.

    This class extends the PromptBase by adding fields for identification and
    timestamping, enabling tracking and management of individual prompts.

    Attributes:
        id (str): A unique identifier for the prompt, generated using UUID4.
        created_at (datetime): The timestamp of when the prompt was created, set to the current UTC time by default.
        updated_at (datetime): The timestamp of when the prompt was last updated, initially set to the current UTC time.

    Configuration:
        from_attributes (bool): A flag indicating if attributes can be set from a dictionary.

    Examples:
        Creating a new Prompt instance:
            >>> prompt = Prompt(
            ...     title="Sample Title",
            ...     content="This is a sample prompt content.",
            ... )
            >>> print(prompt.id)
            >>> print(prompt.created_at)

    See Also:
        `PromptBase`: The base class that holds essential fields for prompt data.
    """

    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)

    class Config:
        from_attributes = True


# ============== Collection Models ==============

class CollectionBase(BaseModel):
    """A base model for a collection with a name and an optional description.

    Attributes:
        name (str): The name of the collection. Must be between 1 and 100 characters long.
        description (Optional[str]): An optional description for the collection with a maximum length of 500 characters.
    """
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class CollectionCreate(CollectionBase):
    """A model for creating a collection, inheriting from CollectionBase.

    Inherits all attributes from CollectionBase without modification or addition.
    """
    pass


class Collection(CollectionBase):
    """A model representing a stored collection, inheriting from CollectionBase.

    Additional Attributes:
        id (str): A unique identifier for the collection, generated automatically.
        created_at (datetime): The timestamp when the collection was created, generated automatically.

    Config:
        from_attributes: Indicates configuration properties are derived from attributes.
    """
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)

    class Config:
        from_attributes = True


# ============== Response Models ==============

class PromptList(BaseModel):
    """Represents a list of prompts along with a total count.

    Attributes:
        prompts (List[Prompt]): A list of Prompt objects.
        total (int): The total number of prompts.
    """
    prompts: List[Prompt]
    total: int


class CollectionList(BaseModel):
    """Represents a list of collections along with a total count.

    Attributes:
        collections (List[Collection]): A list of Collection objects.
        total (int): The total number of collections.
    """
    collections: List[Collection]
    total: int


class HealthResponse(BaseModel):
    """Represents the health status and version information.

    Attributes:
        status (str): The current health status.
        version (str): The version of the application or system.
    """
    status: str
    version: str

