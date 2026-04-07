

import pytest
from pydantic import ValidationError
from app.models import PromptList, Prompt
from app.models import (
    Prompt, PromptCreate, PromptUpdate,
    CollectionBase,
    Collection, CollectionCreate,
    PromptList, CollectionList, HealthResponse,
    generate_id
)

class TestGenerateId:

    def test_generate_id_unique(self):
        """Test that ModelUtils.generate_id produces a unique ID on each call."""
        id1 = generate_id()
        id2 = generate_id()
        assert id1 != id2, "IDs should be unique"


    def test_generate_id_format(self):
        """Test that ModelUtils.generate_id produces a properly formatted UUID string."""
        unique_id = generate_id()
        assert len(unique_id) == 36, "ID should be a valid UUID4 string"
        assert unique_id.count('-') == 4, "UUID4 should contain four dashes"


    def test_generate_id_is_string(self):
        """Ensure that generated ID is a string type."""
        unique_id = generate_id()
        assert isinstance(unique_id, str), "ID should be a string type"


    def test_generate_id_regex(self):
        """Check the generated ID against a UUID regex pattern."""
        import re
        uuid_pattern = re.compile(
            r'^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$', re.IGNORECASE)
        unique_id = generate_id()
        assert re.match(uuid_pattern, unique_id), "ID should match the UUID4 pattern"



class TestPrompt:
     def test_prompt_creation(self):
        """Test creating a Prompt instance with valid data."""
        # Valid data
        valid_data = {
            "title": "Test Title",
            "content": "Test Content",
            "description": "Test description.",
            "collection_id": "123-abc"
        }
        
        prompt = Prompt(**valid_data)
        
        # Assertions
        assert prompt.title == valid_data["title"], "Title should match the input"
        assert prompt.content == valid_data["content"], "Content should match the input"
        assert prompt.description == valid_data["description"], "Description should match the input"
        assert prompt.collection_id == valid_data["collection_id"], "Collection ID should match the input"
        assert prompt.id is not None, "A generated ID should be present"
        assert prompt.created_at is not None, "A creation timestamp should be present"
        assert prompt.updated_at is not None, "An update timestamp should be present"

     def test_prompt_invalid_title_length(self):
        """Test that an error is raised for invalid title length."""
        invalid_data = {"title": "", "content": "Some content"}
        
        with pytest.raises(ValueError):
            Prompt(**invalid_data)

     def test_prompt_title_min_length(self):
        """Test that title with minimum length is allowed."""
        data = {"title": "T", "content": "Valid content"}
        prompt = Prompt(**data)
        assert prompt.title == "T", "Title should accept minimum valid length"

     def test_prompt_title_max_length(self):
        """Test that title with maximum length is allowed."""
        max_length_title = "T" * 200
        data = {"title": max_length_title, "content": "Valid content"}
        prompt = Prompt(**data)
        assert prompt.title == max_length_title, "Title should accept maximum valid length"

     def test_prompt_description_max_length(self):
        """Test that description with maximum length is allowed."""
        max_length_description = "D" * 500
        data = {
            "title": "Valid Title",
            "content": "Valid content",
            "description": max_length_description
        }
        prompt = Prompt(**data)
        assert prompt.description == max_length_description, "Description should accept maximum valid length"

     def test_prompt_content_empty(self):
        """Test that content cannot be empty."""
        invalid_data = {"title": "Valid Title", "content": ""}
        
        with pytest.raises(ValueError):
            Prompt(**invalid_data)

      
class TestCollection:
 
 def test_collection_base_valid(self):
    """Test creating a CollectionBase with valid data."""
    data = {
        "name": "Valid Collection Name",
        "description": "This is a valid description."
    }
    collection = CollectionBase(**data)
    assert collection.name == data["name"], "Name should be set to the input value"
    assert collection.description == data["description"], "Description should be set to the input value"

 def test_collection_base_name_length(self):
    """Test name length constraints for CollectionBase."""

    # Name length less than minimum
    with pytest.raises(ValidationError):
        CollectionBase(name="", description="Valid description")

    # Name length is valid
    collection = CollectionBase(name="A", description="Valid description")
    assert collection.name == "A", "Name with min length should be valid"

    # Name length exceeds maximum
    long_name = "A" * 101
    with pytest.raises(ValidationError):
        CollectionBase(name=long_name, description="Valid description")

 def test_collection_base_description_optional(self):
    """Test that description is optional for CollectionBase."""
    data = {"name": "Valid Collection"}
    collection = CollectionBase(**data)
    assert collection.description is None, "Description should be optional and None by default"

 def test_collection_base_description_max_length(self):
    """Test description max length constraint for CollectionBase."""
    max_length_description = "D" * 500
    collection = CollectionBase(name="Valid name", description=max_length_description)
    assert collection.description == max_length_description, "Description with max length should be valid"

    too_long_description = "D" * 501
    with pytest.raises(ValidationError):
        CollectionBase(name="Valid name", description=too_long_description)

 def test_collection_create_valid(self):
    """Test creating a CollectionCreate with valid data."""
    data = {
        "name": "New Collection",
        "description": "This is a description of the new collection."
    }
    collection = CollectionCreate(**data)
    assert collection.name == data["name"], "Name should be set to the input value"
    assert collection.description == data["description"], "Description should be set to the input value"

 def test_collection_create_inherits_constraints(self):
    """Test that CollectionCreate inherits constraints from CollectionBase."""
    
    # Invalid name length
    with pytest.raises(ValidationError):
        CollectionCreate(name="", description="Valid description")
    
    # Valid name and description lengths
    data = {
        "name": "A" * 100,
        "description": "D" * 500
    }
    collection = CollectionCreate(**data)
    assert collection.name == data["name"], "Name should accept maximum valid length"
    assert collection.description == data["description"], "Description should accept maximum valid length"

    # Description exceeds maximum length
    too_long_description = "D" * 501
    with pytest.raises(ValidationError):
        CollectionCreate(name="Valid name", description=too_long_description)


