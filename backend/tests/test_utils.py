import pytest
from datetime import datetime, timedelta
from app.models import Prompt
from app.utils import sort_prompts_by_date, filter_prompts_by_collection, search_prompts, validate_prompt_content, extract_variables


class TestSortPromptsByDate:

    def test_sort_prompts_success(self):
        """Test that prompts are sorted by date in descending order by default."""
        prompt1 = Prompt(title="Prompt 1", content="Content 1", created_at=datetime.utcnow())
        prompt2 = Prompt(title="Prompt 2", content="Content 2", created_at=datetime.utcnow() - timedelta(days=1))
        prompt3 = Prompt(title="Prompt 3", content="Content 3", created_at=datetime.utcnow() - timedelta(days=2))

        prompts = [prompt1, prompt2, prompt3]
        sorted_prompts = sort_prompts_by_date(prompts)

        assert sorted_prompts == [prompt1, prompt2, prompt3]
        assert sorted_prompts[0].created_at > sorted_prompts[-1].created_at

    def test_sort_prompts_ascending(self):
        """Test sorting prompts in ascending order of creation date."""
        prompt1 = Prompt(title="Prompt 1", content="Content 1", created_at=datetime.utcnow() - timedelta(days=2))
        prompt2 = Prompt(title="Prompt 2", content="Content 2", created_at=datetime.utcnow() - timedelta(days=1))
        prompt3 = Prompt(title="Prompt 3", content="Content 3", created_at=datetime.utcnow())

        prompts = [prompt1, prompt2, prompt3]
        sorted_prompts = sort_prompts_by_date(prompts, descending=False)

        assert sorted_prompts == [prompt1, prompt2, prompt3]
        assert sorted_prompts[0].created_at < sorted_prompts[-1].created_at

    def test_sort_prompts_empty(self):
        """Test sorting an empty list of prompts."""
        prompts = []
        sorted_prompts = sort_prompts_by_date(prompts)
        assert sorted_prompts == []

    def test_sort_prompts_identical_dates(self):
        """Test sorting prompts with identical creation dates."""
        created_time = datetime.utcnow()
        prompt1 = Prompt(title="Prompt 1", content="Content 1", created_at=created_time)
        prompt2 = Prompt(title="Prompt 2", content="Content 2", created_at=created_time)
        prompt3 = Prompt(title="Prompt 3", content="Content 3", created_at=created_time)

        prompts = [prompt1, prompt2, prompt3]
        sorted_prompts = sort_prompts_by_date(prompts)

        # With identical dates, order should match input order
        assert sorted_prompts == [prompt1, prompt2, prompt3]

class TestFilterPromptsByCollection:

    def test_filter_prompts_success(self):
        """Test filtering prompts by a valid collection ID."""
        prompt1 = Prompt(title="Prompt 1", content="Content 1", collection_id="collection_1")
        prompt2 = Prompt(title="Prompt 2", content="Content 2", collection_id="collection_2")
        prompt3 = Prompt(title="Prompt 3", content="Content 3", collection_id="collection_1")

        prompts = [prompt1, prompt2, prompt3]
        filtered_prompts = filter_prompts_by_collection(prompts, "collection_1")

        assert len(filtered_prompts) == 2
        assert all(p.collection_id == "collection_1" for p in filtered_prompts)

    def test_filter_prompts_no_matches(self):
        """Test filtering prompts with no matches for collection ID."""
        prompt1 = Prompt(title="Prompt 1", content="Content 1", collection_id="collection_1")
        prompt2 = Prompt(title="Prompt 2", content="Content 2", collection_id="collection_1")

        prompts = [prompt1, prompt2]
        filtered_prompts = filter_prompts_by_collection(prompts, "non_existent_collection")

        assert len(filtered_prompts) == 0

    def test_filter_prompts_empty(self):
        """Test filtering an empty list of prompts."""
        prompts = []
        filtered_prompts = filter_prompts_by_collection(prompts, "collection_1")
        assert filtered_prompts == []

    def test_filter_prompts_partial_invalid(self):
        """Test list containing prompts without collection_id or invalid collection_id."""
        prompt1 = Prompt(title="Prompt 1", content="Content 1", collection_id=None)  # Invalid
        prompt2 = Prompt(title="Prompt 2", content="Content 2", collection_id="collection_2")

        prompts = [prompt1, prompt2]
        filtered_prompts = filter_prompts_by_collection(prompts, "collection_1")

        assert len(filtered_prompts) == 0  # No valid collection match

