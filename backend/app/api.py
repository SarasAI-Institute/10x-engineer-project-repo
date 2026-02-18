"""FastAPI routes for PromptLab"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from app.models import (
    Prompt, PromptCreate, PromptUpdate,PromptPatch,
    Collection, CollectionCreate,
    PromptList, CollectionList, HealthResponse,
    get_current_time
)
from app.storage import storage
from app.utils import sort_prompts_by_date, filter_prompts_by_collection, search_prompts
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
"""Checks the health status of the API.

This endpoint returns a basic health check status for the API, including
the current version of the application.

Returns:
    HealthResponse: An object containing the health status and application version.

Example:
    >>> health_check()
    HealthResponse(status='healthy', version='1.0.0')
"""
@app.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(status="healthy", version=__version__)


# ============== Prompt Endpoints ==============
""" Retrieve a list of prompts, optionally filtered by collection or search query.

This function retrieves all prompts from storage and applies filters
based on the provided collection ID and search query. The resulting list
is sorted by date in descending order, with the newest prompts first.

Args:
    collection_id (Optional[str]): The ID of the collection to filter prompts.
    search (Optional[str]): A search query to filter prompts by title or content.

Returns:
    PromptList: A list of prompts with the total number of prompts.

Example:
    >>> list_prompts(collection_id="123")
    PromptList(prompts=[Prompt(...), ...], total=1)

    >>> list_prompts(search="example")
    PromptList(prompts=[Prompt(...), ...], total=2)

"""
@app.get("/prompts", response_model=PromptList)
def list_prompts(
    collection_id: Optional[str] = None,
    search: Optional[str] = None
):
    prompts = storage.get_all_prompts()
    
    # Filter by collection if specified
    if collection_id:
        prompts = filter_prompts_by_collection(prompts, collection_id)
    
    # Search if query provided
    if search:
        prompts = search_prompts(prompts, search)
    
    # Sort by date (newest first)
    # Note: There might be an issue with the sorting...
    prompts = sort_prompts_by_date(prompts, descending=True)
    
    return PromptList(prompts=prompts, total=len(prompts))


"""Retrieve a prompt by its unique identifier.

This function fetches a specific prompt from the storage based on the provided
`prompt_id`. If the prompt exists, it returns the prompt details. Otherwise,
it raises a 404 HTTP error indicating that the prompt was not found.

Args:
    prompt_id (str): The unique identifier of the prompt to retrieve.

Returns:
    Prompt: The prompt object if found, otherwise a 404 error is raised.

Raises:
    HTTPException: If the prompt is not found, a 404 error is raised with a
                    "Prompt not found" message.

Example Usage:
    >>> get_prompt("abc123")
    Prompt(id="abc123", title="Example Prompt", content="...", ...)
"""
@app.get("/prompts/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: str):
    # BUG #1: This will raise a 500 error if prompt doesn't exist
    # because we're accessing .id on None
    # Should return 404 instead!
    prompt = storage.get_prompt(prompt_id)
    
    # Check if prompt exists and return it, otherwise raise a 404 error
    if prompt:
        return prompt

    raise HTTPException(status_code=404, detail="Prompt not found")


"""Create a new prompt.

    This function creates a new prompt using the provided data. If a collection ID
    is specified in the prompt data, it verifies the existence of the collection.

    Args:
        prompt_data (PromptCreate): The data for the new prompt, including title, content,
                                    and optional collection ID.

    Returns:
        Prompt: The created prompt object.

    Raises:
        HTTPException: If the specified collection ID does not exist, a 400 error
                       is raised with "Collection not found" message.

    Example Usage:
        >>> create_prompt(prompt_data=PromptCreate(title="New Prompt", content="...", collection_id="123"))
        Prompt(id="xyz789", title="New Prompt", ...)
"""
@app.post("/prompts", response_model=Prompt, status_code=201)
def create_prompt(prompt_data: PromptCreate):
    # Validate collection exists if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    prompt = Prompt(**prompt_data.model_dump())
    return storage.create_prompt(prompt)

"""Update an existing prompt by its unique identifier.

    This function updates the details of an existing prompt specified by `prompt_id`
    using the provided updated data. It also updates the `updated_at` timestamp.

    Args:
        prompt_id (str): The unique identifier of the prompt to update.
        prompt_data (PromptUpdate): The updated data for the prompt.

    Returns:
        Prompt: The updated prompt object.

    Raises:
        HTTPException: If the prompt or collection is not found, 404 or 400
                       errors are raised, respectively.

    Example Usage:
        >>> update_prompt("abc123", prompt_data=PromptUpdate(title="Updated Title"))
        Prompt(id="abc123", title="Updated Title", ...)
