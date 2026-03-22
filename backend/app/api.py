"""FastAPI routes for PromptLab.

Defines all API endpoints for managing prompts and collections.
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
from app.utils import (
    sort_prompts_by_date,
    filter_prompts_by_collection,
    search_prompts,
    normalize_tags
)
from app import __version__


# ✅ SINGLE app instance (correct)
app = FastAPI(
    title="PromptLab API",
    description="AI Prompt Engineering Platform",
    version=__version__
)

# ✅ CORS applied to the correct app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://stunning-memory-wrrgp69rxg6xc94rp-5173.app.github.dev"],   # keep * for now (tighten later)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Health Check ==============

@app.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(status="healthy", version=__version__)


# ============== Prompt Endpoints ==============

@app.get("/prompts/", response_model=PromptList)
def list_prompts(
    collection_id: Optional[str] = None,
    search: Optional[str] = None,
    tag: Optional[str] = None
):
    prompts = storage.get_all_prompts()

    if collection_id:
        prompts = filter_prompts_by_collection(prompts, collection_id)

    if search:
        prompts = search_prompts(prompts, search)

    if tag:
        tag = tag.lower()
        prompts = [
            p for p in prompts
            if tag in [t.lower() for t in p.tags]
        ]

    prompts = sort_prompts_by_date(prompts, descending=True)

    return PromptList(prompts=prompts, total=len(prompts))


@app.get("/prompts/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: str):
    prompt = storage.get_prompt(prompt_id)

    if prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")

    return prompt


@app.post("/prompts/", response_model=Prompt, status_code=201)
def create_prompt(prompt_data: PromptCreate):
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")

    data = prompt_data.model_dump()
    data["tags"] = normalize_tags(data.get("tags", []))

    prompt = Prompt(**data)
    return storage.create_prompt(prompt)


@app.put("/prompts/{prompt_id}", response_model=Prompt)
def update_prompt(prompt_id: str, prompt_data: PromptUpdate):
    existing = storage.get_prompt(prompt_id)

    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")

    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")

    data = prompt_data.model_dump()
    data["tags"] = normalize_tags(data.get("tags", []))

    updated_prompt = Prompt(
        id=existing.id,
        created_at=existing.created_at,
        updated_at=get_current_time(),
        **data
    )

    return storage.update_prompt(prompt_id, updated_prompt)


@app.delete("/prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: str):
    if not storage.delete_prompt(prompt_id):
        raise HTTPException(status_code=404, detail="Prompt not found")
    return None


# ============== Collection Endpoints ==============

@app.get("/collections/", response_model=CollectionList)
def list_collections():
    collections = storage.get_all_collections()
    return CollectionList(collections=collections, total=len(collections))


@app.get("/collections/{collection_id}", response_model=Collection)
def get_collection(collection_id: str):
    collection = storage.get_collection(collection_id)

    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")

    return collection


@app.post("/collections/", response_model=Collection, status_code=201)
def create_collection(collection_data: CollectionCreate):
    collection = Collection(**collection_data.model_dump())
    return storage.create_collection(collection)


@app.delete("/collections/{collection_id}", status_code=204)
def delete_collection(collection_id: str):
    if not storage.delete_collection(collection_id):
        raise HTTPException(status_code=404, detail="Collection not found")

    prompts = storage.get_prompts_by_collection(collection_id)
    for p in prompts:
        p.collection_id = None
        storage.update_prompt(p.id, p)

    return None