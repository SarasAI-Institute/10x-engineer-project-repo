"""FastAPI routes for PromptLab"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from fastapi import APIRouter, HTTPException
from app.models import TagCreate, Tag
from app.models import AssignTagRequest, UpdateTagRequest
from uuid import UUID

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




router = APIRouter()


# ============== Tag Endpoints ==============

@app.post("/tags", response_model=Tag)
def create_tag(tag: TagCreate):
    if any(t.name.lower() == tag.name.lower() for t in storage.get_tags()):
        raise HTTPException(status_code=400, detail="Duplicate tag name")

    return storage.create_tag(tag.name, tag.created_by)


@app.get("/tags", response_model=list[Tag])
def get_tags():
    return storage.get_tags()




@app.post("/prompts/{prompt_id}/tags")
def assign_tag(prompt_id: str, request: AssignTagRequest):
    try:
        return storage.assign_tag_to_prompt(
            prompt_id,
            UUID(request.tag_id)
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/tags/{tag_id}")
def update_tag(tag_id: str, request: UpdateTagRequest):
    try:
        return storage.update_tag_name(
            UUID(tag_id),
            request.new_name
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/prompts/{prompt_id}/tags/{tag_id}")
def remove_tag(prompt_id: str, tag_id: str):
    try:
        from uuid import UUID
        return storage.remove_tag_from_prompt(prompt_id, UUID(tag_id))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============== Health Check ==============

@app.get("/health", response_model=HealthResponse)
def health_check():
    """Check the health status of the API.

    Returns:
        HealthResponse: An object containing the status and version of the API.

    Example usage:
        >>> health_check()
        HealthResponse(status="healthy", version="1.0.0")
    """
    return HealthResponse(status="healthy", version=__version__)





# ============== Prompt Endpoints ==============

@app.get("/prompts", response_model=PromptList)
def list_prompts(
    collection_id: Optional[str] = None,
    search: Optional[str] = None
):
    """List all prompts, optionally filtered by collection and search query.

    Args:
        collection_id (Optional[str]): Filter prompts by a specific collection ID.
        search (Optional[str]): Search query to filter prompts.

    Returns:
        PromptList: A list of prompts with the total count.

    Example usage:
        >>> list_prompts(collection_id="abc123", search="example")
        PromptList(prompts=[...], total=3)
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
    """Retrieve a specific prompt by its ID.

    Args:
        prompt_id (str): The ID of the prompt to retrieve.

    Returns:
        Prompt: The prompt with the specified ID.

    Raises:
        HTTPException: 404 if prompt not found.

    Example usage:
        >>> get_prompt("prompt1")
        Prompt(id="prompt1", title="Example", ...)
    """
    prompt = storage.get_prompt(prompt_id)

    if prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    return prompt


@app.post("/prompts", response_model=Prompt, status_code=201)
def create_prompt(prompt_data: PromptCreate):
    """Create a new prompt.

    Args:
        prompt_data (PromptCreate): The data for the prompt to be created.

    Returns:
        Prompt: The newly created prompt.

    Raises:
        HTTPException: 400 if collection not found when specified.

    Example usage:
        >>> create_prompt(PromptCreate(title="New Prompt", ...))
        Prompt(id="new_id", title="New Prompt", ...)
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
    """Update an existing prompt by its ID.

    Args:
        prompt_id (str): The ID of the prompt to update.
        prompt_data (PromptUpdate): The updated data for the prompt.

    Returns:
        Prompt: The updated prompt.

    Raises:
        HTTPException: 404 if prompt not found, 400 if collection not found when specified.

    Example usage:
        >>> update_prompt("prompt1", PromptUpdate(title="Updated Title", ...))
        Prompt(id="prompt1", title="Updated Title", ...)
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Validate collection if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    # Update the updated_at timestamp with the current time
    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title,
        content=prompt_data.content,
        description=prompt_data.description,
        collection_id=prompt_data.collection_id,
        created_at=existing.created_at,
        updated_at=get_current_time()  # Updated to current time
    )
    
    return storage.update_prompt(prompt_id, updated_prompt)


@app.patch("/prompts/{prompt_id}", response_model=Prompt)
def patch_prompt(prompt_id: str, prompt_data: PromptUpdate):
    """Partially update a prompt by its ID.

    Args:
        prompt_id (str): The ID of the prompt to update.
        prompt_data (PromptUpdate): The partial data for updating the prompt.

    Returns:
        Prompt: The updated prompt.

    Raises:
        HTTPException: 404 if prompt not found.

    Example usage:
        >>> patch_prompt("prompt1", PromptUpdate(title="New Title"))
        Prompt(id="prompt1", title="New Title", ...)
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")

    # Partial update - only update fields that are provided
    updates = {**existing.model_dump(), **prompt_data.model_dump(exclude_unset=True)}
    updated_prompt = Prompt(**updates, updated_at=get_current_time())

    return storage.update_prompt(prompt_id, updated_prompt)


@app.delete("/prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: str):
    """Delete a prompt by its ID.

    Args:
        prompt_id (str): The ID of the prompt to delete.

    Returns:
        None

    Raises:
        HTTPException: 404 if prompt not found.

    Example usage:
        >>> delete_prompt("prompt1")
    """
    if not storage.delete_prompt(prompt_id):
        raise HTTPException(status_code=404, detail="Prompt not found")
    return None


# ============== Collection Endpoints ==============

@app.get("/collections", response_model=CollectionList)
def list_collections():
    """List all collections.

    Returns:
        CollectionList: A list of all collections and their total count.

    Example usage:
        >>> list_collections()
        CollectionList(collections=[...], total=5)
    """
    collections = storage.get_all_collections()
    return CollectionList(collections=collections, total=len(collections))


@app.get("/collections/{collection_id}", response_model=Collection)
def get_collection(collection_id: str):
    """Retrieve a specific collection by its ID.

    Args:
        collection_id (str): The ID of the collection to retrieve.

    Returns:
        Collection: The collection with the specified ID.

    Raises:
        HTTPException: 404 if collection not found.

    Example usage:
        >>> get_collection("collection1")
        Collection(id="collection1", name="Example Collection", ...)
    """
    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@app.post("/collections", response_model=Collection, status_code=201)
def create_collection(collection_data: CollectionCreate):
    """Create a new collection.

    Args:
        collection_data (CollectionCreate): The data for the collection to be created.

    Returns:
        Collection: The newly created collection.

    Example usage:
        >>> create_collection(CollectionCreate(name="New Collection", ...))
        Collection(id="new_id", name="New Collection", ...)
    """
    collection = Collection(**collection_data.model_dump())
    return storage.create_collection(collection)


@app.delete("/collections/{collection_id}", status_code=204)
def delete_collection(collection_id: str):
    """Delete a collection and orphan its prompts.

    Args:
        collection_id (str): The ID of the collection to delete.

    Returns:
        None

    Raises:
        HTTPException: 404 if collection not found.

    Example usage:
        >>> delete_collection("collection1")
    """
    # Check if collection exists
    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    # Get all prompts in this collection
    all_prompts = storage.get_all_prompts()
    prompts_in_collection = [p for p in all_prompts if p.collection_id == collection_id]
    
    # Set collection_id to None for all prompts in this collection
    for prompt in prompts_in_collection:
        prompt.collection_id = None
        prompt.updated_at = get_current_time()
        storage.update_prompt(prompt.id, prompt)
    
    # Now delete the collection
    storage.delete_collection(collection_id)

