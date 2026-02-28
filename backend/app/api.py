"""FastAPI routes for PromptLab"""

from fastapi import FastAPI, HTTPException, status, Path, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Dict, List
import re
from datetime import datetime
import uuid

from app.models import (
    Prompt, PromptCreate, PromptUpdate, PromptPatch,
    Collection, CollectionCreate,
    PromptList, CollectionList, HealthResponse,
    VersionRequest,
    get_current_time
)
from app.storage import storage
from app.utils import sort_prompts_by_date, filter_prompts_by_collection, search_prompts, apply_partial_updates, validate_prompt_id
from app import __version__


app = FastAPI(
    title="PromptLab API",
    description="AI Prompt Engineering Platform",
    version=__version__
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Health Check ==============

@app.get("/health", response_model=HealthResponse)
def health_check():
    """Checks the health status of the API and returns it.

    This endpoint is used to determine if the API is running and healthy.
    It returns the health status along with the version of the currently 
    running application.

    Returns:
        HealthResponse: An object containing the health status and the 
        version of the API.

    Example:
        >>> response = health_check()
        >>> print(response.status)
        "healthy"
        >>> print(response.version)
        "1.0.0"  # or whatever the current version is
    """
    return HealthResponse(status="healthy", version=__version__)


# ============== Prompt Endpoints ==============

@app.get("/prompts", response_model=PromptList)
def list_prompts(
    collection_id: Optional[str] = None,
    search: Optional[str] = None
):
    """Retrieve a list of prompts, optionally filtered by collection or search query.

    This endpoint fetches all available prompts and provides options to filter them
    by a specific collection or search query. The results are sorted by date in
    descending order, presenting the newest prompts first.

    Args:
        collection_id (Optional[str]): An optional ID of the collection to filter the prompts.
        search (Optional[str]): An optional search query to filter prompts by matching text.

    Returns:
        PromptList: An object containing the list of prompts and the total count of prompts.

    Usage Examples:
        To retrieve all prompts:
        >>> list_prompts()

        To retrieve prompts from a specific collection:
        >>> list_prompts(collection_id='collection123')

        To search prompts with a query:
        >>> list_prompts(search='example query')
    """
    prompts = storage.get_all_prompts()
    
    # Filter by collection if specified
    if collection_id:
        collection = storage.get_collection(collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
        prompts = filter_prompts_by_collection(prompts, collection_id)
    
    # Search if query provided
    if search:
        prompts = search_prompts(prompts, search)
    
    # Sort by date (newest first)
    prompts = sort_prompts_by_date(prompts, descending=True)
    
    return PromptList(prompts=prompts, total=len(prompts))


@app.get("/prompts/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: str):
    """Retrieve a prompt by its ID.

    This function looks up a prompt in the storage system using the provided
    prompt ID. If the prompt is found, it is returned. If no prompt is found
    with the given ID, an HTTPException is raised with a 404 status code.

    Args:
        prompt_id (str): The unique identifier for the prompt.

    Returns:
        Prompt: An instance of the `Prompt` model corresponding to the given ID.

    Raises:
        HTTPException: If no prompt is found with the given ID, with a 404 status code.

    Usage Example:
        >>> prompt = get_prompt("example_prompt_id")
        >>> print(prompt.title)
    """
    # Validate prompt ID format using the utility function
    is_valid, error_message = validate_prompt_id(prompt_id)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_message)
    
    # Retrieve the prompt using the provided ID
    prompt = storage.get_prompt(prompt_id)

    # Check if the prompt exists; if not, raise a 404 error
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    # Return the found prompt
    return prompt
    

@app.post("/prompts", response_model=Prompt, status_code=201)
def create_prompt(prompt_data: PromptCreate):
    """Create a new prompt entry in the database.

    This endpoint receives data for a new prompt and stores it in the database.
    If a `collection_id` is specified in the prompt data, it validates that
    the corresponding collection exists. If no collection is found, it raises
    an HTTP exception.

    Args:
        prompt_data (PromptCreate): The data required to create a new prompt,
        encapsulated in a `PromptCreate` model.

    Returns:
        Prompt: The newly created prompt record encapsulated in a `Prompt` model.

    Raises:
        HTTPException: If `collection_id` is specified and the collection is
        not found in the storage, a 400 status code is raised.

    Examples:
        Create a prompt without validation of collection:

        >>> new_prompt = PromptCreate(
        ...     text="What is the capital of France?",
        ...     collection_id=None
        ... )
        >>> created_prompt = create_prompt(new_prompt)

        Create a prompt with validation of existing collection:

        >>> new_prompt = PromptCreate(
        ...     text="What is the capital of Germany?",
        ...     collection_id=1
        ... )
        >>> created_prompt = create_prompt(new_prompt)
    """
    # Validate collection exists if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    # Check for duplicate title
    existing_prompt = storage.get_prompt_by_title(prompt_data.title, prompt_data.collection_id)
    if existing_prompt:
        raise HTTPException(status_code=409, detail="Prompt with this title already exists")
    
    prompt = Prompt(**prompt_data.model_dump())
    return storage.create_prompt(prompt)


@app.put("/prompts/{prompt_id}", response_model=Prompt)
def update_prompt(prompt_id: str, prompt_data: PromptUpdate):
    """Updates an existing prompt with new data.

    This function retrieves an existing prompt by its ID and updates it with the new data provided. If the prompt or collection does not exist, appropriate HTTP exceptions are raised.

    Args:
        prompt_id (str): The unique identifier of the prompt to be updated.
        prompt_data (PromptUpdate): The new data for the prompt, encapsulated in a `PromptUpdate` model.

    Returns:
        Prompt: The updated prompt object.

    Raises:
        HTTPException: If the prompt with the given ID is not found, a 404 status code is returned.
        HTTPException: If the specified collection ID is not found, a 400 status code is returned.

    Usage Example:
        >>> update_prompt("1234", prompt_data)
        Returns the updated prompt object if successful.
    """
    # Validate prompt ID format using the utility function
    is_valid, error_message = validate_prompt_id(prompt_id)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_message)
    
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Validate collection if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title,
        content=prompt_data.content,
        description=prompt_data.description,
        collection_id=prompt_data.collection_id,
        created_at=existing.created_at,
        updated_at=get_current_time()  # Corrected to use current time
    )
    
    return storage.update_prompt(prompt_id, updated_prompt)


