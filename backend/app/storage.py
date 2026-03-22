"""In-memory storage for PromptLab.

Provides a simple storage layer for prompts and collections using in-memory dictionaries.
Intended for development and testing only. Not suitable for production use.
"""

from typing import Dict, List, Optional
from app.models import Prompt, Collection


class Storage:
    """
    In-memory storage handler for prompts and collections.

    Stores data in dictionaries keyed by unique IDs.
    This implementation does not provide persistence, concurrency control,
    or data integrity guarantees.

    Attributes:
        _prompts (Dict[str, Prompt]): Storage for prompt objects.
        _collections (Dict[str, Collection]): Storage for collection objects.
    """

    def __init__(self):
        """Initialize empty storage for prompts and collections."""
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
    
    # ============== Prompt Operations ==============

    def create_prompt(self, prompt: Prompt) -> Prompt:
        """
        Store a new prompt.

        Args:
            prompt (Prompt): Prompt object to store.

        Returns:
            Prompt: The stored prompt.
        """
        self._prompts[prompt.id] = prompt
        return prompt
    
    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """
        Retrieve a prompt by ID.

        Args:
            prompt_id (str): Unique identifier of the prompt.

        Returns:
            Optional[Prompt]: The prompt if found, otherwise None.
        """
        return self._prompts.get(prompt_id)
    
    def get_all_prompts(self) -> List[Prompt]:
        """
        Retrieve all stored prompts.

        Returns:
            List[Prompt]: List of all prompts.
        """
        return list(self._prompts.values())
    
    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        """
        Update an existing prompt.

        Args:
            prompt_id (str): Identifier of the prompt to update.
            prompt (Prompt): Updated prompt object.

        Returns:
            Optional[Prompt]: Updated prompt if successful, otherwise None.
        """
        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        return prompt
    
    def delete_prompt(self, prompt_id: str) -> bool:
        """
        Delete a prompt by ID.

        Args:
            prompt_id (str): Identifier of the prompt.

        Returns:
            bool: True if deleted successfully, False if prompt does not exist.
        """
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            return True
        return False
    
    # ============== Collection Operations ==============

    def create_collection(self, collection: Collection) -> Collection:
        """
        Store a new collection.

        Args:
            collection (Collection): Collection object to store.

        Returns:
            Collection: The stored collection.
        """
        self._collections[collection.id] = collection
        return collection
    
    def get_collection(self, collection_id: str) -> Optional[Collection]:
        """
        Retrieve a collection by ID.

        Args:
            collection_id (str): Unique identifier of the collection.

        Returns:
            Optional[Collection]: The collection if found, otherwise None.
        """
        return self._collections.get(collection_id)
    
    def get_all_collections(self) -> List[Collection]:
        """
        Retrieve all stored collections.

        Returns:
            List[Collection]: List of all collections.
        """
        return list(self._collections.values())
    
    def delete_collection(self, collection_id: str) -> bool:
        """
        Delete a collection by ID.

        Args:
            collection_id (str): Identifier of the collection.

        Returns:
            bool: True if deleted successfully, False if collection does not exist.

        Note:
            This operation does not handle prompts associated with the collection.
            It may leave orphaned prompts referencing a non-existent collection.
        """
        if collection_id in self._collections:
            del self._collections[collection_id]
            return True
        return False
    
    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        """
        Retrieve all prompts belonging to a specific collection.

        Args:
            collection_id (str): Collection identifier.

        Returns:
            List[Prompt]: Prompts associated with the given collection.
        """
        return [p for p in self._prompts.values() if p.collection_id == collection_id]
    
    # ============== Utility ==============

    def clear(self):
        """
        Clear all stored data.

        Removes all prompts and collections from memory.

        Returns:
            None
        """
        self._prompts.clear()
        self._collections.clear()


# Global storage instance
storage = Storage()