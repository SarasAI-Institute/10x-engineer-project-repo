from app.utils import (
    sort_prompts_by_date,
    validate_prompt_content,
    extract_variables
)
from app.models import Prompt


def test_sort_prompts_by_date_desc():
    p1 = Prompt(title="1", content="valid content 1")
    p2 = Prompt(title="2", content="valid content 2")

    sorted_list = sort_prompts_by_date([p1, p2], descending=True)

    assert sorted_list[0].created_at >= sorted_list[1].created_at


def test_validate_prompt_content():
    assert validate_prompt_content("valid content here") is True
    assert validate_prompt_content("   ") is False
    assert validate_prompt_content("short") is False


def test_extract_variables():
    result = extract_variables("Hello {{name}} and {{age}}")

    assert "name" in result
    assert "age" in result