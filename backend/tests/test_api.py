"""API tests for PromptLab

These tests verify the API endpoints work correctly.
Students should expand these tests significantly in Week 3.
"""

import pytest
from fastapi.testclient import TestClient
from app.models import PromptPatch
from app.api import app
from app.models import Prompt
import json

client = TestClient(app)

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

# ============================================================================
# FIXTURES - Test Data Setup
# ============================================================================

    # Add missing fixtures for setup and teardown as needed
    @pytest.fixture
    def valid_prompt_data(self):
        """Fixture with valid prompt data."""
        return {
            "title": "Test Prompt",
            "content": "This is some test content."
        }

    @pytest.fixture
    def created_prompt(self):
        """Fixture to create and return a test prompt."""
        prompt_data = {
            "title": "Test Prompt",
            "content": "This is a test prompt content."
        }
        response = client.post('/prompts', json=prompt_data)
        assert response.status_code == 201
        return response.json()  # Returns created prompt, including the ID
    
    @pytest.fixture
    def nonexistent_id(self):
        """Fixture that returns a non-existent prompt ID."""
        return "nonexistent-prompt-id-0000"

# ============================================================================
# TEST: List Prompts Endpoint
# ============================================================================

    # Happy Path
    def test_list_prompts_all(self):
        """Test listing all prompts without any filtering."""
        response = client.get('/prompts')
        assert response.status_code == 200
        assert 'prompts' in response.json()
        assert isinstance(response.json()['prompts'], list)

    def test_list_prompts_with_valid_collection(self):
        """Test listing prompts with a valid existing collection."""
        # Create a collection first
        collection_data = {
            "name": "Test Collection",
            "description": "A test collection for prompts"
        }
        create_collection_response = client.post("/collections", json=collection_data)
        assert create_collection_response.status_code == 201
        created_collection_id = create_collection_response.json()["id"]

        # Once the collection is created, list prompts with this valid collection
        response = client.get(f'/prompts?collection_id={created_collection_id}')
        assert response.status_code == 200

    def test_list_prompts_with_valid_search(self):
        """Test listing prompts with a valid search query."""
        response = client.get('/prompts?search=test')
        assert response.status_code == 200

    # Error Cases
    def test_list_prompts_invalid_collection(self):
        """Test listing prompts with an invalid collection ID returns 400."""
        response = client.get('/prompts?collection_id=invalid')
        assert response.status_code == 400

    # Edge Cases
    def test_list_prompts_no_matches(self):
        """Test listing prompts with no matches in search results."""
        response = client.get('/prompts?search=no_match')
        assert response.status_code == 200
        assert len(response.json()['prompts']) == 0

    def test_list_prompts_no_prompts(self):
        """Test listing prompts when there are no prompts available."""
        # This requires an initial condition where the database is empty.
        response = client.get('/prompts')
        assert response.status_code == 200
        assert len(response.json()['prompts']) == 0

    def test_list_prompts_with_special_characters_in_search(self):
        """Test listing prompts with special characters in search query."""
        response = client.get('/prompts?search=%!@#%')
        assert response.status_code == 200

    # Query Parameter Tests
    def test_list_prompts_combined_filters(self):
        """Test listing prompts with both collection filter and search query."""
        # Create a collection first
        collection_data = {
            "name": "Combined Filter Collection",
            "description": "For testing combined filters"
        }
        create_collection_response = client.post("/collections", json=collection_data)
        assert create_collection_response.status_code == 201
        created_collection_id = create_collection_response.json()["id"]

        # Once the collection is created, test combined filters
        response = client.get(f'/prompts?collection_id={created_collection_id}&search=query')
        assert response.status_code == 200

    def test_list_prompts_invalid_collection_id_format(self):
        """Test listing prompts with invalid collection ID format."""
        response = client.get('/prompts?collection_id=12345')
        assert response.status_code == 400  # Assuming validation checks on UUID
