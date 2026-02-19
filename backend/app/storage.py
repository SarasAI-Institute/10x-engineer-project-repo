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
        """Create a new prompt in the storage.

        Args:
            prompt (Prompt): The Prompt object to be added to storage.

        Returns:
            Prompt: The Prompt object that was added to storage.

        Example usage:
            new_prompt = Prompt(id='prompt_123', title='New Prompt', collection_id='collection_123')
            stored_prompt = storage.create_prompt(new_prompt)
            print(stored_prompt.id)
        """
        self._prompts[prompt.id] = prompt
        return prompt
    
    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """Retrieve a prompt by its unique ID.

        Args:
            prompt_id (str): The unique ID of the prompt to retrieve.

        Returns:
            Optional[Prompt]: The Prompt object matching the given ID, or None if not found.

        Example usage:
            prompt = storage.get_prompt('prompt_123')
            if prompt is not None:
                print(prompt.title)
        """
        return self._prompts.get(prompt_id)
    
    def get_all_prompts(self) -> List[Prompt]:
        """Retrieve all prompts stored in the system.

        Returns:
            List[Prompt]: A list of all Prompt objects available in storage.

        Example usage:
            all_prompts = storage.get_all_prompts()
            for prompt in all_prompts:
                print(prompt.title)
        """
        return list(self._prompts.values())
    
    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        """Update an existing prompt by its unique ID.

        Args:
            prompt_id (str): The unique ID of the prompt to update.
            prompt (Prompt): The new Prompt object to replace the existing one.

        Returns:
            Optional[Prompt]: The updated Prompt object, or None if the prompt ID was not found.

        Example usage:
            updated_prompt = Prompt(id='prompt_123', title='Updated Prompt', collection_id='collection_123')
            result = storage.update_prompt('prompt_123', updated_prompt)
            if result is not None:
                print(result.title)
        """
        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        return prompt
    
    def delete_prompt(self, prompt_id: str) -> bool:
        """Delete a prompt by its unique ID.

        Args:
            prompt_id (str): The unique ID of the prompt to delete.

        Returns:
            bool: True if the prompt was successfully deleted, otherwise False.

        Example usage:
            success = storage.delete_prompt('prompt_123')
            if success:
                print('Prompt deleted successfully')
            else:
                print('Prompt not found')
        """
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            return True
        return False
    
    def create_collection(self, collection: Collection) -> Collection:
        """Create a new collection in the storage.

        Args:
            collection (Collection): The Collection object to be added to storage.

        Returns:
            Collection: The Collection object that was added to storage.

        Example usage:
            new_collection = Collection(id='collection_123', name='New Collection')
            stored_collection = storage.create_collection(new_collection)
            print(stored_collection.id)
        """
        self._collections[collection.id] = collection
        return collection
    
    def get_collection(self, collection_id: str) -> Optional[Collection]:
        """Retrieve a collection by its unique ID.

        Args:
            collection_id (str): The unique ID of the collection to retrieve.

        Returns:
            Optional[Collection]: The Collection object matching the given ID, or None if not found.

        Example usage:
            collection = storage.get_collection('collection_123')
            if collection is not None:
                print(collection.name)
        """
        return self._collections.get(collection_id)
    
    def get_all_collections(self) -> List[Collection]:
        """Retrieve all collections stored in the system.

        Returns:
            List[Collection]: A list of all Collection objects available in storage.

        Example usage:
            all_collections = storage.get_all_collections()
            for collection in all_collections:
                print(collection.name)
        """
        return list(self._collections.values())
    
    def delete_collection(self, collection_id: str) -> bool:
        """Delete a collection by its unique ID.

        Args:
            collection_id (str): The unique ID of the collection to delete.

        Returns:
            bool: True if the collection was successfully deleted, otherwise False.

        Example usage:
            success = storage.delete_collection('collection_123')
            if success:
                print('Collection deleted successfully')
            else:
                print('Collection not found')
        """
        if collection_id in self._collections:
            del self._collections[collection_id]
            return True
        return False

    def clear(self):
        """Clear all prompts and collections from the storage.

        Example usage:
            storage.clear()
            print('Storage cleared')
        """
        self._prompts.clear()
        self._collections.clear()
    

    

    
    # ============== Collection Operations ==============
    
  
    
    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        """Retrieve all prompts associated with a specific collection.

        Args:
            collection_id (str): The ID of the collection whose prompts are to be retrieved.

        Returns:
            List[Prompt]: A list of Prompt objects that belong to the specified collection.
                          Returns an empty list if no prompts are found for the given collection ID.

        Example usage:
            prompts = storage.get_prompts_by_collection('collection_123')
            for prompt in prompts:
                print(prompt.title)
        """
        return [p for p in self._prompts.values() if p.collection_id == collection_id]
    
    # ============== Utility ==============
    
    def clear(self):
        self._prompts.clear()
        self._collections.clear()


# Global storage instance
storage = Storage()
