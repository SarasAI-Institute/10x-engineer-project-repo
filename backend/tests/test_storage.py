from typing import Collection

import pytest
from app.storage import Storage
from app.models import Prompt
from app.models import Collection


def test_create_prompt():
    # Arrange
    storage = Storage()
    new_prompt = Prompt(
        id='prompt_123',
        title='New Prompt',
        content='This is test content',   # Additional content field
        collection_id='collection_123',
    )

    # Act
    stored_prompt = storage.create_prompt(new_prompt)

    # Assert
    assert stored_prompt == new_prompt
    assert storage._prompts[new_prompt.id] == new_prompt


def test_get_prompt():
    # Arrange
    storage = Storage()
    existing_prompt = Prompt(
        id='prompt_123',
        title='Existing Prompt',
        content='Sample content',  # Ensure content or necessary fields are provided
        collection_id='collection_123'
    )
    storage._prompts[existing_prompt.id] = existing_prompt

    # Act & Assert
    # Case 1: Prompt exists
    retrieved_prompt = storage.get_prompt('prompt_123')
    assert retrieved_prompt == existing_prompt

    # Case 2: Prompt does not exist
    retrieved_prompt_none = storage.get_prompt('non_existent_id')
    assert retrieved_prompt_none is None

    # Edge Case 1: Empty ID
    retrieved_prompt_empty = storage.get_prompt('')
    assert retrieved_prompt_empty is None

    # Edge Case 2: None ID - You may want to explicitly handle None in the method if it doesn't capture this safely
    retrieved_prompt_none_id = storage.get_prompt(None)
    assert retrieved_prompt_none_id is None

    # Edge Case 3: Whitespace ID
    retrieved_prompt_whitespace = storage.get_prompt('   ')
    assert retrieved_prompt_whitespace is None

    # Edge Case 4: Special Characters in ID
    retrieved_prompt_special_chars = storage.get_prompt('!@#$%^&*()')
    assert retrieved_prompt_special_chars is None




def test_get_all_prompts():
    # Arrange
    storage = Storage()
    
    # Act & Assert for empty storage
    assert storage.get_all_prompts() == []

    # Arrange a single prompt
    prompt1 = Prompt(id='prompt_1', title='First Prompt', content='Content 1', collection_id='collection_A')
    storage.create_prompt(prompt1)

    # Act & Assert for single prompt
    all_prompts = storage.get_all_prompts()
    assert len(all_prompts) == 1
    assert all_prompts[0] == prompt1

    # Arrange multiple prompts
    prompt2 = Prompt(id='prompt_2', title='Second Prompt', content='Content 2', collection_id='collection_B')
    storage.create_prompt(prompt2)

    # Act & Assert for multiple prompts
    all_prompts = storage.get_all_prompts()
    assert len(all_prompts) == 2
    assert prompt1 in all_prompts
    assert prompt2 in all_prompts

    # Arrange duplicate content, different ID
    duplicate_prompt = Prompt(id='prompt_3', title='First Prompt', content='Content 1', collection_id='collection_A')
    storage.create_prompt(duplicate_prompt)
    
    # Act & Assert for duplicate content
    all_prompts = storage.get_all_prompts()
    assert len(all_prompts) == 3
    assert duplicate_prompt in all_prompts



def test_update_prompt():
    # Arrange
    storage = Storage()

    # Add a prompt to the storage to update later
    initial_prompt = Prompt(id='prompt_123', title='Initial Title', content='Initial Content', collection_id='collection_123')
    storage.create_prompt(initial_prompt)

    # Act & Assert for updating an existing prompt
    updated_prompt = Prompt(id='prompt_123', title='Updated Title', content='Updated Content', collection_id='collection_123')
    result = storage.update_prompt('prompt_123', updated_prompt)
    assert result == updated_prompt
    assert storage._prompts['prompt_123'].title == 'Updated Title'
    assert storage._prompts['prompt_123'].content == 'Updated Content'

    # Act & Assert for updating a non-existent prompt
    non_existent_update = Prompt(id='prompt_456', title='Non-existent', content='Non-existent Content', collection_id='collection_xyz')
    result_none = storage.update_prompt('prompt_456', non_existent_update)
    assert result_none is None
    assert 'prompt_456' not in storage._prompts



def test_delete_prompt():
    # Arrange
    storage = Storage()

    # Add a prompt to the storage
    prompt = Prompt(id='prompt_123', title='Sample Prompt', content='Sample Content', collection_id='collection_123')
    storage.create_prompt(prompt)

    # Act & Assert for deleting an existing prompt
    result = storage.delete_prompt('prompt_123')
    assert result is True
    assert 'prompt_123' not in storage._prompts

    # Act & Assert for deleting a non-existent prompt
    result_none = storage.delete_prompt('non_existent_id')
    assert result_none is False

    # Act & Assert for deleting a prompt already deleted
    result_again = storage.delete_prompt('prompt_123')
    assert result_again is False



