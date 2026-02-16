"""In-memory storage for PromptLab

This module provides simple in-memory storage for prompts and collections.
In a production environment, this would be replaced with a database.
"""

from typing import Dict, List, Optional
from app.models import Prompt, Collection


class Storage:
    """A class to manage in-memory storage of prompts and collections.

    This class provides methods to create, retrieve, update, and delete prompts
    and collections. It simulates a basic storage system suitable for development
    or testing purposes. In practice, a database or persistent storage solution
    would replace this in-memory design.
    """

    def __init__(self):
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
    
    # ============== Prompt Operations ==============
    
    def create_prompt(self, prompt: Prompt) -> Prompt:
        """Add a new prompt to storage.

        Args:
            prompt (Prompt): The prompt to be added.
        Returns:
            Prompt: The prompt that was added.
        """
        self._prompts[prompt.id] = prompt
        return prompt
    
    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """Retrieve a prompt by its ID.

        Args:
            prompt_id (str): The ID of the prompt to retrieve.
        Returns:
            Optional[Prompt]: The prompt if found, or None if not.
        """
        return self._prompts.get(prompt_id)
    
    def get_all_prompts(self) -> List[Prompt]:
        """Retrieve all stored prompts.

        Returns:
            List[Prompt]: A list of all prompts in storage.
        """
        return list(self._prompts.values())

    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        """Update an existing prompt.

        Args:
            prompt_id (str): The ID of the prompt to update.
            prompt (Prompt): The updated prompt data.

        Returns:
            Optional[Prompt]: The updated prompt if successful, or None if the prompt was not found.
        """
        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        return prompt

    def delete_prompt(self, prompt_id: str) -> bool:
        """Remove a prompt from storage.

        Args:
            prompt_id (str): The ID of the prompt to delete.

        Returns:
            bool: True if the prompt was deleted, False if it was not found.
        """
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            return True
        return False
    
    # ============== Collection Operations ==============
    def create_collection(self, collection: Collection) -> Collection:
        """Add a new collection to storage.

        Args:
            collection (Collection): The collection to be added.

        Returns:
            Collection: The collection that was added.
        """
        self._collections[collection.id] = collection
        return collection

    def get_collection(self, collection_id: str) -> Optional[Collection]:
        """Retrieve a collection by its ID.

        Args:
            collection_id (str): The ID of the collection to retrieve.

        Returns:
            Optional[Collection]: The collection if found, or None if not.
        """
        return self._collections.get(collection_id)

    def get_all_collections(self) -> List[Collection]:
        """Retrieve all stored collections.

        Returns:
            List[Collection]: A list of all collections in storage.
        """
        return list(self._collections.values())

    def delete_collection(self, collection_id: str) -> bool:
        """Remove a collection from storage.

        Args:
            collection_id (str): The ID of the collection to delete.

        Returns:
            bool: True if the collection was deleted, False if not found.
        """
        if collection_id in self._collections:
            del self._collections[collection_id]
            return True
        return False

    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        """Retrieve all prompts associated with a specific collection.

        Args:
            collection_id (str): The ID of the collection for prompt retrieval.

        Returns:
            List[Prompt]: A list of prompts associated with the specified collection.
        """
        return [p for p in self._prompts.values() if p.collection_id == collection_id]
    
    # ============== Utility ==============
    
    def clear(self):
        """Clear all stored prompts and collections."""
        self._prompts.clear()
        self._collections.clear()


# Global storage instance
storage = Storage()

