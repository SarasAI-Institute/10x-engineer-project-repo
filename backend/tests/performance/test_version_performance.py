import pytest
import time
from fastapi.testclient import TestClient
from main import app
from app.storage import storage
from app.models import Collection, Prompt

client = TestClient(app)

@pytest.fixture
def setup_versions():
    # Clear existing data for isolated testing
    storage.clear()

    # Create a collection
    collection_id = "collection_for_perf"
    collection = Collection(id=collection_id, name="Performance Collection")
    storage.create_collection(collection)

    # Create a prompt
    prompt_id = "prompt_for_perf"
    prompt = Prompt(id=prompt_id, title="Performance Title", content="Performance Content", collection_id=collection_id)
    storage.create_prompt(prompt)

    # Add initial versions
    storage.save_prompt_version(prompt_id, {
        "version_id": "v1",
        "prompt_id": prompt_id,
        "collection_id": collection_id,
        "version_number": "1",  # Ensure version_number is a string
        "created_at": "2023-01-01T00:00:00",
        "content": "Version 1 Content",
        "changes_summary": "First version"
    })
    return collection_id, prompt_id


def test_version_retrieval_performance(setup_versions):
    """Test performance of retrieving version history."""
    start_time = time.time()

    collection_id, prompt_id = setup_versions  # Use values from the fixture
    response = client.get(f"/collections/{collection_id}/prompts/{prompt_id}/versions")

    end_time = time.time()
    duration = end_time - start_time

    assert response.status_code == 200
    assert duration < 0.5  # Example benchmark: <500ms


def test_version_creation_performance(setup_versions):
    """Test performance of creating a new version."""
    start_time = time.time()

    collection_id, prompt_id = setup_versions  # Use values from the fixture
    new_version_data = {
        "updated_content": "Performance test content",
        "changes_summary": "Performance optimization"
    }
    response = client.post(f"/collections/{collection_id}/prompts/{prompt_id}/version", json=new_version_data)

    end_time = time.time()
    duration = end_time - start_time

    assert response.status_code == 201
    assert duration < 1  # Example benchmark: <1 second