def test_create_collection():
    # Arrange
    storage = Storage()
    
    # Act & Assert for creating a new collection
    new_collection = Collection(id='collection_123', name='First Collection')
    stored_collection = storage.create_collection(new_collection)
    assert stored_collection == new_collection
    assert storage._collections[new_collection.id] == new_collection

    # Act & Assert for creating a collection with an existing ID
    duplicate_collection = Collection(id='collection_123', name='Updated Collection')
    updated_collection = storage.create_collection(duplicate_collection)
    assert updated_collection == duplicate_collection
    assert storage._collections[duplicate_collection.id] == duplicate_collection



    import pytest
from app.storage import Storage
from app.models import Collection

def test_get_collection():
    # Arrange
    storage = Storage()

    # Create and add a collection to the storage
    collection = Collection(id='collection_123', name='Sample Collection')
    storage.create_collection(collection)

    # Act & Assert: Retrieve existing collection
    retrieved_collection = storage.get_collection('collection_123')
    assert retrieved_collection == collection

    # Act & Assert: Attempt to retrieve a non-existent collection
    non_existent_collection = storage.get_collection('non_existent_id')
    assert non_existent_collection is None

    # Edge Case 1: Empty ID
    retrieved_empty_id = storage.get_collection('')
    assert retrieved_empty_id is None

    # Edge Case 2: Special Characters in ID
    special_char_id = storage.get_collection('!@#$%^&*()')
    assert special_char_id is None

    # Edge Case 3: Whitespace ID
    whitespace_id = storage.get_collection('   ')
    assert whitespace_id is None



    import pytest
from app.storage import Storage
from app.models import Collection

def test_get_all_collections():
    # Arrange
    storage = Storage()
    
    # Act & Assert for empty storage
    assert storage.get_all_collections() == []

    # Arrange a single collection
    collection1 = Collection(id='collection_1', name='First Collection')
    storage.create_collection(collection1)

    # Act & Assert for single collection
    all_collections = storage.get_all_collections()
    assert len(all_collections) == 1
    assert all_collections[0] == collection1

    # Arrange multiple collections
    collection2 = Collection(id='collection_2', name='Second Collection')
    storage.create_collection(collection2)

    # Act & Assert for multiple collections
    all_collections = storage.get_all_collections()
    assert len(all_collections) == 2
    assert collection1 in all_collections
    assert collection2 in all_collections




    import pytest
from app.storage import Storage
from app.models import Prompt, Collection

def test_get_prompts_by_collection():
    # Arrange
    storage = Storage()
    
    # Create collections and prompts
    collection1 = Collection(id='collection_123', name='Collection One')
    collection2 = Collection(id='collection_456', name='Collection Two')
    storage.create_collection(collection1)
    storage.create_collection(collection2)

    prompt1 = Prompt(id='prompt_1', title='Prompt One', content='Content One', collection_id='collection_123')
    prompt2 = Prompt(id='prompt_2', title='Prompt Two', content='Content Two', collection_id='collection_123')
    prompt3 = Prompt(id='prompt_3', title='Prompt Three', content='Content Three', collection_id='collection_456')

    storage.create_prompt(prompt1)
    storage.create_prompt(prompt2)
    storage.create_prompt(prompt3)

    # Act & Assert: Retrieve prompts for a specific collection
    collection1_prompts = storage.get_prompts_by_collection('collection_123')
    assert len(collection1_prompts) == 2
    assert prompt1 in collection1_prompts
    assert prompt2 in collection1_prompts

    # Act & Assert: No prompts for a specific collection
    empty_collection_prompts = storage.get_prompts_by_collection('collection_nonexistent')
    assert empty_collection_prompts == []

    # Act & Assert: Retrieve prompts for another collection with some prompts
    collection2_prompts = storage.get_prompts_by_collection('collection_456')
    assert len(collection2_prompts) == 1
    assert prompt3 in collection2_prompts



def test_clear_storage():
    # Arrange
    storage = Storage()
    
    # Populate with some prompts and collections
    prompt1 = Prompt(id='prompt_1', title='Prompt One', content='Content One', collection_id='collection_1')
    prompt2 = Prompt(id='prompt_2', title='Prompt Two', content='Content Two', collection_id='collection_2')
    collection1 = Collection(id='collection_1', name='Collection One')
    collection2 = Collection(id='collection_2', name='Collection Two')

    storage.create_prompt(prompt1)
    storage.create_prompt(prompt2)
    storage.create_collection(collection1)
    storage.create_collection(collection2)

    # Act: Clear the storage
    storage.clear()

    # Assert: Check that both prompts and collections storage are empty
    assert len(storage._prompts) == 0
    assert len(storage._collections) == 0