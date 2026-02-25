import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from app.api import app
from app.storage import storage
from app.models import Prompt

client = TestClient(app)


@pytest.fixture
def setup():
    storage.clear()
    sample_prompt = Prompt(
        id="prompt_1",
        title="Test Prompt",
        content="This is a test content.",
        description="A detailed description of the test prompt.",
        collection_id=None,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    storage.create_prompt(sample_prompt)


# ================= CREATE =================

def test_create_tag(setup):
    response = client.post(
        "/tags",
        json={"name": "TestTag", "created_by": "user_1"},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "TestTag"
    assert data["created_by"] == "user_1"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


# ================= DUPLICATE =================

def test_create_duplicate_tag(setup):
    client.post(
        "/tags",
        json={"name": "TestTag", "created_by": "user_1"},
    )

    response = client.post(
        "/tags",
        json={"name": "TestTag", "created_by": "user_2"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Duplicate tag name"


# ================= ASSIGN =================

def test_assign_tag_to_prompt(setup):
    tag_response = client.post(
        "/tags",
        json={"name": "TestTag", "created_by": "user_1"},
    )

    assert tag_response.status_code == 200
    tag_id = tag_response.json()["id"]

    assign_response = client.post(
        f"/prompts/prompt_1/tags",
        json={"tag_id": tag_id},
    )

    assert assign_response.status_code == 200


# ================= REMOVE =================

def test_remove_tag_from_prompt(setup):
    tag_response = client.post(
        "/tags",
        json={"name": "TestTag", "created_by": "user_1"},
    )

    tag_id = tag_response.json()["id"]

    client.post(
        f"/prompts/prompt_1/tags",
        json={"tag_id": tag_id},
    )

    remove_response = client.delete(
        f"/prompts/prompt_1/tags/{tag_id}",
    )

    assert remove_response.status_code == 200


# ================= UPDATE =================

def test_update_tag_name(setup):
    tag_response = client.post(
        "/tags",
        json={"name": "OldName", "created_by": "user_1"},
    )

    tag_id = tag_response.json()["id"]

    update_response = client.put(
        f"/tags/{tag_id}",
        json={"new_name": "NewName"},
    )

    assert update_response.status_code == 200
    assert update_response.json()["name"] == "NewName"


# ================= GET =================

def test_get_tags(setup):
    client.post("/tags", json={"name": "Tag1", "created_by": "user_1"})
    client.post("/tags", json={"name": "Tag2", "created_by": "user_1"})

    response = client.get("/tags")

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2
    assert any(tag["name"] == "Tag1" for tag in data)
    assert any(tag["name"] == "Tag2" for tag in data)