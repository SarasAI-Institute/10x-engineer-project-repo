"""In-memory storage layer for PromptLab domain data."""

from typing import Dict, List, Optional
from app.models import Prompt, Collection, Tag


class Storage:
    """Simple in-memory store that mimics persistent operations."""

    def __init__(self):
        """Initialize the storage maps for prompts, collections, and tags."""
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
        self._tags: Dict[str, Tag] = {}
        self._tag_name_index: Dict[str, str] = {}
    
    # ============== Prompt Operations ==============
    
    def create_prompt(self, prompt: Prompt) -> Prompt:
        """Persist a new prompt in memory.

        Args:
            prompt: The prompt instance to store.

        Returns:
            The same prompt instance that was stored.
        """
        self._prompts[prompt.id] = prompt
        return prompt
    
    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """Retrieve a prompt by its identifier.

        Args:
            prompt_id: Unique identifier of the prompt.

        Returns:
            The Prompt instance if present, otherwise None.
        """
        return self._prompts.get(prompt_id)
    
    def get_all_prompts(self) -> List[Prompt]:
        """List all stored prompts (order not guaranteed)."""
        return list(self._prompts.values())
    
    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        """Replace a stored prompt with an updated version.

        Args:
            prompt_id: Identifier of the prompt to replace.
            prompt: Updated prompt instance.

        Returns:
            The updated prompt if it existed, otherwise None.
        """
        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        return prompt
    
    def delete_prompt(self, prompt_id: str) -> bool:
        """Delete a prompt by its identifier.

        Args:
            prompt_id: Identifier of the prompt to remove.

        Returns:
            True if deletion succeeded, False if the prompt was missing.
        """
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            return True
        return False
    
    # ============== Collection Operations ==============
    
    def create_collection(self, collection: Collection) -> Collection:
        """Persist a new collection."""
        self._collections[collection.id] = collection
        return collection
    
    def get_collection(self, collection_id: str) -> Optional[Collection]:
        """Retrieve a collection by its identifier."""
        return self._collections.get(collection_id)
    
    def get_all_collections(self) -> List[Collection]:
        """Return all persisted collections."""
        return list(self._collections.values())
    
    def delete_collection(self, collection_id: str) -> bool:
        """Delete a collection by its identifier.

        Args:
            collection_id: Identifier of the collection to delete.

        Returns:
            True if the collection was deleted, False otherwise.
        """
        if collection_id in self._collections:
            del self._collections[collection_id]
            return True
        return False
    
    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        """List prompts that belong to a specific collection."""
        return [p for p in self._prompts.values() if p.collection_id == collection_id]
    
    # ============== Tag Operations ==============

    def create_tag(self, tag: Tag) -> Tag:
        """Store a new tag, enforcing unique names case-insensitively."""
        normalized = tag.name.lower()
        if normalized in self._tag_name_index:
            raise ValueError("Tag name already exists")
        self._tags[tag.id] = tag
        self._tag_name_index[normalized] = tag.id
        return tag

    def get_tag(self, tag_id: str) -> Optional[Tag]:
        """Retrieve a tag by id."""
        return self._tags.get(tag_id)

    def get_all_tags(self) -> List[Tag]:
        """Return all stored tags."""
        return list(self._tags.values())

    def get_tag_by_name(self, name: str) -> Optional[Tag]:
        """Find a tag by its name (case-insensitive)."""
        tag_id = self._tag_name_index.get(name.lower())
        if not tag_id:
            return None
        return self._tags.get(tag_id)

    def update_tag(self, tag_id: str, tag: Tag) -> Optional[Tag]:
        """Replace an existing tag with new data."""
        if tag_id not in self._tags:
            return None
        normalized = tag.name.lower()
        existing = self._tags[tag_id]
        if normalized != existing.name.lower() and normalized in self._tag_name_index:
            raise ValueError("Tag name already exists")
        self._tag_name_index.pop(existing.name.lower(), None)
        self._tag_name_index[normalized] = tag_id
        self._tags[tag_id] = tag
        return tag

    def delete_tag(self, tag_id: str) -> bool:
        """Delete a tag and remove its references from prompts."""
        if tag_id not in self._tags:
            return False
        tag = self._tags.pop(tag_id)
        self._tag_name_index.pop(tag.name.lower(), None)
        for prompt in self._prompts.values():
            if tag_id in prompt.tags:
                prompt.tags = [t for t in prompt.tags if t != tag_id]
        return True

    def assign_tag_to_prompt(self, prompt_id: str, tag_id: str) -> Prompt:
        """Attach a tag to a prompt."""
        prompt = self.get_prompt(prompt_id)
        tag = self.get_tag(tag_id)
        if not prompt or not tag:
            raise KeyError("Prompt or tag not found")
        if tag_id in prompt.tags:
            raise ValueError("Tag already assigned")
        prompt.tags = prompt.tags + [tag_id]
        return prompt

    def remove_tag_from_prompt(self, prompt_id: str, tag_id: str) -> Prompt:
        """Remove a tag from a prompt."""
        prompt = self.get_prompt(prompt_id)
        if not prompt:
            raise KeyError("Prompt not found")
        if tag_id not in prompt.tags:
            raise ValueError("Tag not assigned to prompt")
        prompt.tags = [t for t in prompt.tags if t != tag_id]
        return prompt

    def get_prompts_by_tag_name(self, tag_name: str) -> List[Prompt]:
        """Return prompts associated with the tag name."""
        tag = self.get_tag_by_name(tag_name)
        if not tag:
            return []
        return [p for p in self._prompts.values() if tag.id in p.tags]

    # ============== Utility ==============
    
    def clear(self):
        """Reset all stored prompts, collections, and tags."""
        self._prompts.clear()
        self._collections.clear()
        self._tags.clear()
        self._tag_name_index.clear()


# Global storage instance
storage = Storage()
