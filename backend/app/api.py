"""FastAPI routes for PromptLab.

This module defines all API endpoints for the PromptLab application,
including routes for managing prompts, collections, and health checks.

The API follows RESTful conventions and includes:
- CRUD operations for prompts
- CRUD operations for collections
- Search and filtering capabilities
- Health check endpoint

All endpoints return appropriate HTTP status codes and error messages.
"""

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
    """Check the health status of the API.
    
    Returns:
        HealthResponse: Contains the API status and version number.
        
    Example:
        >>> GET /health
        {"status": "healthy", "version": "1.0.0"}
    """
    return HealthResponse(status="healthy", version=__version__)


# ============== Prompt Endpoints ==============

@app.get("/prompts", response_model=PromptList)
def list_prompts(
    collection_id: Optional[str] = None,
    search: Optional[str] = None
):
    """List all prompts with optional filtering.
    
    Args:
        collection_id: Optional collection ID to filter prompts by collection.
        search: Optional search query to filter prompts by title or description.
        
    Returns:
        PromptList: List of prompts matching the filters and total count.
        Prompts are sorted by creation date (newest first).
        
    Example:
        >>> GET /prompts?collection_id=abc123&search=email
        {"prompts": [...], "total": 5}
    """
    prompts = storage.get_all_prompts()
    
    # Filter by collection if specified
    if collection_id:
        prompts = filter_prompts_by_collection(prompts, collection_id)
    
    # Search if query provided
    if search:
        prompts = search_prompts(prompts, search)
    
    # Sort by date (newest first)
    prompts = sort_prompts_by_date(prompts, descending=True)
    
    return PromptList(prompts=prompts, total=len(prompts))


