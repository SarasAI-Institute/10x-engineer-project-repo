"""In-memory storage for PromptLab

This module provides simple in-memory storage for prompts and collections.
In a production environment, this would be replaced with a database.
"""

from typing import Dict, List, Optional
from app.models import Prompt, Collection


class Storage:
    """Simple in-memory storage for prompts and collections.

    This class provides a minimal CRUD-style API used by the application and
    by tests. It stores data in-process using Python dictionaries. In a real
    deployment this would be replaced with a persistent database layer.

    Attributes:
        _prompts: Internal mapping of prompt_id -> Prompt.
        _collections: Internal mapping of collection_id -> Collection.
    """
    def __init__(self):
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
    
    # ============== Prompt Operations ==============
    
    def create_prompt(self, prompt: Prompt) -> Prompt:
        """Create and store a Prompt object.

        Args:
            prompt: A fully-initialized `Prompt` instance. Its `id` must be
                unique within the current storage instance.

        Returns:
            Prompt: The stored Prompt (same object passed in).
        """
        self._prompts[prompt.id] = prompt
        return prompt
    
    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """Retrieve a prompt by ID.

        Args:
            prompt_id: Identifier of the prompt to return.

        Returns:
            Optional[Prompt]: The prompt if found, otherwise None.
        """
        return self._prompts.get(prompt_id)
    
    def get_all_prompts(self) -> List[Prompt]:
        """Return a list of all prompts in storage.

        Returns:
            List[Prompt]: All stored prompts (possibly empty).
        """
        return list(self._prompts.values())
    
    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        """Replace an existing prompt with the provided value.

        Args:
            prompt_id: ID of the prompt to update.
            prompt: Prompt object to store in place of the existing one.

        Returns:
            Optional[Prompt]: The updated prompt, or None if the prompt_id was
            not found.
        """
        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        return prompt
    
    def delete_prompt(self, prompt_id: str) -> bool:
        """Delete a prompt by ID.

        Returns True when a prompt was deleted, False if it did not exist.
        """
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            return True
        return False
    
    # ============== Collection Operations ==============
    
    def create_collection(self, collection: Collection) -> Collection:
        """Create and store a Collection object.

        Args:
            collection: A `Collection` instance with an `id` field.

        Returns:
            Collection: The stored collection object.
        """
        self._collections[collection.id] = collection
        return collection
    
    def get_collection(self, collection_id: str) -> Optional[Collection]:
        """Retrieve a collection by ID.

        Args:
            collection_id: Identifier of the collection to return.

        Returns:
            Optional[Collection]: The collection if found, otherwise None.
        """
        return self._collections.get(collection_id)
    
    def get_all_collections(self) -> List[Collection]:
        """Return all collections stored in memory.

        Returns:
            List[Collection]: All stored collections.
        """
        return list(self._collections.values())
    
    def delete_collection(self, collection_id: str) -> bool:
        """Delete a collection by ID.

        Returns True when the collection was removed, False if it did not
        exist.
        """
        if collection_id in self._collections:
            del self._collections[collection_id]
            return True
        return False
    
    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        """Return prompts that belong to the given collection.

        Args:
            collection_id: Collection identifier to filter prompts by.

        Returns:
            List[Prompt]: Prompts whose `collection_id` equals the argument.
        """
        return [p for p in self._prompts.values() if p.collection_id == collection_id]
    
    # ============== Utility ==============
    
    def clear(self):
        """Clear all stored prompts and collections (test helper).

        Useful for tests and resets during development.
        """
        self._prompts.clear()
        self._collections.clear()


# Global storage instance
storage = Storage()
