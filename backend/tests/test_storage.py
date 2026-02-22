"""Tests for storage layer.

This module tests the in-memory storage implementation including:
- CRUD operations
- Data persistence in memory
- Thread safety considerations
- Edge cases
"""

import pytest
from datetime import datetime, timezone
from app.storage import storage
from app.models import Prompt, PromptCreate, PromptUpdate, Collection, CollectionCreate


class TestStorageInitialization:
    """Tests for storage initialization."""
    
    def test_prompts_db_is_dict(self):
        """Test that prompts storage exists."""
        assert hasattr(storage, '_prompts')
        assert isinstance(storage._prompts, dict)
    
    def test_collections_db_is_dict(self):
        """Test that collections storage exists."""
        assert hasattr(storage, '_collections')
        assert isinstance(storage._collections, dict)
    
    def test_clear_storage_empties_dicts(self):
        """Test that clear empties both databases."""
        # Add some data
        prompt = Prompt(title="Test", content="Content")
        storage.create_prompt(prompt)
        collection = Collection(name="Test")
        storage.create_collection(collection)
        
        # Clear storage
        storage.clear()
        
        # Verify empty
        assert len(storage._prompts) == 0
        assert len(storage._collections) == 0


class TestPromptCRUD:
    """Tests for prompt CRUD operations."""
    
    def test_create_prompt(self):
        """Test creating a prompt."""
        prompt = Prompt(title="Test", content="Content")
        created = storage.create_prompt(prompt)
        
        assert created.id is not None
        assert created.title == "Test"
        assert created.content == "Content"
        assert created.id in storage._prompts
    
    def test_create_prompt_stores_in_db(self):
        """Test that created prompt is stored in database."""
        prompt = Prompt(title="Test", content="Content")
        created = storage.create_prompt(prompt)
        
        stored = storage._prompts[created.id]
        assert stored.id == created.id
        assert stored.title == "Test"
    
    def test_get_prompt_exists(self):
        """Test getting existing prompt."""
        prompt = Prompt(title="Test", content="Content")
        created = storage.create_prompt(prompt)
        
        retrieved = storage.get_prompt(created.id)
        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.title == "Test"
    
    def test_get_prompt_not_exists(self):
        """Test getting non-existent prompt returns None."""
        result = storage.get_prompt("nonexistent-id")
        assert result is None
    
    def test_get_all_prompts_empty(self):
        """Test getting all prompts when empty."""
        storage.clear()
        result = storage.get_all_prompts()
        assert result == []
    
    def test_get_all_prompts_multiple(self):
        """Test getting all prompts with multiple items."""
        storage.clear()
        storage.create_prompt(Prompt(title="P1", content="C1"))
        storage.create_prompt(Prompt(title="P2", content="C2"))
        storage.create_prompt(Prompt(title="P3", content="C3"))
        
        result = storage.get_all_prompts()
        assert len(result) == 3
        titles = [p.title for p in result]
        assert "P1" in titles
        assert "P2" in titles
        assert "P3" in titles
    
    def test_update_prompt_exists(self):
        """Test updating existing prompt."""
        prompt = Prompt(title="Original", content="Content")
        created = storage.create_prompt(prompt)
        original_updated_at = created.updated_at
        
        # Update it
        updated_prompt = created.model_copy(update={"title": "Updated"})
        result = storage.update_prompt(created.id, updated_prompt)
        
        assert result is not None
        assert result.title == "Updated"
        assert result.content == "Content"  # Unchanged
        assert result.updated_at >= original_updated_at
    
    def test_update_prompt_not_exists(self):
        """Test updating non-existent prompt returns None."""
        prompt = Prompt(title="Test", content="Content")
        result = storage.update_prompt("nonexistent-id", prompt)
        assert result is None
    
    def test_update_prompt_partial(self):
        """Test partial update of prompt."""
        prompt = Prompt(
            title="Original",
            content="Original Content",
            description="Original Description"
        )
        created = storage.create_prompt(prompt)
        
        # Update only description
        updated_prompt = created.model_copy(update={"description": "Updated Description"})
        result = storage.update_prompt(created.id, updated_prompt)
        
        assert result.title == "Original"  # Unchanged
        assert result.content == "Original Content"  # Unchanged
        assert result.description == "Updated Description"  # Changed
    
    def test_update_prompt_all_fields(self):
        """Test updating all fields of prompt."""
        prompt = Prompt(title="Original", content="Content")
        created = storage.create_prompt(prompt)
        
        updated_prompt = created.model_copy(update={
            "title": "New Title",
            "content": "New Content",
            "description": "New Description",
            "collection_id": "col-123"
        })
        result = storage.update_prompt(created.id, updated_prompt)
        
        assert result.title == "New Title"
        assert result.content == "New Content"
        assert result.description == "New Description"
        assert result.collection_id == "col-123"
    
    def test_delete_prompt_exists(self):
        """Test deleting existing prompt."""
        prompt = Prompt(title="Test", content="Content")
        created = storage.create_prompt(prompt)
        
        result = storage.delete_prompt(created.id)
        assert result is True
        assert created.id not in storage._prompts
        assert storage.get_prompt(created.id) is None
    
    def test_delete_prompt_not_exists(self):
        """Test deleting non-existent prompt returns False."""
        result = storage.delete_prompt("nonexistent-id")
        assert result is False


