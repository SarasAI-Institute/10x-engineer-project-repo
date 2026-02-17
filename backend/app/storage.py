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
        """Create and store a new prompt.

        Adds a new prompt to the in-memory storage.

        Args:
            prompt (Prompt): The prompt object to be stored.

        Returns:
            Prompt: The stored prompt object.

        Example Usage:
            >>> new_prompt = Prompt(id="p1", ...)
            >>> storage.create_prompt(new_prompt)
        """
        self._prompts[prompt.id] = prompt
        return prompt
    
    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """Retrieve a prompt by its unique identifier.

        Fetches a prompt from storage using its ID.

        Args:
            prompt_id (str): The unique identifier of the prompt.

        Returns:
            Optional[Prompt]: The prompt object if found, None otherwise.

        Example Usage:
            >>> prompt = storage.get_prompt("p1")
        """
        return self._prompts.get(prompt_id)
    
    def get_all_prompts(self) -> List[Prompt]:
        """Retrieve all stored prompts.

        Returns a list of all prompts currently stored in memory.

        Returns:
            List[Prompt]: A list of all prompt objects stored.

        Example Usage:
            >>> all_prompts = storage.get_all_prompts()
        """
        return list(self._prompts.values())
    
    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        """Update the details of an existing prompt.

        Updates a stored prompt with new data if it exists.

        Args:
            prompt_id (str): The unique identifier of the prompt to update.
            prompt (Prompt): The updated prompt object.

        Returns:
            Optional[Prompt]: The updated prompt object if successful, None otherwise.

        Example Usage:
            >>> updated_prompt = Prompt(id="p1", ...)
            >>> storage.update_prompt("p1", updated_prompt)
        """
        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        return prompt
    
    def delete_prompt(self, prompt_id: str) -> bool:
        """Delete a prompt by its unique identifier.

        Removes a prompt from storage if it exists.

        Args:
            prompt_id (str): The unique identifier of the prompt to delete.

        Returns:
            bool: True if the prompt was deleted, False if it was not found.

        Example Usage:
            >>> success = storage.delete_prompt("p1")
        """
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            return True
        return False
    
    # ============== Collection Operations ==============
    
    def create_collection(self, collection: Collection) -> Collection:
        """Create and store a new collection.

        Adds a new collection to the in-memory storage.

        Args:
            collection (Collection): The collection object to be stored.

        Returns:
            Collection: The stored collection object.

        Example Usage:
            >>> new_collection = Collection(id="c1", ...)
            >>> storage.create_collection(new_collection)
        """
        self._collections[collection.id] = collection
        return collection
    
    def get_collection(self, collection_id: str) -> Optional[Collection]:
        """Retrieve a collection by its unique identifier.

        Fetches a collection from storage using its ID.

        Args:
            collection_id (str): The unique identifier of the collection.

        Returns:
            Optional[Collection]: The collection object if found, None otherwise.

        Example Usage:
            >>> collection = storage.get_collection("c1")
        """
        return self._collections.get(collection_id)
    
    def get_all_collections(self) -> List[Collection]:
        """Retrieve all stored collections.

        Returns a list of all collections currently stored in memory.

        Returns:
            List[Collection]: A list of all collection objects stored.

        Example Usage:
            >>> all_collections = storage.get_all_collections()
        """
        return list(self._collections.values())
    
    def delete_collection(self, collection_id: str) -> bool:
        """Delete a collection by its unique identifier.

        Removes a collection from storage if it exists.

        Args:
            collection_id (str): The unique identifier of the collection to delete.

        Returns:
            bool: True if the collection was deleted, False if it was not found.

        Example Usage:
            >>> success = storage.delete_collection("c1")
        """
        if collection_id in self._collections:
            del self._collections[collection_id]
            return True
        return False
    
    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        """Retrieve all prompts associated with a specific collection.

        Filters and returns all prompts belonging to the specified collection.

        Args:
            collection_id (str): The unique identifier of the collection.

        Returns:
            List[Prompt]: A list of prompts associated with the collection.

        Example Usage:
            >>> prompts_in_collection = storage.get_prompts_by_collection("c1")
        """
        return [p for p in self._prompts.values() if p.collection_id == collection_id]
    
    def get_or_create_default_collection(self) -> Collection:
        """Retrieve or create a default 'Uncategorized' collection.

        Checks if a default collection named 'Uncategorized' exists. 
        If not, creates and returns a new one.

        Returns:
            Collection: The existing or newly created 'Uncategorized' collection.

        Example Usage:
            >>> default_collection = storage.get_or_create_default_collection()
        """
        # Check if a default collection exists and return it
        for collection in self._collections.values():
            if collection.name == "Uncategorized":
                return collection

        # If not, create a new default collection
        # id will be auto-generated by the model's default_factory
        new_collection = Collection(name="Uncategorized")
        self.create_collection(new_collection)
        return new_collection

    # ============== Utility ==============
    
    def clear(self):
        """Clear all stored prompts and collections.

        Empties the in-memory storage for both prompts and collections.

        Example Usage:
            >>> storage.clear()
        """
        self._prompts.clear()
        self._collections.clear()


# Global storage instance
storage = Storage()

