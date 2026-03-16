"""In-memory storage for PromptLab

    
This module provides simple in-memory storage for prompts and collections.
In a production environment, this would be replaced with a database.
"""

from typing import Dict, List, Optional
from app.models import Prompt, PromptVersion, Collection


class Storage:
    """Simple in-memory repository for prompts and collections."""

    def __init__(self):
        """Initialize the storage dictionaries."""

        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
        self._prompt_versions: Dict[str, List[PromptVersion]] = {}
    
    # ============== Prompt Operations ==============
    
    def create_prompt(self, prompt: Prompt) -> Prompt:
        """Store a prompt in memory.

        Args:
            prompt (Prompt): The prompt to persist.

        Returns:
            Prompt: The stored prompt instance.
        """

        self._prompts[prompt.id] = prompt
        return prompt
    
    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """Retrieve a prompt by identifier.

        Args:
            prompt_id (str): The unique prompt identifier.

        Returns:
            Optional[Prompt]: The matching prompt or ``None`` if absent.
        """

        return self._prompts.get(prompt_id)
    
    def get_all_prompts(self) -> List[Prompt]:
        """List all stored prompts.

        Returns:
            List[Prompt]: Every prompt currently stored.
        """

        return list(self._prompts.values())
    
    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        """Replace the prompt stored under the given identifier.

        Args:
            prompt_id (str): The unique prompt identifier.
            prompt (Prompt): The updated prompt payload.

        Returns:
            Optional[Prompt]: The updated prompt if it exists, otherwise ``None``.
        """

        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        return prompt
    
    def delete_prompt(self, prompt_id: str) -> bool:
        """Remove a prompt by identifier.

        Args:
            prompt_id (str): The identifier of the prompt to delete.

        Returns:
            bool: ``True`` if the prompt was deleted, ``False`` otherwise.
        """

        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            self._prompt_versions.pop(prompt_id, None)
            return True
        return False
    
    # ============== Collection Operations ==============
    
    def create_collection(self, collection: Collection) -> Collection:
        """Store a collection in memory.

        Args:
            collection (Collection): The collection to persist.

        Returns:
            Collection: The stored collection instance.
        """

        self._collections[collection.id] = collection
        return collection
    
    def get_collection(self, collection_id: str) -> Optional[Collection]:
        """Retrieve a collection by identifier.

        Args:
            collection_id (str): The unique collection identifier.

        Returns:
            Optional[Collection]: The matching collection or ``None`` if absent.
        """

        return self._collections.get(collection_id)
    
    def get_all_collections(self) -> List[Collection]:
        """List all stored collections.

        Returns:
            List[Collection]: Every collection currently stored.
        """

        return list(self._collections.values())
    
    
    def delete_collection(self, collection_id: str) -> bool:
        """Remove a collection and clear prompt references to it.

        Args:
            collection_id (str): The identifier of the collection to delete.

        Returns:
            bool: ``True`` if the collection was deleted, ``False`` otherwise.
        """

        if collection_id in self._collections:
            # Clear collection_id on prompts that referenced this collection
            for prompt in self._prompts.values():
                if prompt.collection_id == collection_id:
                    prompt.collection_id = None

            del self._collections[collection_id]
            return True
        return False

    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        """Get prompts that belong to the specified collection.

        Args:
            collection_id (str): The collection identifier to filter by.

        Returns:
            List[Prompt]: Prompts associated with the collection.
        """

        return [p for p in self._prompts.values() if p.collection_id == collection_id]
    
    # ============== Version Operations ==============

    def create_prompt_version(self, version: PromptVersion) -> PromptVersion:
        """Persist a snapshot of a prompt before it was modified."""

        versions = self._prompt_versions.setdefault(version.prompt_id, [])
        versions.append(version)
        return version

    def get_prompt_versions(self, prompt_id: str) -> List[PromptVersion]:
        """Return versions for a prompt ordered newest-first."""

        versions = self._prompt_versions.get(prompt_id, [])
        return sorted(versions, key=lambda v: v.version_number, reverse=True)

    def get_prompt_version(self, prompt_id: str, version_id: str) -> Optional[PromptVersion]:
        """Fetch a single version for a prompt."""

        for version in self._prompt_versions.get(prompt_id, []):
            if version.id == version_id:
                return version
        return None

    def get_next_version_number(self, prompt_id: str) -> int:
        """Compute the next sequential version number for a prompt."""

        versions = self._prompt_versions.get(prompt_id, [])
        if not versions:
            return 1
        return max(version.version_number for version in versions) + 1
    
    # ============== Utility ==============
    
    def clear(self):
        """Remove all prompts, collections, and versions from storage."""

        self._prompts.clear()
        self._collections.clear()
        self._prompt_versions.clear()


# Global storage instance
storage = Storage()
