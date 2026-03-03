"""API tests for PromptLab

These tests verify the API endpoints work correctly.
Students should expand these tests significantly in Week 3.
"""

import pytest
from fastapi.testclient import TestClient


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
    
    def test_list_prompts_empty(self, client: TestClient):
        response = client.get("/prompts")
        assert response.status_code == 200
        data = response.json()
        assert data["prompts"] == []
        assert data["total"] == 0
    
    def test_list_prompts_with_data(self, client: TestClient, sample_prompt_data):
        # Create a prompt first
        client.post("/prompts", json=sample_prompt_data)
        
        response = client.get("/prompts")
        assert response.status_code == 200
        data = response.json()
        assert len(data["prompts"]) == 1
        assert data["total"] == 1
    
    def test_get_prompt_success(self, client: TestClient, sample_prompt_data):
        # Create a prompt first
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        
        response = client.get(f"/prompts/{prompt_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == prompt_id
    
    def test_get_prompt_not_found(self, client: TestClient):
        """Test that getting a non-existent prompt returns 404.
        
        NOTE: This test currently FAILS due to Bug #1!
        The API returns 500 instead of 404.
        """
        response = client.get("/prompts/nonexistent-id")
        # This should be 404, but there's a bug...
        assert response.status_code == 404  # Will fail until bug is fixed
    
    def test_delete_prompt(self, client: TestClient, sample_prompt_data):
        # Create a prompt first
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        
        # Delete it
        response = client.delete(f"/prompts/{prompt_id}")
        assert response.status_code == 204
        
        # Verify it's gone
        get_response = client.get(f"/prompts/{prompt_id}")
        # Note: This might fail due to Bug #1
        assert get_response.status_code in [404, 500]  # 404 after fix
    
    def test_update_prompt(self, client: TestClient, sample_prompt_data):
        # Create a prompt first
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        original_updated_at = create_response.json()["updated_at"]
        
        # Update it
        updated_data = {
            "title": "Updated Title",
            "content": "Updated content for the prompt",
            "description": "Updated description"
        }
        
        import time
        time.sleep(0.1)  # Small delay to ensure timestamp would change
        
        response = client.put(f"/prompts/{prompt_id}", json=updated_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        
        # NOTE: This assertion will fail due to Bug #2!
        # The updated_at should be different from original
        assert data["updated_at"] != original_updated_at  # Uncomment after fix
    
    def test_sorting_order(self, client: TestClient):
        """Test that prompts are sorted newest first.
        
        NOTE: This test might fail due to Bug #3!
        """
        import time
        
        # Create prompts with delay
        prompt1 = {"title": "First", "content": "First prompt content"}
        prompt2 = {"title": "Second", "content": "Second prompt content"}
        
        client.post("/prompts", json=prompt1)
        time.sleep(0.1)
        client.post("/prompts", json=prompt2)
        
        response = client.get("/prompts")
        prompts = response.json()["prompts"]
        
        # Newest (Second) should be first
        assert prompts[0]["title"] == "Second"  # Will fail until Bug #3 fixed


class TestCollections:
    """Tests for collection endpoints."""
    
    def test_create_collection(self, client: TestClient, sample_collection_data):
        response = client.post("/collections", json=sample_collection_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_collection_data["name"]
        assert "id" in data
    
    def test_list_collections(self, client: TestClient, sample_collection_data):
        client.post("/collections", json=sample_collection_data)
        
        response = client.get("/collections")
        assert response.status_code == 200
        data = response.json()
        assert len(data["collections"]) == 1
    
    def test_get_collection_not_found(self, client: TestClient):
        response = client.get("/collections/nonexistent-id")
        assert response.status_code == 404
    
    def test_delete_collection_with_prompts(self, client: TestClient, sample_collection_data, sample_prompt_data):
        """Test deleting a collection that has prompts.
        
        BUG #4 FIX: When a collection is deleted, all associated prompts should have
        their collection_id set to None instead of becoming orphaned records.
        """
        # Create collection
        col_response = client.post("/collections", json=sample_collection_data)
        collection_id = col_response.json()["id"]
        
        # Create prompt in collection
        prompt_data = {**sample_prompt_data, "collection_id": collection_id}
        prompt_response = client.post("/prompts", json=prompt_data)
        prompt_id = prompt_response.json()["id"]
        
        # Verify prompt is associated with collection
        prompt_before = client.get(f"/prompts/{prompt_id}").json()
        assert prompt_before["collection_id"] == collection_id
        
        # Delete collection
        response = client.delete(f"/collections/{collection_id}")
        assert response.status_code == 204
        
        # Verify collection no longer exists
        col_response = client.get(f"/collections/{collection_id}")
        assert col_response.status_code == 404
        
        # FIXED: Prompt should still exist but with collection_id set to None
        prompt_after = client.get(f"/prompts/{prompt_id}").json()
        assert prompt_after["id"] == prompt_id
        assert prompt_after["collection_id"] is None  # Collection reference cleared
        assert prompt_after["title"] == sample_prompt_data["title"]  # Content preserved

class TestPromptsAPI:
    """Comprehensive tests for the prompts API endpoints."""

    def test_list_prompts_success(self, client: TestClient, sample_prompt_data):
        # Create multiple prompts
        client.post("/prompts", json=sample_prompt_data)
        client.post("/prompts", json={"title": "Sample Prompt 2", "content": "Content for prompt 2"})

        # Retrieve the list of prompts
        response = client.get("/prompts")
        assert response.status_code == 200
        data = response.json()
        assert len(data["prompts"]) >= 2
        assert data["total"] >= 2

    def test_list_prompts_empty(self, client: TestClient):
        # Retrieve prompts when there are none
        response = client.get("/prompts")
        assert response.status_code == 200
        data = response.json()
        assert data["prompts"] == []
        assert data["total"] == 0

    def test_get_prompt_success(self, client: TestClient, sample_prompt_data):
        # Create a specific prompt
        response_create = client.post("/prompts", json=sample_prompt_data)
        prompt_id = response_create.json()["id"]

        # Retrieve this prompt by ID
        response = client.get(f"/prompts/{prompt_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == prompt_id

    def test_get_prompt_not_found(self, client: TestClient):
        # Try to retrieve a non-existent prompt
        response = client.get("/prompts/nonexistent-id")
        assert response.status_code == 404
        assert response.json()["detail"] == "Prompt not found"

    def test_create_prompt_success(self, client: TestClient, sample_prompt_data):
        # Successfully create a prompt
        response = client.post("/prompts", json=sample_prompt_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == sample_prompt_data["title"]

    def test_create_prompt_invalid_data(self, client: TestClient):
        # Attempt to create a prompt with missing title
        invalid_data = {"content": "Missing title"}
        response = client.post("/prompts", json=invalid_data)
        assert response.status_code == 422  # Unprocessable entity or validation error

    def test_create_prompt_with_invalid_collection(self, client: TestClient, sample_prompt_data):
        # Attempt to create a prompt with a non-existent collection
        prompt_data = sample_prompt_data.copy()
        prompt_data["collection_id"] = "nonexistent-collection"
        response = client.post("/prompts", json=prompt_data)
        assert response.status_code == 400
        assert "Collection not found" in response.json()["detail"]

class TestPromptModificationAPI:
    """Comprehensive tests for prompt modification API endpoints."""

    def test_update_prompt_success(self, client: TestClient, sample_prompt_data):
        # Create a prompt
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]

        # Prepare updated data
        updated_data = {
            "title": "Updated Title",
            "content": "Updated Content",
            "description": "Updated Description"
        }

        # Update the prompt
        response = client.put(f"/prompts/{prompt_id}", json=updated_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == updated_data["title"]
        assert data["content"] == updated_data["content"]

    def test_update_prompt_not_found(self, client: TestClient):
        # Attempt to update a non-existent prompt
        updated_data = {
            "title": "Updated Title",
            "content": "Content"
        }
        response = client.put("/prompts/nonexistent-id", json=updated_data)
        assert response.status_code == 404
        assert response.json()["detail"] == "Prompt not found"

    def test_delete_prompt_success(self, client: TestClient, sample_prompt_data):
        # Create a prompt
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]

        # Delete the prompt
        response = client.delete(f"/prompts/{prompt_id}")
        assert response.status_code == 204

        # Attempt to delete again
        response = client.delete(f"/prompts/{prompt_id}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Prompt not found"

    def test_delete_prompt_not_found(self, client: TestClient):
        # Attempt to delete a non-existent prompt
        response = client.delete("/prompts/nonexistent-id")
        assert response.status_code == 404
        assert response.json()["detail"] == "Prompt not found"

class TestCollectionEndpoints:
    """Comprehensive tests for the collection endpoints."""

    def test_list_collections_success(self, client: TestClient, sample_collection_data):
        # Create sample collections
        client.post("/collections", json=sample_collection_data)
        client.post("/collections", json={"name": "Second Collection"})

        # List all collections
        response = client.get("/collections")
        assert response.status_code == 200
        data = response.json()
        assert len(data["collections"]) >= 2
        assert data["total"] == len(data["collections"])

    def test_list_collections_empty(self, client: TestClient):
        # Verify behavior when no collections exist
        response = client.get("/collections")
        assert response.status_code == 200
        data = response.json()
        assert data["collections"] == []
        assert data["total"] == 0

    def test_get_collection_success(self, client: TestClient, sample_collection_data):
        # Create a collection
        create_response = client.post("/collections", json=sample_collection_data)
        collection_id = create_response.json()["id"]

        # Retrieve the collection by ID
        response = client.get(f"/collections/{collection_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == collection_id

    def test_get_collection_not_found(self, client: TestClient):
        # Try retrieving a collection that doesn't exist
        response = client.get("/collections/nonexistent-id")
        assert response.status_code == 404
        assert response.json()["detail"] == "Collection not found"

    def test_create_collection_success(self, client: TestClient, sample_collection_data):
        # Successfully create a collection
        response = client.post("/collections", json=sample_collection_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_collection_data["name"]

    def test_create_collection_invalid_data(self, client: TestClient):
        # Attempt to create with invalid data (e.g., no name)
        invalid_data = {}
        response = client.post("/collections", json=invalid_data)
        assert response.status_code == 422  # Unprocessable entity or validation error

    def test_delete_collection_success(self, client: TestClient, sample_collection_data, sample_prompt_data):
        # Create a collection and a prompt within it
        create_collection_response = client.post("/collections", json=sample_collection_data)
        collection_id = create_collection_response.json()["id"]
        sample_prompt_data["collection_id"] = collection_id
        client.post("/prompts", json=sample_prompt_data)

        # Delete the collection
        response = client.delete(f"/collections/{collection_id}")
        assert response.status_code == 204

        # Verify collection is deleted
        response = client.get(f"/collections/{collection_id}")
        assert response.status_code == 404

    def test_delete_collection_with_prompts(self, client: TestClient, sample_collection_data, sample_prompt_data):
        # Create a collection and a prompt within it
        create_collection_response = client.post("/collections", json=sample_collection_data)
        collection_id = create_collection_response.json()["id"]
        sample_prompt_data["collection_id"] = collection_id
        create_prompt_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_prompt_response.json()["id"]

        # Delete the collection
        response = client.delete(f"/collections/{collection_id}")
        assert response.status_code == 204

        # Verify prompt still exists but is orphaned (no collection_id)
        response = client.get(f"/prompts/{prompt_id}")
        assert response.status_code == 200
        prompt_data = response.json()
        assert prompt_data["collection_id"] is None

    def test_delete_collection_not_found(self, client: TestClient):
        # Attempt to delete a non-existent collection
        response = client.delete("/collections/nonexistent-id")
        assert response.status_code == 404
        assert response.json()["detail"] == "Collection not found"

class TestTagsAPI:
    """Tests for the tags endpoints related to prompts."""
    
    def test_add_tags_success(self, client: TestClient, sample_prompt_data):
        # Create a prompt
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]

        # Add tags to the prompt
        tags_input = {"tags": ["AI", "Machine Learning"]}
        response = client.post(f"/prompts/{prompt_id}/tags", json=tags_input)
        assert response.status_code == 200
        data = response.json()
        assert len(data["tags"]) == 2

    def test_add_tags_partial_failure(self, client: TestClient, sample_prompt_data):
        # Create a prompt
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]

        # Add tags with one invalid tag
        tags_input = {"tags": ["AI", "", "Deep Learning"]}
        response = client.post(f"/prompts/{prompt_id}/tags", json=tags_input)
        assert response.status_code == 400  # Assuming API returns 400 for any invalid input

    def test_add_tags_empty_input(self, client: TestClient, sample_prompt_data):
        # Create a prompt
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]

        # Add empty tags
        tags_input = {"tags": []}
        response = client.post(f"/prompts/{prompt_id}/tags", json=tags_input)
        assert response.status_code == 400  # Assuming API returns 400 for empty input

    def test_get_tags_success(self, client: TestClient, sample_prompt_data):
        # Create a prompt
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]

        # Add tags
        tags_input = {"tags": ["AI", "Machine Learning"]}
        client.post(f"/prompts/{prompt_id}/tags", json=tags_input)

        # Retrieve tags
        response = client.get(f"/prompts/{prompt_id}/tags")
        assert response.status_code == 200
        tags = response.json()
        assert len(tags) == 2

    def test_get_tags_not_found(self, client: TestClient):
        # Attempt to retrieve tags for a non-existent prompt
        response = client.get("/prompts/nonexistent-id/tags")
        assert response.status_code == 404
        assert response.json()["detail"] == "Prompt not found or has no tags"

    def test_get_tags_no_tags(self, client: TestClient, sample_prompt_data):
        # Create a prompt
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]

        # Retrieve tags when there are none
        response = client.get(f"/prompts/{prompt_id}/tags")
        assert response.status_code == 200  # Expect 200 OK instead
        tags = response.json()
        assert tags == []  # Ensure it's an empty list
        
    def test_remove_tag_success(self, client: TestClient, sample_prompt_data):
        # Create a prompt
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]

        # Add tags to prompt
        tags_input = {"tags": ["AI", "Machine Learning"]}
        client.post(f"/prompts/{prompt_id}/tags", json=tags_input)

        # Remove a tag
        response = client.delete(f"/prompts/{prompt_id}/tags/AI")
        assert response.status_code == 200
    
        updated_prompt = response.json()
        tag_names = [tag['name'] for tag in updated_prompt["tags"]]
    
        assert "AI" not in tag_names
        assert "Machine Learning" in tag_names

    def test_remove_tag_not_associated(self, client: TestClient, sample_prompt_data):
        # Create a prompt
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]

        # Attempt to remove a tag that wasn't added
        response = client.delete(f"/prompts/{prompt_id}/tags/Nonexistent")
        assert response.status_code == 404
        assert response.json()["detail"] == "Prompt or tag not found"

    def test_remove_tag_not_found(self, client: TestClient):
        # Attempt to remove a tag from a non-existent prompt
        response = client.delete("/prompts/nonexistent-id/tags/AI")
        assert response.status_code == 404
        assert response.json()["detail"] == "Prompt or tag not found"

class TestTagsSearchAPI:
    """Tests for the tags endpoint that searches prompts by tag."""

    def test_search_prompts_by_tag_no_prompts(self, client: TestClient):
        # Search for a non-existent tag or a tag with no prompts
        response = client.get("/tags/nonexistent/prompts")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0  # No prompts should be associated
    
    def test_search_prompts_by_tag_partial_failure(self, client: TestClient, sample_prompt_data):
        # Create a prompt with a valid tag
        prompt1 = sample_prompt_data.copy()
        prompt1["tags"] = ["AI"]
        client.post("/prompts", json=prompt1)

        # Attempt to search for a tag with a typo or non-existent
        response = client.get("/tags/A-I/prompts")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0  # Should find no prompts

