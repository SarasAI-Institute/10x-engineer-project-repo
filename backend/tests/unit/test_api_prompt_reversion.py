import pytest
from fastapi.testclient import TestClient
from main import app
from app.storage import storage
from app.models import Prompt, Collection, VersionRequest
from typing import Dict  # Import Dict for the request data typing

client = TestClient(app)

@pytest.fixture
def setup_prompts_and_versions():
    # Clear existing data
    storage.clear()

    # Create a collection
    collection_id = "test_collection"
    collection = Collection(id=collection_id, name="Test Collection")
    storage.create_collection(collection)

    # Create a prompt
    prompt_id = "test_prompt"
    prompt = Prompt(id=prompt_id, title="Original Title", content="Original Content", collection_id=collection_id)
    storage.create_prompt(prompt)

    # Create a version
    version_data = {
        "version_id": "version_1",
        "prompt_id": prompt_id,
        "collection_id": collection_id,
        "version_number": 1,
        "created_at": "2023-01-01T00:00:00",
        "content": "Original Content",
        "changes_summary": "Initial version"
    }
    storage.save_prompt_version(prompt_id, version_data)

    return collection_id, prompt_id


def test_revert_prompt_success(setup_prompts_and_versions):
    collection_id, prompt_id = setup_prompts_and_versions
    # Prepare the request to revert
    target_version_id = "version_1"
    # Use a simple dict to represent the request body
    request_data: Dict[str, str] = {"target_version_id": target_version_id}
    response = client.post(f"/collections/{collection_id}/prompts/{prompt_id}/revert", json=request_data)
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["detail"] == "Target version is the current version; no changes made."


def test_revert_prompt_nonexistent_version(setup_prompts_and_versions):
    collection_id, prompt_id = setup_prompts_and_versions
    # Attempt to revert to a non-existent version
    target_version_id = "nonexistent_version"
    # Use a simple dict to represent the request body
    request_data: Dict[str, str] = {"target_version_id": target_version_id}
    response = client.post(f"/collections/{collection_id}/prompts/{prompt_id}/revert", json=request_data)
    
    assert response.status_code == 404


def test_revert_prompt_to_current_version(setup_prompts_and_versions):
    collection_id, prompt_id = setup_prompts_and_versions
    # Revert to the original version, which is the current state
    target_version_id = "version_1"
    # Use a simple dict to represent the request body
    request_data: Dict[str, str] = {"target_version_id": target_version_id}
    response = client.post(f"/collections/{collection_id}/prompts/{prompt_id}/revert", json=request_data)
    
    # Assuming this should just pass silently with no effect or create a new version
    # The expected behavior needs to be explicitly defined in the application logic
    assert response.status_code == 200  # Assuming success or no-op

