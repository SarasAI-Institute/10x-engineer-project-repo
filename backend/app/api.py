"""FastAPI routes for PromptLab"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from app.models import (
    Prompt,
    PromptCreate,
    PromptUpdate,
    PromptPatch,
    Collection,
    CollectionCreate,
    PromptList,
    CollectionList,
    HealthResponse,
    PromptVersion,
    PromptVersionList,
    PromptVersionSummary,
    PromptVersionRestoreRequest,
    get_current_time,
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


def _create_version_snapshot(prompt: Prompt, change_note: Optional[str]) -> PromptVersion:
    """Create and persist a new version snapshot for the given prompt."""

    version_number = storage.get_next_version_number(prompt.id)
    version = PromptVersion(
        prompt_id=prompt.id,
        version_number=version_number,
        title=prompt.title,
        content=prompt.content,
        description=prompt.description,
        collection_id=prompt.collection_id,
        change_note=change_note,
    )
    return storage.create_prompt_version(version)


def _get_prompt_or_404(prompt_id: str) -> Prompt:
    """Return a prompt or raise a 404 HTTP exception."""

    prompt = storage.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt


def _get_version_or_404(prompt_id: str, version_id: str) -> PromptVersion:
    """Return a prompt version or raise a 404 HTTP exception."""

    version = storage.get_prompt_version(prompt_id, version_id)
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")
    return version


def _validate_collection_reference(collection_id: Optional[str]) -> None:
    """Ensure a referenced collection exists if an ID is provided."""

    if not collection_id:
        return
    if not storage.get_collection(collection_id):
        raise HTTPException(status_code=400, detail="Collection not found")


def _filtered_prompts(collection_id: Optional[str], search: Optional[str]) -> list[Prompt]:
    """Apply collection and search filters before sorting prompts."""

    prompts = storage.get_all_prompts()
    if collection_id:
        prompts = filter_prompts_by_collection(prompts, collection_id)
    if search:
        prompts = search_prompts(prompts, search)
    return sort_prompts_by_date(prompts, descending=True)



# ============== Health Check ==============

@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Return overall API health information."""

    return HealthResponse(status="healthy", version=__version__)



# ============== Prompt Endpoints ==============

@app.get("/prompts", response_model=PromptList)
def list_prompts(
    collection_id: Optional[str] = None,
    search: Optional[str] = None
) -> PromptList:
    """List prompts optionally filtered by collection and/or search query."""

    prompts = _filtered_prompts(collection_id, search)
    return PromptList(prompts=prompts, total=len(prompts))


@app.get("/prompts/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: str) -> Prompt:
    """Fetch a single prompt by identifier."""

    return _get_prompt_or_404(prompt_id)


@app.post("/prompts", response_model=Prompt, status_code=201)
def create_prompt(prompt_data: PromptCreate) -> Prompt:
    """Create a new prompt resource."""

    _validate_collection_reference(prompt_data.collection_id)
    prompt = Prompt(**prompt_data.model_dump())
    return storage.create_prompt(prompt)


@app.put("/prompts/{prompt_id}", response_model=Prompt)
def update_prompt(prompt_id: str, prompt_data: PromptUpdate) -> Prompt:
    """Replace an existing prompt with updated data."""

    existing = _get_prompt_or_404(prompt_id)
    _validate_collection_reference(prompt_data.collection_id)

    version = _create_version_snapshot(existing, prompt_data.change_note)

    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title,
        content=prompt_data.content,
        description=prompt_data.description,
        collection_id=prompt_data.collection_id,
        created_at=existing.created_at,
        updated_at=get_current_time(),
        current_version=version.version_number,
    )

    storage.update_prompt(prompt_id, updated_prompt)
    return updated_prompt


# PATCH endpoint allows partial updates (only provided fields are changed).

@app.patch("/prompts/{prompt_id}", response_model=Prompt)
def patch_prompt(prompt_id: str, prompt_data: PromptPatch) -> Prompt:
    """Apply partial updates to a prompt."""

    existing = _get_prompt_or_404(prompt_id)

    updates = prompt_data.model_dump(exclude_unset=True)
    change_note = updates.pop("change_note", None)

    if "collection_id" in updates:
        _validate_collection_reference(updates["collection_id"])

    version = _create_version_snapshot(existing, change_note)

    updated_prompt = existing.model_copy(
        update={**updates, "updated_at": get_current_time(), "current_version": version.version_number}
    )
    storage.update_prompt(prompt_id, updated_prompt)
    return updated_prompt

# ============== Prompt Version Endpoints ==============

@app.get("/prompts/{prompt_id}/versions", response_model=PromptVersionList)
def list_prompt_versions(prompt_id: str) -> PromptVersionList:
    """Return summaries for all versions of a prompt."""

    _get_prompt_or_404(prompt_id)
    versions = storage.get_prompt_versions(prompt_id)
    summaries = [
        PromptVersionSummary(
            id=version.id,
            version_number=version.version_number,
            editor=version.editor,
            change_note=version.change_note,
            created_at=version.created_at,
        )
        for version in versions
    ]

    return PromptVersionList(prompt_id=prompt_id, versions=summaries, total=len(summaries))


@app.get("/prompts/{prompt_id}/versions/{version_id}", response_model=PromptVersion)
def get_prompt_version_detail(prompt_id: str, version_id: str) -> PromptVersion:
    """Return the details for a specific prompt version."""

    _get_prompt_or_404(prompt_id)
    return _get_version_or_404(prompt_id, version_id)


@app.post("/prompts/{prompt_id}/versions/{version_id}/restore", response_model=Prompt)
def restore_prompt_version(
    prompt_id: str,
    version_id: str,
    restore_request: PromptVersionRestoreRequest,
) -> Prompt:
    """Restore a prompt to a previous version and record the change."""

    prompt = _get_prompt_or_404(prompt_id)
    version = _get_version_or_404(prompt_id, version_id)

    audit_version = _create_version_snapshot(prompt, restore_request.change_note)

    restored_prompt = prompt.model_copy(
        update={
            "title": version.title,
            "content": version.content,
            "description": version.description,
            "collection_id": version.collection_id,
            "updated_at": get_current_time(),
            "current_version": audit_version.version_number,
        }
    )

    storage.update_prompt(prompt_id, restored_prompt)
    return restored_prompt


@app.delete("/prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: str) -> None:
    """Delete a prompt by identifier."""

    if not storage.delete_prompt(prompt_id):
        raise HTTPException(status_code=404, detail="Prompt not found")
    return None


# ============== Collection Endpoints ==============

@app.get("/collections", response_model=CollectionList)
def list_collections() -> CollectionList:
    """Return all collections."""

    collections = storage.get_all_collections()
    return CollectionList(collections=collections, total=len(collections))


@app.get("/collections/{collection_id}", response_model=Collection)
def get_collection(collection_id: str) -> Collection:
    """Retrieve a single collection by identifier."""

    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@app.post("/collections", response_model=Collection, status_code=201)
def create_collection(collection_data: CollectionCreate) -> Collection:
    """Create a new collection."""

    collection = Collection(**collection_data.model_dump())
    return storage.create_collection(collection)


@app.delete("/collections/{collection_id}", status_code=204)
def delete_collection(collection_id: str) -> None:
    """Delete a collection and clear prompt references to it."""

    if not storage.delete_collection(collection_id):
        raise HTTPException(status_code=404, detail="Collection not found")
    return None
