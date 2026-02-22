"""Pydantic models for PromptLab"""

from datetime import datetime, timezone
from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import uuid4


def generate_id() -> str:
    return str(uuid4())


def get_current_time() -> datetime:
    return datetime.now(timezone.utc)


# ============== Prompt Models ==============

class PromptBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None
    tags: List[str] = Field(default_factory=list)


class PromptCreate(PromptBase):
    pass


class PromptUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    description: Optional[str] = None
    collection_id: Optional[str] = None
    tags: Optional[List[str]] = None


class Prompt(PromptBase):
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)

    model_config = {"from_attributes": True}


# ============== Collection Models ==============

class CollectionBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class CollectionCreate(CollectionBase):
    pass


class Collection(CollectionBase):
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)

    model_config = {"from_attributes": True}


# ============== Response Models ==============

class PromptList(BaseModel):
    prompts: List[Prompt]
    total: int


class CollectionList(BaseModel):
    collections: List[Collection]
    total: int


class TagList(BaseModel):
    tags: List[str]


class TagAdd(BaseModel):
    tag: str = Field(..., min_length=1, max_length=50)


class HealthResponse(BaseModel):
    status: str
    version: str
