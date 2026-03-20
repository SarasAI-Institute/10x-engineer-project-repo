import pytest
from app.models import Prompt


def test_prompt_defaults():
    p = Prompt(title="Test", content="valid content here")

    assert p.id is not None
    assert p.created_at is not None
    assert p.updated_at is not None


def test_prompt_validation_fails():
    with pytest.raises(Exception):
        Prompt(title="", content="")