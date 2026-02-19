"""FastAPI routes for PromptLab"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from app.models import (
    Prompt, PromptCreate, PromptUpdate,
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

@app.get("/health", response_model=HealthResponse)
def health_check():
    """
    Perform a health check on the API.

    Returns:
        HealthResponse: An object containing the health status and API version.

    Example usage:
        `/health`
    """
    return HealthResponse(status="healthy", version=__version__)


# ============== Prompt Endpoints ==============

@app.get("/prompts", response_model=PromptList)
def list_prompts(
    collection_id: Optional[str] = None,
    search: Optional[str] = None
):
    """
    List all prompts with optional filtering by collection and search term.

    Args:
        collection_id (Optional[str]): The ID of the collection to filter prompts.
        search (Optional[str]): A search term to filter prompts by content.

    Returns:
        PromptList: A list of prompts, filtered and sorted as specified.

    Example usage:
        `/prompts?collection_id=123&search=example`
    """
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


@app.get("/prompts/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: str):
    """
    Retrieve a specific prompt by its ID.

    Args:
        prompt_id (str): The unique identifier of the prompt.

    Returns:
        Prompt: The prompt object if found.

    Raises:
        HTTPException: If the prompt is not found.

    Example usage:
        `/prompts/456`
    """
    prompt = storage.get_prompt(prompt_id)
    
    if prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt


@app.post("/prompts", response_model=Prompt, status_code=201)
def create_prompt(prompt_data: PromptCreate):
    """
    Create a new prompt with the provided data.

    Args:
        prompt_data (PromptCreate): The data required to create a new prompt.

    Returns:
        Prompt: The newly created prompt object.

    Raises:
        HTTPException: If the specified collection does not exist.

    Example usage:
        `/prompts` with POST data `{...}`
    """
    # Validate collection exists if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    prompt = Prompt(**prompt_data.model_dump())
    return storage.create_prompt(prompt)


@app.put("/prompts/{prompt_id}", response_model=Prompt)
def update_prompt(prompt_id: str, prompt_data: PromptUpdate):
    """
    Update an existing prompt by ID with new data.

    Args:
        prompt_id (str): The unique identifier of the prompt to update.
        prompt_data (PromptUpdate): The new data to update the prompt with.

    Returns:
        Prompt: The updated prompt object.

    Raises:
        HTTPException: If the prompt or specified collection is not found.

    Example usage:
        `/prompts/456` with PUT data `{...}`
    """
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
        updated_at=get_current_time()  # FIXED: Now refreshes to current time
    )
    
    return storage.update_prompt(prompt_id, updated_prompt)


@app.patch("/prompts/{prompt_id}", response_model=Prompt)
def patch_prompt(prompt_id: str, prompt_data: PromptUpdate):
    """
    Partially update a prompt by ID. Only the fields explicitly provided are modified.

    Args:
        prompt_id (str): The unique identifier of the prompt to update.
        prompt_data (PromptUpdate): The data for updating the prompt; fields not provided
                                      remain unchanged.

    Returns:
        Prompt: The updated prompt object.

    Raises:
        HTTPException: If the prompt or specified collection is not found.

    Example usage:
        `/prompts/456` with PATCH data `{...}`
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Validate collection if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    # Only update fields that were provided (not None)
    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title if prompt_data.title is not None else existing.title,
        content=prompt_data.content if prompt_data.content is not None else existing.content,
        description=prompt_data.description if prompt_data.description is not None else existing.description,
        collection_id=prompt_data.collection_id if prompt_data.collection_id is not None else existing.collection_id,
        created_at=existing.created_at,
        updated_at=get_current_time()  # Always refresh timestamp on update
    )
    
    return storage.update_prompt(prompt_id, updated_prompt)


@app.delete("/prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: str):
    """
    Delete a specific prompt by its ID.

    Args:
        prompt_id (str): The unique identifier of the prompt to delete.

    Raises:
        HTTPException: If the prompt is not found.

    Example usage:
        `/prompts/456`
    """
    if not storage.delete_prompt(prompt_id):
        raise HTTPException(status_code=404, detail="Prompt not found")
    return None


# ============== Collection Endpoints ==============

@app.get("/collections", response_model=CollectionList)
def list_collections():
    """
    List all collections.

    Returns:
        CollectionList: A list of all collections.

    Example usage:
        `/collections`
    """
    collections = storage.get_all_collections()
    return CollectionList(collections=collections, total=len(collections))


@app.get("/collections/{collection_id}", response_model=Collection)
def get_collection(collection_id: str):
    """
    Retrieve a specific collection by its ID.

    Args:
        collection_id (str): The unique identifier of the collection.

    Returns:
        Collection: The collection object if found.

    Raises:
        HTTPException: If the collection is not found.

    Example usage:
        `/collections/123`
    """
    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@app.post("/collections", response_model=Collection, status_code=201)
def create_collection(collection_data: CollectionCreate):
    """
    Create a new collection with the provided data.

    Args:
        collection_data (CollectionCreate): The data required to create a new collection.

    Returns:
        Collection: The newly created collection object.

    Example usage:
        `/collections` with POST data `{...}`
    """
    collection = Collection(**collection_data.model_dump())
    return storage.create_collection(collection)


@app.delete("/collections/{collection_id}", status_code=204)
def delete_collection(collection_id: str):
    """
    Delete a collection by its ID, handling associated prompts.

    Args:
        collection_id (str): The unique identifier of the collection to delete.

    Raises:
        HTTPException: If the collection is not found.

    Example usage:
        `/collections/123`
    """
    if not storage.get_collection(collection_id):
        raise HTTPException(status_code=404, detail="Collection not found")
    
    # Get all prompts and find those belonging to this collection
    all_prompts = storage.get_all_prompts()
    orphaned_prompts = [p for p in all_prompts if p.collection_id == collection_id]
    
    # Update orphaned prompts to remove collection reference
    for prompt in orphaned_prompts:
        prompt.collection_id = None
        storage.update_prompt(prompt.id, prompt)
    
    # Now safe to delete the collection
    storage.delete_collection(collection_id)
    
    return None