# ============================================================================
    # TEST: Retrieve Prompt by ID
    # ============================================================================
    
    def test_get_prompt_valid_id(self, created_prompt):
        """Test retrieving prompt with a valid ID."""
        prompt_id = created_prompt['id']
        response = client.get(f'/prompts/{prompt_id}')
        assert response.status_code == 200
        assert response.json()['title'] == created_prompt['title']

    def test_get_prompt_invalid_id_format(self):
        """Test retrieving a prompt with an invalid ID format returns 400."""
        response = client.get('/prompts/invalid-format')
        assert response.status_code == 404

    def test_get_prompt_nonexistent_id(self):
        """Test retrieving a non-existent prompt ID returns 404."""
        response = client.get('/prompts/00000000-0000-0000-0000-000000000000')
        assert response.status_code == 404
    
    def test_get_prompt_valid_id(self, created_prompt):
        """Test retrieving a prompt with a valid ID."""
        prompt_id = created_prompt['id']
        response = client.get(f'/prompts/{prompt_id}')
        assert response.status_code == 200
        assert response.json()['title'] == created_prompt['title']

    def test_get_prompt_invalid_id_format(self):
        """Test retrieving a prompt with an invalid ID format returns 404."""
        response = client.get('/prompts/invalid-format')
        assert response.status_code == 404

    def test_get_prompt_malformed_id(self):
        """Test retrieving a prompt with a malformed ID returns 400."""
        response = client.get('/prompts/!@#%-id')
        assert response.status_code == 400
        assert 'Malformed prompt ID' in response.json().get('detail', '')

    def test_get_prompt_excessively_long_id(self):
        """Test retrieving a prompt with an excessively long ID returns 400."""
        long_id = 'a' * 1000  # Assume 1000 chars is excessively long
        response = client.get(f'/prompts/{long_id}')
        assert response.status_code == 400
        assert 'Invalid ID format' in response.json().get('detail', '')
    
    # ============================================================================
    # TEST: Create Prompt
    # ============================================================================

    def test_create_prompt_valid_data(self, valid_prompt_data):
        """Test creating a prompt with valid data returns 201."""
        response = client.post('/prompts', json=valid_prompt_data)
        assert response.status_code == 201
        assert 'id' in response.json(), "Response missing prompt ID"

    def test_create_prompt_missing_fields(self):
        """Test creating a prompt with missing fields returns 422."""
        response = client.post('/prompts', json={"title": "Only Title"})
        assert response.status_code == 422

    def test_create_prompt_empty_payload(self):
        """Test posting an empty JSON returns 422."""
        response = client.post('/prompts', json={})
        assert response.status_code == 422
    
    def test_create_prompt_with_long_title_and_content(self):
        """Test creating a prompt with excessively long title and content."""
        long_title = 'a' * 256
        long_content = 'b' * 1024  # Assuming these lengths are excessive
        response = client.post('/prompts', json={"title": long_title, "content": long_content})
        assert response.status_code == 422  # Assuming validation fails for long input

    def test_create_prompt_with_special_characters(self):
        """Test creating a prompt with special characters in title and content."""
        special_title = "!@#%^&*()_+=-[]{}|;:'<>,.?/~`"
        special_content = "Content!@#%^&*()"
        response = client.post('/prompts', json={"title": special_title, "content": special_content})
        assert response.status_code == 201
        assert response.json()['title'] == special_title

    def test_create_prompt_with_duplicate_title(self):
        """Test creating a prompt with a duplicate title."""
        # Assuming titles should be unique within a collection or system
        prompt_data = {"title": "Duplicate Title", "content": "Content for duplicate title."}
        client.post('/prompts', json=prompt_data)  # Create the initial prompt
        response = client.post('/prompts', json=prompt_data)  # Attempt to create a duplicate
        assert response.status_code == 409  # Assuming 409 Conflict for duplicates
    
    # ============================================================================
    # TEST: Update Prompt
    # ============================================================================

    def test_update_prompt_valid_data(self, created_prompt):
        """Test updating a prompt with valid data returns 200."""
        prompt_id = created_prompt['id']
        update_data = {"title": "Updated Title", "content": "Updated content"}
        response = client.put(f'/prompts/{prompt_id}', json=update_data)
        assert response.status_code == 200
        updated_prompt = response.json()
        assert updated_prompt['title'] == "Updated Title"

    def test_update_prompt_nonexistent_id(self):
        """Test updating a non-existent prompt returns 404."""
        response = client.put('/prompts/00000000-0000-0000-0000-000000000000', json={"title": "Update", "content": "Updated Content"})
        assert response.status_code == 404

    # Happy Path
    def test_update_prompt_valid_data(self, created_prompt):
        """Test updating a prompt with valid data returns 200."""
        prompt_id = created_prompt['id']
        update_data = {"title": "Updated Title", "content": "Updated content"}
        response = client.put(f'/prompts/{prompt_id}', json=update_data)
        assert response.status_code == 200
        updated_prompt = response.json()
        assert updated_prompt['title'] == "Updated Title"

    # Error Cases
    def test_update_prompt_nonexistent_id(self):
        """Test updating a non-existent prompt returns 404."""
        response = client.put('/prompts/00000000-0000-0000-0000-000000000000', json={"title": "Update", "content": "Updated Content"})
        assert response.status_code == 404

    def test_update_prompt_invalid_id_format(self):
        """Test updating a prompt with an invalid ID format returns 400."""
        response = client.put('/prompts/@-!-@invalid-format', json={"title": "Title", "content": "Content"})
        assert response.status_code == 400

    # Edge Cases
    def test_update_prompt_with_empty_fields(self, created_prompt):
        """Test updating a prompt with empty fields returns 422."""
        prompt_id = created_prompt['id']
        update_data = {"title": "", "content": ""}
        response = client.put(f'/prompts/{prompt_id}', json=update_data)
        assert response.status_code == 422  # Assuming empty strings are invalid

    def test_update_prompt_with_special_characters(self, created_prompt):
        """Test updating a prompt with special characters."""
        prompt_id = created_prompt['id']
        update_data = {
            "title": "!@#%^&*()_+=-[]{}|;:'<>,.?/~`",
            "content": "Content!@#%^&*()"
        }
        response = client.put(f'/prompts/{prompt_id}', json=update_data)
        assert response.status_code == 200
        updated_prompt = response.json()
        assert updated_prompt['title'] == "!@#%^&*()_+=-[]{}|;:'<>,.?/~`"

    # ============================================================================
    # TEST: Patch Prompt
    # ============================================================================
    
        # Happy Path
    def test_patch_prompt_valid_data(self, created_prompt):
        """Test patching a prompt with valid data."""
        prompt_id = created_prompt['id']
        # Arrange - Prepare valid data for patching
        valid_data = {
            "title": "New Title",
            "content": "Updated content.",
            "description": "Updated description",
            "collection_id": "collection123"
        }
        update_data = PromptPatch(**valid_data).model_dump(exclude_unset=True)
        response = client.patch(f'/prompts/{prompt_id}', json=update_data)
        assert response.status_code == 200
        updated_prompt = response.json()
        assert updated_prompt['title'] == update_data["title"]

    # Error Cases
    def test_patch_prompt_nonexistent_id(self):
        """Test patching a non-existent prompt returns 404."""
        update_data = PromptPatch(title="Title").model_dump(exclude_unset=True)
        response = client.patch('/prompts/00000000-0000-0000-0000-000000000000', json=update_data)
        assert response.status_code == 404

    def test_patch_prompt_invalid_id_format(self):
        """Test patching a prompt with invalid ID format returns 400."""
        update_data = PromptPatch(title="Title").model_dump(exclude_unset=True)
        response = client.patch('/prompts/invalid-format', json=update_data)
        assert response.status_code == 404

    def test_patch_prompt_with_special_characters(self, created_prompt):
        """Test patching a prompt with special characters."""
        prompt_id = created_prompt['id']
        update_data = PromptPatch(title="!@#%^&*()_+=-[]{}|;:'<>,.?/~`").model_dump(exclude_unset=True)
        response = client.patch(f'/prompts/{prompt_id}', json=update_data)
        assert response.status_code == 200
        updated_prompt = response.json()
        assert updated_prompt['title'] == "!@#%^&*()_+=-[]{}|;:'<>,.?/~`"
    # ============================================================================
    # TEST: Delete Prompt
    # ============================================================================

    # Happy Path
    def test_delete_prompt_valid_id(self, created_prompt):
        """Test deletion of an existing prompt by valid ID."""
        prompt_id = created_prompt['id']
        response = client.delete(f'/prompts/{prompt_id}')
        assert response.status_code == 204

        # Verify that prompt no longer exists
        get_response = client.get(f'/prompts/{prompt_id}')
        assert get_response.status_code == 404

    # Error Cases
    def test_delete_prompt_nonexistent_id(self, nonexistent_id):
        """Test deletion of a prompt by a non-existent ID returns 404."""
        response = client.delete(f'/prompts/{nonexistent_id}')
        assert response.status_code == 404
        assert 'not found' in response.json().get('detail', '').lower()

    def test_delete_prompt_empty_id(self):
        """Test deletion of a prompt with empty ID should raise HTTPException."""
        response = client.delete('/prompts/')
        assert response.status_code == 405

    def test_delete_prompt_invalid_id_format(self):
        """Test deletion with invalid ID format should trigger a handling mechanism."""
        response = client.delete('/prompts/invalid-format-!!!@@')
        assert response.status_code == 400

    # Edge Cases
    def test_delete_prompt_with_special_characters_in_id(self):
        """Test deletion with special characters in ID should result in not found."""
        special_id = "special-!@#-characters"
        response = client.delete(f'/prompts/{special_id}')
        assert response.status_code == 400
        assert 'malformed prompt id' in response.json().get('detail', '').lower()