class TestCollectionCRUD:
    """Tests for collection CRUD operations."""
    
    def test_create_collection(self):
        """Test creating a collection."""
        collection = Collection(name="Development")
        created = storage.create_collection(collection)
        
        assert created.id is not None
        assert created.name == "Development"
        assert created.id in storage._collections
    
    def test_create_collection_stores_in_db(self):
        """Test that created collection is stored in database."""
        collection = Collection(name="Test")
        created = storage.create_collection(collection)
        
        stored = storage._collections[created.id]
        assert stored.id == created.id
        assert stored.name == "Test"
    
    def test_get_collection_exists(self):
        """Test getting existing collection."""
        collection = Collection(name="Test")
        created = storage.create_collection(collection)
        
        retrieved = storage.get_collection(created.id)
        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.name == "Test"
    
    def test_get_collection_not_exists(self):
        """Test getting non-existent collection returns None."""
        result = storage.get_collection("nonexistent-id")
        assert result is None
    
    def test_get_all_collections_empty(self):
        """Test getting all collections when empty."""
        storage.clear()
        result = storage.get_all_collections()
        assert result == []
    
    def test_get_all_collections_multiple(self):
        """Test getting all collections with multiple items."""
        storage.clear()
        storage.create_collection(Collection(name="C1"))
        storage.create_collection(Collection(name="C2"))
        storage.create_collection(Collection(name="C3"))
        
        result = storage.get_all_collections()
        assert len(result) == 3
        names = [c.name for c in result]
        assert "C1" in names
        assert "C2" in names
        assert "C3" in names
    
    def test_delete_collection_exists(self):
        """Test deleting existing collection."""
        collection = Collection(name="Test")
        created = storage.create_collection(collection)
        
        result = storage.delete_collection(created.id)
        assert result is True
        assert created.id not in storage._collections
        assert storage.get_collection(created.id) is None
    
    def test_delete_collection_not_exists(self):
        """Test deleting non-existent collection returns False."""
        result = storage.delete_collection("nonexistent-id")
        assert result is False


class TestDataPersistence:
    """Tests for data persistence in memory."""
    
    def test_prompt_persists_after_creation(self):
        """Test that prompt persists in memory after creation."""
        prompt = Prompt(title="Persistent", content="Content")
        created = storage.create_prompt(prompt)
        
        # Retrieve multiple times
        for _ in range(3):
            retrieved = storage.get_prompt(created.id)
            assert retrieved.id == created.id
            assert retrieved.title == "Persistent"
    
    def test_collection_persists_after_creation(self):
        """Test  that collection persists in memory after creation."""
        collection = Collection(name="Persistent")
        created = storage.create_collection(collection)
        
        # Retrieve multiple times
        for _ in range(3):
            retrieved = storage.get_collection(created.id)
            assert retrieved.id == created.id
            assert retrieved.name == "Persistent"
    
    def test_updates_persist(self):
        """Test that updates persist correctly."""
        prompt = Prompt(title="Original", content="Content")
        created = storage.create_prompt(prompt)
        
        updated_prompt = created.model_copy(update={"title": "Updated"})
        storage.update_prompt(created.id, updated_prompt)
        
        retrieved = storage.get_prompt(created.id)
        assert retrieved.title == "Updated"


