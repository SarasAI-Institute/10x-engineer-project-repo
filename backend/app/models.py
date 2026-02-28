"""Pydantic models for PromptLab"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import uuid4
from typing import TYPE_CHECKING


def generate_id() -> str:
    return str(uuid4())


def get_current_time() -> datetime:
    return datetime.utcnow()


# ============== Prompt Models ==============

class PromptBase(BaseModel):
    """Base model for prompt attributes.

    Represents the common attributes shared by prompts for title, content,
    description, and collection association.

    Attributes:
        title (str): The title of the prompt, between 1 and 200 characters.
        content (str): The main content of the prompt, minimum 1 character.
        description (Optional[str]): An optional description of the prompt, max 500 characters.
        collection_id (Optional[str]): ID of the collection the prompt belongs to.

    Example Usage:
        >>> prompt = PromptBase(title="Sample", content="This is content.")
    """
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None


class PromptCreate(PromptBase):
    """Model for creating a new prompt.

    Inherits all fields from PromptBase for initialization of a new prompt.

    Example Usage:
        >>> new_prompt = PromptCreate(title="New Title", content="Content here.")
    """
    pass


class PromptUpdate(PromptBase):
    """Model for updating an existing prompt.

    Inherits all fields from PromptBase for updating details of an existing prompt.

    Example Usage:
        >>> updated_prompt = PromptUpdate(title="Updated Title")
    """
    pass

class PromptPatch(BaseModel):
    """Model for partially updating a prompt.

    Utilized for fields that require updates without changing others.
    Allows optional updating of prompt attributes.

    Attributes:
        title (Optional[str]): New title for the prompt.
        content (Optional[str]): New content for the prompt.
        description (Optional[str]): New description for the prompt.
        collection_id (Optional[str]): Updated collection ID for the prompt.

    Example Usage:
        >>> patch_prompt = PromptPatch(content="Updated content.")
    """
    title: Optional[str] = None
    content: Optional[str] = None
    description: Optional[str] = None
    collection_id: Optional[str] = None

    
class Prompt(PromptBase):
    """Complete model representing a stored prompt with metadata.

    Extends PromptBase and includes unique identifier and timestamps for
    creation and updates.

    Attributes:
        id (str): Unique identifier for the prompt.
        created_at (datetime): Timestamp when the prompt was created.
        updated_at (datetime): Timestamp of the last update to the prompt.

    Example Usage:
        >>> full_prompt = Prompt(title="Title", content="Content")
    """
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)
    versions: List['PromptVersions'] = Field(default_factory=list)

    class Config:
        from_attributes = True

class PromptVersions(BaseModel):
    """Model representing a version of a prompt.

    Attributes:
        version_id (str): A unique identifier for this version of the prompt.
        prompt_data (Prompt): The data of the prompt at this version.
        timestamp (datetime): The time when this version was created, defaults
            to the current time on creation.

    """
    version_id: str
    prompt_data: Prompt
    timestamp: datetime = Field(default_factory=get_current_time)
    version_id: str
    prompt_data: Prompt
    timestamp: datetime = Field(default_factory=get_current_time)

# ============== Collection Models ==============

class CollectionBase(BaseModel):
    """Base model for collection attributes.

    Represents common attributes for collections including a name and description.

    Attributes:
        name (str): Name of the collection, between 1 and 100 characters.
        description (Optional[str]): Optional description for the collection, max 500 characters.

    Example Usage:
        >>> collection = CollectionBase(name="New Collection")
    """
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class CollectionCreate(CollectionBase):
    """Model for creating a new collection.

    Inherits all fields from CollectionBase to initialize a new collection.

    Example Usage:
        >>> new_collection = CollectionCreate(name="Collection Name")
    """
    pass


class Collection(CollectionBase):
    """Complete model representing a stored collection with metadata.

    Extends CollectionBase and includes a unique identifier and creation timestamp.

    Attributes:
        id (str): Unique identifier for the collection.
        created_at (datetime): Timestamp when the collection was created.

    Example Usage:
        >>> full_collection = Collection(name="Collection", description="Description")
    """
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)

    class Config:
        from_attributes = True


# ============== Response Models ==============

class PromptList(BaseModel):
    """Model representing a list of prompts.

    Attributes:
        prompts (List[Prompt]): List containing prompt objects.
        total (int): Total number of prompts in the list.

    Example Usage:
        >>> prompt_list = PromptList(prompts=[Prompt(...)], total=1)
    """
    prompts: List[Prompt]
    total: int


class CollectionList(BaseModel):
    """Model representing a list of collections.

    Attributes:
        collections (List[Collection]): List containing collection objects.
        total (int): Total number of collections in the list.

    Example Usage:
        >>> collection_list = CollectionList(collections=[Collection(...)], total=1)
    """
    collections: List[Collection]
    total: int


class HealthResponse(BaseModel):
    """Model representing the health status of the API.

    Attributes:
        status (str): Current status indicating health (e.g., 'healthy').
        version (str): Current version number of the API.

    Example Usage:
        >>> health_response = HealthResponse(status="healthy", version="1.0.0")
    """
    status: str
    version: str