# It should allow partial updates (only update provided fields)
@app.patch("/prompts/{prompt_id}", response_model=Prompt)
def patch_prompt(prompt_id: str, prompt_data: PromptPatch):
    """Partially updates the fields of an existing prompt.

    This function allows updating only the specified fields of a prompt without affecting
    other fields. If the prompt with the given ID does not exist, a 404 HTTP exception is raised.

    Args:
        prompt_id (str): The unique identifier of the prompt to update.
        prompt_data (PromptUpdate): An object containing the fields and their new values
            that need to be updated on the prompt.

    Returns:
        Prompt: The updated prompt object with the newly applied changes.

    Raises:
        HTTPException: If no prompt with the specified ID is found, raises a 404 error.

    Example:
        >>> from fastapi.testclient import TestClient
        >>> client = TestClient(app)
        >>> prompt_id = "12345"
        >>> update_data = {"title": "New Title"}
        >>> response = client.patch(f"/prompts/{prompt_id}", json=update_data)
        >>> assert response.status_code == 200
        >>> assert response.json()["title"] == "New Title"
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Utilize utility to apply partial updates
    updated_prompt = apply_partial_updates(existing, prompt_data)
    return storage.update_prompt(prompt_id, updated_prompt)

@app.delete("/prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: str):
    """Deletes a prompt from the storage by its ID.

    Args:
        prompt_id (str): The unique identifier of the prompt to be deleted.

    Returns:
        None: Returns `None` upon successful deletion of the prompt.

    Raises:
        HTTPException: Raises a 404 HTTP exception if the prompt with the specified ID is not found.

    Example:
        To delete a prompt with a specific ID, you can call:

        >>> delete_prompt("example_prompt_id")
    """
    
    # Validate prompt ID format using the utility function
    is_valid, error_message = validate_prompt_id(prompt_id)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_message)
    
    if not storage.delete_prompt(prompt_id):
        raise HTTPException(status_code=404, detail="Prompt not found")
    return None


# ============== Collection Endpoints ==============
@app.get("/collections", response_model=CollectionList)
def list_collections():
    """Retrieve and return a list of all collections.

    This endpoint fetches all available collections from the storage and returns
    them as a response model `CollectionList` which includes the collections
    themselves and the total count of collections.

    Returns:
        CollectionList: An object containing the list of collections and the total number
        of collections.

    Example:
        To retrieve all collections, you can make a GET request to the `/collections`
        endpoint. This will return a JSON response with the list of collections and
        their total count.

    """
    collections = storage.get_all_collections()
    return CollectionList(collections=collections, total=len(collections))


@app.get("/collections/{collection_id}", response_model=Collection)
def get_collection(collection_id: str):
    """Retrieve a collection by its ID.

    This endpoint retrieves a specific collection from the storage based on the provided
    collection ID. If the collection does not exist, it raises a 404 HTTP exception.

    Args:
        collection_id (str): The unique identifier of the collection to retrieve.

    Returns:
        Collection: The collection object corresponding to the provided collection ID.

    Raises:
        HTTPException: If the collection is not found, a 404 error is raised with the message
        "Collection not found".

    Usage Example:
        collection = get_collection("12345")
        print(collection.name)
    """
    print("---------------------- Collection ID ------------" + collection_id)
    if not collection_id or collection_id.strip() == '':
        raise HTTPException(status_code=422, detail="Collection ID is empty")
    
    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection
    

@app.post("/collections", response_model=Collection, status_code=201)
def create_collection(collection_data: CollectionCreate):
    """Create a new collection.

    This endpoint allows the creation of a new collection using the data provided in
    the `CollectionCreate` model. The created collection is stored and returned.

    Args:
        collection_data (CollectionCreate): The data model containing the necessary
            information to create a new collection.

    Returns:
        Collection: The created collection object with all its attributes filled.

    Usage Example:
        >>> from backend.app.models import CollectionCreate
        >>> new_collection_data = CollectionCreate(name="My Collection", description="A sample collection")
        >>> created_collection = create_collection(new_collection_data)
        >>> print(created_collection.id)  # Outputs the ID of the created collection
    """
    # Validate collection name.
    if not collection_data.name or collection_data.name.strip() == '' or not re.match(r'^[\w\s\-\&]+$', collection_data.name) or len(collection_data.name) > 255:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid collection name '{collection_data.name}'. Only alphanumeric characters, spaces, '-', and '&' are allowed."
        )
    
    # Check for duplicate collection name.
    if storage.collection_exists_by_name(collection_data.name):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Collection '{collection_data.name}' already exists"
        )
    
    collection = Collection(**collection_data.model_dump())
    return storage.create_collection(collection)


@app.delete("/collections/{collection_id}", status_code=204)
def delete_collection(collection_id: str):
    """Delete a collection and optionally handle orphaned prompts.

    This endpoint deletes the specified collection from storage.
    If the deletion is unsuccessful because the collection does not exist, a 404
    HTTPException is raised. Additionally, it handles orphaned prompts by deleting them.

    Args:
        collection_id (str): The unique identifier of the collection to be deleted.

    Returns:
        None: The function does not return a value as it raises an HTTPException
        if the collection is not found and the deletion was unsuccessful.

    Raises:
        HTTPException: If the collection with the specified `collection_id` does
        not exist, a 404 status code is returned.

    Example usage:
        - Delete a collection with its collection ID:
            The client sends a DELETE request to the endpoint, replacing
            `{collection_id}` with the actual ID of the existing collection:
            DELETE /collections/12345

        - Handling the response:
            On successful deletion, the API responds with a 204 No Content status.
            If the requested collection does not exist, a 404 Not Found error is
            returned in the response.
    """
    if not storage.delete_collection(collection_id):
        raise HTTPException(status_code=404, detail="Collection not found")
    
    # Handle orphaned prompts
    prompts = storage.get_prompts_by_collection(collection_id)
    for prompt in prompts:
        # Option 1: Delete the prompts
        storage.delete_prompt(prompt.id)
    return None

# Assume 'storage' is your storage instance and has methods to interact with the database



@app.post("/collections/{collection_id}/prompts/{prompt_id}/version", response_model=Dict[str, str], status_code=201)
def create_prompt_version(collection_id: str, prompt_id: str, version_data: VersionRequest):
    """Create a new version of a prompt with updated content and change summary."""
    # Retrieve the collection and prompt
    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    existing_prompt = storage.get_prompt_by_id_and_collection(prompt_id, collection_id)
    if not existing_prompt:
        raise HTTPException(status_code=404, detail="Prompt not found in the specified collection")
    
    # Ensure there's an actual change in content
    if existing_prompt.content.strip() == version_data.updated_content.strip():
        raise HTTPException(status_code=400, detail="No actual content change")

    # Create a new version ID
    version_id = str(uuid.uuid4())
    version_timestamp = datetime.utcnow()
    
    # Construct the new version data
    new_version = {
        "version_id": version_id,
        "prompt_id": prompt_id,
        "collection_id": collection_id,
        "version_number": str(len(storage.get_versions_by_prompt(prompt_id)) + 1),
        "created_at": version_timestamp.isoformat(),
        "content": version_data.updated_content,
        "changes_summary": version_data.changes_summary
    }

    # Simulating a storage mechanism for storing a new version
    storage.save_prompt_version(prompt_id, new_version)
    
    return {
        "version_id": version_id,
        "prompt_id": prompt_id,
        "collection_id": collection_id,
        "version_number": new_version["version_number"],
        "created_at": new_version["created_at"]
    }


@app.get("/collections/{collection_id}/prompts/{prompt_id}/versions", response_model=List[Dict[str, str]])
async def get_prompt_versions(collection_id: str, prompt_id: str) -> List[Dict[str, str]]:
    """Retrieve all versions of a given prompt."""
    prompt = storage.get_prompt_by_id_and_collection(prompt_id, collection_id)
    if not prompt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prompt not found")

    versions = storage.get_versions_by_prompt(prompt_id)
    return versions

# ============== Revert Prompt Version Endpoint ==============

@app.post("/collections/{collection_id}/prompts/{prompt_id}/revert", response_model=Dict[str, str])
def revert_to_prompt_version(collection_id: str, prompt_id: str, version_request: Dict[str, str]):
    """Reverts a prompt to a specific previous version, given the version ID."""
    # Validate the request input for 'target_version_id'.
    target_version_id = version_request.get("target_version_id")
    if not target_version_id:
        raise HTTPException(status_code=422, detail="Missing version ID")

    # Retrieve the collection and ensure it exists
    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")

    # Retrieve the prompt and ensure it belongs to the collection
    prompt = storage.get_prompt_by_id_and_collection(prompt_id, collection_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")

    # Retrieve the target version
    target_version = next((version for version in storage.get_versions_by_prompt(prompt_id) 
                           if version["version_id"] == target_version_id), None)
    if not target_version:
        raise HTTPException(status_code=404, detail="Version not found")

    # Ensure reversion only if there's an actual difference
    if prompt.content.strip() != target_version["content"].strip():
        # Update the prompt to the target version's content
        prompt.content = target_version["content"]

        # Create a new version entry post-reversion
        version_id = str(uuid.uuid4())
        version_number = len(storage.get_versions_by_prompt(prompt_id)) + 1
        storage.save_prompt_version(prompt_id, {
            "version_id": version_id,
            "prompt_id": prompt_id,
            "collection_id": collection_id,
            "version_number": version_number,
            "created_at": datetime.utcnow().isoformat(),
            "content": prompt.content,
            "changes_summary": f"Reverted to version {target_version['version_id']}"
        })
        
        return {
            "version_id": version_id,
            "prompt_id": prompt_id,
            "collection_id": collection_id,
            "version_number": version_number,
            "created_at": datetime.utcnow().isoformat()
        }

    return {"detail": "Target version is the current version; no changes made."}




@app.post("/collections/{collection_id}/prompts/{prompt_id}/revert", response_model=Dict[str, str])
def revert_to_prompt_version(collection_id: str, prompt_id: str, version_request: Dict[str, str]):
    """Reverts a prompt to a specific previous version, given the version ID."""
    # Validate the request input for 'target_version_id'.
    target_version_id = version_request.get("target_version_id")
    if not target_version_id:
        raise HTTPException(status_code=422, detail="Missing version ID")

    # Retrieve the collection and ensure it exists
    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")

    # Retrieve the prompt and ensure it belongs to the collection
    prompt = storage.get_prompt_by_id_and_collection(prompt_id, collection_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")

    # Retrieve the target version
    target_version = next((version for version in storage.get_versions_by_prompt(prompt_id) 
                           if version["version_id"] == target_version_id), None)
    if not target_version:
        raise HTTPException(status_code=404, detail="Version not found")

    # Ensure reversion only if there's an actual difference
    if prompt.content.strip() != target_version["content"].strip():
        # Update the prompt to the target version's content
        prompt.content = target_version["content"]

        # Create a new version entry post-reversion
        version_id = str(uuid.uuid4())
        version_number = len(storage.get_versions_by_prompt(prompt_id)) + 1
        storage.save_prompt_version(prompt_id, {
            "version_id": version_id,
            "prompt_id": prompt_id,
            "collection_id": collection_id,
            "version_number": version_number,
            "created_at": datetime.utcnow().isoformat(),
            "content": prompt.content,
            "changes_summary": f"Reverted to version {target_version['version_id']}"
        })

        return {
            "version_id": version_id,
            "prompt_id": prompt_id,
            "collection_id": collection_id,
            "version_number": version_number,
            "created_at": datetime.utcnow().isoformat()
        }
    else:
        return HTTPException(status_code=200, detail="Target version is the current version; no changes made.")




