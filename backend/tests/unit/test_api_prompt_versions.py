from app.storage import storage  # Use the global storage instance
from fastapi.testclient import TestClient
import pytest
from app.api import app
from app.models import Prompt, Collection  # Newly added import statement

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_test_data():
    """Setup storage with initial data for testing versions."""
    collection_id = "sample_collection_id"
    prompt_id = "sample_prompt_id"

    # Clear existing data
    storage.clear()

    # Setup collection
    collection = Collection(id=collection_id, name="Sample Collection")
    storage.create_collection(collection)

    # Setup prompt
    prompt = Prompt(id=prompt_id, title="Sample Title", content="Sample prompt content", collection_id=collection_id)
    storage.create_prompt(prompt)

    # Setup versions
    version_data = {
        "version_id": "v1",
        "changes_summary": "Initial version",
        "created_at": "2024-01-01T00:00:00",
        "prompt_id": prompt_id,
        "collection_id": collection_id,
        "version_number": "1"
    }
    storage.save_prompt_version(prompt_id, version_data)

    # Setup a prompt without versions for testing
    prompt_without_versions = Prompt(
        id="prompt_without_versions",
        title="No Version Prompt",
        content="This prompt has no versions.",
        collection_id=collection_id
    )
    storage.create_prompt(prompt_without_versions)

@pytest.fixture
def sample_collection_id() -> str:
    return "sample_collection_id"

@pytest.fixture
def sample_prompt_id() -> str:
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

