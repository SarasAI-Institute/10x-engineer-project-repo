from app.storage import Storage
from app.models import Prompt, Collection


def test_create_and_get_prompt():
    storage = Storage()

    prompt = Prompt(title="Test", content="valid content here")
    storage.create_prompt(prompt)

    result = storage.get_prompt(prompt.id)
    assert result is not None
    assert result.title == "Test"


def test_update_prompt():
    storage = Storage()

    prompt = Prompt(title="Old", content="valid content here")
    storage.create_prompt(prompt)

    updated = Prompt(
        id=prompt.id,
        title="New",
        content="updated content",
        description=None,
        collection_id=None,
        created_at=prompt.created_at,
        updated_at=prompt.updated_at
    )

    result = storage.update_prompt(prompt.id, updated)

    assert result.title == "New"


def test_delete_prompt():
    storage = Storage()

    prompt = Prompt(title="Test", content="valid content here")
    storage.create_prompt(prompt)

    assert storage.delete_prompt(prompt.id) is True
    assert storage.get_prompt(prompt.id) is None


def test_create_and_get_collection():
    storage = Storage()

    collection = Collection(name="Test")
    storage.create_collection(collection)

    result = storage.get_collection(collection.id)
    assert result is not None


def test_get_prompts_by_collection():
    storage = Storage()

    collection = Collection(name="Test")
    storage.create_collection(collection)

    prompt = Prompt(
        title="Test",
        content="valid content here",
        collection_id=collection.id
    )
    storage.create_prompt(prompt)

    results = storage.get_prompts_by_collection(collection.id)
    assert len(results) == 1