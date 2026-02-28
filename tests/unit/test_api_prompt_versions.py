import pytest
from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)


@pytest.fixture
def sample_collection_id() -> str:
    # Ideally, fetch from a test database or mock
    return "sample_collection_id"


@pytest.fixture
def sample_prompt_id() -> str:
    # Ideally, fetch from a test database or mock
    return "sample_prompt_id"


def test_get_prompt_versions_success(sample_collection_id, sample_prompt_id):
    """Test successfully retrieving prompt versions."""
    response = client.get(f"/collections/{sample_collection_id}/prompts/{sample_prompt_id}/versions")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_prompt_versions_empty(sample_collection_id):
    """Test retrieving prompt versions with no versions available."""
    prompt_id = "prompt_without_versions"
    response = client.get(f"/collections/{sample_collection_id}/prompts/{prompt_id}/versions")
    assert response.status_code == 200
    assert response.json() == []  # Expecting an empty list if no versions


def test_get_prompt_versions_not_found(sample_collection_id):
    """Test retrieving versions of a non-existent prompt."""
    prompt_id = "non_existent_prompt"
    response = client.get(f"/collections/{sample_collection_id}/prompts/{prompt_id}/versions")
    assert response.status_code == 404
    assert response.json()["detail"] == "Prompt not found"
