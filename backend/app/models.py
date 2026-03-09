"""Pydantic models that describe PromptLab domain objects."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import uuid4


def generate_id() -> str:
    """Produce a UUID4 string for persistent entities.

    Returns:
        A version 4 UUID string suitable for use as an identifier.
    """
    return str(uuid4())


def get_current_time() -> datetime:
    """Capture the current UTC timestamp for audit fields.

    Returns:
        A datetime object representing the current UTC time.
    """
    return datetime.utcnow()


# ============== Prompt Models ==============

class PromptBase(BaseModel):
    """Shared prompt attributes required for creation and validation.

    Attributes:
        title: Human-readable prompt title (1-200 characters).
        content: The prompt template text that can include variables.
        description: Optional short summary for context.
        collection_id: Optional identifier of the owning collection.
    """

    title: str = Field(
        ..., min_length=1, max_length=200,
        description="Human-readable prompt title (1-200 characters)."
    )
    content: str = Field(
        ..., min_length=1,
        description="Template text for the prompt, may include placeholders."
    )
    description: Optional[str] = Field(
        None, max_length=500,
        description="Optional summary or guidance for the prompt."
    )
    collection_id: Optional[str] = Field(
        None,
        description="Optional collection identifier that groups prompts."
    )


class PromptCreate(PromptBase):
    """Input shape used when creating a new prompt."""


class PromptUpdate(BaseModel):
    """Fields that can be updated for an existing prompt.

    All fields are optional to allow partial updates.
    """

    title: Optional[str] = Field(
        None, min_length=1, max_length=200,
        description="Updated title for the prompt."
    )
    content: Optional[str] = Field(
        None, min_length=1,
        description="Updated prompt body text."
    )
    description: Optional[str] = Field(
        None, max_length=500,
        description="Updated summary or guidance text."
    )
    collection_id: Optional[str] = Field(
        None,
        description="Updated collection association (use null to unlink)."
    )


class Prompt(PromptBase):
    """Full prompt representation stored in PromptLab.

    Attributes:
        id: Unique identifier for the prompt.
        created_at: UTC timestamp when the prompt was created.
        updated_at: UTC timestamp of the most recent change.
        tags: Identifiers for tags associated with this prompt.
    """

    id: str = Field(
        default_factory=generate_id,
        description="Unique identifier assigned to the prompt."
    )
    created_at: datetime = Field(
        default_factory=get_current_time,
        description="UTC timestamp when the prompt was created."
    )
    updated_at: datetime = Field(
        default_factory=get_current_time,
        description="UTC timestamp of the last modification."
    )
    tags: List[str] = Field(
        default_factory=list,
        description="List of tag identifiers assigned to the prompt."
    )

    class Config:
        from_attributes = True


# ============== Collection Models ==============

class CollectionBase(BaseModel):
    """Shared metadata fields for collections.

    Attributes:
        name: Human-friendly collection name (1-100 characters).
        description: Optional description of the collection purpose.
    """

    name: str = Field(
        ..., min_length=1, max_length=100,
        description="Human-friendly name for the collection (1-100 characters)."
    )
    description: Optional[str] = Field(
        None, max_length=500,
        description="Optional explanation of what prompts belong in this collection."
    )


class CollectionCreate(CollectionBase):
    """Input schema when creating a collection."""


class Collection(CollectionBase):
    """Stored representation of a collection."""

    id: str = Field(
        default_factory=generate_id,
        description="Unique identifier assigned to the collection."
    )
    created_at: datetime = Field(
        default_factory=get_current_time,
        description="UTC timestamp when the collection was created."
    )

    class Config:
        from_attributes = True


# ============== Response Models ==============

class PromptList(BaseModel):
    """Payload returned when listing prompts.

    Attributes:
        prompts: The prompt records that match the request.
        total: Count of matching prompts (same as len(prompts)).
    """

    prompts: List[Prompt] = Field(
        ..., description="Matching prompts paged back to the caller."
    )
    total: int = Field(
        ..., description="Total number of prompts attached to this response."
    )


class CollectionList(BaseModel):
    """Payload returned when listing collections."""

    collections: List[Collection] = Field(
        ..., description="Collections returned in the response."
    )
    total: int = Field(
        ..., description="Total number of collections returned."
    )


class HealthResponse(BaseModel):
    """Simple health-check payload."""

    status: str = Field(
        ..., description="Current health status of the API."
    )
    version: str = Field(
        ..., description="Semantic version of the PromptLab API."
    )


# ============== Tag Models ==============

class TagBase(BaseModel):
    """Shared fields for tags."""

    name: str = Field(
        ..., min_length=1, max_length=100,
        description="Unique human-readable tag name."
    )
    description: Optional[str] = Field(
        None, max_length=500,
        description="Optional explanation about the tag's purpose."
    )


class TagCreate(TagBase):
    """Input schema for creating a tag."""


class TagUpdate(BaseModel):
    """Fields that can be updated on a tag."""

    name: Optional[str] = Field(
        None, min_length=1, max_length=100,
        description="New name for the tag."
    )
    description: Optional[str] = Field(
        None, max_length=500,
        description="Updated tag description."
    )


class Tag(TagBase):
    """Stored representation of a tag."""

    id: str = Field(
        default_factory=generate_id,
        description="Unique identifier assigned to the tag."
    )
    created_at: datetime = Field(
        default_factory=get_current_time,
        description="UTC timestamp when the tag was created."
    )

    class Config:
        from_attributes = True


class TagList(BaseModel):
    """Response payload for tag collection endpoints."""

    tags: List[Tag] = Field(..., description="Tags returned in the response.")
    total: int = Field(..., description="Total number of tags returned.")


class TagAssignment(BaseModel):
    """Payload used to assign a tag to a prompt."""

    tag_id: str = Field(
        ..., description="Identifier of the tag to assign."
    )
