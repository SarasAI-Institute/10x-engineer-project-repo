"""Pydantic models for PromptLab.

This module defines all data models used throughout the PromptLab application.
All models use Pydantic for data validation and serialization.

Models are organized into:
- Prompt models: For managing AI prompt templates
- Collection models: For organizing prompts into groups
- Response models: For API responses with metadata
- Health check models: For API status monitoring
"""

from datetime import datetime, timezone
from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import uuid4


def generate_id() -> str:
    """Generate a unique identifier using UUID4.
    
    Returns:
        str: A unique identifier string.
    """
    return str(uuid4())


def get_current_time() -> datetime:
    """Get the current UTC timestamp.
    
    Returns:
        datetime: Current time in UTC timezone.
    """
    return datetime.now(timezone.utc)


# ============== Prompt Models ==============

class PromptBase(BaseModel):
    """Base model for prompt data.
    
    This model contains the core fields shared by all prompt-related models.
    
    Attributes:
        title: The prompt title (1-200 characters).
        content: The actual prompt text with optional template variables.
        description: Optional description of the prompt's purpose.
        collection_id: Optional ID linking this prompt to a collection.
    """
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None


class PromptCreate(PromptBase):
    """Model for creating a new prompt.
    
    Inherits all fields from PromptBase. ID and timestamps are
    automatically generated upon creation.
    """
    pass


class PromptUpdate(BaseModel):
    """Model for updating an existing prompt.
    
    All fields are optional to support partial updates (PATCH).
    Only provided fields will be updated.
    
    Attributes:
        title: Optional new title.
        content: Optional new content.
        description: Optional new description.
        collection_id: Optional new collection ID.
    """
    title: Optional[str] = None
    content: Optional[str] = None
    description: Optional[str] = None
    collection_id: Optional[str] = None


class Prompt(PromptBase):
    """Complete prompt model with all fields.
    
    This model represents a prompt as stored in the system,
    including auto-generated fields like ID and timestamps.
    
    Attributes:
        id: Unique identifier (auto-generated UUID).
        created_at: Creation timestamp (auto-generated UTC).
        updated_at: Last update timestamp (auto-updated).
    """
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)

    model_config = {"from_attributes": True}


# ============== Collection Models ==============

class CollectionBase(BaseModel):
    """Base model for collection data.
    
    Collections are used to organize related prompts into logical groups.
    
    Attributes:
        name: The collection name (1-100 characters).
        description: Optional description of the collection's purpose.
    """
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class CollectionCreate(CollectionBase):
    """Model for creating a new collection.
    
    Inherits all fields from CollectionBase. ID and timestamp are
    automatically generated upon creation.
    """
    pass


class Collection(CollectionBase):
    """Complete collection model with all fields.
    
    This model represents a collection as stored in the system,
    including auto-generated fields.
    
    Attributes:
        id: Unique identifier (auto-generated UUID).
        created_at: Creation timestamp (auto-generated UTC).
    """
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)

    model_config = {"from_attributes": True}


# ============== Response Models ==============

class PromptList(BaseModel):
    """Response model for listing prompts.
    
    Attributes:
        prompts: List of prompt objects.
        total: Total count of prompts in the list.
    """
    prompts: List[Prompt]
    total: int


class CollectionList(BaseModel):
    """Response model for listing collections.
    
    Attributes:
        collections: List of collection objects.
        total: Total count of collections in the list.
    """
    collections: List[Collection]
    total: int


class HealthResponse(BaseModel):
    """Response model for health check endpoint.
    
    Attributes:
        status: Current API health status (e.g., 'healthy').
        version: API version number.
    """
    status: str
    version: str
