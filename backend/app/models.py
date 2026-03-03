"""Pydantic models for PromptLab

Functions:
    generate_id: Generates a unique identifier using UUID.
    get_current_time: Returns the current UTC time.

Models:
    PromptBase: Shared fields for prompts.
    PromptCreate: Fields required to create a prompt.
    PromptUpdate: Fields for updating a prompt.
    Prompt: Complete prompt model with metadata.
    CollectionBase: Shared fields for collections.
    CollectionCreate: Fields required to create a collection.
    Collection: Complete collection model with metadata.
    PromptList: List of prompts with a total count.
    CollectionList: List of collections with a total count.
    HealthResponse: Health check response model.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import uuid4


def generate_id() -> str:
    """Generates a unique identifier using UUID."""
    return str(uuid4())


def get_current_time() -> datetime:
    """Returns the current UTC time."""
    return datetime.utcnow()


# ============== Prompt Models ==============
# New model for Tag

class TagsInput(BaseModel):
    tags: List[str]
    
class PromptBase(BaseModel):
    """Base class for prompt models.

    Attributes:
        title (str): Title of the prompt, must be between 1 and 200 characters.
        content (str): Main content of the prompt.
        description (Optional[str]): Optional description, up to 500 characters.
        collection_id (Optional[str]): Identifier for the collection the prompt belongs to.

    Example:
        >>> prompt_base = PromptBase(title='Sample Title', content='Sample Content')
        >>> prompt_base.title
        'Sample Title'
    """
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None

class Tag(BaseModel):
    """Represents a tag with a unique identifier and name."""
    id: str
    name: str

# New model extending Prompt to include tags
class PromptWithTags(PromptBase):
    """Extends the Prompt model to include associated tags."""
    tags: List[Tag] = []

    class Config:
        from_attributes = True

class PromptCreate(PromptBase):
    """Model for creating a new prompt.
    Example:
        >>> new_prompt = PromptCreate(title='New Title', content='New Content')
        >>> new_prompt.content
        'New Content'
    """
    pass


class PromptUpdate(PromptBase):
    """Model for updating an existing prompt.
    Example:
        >>> update_prompt = PromptUpdate(title='Updated Title', content='Updated Content')
        >>> update_prompt.title
        'Updated Title'
    """
    pass


class Prompt(PromptBase):
    """Detailed prompt model that includes metadata.
    Attributes:
        id (str): Unique identifier for the prompt.
        created_at (datetime): Creation timestamp.
        updated_at (datetime): Last update timestamp.
    Example:
        >>> prompt = Prompt(title='Title', content='Content')
        >>> prompt.id
        'some-unique-id'
    """
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)

    class Config:
        from_attributes = True


# ============== Collection Models ==============
class CollectionBase(BaseModel):
    """Base class for collection models.
    Attributes:
        name (str): Name of the collection, between 1 and 100 characters.
        description (Optional[str]): Description of the collection, up to 500 characters.
    Example:
        >>> collection_base = CollectionBase(name='Collection Name')
        >>> collection_base.name
        'Collection Name'
    """
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class CollectionCreate(CollectionBase):
    """Model for creating a new collection.
    Example:
        >>> new_collection = CollectionCreate(name='New Collection')
        >>> new_collection.name
        'New Collection'
    """
    pass


class Collection(CollectionBase):
    """Collection model that includes metadata.

    Attributes:
        id (str): Unique identifier for the collection.
        created_at (datetime): Creation timestamp.

    Example:
        >>> collection = Collection(name='Collection Name')
        >>> collection.id
        'some-unique-id'
    """
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)

    class Config:
        from_attributes = True


# ============== Response Models ==============

class PromptList(BaseModel):
    """Model for a list of prompts.

    Attributes:
        prompts (List[Prompt]): List of prompt items.
        total (int): Total number of prompts.

    Example:
        >>> prompt_list = PromptList(prompts=[Prompt(title='Title', content='Content')], total=1)
        >>> len(prompt_list.prompts)
        1
    """
    prompts: List[Prompt]
    total: int


class CollectionList(BaseModel):
    """Model for a list of collections.

    Attributes:
        collections (List[Collection]): List of collection items.
        total (int): Total number of collections.

    Example:
        >>> collection_list = CollectionList(collections=[Collection(name='Name')], total=1)
        >>> len(collection_list.collections)
        1
    """
    collections: List[Collection]
    total: int


class HealthResponse(BaseModel):
    """Model for health check response.

    Attributes:
        status (str): Status of the service.
        version (str): Version of the service.

    Example:
        >>> health = HealthResponse(status='OK', version='1.0.0')
        >>> health.status
        'OK'
    """
    status: str
    version: str

