# File: backend/tests/test_api.py

import pytest
from fastapi.testclient import TestClient
from main import app
import random
import string

@pytest.fixture(scope="module")
def client():
    """Create a TestClient for the FastAPI app."""
    return TestClient(app)

@pytest.fixture
def sample_prompt_data():
    """Provide a sample prompt data for testing."""
    return {
        "title": "Sample Prompt",
        "content": "This is a sample prompt"
    }

@pytest.fixture
def sample_collection_data():
    """Provide a sample collection data for testing."""
    return {
        "name": "Sample Collection"
    }

class TestHealth:
    """Tests for health endpoint."""
    
    def test_health_check(self, client: TestClient):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data

class TestPrompts:
    """Tests for prompt endpoints."""
    
    def test_create_prompt(self, client: TestClient, sample_prompt_data):
        response = client.post("/prompts", json=sample_prompt_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == sample_prompt_data["title"]
        assert data["content"] == sample_prompt_data["content"]
        assert "id" in data
        assert "created_at" in data

    def test_create_prompt_empty_content(self, client: TestClient, sample_prompt_data):
        """Create a prompt with an empty content."""
        prompt_data = sample_prompt_data.copy()
        prompt_data["content"] = ""
        response = client.post("/prompts", json=prompt_data)
        assert response.status_code == 422  # Fails validation

    def test_create_prompt_max_length_title(self, client: TestClient):
        """Create a prompt with a title at maximum allowable length."""
        max_length_title = ''.join(random.choices(string.ascii_letters + string.digits, k=200))
        response = client.post("/prompts", json={"title": max_length_title, "content": "Max length title content"})
        assert response.status_code == 201
        assert response.json()["title"] == max_length_title

    def test_create_prompt_invalid_json_format(self, client: TestClient):
        """Send invalid JSON structure."""
        response = client.post("/prompts", data="This is not JSON")
        assert response.status_code == 422
    
    def test_delete_prompt_not_found(self, client: TestClient):
        """Delete a prompt that doesn't exist."""
        response = client.delete("/prompts/nonexistent-id")
        assert response.status_code == 404

    def test_update_prompt_invalid_id(self, client: TestClient, sample_prompt_data):
        """Try updating a prompt with a non-existent ID."""
        response = client.put("/prompts/invalid-id", json=sample_prompt_data)
        assert response.status_code == 404

    def test_patch_prompt_empty_update(self, client: TestClient, sample_prompt_data):
        """Send an empty patch update (should not change anything)."""
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]

        patch_data = {}
        response = client.patch(f"/prompts/{prompt_id}", json=patch_data)
        assert response.status_code == 200
        print("Expected:", response.json())
        print("Actual:", create_response.json())
        assert response.json() == create_response.json()  # No change expected

    def test_list_prompts_with_special_characters_search(self, client: TestClient, sample_prompt_data):
        """Check behavior when using special characters in search."""
        client.post("/prompts", json=sample_prompt_data)
        response = client.get("/prompts?search=!@#$%^&*()")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0

    def test_list_prompts_concurrent_access(self, client: TestClient, sample_prompt_data):
        """Simulate concurrent creation of prompts to test ordering."""
        num_concurrent_prompts = 10
        created_prompts = []

        for i in range(num_concurrent_prompts):
            response = client.post("/prompts", json={**sample_prompt_data, "title": f"Prompt {i}"})
            created_prompts.append(response.json())

        response = client.get("/prompts")
        assert response.status_code == 200
        prompts = response.json()["prompts"]

        # Confirm the number of returned prompts matches the creation count
        assert len(prompts) >= num_concurrent_prompts
        
        # Check ordering (newest first)
        for i in range(1, num_concurrent_prompts):
            assert prompts[i - 1]["created_at"] >= prompts[i]["created_at"]

class TestCollections:
    """Tests for collection endpoints."""
    
    def test_create_collection(self, client: TestClient, sample_collection_data):
        response = client.post("/collections", json=sample_collection_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_collection_data["name"]
        assert "id" in data

    def test_create_collection_without_name(self, client: TestClient):
        """Attempt to create a collection with no name."""
        response = client.post("/collections", json={})
        assert response.status_code == 422
    
    def test_get_collection_not_found(self, client: TestClient):
        """Attempt to retrieve a nonexistent collection."""
        response = client.get("/collections/nonexistent-id")
        assert response.status_code == 404

    def test_delete_collection_with_prompts(self, client: TestClient, sample_collection_data, sample_prompt_data):
        """Delete a collection with associated prompts and ensure they move to 'Uncategorized'."""
        col_response = client.post("/collections", json=sample_collection_data)
        collection_id = col_response.json()["id"]

        prompt_data = {**sample_prompt_data, "collection_id": collection_id}
        client.post("/prompts", json=prompt_data)
        
        client.delete(f"/collections/{collection_id}")

        all_cols = client.get("/collections").json()["collections"]
        uncategorized_col = next(c for c in all_cols if c["name"] == "Uncategorized")
        uncategorized_id = uncategorized_col["id"]
        
        prompts = client.get("/prompts").json()["prompts"]
        assert all(prompt["collection_id"] == uncategorized_id for prompt in prompts)  # All moved

class TestPromptEdgeCases:
    """Edge cases for prompt endpoints."""

    def test_create_prompt_missing_fields(self, client: TestClient):
        """Attempt to create a prompt with missing title/content."""
        response = client.post("/prompts", json={"title": "Incomplete Prompt"})
        assert response.status_code == 422  # Expect validation error

    def test_get_prompt_invalid_id_format(self, client: TestClient):
        """Retrieve a prompt using an invalid ID format."""
        response = client.get("/prompts/invalid!d")
        assert response.status_code == 404  # Handles gracefully

    def test_patch_prompt_with_missing_optional_fields(self, client: TestClient, sample_prompt_data):
        """Patch a prompt without some optional fields."""
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]

        patch_data = {"description": "New Description"}
        response = client.patch(f"/prompts/{prompt_id}", json=patch_data)
        assert response.status_code == 200
        assert response.json()["description"] == "New Description"

    def test_update_prompt_invalid_fields(self, client: TestClient, sample_prompt_data):
        """Attempt to update a prompt with invalid field types."""
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]

        response = client.put(f"/prompts/{prompt_id}", json={"title": 12345})
        assert response.status_code == 422  # Validation should catch this

class TestCollectionEdgeCases:
    """Edge cases for collection endpoints."""
    
    def test_create_collection_empty_name(self, client: TestClient):
        """Create a collection with an empty name."""
        response = client.post("/collections", json={"name": ""})
        assert response.status_code == 422  # Should handle gracefully
    
    def test_delete_collection_with_orphaned_prompts(self, client: TestClient, sample_collection_data, sample_prompt_data):
        """Delete a collection and handle orphaned prompts."""
        # Create collection and prompt
        col_response = client.post("/collections", json=sample_collection_data)
        collection_id = col_response.json()["id"]

        prompt_data = {**sample_prompt_data, "collection_id": collection_id}
        client.post("/prompts", json=prompt_data)

        # Delete the collection
        client.delete(f"/collections/{collection_id}")

        # Ensure orphaned prompts are reassigned correctly
        uncategorized_id = client.get("/collections").json()["collections"][0]["id"]
        prompts = client.get("/prompts").json()["prompts"]
        assert all(prompt["collection_id"] == uncategorized_id for prompt in prompts)  # All reassigned