class TestSearchPrompts:

    def test_search_prompts_success(self):
        """Test searching prompts successfully with matching queries."""
        prompt1 = Prompt(title="Introduction to Python", content="Content 1", description="Beginner-friendly intro")
        prompt2 = Prompt(title="Advanced Python", content="Content 2", description="Advanced topics in Python")
        prompt3 = Prompt(title="JavaScript Guide", content="Content 3", description="Basics of JavaScript")

        prompts = [prompt1, prompt2, prompt3]
        search_results = search_prompts(prompts, "Python")

        assert len(search_results) == 2
        assert all("Python" in p.title or "Python" in (p.description or "") for p in search_results)

    def test_search_prompts_case_insensitivity(self):
        """Test that search is case-insensitive."""
        prompt1 = Prompt(title="Data Science with Python", content="Content 1")
        prompt2 = Prompt(title="Python for Data Analysis", content="Content 2")

        prompts = [prompt1, prompt2]
        search_results = search_prompts(prompts, "python")

        assert len(search_results) == 2

        search_results = search_prompts(prompts, "PYTHON")
        assert len(search_results) == 2

    def test_search_prompts_no_matches(self):
        """Test searching prompts with no matching query results."""
        prompt1 = Prompt(title="Data Science", content="Content 1")
        prompt2 = Prompt(title="Machine Learning", content="Content 2")

        prompts = [prompt1, prompt2]
        search_results = search_prompts(prompts, "JavaScript")

        assert len(search_results) == 0

    def test_search_prompts_empty(self):
        """Test searching an empty list of prompts."""
        prompts = []
        search_results = search_prompts(prompts, "Python")
        assert search_results == []

class TestValidatePromptContent:

    def test_validate_prompt_content_success(self):
        """Test content that should be valid."""
        valid_content = "This is a valid prompt with sufficient length."
        assert validate_prompt_content(valid_content) is True

    def test_validate_prompt_content_minimum_length(self):
        """Test content right at the minimum valid length (10)."""
        min_length_content = "1234567890"  # Exactly 10 characters
        assert validate_prompt_content(min_length_content) is True

    def test_validate_prompt_content_empty_string(self):
        """Test empty string content."""
        empty_content = ""
        assert validate_prompt_content(empty_content) is False

    def test_validate_prompt_content_whitespace_only(self):
        """Test content with only whitespace characters."""
        whitespace_content = " " * 10
        assert validate_prompt_content(whitespace_content) is False

    def test_validate_prompt_content_too_short(self):
        """Test content that is too short."""
        short_content = "Too short"
        assert validate_prompt_content(short_content) is False

    def test_validate_prompt_content_partial_space(self):
        """Test content with leading or trailing spaces."""
        content_with_spaces = "    Valid content with spaces    "
        assert validate_prompt_content(content_with_spaces) is True

class TestExtractVariables:

    def test_extract_variables_success(self):
        """Test successful extraction of variables from valid content."""
        content = "Hello, {{name}}! Your ID is {{id_number}}."
        expected_variables = ["name", "id_number"]
        assert extract_variables(content) == expected_variables
    
    def test_extract_variables_no_variables(self):
        """Test content with no extractable variables."""
        content = "Hello, World! No variables here."
        assert extract_variables(content) == []

    def test_extract_variables_malformed(self):
        """Test content with malformed variables."""
        content = "Hello, {{name}! Unfinished {{variable and a {{another"
        assert extract_variables(content) == []

    def test_extract_variables_empty_input(self):
        """Test extraction from an empty string."""
        content = ""
        assert extract_variables(content) == []

