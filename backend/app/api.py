"""FastAPI routes for PromptLab"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from app.models import (
    Prompt, PromptCreate, PromptUpdate,
    Collection, CollectionCreate,
    PromptList, CollectionList, HealthResponse,
    Tag, TagCreate, TagUpdate, TagList, TagAssignment,
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
    """Return the current health state of PromptLab.

    Returns:
        HealthResponse signaling overall service health and version.
    """
    return HealthResponse(status="healthy", version=__version__)


# ============== Prompt Endpoints ==============

@app.get("/prompts", response_model=PromptList)
def list_prompts(
    collection_id: Optional[str] = None,
    search: Optional[str] = None,
    tag: Optional[str] = None
):
    """Retrieve prompts with optional filtering, search, and tag criteria.

    Args:
        collection_id: Optional identifier to limit prompts to a collection.
        search: Optional term that filters prompts by title or description.
        tag: Optional tag name used to narrow the results.

    Returns:
        PromptList containing prompts ordered newest-first with metadata.
    """
    prompts = storage.get_all_prompts()
    
    # Filter by collection if specified
    if collection_id:
        prompts = filter_prompts_by_collection(prompts, collection_id)
    
    # Search if query provided
    if search:
        prompts = search_prompts(prompts, search)

    if tag:
        matching_tag = storage.get_tag_by_name(tag)
        if not matching_tag:
            prompts = []
        else:
            prompts = [p for p in prompts if matching_tag.id in p.tags]
    
    # Sort by date (newest first)
    # Note: There might be an issue with the sorting...
    prompts = sort_prompts_by_date(prompts, descending=True)
    
    return PromptList(prompts=prompts, total=len(prompts))


@app.get("/prompts/{prompt_id}", response_model=Prompt)

def get_prompt(prompt_id: str):
    """Fetch a prompt by its unique identifier.

    Args:
        prompt_id: Identifier of the prompt to retrieve.

    Returns:
        Prompt matching the requested identifier.

    Raises:
        HTTPException: If no prompt exists for the supplied id.
    """
    prompt = storage.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt



@app.post("/prompts", response_model=Prompt, status_code=201)
def create_prompt(prompt_data: PromptCreate):
    """Create and persist a new prompt.

    Args:
        prompt_data: Prompt payload used to build the record.

    Returns:
        Newly created Prompt instance with identifiers and timestamps.

    Raises:
        HTTPException: If a provided collection_id does not exist.
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
    """Update a prompt with the provided complete payload.

    Args:
        prompt_id: Identifier of the prompt to modify.
        prompt_data: Data used to replace the prompt's mutable fields.

    Returns:
        Prompt instance reflecting the applied changes.

    Raises:
        HTTPException: If the prompt or any referenced collection is missing.
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Validate collection if provided (allow clearing the relationship)
    if prompt_data.collection_id is not None:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    # Merge payloads so we don't overwrite existing values with None
    prompt_payload = existing.model_dump()
    prompt_payload.update(prompt_data.model_dump(exclude_none=True))
    prompt_payload["updated_at"] = get_current_time()

    updated_prompt = Prompt(**prompt_payload)
    
    return storage.update_prompt(prompt_id, updated_prompt)


@app.patch("/prompts/{prompt_id}", response_model=Prompt)

def patch_prompt(prompt_id: str, prompt_data: PromptUpdate):
    """Apply a partial update to an existing prompt.

    Args:
        prompt_id: Unique identifier of the prompt to patch.
        prompt_data: Payload containing the subset of fields to update.

    Returns:
        The updated Prompt model instance.

    Raises:
        HTTPException: If the prompt is missing or any referenced entity is invalid.
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(
            status_code=404,
            detail=f"Prompt with id '{prompt_id}' was not found."
        )

    patch_payload = prompt_data.model_dump(exclude_unset=True)
    if not patch_payload:
        raise HTTPException(
            status_code=400,
            detail="Provide at least one field to update for a PATCH request."
        )

    if "collection_id" in patch_payload and patch_payload["collection_id"] is not None:
        collection = storage.get_collection(patch_payload["collection_id"])
        if not collection:
            raise HTTPException(
                status_code=400,
                detail=f"Collection '{patch_payload['collection_id']}' could not be located."
            )

    prompt_payload = existing.model_dump()
    prompt_payload.update(patch_payload)
    prompt_payload["updated_at"] = get_current_time()

    updated_prompt = Prompt(**prompt_payload)
    return storage.update_prompt(prompt_id, updated_prompt)




@app.delete("/prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: str):
    """Delete a prompt and return no content.

    Args:
        prompt_id: Identifier of the prompt to remove.

    Raises:
        HTTPException: If the prompt cannot be found.
    """
    if not storage.delete_prompt(prompt_id):
        raise HTTPException(status_code=404, detail="Prompt not found")
    return None


# ============== Collection Endpoints ==============

@app.get("/collections", response_model=CollectionList)
def list_collections():
    """List all collections registered in PromptLab.

    Returns:
        CollectionList containing every stored collection.
    """
    collections = storage.get_all_collections()
    return CollectionList(collections=collections, total=len(collections))


@app.get("/collections/{collection_id}", response_model=Collection)
def get_collection(collection_id: str):
    """Retrieve a collection by identifier.

    Args:
        collection_id: Identifier of the requested collection.

    Returns:
        Collection matching the identifier.

    Raises:
        HTTPException: If no collection exists for the given id.
    """
    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@app.post("/collections", response_model=Collection, status_code=201)
def create_collection(collection_data: CollectionCreate):
    """Create a new collection record.

    Args:
        collection_data: Payload describing the collection to create.

    Returns:
        The newly created Collection instance.
    """
    collection = Collection(**collection_data.model_dump())
    return storage.create_collection(collection)


@app.delete("/collections/{collection_id}", status_code=204)
def delete_collection(collection_id: str):
    """Remove a collection and return no content.

    Args:
        collection_id: Identifier of the collection to remove.

    Raises:
        HTTPException: If the collection cannot be found.
    """
    # BUG #4: We delete the collection but don't handle the prompts!
    # Prompts with this collection_id become orphaned with invalid reference
    # Should either: delete the prompts, set collection_id to None, or prevent deletion
    
    if not storage.delete_collection(collection_id):
        raise HTTPException(status_code=404, detail="Collection not found")
    
    # Missing: Handle prompts that belong to this collection!
    
    return None
