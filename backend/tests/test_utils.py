import pytest
from datetime import datetime, timedelta
from app.models import Prompt, PromptUpdate
from app.utils import (
    sort_prompts_by_date,
    filter_prompts_by_collection,
    search_prompts,
    validate_prompt_content,
    extract_variables,
    apply_partial_updates,
    validate_prompt_id
)

class TestUtils:
    """Tests for utility functions."""

    def test_sort_prompts_by_date(self):
        """Test sorting prompts by creation date."""
        prompts = [
            Prompt(title="Prompt 2", content="Content 2", created_at=datetime(2023, 1, 2)),
            Prompt(title="Prompt 1", content="Content 1", created_at=datetime(2023, 1, 1))
        ]
        sorted_prompts = sort_prompts_by_date(prompts)
        assert sorted_prompts[0].title == "Prompt 2"
        sorted_prompts_asc = sort_prompts_by_date(prompts, descending=False)
        assert sorted_prompts_asc[0].title == "Prompt 1"

    def test_filter_prompts_by_collection(self):
        """Test filtering prompts by collection ID."""
        prompts = [
            Prompt(title="Prompt 1", content="Content 1", collection_id="123"),
            Prompt(title="Prompt 2", content="Content 2", collection_id="456")
        ]
        filtered = filter_prompts_by_collection(prompts, "123")
        assert len(filtered) == 1
        assert filtered[0].collection_id == "123"

    def test_search_prompts(self):
        """Test searching prompts by title or description."""
        prompts = [
            Prompt(title="Daily Standup", content="Discuss daily progress"),
            Prompt(title="Project Planning", content="Plan the next milestones")
        ]
        query = "daily"
        matching_prompts = search_prompts(prompts, query)
        assert len(matching_prompts) == 1
        assert matching_prompts[0].title == "Daily Standup"

    def test_validate_prompt_content(self):
        """Test validation of prompt content."""
        assert validate_prompt_content("Hello, world!") is True
        assert validate_prompt_content("   ") is False
        assert validate_prompt_content("Short") is False

    def test_extract_variables(self):
        """Test extraction of template variables from content."""
        content = "Hello {{user}}, you have {{count}} new messages."
        variables = extract_variables(content)
        assert variables == ['user', 'count']
        assert extract_variables("No variables here.") == []

    def test_apply_partial_updates(self):
        """Test applying partial updates to a prompt."""
        existing_prompt = Prompt(title="Old Title", content="Old Content", updated_at=datetime(2023, 1, 1))
        updates = PromptUpdate(title="New Title")
        updated_prompt = apply_partial_updates(existing_prompt, updates)
        assert updated_prompt.title == "New Title"
        assert updated_prompt.content == "Old Content"

    def test_validate_prompt_id(self):
        """Test validation of prompt IDs."""
        assert validate_prompt_id("valid-id-123") == (True, None)
        assert validate_prompt_id("invalid id") == (False, "Malformed prompt ID")
        assert validate_prompt_id("a" * 256) == (False, "Invalid ID format")
