"""Pydantic models for PromptLab"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

# ================= Tag Models =================

class Tag(BaseModel):
    """Model representing a tag used for categorization in the system.

    Attributes:
        id (UUID): Unique identifier for the tag.
        name (str): The name of the tag, with a length between 1 and 50 characters.
        created_by (str): Identifier for the user who created the tag.
        created_at (datetime): Timestamp when the tag was created.
        updated_at (datetime): Timestamp when the tag was last updated.

    Example:
        Tag(
            id=UUID('12345678-1234-5678-1234-567812345678'),
            name="Urgent",
            created_by="user1",
            created_at=datetime(...),
            updated_at=datetime(...)
        )
    """
    id: UUID
    name: str = Field(..., min_length=1, max_length=50)
    created_by: str
    created_at: datetime
    updated_at: datetime

class TagCreate(BaseModel):
    """Model for creating a new tag.

    This class defines the structure for data required to create a new tag,
    including the name and creator of the tag.

    Attributes:
        name (str): The name of the tag, must be between 1 and 50 characters.
        created_by (str): Identifier for the user creating the tag.

    Example:
        TagCreate(
            name="Important",
            created_by="user1"
        )
    """
    name: str = Field(..., min_length=1, max_length=50)
    created_by: str

class PromptTag(BaseModel):
    """Model representing the association between a prompt and a tag.

    This model is used to link prompts with their respective tags, including metadata about the creation of the association.

    Attributes:
        id (UUID): Unique identifier for the prompt-tag association.
        prompt_id (str): The ID of the prompt being tagged.
        tag_id (UUID): The ID of the tag applied to the prompt.
        created_at (datetime): Timestamp indicating when the association was created.

    Example:
        PromptTag(
            id=UUID('12345678-1234-5678-1234-567812345678'),
            prompt_id='prompt1',
            tag_id=UUID('87654321-4321-8765-4321-876543218765'),
            created_at=datetime(...)
        )
    """
    id: UUID
    prompt_id: str
    tag_id: UUID
    created_at: datetime


def generate_id() -> str:
    """Generate a unique identifier using UUID4.

    This function leverages the UUID module to create a unique string
    identifier each time it's called.

    Returns:
        str: A unique identifier string.

    Example usage:
        unique_id = generate_id()
    """
    return str(uuid4())


def get_current_time() -> datetime:
    """Get the current UTC time.

    This function returns the current time in UTC format using
    the datetime module.

    Returns:
        datetime: The current UTC time as a datetime object.

    Example usage:
        current_time = get_current_time()
    """
    return datetime.utcnow()


# ============== Prompt Models ==============

class PromptBase(BaseModel):
    """Base model for a Prompt.

    Attributes:
        title (str): The title of the prompt, must be between 1 and 200 characters.
        content (str): The main content of the prompt, must be at least 1 character.
        description (Optional[str]): An optional description of the prompt, capped at 500 characters.
        collection_id (Optional[str]): An identifier for the associated collection, if any.

    Example:
        PromptBase(
            title="Example Title",
            content="This is the content of the prompt.",
            description="A brief description.",
            collection_id="123-abc"
        )
    """
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None


class PromptCreate(PromptBase):
    """Model for creating a new Prompt.

    Inherits all fields from PromptBase.
    """
    pass


class PromptUpdate(BaseModel):
    """Model for updating an existing Prompt.

    Attributes:
        title (Optional[str]): The updated title of the prompt.
        content (Optional[str]): The updated content of the prompt.
        description (Optional[str]): An updated description of the prompt.
        collection_id (Optional[str]): An updated collection identifier.

    Example:
        PromptUpdate(
            title="New Example Title",
            content="Updated content.",
            description="Updated description.",
            collection_id="123-xyz"
        )
    """
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None


class Prompt(PromptBase):
    """Model representing a stored Prompt with metadata.

    Attributes:
        id (str): Unique identifier for the prompt.
        created_at (datetime): Timestamp when the prompt was created.
        updated_at (datetime): Timestamp when the prompt was last updated.

    Example:
        Prompt(
            title="Persistent Title",
            content="Persistent content.",
            description="Persistent description.",
            collection_id="321-cba",
            id="unique-id-123",
            created_at=<datetime_instance>,
            updated_at=<datetime_instance>
        )
    """
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)

    class Config:
        from_attributes = True


# ============== Collection Models ==============

class CollectionBase(BaseModel):
    """Base model for a Collection.

    Attributes:
        name (str): The name of the collection, must be between 1 and 100 characters.
        description (Optional[str]): An optional description of the collection, capped at 500 characters.

    Example:
        CollectionBase(
            name="Collection Name",
            description="Collection description."
        )
    """
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class CollectionCreate(CollectionBase):
    """Model for creating a new Collection.

    This class is used to create a new collection and inherits all 
    fields from the `CollectionBase` class.

    Attributes:
        name (str): The name of the collection, with a length between 1 and 100 characters.
        description (Optional[str]): An optional description of the collection, with a maximum length of 500 characters.

    Example usage:
        collection = CollectionCreate(
            name="New Collection",
            description="This is a description of the new collection."
        )
    """
    pass


class Collection(CollectionBase):
    """Model representing a stored Collection with metadata.

    Attributes:
        id (str): Unique identifier for the collection.
        created_at (datetime): Timestamp when the collection was created.

    Example:
        Collection(
            name="Persistent Collection",
            description="Persistent collection description.",
            id="collection-id-123",
            created_at=<datetime_instance>
        )
    """
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)

    class Config:
        from_attributes = True


# ============== Response Models ==============

class PromptList(BaseModel):
    """Model for a list of Prompts.

    Attributes:
        prompts (list[Prompt]): List containing multiple Prompt objects.
        total (int): Total number of prompts.

    Example:
        PromptList(
            prompts=[Prompt(...), Prompt(...)],
            total=2
        )
    """
    prompts: list[Prompt]
    total: int


class CollectionList(BaseModel):
    """Model for a list of Collections.

    Attributes:
        collections (list[Collection]): List containing multiple Collection objects.
        total (int): Total number of collections.

    Example:
        CollectionList(
            collections=[Collection(...), Collection(...)],
            total=2
        )
    """
    collections: list[Collection]
    total: int


class HealthResponse(BaseModel):
    """Model for representing health status response.

    Attributes:
        status (str): Status of the application health.
        version (str): Current version of the application.

    Example:
        HealthResponse(
            status="OK",
            version="1.0.0"
        )
    """
    status: str
    version: str

class AssignTagRequest(BaseModel):
    tag_id: str

class UpdateTagRequest(BaseModel):
    new_name: str
