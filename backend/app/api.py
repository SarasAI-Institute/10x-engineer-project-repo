"""FastAPI routes for PromptLab"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from app.models import (
    Prompt, PromptCreate, PromptUpdate,
    PromptPatch,
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
    """Health check endpoint.

    Returns the current status of the API and the running version. This can be
    used by load-balancers and uptime checks.

    Returns:
        HealthResponse: Object with `status` (string) and `version` (string).
    """
    return HealthResponse(status="healthy", version=__version__)


# ============== Prompt Endpoints ==============

@app.get("/prompts", response_model=PromptList)
def list_prompts(
    collection_id: Optional[str] = None,
    search: Optional[str] = None
):
    """List prompts with optional filtering and search.

    Args:
        collection_id: If provided, only prompts belonging to this collection
            will be returned.
        search: Optional full-text query to search prompt titles and
            descriptions.

    Returns:
        PromptList: A list container with prompts and the total count.
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
    """Retrieve a single prompt by ID.

    Args:
        prompt_id: Unique identifier of the prompt.

    Raises:
        HTTPException: 404 if the prompt does not exist.

    Returns:
        Prompt: The requested prompt.
    """
    # Return 404 if prompt does not exist (fix for Bug #1)
    prompt = storage.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt


@app.post("/prompts", response_model=Prompt, status_code=201)
def create_prompt(prompt_data: PromptCreate):
    """Create a new prompt.

    Validates that a referenced `collection_id` exists (if provided). Returns
    the created prompt with its assigned ID and timestamps.

    Args:
        prompt_data: Incoming data required to create a Prompt.

    Raises:
        HTTPException: 400 if the provided `collection_id` does not exist.

    Returns:
        Prompt: The newly created prompt.
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
    """Replace an existing prompt with new values.

    This is a full replace (PUT semantics). The endpoint validates the prompt
    exists and the referenced collection (if any), then sets `updated_at` to
    the current time.

    Args:
        prompt_id: ID of the prompt to update.
        prompt_data: Payload with the new prompt values.

    Raises:
        HTTPException: 404 if the prompt does not exist.
        HTTPException: 400 if the provided `collection_id` does not exist.

    Returns:
        Prompt: The updated prompt.
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")

    # Validate collection if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")

    # Create updated prompt with new timestamp
    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title,
        content=prompt_data.content,
        description=prompt_data.description,
        collection_id=prompt_data.collection_id,
        created_at=existing.created_at,
        updated_at=get_current_time()
    )

    return storage.update_prompt(prompt_id, updated_prompt)


@app.patch("/prompts/{prompt_id}", response_model=Prompt)
def patch_prompt(prompt_id: str, prompt_data: PromptPatch):
    """Partially update a prompt.

    Only fields present in `prompt_data` are changed; all other fields are
    preserved. The `updated_at` timestamp is set to the current time.

    Args:
        prompt_id: ID of the prompt to patch.
        prompt_data: Partial prompt payload where each field is optional.

    Raises:
        HTTPException: 404 if the prompt does not exist.
        HTTPException: 400 if the provided `collection_id` does not exist.

    Returns:
        Prompt: The updated prompt.
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")

    # Validate collection if provided
    if prompt_data.collection_id is not None:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")

    # Build new prompt by merging existing values with provided ones
    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title if prompt_data.title is not None else existing.title,
        content=prompt_data.content if prompt_data.content is not None else existing.content,
        description=(prompt_data.description if prompt_data.description is not None else existing.description),
        collection_id=(prompt_data.collection_id if prompt_data.collection_id is not None else existing.collection_id),
        created_at=existing.created_at,
        updated_at=get_current_time()
    )

    return storage.update_prompt(prompt_id, updated_prompt)


# NOTE: PATCH endpoint is missing! Students need to implement this.
# It should allow partial updates (only update provided fields)


@app.delete("/prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: str):
    """Delete a prompt by ID.

    Args:
        prompt_id: ID of the prompt to remove.

    Raises:
        HTTPException: 404 if the prompt does not exist.

    Returns:
        None: On successful deletion the endpoint returns HTTP 204 with no body.
    """
    if not storage.delete_prompt(prompt_id):
        raise HTTPException(status_code=404, detail="Prompt not found")
    return None


# ============== Collection Endpoints ==============

@app.get("/collections", response_model=CollectionList)
def list_collections():
    """Return all collections.

    Returns a `CollectionList` containing all known collections and a total
    count.
    """
    collections = storage.get_all_collections()
    return CollectionList(collections=collections, total=len(collections))


@app.get("/collections/{collection_id}", response_model=Collection)
def get_collection(collection_id: str):
    """Retrieve a collection by ID.

    Args:
        collection_id: Identifier of the collection.

    Raises:
        HTTPException: 404 if the collection does not exist.

    Returns:
        Collection: The requested collection object.
    """
    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@app.post("/collections", response_model=Collection, status_code=201)
def create_collection(collection_data: CollectionCreate):
    """Create a new collection.

    Args:
        collection_data: Payload describing the new collection.

    Returns:
        Collection: The created collection object.
    """
    collection = Collection(**collection_data.model_dump())
    return storage.create_collection(collection)


@app.delete("/collections/{collection_id}", status_code=204)
def delete_collection(collection_id: str):
    """Delete a collection and nullify references on prompts.

    When a collection is removed we preserve any prompts that referenced it by
    setting their `collection_id` to None and updating their `updated_at`.

    Args:
        collection_id: ID of the collection to delete.

    Raises:
        HTTPException: 404 if the collection does not exist.

    Returns:
        None: On success the endpoint returns HTTP 204 with no body.
    """
    if not storage.delete_collection(collection_id):
        raise HTTPException(status_code=404, detail="Collection not found")
    # Handle prompts that belong to this collection by nullifying their collection_id
    # This preserves the prompt data while removing the invalid reference.
    prompts = storage.get_prompts_by_collection(collection_id)
    for p in prompts:
        updated = Prompt(
            id=p.id,
            title=p.title,
            content=p.content,
            description=p.description,
            collection_id=None,
            created_at=p.created_at,
            updated_at=get_current_time()
        )
        storage.update_prompt(updated.id, updated)

    return None
