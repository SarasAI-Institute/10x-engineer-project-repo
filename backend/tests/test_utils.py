import pytest
from datetime import datetime
from app.utils import sort_prompts_by_date, filter_prompts_by_collection, search_prompts

class Prompt:
    def __init__(self, title, created_at=None, collection_id=None, description=None):
        self.title = title
        self.created_at = created_at
        self.collection_id = collection_id
        self.description = description

# Sorting tests

def test_sort_prompts_descending():
    prompts = [
        Prompt("Prompt 1", datetime(2023, 9, 10)),
        Prompt("Prompt 2", datetime(2023, 8, 25)),
        Prompt("Prompt 3", datetime(2023, 10, 5)),
    ]
    sorted_desc = sort_prompts_by_date(prompts, descending=True)
    assert sorted_desc[0].title == "Prompt 3"
    assert sorted_desc[-1].title == "Prompt 2"

def test_sort_prompts_ascending():
    prompts = [
        Prompt("Prompt 1", datetime(2023, 9, 10)),
        Prompt("Prompt 2", datetime(2023, 8, 25)),
        Prompt("Prompt 3", datetime(2023, 10, 5)),
    ]
    sorted_asc = sort_prompts_by_date(prompts, descending=False)
    assert sorted_asc[0].title == "Prompt 2"
    assert sorted_asc[-1].title == "Prompt 3"

def test_sort_empty_prompts():
    empty_prompts = []
    sorted_empty = sort_prompts_by_date(empty_prompts)
    assert sorted_empty == []

def test_sort_prompts_same_date():
    same_date_prompts = [
        Prompt("Prompt A", datetime(2023, 9, 10)),
        Prompt("Prompt B", datetime(2023, 9, 10)),
        Prompt("Prompt C", datetime(2023, 9, 10)),
    ]
    sorted_same_date = sort_prompts_by_date(same_date_prompts)
    assert sorted_same_date == same_date_prompts

def test_sort_single_prompt():
    single_prompt = [Prompt("Single Prompt", datetime(2023, 8, 20))]
    sorted_single = sort_prompts_by_date(single_prompt)
    assert sorted_single == single_prompt

# Filtering tests

def test_filter_prompts_by_valid_collection_id():
    prompts = [
        Prompt("Prompt 1", collection_id="12345"),
        Prompt("Prompt 2", collection_id="67890"),
        Prompt("Prompt 3", collection_id="12345"),
    ]
    filtered = filter_prompts_by_collection(prompts, "12345")
    assert len(filtered) == 2
    assert all(prompt.collection_id == "12345" for prompt in filtered)

def test_filter_prompts_by_nonexistent_collection_id():
    prompts = [
        Prompt("Prompt 1", collection_id="12345"),
        Prompt("Prompt 2", collection_id="67890"),
    ]
    filtered = filter_prompts_by_collection(prompts, "00000")
    assert filtered == []

def test_filter_prompts_empty_list():
    empty_prompts = []
    filtered = filter_prompts_by_collection(empty_prompts, "12345")
    assert filtered == []

def test_filter_prompts_no_matching_collection_id():
    prompts = [
        Prompt("Prompt 1", collection_id="12345"),
        Prompt("Prompt 2", collection_id="67890"),
        Prompt("Prompt 3", collection_id="54321"),
    ]
    filtered = filter_prompts_by_collection(prompts, "11111")
    assert filtered == []

def test_filter_prompts_multiple_matching_ids():
    prompts = [
        Prompt("Prompt 1", collection_id="12345"),
        Prompt("Prompt 2", collection_id="12345"),
        Prompt("Prompt 3", collection_id="12345"),
    ]
    filtered = filter_prompts_by_collection(prompts, "12345")
    assert len(filtered) == 3
    assert all(prompt.collection_id == "12345" for prompt in filtered)

# Search tests

def test_search_prompts_title_match():
    prompts = [
        Prompt("Welcome to the jungle"),
        Prompt("Quick start guide"),
        Prompt("Advanced topics")
    ]
    query = "welcome"
    results = search_prompts(prompts, query)
    assert len(results) == 1
    assert results[0].title == "Welcome to the jungle"

def test_search_prompts_description_match():
    prompts = [
        Prompt("Intro", description="This is the welcome section"),
        Prompt("Getting Started", description="Initial setup and configuration"),
        Prompt("Features", description="Explore advanced topics")
    ]
    query = "welcome"
    results = search_prompts(prompts, query)
    assert len(results) == 1
    assert results[0].description == "This is the welcome section"

def test_search_prompts_case_insensitivity():
    prompts = [
        Prompt("Welcome to the Jungle"),
        Prompt("Guide", description="Welcome Here"),
    ]
    query = "WELCOME"
    results = search_prompts(prompts, query)
    assert len(results) == 2  # Should match both title and description

def test_search_prompts_no_match():
    prompts = [
        Prompt("Intro to Python"),
        Prompt("Data Science Overview"),
    ]
    query = "Java"
    results = search_prompts(prompts, query)
    assert results == []

def test_search_prompts_empty_query():
    prompts = [
        Prompt("Intro to Machine Learning"),
        Prompt("Deep Dive into AI"),
    ]
    query = ""
    results = search_prompts(prompts, query)
    assert len(results) == 2  # Should match all as empty string matches every title


    import pytest
from app.utils import validate_prompt_content

def test_validate_prompt_content_valid():
    """Test with valid content."""
    content = "Valid content here."
    assert validate_prompt_content(content) is True

def test_validate_prompt_content_empty_string():
    """Test with an empty string."""
    content = ""
    assert validate_prompt_content(content) is False

def test_validate_prompt_content_whitespace():
    """Test with content that is only whitespace."""
    content = "     "
    assert validate_prompt_content(content) is False

def test_validate_prompt_content_too_short():
    """Test with content that is too short."""
    content = "Too short"
    assert validate_prompt_content(content) is False

def test_validate_prompt_content_exact_length():
    """Test with content that is exactly the minimum length."""
    content = "1234567890"
    assert validate_prompt_content(content) is True

def test_validate_prompt_content_long_content():
    """Test with very long content."""
    content = "L" * 1000  # Long string of length 1000
    assert validate_prompt_content(content) is True



    import pytest
from app.utils import extract_variables

def test_extract_variables_multiple():
    """Test extracting multiple variables."""
    content = "Hello {{name}}, welcome to {{place}}."
    variables = extract_variables(content)
    assert variables == ["name", "place"]

def test_extract_variables_single():
    """Test extracting a single variable."""
    content = "Your order number is {{order_number}}."
    variables = extract_variables(content)
    assert variables == ["order_number"]

def test_extract_variables_no_variables():
    """Test content with no template variables."""
    content = "Just a plain text with no variables."
    variables = extract_variables(content)
    assert variables == []

def test_extract_variables_adjacent_variables():
    """Test extracting adjacent variables."""
    content = "Coordinates are {{x}}{{y}}."
    variables = extract_variables(content)
    assert variables == ["x", "y"]

def test_extract_variables_with_underscores():
    """Test variable names with underscores."""
    content = "Today's forecast is {{weather_update}}."
    variables = extract_variables(content)
    assert variables == ["weather_update"]

def test_extract_variables_empty_string():
    """Test with an empty string."""
    content = ""
    variables = extract_variables(content)
    assert variables == []

def test_extract_variables_special_characters():
    """Test content with special characters in text but not in variable names."""
    content = "Price: {{price}} $ and tax: {{tax}}%"
    variables = extract_variables(content)
    assert variables == ["price", "tax"]
