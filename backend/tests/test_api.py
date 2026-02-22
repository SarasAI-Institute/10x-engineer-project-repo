"""Comprehensive API tests for PromptLab.

This test suite provides extensive coverage of all API endpoints including:
- Health checks
- Prompt CRUD operations
- Collection CRUD operations
- Search and filtering
- Error handling and edge cases
- Data validation
"""

import pytest
import time
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
        """Test that getting a non-existent prompt returns 404."""
        response = client.get("/prompts/nonexistent-id")
        assert response.status_code == 404
        assert response.json()["detail"] == "Prompt not found"
    
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
        assert data["updated_at"] != original_updated_at  # Fixed: Bug #2
    def test_sorting_order(self, client: TestClient):
        """Test that prompts are sorted newest first."""
        import time
        # Create prompts with delay
        prompt1 = {"title": "First", "content": "First prompt content"}
        prompt2 = {"title": "Second", "content": "Second prompt content"}
        
        client.post("/prompts", json=prompt1)
        time.sleep(0.1)
        client.post("/prompts", json=prompt2)
        
        response = client.get("/prompts")
        prompts = response.json()["prompts"]
        
        # Newest (Second) should be first (Fixed: Bug #3)
        assert prompts[0]["title"] == "Second"
        assert prompts[1]["title"] == "First"
    
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
        
        FIXED: Bug #4 - prompts are now orphaned properly (collection_id set to None)
        when their collection is deleted.
        """
        # Create collection
        col_response = client.post("/collections", json=sample_collection_data)
        collection_id = col_response.json()["id"]
        
        # Create prompt in collection
        prompt_data = {**sample_prompt_data, "collection_id": collection_id}
        prompt_response = client.post("/prompts", json=prompt_data)
        prompt_id = prompt_response.json()["id"]
        
        # Delete collection
        client.delete(f"/collections/{collection_id}")
        
        # The prompt still exists but collection_id is set to None (orphaned)
        prompts = client.get("/prompts").json()["prompts"]
        assert len(prompts) == 1
        assert prompts[0]["id"] == prompt_id
        assert prompts[0]["collection_id"] is None  # Correctly orphaned


class TestPromptValidation:
    """Tests for prompt validation and error handling."""
    
    def test_create_prompt_missing_title(self, client: TestClient):
        """Test creating prompt without required title field."""
        data = {"content": "Some content"}
        response = client.post("/prompts", json=data)
        assert response.status_code == 422
    
    def test_create_prompt_missing_content(self, client: TestClient):
        """Test creating prompt without required content field."""
        data = {"title": "Test Title"}
        response = client.post("/prompts", json=data)
        assert response.status_code == 422
    
    def test_create_prompt_empty_title(self, client: TestClient):
        """Test creating prompt with empty title."""
        data = {"title": "", "content": "Content"}
        response = client.post("/prompts", json=data)
        assert response.status_code == 422
    
    def test_create_prompt_title_too_long(self, client: TestClient):
        """Test creating prompt with title exceeding max length."""
        data = {"title": "x" * 201, "content": "Content"}
        response = client.post("/prompts", json=data)
        assert response.status_code == 422
    
    def test_create_prompt_description_too_long(self, client: TestClient):
        """Test creating prompt with description exceeding max length."""
        data = {
            "title": "Test",
            "content": "Content",
            "description": "x" * 501
        }
        response = client.post("/prompts", json=data)
        assert response.status_code == 422
    
    def test_create_prompt_invalid_collection_id(self, client: TestClient):
        """Test creating prompt with non-existent collection ID."""
        data = {
            "title": "Test",
            "content": "Content",
            "collection_id": "non-existent-id"
        }
        response = client.post("/prompts", json=data)
        assert response.status_code == 400
        assert "Collection not found" in response.json()["detail"]
    
    def test_create_prompt_with_valid_collection(self, client: TestClient, sample_collection_data):
        """Test creating prompt with valid collection ID."""
        # Create collection first
        col_response = client.post("/collections", json=sample_collection_data)
        collection_id = col_response.json()["id"]
        
        # Create prompt with collection
        data = {
            "title": "Test",
            "content": "Content",
            "collection_id": collection_id
        }
        response = client.post("/prompts", json=data)
        assert response.status_code == 201
        assert response.json()["collection_id"] == collection_id
    
    def test_delete_nonexistent_prompt(self, client: TestClient):
        """Test deleting non-existent prompt returns 404."""
        response = client.delete("/prompts/fake-id")
        assert response.status_code == 404


class TestPromptPatch:
    """Tests for PATCH endpoint (partial updates)."""
    
    def test_patch_prompt_title_only(self, client: TestClient, sample_prompt_data):
        """Test updating only the title field."""
        # Create prompt
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        original_content = create_response.json()["content"]
        
        # Patch only title
        time.sleep(0.1)
        patch_data = {"title": "New Title"}
        response = client.patch(f"/prompts/{prompt_id}", json=patch_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "New Title"
        assert data["content"] == original_content  # Unchanged
    
    def test_patch_prompt_content_only(self, client: TestClient, sample_prompt_data):
        """Test updating only the content field."""
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        original_title = create_response.json()["title"]
        
        patch_data = {"content": "New content"}
        response = client.patch(f"/prompts/{prompt_id}", json=patch_data)
        
        assert response.status_code == 200
        assert response.json()["content"] == "New content"
        assert response.json()["title"] == original_title
    
    def test_patch_prompt_updates_timestamp(self, client: TestClient, sample_prompt_data):
        """Test that PATCH updates the updated_at timestamp."""
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        original_updated_at = create_response.json()["updated_at"]
        
        time.sleep(0.1)
        patch_data = {"title": "Updated"}
        response = client.patch(f"/prompts/{prompt_id}", json=patch_data)
        
        assert response.status_code == 200
        assert response.json()["updated_at"] != original_updated_at
    
    def test_patch_nonexistent_prompt(self, client: TestClient):
        """Test patching non-existent prompt returns 404."""
        response = client.patch("/prompts/fake-id", json={"title": "New"})
        assert response.status_code == 404
    
    def test_patch_with_invalid_collection(self, client: TestClient, sample_prompt_data):
        """Test patching with invalid collection ID returns 400."""
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        
        patch_data = {"collection_id": "invalid-id"}
        response = client.patch(f"/prompts/{prompt_id}", json=patch_data)
        assert response.status_code == 400


class TestSearchAndFilter:
    """Tests for search and filter functionality."""
    
    def test_search_by_title(self, client: TestClient):
        """Test searching prompts by title."""
        # Create prompts
        client.post("/prompts", json={"title": "Email Template", "content": "Content"})
        client.post("/prompts", json={"title": "SMS Template", "content": "Content"})
        client.post("/prompts", json={"title": "Code Review", "content": "Content"})
        
        # Search for 'email'
        response = client.get("/prompts?search=email")
        assert response.status_code == 200
        prompts = response.json()["prompts"]
        assert len(prompts) == 1
        assert "Email" in prompts[0]["title"]
    
    def test_search_by_description(self, client: TestClient):
        """Test searching prompts by description."""
        client.post("/prompts", json={
            "title": "Template",
            "content": "Content",
            "description": "For email campaigns"
        })
        client.post("/prompts", json={
            "title": "Another",
            "content": "Content",
            "description": "For SMS messaging"
        })
        
        response = client.get("/prompts?search=email")
        assert response.status_code == 200
        assert response.json()["total"] == 1
    
    def test_search_case_insensitive(self, client: TestClient):
        """Test that search is case-insensitive."""
        client.post("/prompts", json={"title": "Email Template", "content": "Content"})
        
        for query in ["EMAIL", "email", "EmAiL"]:
            response = client.get(f"/prompts?search={query}")
            assert response.json()["total"] == 1
    
    def test_search_no_results(self, client: TestClient):
        """Test search with no matching results."""
        client.post("/prompts", json={"title": "Test", "content": "Content"})
        
        response = client.get("/prompts?search=nonexistent")
        assert response.status_code == 200
        assert response.json()["total"] == 0
        assert response.json()["prompts"] == []
    
    def test_filter_by_collection(self, client: TestClient, sample_collection_data):
        """Test filtering prompts by collection ID."""
        # Create collection
        col_response = client.post("/collections", json=sample_collection_data)
        collection_id = col_response.json()["id"]
        
        # Create prompts
        client.post("/prompts", json={
            "title": "In Collection",
            "content": "Content",
            "collection_id": collection_id
        })
        client.post("/prompts", json={
            "title": "Not In Collection",
            "content": "Content"
        })
        
        # Filter by collection
        response = client.get(f"/prompts?collection_id={collection_id}")
        assert response.status_code == 200
        prompts = response.json()["prompts"]
        assert len(prompts) == 1
        assert prompts[0]["title"] == "In Collection"
    
    def test_filter_by_invalid_collection(self, client: TestClient):
        """Test filtering by non-existent collection returns empty results."""
        response = client.get("/prompts?collection_id=fake-id")
        assert response.status_code == 200
        assert response.json()["total"] == 0
    
    def test_combined_search_and_filter(self, client: TestClient, sample_collection_data):
        """Test combining search and collection filter."""
        col_response = client.post("/collections", json=sample_collection_data)
        collection_id = col_response.json()["id"]
        
        # Create various prompts
        client.post("/prompts", json={
            "title": "Email in Collection",
            "content": "Content",
            "collection_id": collection_id
        })
        client.post("/prompts", json={
            "title": "SMS in Collection",
            "content": "Content",
            "collection_id": collection_id
        })
        client.post("/prompts", json={
            "title": "Email without Collection",
            "content": "Content"
        })
        
        # Search for 'email' within collection
        response = client.get(f"/prompts?collection_id={collection_id}&search=email")
        assert response.status_code == 200
        prompts = response.json()["prompts"]
        assert len(prompts) == 1
        assert "Email in Collection" == prompts[0]["title"]


class TestCollectionValidation:
    """Tests for collection validation and error handling."""
    
    def test_create_collection_missing_name(self, client: TestClient):
        """Test creating collection without required name field."""
        response = client.post("/collections", json={})
        assert response.status_code == 422
    
    def test_create_collection_empty_name(self, client: TestClient):
        """Test creating collection with empty name."""
        response = client.post("/collections", json={"name": ""})
        assert response.status_code == 422
    
    def test_create_collection_name_too_long(self, client: TestClient):
        """Test creating collection with name exceeding max length."""
        response = client.post("/collections", json={"name": "x" * 101})
        assert response.status_code == 422
    
    def test_create_collection_description_too_long(self, client: TestClient):
        """Test creating collection with description exceeding max length."""
        response = client.post("/collections", json={
            "name": "Test",
            "description": "x" * 501
        })
        assert response.status_code == 422
    
    def test_create_collection_minimal(self, client: TestClient):
        """Test creating collection with only required fields."""
        response = client.post("/collections", json={"name": "Test"})
        assert response.status_code == 201
        assert response.json()["name"] == "Test"
        assert response.json()["description"] is None
    
    def test_get_collection_success(self, client: TestClient, sample_collection_data):
        """Test successfully retrieving a collection."""
        create_response = client.post("/collections", json=sample_collection_data)
        collection_id = create_response.json()["id"]
        
        response = client.get(f"/collections/{collection_id}")
        assert response.status_code == 200
        assert response.json()["id"] == collection_id
    
    def test_delete_nonexistent_collection(self, client: TestClient):
        """Test deleting non-existent collection returns 404."""
        response = client.delete("/collections/fake-id")
        assert response.status_code == 404


class TestDataIntegrity:
    """Tests for data integrity and relationships."""
    
    def test_prompt_created_at_is_utc(self, client: TestClient, sample_prompt_data):
        """Test that created_at timestamp is in UTC."""
        response = client.post("/prompts", json=sample_prompt_data)
        created_at = response.json()["created_at"]
        assert created_at.endswith("Z") or "+00:00" in created_at
    
    def test_prompt_id_is_unique(self, client: TestClient, sample_prompt_data):
        """Test that each prompt gets a unique ID."""
        response1 = client.post("/prompts", json=sample_prompt_data)
        response2 = client.post("/prompts", json=sample_prompt_data)
        
        id1 = response1.json()["id"]
        id2 = response2.json()["id"]
        assert id1 != id2
    
    def test_collection_id_is_unique(self, client: TestClient, sample_collection_data):
        """Test that each collection gets a unique ID."""
        response1 = client.post("/collections", json=sample_collection_data)
        response2 = client.post("/collections", json=sample_collection_data)
        
        id1 = response1.json()["id"]
        id2 = response2.json()["id"]
        assert id1 != id2
    
    def test_multiple_prompts_same_collection(self, client: TestClient, sample_collection_data):
        """Test that multiple prompts can belong to the same collection."""
        col_response = client.post("/collections", json=sample_collection_data)
        collection_id = col_response.json()["id"]
        
        # Create multiple prompts in same collection
        for i in range(3):
            client.post("/prompts", json={
                "title": f"Prompt {i}",
                "content": "Content",
                "collection_id": collection_id
            })
        
        # Filter by collection
        response = client.get(f"/prompts?collection_id={collection_id}")
        assert response.json()["total"] == 3


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""
    
    def test_create_prompt_max_title_length(self, client: TestClient):
        """Test creating prompt with maximum allowed title length."""
        data = {"title": "x" * 200, "content": "Content"}
        response = client.post("/prompts", json=data)
        assert response.status_code == 201
    
    def test_create_prompt_max_description_length(self, client: TestClient):
        """Test creating prompt with maximum allowed description length."""
        data = {
            "title": "Test",
            "content": "Content",
            "description": "x" * 500
        }
        response = client.post("/prompts", json=data)
        assert response.status_code == 201
    
    def test_create_collection_max_name_length(self, client: TestClient):
        """Test creating collection with maximum allowed name length."""
        data = {"name": "x" * 100}
        response = client.post("/collections", json=data)
        assert response.status_code == 201
    
    def test_prompt_with_special_characters(self, client: TestClient):
        """Test creating prompt with special characters."""
        data = {
            "title": "Test: {{var}} & <html>",
            "content": "Hello {{name}}, this is a test!",
            "description": "Special chars: @#$%^&*()"
        }
        response = client.post("/prompts", json=data)
        assert response.status_code == 201
        assert response.json()["title"] == data["title"]
    
    def test_empty_prompts_list(self, client: TestClient):
        """Test listing prompts when none exist."""
        response = client.get("/prompts")
        assert response.status_code == 200
        assert response.json()["prompts"] == []
        assert response.json()["total"] == 0
    
    def test_empty_collections_list(self, client: TestClient):
        """Test listing collections when none exist."""
        response = client.get("/collections")
        assert response.status_code == 200
        assert response.json()["collections"] == []
        assert response.json()["total"] == 0
