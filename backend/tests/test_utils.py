"""Unit tests for ``app.utils`` helpers."""

from datetime import datetime

import pytest

from app.models import Prompt
from app.utils import (
    sort_prompts_by_date,
    filter_prompts_by_collection,
    search_prompts,
    validate_prompt_content,
    extract_variables,
)


@pytest.fixture
def prompt_factory():
    """Return a factory that builds ``Prompt`` instances with sensible defaults."""

    def _factory(**overrides):
        base_time = datetime(2024, 1, 1)
        payload = {
            "title": "Sample",
            "content": "Prompt body content",
            "description": "Sample description",
            "collection_id": "alpha",
            "created_at": base_time,
            "updated_at": base_time,
        }
        payload.update(overrides)
        return Prompt(**payload)

    return _factory


class TestSortPromptsByDate:
    """Tests for ``sort_prompts_by_date`` utility."""

    def test_sort_prompts_by_date_descending_returns_newest_first(self, prompt_factory):
        older = prompt_factory(title="Old", updated_at=datetime(2024, 1, 1))
        newer = prompt_factory(title="New", updated_at=datetime(2024, 5, 1))

        ordered = sort_prompts_by_date([older, newer], descending=True)

        assert [prompt.title for prompt in ordered] == ["New", "Old"]

    def test_sort_prompts_by_date_ascending_when_flag_false(self, prompt_factory):
        first = prompt_factory(title="First", updated_at=datetime(2024, 1, 1))
        second = prompt_factory(title="Second", updated_at=datetime(2024, 2, 1))

        ordered = sort_prompts_by_date([second, first])

        assert [prompt.title for prompt in ordered] == ["First", "Second"]

    def test_sort_prompts_by_date_handles_empty_iterable(self):
        assert sort_prompts_by_date([], descending=True) == []


class TestFilterPromptsByCollection:
    """Tests for ``filter_prompts_by_collection`` utility."""

    def test_filter_prompts_by_collection_returns_only_matching_prompts(self, prompt_factory):
        alpha_prompt = prompt_factory(title="Alpha", collection_id="alpha")
        beta_prompt = prompt_factory(title="Beta", collection_id="beta")

        filtered = filter_prompts_by_collection([alpha_prompt, beta_prompt], "alpha")

        assert len(filtered) == 1
        assert filtered[0].title == "Alpha"

    def test_filter_prompts_by_collection_handles_no_matches(self, prompt_factory):
        prompts = [prompt_factory(collection_id="alpha")]

        assert filter_prompts_by_collection(prompts, "missing") == []


class TestSearchPrompts:
    """Tests for ``search_prompts`` utility."""

    def test_search_prompts_matches_title_and_description_case_insensitively(self, prompt_factory):
        title_prompt = prompt_factory(title="Greeting", description="Say hello")
        description_prompt = prompt_factory(title="Salute", description="Warm HELLO from afar")
        unrelated_prompt = prompt_factory(title="Farewell", description="Says goodbye")

        results = search_prompts([title_prompt, description_prompt, unrelated_prompt], "hello")

        assert {prompt.title for prompt in results} == {"Greeting", "Salute"}

    def test_search_prompts_ignores_missing_descriptions(self, prompt_factory):
        prompt_without_description = prompt_factory(title="Plain", description=None)

        assert search_prompts([prompt_without_description], "anything") == []


class TestValidatePromptContent:
    """Tests for ``validate_prompt_content`` utility."""

    def test_validate_prompt_content_rejects_blank_or_whitespace_strings(self):
        assert validate_prompt_content("") is False
        assert validate_prompt_content("   \n \t") is False

    def test_validate_prompt_content_enforces_minimum_length(self):
        assert validate_prompt_content("short txt") is False  # 9 characters after trim

    def test_validate_prompt_content_accepts_valid_strings(self):
        assert validate_prompt_content("Sufficient body text") is True


class TestExtractVariables:
    """Tests for ``extract_variables`` utility."""

    def test_extract_variables_returns_all_placeholders_in_order(self):
        content = "Use {{first}} then {{second}} and finally {{third}}"
        assert extract_variables(content) == ["first", "second", "third"]

    def test_extract_variables_returns_empty_for_missing_placeholders(self):
        assert extract_variables("No variables here") == []
