import pytest
from fastapi.testclient import TestClient
from main import app
from app.storage import storage
from app.models import Prompt, Collection

client = TestClient(app)

@pytest.fixture
def setup_prompts_with_versions():
    # Clear existing data for isolated testing
    storage.clear()

    # Create a collection
    collection_id = "test_collection"
    collection = Collection(id=collection_id, name="Test Collection")
    storage.create_collection(collection)

    # Create a prompt
    prompt_id = "test_prompt"
    prompt = Prompt(id=prompt_id, title="Initial Title", content="Initial Content", collection_id=collection_id)
    storage.create_prompt(prompt)

    # Add versions
    storage.save_prompt_version(prompt_id, {
        "version_id": "v1",
        "prompt_id": prompt_id,
        "collection_id": collection_id,
        "version_number": 1,
        "created_at": "2023-01-01T00:00:00",
        "content": "Initial Content",
        "changes_summary": "Initial version"
    })

    storage.save_prompt_version(prompt_id, {
        "version_id": "v2",
        "prompt_id": prompt_id,
        "collection_id": collection_id,
        "version_number": 2,
        "created_at": "2023-02-01T00:00:00",
        "content": "Updated Content",
        "changes_summary": "Updated version"
    })

    return collection_id, prompt_id


def test_get_version_diff_success(setup_prompts_with_versions):
    collection_id, prompt_id = setup_prompts_with_versions
    response = client.get(f"/collections/{collection_id}/prompts/{prompt_id}/versions/diff?first_version_id=v1&second_version_id=v2")
    assert response.status_code == 200
    data = response.json()
    assert "differences" in data
    assert data["differences"] is not None


def test_get_version_diff_no_difference(setup_prompts_with_versions):
    collection_id, prompt_id = setup_prompts_with_versions
    response = client.get(f"/collections/{collection_id}/prompts/{prompt_id}/versions/diff?first_version_id=v2&second_version_id=v2")
    assert response.status_code == 200
    data = response.json()
    assert data["differences"] == []  # Expect no differences


def test_get_version_diff_nonexistent_version(setup_prompts_with_versions):
    collection_id, prompt_id = setup_prompts_with_versions
    response = client.get(f"/collections/{collection_id}/prompts/{prompt_id}/versions/diff?first_version_id=nonexistent&second_version_id=v2")
    assert response.status_code == 404
