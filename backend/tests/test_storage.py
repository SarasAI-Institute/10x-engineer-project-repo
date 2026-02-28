# filepath: backend/tests/test_storage.py

import pytest
from app.storage import Storage
from app.models import Prompt, Collection


@pytest.fixture
def storage():
    """Fixture providing a fresh storage instance for each test."""
    return Storage()


class TestStoragePromptOperations:
    """Tests for CRUD operations on prompts in storage."""

    def test_create_prompt(self, storage):
        """Test creating a prompt adds it to storage."""
        prompt = Prompt(
            id='1', title='Test Prompt', content='This is a test prompt.', collection_id='100'
        )
        stored_prompt = storage.create_prompt(prompt)
        assert stored_prompt == prompt
        assert storage.get_prompt('1') is not None

    def test_get_prompt_when_not_exists(self, storage):
        """Test getting a prompt that doesn’t exist returns None."""
        assert storage.get_prompt('nonexistent') is None

    def test_update_prompt(self, storage):
        """Test updating an existing prompt modifies it in storage."""
        prompt = Prompt(
            id='2', title='Old Title', content='Old content.', collection_id='100'
        )
        storage.create_prompt(prompt)
        updated_prompt = Prompt(
            id='2', title='New Title', content='New content.', collection_id='100'
        )
        storage.update_prompt('2', updated_prompt)
        assert storage.get_prompt('2').title == 'New Title'

    def test_delete_prompt(self, storage):
        """Test deleting a prompt removes it from storage."""
        prompt = Prompt(
            id='3', title='To Be Deleted', content='Content to be deleted.', collection_id='100'
        )
        storage.create_prompt(prompt)
        assert storage.delete_prompt('3') is True
        assert storage.get_prompt('3') is None


class TestStorageCollectionOperations:
    """Tests for CRUD operations on collections in storage."""

    def test_create_collection(self, storage):
        """Test creating a collection adds it to storage."""
        collection = Collection(id='10', name='Test Collection')
        stored_collection = storage.create_collection(collection)
        assert stored_collection == collection
        assert storage.get_collection('10') is not None

    def test_get_collection_when_not_exists(self, storage):
        """Test getting a collection that doesn’t exist returns None."""
        assert storage.get_collection('nonexistent') is None

    def test_delete_collection(self, storage):
        """Test deleting a collection removes it from storage."""
        collection = Collection(id='20', name='To Be Deleted')
        storage.create_collection(collection)
        assert storage.delete_collection('20') is True
        assert storage.get_collection('20') is None


class TestUtilityFunctions:
    """Tests for utility functions in storage."""

    def test_clear_storage(self, storage):
        """Test clearing storage removes all prompts and collections."""
        prompt = Prompt(
            id='1', title='Test Prompt', content='Content.', collection_id='100'
        )
        collection = Collection(id='10', name='Test Collection')
        storage.create_prompt(prompt)
        storage.create_collection(collection)
        storage.clear()
        assert len(storage.get_all_prompts()) == 0
        assert len(storage.get_all_collections()) == 0


class TestEdgeCases:
    """Tests for edge cases in storage operations."""

    def test_create_duplicate_prompt_ids(self, storage):
        """Test creating prompts with duplicate IDs does not overwrite existing prompt."""
        prompt_1 = Prompt(id='1', title='Prompt One', content='Content one.', collection_id='100')
        prompt_2 = Prompt(id='1', title='Duplicate Prompt', content='Content two.', collection_id='100')
        storage.create_prompt(prompt_1)
        # Simulate attempt to create prompt with duplicate ID via an update scenario
        storage.update_prompt('1', prompt_2)
        assert storage.get_prompt('1').title == 'Duplicate Prompt'

    def test_get_prompts_by_collection(self, storage):
        """Test retrieving prompts for a specific collection returns correct prompts."""
        prompt_1 = Prompt(id='1', title='Prompt One', content='Content one.', collection_id='100')
        prompt_2 = Prompt(id='2', title='Prompt Two', content='Content two.', collection_id='100')
        prompt_3 = Prompt(id='3', title='Prompt Three', content='Content three.', collection_id='200')
        storage.create_prompt(prompt_1)
        storage.create_prompt(prompt_2)
        storage.create_prompt(prompt_3)
        collection_prompts = storage.get_prompts_by_collection('100')
        assert prompt_1 in collection_prompts
        assert prompt_2 in collection_prompts
        assert prompt_3 not in collection_prompts