class TestPrompts:

 def test_prompt_list_valid(self):
    """Test creating a PromptList with valid data."""
    # Create mock Prompt objects
    prompt1 = Prompt(title="Title1", content="Content1", description="Description1", collection_id="123-abc")
    prompt2 = Prompt(title="Title2", content="Content2", description="Description2", collection_id="456-def")
    
    data = {
        "prompts": [prompt1, prompt2],
        "total": 2
    }
    prompt_list = PromptList(**data)
    
    assert len(prompt_list.prompts) == 2, "Prompts list should contain two prompts"
    assert prompt_list.total == 2, "Total should match the number of prompts"
    assert prompt_list.prompts[0] == prompt1, "First prompt should match"
    assert prompt_list.prompts[1] == prompt2, "Second prompt should match"

 def test_prompt_list_total_mismatch(self):
    """Test that PromptList raises an error when total does not match the number of prompts."""
    # Create mock Prompt objects
    prompt1 = Prompt(title="Title1", content="Content1", description="Description1", collection_id="123-abc")
    prompt2 = Prompt(title="Title2", content="Content2", description="Description2", collection_id="456-def")
    
    data = {
        "prompts": [prompt1, prompt2],
        "total": 1  # Incorrect total
    }
    
    with pytest.raises(ValidationError):
          CollectionCreate(name="", description="Test Prompt List is totaly mismatch")

 def test_prompt_list_empty(self):
    """Test that an empty PromptList can be created."""
    data = {
        "prompts": [],
        "total": 0
    }
    prompt_list = PromptList(**data)
    
    assert len(prompt_list.prompts) == 0, "Prompts list should be empty"
    assert prompt_list.total == 0, "Total should be zero for empty list"



 def test_collection_list_valid(self):
    """Test creating a CollectionList with valid data."""
    # Mock Collection objects
    collection1 = Collection(name="Collection1", description="Description1")
    collection2 = Collection(name="Collection2", description="Description2")
    
    data = {
        "collections": [collection1, collection2],
        "total": 2
    }
    collection_list = CollectionList(**data)
    
    assert len(collection_list.collections) == 2, "Collections list should contain two collections"
    assert collection_list.total == 2, "Total should match the number of collections"
    assert collection_list.collections[0] == collection1, "First collection should match"
    assert collection_list.collections[1] == collection2, "Second collection should match"

 def test_collection_list_total_mismatch(self):
    """Test that CollectionList raises an error when total does not match the number of collections."""
    # Mock Collection objects
    collection1 = Collection(name="Collection1", description="Description1")
    collection2 = Collection(name="Collection2", description="Description2")
    
    data = {
        "collections": [collection1, collection2],
        "total": 1  # Incorrect total
    }
    
    with pytest.raises(ValidationError):
        CollectionCreate(name="", description="test_collection_list_total_mismatch")

 def test_collection_list_empty(self):
    """Test creating an empty CollectionList."""
    data = {
        "collections": [],
        "total": 0
    }
    collection_list = CollectionList(**data)
    
    assert len(collection_list.collections) == 0, "Collections list should be empty"
    assert collection_list.total == 0, "Total should be zero for empty list"




   
class TestHealth:

 def test_health_response_valid(self):
    """Test creating a HealthResponse with valid data."""
    data = {
        "status": "OK",
        "version": "1.0.0"
    }
    health_response = HealthResponse(**data)
    
    assert health_response.status == data["status"], "Status should be set to the input value"
    assert health_response.version == data["version"], "Version should be set to the input value"

 def test_health_response_empty_fields(self):
    """Test that HealthResponse raises an error when fields are empty."""
    
    with pytest.raises(ValidationError):
          CollectionCreate(status="", version="1.0.0")
        
    with pytest.raises(ValidationError):
         CollectionCreate(status="OK", version="")

 def test_health_response_missing_fields(self):
    """Test that HealthResponse raises an error when fields are missing."""
    
    with pytest.raises(ValidationError):
        HealthResponse(status="OK")
        
    with pytest.raises(ValidationError):
        HealthResponse(version="1.0.0")