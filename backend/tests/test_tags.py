import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from app.api import app
from app.storage import storage
from app.models import Prompt

client = TestClient(app)


@pytest.fixture
def setup():
    """Fixture to set up the test environment with a sample prompt.

    This fixture is used to initialize the test storage environment by clearing any existing data,
    and then creating a sample prompt with predefined attributes for use in tests.

    Args:
        None

    Returns:
        None

    Example usage:
        Use this fixture in test functions to ensure a clean initial state:

        def test_example(setup):
            # ... perform test actions ...
    """
    # Clear existing storage data
    storage.clear()

    # Create a sample prompt with predefined attributes
    sample_prompt = Prompt(
        id="prompt_1",
        title="Test Prompt",
        content="This is a test content.",
        description="A detailed description of the test prompt.",
        collection_id=None,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    # Add the sample prompt to storage
    storage.create_prompt(sample_prompt)


# ================= CREATE =================

def test_create_tag(setup):
    """Test the creation of a new tag via the API.

    This test verifies that a tag can be successfully created using the FastAPI client.
    It checks the response status code and validates that the returned JSON includes the correct tag details.

    Args:
        setup: A pytest fixture that sets up the test environment, clearing storage and creating a sample prompt.

    Returns:
        None

    Example usage:
        This function is used as a test case and does not require direct invocation.
        It runs automatically when executing tests with pytest:

        pytest backend/tests/test_tags.py::test_create_tag
    """
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
    """Test the API's handling of attempting to create a duplicate tag.

    This test checks that the API correctly identifies and rejects an attempt to create a tag with a name that already exists,
    ensuring that duplicate tags are not allowed. It validates that the response status code is 400 and the appropriate error message is returned.

    Args:
        setup: A pytest fixture that sets up the test environment, clearing storage and creating a sample prompt.

    Returns:
        None

    Example usage:
        This function is used as a test case and does not require direct invocation.
        It runs automatically when executing tests with pytest:

        pytest backend/tests/test_tags.py::test_create_duplicate_tag
    """
    client.post(
        "/tags",
        json={"name": "TestTag", "created_by": "user_1"},
    )

    response = client.post(
        "/tags",
        json={"name": "TestTag", "created_by": "user_2"},
    )

    # Assert to ensure the response status code is 400
    assert response.status_code == 400

    # Assert to check that the correct error message is returned
    assert response.json()["detail"] == "Duplicate tag name"


# ================= ASSIGN =================

def test_assign_tag_to_prompt(setup):
    """Test assigning a tag to a prompt using the API.

    This test verifies that a tag can be successfully assigned to a prompt, ensuring that the tag association is correctly handled by the API.
    It first creates a tag, checks for successful creation, and then assigns the tag to a predefined prompt, verifying the assignment is successful.

    Args:
        setup: A pytest fixture that sets up the test environment by clearing existing storage and creating a sample prompt.

    Returns:
        None

    Example usage:
        This function is intended for use as a test case and is not directly invoked.
        It runs automatically when executing tests with pytest:

        pytest backend/tests/test_tags.py::test_assign_tag_to_prompt
    """
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
    """Test removing a tag from a prompt via the API.

    This test checks the API's ability to successfully remove a previously assigned tag from a prompt.
    It involves creating a tag, assigning it to a prompt, and then using the API to remove the tag, verifying the removal is successful with an appropriate status code.

    Args:
        setup: A pytest fixture that prepares the test environment by clearing storage and setting up a sample prompt.

    Returns:
        None

    Example usage:
        This function is used as a test case and should not be directly invoked.
        It runs automatically when executing tests with pytest:

        pytest backend/tests/test_tags.py::test_remove_tag_from_prompt
    """
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
    """Test updating the name of an existing tag via the API.

    This test verifies that a tag's name can be successfully updated using the API.
    It involves creating a tag, updating its name, and asserting that the API reflects the updated name and returns a successful status code.

    Args:
        setup: A pytest fixture that sets up the test environment by clearing storage and initializing a sample prompt.

    Returns:
        None

    Example usage:
        This function is intended to be used as a test case and is not directly called.
        It runs automatically when executing tests with pytest:

        pytest backend/tests/test_tags.py::test_update_tag_name
    """
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
    """Test retrieving all tags via the API.

    This test ensures that all tags can be successfully retrieved using the API.
    It involves creating multiple tags and asserting that they can be fetched and correctly listed, with the response containing the appropriate number of tags and their correct names.

    Args:
        setup: A pytest fixture that prepares the environment by clearing existing data and creating a sample prompt.

    Returns:
        None

    Example usage:
        This function acts as a test case and is not meant for direct invocation.
        It runs automatically during test execution with pytest:

        pytest backend/tests/test_tags.py::test_get_tags
    """
    client.post("/tags", json={"name": "Tag1", "created_by": "user_1"})
    client.post("/tags", json={"name": "Tag2", "created_by": "user_1"})

    response = client.get("/tags")

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2
    assert any(tag["name"] == "Tag1" for tag in data)
    assert any(tag["name"] == "Tag2" for tag in data)