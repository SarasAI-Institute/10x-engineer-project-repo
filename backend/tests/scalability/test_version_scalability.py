import pytest
import time
from fastapi.testclient import TestClient
from main import app
from app.storage import storage
from app.models import Collection, Prompt

client = TestClient(app)

@pytest.fixture
def large_dataset_setup():
    # Clear existing data for isolated testing
    storage.clear()

    # Create a large collection
    collection_id = "large_collection"
    collection = Collection(id=collection_id, name="Scalability Test Collection")
    storage.create_collection(collection)

    # Create a large prompt
    prompt_id = "large_prompt"
    prompt = Prompt(id=prompt_id, title="Scalability Test Title", content="Initial large content", collection_id=collection_id)
    storage.create_prompt(prompt)

    # Preparing a large number of versions
    for i in range(1000):
        storage.save_prompt_version(prompt_id, {
            "version_id": f"v{i}",
            "prompt_id": prompt_id,
            "collection_id": collection_id,
            "version_number": str(i + 1),
            "created_at": "2023-01-01T00:00:00",
            "content": f"Version {i} Content",
            "changes_summary": f"Version {i} created for testing"
        })

    return collection_id, prompt_id


def test_large_version_retrieval(large_dataset_setup):
    """Test system handles large version data efficiently."""
    collection_id, prompt_id = large_dataset_setup
    start_time = time.time()
    response = client.get(f"/collections/{collection_id}/prompts/{prompt_id}/versions")
    end_time = time.time()
    
    assert response.status_code == 200
    duration = end_time - start_time
    assert duration < 3  # Example limit, optimise further as necessary


def test_large_version_creation(large_dataset_setup):
    """Simulate heavy load version creation."""
    collection_id, prompt_id = large_dataset_setup
    version_data = {
        "updated_content": "Load Test",
        "changes_summary": "Scalability testing"
    }
    
    # Simulating batch version creation
    for _ in range(1000):
        response = client.post(f"/collections/{collection_id}/prompts/{prompt_id}/version", json=version_data)
        assert response.status_code in [201, 200]  # Depending on logic handling duplicates
