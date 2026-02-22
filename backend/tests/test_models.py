"""Tests for Pydantic models.

This module tests data validation and model behavior including:
- Field validation
- Default value generation
- Model serialization
- Type validation
"""

import pytest
from datetime import datetime, timezone
from pydantic import ValidationError
from app.models import (
    Prompt, PromptCreate, PromptUpdate,
    Collection, CollectionCreate,
    PromptList, CollectionList, HealthResponse,
    generate_id, get_current_time
)


class TestHelperFunctions:
    """Tests for helper functions."""
    
    def test_generate_id_returns_string(self):
        """Test that generate_id returns a string."""
        result = generate_id()
        assert isinstance(result, str)
    
    def test_generate_id_is_unique(self):
        """Test that generate_id returns unique IDs."""
        id1 = generate_id()
        id2 = generate_id()
        assert id1 != id2
    
    def test_generate_id_not_empty(self):
        """Test that generated ID is not empty."""
        result = generate_id()
        assert len(result) > 0
    
    def test_get_current_time_returns_datetime(self):
        """Test that get_current_time returns datetime."""
        result = get_current_time()
        assert isinstance(result, datetime)
    
    def test_get_current_time_is_utc(self):
        """Test that returned time is in UTC."""
        result = get_current_time()
        assert result.tzinfo == timezone.utc


class TestPromptCreate:
    """Tests for PromptCreate model validation."""
    
    def test_valid_prompt_create(self):
        """Test creating valid PromptCreate instance."""
        data = {
            "title": "Test Prompt",
            "content": "Test content"
        }
        prompt = PromptCreate(**data)
        assert prompt.title == "Test Prompt"
        assert prompt.content == "Test content"
        assert prompt.description is None
        assert prompt.collection_id is None
    
    def test_prompt_create_with_all_fields(self):
        """Test PromptCreate with all fields."""
        data = {
            "title": "Test",
            "content": "Content",
            "description": "Description",
            "collection_id": "col-123"
        }
        prompt = PromptCreate(**data)
        assert prompt.description == "Description"
        assert prompt.collection_id == "col-123"
    
    def test_prompt_create_missing_title(self):
        """Test validation fails without title."""
        with pytest.raises(ValidationError) as exc_info:
            PromptCreate(content="Content")
        assert "title" in str(exc_info.value)
    
    def test_prompt_create_missing_content(self):
        """Test validation fails without content."""
        with pytest.raises(ValidationError) as exc_info:
            PromptCreate(title="Title")
        assert "content" in str(exc_info.value)
    
    def test_prompt_create_empty_title(self):
        """Test validation fails for empty title."""
        with pytest.raises(ValidationError):
            PromptCreate(title="", content="Content")
    
    def test_prompt_create_title_too_long(self):
        """Test validation fails for title > 200 chars."""
        with pytest.raises(ValidationError):
            PromptCreate(title="x" * 201, content="Content")
    
    def test_prompt_create_description_too_long(self):
        """Test validation fails for description > 500 chars."""
        with pytest.raises(ValidationError):
            PromptCreate(
                title="Test",
                content="Content",
                description="x" * 501
            )
    
    def test_prompt_create_max_valid_lengths(self):
        """Test creating prompt at maximum valid lengths."""
        data = {
            "title": "x" * 200,
            "content": "y" * 1000,
            "description": "z" * 500
        }
        prompt = PromptCreate(**data)
        assert len(prompt.title) == 200
        assert len(prompt.description) == 500


class TestPromptUpdate:
    """Tests for PromptUpdate model validation."""
    
    def test_prompt_update_all_fields_optional(self):
        """Test that all fields are optional in PromptUpdate."""
        update = PromptUpdate()
        assert update.title is None
        assert update.content is None
        assert update.description is None
        assert update.collection_id is None
    
    def test_prompt_update_partial_fields(self):
        """Test PromptUpdate with only some fields."""
        update = PromptUpdate(title="New Title")
        assert update.title == "New Title"
        assert update.content is None
    
    def test_prompt_update_all_fields(self):
        """Test PromptUpdate with all fields."""
        update = PromptUpdate(
            title="Title",
            content="Content",
            description="Desc",
            collection_id="col-1"
        )
        assert update.title == "Title"
        assert update.content == "Content"


