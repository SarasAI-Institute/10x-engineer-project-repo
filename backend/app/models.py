"""Pydantic models for PromptLab.

Defines request, response, and internal data models used across the API.
Includes prompt, collection, and health response schemas.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from uuid import uuid4


def generate_id() -> str:
    """Generate a unique identifier for resources."""
    return str(uuid4())


def get_current_time() -> datetime:
    """Return the current UTC timestamp."""
    return datetime.utcnow()


# ============== Prompt Models ==============

class PromptBase(BaseModel):
    """
    Base model for prompt data.

    Contains common fields shared across create, update, and response models.
    """

    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Title of the prompt"
    )
    content: str = Field(
        ...,
        min_length=1,
        description="Main prompt content or template"
    )
    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Optional description explaining the purpose of the prompt"
    )
    collection_id: Optional[str] = Field(
        None,
        description="Identifier of the collection this prompt belongs to"
    )
    tags: List[str] = Field(
        default_factory=list,
        description="List of tags associated with the prompt"
    )


class PromptCreate(PromptBase):
    """
    Model used when creating a new prompt.
    """
    pass


class PromptUpdate(PromptBase):
    """
    Model used when updating an existing prompt.
    """
    pass


class Prompt(PromptBase):
    """
    Complete prompt model including system-generated fields.
    """

    id: str = Field(
        default_factory=generate_id,
        description="Unique identifier for the prompt"
    )
    created_at: datetime = Field(
        default_factory=get_current_time,
        description="Timestamp when the prompt was created"
    )
    updated_at: datetime = Field(
        default_factory=get_current_time,
        description="Timestamp when the prompt was last updated"
    )

    model_config = ConfigDict(from_attributes=True)


# ============== Collection Models ==============

class CollectionBase(BaseModel):
    """
    Base model for collection data.

    Represents a logical grouping of prompts.
    """

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Name of the collection"
    )
    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Optional description of the collection"
    )


class CollectionCreate(CollectionBase):
    """
    Model used when creating a new collection.
    """
    pass


class Collection(CollectionBase):
    """
    Complete collection model including system-generated fields.
    """

    id: str = Field(
        default_factory=generate_id,
        description="Unique identifier for the collection"
    )
    created_at: datetime = Field(
        default_factory=get_current_time,
        description="Timestamp when the collection was created"
    )

    model_config = ConfigDict(from_attributes=True)


# ============== Response Models ==============

class PromptList(BaseModel):
    """
    Response model for returning a list of prompts.
    """

    prompts: List[Prompt] = Field(
        ...,
        description="List of prompt objects"
    )
    total: int = Field(
        ...,
        description="Total number of prompts returned"
    )


class CollectionList(BaseModel):
    """
    Response model for returning a list of collections.
    """

    collections: List[Collection] = Field(
        ...,
        description="List of collection objects"
    )
    total: int = Field(
        ...,
        description="Total number of collections returned"
    )


class HealthResponse(BaseModel):
    """
    Health check response model.

    Used to verify API availability and version.
    """

    status: str = Field(
        ...,
        description="Health status of the API (e.g., healthy)"
    )
    version: str = Field(
        ...,
        description="Current version of the API"
    )