"""FastAPI routes for PromptLab"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from app.models import (
    Prompt, PromptCreate, PromptUpdate,
    Collection, CollectionCreate,
    PromptList, CollectionList, HealthResponse,
    TagList, TagAdd,
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
    return HealthResponse(status="healthy", version=__version__)


# ============== Prompt Endpoints ==============

@app.get("/prompts", response_model=PromptList)
def list_prompts(
    collection_id: Optional[str] = None,
    search: Optional[str] = None,
    tag: Optional[str] = None
):
    prompts = storage.get_all_prompts()
    
    # Filter by collection if specified
    if collection_id:
        prompts = filter_prompts_by_collection(prompts, collection_id)
    
    # Search if query provided
    if search:
        prompts = search_prompts(prompts, search)
    
    # Filter by tag if specified
    if tag:
        prompts = [p for p in prompts if tag.lower() in p.tags]
    
    # Sort by date (newest first)
    # Note: There might be an issue with the sorting...
    prompts = sort_prompts_by_date(prompts, descending=True)
    
    return PromptList(prompts=prompts, total=len(prompts))


@app.get("/prompts/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: str):
    prompt = storage.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt


@app.post("/prompts", response_model=Prompt, status_code=201)
def create_prompt(prompt_data: PromptCreate):
    # Validate collection exists if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    # Normalize tags to lowercase
    prompt_dict = prompt_data.model_dump()
    prompt_dict['tags'] = [tag.lower() for tag in prompt_dict.get('tags', [])]
    
    prompt = Prompt(**prompt_dict)
    return storage.create_prompt(prompt)


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
    # For PUT, replace all fields — fall back to existing values if not provided
    title = prompt_data.title if getattr(prompt_data, 'title', None) is not None else existing.title
    content = prompt_data.content if getattr(prompt_data, 'content', None) is not None else existing.content
    description = prompt_data.description if getattr(prompt_data, 'description', None) is not None else existing.description
    collection_id = prompt_data.collection_id if getattr(prompt_data, 'collection_id', None) is not None else existing.collection_id
    tags = prompt_data.tags if getattr(prompt_data, 'tags', None) is not None else existing.tags
    # Normalize tags to lowercase
    if tags:
        tags = [tag.lower() for tag in tags]

    updated_prompt = Prompt(
        id=existing.id,
        title=title,
        content=content,
        description=description,
        collection_id=collection_id,
        tags=tags,
        created_at=existing.created_at,
        updated_at=get_current_time()
    )

    return storage.update_prompt(prompt_id, updated_prompt)


@app.patch("/prompts/{prompt_id}", response_model=Prompt)
def patch_prompt(prompt_id: str, prompt_data: PromptUpdate):
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
    tags = prompt_data.tags if getattr(prompt_data, 'tags', None) is not None else existing.tags
    # Normalize tags to lowercase
    if tags and prompt_data.tags is not None:
        tags = [tag.lower() for tag in tags]

    patched = Prompt(
        id=existing.id,
        title=title,
        content=content,
        description=description,
        collection_id=collection_id,
        tags=tags,
        created_at=existing.created_at,
        updated_at=get_current_time()
    )

    return storage.update_prompt(prompt_id, patched)


# NOTE: PATCH endpoint is missing! Students need to implement this.
# It should allow partial updates (only update provided fields)


@app.delete("/prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: str):
    if not storage.delete_prompt(prompt_id):
        raise HTTPException(status_code=404, detail="Prompt not found")
    return None


# ============== Collection Endpoints ==============

@app.get("/collections", response_model=CollectionList)
def list_collections():
    collections = storage.get_all_collections()
    return CollectionList(collections=collections, total=len(collections))


@app.get("/collections/{collection_id}", response_model=Collection)
def get_collection(collection_id: str):
    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@app.post("/collections", response_model=Collection, status_code=201)
def create_collection(collection_data: CollectionCreate):
    collection = Collection(**collection_data.model_dump())
    return storage.create_collection(collection)


@app.delete("/collections/{collection_id}", status_code=204)
def delete_collection(collection_id: str):
    if not storage.delete_collection(collection_id):
        raise HTTPException(status_code=404, detail="Collection not found")

    # Prompts that referenced this collection are now orphaned (collection_id set to None)
    return None


# ============== Tag Endpoints ==============

@app.get("/tags", response_model=TagList)
def get_all_tags():
    """Get all unique tags across all prompts."""
    prompts = storage.get_all_prompts()
    all_tags = set()
    for prompt in prompts:
        all_tags.update(prompt.tags)
    return TagList(tags=sorted(list(all_tags)))


@app.post("/prompts/{prompt_id}/tags", response_model=Prompt)
def add_tag_to_prompt(prompt_id: str, tag_data: TagAdd):
    """Add a tag to a prompt."""
    prompt = storage.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Normalize tag to lowercase and strip whitespace
    tag = tag_data.tag.strip().lower()
    
    # Validate tag is not empty after stripping
    if not tag:
        raise HTTPException(status_code=422, detail="Tag cannot be empty or whitespace only")
    
    # Add tag if not already present (avoid duplicates)
    if tag not in prompt.tags:
        prompt.tags.append(tag)
    
    # Update the prompt
    updated = storage.update_prompt(prompt_id, prompt)
    return updated


@app.delete("/prompts/{prompt_id}/tags/{tag}", status_code=204)
def remove_tag_from_prompt(prompt_id: str, tag: str):
    """Remove a tag from a prompt."""
    prompt = storage.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Normalize tag to lowercase
    tag = tag.lower()
    
    # Check if tag exists
    if tag not in prompt.tags:
        raise HTTPException(status_code=404, detail="Tag not found on this prompt")
    
    # Remove the tag
    prompt.tags.remove(tag)
    
    # Update the prompt
    storage.update_prompt(prompt_id, prompt)
    return None