# ============================================================================
# FIXTURES - Test Data Setup
# ============================================================================

@pytest.fixture
def api_client():
    """Fixture providing API client for testing."""
    return TestClient(app)

@pytest.fixture
def created_collections(api_client):
    """Fixture to create multiple collections for testing."""
    collections = []
    for i in range(3):
        collection_name = f"Collection {i}"
        collection_data = {"name": collection_name, "description": f"Description {i}"}
        response = api_client.post('/collections', json=collection_data)
        assert response.status_code == 201
        collections.append(response.json())
    return collections

@pytest.fixture
def created_collection():
    """Fixture that creates a collection and returns its data."""
    collection_data = {"name": "Test Collection"}
    response = client.post('/collections', json=collection_data)
    assert response.status_code == 201, "Failed to create test collection"
    return response.json()  # Returns created collection with ID

@pytest.fixture
def nonexistent_collection_id():
    """Fixture that provides a non-existent collection ID."""
    return "00000000-0000-0000-0000-000000000000"  # UUID that doesn't exist

# ============================================================================
# TEST: List Collections Endpoint
# ============================================================================

class TestListCollections:
    """Tests for listing collections."""

    def test_list_collections_returns_200(self, api_client, created_collections):
        """Test successful list of collections returns 200."""
        response = api_client.get('/collections')
        assert response.status_code == 200
        collection_list = response.json()
        
        assert len(collection_list['collections']) == len(created_collections)
        assert collection_list['total'] == len(created_collections)
        for idx, collection in enumerate(created_collections):
            assert collection['name'] == collection_list['collections'][idx]['name']

    def test_list_collections_empty_returns_200(self, api_client):
        """Test listing collections when no collections exist returns empty list."""
        # Assuming this test runs in isolation without the fixture
        response = api_client.get('/collections')
        assert response.status_code == 200
        
        collection_list = response.json()
        assert collection_list['collections'] == []
        assert collection_list['total'] == 0