class TestPrompt:
    """Tests for Prompt model."""
    
    def test_prompt_auto_generates_id(self):
        """Test that Prompt auto-generates ID."""
        prompt = Prompt(title="Test", content="Content")
        assert prompt.id is not None
        assert isinstance(prompt.id, str)
    
    def test_prompt_auto_generates_timestamps(self):
        """Test that Prompt auto-generates timestamps."""
        prompt = Prompt(title="Test", content="Content")
        assert prompt.created_at is not None
        assert prompt.updated_at is not None
        assert isinstance(prompt.created_at, datetime)
        assert isinstance(prompt.updated_at, datetime)
    
    def test_prompt_unique_ids(self):
        """Test that each Prompt gets unique ID."""
        prompt1 = Prompt(title="Test1", content="Content1")
        prompt2 = Prompt(title="Test2", content="Content2")
        assert prompt1.id != prompt2.id
    
    def test_prompt_with_all_fields(self):
        """Test creating Prompt with all fields."""
        now = get_current_time()
        prompt = Prompt(
            id="custom-id",
            title="Test",
            content="Content",
            description="Desc",
            collection_id="col-1",
            created_at=now,
            updated_at=now
        )
        assert prompt.id == "custom-id"
        assert prompt.description == "Desc"
        assert prompt.collection_id == "col-1"
    
    def test_prompt_timestamps_are_utc(self):
        """Test that timestamps are UTC."""
        prompt = Prompt(title="Test", content="Content")
        assert prompt.created_at.tzinfo == timezone.utc
        assert prompt.updated_at.tzinfo == timezone.utc
    
    def test_prompt_model_dump(self):
        """Test serializing Prompt to dict."""
        prompt = Prompt(title="Test", content="Content")
        data = prompt.model_dump()
        assert "id" in data
        assert "title" in data
        assert "created_at" in data


class TestCollectionCreate:
    """Tests for CollectionCreate model validation."""
    
    def test_valid_collection_create(self):
        """Test creating valid CollectionCreate instance."""
        collection = CollectionCreate(name="Development")
        assert collection.name == "Development"
        assert collection.description is None
    
    def test_collection_create_with_description(self):
        """Test CollectionCreate with description."""
        collection = CollectionCreate(
            name="Marketing",
            description="Marketing prompts"
        )
        assert collection.description == "Marketing prompts"
    
    def test_collection_create_missing_name(self):
        """Test validation fails without name."""
        with pytest.raises(ValidationError) as exc_info:
            CollectionCreate()
        assert "name" in str(exc_info.value)
    
    def test_collection_create_empty_name(self):
        """Test validation fails for empty name."""
        with pytest.raises(ValidationError):
            CollectionCreate(name="")
    
    def test_collection_create_name_too_long(self):
        """Test validation fails for name > 100 chars."""
        with pytest.raises(ValidationError):
            CollectionCreate(name="x" * 101)
    
    def test_collection_create_description_too_long(self):
        """Test validation fails for description > 500 chars."""
        with pytest.raises(ValidationError):
            CollectionCreate(name="Test", description="x" * 501)
    
    def test_collection_create_max_valid_lengths(self):
        """Test creating collection at maximum valid lengths."""
        collection = CollectionCreate(
            name="x" * 100,
            description="y" * 500
        )
        assert len(collection.name) == 100
        assert len(collection.description) == 500


