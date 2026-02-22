"""Tests for tagging system feature.

This module implements tests for the tagging feature following TDD approach.
Tests are written first, then implementation follows.
"""

import pytest
from fastapi.testclient import TestClient


class TestTagEndpoints:
    """Tests for tag-related API endpoints."""
    
    def test_add_tag_to_prompt(self, client: TestClient, sample_prompt_data):
        """Test adding a single tag to a prompt."""
        # Create a prompt first
        response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = response.json()["id"]
        
        # Add a tag
        response = client.post(f"/prompts/{prompt_id}/tags", json={"tag": "python"})
        assert response.status_code == 200
        data = response.json()
        assert "python" in data["tags"]
    
    def test_add_multiple_tags_to_prompt(self, client: TestClient, sample_prompt_data):
        """Test adding multiple tags to a prompt."""
        # Create a prompt
        response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = response.json()["id"]
        
        # Add multiple tags
        client.post(f"/prompts/{prompt_id}/tags", json={"tag": "python"})
        client.post(f"/prompts/{prompt_id}/tags", json={"tag": "ai"})
        client.post(f"/prompts/{prompt_id}/tags", json={"tag": "coding"})
        
        # Get prompt and check tags
        response = client.get(f"/prompts/{prompt_id}")
        data = response.json()
        assert len(data["tags"]) == 3
        assert "python" in data["tags"]
        assert "ai" in data["tags"]
        assert "coding" in data["tags"]
    
    def test_remove_tag_from_prompt(self, client: TestClient, sample_prompt_data):
        """Test removing a tag from a prompt."""
        # Create prompt and add tag
        response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = response.json()["id"]
        client.post(f"/prompts/{prompt_id}/tags", json={"tag": "python"})
        
        # Remove the tag
        response = client.delete(f"/prompts/{prompt_id}/tags/python")
        assert response.status_code == 204
        
        # Verify tag is removed
        response = client.get(f"/prompts/{prompt_id}")
        assert "python" not in response.json()["tags"]
    
    def test_add_duplicate_tag_ignored(self, client: TestClient, sample_prompt_data):
        """Test that adding duplicate tag is ignored."""
        response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = response.json()["id"]
        
        # Add same tag twice
        client.post(f"/prompts/{prompt_id}/tags", json={"tag": "python"})
        client.post(f"/prompts/{prompt_id}/tags", json={"tag": "python"})
        
        # Should only have one instance
        response = client.get(f"/prompts/{prompt_id}")
        assert response.json()["tags"].count("python") == 1
    
    def test_filter_prompts_by_tag(self, client: TestClient):
        """Test filtering prompts by tag."""
        # Create multiple prompts with different tags
        p1 = client.post("/prompts", json={"title": "P1", "content": "Content1"})
        p1_id = p1.json()["id"]
        client.post(f"/prompts/{p1_id}/tags", json={"tag": "python"})
        
        p2 = client.post("/prompts", json={"title": "P2", "content": "Content2"})
        p2_id = p2.json()["id"]
        client.post(f"/prompts/{p2_id}/tags", json={"tag": "javascript"})
        
        p3 = client.post("/prompts", json={"title": "P3", "content": "Content3"})
        p3_id = p3.json()["id"]
        client.post(f"/prompts/{p3_id}/tags", json={"tag": "python"})
        
        # Filter by python tag
        response = client.get("/prompts?tag=python")
        assert response.status_code == 200
        prompts = response.json()["prompts"]
        assert len(prompts) == 2
        titles = [p["title"] for p in prompts]
        assert "P1" in titles
        assert "P3" in titles
        assert "P2" not in titles
    
    def test_get_all_tags(self, client: TestClient):
        """Test getting all unique tags in the system."""
        # Create prompts with various tags
        p1 = client.post("/prompts", json={"title": "P1", "content": "C1"}).json()
        p2 = client.post("/prompts", json={"title": "P2", "content": "C2"}).json()
        
        client.post(f"/prompts/{p1['id']}/tags", json={"tag": "python"})
        client.post(f"/prompts/{p1['id']}/tags", json={"tag": "ai"})
        client.post(f"/prompts/{p2['id']}/tags", json={"tag": "python"})
        client.post(f"/prompts/{p2['id']}/tags", json={"tag": "javascript"})
        
        # Get all tags
        response = client.get("/tags")
        assert response.status_code == 200
        tags = response.json()["tags"]
        assert len(tags) == 3
        assert "python" in tags
        assert "ai" in tags
        assert "javascript" in tags
    
    def test_tag_validation_empty_string(self, client: TestClient, sample_prompt_data):
        """Test that empty tag strings are rejected."""
        response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = response.json()["id"]
        
        # Try to add empty tag
        response = client.post(f"/prompts/{prompt_id}/tags", json={"tag": ""})
        assert response.status_code == 422
    
    def test_tag_validation_whitespace_only(self, client: TestClient, sample_prompt_data):
        """Test that whitespace-only tags are rejected."""
        response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = response.json()["id"]
        
        # Try to add whitespace tag
        response = client.post(f"/prompts/{prompt_id}/tags", json={"tag": "   "})
        assert response.status_code == 422
    
    def test_tag_normalized_lowercase(self, client: TestClient, sample_prompt_data):
        """Test that tags are normalized to lowercase."""
        response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = response.json()["id"]
        
        # Add tag with mixed case
        client.post(f"/prompts/{prompt_id}/tags", json={"tag": "PyThOn"})
        
        # Should be stored as lowercase
        response = client.get(f"/prompts/{prompt_id}")
        assert "python" in response.json()["tags"]
        assert "PyThOn" not in response.json()["tags"]
    
    def test_remove_tag_from_nonexistent_prompt(self, client: TestClient):
        """Test removing tag from prompt that doesn't exist."""
        response = client.delete("/prompts/nonexistent/tags/python")
        assert response.status_code == 404
    
    def test_remove_nonexistent_tag(self, client: TestClient, sample_prompt_data):
        """Test removing a tag that doesn't exist on the prompt."""
        response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = response.json()["id"]
        
        # Try to remove tag that was never added
        response = client.delete(f"/prompts/{prompt_id}/tags/python")
        assert response.status_code == 404
    
    def test_create_prompt_with_tags(self, client: TestClient):
        """Test creating a prompt with tags in the initial request."""
        data = {
            "title": "Test Prompt",
            "content": "Test content for prompt",
            "tags": ["python", "ai", "coding"]
        }
        
        response = client.post("/prompts", json=data)
        assert response.status_code == 201
        assert len(response.json()["tags"]) == 3
        assert "python" in response.json()["tags"]
