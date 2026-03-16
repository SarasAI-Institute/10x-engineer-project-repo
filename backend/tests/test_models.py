"""Pydantic model tests for PromptLab."""

from datetime import datetime

import pytest
from pydantic import ValidationError

from app.models import (
    Prompt,
    PromptCreate,
    PromptPatch,
    PromptUpdate,
    PromptVersion,
    Collection,
    CollectionCreate,
)


class TestPromptModel:
    """Validation, default, and serialization checks for ``Prompt`` models."""

    def test_prompt_defaults_generate_identifiers_and_timestamps(self):
        prompt = Prompt(title="Test", content="Prompt body")

        assert isinstance(prompt.id, str)
        assert prompt.id
        assert isinstance(prompt.created_at, datetime)
        assert isinstance(prompt.updated_at, datetime)
        assert prompt.updated_at >= prompt.created_at
        assert prompt.description is None
        assert prompt.collection_id is None

    def test_prompt_validation_enforces_title_and_content_constraints(self):
        with pytest.raises(ValidationError):
            Prompt(title="", content="Valid content")
        with pytest.raises(ValidationError):
            Prompt(title="Valid", content="")

    def test_prompt_current_version_defaults_to_zero(self):
        prompt = Prompt(title="Versioned", content="Content")
        assert prompt.current_version == 0

    def test_prompt_serialization_round_trip(self):
        original = Prompt(
            title="Serializable",
            content="Serializable body",
            description="Desc",
            collection_id="col-1",
        )
        payload = original.model_dump()
        recreated = Prompt(**payload)

        assert recreated.id == original.id
        assert recreated.title == original.title
        assert recreated.description == original.description
        assert recreated.collection_id == "col-1"

    def test_prompt_patch_only_updates_provided_fields(self):
        base = Prompt(title="Base", content="Original content")
        patch = PromptPatch(title="Updated")
        updated = base.model_copy(update=patch.model_dump(exclude_unset=True))

        assert updated.title == "Updated"
        assert updated.content == base.content

    def test_prompt_update_requires_all_fields(self):
        with pytest.raises(ValidationError):
            PromptUpdate(title="Only title")


class TestCollectionModel:
    """Validation and defaults for collection models."""

    def test_collection_defaults_generate_identifier_and_timestamp(self):
        collection = Collection(name="Research", description="Notes")

        assert isinstance(collection.id, str)
        assert collection.id
        assert isinstance(collection.created_at, datetime)
        assert collection.name == "Research"
        assert collection.description == "Notes"

    def test_collection_validation_rejects_blank_name(self):
        with pytest.raises(ValidationError):
            Collection(name="", description="Invalid")

    def test_collection_serialization_round_trip(self):
        original = Collection(name="Alpha")
        payload = original.model_dump()
        recreated = Collection(**payload)

        assert recreated.id == original.id
        assert recreated.created_at == original.created_at

    def test_collection_create_model_requires_name(self):
        with pytest.raises(ValidationError):
            CollectionCreate()


class TestPromptVersionModel:
    """PromptVersion schema validation tests."""

    def test_prompt_version_defaults_editor_and_timestamps(self):
        version = PromptVersion(
            prompt_id="prompt-1",
            version_number=1,
            title="Snapshot",
            content="Snapshot body",
        )
        assert version.editor == "system"
        assert version.change_note is None
        assert version.created_at <= datetime.utcnow()


class TestPromptCreateModel:
    """Tests for request-oriented prompt schemas."""

    def test_prompt_create_accepts_optional_description_and_collection(self):
        data = {
            "title": "Prompt",
            "content": "Body",
            "description": "Desc",
            "collection_id": "col-1",
        }
        prompt_create = PromptCreate(**data)

        assert prompt_create.description == "Desc"
        assert prompt_create.collection_id == "col-1"

    def test_prompt_create_rejects_blank_title(self):
        with pytest.raises(ValidationError):
            PromptCreate(title="", content="Body")


class TestPromptUpdateAndPatchModels:
    """Tests for change note behavior on PUT/PATCH schemas."""

    def test_prompt_update_accepts_optional_change_note(self):
        payload = PromptUpdate(
            title="Updated",
            content="Updated content",
            description="Desc",
            change_note="Reason",
        )
        assert payload.change_note == "Reason"

    def test_prompt_update_rejects_long_change_note(self):
        with pytest.raises(ValidationError):
            PromptUpdate(
                title="Updated",
                content="Updated content",
                description="Desc",
                change_note="x" * 256,
            )

    def test_prompt_patch_accepts_partial_change_note(self):
        payload = PromptPatch(change_note="Short reason")
        assert payload.change_note == "Short reason"

    def test_prompt_patch_rejects_long_change_note(self):
        with pytest.raises(ValidationError):
            PromptPatch(change_note="x" * 512)