class TestCollection:
    """Tests for Collection model."""
    
    def test_collection_auto_generates_id(self):
        """Test that Collection auto-generates ID."""
        collection = Collection(name="Test")
        assert collection.id is not None
        assert isinstance(collection.id, str)
    
    def test_collection_auto_generates_timestamp(self):
        """Test that Collection auto-generates created_at."""
        collection = Collection(name="Test")
        assert collection.created_at is not None
        assert isinstance(collection.created_at, datetime)
    
    def test_collection_unique_ids(self):
        """Test that each Collection gets unique ID."""
        col1 = Collection(name="Test1")
        col2 = Collection(name="Test2")
        assert col1.id != col2.id
    
    def test_collection_timestamp_is_utc(self):
        """Test that timestamp is UTC."""
        collection = Collection(name="Test")
        assert collection.created_at.tzinfo == timezone.utc


class TestResponseModels:
    """Tests for response models."""
    
    def test_prompt_list(self):
        """Test PromptList model."""
        prompt1 = Prompt(title="P1", content="C1")
        prompt2 = Prompt(title="P2", content="C2")
        
        prompt_list = PromptList(prompts=[prompt1, prompt2], total=2)
        assert len(prompt_list.prompts) == 2
        assert prompt_list.total == 2
    
    def test_prompt_list_empty(self):
        """Test PromptList with empty list."""
        prompt_list = PromptList(prompts=[], total=0)
        assert prompt_list.prompts == []
        assert prompt_list.total == 0
    
    def test_collection_list(self):
        """Test CollectionList model."""
        col1 = Collection(name="C1")
        col2 = Collection(name="C2")
        
        col_list = CollectionList(collections=[col1, col2], total=2)
        assert len(col_list.collections) == 2
        assert col_list.total == 2
    
    def test_health_response(self):
        """Test HealthResponse model."""
        response = HealthResponse(status="healthy", version="1.0.0")
        assert response.status == "healthy"
        assert response.version == "1.0.0"
    
    def test_health_response_validation(self):
        """Test HealthResponse requires both fields."""
        with pytest.raises(ValidationError):
            HealthResponse(status="healthy")


class TestModelSerialization:
    """Tests for model serialization and deserialization."""
    
    def test_prompt_from_dict(self):
        """Test creating Prompt from dict."""
        data = {
            "title": "Test",
            "content": "Content",
            "description": "Desc"
        }
        prompt = Prompt(**data)
        assert prompt.title == "Test"
        assert prompt.content == "Content"
    
    def test_prompt_to_dict(self):
        """Test converting Prompt to dict."""
        prompt = Prompt(title="Test", content="Content")
        data = prompt.model_dump()
        
        assert isinstance(data, dict)
        assert data["title"] == "Test"
        assert data["content"] == "Content"
        assert "id" in data
        assert "created_at" in data
    
    def test_prompt_json_serialization(self):
        """Test JSON serialization of Prompt."""
        prompt = Prompt(title="Test", content="Content")
        json_str = prompt.model_dump_json()
        
        assert isinstance(json_str, str)
        assert "Test" in json_str
        assert "Content" in json_str
    
    def test_collection_model_dump(self):
        """Test Collection serialization."""
        collection = Collection(name="Test", description="Desc")
        data = collection.model_dump()
        
        assert data["name"] == "Test"
        assert data["description"] == "Desc"
        assert "id" in data
        assert "created_at" in data


class TestTypeValidation:
    """Tests for type validation."""
    
    def test_prompt_title_must_be_string(self):
        """Test that title must be string."""
        with pytest.raises(ValidationError):
            Prompt(title=123, content="Content")
    
    def test_prompt_content_must_be_string(self):
        """Test that content must be string."""
        with pytest.raises(ValidationError):
            Prompt(title="Test", content=123)
    
    def test_collection_name_must_be_string(self):
        """Test that name must be string."""
        with pytest.raises(ValidationError):
            Collection(name=123)
    
    def test_prompt_list_total_must_be_int(self):
        """Test that total must be integer."""
        with pytest.raises(ValidationError):
            PromptList(prompts=[], total="not an int")
