import pytest
from pydantic import ValidationError
from app.models import (
    Prompt,
    PromptCreate,
    PromptUpdate,
    Collection,
    CollectionCreate,
    PromptList,
    CollectionList,
    HealthResponse
)
from datetime import datetime

def test_prompt_create_valid_data():
    """Test that a Prompt model instance can be created with valid data."""
    prompt = Prompt(
        title="Valid Title",
        content="This is valid content.",
        description="Optional description",
        collection_id="col123"
    )
    assert prompt.title == "Valid Title"
    assert prompt.content == "This is valid content."
    assert prompt.description == "Optional description"
    assert prompt.collection_id == "col123"
    assert isinstance(prompt.id, str)
    assert isinstance(prompt.created_at, datetime)
    assert isinstance(prompt.updated_at, datetime)

def test_prompt_create_invalid_data():
    """Test that creating a Prompt model fails with invalid data."""    
    with pytest.raises(ValidationError):
        Prompt(title="Valid Title", content="")  # Invalid, content shorter than valid length

def test_default_values_for_prompt():
    """Test default values for Prompt model fields."""
    prompt = Prompt(
        title="Title",
        content="Content"
    )
    assert isinstance(prompt.id, str)
    assert isinstance(prompt.created_at, datetime)
    assert isinstance(prompt.updated_at, datetime)

def test_collection_create_valid_data():
    """Test creation of a Collection with valid data."""
    collection = Collection(
        name="Collection Name",
        description="A valid description"
    )
    assert collection.name == "Collection Name"
    assert collection.description == "A valid description"
    assert isinstance(collection.id, str)
    assert isinstance(collection.created_at, datetime)

def test_collection_create_invalid_data():
    """Test that creating a Collection model fails with invalid data."""
    with pytest.raises(ValidationError):
        Collection(name="", description="Desc")  # Invalid, name is empty

def test_prompt_list_serialization():
    """Test serialization of PromptList model."""
    prompt_1 = Prompt(title="Prompt 1", content="Content 1")
    prompt_2 = Prompt(title="Prompt 2", content="Content 2")
    prompt_list = PromptList(prompts=[prompt_1, prompt_2], total=2)
    serialized_data = prompt_list.json()
    assert 'Prompt 1' in serialized_data
    assert 'Prompt 2' in serialized_data
    assert 'total' in serialized_data

def test_collection_list_serialization():
    """Test serialization of CollectionList model."""
    collection_1 = Collection(name="Collection 1")
    collection_2 = Collection(name="Collection 2")
    collection_list = CollectionList(collections=[collection_1, collection_2], total=2)
    serialized_data = collection_list.json()
    assert 'Collection 1' in serialized_data
    assert 'Collection 2' in serialized_data
    assert 'total' in serialized_data

def test_health_response_model():
    """Test HealthResponse model fields."""
    health = HealthResponse(status="Healthy", version="1.0")
    assert health.status == "Healthy"
    assert health.version == "1.0"
