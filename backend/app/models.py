"""Pydantic models for PromptLab.

This module defines the data shapes used by the API: prompts and collections.
Models are implemented with Pydantic for validation and serialization.

Contracts:
- PromptCreate / PromptUpdate: shapes accepted from clients when creating or
    replacing a prompt.
- PromptPatch: shape for partial updates (PATCH).
- Prompt / Collection: complete persisted models returned by the API.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import uuid4


def generate_id() -> str:
    """Generate a new UUID4-based string identifier.

    Returns:
        A string containing a UUID4 value, e.g. "e7b8f9d2-...".
    """
    return str(uuid4())


def get_current_time() -> datetime:
    """Return the current UTC datetime.

    Returns:
        A timezone-naive datetime representing now in UTC.
    """
    return datetime.utcnow()


# ============== Prompt Models ==============

class PromptBase(BaseModel):
    """Base fields shared by prompt create/update operations.

    Attributes:
        title: Short descriptive title for the prompt (1-200 chars).
        content: The prompt text to be executed or stored.
        description: Optional longer description (up to 500 chars).
        collection_id: Optional id of the collection this prompt belongs to.
    """
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None


class PromptCreate(PromptBase):
    """Model used when creating a new Prompt.

    Inherits all validation rules from PromptBase.
    """
    pass


class PromptUpdate(PromptBase):
    """Model used when replacing (PUT) a Prompt.

    All fields are required by PromptBase semantics; use PATCH for partial
    updates.
    """
    pass


class Prompt(PromptBase):
    """Full Prompt model returned by the API.

    Fields:
        id: unique identifier
        created_at: timestamp when the prompt was first created
        updated_at: timestamp when the prompt was last modified
    """
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)

    class Config:
        from_attributes = True


class PromptPatch(BaseModel):
    """Model for PATCH updates to a Prompt where all fields are optional.

    Only fields provided will be updated by the API endpoint.
    """
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[Optional[str]] = None


# ============== Collection Models ==============

class CollectionBase(BaseModel):
    """Base fields for collection create operations.

    Attributes:
        name: The display name for the collection (1-100 chars).
        description: Optional description for the collection.
    """
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class CollectionCreate(CollectionBase):
    """Model used when creating a new Collection."""
    pass


class Collection(CollectionBase):
    """Full Collection model returned by the API.

    Fields:
        id: unique identifier
        created_at: timestamp when the collection was created
    """
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)

    class Config:
        from_attributes = True


# ============== Response Models ==============

class PromptList(BaseModel):
    """Response model for listing prompts."""
    prompts: List[Prompt]
    total: int


class CollectionList(BaseModel):
    """Response model for listing collections."""
    collections: List[Collection]
    total: int


class HealthResponse(BaseModel):
    """Simple health-check response.

    Attributes:
        status: human-readable status (e.g. 'healthy')
        version: application version string
    """
    status: str
    version: str
