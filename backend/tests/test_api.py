"""API tests for PromptLab

These tests verify the API endpoints work correctly.
Students should expand these tests significantly in Week 3.
"""

from fastapi.testclient import TestClient


class TestHealth:
    """Tests for health endpoint."""
    
    def test_health_successful_creation(self, client: TestClient):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert isinstance(data["version"], str)
        assert data["version"]
    
    def test_health_partial_failure_with_mixed_query_params(self, client: TestClient):
        response = client.get("/health", params=[("status", "healthy"), ("unexpected", "")])
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["version"]
    
    def test_health_empty_input_defaults(self, client: TestClient):
        response = client.get("/health", params={"status": ""})
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["version"]
    
    def test_health_invalid_method_error(self, client: TestClient):
        response = client.post("/health")
        assert response.status_code == 405
        allow_header = response.headers.get("allow")
        assert allow_header is not None
        assert "GET" in allow_header
    
    def test_health_edge_case_head_request(self, client: TestClient):
        response = client.request("HEAD", "/health")
        assert response.status_code == 405
        allow_header = response.headers.get("allow")
        assert allow_header is not None
        assert "GET" in allow_header
    
    def test_health_query_parameters_do_not_override_version(self, client: TestClient):
        response = client.get("/health", params={"version": "9.9.9"})
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["version"] != "9.9.9"


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
    
    def test_create_prompt_bulk_success(self, client: TestClient):
        payloads = [
            {"title": f"Prompt {i}", "content": f"Content {i}"}
            for i in range(3)
        ]
        for payload in payloads:
            response = client.post("/prompts", json=payload)
            assert response.status_code == 201
        list_response = client.get("/prompts")
        assert list_response.status_code == 200
        assert list_response.json()["total"] == len(payloads)
    
    def test_create_prompt_partial_failure_with_mixed_payloads(self, client: TestClient):
        payloads = [
            {"title": "Valid 1", "content": "Content 1"},
            {"title": "", "content": "Missing title should fail"},
            {"title": "Valid 2", "content": "Content 2"},
        ]
        statuses = [client.post("/prompts", json=payload).status_code for payload in payloads]
        assert statuses == [201, 422, 201]
        prompts = client.get("/prompts").json()["prompts"]
        assert len(prompts) == 2
        assert all(prompt["title"].startswith("Valid") for prompt in prompts)
    
    def test_create_prompt_empty_input(self, client: TestClient):
        response = client.post("/prompts", json={})
        assert response.status_code == 422
        error = response.json()
        assert error["detail"]
    
    def test_create_prompt_error_invalid_collection(self, client: TestClient, sample_prompt_data):
        payload = {**sample_prompt_data, "collection_id": "missing-collection"}
        response = client.post("/prompts", json=payload)
        assert response.status_code == 400
        assert response.json()["detail"] == "Collection not found"
    
    def test_create_prompt_edge_case_minimal_fields(self, client: TestClient):
        payload = {"title": "A", "content": "B"}
        response = client.post("/prompts", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "A"
        assert data["content"] == "B"
        assert data["description"] is None
    
    def test_create_prompt_with_query_parameters(self, client: TestClient, sample_prompt_data):
        response = client.post("/prompts?dry_run=true", json=sample_prompt_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == sample_prompt_data["title"]
        prompts = client.get("/prompts", params={"dry_run": "true"}).json()
        assert prompts["total"] == 1
    
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
    
    def test_list_prompts_successful_multiple_entries(self, client: TestClient):
        payloads = [
            {"title": f"Prompt {i}", "content": f"Content {i}"}
            for i in range(5)
        ]
        for payload in payloads:
            client.post("/prompts", json=payload)
        response = client.get("/prompts")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 5
        returned_titles = [prompt["title"] for prompt in data["prompts"]]
        assert returned_titles[0] == "Prompt 4"
        assert returned_titles[-1] == "Prompt 0"
    
    def test_list_prompts_partial_failure_mixed_creations(self, client: TestClient):
        payloads = [
            {"title": "Valid", "content": "Good"},
            {"title": "", "content": "Bad"},
            {"title": "Valid 2", "content": "Good 2"},
        ]
        statuses = [client.post("/prompts", json=p).status_code for p in payloads]
        assert statuses == [201, 422, 201]
        response = client.get("/prompts")
        data = response.json()
        assert data["total"] == 2
        assert all(prompt["title"].startswith("Valid") for prompt in data["prompts"])
    
    def test_list_prompts_empty_input_search_param(self, client: TestClient, sample_prompt_data):
        client.post("/prompts", json=sample_prompt_data)
        response = client.get("/prompts", params={"search": ""})
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
    
    def test_list_prompts_error_invalid_method(self, client: TestClient):
        response = client.delete("/prompts")
        assert response.status_code == 405
        assert "GET" in response.headers.get("allow", "")
    
    def test_list_prompts_edge_case_special_characters(self, client: TestClient):
        payload = {"title": "🚀 Launch", "content": "Prepare"}
        client.post("/prompts", json=payload)
        response = client.get("/prompts", params={"search": "🚀"})
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["prompts"][0]["title"] == "🚀 Launch"
    
    def test_list_prompts_query_parameters_collection_filter(self, client: TestClient, sample_prompt_data, sample_collection_data):
        collection_response = client.post("/collections", json=sample_collection_data)
        collection_id = collection_response.json()["id"]
        prompt_in_collection = {**sample_prompt_data, "collection_id": collection_id}
        client.post("/prompts", json=prompt_in_collection)
        client.post("/prompts", json={"title": "Other", "content": "Other"})
        response = client.get("/prompts", params={"collection_id": collection_id})
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["prompts"][0]["collection_id"] == collection_id

    def test_list_prompts_combined_filters_return_intersection(self, client: TestClient, sample_prompt_data, sample_collection_data):
        primary_collection_id = client.post("/collections", json=sample_collection_data).json()["id"]
        secondary_collection_id = client.post(
            "/collections",
            json={"name": "Secondary", "description": "Secondary collection"}
        ).json()["id"]

        matching_prompt = {
            **sample_prompt_data,
            "title": "Alpha Draft",
            "description": "Alpha research",
            "collection_id": primary_collection_id
        }
        same_collection_non_match = {
            "title": "Beta Draft",
            "content": "Beta research",
            "collection_id": primary_collection_id
        }
        different_collection_match = {
            "title": "Alpha Outside",
            "content": "Alpha content",
            "collection_id": secondary_collection_id
        }

        client.post("/prompts", json=matching_prompt)
        client.post("/prompts", json=same_collection_non_match)
        client.post("/prompts", json=different_collection_match)

        response = client.get(
            "/prompts",
            params={"collection_id": primary_collection_id, "search": "alpha"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["prompts"][0]["title"] == "Alpha Draft"
        assert data["prompts"][0]["collection_id"] == primary_collection_id

    def test_list_prompts_filters_can_exclude_all_results(self, client: TestClient, sample_prompt_data, sample_collection_data):
        collection_id = client.post("/collections", json=sample_collection_data).json()["id"]
        client.post("/prompts", json={**sample_prompt_data, "collection_id": collection_id})

        response = client.get(
            "/prompts",
            params={"collection_id": collection_id, "search": "no-match"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["prompts"] == []
    
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

    def test_get_prompt_success_returns_full_payload(self, client: TestClient, sample_prompt_data):
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        response = client.get(f"/prompts/{prompt_id}")
        assert response.status_code == 200
        data = response.json()
        for key in ("title", "content", "description", "created_at", "updated_at"):
            assert key in data
        assert data["id"] == prompt_id
    
    def test_get_prompt_partial_failure_mixed_ids(self, client: TestClient, sample_prompt_data):
        prompt_id = client.post("/prompts", json=sample_prompt_data).json()["id"]
        valid_response = client.get(f"/prompts/{prompt_id}")
        invalid_response = client.get("/prompts/invalid-id")
        assert valid_response.status_code == 200
        assert invalid_response.status_code == 404
    
    def test_get_prompt_empty_identifier_returns_404(self, client: TestClient):
        response = client.get("/prompts/%20")
        assert response.status_code == 404
    
    def test_get_prompt_error_invalid_method(self, client: TestClient, sample_prompt_data):
        prompt_id = client.post("/prompts", json=sample_prompt_data).json()["id"]
        response = client.post(f"/prompts/{prompt_id}")
        assert response.status_code == 405
        allow_header = response.headers.get("allow", "")
        assert "GET" in allow_header
    
    def test_get_prompt_edge_case_long_identifier(self, client: TestClient):
        long_id = "x" * 256
        response = client.get(f"/prompts/{long_id}")
        assert response.status_code == 404
    
    def test_get_prompt_query_parameters_ignored(self, client: TestClient, sample_prompt_data):
        prompt_id = client.post("/prompts", json=sample_prompt_data).json()["id"]
        response = client.get(f"/prompts/{prompt_id}", params={"verbose": "true"})
        assert response.status_code == 200
        assert response.json()["id"] == prompt_id

    
    def test_delete_prompt_successful_removal(self, client: TestClient, sample_prompt_data):
        prompt_id = client.post("/prompts", json=sample_prompt_data).json()["id"]
        response = client.delete(f"/prompts/{prompt_id}")
        assert response.status_code == 204
        follow_up = client.get(f"/prompts/{prompt_id}")
        assert follow_up.status_code == 404
    
    def test_delete_prompt_partial_failure_mixed_ids(self, client: TestClient, sample_prompt_data):
        valid_id = client.post("/prompts", json=sample_prompt_data).json()["id"]
        other_prompt_id = client.post(
            "/prompts",
            json={"title": "Keep", "content": "Stay"}
        ).json()["id"]
        valid_response = client.delete(f"/prompts/{valid_id}")
        invalid_response = client.delete("/prompts/does-not-exist")
        assert valid_response.status_code == 204
        assert invalid_response.status_code == 404
        remaining_prompts = client.get("/prompts").json()["prompts"]
        assert len(remaining_prompts) == 1
        assert remaining_prompts[0]["id"] == other_prompt_id
    
    def test_delete_prompt_with_empty_identifier(self, client: TestClient):
        response = client.delete("/prompts/%20")
        assert response.status_code == 404
    
    def test_delete_prompt_error_nonexistent_prompt(self, client: TestClient):
        response = client.delete("/prompts/unknown-id")
        assert response.status_code == 404
    
    def test_delete_prompt_edge_case_long_identifier(self, client: TestClient):
        long_id = "x" * 256
        response = client.delete(f"/prompts/{long_id}")
        assert response.status_code == 404
    
    def test_delete_prompt_query_parameters_ignored(self, client: TestClient, sample_prompt_data):
        prompt_id = client.post("/prompts", json=sample_prompt_data).json()["id"]
        response = client.delete(f"/prompts/{prompt_id}?force=true")
        assert response.status_code == 204
        assert client.get(f"/prompts/{prompt_id}").status_code == 404
    
    def test_patch_prompt(self, client: TestClient, sample_prompt_data):
        # Create a prompt first
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        original_updated_at = create_response.json()["updated_at"]
        # Patch it
        response = client.patch(f"/prompts/{prompt_id}", json={"title": "Patched Title"})
        assert response.status_code == 200
        data = response.json()

        assert data["title"] == "Patched Title"
        assert data["content"] == sample_prompt_data["content"]
        assert data["updated_at"] != original_updated_at 
        # Verify it's gone
        # get_response = client.get(f"/prompts/{prompt_id}")
        # Note: This might fail due to Bug #1
        # assert get_response.status_code in [404, 500]  # 404 after fix
    
    def test_patch_prompt_partial_failure_mixed_payloads(self, client: TestClient, sample_prompt_data):
        prompt_id = client.post("/prompts", json=sample_prompt_data).json()["id"]
        success = client.patch(f"/prompts/{prompt_id}", json={"description": "Updated desc"})
        failure = client.patch(f"/prompts/{prompt_id}", json={"title": ""})
        assert success.status_code == 200
        assert failure.status_code == 422
        latest = client.get(f"/prompts/{prompt_id}").json()
        assert latest["description"] == "Updated desc"
        assert latest["title"] == sample_prompt_data["title"]
    
    def test_patch_prompt_empty_body_updates_timestamp(self, client: TestClient, sample_prompt_data):
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        original_updated_at = create_response.json()["updated_at"]
        import time
        time.sleep(0.01)
        response = client.patch(f"/prompts/{prompt_id}", json={})
        assert response.status_code == 200
        data = response.json()
        assert data["updated_at"] != original_updated_at
        assert data["title"] == sample_prompt_data["title"]
    
    def test_patch_prompt_error_nonexistent_prompt(self, client: TestClient):
        response = client.patch("/prompts/unknown-id", json={"title": "New"})
        assert response.status_code == 404
        assert response.json()["detail"] == "Prompt not found"
    
    def test_patch_prompt_edge_case_minimal_title(self, client: TestClient, sample_prompt_data):
        prompt_id = client.post("/prompts", json=sample_prompt_data).json()["id"]
        response = client.patch(f"/prompts/{prompt_id}", json={"title": "A"})
        assert response.status_code == 200
        assert client.get(f"/prompts/{prompt_id}").json()["title"] == "A"
    
    def test_patch_prompt_query_parameters_ignored(self, client: TestClient, sample_prompt_data):
        prompt_id = client.post("/prompts", json=sample_prompt_data).json()["id"]
        response = client.patch(f"/prompts/{prompt_id}?preview=true", json={"description": "Preview"})
        assert response.status_code == 200
        assert client.get(f"/prompts/{prompt_id}").json()["description"] == "Preview"

    def test_patch_prompt_invalid_collection_returns_400(self, client: TestClient, sample_prompt_data):
        prompt_id = client.post("/prompts", json=sample_prompt_data).json()["id"]
        response = client.patch(f"/prompts/{prompt_id}", json={"collection_id": "missing"})
        assert response.status_code == 400
        assert response.json()["detail"] == "Collection not found"
    

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
        assert data["updated_at"] != original_updated_at
    
    def test_update_prompt_partial_failure_mixed_payloads(self, client: TestClient, sample_prompt_data):
        prompt_id = client.post("/prompts", json=sample_prompt_data).json()["id"]
        valid_payload = {
            "title": "Valid Update",
            "content": "New content",
            "description": "New description"
        }
        invalid_payload = {"title": "Missing fields"}
        valid_response = client.put(f"/prompts/{prompt_id}", json=valid_payload)
        invalid_response = client.put(f"/prompts/{prompt_id}", json=invalid_payload)
        assert valid_response.status_code == 200
        assert invalid_response.status_code == 422
        assert client.get(f"/prompts/{prompt_id}").json()["title"] == "Valid Update"
    
    def test_update_prompt_empty_payload(self, client: TestClient, sample_prompt_data):
        prompt_id = client.post("/prompts", json=sample_prompt_data).json()["id"]
        response = client.put(f"/prompts/{prompt_id}", json={})
        assert response.status_code == 422
    
    def test_update_prompt_error_nonexistent(self, client: TestClient):
        payload = {
            "title": "Doesn't matter",
            "content": "No prompt",
            "description": "No prompt"
        }
        response = client.put("/prompts/unknown-id", json=payload)
        assert response.status_code == 404
        assert response.json()["detail"] == "Prompt not found"
    
    def test_update_prompt_edge_case_min_lengths(self, client: TestClient, sample_prompt_data):
        prompt_id = client.post("/prompts", json=sample_prompt_data).json()["id"]
        payload = {"title": "A", "content": "B", "description": "C"}
        response = client.put(f"/prompts/{prompt_id}", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "A"
        assert data["content"] == "B"
    
    def test_update_prompt_query_parameters_ignored(self, client: TestClient, sample_prompt_data):
        prompt_id = client.post("/prompts", json=sample_prompt_data).json()["id"]
        payload = {
            "title": "Query Param Update",
            "content": "Same content",
            "description": "Same description"
        }
        response = client.put(f"/prompts/{prompt_id}?dry_run=true", json=payload)
        assert response.status_code == 200
        assert client.get(f"/prompts/{prompt_id}").json()["title"] == "Query Param Update"
    
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
    
    def test_sorting_order_partial_failure_excludes_invalid(self, client: TestClient):
        import time
        valid_old = {"title": "Old", "content": "Old"}
        valid_new = {"title": "New", "content": "New"}
        invalid_payload = {"title": "", "content": "Invalid"}
        client.post("/prompts", json=valid_old)
        time.sleep(0.02)
        assert client.post("/prompts", json=invalid_payload).status_code == 422
        time.sleep(0.02)
        client.post("/prompts", json=valid_new)
        response = client.get("/prompts")
        titles = [prompt["title"] for prompt in response.json()["prompts"]]
        assert titles[0] == "New"
        assert titles[-1] == "Old"
        assert all(title for title in titles)
    
    def test_sorting_order_empty_dataset(self, client: TestClient):
        response = client.get("/prompts")
        assert response.status_code == 200
        data = response.json()
        assert data["prompts"] == []
    
    def test_sorting_order_error_invalid_method(self, client: TestClient):
        response = client.delete("/prompts?_sort=true")
        assert response.status_code == 405
        assert "GET" in response.headers.get("allow", "")
    
    def test_sorting_order_edge_case_same_timestamp(self, client: TestClient):
        payload = {"title": "Same", "content": "Same time"}
        client.post("/prompts", json=payload)
        client.post("/prompts", json=payload)
        response = client.get("/prompts")
        data = response.json()["prompts"]
        assert len(data) == 2
        assert data[0]["title"] == "Same"
    
    def test_sorting_order_query_parameters_preserved(self, client: TestClient):
        client.post("/prompts", json={"title": "Alpha", "content": "Alpha"})
        client.post("/prompts", json={"title": "Beta", "content": "Beta"})
        response = client.get("/prompts", params={"search": "Beta"})
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["prompts"][0]["title"] == "Beta"


class TestPromptVersions:
    """Tests covering prompt versioning workflows."""

    def test_versions_list_empty_for_new_prompt(self, client: TestClient, sample_prompt_data):
        prompt_id = client.post("/prompts", json=sample_prompt_data).json()["id"]

        response = client.get(f"/prompts/{prompt_id}/versions")
        assert response.status_code == 200
        data = response.json()
        assert data["prompt_id"] == prompt_id
        assert data["total"] == 0
        assert data["versions"] == []

    def test_put_creates_version_and_accepts_change_note(self, client: TestClient, sample_prompt_data):
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        original_title = create_response.json()["title"]

        update_payload = {
            "title": "Updated Title",
            "content": "Updated content",
            "description": "Updated description",
            "change_note": "Initial edit",
        }
        update_response = client.put(f"/prompts/{prompt_id}", json=update_payload)
        assert update_response.status_code == 200
        updated_prompt = update_response.json()
        assert updated_prompt["title"] == "Updated Title"
        assert updated_prompt["current_version"] == 1

        versions = client.get(f"/prompts/{prompt_id}/versions").json()
        assert versions["total"] == 1
        snapshot = versions["versions"][0]
        assert snapshot["version_number"] == 1
        assert snapshot["change_note"] == "Initial edit"
        assert snapshot["editor"] == "system"

        version_detail = client.get(
            f"/prompts/{prompt_id}/versions/{snapshot['id']}"
        ).json()
        assert version_detail["title"] == original_title
        assert version_detail["version_number"] == 1

    def test_restore_prompt_version_reverts_content_and_records_new_version(self, client: TestClient, sample_prompt_data):
        prompt = client.post("/prompts", json=sample_prompt_data).json()
        prompt_id = prompt["id"]

        first_update = {
            "title": "First Update",
            "content": "First update content",
            "description": "First update description",
            "change_note": "First revision",
        }
        client.put(f"/prompts/{prompt_id}", json=first_update)

        second_update = {
            "title": "Second Update",
            "content": "Second update content",
            "description": "Second update description",
            "change_note": "Second revision",
        }
        client.put(f"/prompts/{prompt_id}", json=second_update)

        versions = client.get(f"/prompts/{prompt_id}/versions").json()
        assert versions["total"] == 2
        original_snapshot = next(
            version for version in versions["versions"]
            if version["version_number"] == 1
        )

        restore_response = client.post(
            f"/prompts/{prompt_id}/versions/{original_snapshot['id']}/restore",
            json={"change_note": "Rolled back to original"}
        )
        assert restore_response.status_code == 200
        restored_prompt = restore_response.json()
        assert restored_prompt["title"] == sample_prompt_data["title"]
        assert restored_prompt["current_version"] == 3

        refreshed_versions = client.get(f"/prompts/{prompt_id}/versions").json()
        assert refreshed_versions["total"] == 3
        assert refreshed_versions["versions"][0]["version_number"] == 3
        assert refreshed_versions["versions"][0]["change_note"] == "Rolled back to original"

    def test_restore_prompt_version_missing_returns_404(self, client: TestClient, sample_prompt_data):
        prompt_id = client.post("/prompts", json=sample_prompt_data).json()["id"]
        response = client.post(
            f"/prompts/{prompt_id}/versions/missing/restore",
            json={"change_note": "Should fail"}
        )
        assert response.status_code == 404

    def test_change_note_length_validation(self, client: TestClient, sample_prompt_data):
        prompt_id = client.post("/prompts", json=sample_prompt_data).json()["id"]
        payload = {
            "title": "Valid",
            "content": "Still valid",
            "description": "Desc",
            "change_note": "x" * 256,
        }
        response = client.put(f"/prompts/{prompt_id}", json=payload)
        assert response.status_code == 422

        patch_response = client.patch(
            f"/prompts/{prompt_id}",
            json={"change_note": "x" * 300}
        )
        assert patch_response.status_code == 422


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

    def test_get_collection_success(self, client: TestClient, sample_collection_data):
        collection_id = client.post("/collections", json=sample_collection_data).json()["id"]
        response = client.get(f"/collections/{collection_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == collection_id
        assert data["name"] == sample_collection_data["name"]
    
    def test_delete_collection_with_prompts(self, client: TestClient, sample_collection_data, sample_prompt_data):
        """Ensure deleting a collection clears the collection_id on associated prompts."""
        # Create collection
        col_response = client.post("/collections", json=sample_collection_data)
        collection_id = col_response.json()["id"]
        
        # Create prompt in collection
        prompt_data = {**sample_prompt_data, "collection_id": collection_id}
        prompt_response = client.post("/prompts", json=prompt_data)
        prompt_id = prompt_response.json()["id"]
        
        # Delete collection
        client.delete(f"/collections/{collection_id}")
        
        prompts = client.get("/prompts").json()["prompts"]
        assert len(prompts) == 1
        prompt = prompts[0]
        assert prompt["id"] == prompt_id
        assert prompt["collection_id"] is None

    def test_delete_collection_not_found(self, client: TestClient):
        response = client.delete("/collections/does-not-exist")
        assert response.status_code == 404
        assert response.json()["detail"] == "Collection not found"
    
    def test_create_collection_partial_failure(self, client: TestClient, sample_collection_data):
        valid_response = client.post("/collections", json=sample_collection_data)
        invalid_response = client.post("/collections", json={"name": "", "description": "Invalid"})
        assert valid_response.status_code == 201
        assert invalid_response.status_code == 422
        collections = client.get("/collections").json()["collections"]
        assert len(collections) == 1
        assert collections[0]["name"] == sample_collection_data["name"]
    
    def test_create_collection_empty_payload(self, client: TestClient):
        response = client.post("/collections", json={})
        assert response.status_code == 422
        assert response.json()["detail"]
    
    def test_collection_error_invalid_method(self, client: TestClient):
        response = client.delete("/collections")
        assert response.status_code == 405
        assert "GET" in response.headers.get("allow", "")
    
    def test_collection_edge_case_long_name(self, client: TestClient):
        payload = {"name": "X" * 100, "description": "Edge case"}
        response = client.post("/collections", json=payload)
        assert response.status_code == 201
        assert response.json()["name"] == "X" * 100
    
    def test_collection_query_parameters_ignored(self, client: TestClient, sample_collection_data):
        client.post("/collections", json=sample_collection_data)
        response = client.get("/collections", params={"search": sample_collection_data["name"]})
        assert response.status_code == 200
        data = response.json()
        assert len(data["collections"]) == 1
        assert data["collections"][0]["name"] == sample_collection_data["name"]
