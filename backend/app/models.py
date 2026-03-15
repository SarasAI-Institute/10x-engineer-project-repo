"""Pydantic models for PromptLab."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from uuid import uuid4


def generate_id() -> str:
    """Generate a unique identifier for persisted resources.

    Returns:
        str: A randomly generated UUID4 string.
    """

    return str(uuid4())


def get_current_time() -> datetime:
    """Fetch the current UTC timestamp.

    Returns:
        datetime: The current UTC datetime.
    """

    return datetime.utcnow()


# ============== Prompt Models ==============

class PromptBase(BaseModel):
    """Base schema containing shared prompt attributes.

    Attributes:
        title (str): Human-readable name for the prompt.
        content (str): The actual prompt text.
        description (Optional[str]): Additional context or annotations for the prompt.
        collection_id (Optional[str]): Identifier of the collection the prompt is grouped under.
    """

    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Human-readable name for the prompt.",
    )
    content: str = Field(
        ...,
        min_length=1,
        description="The actual prompt text.",
    )
    description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Additional context or annotations for the prompt.",
    )
    collection_id: Optional[str] = Field(
        default=None,
        description="Identifier of the collection the prompt is grouped under.",
    )


class PromptCreate(PromptBase):
    """Model for creating new prompts using user-provided fields."""


class PromptUpdate(PromptBase):
    """Model for replacing an existing prompt's mutable fields."""

    change_note: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="Reason for the update stored with the created version.",
    )


class PromptPatch(BaseModel):
    """Model for partially updating prompt attributes.

    Attributes:
        title (Optional[str]): Updated human-readable name for the prompt.
        content (Optional[str]): Updated prompt text.
        description (Optional[str]): Updated annotations or notes for the prompt.
        collection_id (Optional[str]): Updated collection identifier for the prompt.
    """

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=200,
        description="Updated human-readable name for the prompt.",
    )
    content: Optional[str] = Field(
        default=None,
        min_length=1,
        description="Updated prompt text.",
    )
    description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Updated annotations or notes for the prompt.",
    )
    collection_id: Optional[str] = Field(
        default=None,
        description="Updated collection identifier for the prompt.",
    )
    change_note: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="Reason for the change stored with the created version.",
    )


class Prompt(PromptBase):
    """Complete prompt model with server-managed metadata.

    Attributes:
        id (str): Unique identifier of the prompt.
        created_at (datetime): Timestamp when the prompt was created.
        updated_at (datetime): Timestamp of the most recent modification.
    """

    id: str = Field(
        default_factory=generate_id,
        description="Unique identifier of the prompt.",
    )
    created_at: datetime = Field(
        default_factory=get_current_time,
        description="Timestamp when the prompt was created.",
    )
    updated_at: datetime = Field(
        default_factory=get_current_time,
        description="Timestamp of the most recent modification.",
    )
    current_version: int = Field(
        default=0,
        ge=0,
        description="Latest saved version number for this prompt.",
    )

    model_config = ConfigDict(from_attributes=True)


# ============== Collection Models ==============

class CollectionBase(BaseModel):
    """Base schema for collection attributes.

    Attributes:
        name (str): Human-readable name for the collection.
        description (Optional[str]): Optional summary describing the collection.
    """

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Human-readable name for the collection.",
    )
    description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Optional summary describing the collection.",
    )


class CollectionCreate(CollectionBase):
    """Model for creating new collections."""


class Collection(CollectionBase):
    """Collection model enriched with server-managed metadata.

    Attributes:
        id (str): Unique identifier of the collection.
        created_at (datetime): Timestamp when the collection was created.
    """

    id: str = Field(
        default_factory=generate_id,
        description="Unique identifier of the collection.",
    )
    created_at: datetime = Field(
        default_factory=get_current_time,
        description="Timestamp when the collection was created.",
    )

    model_config = ConfigDict(from_attributes=True)


# ============== Response Models ==============

class PromptList(BaseModel):
    """Response model containing paginated prompts.

    Attributes:
        prompts (List[Prompt]): List of prompts returned for the current page.
        total (int): Total number of prompts available across all pages.
    """

    prompts: List[Prompt] = Field(
        ...,
        description="List of prompts returned for the current page.",
    )
    total: int = Field(
        ...,
        description="Total number of prompts available across all pages.",
    )


class CollectionList(BaseModel):
    """Response model containing paginated collections.

    Attributes:
        collections (List[Collection]): List of collections returned for the current page.
        total (int): Total number of collections available across all pages.
    """

    collections: List[Collection] = Field(
        ...,
        description="List of collections returned for the current page.",
    )
    total: int = Field(
        ...,
        description="Total number of collections available across all pages.",
    )


# ============== Prompt Version Models ==============


class PromptVersion(BaseModel):
    """Immutable snapshot of a prompt prior to an update."""

    id: str = Field(default_factory=generate_id, description="Unique version identifier.")
    prompt_id: str = Field(..., description="Identifier of the prompt this version belongs to.")
    version_number: int = Field(
        ...,
        ge=1,
        description="Sequential version number scoped to a single prompt.",
    )
    title: str = Field(..., description="Title captured in the snapshot.")
    content: str = Field(..., description="Content captured in the snapshot.")
    description: Optional[str] = Field(
        default=None,
        description="Description captured in the snapshot.",
    )
    collection_id: Optional[str] = Field(
        default=None,
        description="Collection ID captured in the snapshot.",
    )
    created_at: datetime = Field(
        default_factory=get_current_time,
        description="Timestamp when the version was recorded.",
    )
    editor: str = Field(
        default="system",
        min_length=1,
        max_length=100,
        description="Identifier for who performed the change.",
    )
    change_note: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Reason provided for the change that produced this version.",
    )

    model_config = ConfigDict(from_attributes=True)


class PromptVersionSummary(BaseModel):
    """Subset of version fields returned when listing versions."""

    id: str = Field(..., description="Unique version identifier.")
    version_number: int = Field(..., description="Sequential version number.")
    editor: str = Field(..., description="Editor associated with the change.")
    change_note: Optional[str] = Field(
        default=None,
        description="Optional note supplied for the change.",
    )
    created_at: datetime = Field(..., description="Timestamp when the version was created.")

    model_config = ConfigDict(from_attributes=True)


class PromptVersionList(BaseModel):
    """Response for listing versions of a prompt."""

    prompt_id: str = Field(..., description="Prompt identifier for the listed versions.")
    versions: List[PromptVersionSummary] = Field(
        ..., description="Versions available for the prompt, newest first."
    )
    total: int = Field(..., description="Total number of versions returned.")


class PromptVersionRestoreRequest(BaseModel):
    """Payload accepted when restoring a prompt version."""

    change_note: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="Reason recorded for restoring to a previous version.",
    )


class HealthResponse(BaseModel):
    """Health check response payload.

    Attributes:
        status (str): Indicator of API availability.
        version (str): Semantic version of the running service.
    """

    status: str = Field(
        ...,
        description="Indicator of API availability.",
    )
    version: str = Field(
        ...,
        description="Semantic version of the running service.",
    )