# ============================================================================
# FIXTURES - Test Data Setup
# ============================================================================

@pytest.fixture
def created_collection():
    """Fixture that creates a collection and returns its data."""
    collection_data = {"name": "Test Collection"}
    response = client.post('/collections', json=collection_data)
    assert response.status_code == 201, "Failed to create test collection"
    return response.json()  # Returns created collection with ID


@pytest.fixture
def nonexistent_collection_id():
    """Fixture that provides a non-existent collection ID."""
    return "00000000-0000-0000-0000-000000000000"  # UUID that doesn't exist

@pytest.fixture
def valid_collection_data():
    """Fixture providing valid collection data."""
    return {
        "name": "Test Collection",
        "description": "A test description for the collection"
    }

@pytest.fixture
def created_prompts(api_client, created_collection):
    """Fixture creating multiple prompts associated with the created collection."""
    collection_id = created_collection['id']
    prompts = []
    for i in range(3):
        prompt_data = {
            "title": f"Test Prompt {i}",
            "content": f"Content {i}",
            "collection_id": collection_id
        }
        response = api_client.post('/prompts', json=prompt_data)
        assert response.status_code == 201
        prompts.append(response.json())
    return prompts
# ============================================================================
# TEST: Get Collection Endpoint
# ============================================================================

class TestGetCollection:
    """Tests for retrieving collection by ID."""
    
    def test_get_collection_by_valid_id_returns_200(self, created_collection):
        """Test retrieval of collection by valid ID returns 200."""
        collection_id = created_collection['id']
        response = client.get(f'/collections/{collection_id}')
        assert response.status_code == 200
        assert response.json()['id'] == collection_id
        assert 'name' in response.json()

    def test_get_collection_with_nonexistent_id_returns_404(self, nonexistent_collection_id):
        """Test retrieval of collection with non-existent ID returns 404."""
        response = client.get(f'/collections/{nonexistent_collection_id}')
        assert response.status_code == 404
        assert 'Collection not found' in response.json()['detail']

