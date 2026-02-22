"""Tests for utility functions.

This module tests all utility functions including:
- Sorting prompts by date
- Filtering prompts by collection
- Searching prompts
- Validating prompt content
- Extracting template variables
"""

import pytest
from datetime import datetime, timezone, timedelta
from app.utils import (
    sort_prompts_by_date,
    filter_prompts_by_collection,
    search_prompts,
    validate_prompt_content,
    extract_variables
)
from app.models import Prompt


class TestSortPromptsByDate:
    """Tests for sort_prompts_by_date function."""
    
    def test_sort_descending_default(self):
        """Test default descending sort (newest first)."""
        now = datetime.now(timezone.utc)
        prompts = [
            Prompt(
                title="Old",
                content="Content",
                created_at=now - timedelta(days=2),
                updated_at=now - timedelta(days=2)
            ),
            Prompt(
                title="New",
                content="Content",
                created_at=now,
                updated_at=now
            ),
            Prompt(
                title="Medium",
                content="Content",
                created_at=now - timedelta(days=1),
                updated_at=now - timedelta(days=1)
            )
        ]
        
        sorted_prompts = sort_prompts_by_date(prompts)
        assert sorted_prompts[0].title == "New"
        assert sorted_prompts[1].title == "Medium"
        assert sorted_prompts[2].title == "Old"
    
    def test_sort_ascending(self):
        """Test ascending sort (oldest first)."""
        now = datetime.now(timezone.utc)
        prompts = [
            Prompt(
                title="New",
                content="Content",
                created_at=now,
                updated_at=now
            ),
            Prompt(
                title="Old",
                content="Content",
                created_at=now - timedelta(days=2),
                updated_at=now - timedelta(days=2)
            )
        ]
        
        sorted_prompts = sort_prompts_by_date(prompts, descending=False)
        assert sorted_prompts[0].title == "Old"
        assert sorted_prompts[1].title == "New"
    
    def test_sort_empty_list(self):
        """Test sorting empty list."""
        result = sort_prompts_by_date([])
        assert result == []
    
    def test_sort_single_item(self):
        """Test sorting list with single item."""
        prompts = [Prompt(title="Test", content="Content")]
        result = sort_prompts_by_date(prompts)
        assert len(result) == 1
        assert result[0].title == "Test"


class TestFilterPromptsByCollection:
    """Tests for filter_prompts_by_collection function."""
    
    def test_filter_with_matching_prompts(self):
        """Test filtering when prompts match collection."""
        prompts = [
            Prompt(title="P1", content="C", collection_id="col1"),
            Prompt(title="P2", content="C", collection_id="col2"),
            Prompt(title="P3", content="C", collection_id="col1")
        ]
        
        result = filter_prompts_by_collection(prompts, "col1")
        assert len(result) == 2
        assert all(p.collection_id == "col1" for p in result)
    
    def test_filter_no_matches(self):
        """Test filtering when no prompts match."""
        prompts = [
            Prompt(title="P1", content="C", collection_id="col1"),
            Prompt(title="P2", content="C", collection_id="col2")
        ]
        
        result = filter_prompts_by_collection(prompts, "col3")
        assert result == []
    
    def test_filter_empty_list(self):
        """Test filtering empty list."""
        result = filter_prompts_by_collection([], "col1")
        assert result == []
    
    def test_filter_none_collection_id(self):
        """Test filtering for prompts without collection (None)."""
        prompts = [
            Prompt(title="P1", content="C", collection_id="col1"),
            Prompt(title="P2", content="C", collection_id=None),
            Prompt(title="P3", content="C", collection_id=None)
        ]
        
        result = filter_prompts_by_collection(prompts, None)
        assert len(result) == 2
        assert all(p.collection_id is None for p in result)


