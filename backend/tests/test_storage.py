"""Unit tests for the in-memory storage layer."""

import pytest

from app.models import Collection, Prompt, PromptVersion
from app.storage import Storage


@pytest.fixture
def storage_instance() -> Storage:
    """Return a fresh storage instance for each test."""

    return Storage()


@pytest.fixture
def prompt_factory():
    """Factory for creating Prompt instances with sensible defaults."""

    def _factory(**overrides) -> Prompt:
        data = {
            "title": "Investigate latency spikes",
            "content": "Check metrics, logs, and dependencies",
            "description": "Baseline prompt used across tests",
            "collection_id": None,
        }
        data.update(overrides)
        return Prompt(**data)

    return _factory


@pytest.fixture
def collection_factory():
    """Factory for creating Collection instances with sensible defaults."""

    def _factory(**overrides) -> Collection:
        data = {
            "name": "Default Collection",
            "description": "Used for storage tests",
        }
        data.update(overrides)
        return Collection(**data)

    return _factory


def test_create_prompt_crud_flow(storage_instance: Storage, prompt_factory):
    """Ensure create, read, update, and delete work end-to-end for prompts."""

    prompt = prompt_factory()
    created = storage_instance.create_prompt(prompt)
    assert created.id == prompt.id

    fetched = storage_instance.get_prompt(prompt.id)
    assert fetched is not None
    assert fetched.title == prompt.title

    updated_payload = prompt.model_copy(update={"title": "Updated title"})
    updated = storage_instance.update_prompt(prompt.id, updated_payload)
    assert updated is not None
    assert updated.title == "Updated title"

    all_prompts = storage_instance.get_all_prompts()
    assert len(all_prompts) == 1
    assert all_prompts[0].id == prompt.id

    deleted = storage_instance.delete_prompt(prompt.id)
    assert deleted is True
    assert storage_instance.get_prompt(prompt.id) is None
    assert storage_instance.get_all_prompts() == []


def test_prompts_persist_within_session(storage_instance: Storage, prompt_factory):
    """Verify prompts remain available within the same storage session."""

    first = prompt_factory(title="First prompt")
    second = prompt_factory(title="Second prompt")

    storage_instance.create_prompt(first)
    assert storage_instance.get_prompt(first.id) is first

    storage_instance.create_prompt(second)
    ids_in_store = {prompt.id for prompt in storage_instance.get_all_prompts()}
    assert ids_in_store == {first.id, second.id}

    # Ensure earlier prompts remain readable after additional writes
    persisted_first = storage_instance.get_prompt(first.id)
    assert persisted_first is first
    assert persisted_first.title == "First prompt"


def test_create_prompt_overwrites_existing_identifier(storage_instance: Storage, prompt_factory):
    """Edge case: storing a prompt with an existing ID should overwrite the prior entry."""

    prompt = prompt_factory(title="Original")
    storage_instance.create_prompt(prompt)

    duplicate = prompt.model_copy(update={"title": "Duplicate Title"})
    storage_instance.create_prompt(duplicate)

    stored = storage_instance.get_prompt(prompt.id)
    assert stored is duplicate
    assert stored.title == "Duplicate Title"


def test_delete_prompt_missing_id_returns_false(storage_instance: Storage):
    """Edge case: deleting a non-existent prompt should return False."""

    assert storage_instance.delete_prompt("does-not-exist") is False


def test_update_prompt_missing_id_returns_none(storage_instance: Storage, prompt_factory):
    """Updating a non-existent prompt should return ``None``."""

    prompt = prompt_factory()
    assert storage_instance.update_prompt("missing", prompt) is None


def test_collection_crud_flow(storage_instance: Storage, collection_factory):
    """Ensure collection create/list/get/delete behave as expected."""

    collection = collection_factory()
    created = storage_instance.create_collection(collection)
    assert created.id == collection.id

    fetched = storage_instance.get_collection(collection.id)
    assert fetched is not None
    assert fetched.name == collection.name

    all_collections = storage_instance.get_all_collections()
    assert len(all_collections) == 1
    assert all_collections[0].id == collection.id

    deleted = storage_instance.delete_collection(collection.id)
    assert deleted is True
    assert storage_instance.get_collection(collection.id) is None
    assert storage_instance.get_all_collections() == []


def test_collection_delete_clears_prompt_references(
    storage_instance: Storage,
    prompt_factory,
    collection_factory,
):
    """Deleting a collection should nullify collection_id on associated prompts."""

    collection = storage_instance.create_collection(collection_factory())
    prompt_in_collection = prompt_factory(collection_id=collection.id)
    storage_instance.create_prompt(prompt_in_collection)

    storage_instance.delete_collection(collection.id)

    prompt = storage_instance.get_prompt(prompt_in_collection.id)
    assert prompt is not None
    assert prompt.collection_id is None


def test_get_prompts_by_collection_filters_correctly(
    storage_instance: Storage,
    prompt_factory,
    collection_factory,
):
    """Prompts fetched by collection should exclude non-members."""

    collection = storage_instance.create_collection(collection_factory())
    other_collection = storage_instance.create_collection(
        collection_factory(name="Other Collection")
    )

    in_collection = prompt_factory(collection_id=collection.id)
    other_prompt = prompt_factory(title="Other", collection_id=other_collection.id)
    storage_instance.create_prompt(in_collection)
    storage_instance.create_prompt(other_prompt)

    filtered = storage_instance.get_prompts_by_collection(collection.id)
    assert len(filtered) == 1
    assert filtered[0].id == in_collection.id


def test_delete_collection_missing_id_returns_false(storage_instance: Storage):
    """Edge case: deleting a non-existent collection should return False."""

    assert storage_instance.delete_collection("missing") is False


def test_prompt_version_creation_and_retrieval(
    storage_instance: Storage, prompt_factory
):
    """Version snapshots should be persisted and retrievable per prompt."""

    prompt = storage_instance.create_prompt(prompt_factory())
    version = PromptVersion(
        prompt_id=prompt.id,
        version_number=1,
        title=prompt.title,
        content=prompt.content,
    )
    created = storage_instance.create_prompt_version(version)
    assert created.id == version.id

    versions = storage_instance.get_prompt_versions(prompt.id)
    assert len(versions) == 1
    assert versions[0].version_number == 1

    fetched = storage_instance.get_prompt_version(prompt.id, created.id)
    assert fetched is not None
    assert fetched.id == created.id


def test_get_next_version_number_increments_per_prompt(
    storage_instance: Storage, prompt_factory
):
    """Version numbers should increment sequentially per prompt."""

    prompt = storage_instance.create_prompt(prompt_factory())
    assert storage_instance.get_next_version_number(prompt.id) == 1

    storage_instance.create_prompt_version(
        PromptVersion(
            prompt_id=prompt.id,
            version_number=1,
            title=prompt.title,
            content=prompt.content,
        )
    )
    assert storage_instance.get_next_version_number(prompt.id) == 2


def test_deleting_prompt_removes_versions(
    storage_instance: Storage, prompt_factory
):
    """Deleting a prompt should also remove its stored versions."""

    prompt = storage_instance.create_prompt(prompt_factory())
    storage_instance.create_prompt_version(
        PromptVersion(
            prompt_id=prompt.id,
            version_number=1,
            title=prompt.title,
            content=prompt.content,
        )
    )

    assert storage_instance.delete_prompt(prompt.id) is True
    assert storage_instance.get_prompt_versions(prompt.id) == []