# ============================================================================
# TEST: Create Collection Endpoint
# ============================================================================

class TestCreateCollection:
    """Tests for creating a new collection."""

    # Happy Path
    def test_create_collection_with_valid_data_returns_201(self, api_client, valid_collection_data):
        """Test creating collection with valid data returns 201."""
        response = api_client.post('/collections', json=valid_collection_data)
        
        assert response.status_code == 201
        data = response.json()
        assert 'id' in data
        assert data['name'] == valid_collection_data['name']
        assert data['description'] == valid_collection_data['description']

    # Error Cases
    def test_create_collection_missing_name_returns_422(self, api_client):
        """Test creating a collection without a name returns 422."""
        collection_data = {"description": "Description without a name"}
        response = api_client.post('/collections', json=collection_data)
        assert response.status_code == 422

    def test_create_collection_duplicate_name_returns_409(self, api_client, created_collection):
        """Test creating a collection with a duplicate name returns 409."""
        duplicate_data = {
            "name": created_collection['name'],
            "description": "Another description"
        }
        response = api_client.post('/collections', json=duplicate_data)

        assert response.status_code == 409
        assert "already exists" in response.json().get('detail', '').lower()

    # Edge Cases
    @pytest.mark.parametrize("name", [
        "",     # Empty name
        "   ",  # Whitespace name
        "a" * 300  # Very long name
    ])
    def test_create_collection_edge_case_names(self, api_client, name):
        """Test creating collections with edge case names."""
        collection_data = {"name": name, "description": "Valid description"}
        response = api_client.post('/collections', json=collection_data)

        assert response.status_code in [400, 422]

    # Input Variations
    def test_create_collection_with_full_input(self, api_client):
        """Test creating a collection with all fields."""
        full_data = {
            "name": "Comprehensive Collection",
            "description": "Full description testing",
            "extra_field": "Extra value"  # Assuming this field is optional
        }
        response = api_client.post('/collections', json=full_data)

        assert response.status_code == 201
        data = response.json()
        assert data['name'] == "Comprehensive Collection"
        assert data['description'] == "Full description testing"

    def test_create_collection_with_partial_input(self, api_client):
        """Test creating collection with only the name field."""
        partial_data = {"name": "Name Only Collection"}
        response = api_client.post('/collections', json=partial_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data['name'] == "Name Only Collection"

# ============================================================================
# TEST: Delete Collection Endpoint
# ============================================================================

class TestDeleteCollection:
    """Tests for deleting a collection."""

    # Happy Path
    def test_delete_collection_successfully_returns_204(self, api_client, created_collection):
        """Test successfully deleting a collection returns 204."""
        collection_id = created_collection['id']
        response = api_client.delete(f'/collections/{collection_id}')
        assert response.status_code == 204
    
    def test_delete_collection_with_prompts_handles_orphans(self, api_client, created_collection, created_prompts):
        """Test deleting a collection also handles orphaned prompts."""
        collection_id = created_collection['id']
        
        # Delete the collection
        response = api_client.delete(f'/collections/{collection_id}')
        assert response.status_code == 204
        
        # Confirm prompts are deleted
        for prompt in created_prompts:
            prompt_response = api_client.get(f'/prompts/{prompt["id"]}')
            assert prompt_response.status_code == 404

    # Error Cases
    def test_delete_nonexistent_collection_returns_404(self, api_client):
        """Test deleting a non-existent collection returns 404."""
        nonexistent_id = "00000000-0000-0000-0000-000000000000"
        response = api_client.delete(f'/collections/{nonexistent_id}')
        assert response.status_code == 404
    
    # Edge Cases
    def test_delete_collection_concurrently(self, api_client, created_collection):
        """Test concurrent deletions of the same collection."""
        collection_id = created_collection['id']
        
        # First deletion attempt should succeed
        response_1 = api_client.delete(f'/collections/{collection_id}')
        assert response_1.status_code == 204
        
        # Second deletion attempt should return 404
        response_2 = api_client.delete(f'/collections/{collection_id}')
        assert response_2.status_code == 404