@app.get("/prompts/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: str):
    """Get a single prompt by ID.
    
    Args:
        prompt_id: The unique identifier of the prompt.
        
    Returns:
        Prompt: The requested prompt with all its fields.
        
    Raises:
        HTTPException: 404 if the prompt does not exist.
        
    Example:
        >>> GET /prompts/abc123
        {"id": "abc123", "title": "Email Template", ...}
    """
    prompt = storage.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt


@app.post("/prompts", response_model=Prompt, status_code=201)
def create_prompt(prompt_data: PromptCreate):
    """Create a new prompt.
    
    Args:
        prompt_data: The prompt data including title, content, description, 
                    and optional collection_id.
                    
    Returns:
        Prompt: The newly created prompt with generated ID and timestamps.
        
    Raises:
        HTTPException: 400 if the specified collection does not exist.
        
    Example:
        >>> POST /prompts
        {"title": "Email Template", "content": "Hello {{name}}"}
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
    """Update a prompt (full replacement).
    
    This endpoint performs a full update, replacing all fields of the prompt.
    Fields not provided in the request will fall back to existing values.
    The updated_at timestamp is automatically updated.
    
    Args:
        prompt_id: The unique identifier of the prompt to update.
        prompt_data: The updated prompt data.
        
    Returns:
        Prompt: The updated prompt with new updated_at timestamp.
        
    Raises:
        HTTPException: 404 if the prompt does not exist.
        HTTPException: 400 if the specified collection does not exist.
        
    Example:
        >>> PUT /prompts/abc123
        {"title": "Updated Title", "content": "New content"}
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Validate collection if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    # For PUT, replace all fields — fall back to existing values if not provided
    title = prompt_data.title if getattr(prompt_data, 'title', None) is not None else existing.title
    content = prompt_data.content if getattr(prompt_data, 'content', None) is not None else existing.content
    description = prompt_data.description if getattr(prompt_data, 'description', None) is not None else existing.description
    collection_id = prompt_data.collection_id if getattr(prompt_data, 'collection_id', None) is not None else existing.collection_id

    updated_prompt = Prompt(
        id=existing.id,
        title=title,
        content=content,
        description=description,
        collection_id=collection_id,
        created_at=existing.created_at,
        updated_at=get_current_time()
    )

    return storage.update_prompt(prompt_id, updated_prompt)


@app.patch("/prompts/{prompt_id}", response_model=Prompt)
def patch_prompt(prompt_id: str, prompt_data: PromptUpdate):
    """Partially update a prompt.
    
    This endpoint performs a partial update, only modifying the fields
    provided in the request. Unprovided fields retain their existing values.
    The updated_at timestamp is automatically updated.
    
    Args:
        prompt_id: The unique identifier of the prompt to update.
        prompt_data: The partial prompt data with only fields to update.
        
    Returns:
        Prompt: The updated prompt with new updated_at timestamp.
        
    Raises:
        HTTPException: 404 if the prompt does not exist.
        HTTPException: 400 if the specified collection does not exist.
        
    Example:
        >>> PATCH /prompts/abc123
        {"title": "New Title Only"}
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")

    # Validate collection if provided
    if getattr(prompt_data, 'collection_id', None):
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")

    # Only update provided fields
    title = prompt_data.title if getattr(prompt_data, 'title', None) is not None else existing.title
    content = prompt_data.content if getattr(prompt_data, 'content', None) is not None else existing.content
    description = prompt_data.description if getattr(prompt_data, 'description', None) is not None else existing.description
    collection_id = prompt_data.collection_id if getattr(prompt_data, 'collection_id', None) is not None else existing.collection_id

    patched = Prompt(
        id=existing.id,
        title=title,
        content=content,
        description=description,
        collection_id=collection_id,
        created_at=existing.created_at,
        updated_at=get_current_time()
    )

    return storage.update_prompt(prompt_id, patched)


# NOTE: PATCH endpoint is missing! Students need to implement this.
# It should allow partial updates (only update provided fields)


@app.delete("/prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: str):
    """Delete a prompt.
    
    Args:
        prompt_id: The unique identifier of the prompt to delete.
        
    Returns:
        None: Returns 204 No Content on success.
        
    Raises:
        HTTPException: 404 if the prompt does not exist.
        
    Example:
        >>> DELETE /prompts/abc123
        204 No Content
    """
    if not storage.delete_prompt(prompt_id):
        raise HTTPException(status_code=404, detail="Prompt not found")
    return None


# ============== Collection Endpoints ==============

@app.get("/collections", response_model=CollectionList)
def list_collections():
    """List all collections.
    
    Returns:
        CollectionList: List of all collections and total count.
        
    Example:
        >>> GET /collections
        {"collections": [...], "total": 3}
    """
    collections = storage.get_all_collections()
    return CollectionList(collections=collections, total=len(collections))


@app.get("/collections/{collection_id}", response_model=Collection)
def get_collection(collection_id: str):
    """Get a single collection by ID.
    
    Args:
        collection_id: The unique identifier of the collection.
        
    Returns:
        Collection: The requested collection with all its fields.
        
    Raises:
        HTTPException: 404 if the collection does not exist.
        
    Example:
        >>> GET /collections/abc123
        {"id": "abc123", "name": "Marketing", ...}
    """
    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@app.post("/collections", response_model=Collection, status_code=201)
def create_collection(collection_data: CollectionCreate):
    """Create a new collection.
    
    Args:
        collection_data: The collection data including name and optional description.
        
    Returns:
        Collection: The newly created collection with generated ID and timestamp.
        
    Example:
        >>> POST /collections
        {"name": "Marketing", "description": "Marketing prompts"}
    """
    collection = Collection(**collection_data.model_dump())
    return storage.create_collection(collection)


@app.delete("/collections/{collection_id}", status_code=204)
def delete_collection(collection_id: str):
    """Delete a collection.
    
    When a collection is deleted, all prompts that belonged to it have their
    collection_id set to None (orphaned prompts).
    
    Args:
        collection_id: The unique identifier of the collection to delete.
        
    Returns:
        None: Returns 204 No Content on success.
        
    Raises:
        HTTPException: 404 if the collection does not exist.
        
    Example:
        >>> DELETE /collections/abc123
        204 No Content
    """
    if not storage.delete_collection(collection_id):
        raise HTTPException(status_code=404, detail="Collection not found")

    # Prompts that referenced this collection are now orphaned (collection_id set to None)
    return None
