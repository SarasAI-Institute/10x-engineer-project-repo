import pytest
from datetime import datetime
from pydantic import ValidationError
from uuid import UUID
from app.models import (
    Prompt,
    PromptBase,
    PromptCreate,
    PromptUpdate,
    Collection,
    CollectionBase,
    CollectionCreate,
    generate_id,
    get_current_time,
    PromptList, 
    CollectionList,
    HealthResponse
)

class TestModels:
    def test_generate_id_success(self):
        """Test that generate_id returns a valid UUID string."""
        unique_id = generate_id()
        # Verify the ID is a valid UUID
        try:
            val = UUID(unique_id, version=4)
        except ValueError:
            pytest.fail(f"generate_id() returned an invalid UUID: {unique_id}")

        assert isinstance(unique_id, str)
        assert unique_id == str(val)  # Check if the representation matches

    def test_generate_id_uniqueness(self):
        """Test that generate_id generates unique IDs."""
        ids = {generate_id() for _ in range(1000)}
        assert len(ids) == 1000  # Ensure all generated IDs are unique

    def test_get_current_time_success(self):
        """Test that get_current_time returns the current UTC time."""
        current_time = get_current_time()

        # Check that current_time is a datetime object and is timezone-naive
        assert isinstance(current_time, datetime)
        assert current_time.tzinfo is None  # `utcnow` is naive (i.e., no tzinfo)

        # Manual delay check (not precise, but ensures it's reasonably recent)
        assert (datetime.utcnow() - current_time).total_seconds() < 2

    def test_get_current_time_datetime_format(self):
        """Ensure that get_current_time returns a datetime object in UTC."""
        current_time = get_current_time()
        assert isinstance(current_time, datetime)
        # UTC time should have no tzinfo (naive datetime)
        assert current_time.tzinfo is None

class TestPromptBaseModel:
    """Tests for the PromptBase model."""

    def test_prompt_base_success(self):
        """Test creating a valid PromptBase instance."""
        prompt = PromptBase(
            title="Valid Title",
            content="This is a valid content for the prompt.",
            description="Optional description here.",
            collection_id="collection_123"
        )
        assert prompt.title == "Valid Title"
        assert prompt.content == "This is a valid content for the prompt."
        assert prompt.description == "Optional description here."
        assert prompt.collection_id == "collection_123"
    
    def test_prompt_base_partial_failure(self):
        """Test creating prompts with some missing optional fields."""
        prompt1 = PromptBase(title="Valid Title", content="Valid content")
        assert prompt1.description is None
        assert prompt1.collection_id is None

        prompt2 = PromptBase(title="Another Title", content="More content", description="Short desc")
        assert prompt2.description == "Short desc"
        assert prompt2.collection_id is None

class TestPromptModels:

    def test_prompt_create_success(self):
        """Test creating a valid PromptCreate instance."""
        prompt = PromptCreate(
            title="Create Title",
            content="Create Content",
            description="Optional description",
            collection_id="collection_1"
        )
        assert prompt.title == "Create Title"
        assert prompt.content == "Create Content"

    def test_prompt_update_success(self):
        """Test creating a valid PromptUpdate instance."""
        prompt = PromptUpdate(
            title="Update Title",
            content="Update Content",
            description="Updated description"
        )
        assert prompt.title == "Update Title"
        assert prompt.content == "Update Content"

    def test_prompt_model_success(self):
        """Test creating a full-fledged Prompt instance."""
        prompt = Prompt(
            title="Full Prompt",
            content="Full Content",
            description="Detailed description",
            collection_id="collection_2"
        )
        assert isinstance(prompt.id, str)
        assert isinstance(prompt.created_at, datetime)
        assert isinstance(prompt.updated_at, datetime)

    def test_prompt_model_empty_fields(self):
        """Test fields are correctly set to default when not provided in Prompt."""
        prompt = Prompt(
            title="Example Title",
            content="Example Content"
        )
        assert prompt.description is None
        assert prompt.collection_id is None

class TestCollectionModels:

    def test_collection_base_success(self):
        """Test creating a valid CollectionBase instance."""
        collection = CollectionBase(
            name="Collection Name",
            description="Optional description for the collection."
        )
        assert collection.name == "Collection Name"
        assert collection.description == "Optional description for the collection."

    def test_collection_model_success(self):
        """Test creating a full-fledged Collection instance."""
        collection = Collection(
            name="My Collection",
            description="Description of my collection."
        )
        assert isinstance(collection.id, str)
        assert isinstance(collection.created_at, datetime)

    def test_collection_create_success(self):
        """Test creating a valid CollectionCreate instance."""
        collection = CollectionCreate(
            name="Create Collection",
            description="A description for creation."
        )
        assert collection.name == "Create Collection"
        assert collection.description == "A description for creation."

class TestListModels:

    def test_prompt_list_success(self):
        """Test creating a valid PromptList instance."""
        prompt = Prompt(title="Title", content="Content")
        prompt_list = PromptList(prompts=[prompt], total=1)

        assert len(prompt_list.prompts) == 1
        assert prompt_list.total == 1
        assert prompt_list.prompts[0] == prompt

    def test_prompt_list_empty(self):
        """Test creating a PromptList with no prompts."""
        prompt_list = PromptList(prompts=[], total=0)

        assert len(prompt_list.prompts) == 0
        assert prompt_list.total == 0

    def test_prompt_list_total_independent(self):
        """Check total field set independently of list length (no automatic validation)."""
        prompt = Prompt(title="Title", content="Content")
        prompt_list = PromptList(prompts=[prompt], total=2)

        # Not an error, total is set manually
        assert len(prompt_list.prompts) == 1
        assert prompt_list.total == 2

    def test_collection_list_success(self):
        """Test creating a valid CollectionList instance."""
        collection = Collection(name="Name")
        collection_list = CollectionList(collections=[collection], total=1)

        assert len(collection_list.collections) == 1
        assert collection_list.total == 1
        assert collection_list.collections[0] == collection

    def test_collection_list_empty(self):
        """Test creating a CollectionList with no collections."""
        collection_list = CollectionList(collections=[], total=0)

        assert len(collection_list.collections) == 0
        assert collection_list.total == 0

    def test_collection_list_total_independent(self):
        """Check total field set independently of list length (no automatic validation)."""
        collection = Collection(name="Name")
        collection_list = CollectionList(collections=[collection], total=2)

        # Not an error, total is set manually
        assert len(collection_list.collections) == 1
        assert collection_list.total == 2

    def test_health_response_success(self):
        """Test creating a valid HealthResponse instance."""
        health = HealthResponse(status="OK", version="1.0.0")

        assert health.status == "OK"
        assert health.version == "1.0.0"

    def test_health_response_missing_fields(self):
        """Test HealthResponse with missing fields (should trigger a validation error)."""
        with pytest.raises(ValidationError) as excinfo:
            HealthResponse(status="OK")  # Missing 'version'
        
        errors = excinfo.value.errors()
        assert any(err['loc'] == ('version',) and err['type'] == 'missing' for err in errors)
