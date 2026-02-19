"""In-memory storage for PromptLab

This module provides simple in-memory storage for prompts and collections.
In a production environment, this would be replaced with a database.
"""

from typing import Dict, List, Optional
from app.models import Prompt, Collection


class Storage:
    def __init__(self):
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
    
    # ============== Prompt Operations ==============  
    def create_prompt(self, prompt: Prompt) -> Prompt:
        """Creates and stores a new prompt.

        This method adds a new prompt to the storage using the prompt's unique identifier.

        Args:
            prompt (Prompt): The prompt to be stored, with a unique identifier.

        Returns:
            Prompt: The prompt that was added to the storage.

        Example:
            new_prompt = Prompt(id="123", text="Sample text")
            stored_prompt = storage.create_prompt(new_prompt)
        """
        self._prompts[prompt.id] = prompt
        return prompt
    
    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """Retrieves a prompt by its unique identifier.

        Args:
            prompt_id (str): The unique identifier of the prompt to retrieve.

        Returns:
            Optional[Prompt]: The prompt associated with the ID, or None if not found.
        """
        return self._prompts.get(prompt_id)
    
    def get_all_prompts(self) -> List[Prompt]:
        """Retrieves all stored prompts.

        Returns:
            List[Prompt]: A list of all prompts currently stored.
        """
        return list(self._prompts.values())
    
    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        """Updates an existing prompt.

        Args:
            prompt_id (str): The unique identifier of the prompt to update.
            prompt (Prompt): The prompt data to update with.

        Returns:
            Optional[Prompt]: The updated prompt if found, otherwise None.
        """
        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        return prompt
    
    def delete_prompt(self, prompt_id: str) -> bool:
        """Deletes a prompt by its unique identifier.

        Args:
            prompt_id (str): The unique identifier of the prompt to delete.

        Returns:
            bool: True if the prompt was deleted, False if not found.
        """
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            return True
        return False
    
    def create_collection(self, collection: Collection) -> Collection:
        """Creates and stores a new collection.

        Args:
            collection (Collection): The collection to be stored, with a unique identifier.

        Returns:
            Collection: The collection that was added to the storage.
        """
        self._collections[collection.id] = collection
        return collection
    
    def get_collection(self, collection_id: str) -> Optional[Collection]:
        """Retrieves a collection by its unique identifier.

        Args:
            collection_id (str): The unique identifier of the collection to retrieve.

        Returns:
            Optional[Collection]: The collection associated with the ID, or None if not found.
        """
        return self._collections.get(collection_id)
    
    def get_all_collections(self) -> List[Collection]:
        """Retrieves all stored collections.

        Returns:
            List[Collection]: A list of all collections currently stored.
        """
        return list(self._collections.values())
    
    def delete_collection(self, collection_id: str) -> bool:
        """Deletes a collection by its unique identifier.

        Args:
            collection_id (str): The unique identifier of the collection to delete.

        Returns:
            bool: True if the collection was deleted, False if not found.
        """
        if collection_id in self._collections:
            del self._collections[collection_id]
            return True
        return False
    
    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        """Retrieves all prompts belonging to a specific collection.

        Args:
            collection_id (str): The unique identifier of the collection whose prompts are to be retrieved.

        Returns:
            List[Prompt]: A list of prompts associated with the specified collection.
        """
        return [p for p in self._prompts.values() if p.collection_id == collection_id]
    
    def clear(self):
        """Clears all stored prompts and collections.

        This will remove all entries from the storage.
        """
        self._prompts.clear()
        self._collections.clear()

# Global storage instance
storage = Storage()