class TestDataIntegrity:
    """Tests for data integrity in storage."""
    
    def test_prompt_id_uniqueness(self):
        """Test that each prompt gets unique ID."""
        storage.clear()
        p1 = storage.create_prompt(Prompt(title="P1", content="C1"))
        p2 = storage.create_prompt(Prompt(title="P2", content="C2"))
        p3 = storage.create_prompt(Prompt(title="P3", content="C3"))
        
        ids = [p1.id, p2.id, p3.id]
        assert len(ids) == len(set(ids))  # All unique
    
    def test_collection_id_uniqueness(self):
        """Test that each collection gets unique ID."""
        storage.clear()
        c1 = storage.create_collection(Collection(name="C1"))
        c2 = storage.create_collection(Collection(name="C2"))
        c3 = storage.create_collection(Collection(name="C3"))
        
        ids = [c1.id, c2.id, c3.id]
        assert len(ids) == len(set(ids))  # All unique
    
    def test_deleting_prompt_doesnt_affect_others(self):
        """Test that deleting one prompt doesn't affect others."""
        storage.clear()
        p1 = storage.create_prompt(Prompt(title="P1", content="C1"))
        p2 = storage.create_prompt(Prompt(title="P2", content="C2"))
        p3 = storage.create_prompt(Prompt(title="P3", content="C3"))
        
        storage.delete_prompt(p2.id)
        
        assert storage.get_prompt(p1.id) is not None
        assert storage.get_prompt(p2.id) is None
        assert storage.get_prompt(p3.id) is not None
    
    def test_deleting_collection_doesnt_affect_others(self):
        """Test that deleting one collection doesn't affect others."""
        storage.clear()
        c1 = storage.create_collection(Collection(name="C1"))
        c2 = storage.create_collection(Collection(name="C2"))
        c3 = storage.create_collection(Collection(name="C3"))
        
        storage.delete_collection(c2.id)
        
        assert storage.get_collection(c1.id) is not None
        assert storage.get_collection(c2.id) is None
        assert storage.get_collection(c3.id) is not None
    
    def test_updating_prompt_preserves_id(self):
        """Test that updating doesn't change prompt ID."""
        prompt = Prompt(title="Original", content="Content")
        created = storage.create_prompt(prompt)
        original_id = created.id
        
        updated_prompt = created.model_copy(update={"title": "Updated"})
        result = storage.update_prompt(created.id, updated_prompt)
        
        assert result.id == original_id
    
    def test_updating_prompt_preserves_created_at(self):
        """Test that updating doesn't change created_at timestamp."""
        prompt = Prompt(title="Original", content="Content")
        created = storage.create_prompt(prompt)
        original_created_at = created.created_at
        
        updated_prompt = created.model_copy(update={"title": "Updated"})
        result = storage.update_prompt(created.id, updated_prompt)
        
        assert result.created_at == original_created_at


class TestEdgeCases:
    """Tests for edge cases in storage operations."""
    
    def test_create_many_prompts(self):
        """Test creating many prompts."""
        storage.clear()
        count = 100
        
        for i in range(count):
            storage.create_prompt(Prompt(
                title=f"Prompt {i}",
                content=f"Content {i}"
            ))
        
        result = storage.get_all_prompts()
        assert len(result) == count
    
    def test_create_many_collections(self):
        """Test creating many collections."""
        storage.clear()
        count = 50
        
        for i in range(count):
            storage.create_collection(Collection(name=f"Collection {i}"))
        
        result = storage.get_all_collections()
        assert len(result) == count
    
    def test_update_with_empty_update_data(self):
        """Test updating prompt with minimal changes."""
        prompt = Prompt(title="Original", content="Content")
        created = storage.create_prompt(prompt)
        
        # Update with same data
        result = storage.update_prompt(created.id, created)
        
        # Title and content should be unchanged
        assert result.title == "Original"
        assert result.content == "Content"
        # But updated_at should change
        assert result.updated_at >= created.updated_at
    
    def test_create_prompt_with_special_characters(self):
        """Test creating prompt with special characters."""
        prompt = Prompt(
            title="Test @#$% & *()[]",
            content="Content with emoji 🚀 and unicode 你好"
        )
        created = storage.create_prompt(prompt)
        
        retrieved = storage.get_prompt(created.id)
        assert retrieved.title == "Test @#$% & *()[]"
        assert "🚀" in retrieved.content
        assert "你好" in retrieved.content
    
    def test_create_collection_with_special_characters(self):
        """Test creating collection with special characters."""
        collection = Collection(name="Test @#$% & Collection 🎉")
        created = storage.create_collection(collection)
        
        retrieved = storage.get_collection(created.id)
        assert "🎉" in retrieved.name
    
    def test_multiple_updates_to_same_prompt(self):
        """Test multiple sequential updates to same prompt."""
        prompt = Prompt(title="V1", content="Content")
        created = storage.create_prompt(prompt)
        
        p2 = created.model_copy(update={"title": "V2"})
        storage.update_prompt(created.id, p2)
        p3 = p2.model_copy(update={"title": "V3"})
        storage.update_prompt(created.id, p3)
        p4 = p3.model_copy(update={"title": "V4"})
        result = storage.update_prompt(created.id, p4)
        
        assert result.title == "V4"
        
        # Verify it's actually stored
        retrieved = storage.get_prompt(created.id)
        assert retrieved.title == "V4"