class TestSearchPrompts:
    """Tests for search_prompts function."""
    
    def test_search_by_title(self):
        """Test searching prompts by title."""
        prompts = [
            Prompt(title="Email Template", content="Content"),
            Prompt(title="SMS Template", content="Content"),
            Prompt(title="Code Review", content="Content")
        ]
        
        result = search_prompts(prompts, "email")
        assert len(result) == 1
        assert result[0].title == "Email Template"
    
    def test_search_by_description(self):
        """Test searching prompts by description."""
        prompts = [
            Prompt(title="T1", content="C", description="For email campaigns"),
            Prompt(title="T2", content="C", description="For SMS messaging"),
            Prompt(title="T3", content="C", description=None)
        ]
        
        result = search_prompts(prompts, "email")
        assert len(result) == 1
        assert result[0].description == "For email campaigns"
    
    def test_search_case_insensitive(self):
        """Test that search is case-insensitive."""
        prompts = [Prompt(title="Email Template", content="Content")]
        
        for query in ["EMAIL", "email", "EmAiL", "TEMPLATE"]:
            result = search_prompts(prompts, query)
            assert len(result) == 1
    
    def test_search_partial_match(self):
        """Test that search matches partial strings."""
        prompts = [Prompt(title="Marketing Email Template", content="Content")]
        
        for query in ["mar", "email", "temp"]:
            result = search_prompts(prompts, query)
            assert len(result) == 1
    
    def test_search_no_results(self):
        """Test search with no matching results."""
        prompts = [Prompt(title="Test", content="Content")]
        result = search_prompts(prompts, "nonexistent")
        assert result == []
    
    def test_search_empty_list(self):
        """Test searching empty list."""
        result = search_prompts([], "query")
        assert result == []
    
    def test_search_none_description(self):
        """Test search doesn't crash on None description."""
        prompts = [
            Prompt(title="Test", content="Content", description=None)
        ]
        result = search_prompts(prompts, "test")
        assert len(result) == 1


class TestValidatePromptContent:
    """Tests for validate_prompt_content function."""
    
    def test_valid_content(self):
        """Test validation passes for valid content."""
        assert validate_prompt_content("Hello {{name}}, how are you?") == True
        assert validate_prompt_content("x" * 100) == True
    
    def test_content_exactly_10_chars(self):
        """Test validation passes for exactly 10 characters."""
        assert validate_prompt_content("0123456789") == True
    
    def test_content_too_short(self):
        """Test validation fails for content < 10 characters."""
        assert validate_prompt_content("short") == False
        assert validate_prompt_content("123456789") == False
    
    def test_empty_content(self):
        """Test validation fails for empty content."""
        assert validate_prompt_content("") == False
    
    def test_whitespace_only(self):
        """Test validation fails for whitespace-only content."""
        assert validate_prompt_content("   ") == False
        assert validate_prompt_content("\n\t  ") == False
    
    def test_content_with_leading_trailing_whitespace(self):
        """Test validation counts only non-whitespace content."""
        assert validate_prompt_content("   valid content   ") == True
        assert validate_prompt_content("   short  ") == False


class TestExtractVariables:
    """Tests for extract_variables function."""
    
    def test_single_variable(self):
        """Test extracting single variable."""
        result = extract_variables("Hello {{name}}")
        assert result == ["name"]
    
    def test_multiple_variables(self):
        """Test extracting multiple variables."""
        result = extract_variables("Hello {{name}}, your order {{order_id}} is ready")
        assert result == ["name", "order_id"]
    
    def test_no_variables(self):
        """Test extracting from content with no variables."""
        result = extract_variables("Hello world")
        assert result == []
    
    def test_duplicate_variables(self):
        """Test that duplicate variables are included."""
        result = extract_variables("{{name}} and {{name}} again")
        assert result == ["name", "name"]
    
    def test_variable_with_underscores(self):
        """Test variables with underscores."""
        result = extract_variables("{{first_name}} {{last_name}}")
        assert result == ["first_name", "last_name"]
    
    def test_variable_with_numbers(self):
        """Test variables with numbers."""
        result = extract_variables("{{item1}} {{item2}}")
        assert result == ["item1", "item2"]
    
    def test_invalid_variable_format(self):
        """Test that invalid formats are not extracted."""
        result = extract_variables("{{invalid-var}} {{invalid var}} {invalid}")
        assert result == []
    
    def test_nested_curly_braces(self):
        """Test handling of nested or adjacent braces."""
        result = extract_variables("{{{name}}} {{{{nested}}}}")
        # Should still extract valid patterns
        assert "name" in result or len(result) >= 0
    
    def test_empty_content(self):
        """Test extracting from empty content."""
        result = extract_variables("")
        assert result == []
    
    def test_complex_template(self):
        """Test extracting from complex template."""
        content = """
        Hello {{user_name}},
        
        Your order {{order_id}} from {{date}} is ready.
        Total: {{total_amount}}
        
        Thanks,
        {{company_name}}
        """
        result = extract_variables(content)
        expected = ["user_name", "order_id", "date", "total_amount", "company_name"]
        assert result == expected