"""
@app.put("/prompts/{prompt_id}", response_model=Prompt)
def update_prompt(prompt_id: str, prompt_data: PromptUpdate):
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Validate collection if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    # BUG #2: We're not updating the updated_at timestamp!
    # The updated prompt keeps the old timestamp
    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title,
        content=prompt_data.content,
        description=prompt_data.description,
        collection_id=prompt_data.collection_id,
        created_at=existing.created_at,
        updated_at=get_current_time()  # BUG: Should be get_current_time()
    )
    
    return storage.update_prompt(prompt_id, updated_prompt)


# NOTE: PATCH endpoint is missing! Students need to implement this.
# It should allow partial updates (only update provided fields)
"""Partially update an existing prompt.

    This function applies partial updates to a prompt based on the provided fields.
    It updates only the specified fields and refreshes the `updated_at` timestamp.

    Args:
        prompt_id (str): The unique identifier of the prompt to update.
        prompt_data (PromptPatch): A structure containing fields to update.

    Returns:
        Prompt: The partially updated prompt object.

    Raises:
        HTTPException: If the prompt or collection is not found, 404 or 400
                       errors are raised, respectively.

    Example Usage:
        >>> patch_prompt("abc123", prompt_data=PromptPatch(content="Updated content"))
        Prompt(id="abc123", content="Updated content", ...)
"""
@app.patch("/prompts/{prompt_id}", response_model=Prompt)
def patch_prompt(prompt_id: str, prompt_data: PromptPatch):
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")

    # Validate collection if provided
    if prompt_data.collection_id is not None:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")

    # Apply only provided updates
    updated_prompt = existing.copy(update=prompt_data.dict(exclude_unset=True))

    # Ensure updated_at timestamp is updated
    updated_prompt.updated_at = get_current_time()

    return storage.update_prompt(prompt_id, updated_prompt)

"""Delete a prompt by its unique identifier.

    This function deletes the prompt specified by `prompt_id` from the storage.

    Args:
        prompt_id (str): The unique identifier of the prompt to delete.

    Returns:
        None: If the prompt is successfully deleted, returns HTTP 204 status.

    Raises:
        HTTPException: If the prompt is not found, a 404 error is raised.

    Example Usage:
        >>> delete_prompt("abc123")
        # Returns HTTP 204 No Content
    """
@app.delete("/prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: str):
    if not storage.delete_prompt(prompt_id):
        raise HTTPException(status_code=404, detail="Prompt not found")
    return None


# ============== Collection Endpoints ==============

"""Retrieve all collections.

    This function fetches and returns a list of all collections.

    Returns:
        CollectionList: A list containing all collections and the total count.

    Example Usage:
        >>> list_collections()
        CollectionList(collections=[Collection(id="col123", ...), ...], total=3)
    """
@app.get("/collections", response_model=CollectionList)
def list_collections():
    collections = storage.get_all_collections()
    return CollectionList(collections=collections, total=len(collections))

"""Retrieve a collection by its unique identifier.

    This function fetches a specific collection using the given `collection_id`.

    Args:
        collection_id (str): The unique identifier of the collection to retrieve.

    Returns:
        Collection: The collection object if found, otherwise raises a 404 error.

    Raises:
        HTTPException: If the collection is not found, a 404 error is raised.

    Example Usage:
        >>> get_collection("col123")
        Collection(id="col123", name="Example Collection", ...)
    """
@app.get("/collections/{collection_id}", response_model=Collection)
def get_collection(collection_id: str):
    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection

"""Create a new collection.

    This function creates a new collection using the provided data.

    Args:
        collection_data (CollectionCreate): The data required to create a collection.

    Returns:
        Collection: The created collection object.

    Example Usage:
        >>> create_collection(collection_data=CollectionCreate(name="New Collection"))
        Collection(id="col456", name="New Collection", ...)
    """
@app.post("/collections", response_model=Collection, status_code=201)
def create_collection(collection_data: CollectionCreate):
    collection = Collection(**collection_data.model_dump())
    return storage.create_collection(collection)

"""Delete a collection by its unique identifier.

    This function deletes a specific collection and handles associated prompts,
    reassigning them if necessary.

    Args:
        collection_id (str): The unique identifier of the collection to delete.

    Returns:
        None: If the collection is successfully deleted, returns HTTP 204 status.

    Raises:
        HTTPException: If the collection is not found, a 404 error is given.

    Example Usage:
        >>> delete_collection("col123")
        # Returns HTTP 204 No Content
    """
@app.delete("/collections/{collection_id}", status_code=204)
def delete_collection(collection_id: str):
    # BUG #4: We delete the collection but don't handle the prompts!
    # Prompts with this collection_id become orphaned with invalid reference
    # Should either: delete the prompts, set collection_id to None, or prevent deletion
    
    if not storage.delete_collection(collection_id):
        raise HTTPException(status_code=404, detail="Collection not found")
    
    # BUG #4: FIXED - Now handle prompts that belong to this collection
    # We'll set their collection_id to None
    # Ensure there is a default 'Uncategorized' collection
    uncategorized_collection = storage.get_or_create_default_collection()
    
    # Reassign prompts to the 'Uncategorized' collection
    prompts = storage.get_all_prompts()
    for prompt in prompts:
        if prompt.collection_id == collection_id:
            new_prompt_data = prompt.model_dump()
            new_prompt_data["collection_id"] = uncategorized_collection.id
            new_prompt_data["updated_at"] = get_current_time()
            storage.update_prompt(prompt.id, Prompt(**new_prompt_data))
    
    return None