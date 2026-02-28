import pytest
from fastapi.testclient import TestClient
from app.api import app
from app.models import CollectionCreate, PromptCreate

client = TestClient(app)

@pytest.fixture
def example_collection():
    collection_data = CollectionCreate(name="Example Collection", description="A collection for testing")
    response = client.post("/collections", json=collection_data.model_dump())
    assert response.status_code == 201
    return response.json()

@pytest.fixture
def example_prompt(example_collection):
    prompt_data = PromptCreate(
        title="Example Prompt",
        content="This is some example content for testing purposes.",
        collection_id=example_collection['id']
    )
    response = client.post("/prompts", json=prompt_data.model_dump())
    assert response.status_code == 201
    created_prompt = response.json()
    return {
        "collection_id": example_collection['id'],
        "prompt_id": created_prompt['id'],
        "updated_content": "This is updated content",
        "changes_summary": "Initial version creation"
    }


def test_create_prompt_version_success(example_prompt):
    response = client.post(
        f"/collections/{example_prompt['collection_id']}/prompts/{example_prompt['prompt_id']}/version",
        json={
            "updated_content": example_prompt["updated_content"],
            "changes_summary": example_prompt["changes_summary"]
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert "version_id" in data
    assert data["prompt_id"] == example_prompt["prompt_id"]
    assert data["collection_id"] == example_prompt["collection_id"]
    assert "version_number" in data
    assert "created_at" in data


def test_create_prompt_version_invalid_ids():
    response = client.post(
        "/collections/invalid_collection/prompts/invalid_prompt/version",
        json={
            "updated_content": "Some content",
            "changes_summary": "Invalid IDs test"
        }
    )
    assert response.status_code == 404


def test_create_prompt_version_no_content_change(example_prompt):
    response = client.post(
        f"/collections/{example_prompt['collection_id']}/prompts/{example_prompt['prompt_id']}/version",
        json={
            "updated_content": "This is some example content for testing purposes.",
            "changes_summary": "No content change"
        }
    )
    assert response.status_code == 400
