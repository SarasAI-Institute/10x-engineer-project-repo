import pytest
from app.models import Prompt, Collection
from app.storage import Storage, Collection


class TestStorage:

    def setup_method(self):
        """Set up a fresh instance of Storage before each test."""
        self.storage = Storage()

    # ============== Prompt Operations ==============

    def test_create_prompt_success(self):
        """Test creating and storing a new prompt."""
        prompt = Prompt(id="123", title="Sample Title", content="Sample Content")
        created_prompt = self.storage.create_prompt(prompt)

        assert created_prompt.id == "123"
        assert self.storage.get_prompt("123") == prompt

    def test_get_prompt_success(self):
        """Test retrieving an existing prompt by ID."""
        prompt = Prompt(id="123", title="Sample Title", content="Sample Content")
        self.storage.create_prompt(prompt)

        retrieved_prompt = self.storage.get_prompt("123")
        assert retrieved_prompt == prompt

    def test_get_prompt_not_found(self):
        """Test retrieving a non-existent prompt."""
        retrieved_prompt = self.storage.get_prompt("nonexistent-id")
        assert retrieved_prompt is None

    def test_get_all_prompts(self):
        """Test retrieving all stored prompts."""
        prompt1 = Prompt(id="123", title="Title 1", content="Content 1")
        prompt2 = Prompt(id="456", title="Title 2", content="Content 2")
        self.storage.create_prompt(prompt1)
        self.storage.create_prompt(prompt2)

        all_prompts = self.storage.get_all_prompts()
        assert len(all_prompts) == 2
        assert prompt1 in all_prompts
        assert prompt2 in all_prompts

    def test_update_prompt_success(self):
        """Test updating an existing prompt."""
        original_prompt = Prompt(id="123", title="Original Title", content="Original Content")
        self.storage.create_prompt(original_prompt)
        
        updated_prompt = Prompt(id="123", title="Updated Title", content="Updated Content")
        result = self.storage.update_prompt("123", updated_prompt)
        
        assert result == updated_prompt
        assert self.storage.get_prompt("123").title == "Updated Title"

    def test_update_prompt_not_found(self):
        """Test updating a non-existent prompt."""
        non_existent_update = Prompt(id="123", title="New Title", content="New Content")
        result = self.storage.update_prompt("nonexistent-id", non_existent_update)
        
        assert result is None

    def test_delete_prompt_success(self):
        """Test successfully deleting a stored prompt."""
        prompt = Prompt(id="123", title="Sample Title", content="Sample Content")
        self.storage.create_prompt(prompt)

        result = self.storage.delete_prompt("123")
        assert result is True
        assert self.storage.get_prompt("123") is None

    def test_delete_prompt_not_found(self):
        """Test deleting a non-existent prompt."""
        result = self.storage.delete_prompt("nonexistent-id")
        assert result is False

class TestStorageCollections:

    def setup_method(self):
        """Set up a fresh instance of Storage before each test."""
        self.storage = Storage()

    # ============== Collection Operations ==============

    def test_create_collection_success(self):
        """Test creating and storing a new collection."""
        collection = Collection(id="col-123", name="Sample Collection")
        created_collection = self.storage.create_collection(collection)

        assert created_collection.id == "col-123"
        assert self.storage.get_collection("col-123") == collection

    def test_get_collection_success(self):
        """Test retrieving an existing collection by ID."""
        collection = Collection(id="col-123", name="Sample Collection")
        self.storage.create_collection(collection)

        retrieved_collection = self.storage.get_collection("col-123")
        assert retrieved_collection == collection

    def test_get_collection_not_found(self):
        """Test retrieving a non-existent collection."""
        retrieved_collection = self.storage.get_collection("nonexistent-id")
        assert retrieved_collection is None

    def test_get_all_collections(self):
        """Test retrieving all stored collections."""
        collection1 = Collection(id="col-123", name="Collection 1")
        collection2 = Collection(id="col-456", name="Collection 2")
        self.storage.create_collection(collection1)
        self.storage.create_collection(collection2)

        all_collections = self.storage.get_all_collections()
        assert len(all_collections) == 2
        assert collection1 in all_collections
        assert collection2 in all_collections

    def test_delete_collection_success(self):
        """Test successfully deleting a stored collection."""
        collection = Collection(id="col-123", name="Sample Collection")
        self.storage.create_collection(collection)

        result = self.storage.delete_collection("col-123")
        assert result is True
        assert self.storage.get_collection("col-123") is None

    def test_delete_collection_not_found(self):
        """Test deleting a non-existent collection."""
        result = self.storage.delete_collection("nonexistent-id")
        assert result is False

class TestStorageAdditional:

    def setup_method(self):
        """Set up a fresh instance of Storage before each test."""
        self.storage = Storage()

    def test_get_prompts_by_collection_success(self):
        """Test retrieving prompts by a specific collection ID."""
        prompt1 = Prompt(id="1", title="Prompt One", content="Content One", collection_id="collection_1")
        prompt2 = Prompt(id="2", title="Prompt Two", content="Content Two", collection_id="collection_1")
        prompt3 = Prompt(id="3", title="Prompt Three", content="Content Three", collection_id="collection_2")

        self.storage.create_prompt(prompt1)
        self.storage.create_prompt(prompt2)
        self.storage.create_prompt(prompt3)

        retrieved_prompts = self.storage.get_prompts_by_collection("collection_1")
        assert len(retrieved_prompts) == 2
        assert prompt1 in retrieved_prompts
        assert prompt2 in retrieved_prompts

    def test_get_prompts_by_collection_no_match(self):
        """Test when no prompts match the collection ID."""
        prompt1 = Prompt(id="1", title="Prompt One", content="Content One", collection_id="collection_3")
        self.storage.create_prompt(prompt1)

        retrieved_prompts = self.storage.get_prompts_by_collection("collection_1")
        assert len(retrieved_prompts) == 0

    def test_get_prompts_by_collection_empty(self):
        """Test retrieving prompts with no prompts in storage."""
        retrieved_prompts = self.storage.get_prompts_by_collection("collection_1")
        assert len(retrieved_prompts) == 0

    def test_clear_storage(self):
        """Test clearing all stored prompts and collections."""
        prompt = Prompt(id="1", title="Prompt One", content="Content One", collection_id="collection_1")
        collection = Collection(id="collection_1", name="Collection One")

        self.storage.create_prompt(prompt)
        self.storage.create_collection(collection)
        self.storage.clear()

        assert len(self.storage.get_all_prompts()) == 0
        assert len(self.storage.get_all_collections()) == 0
        assert self.storage.get_prompt("1") is None
        assert self.storage.get_collection("collection_1") is None
