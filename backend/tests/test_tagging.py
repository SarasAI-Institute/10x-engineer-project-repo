import pytest
from app.models import Tag, PromptWithTags, generate_id

class TestTagModel:
    """Tests for the Tag model."""

    def test_tag_creation_success(self):
        """Test creating a valid Tag instance."""
        tag = Tag(id=generate_id(), name="AI")
        assert tag.name == "AI"
        assert isinstance(tag.id, str)


class TestPromptWithTagsModel:
    """Tests for the PromptWithTags model."""

    def test_prompt_with_tags_creation(self):
        """Test creating a PromptWithTags instance with tags."""
        prompt = PromptWithTags(
            title="AI Basics",
            content="Understanding the basics of AI",
            tags=[Tag(id=generate_id(), name="AI"), Tag(id=generate_id(), name="Introduction")]
        )
        assert len(prompt.tags) == 2
        assert prompt.tags[0].name == "AI"
        assert prompt.tags[1].name == "Introduction"

    def test_add_tag_to_prompt_success(self):
        """Test adding a tag to a PromptWithTags instance."""
        prompt = PromptWithTags(title="AI Basics", content="Content")
        new_tag = Tag(id=generate_id(), name="New Tag")
        prompt.tags.append(new_tag)
        assert len(prompt.tags) == 1
        assert prompt.tags[0].name == "New Tag"

    def test_remove_tag_from_prompt_success(self):
        """Test removing a tag from a PromptWithTags instance."""
        prompt = PromptWithTags(
            title="AI Basics",
            content="Content",
            tags=[Tag(id=generate_id(), name="AI")]
        )
        prompt.tags.pop()
        assert len(prompt.tags) == 0
