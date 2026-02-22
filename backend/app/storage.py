"""In-memory storage for PromptLab.

This module provides simple in-memory storage for prompts and collections.
In a production environment, this would be replaced with a database like
PostgreSQL, MongoDB, or another persistent storage solution.

The storage is implemented as a singleton pattern using a global instance.
All data is stored in Python dictionaries keyed by ID for O(1) lookups.

Note: All data is lost when the application restarts since it's in-memory only.
"""

from typing import Dict, List, Optional
from app.models import Prompt, Collection, get_current_time


class Storage:
    """In-memory storage manager for prompts and collections.
    
    This class manages two separate in-memory stores:
    - _prompts: Dictionary mapping prompt IDs to Prompt objects
    - _collections: Dictionary mapping collection IDs to Collection objects
    
    All operations are synchronous and thread-unsafe. For production use,
    proper database with ACID guarantees should be used.
    """
    def __init__(self):
        """Initialize empty storage dictionaries."""
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
    
    # ============== Prompt Operations ==============
    
    def create_prompt(self, prompt: Prompt) -> Prompt:
        """Store a new prompt.
        
        Args:
            prompt: The prompt object to store.
            
        Returns:
            Prompt: The stored prompt (same as input).
        """
        self._prompts[prompt.id] = prompt
        return prompt
    
    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """Retrieve a prompt by ID.
        
        Args:
            prompt_id: The unique identifier of the prompt.
            
        Returns:
            Optional[Prompt]: The prompt if found, None otherwise.
        """
        return self._prompts.get(prompt_id)
    
    def get_all_prompts(self) -> List[Prompt]:
        """Retrieve all prompts.
        
        Returns:
            List[Prompt]: List of all stored prompts.
        """
        return list(self._prompts.values())
    
    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        """Update an existing prompt.
        
        The updated_at timestamp is automatically refreshed to current time.
        
        Args:
            prompt_id: The unique identifier of the prompt to update.
            prompt: The updated prompt object.
            
        Returns:
            Optional[Prompt]: The updated prompt if found, None otherwise.
        """
        if prompt_id not in self._prompts:
            return None
        # Ensure updated_at reflects the update time
        try:
            prompt = prompt.model_copy(update={"updated_at": get_current_time()})
        except Exception:
            # Fallback: if model_copy isn't available (older pydantic), set attribute
            try:
                prompt.updated_at = get_current_time()
            except Exception:
                pass

        self._prompts[prompt_id] = prompt
        return prompt
    
    def delete_prompt(self, prompt_id: str) -> bool:
        """Delete a prompt by ID.
        
        Args:
            prompt_id: The unique identifier of the prompt to delete.
            
        Returns:
            bool: True if the prompt was deleted, False if not found.
        """
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            return True
        return False
    
    # ============== Collection Operations ==============
    
    def create_collection(self, collection: Collection) -> Collection:
        """Store a new collection.
        
        Args:
            collection: The collection object to store.
            
        Returns:
            Collection: The stored collection (same as input).
        """
        self._collections[collection.id] = collection
        return collection
    
    def get_collection(self, collection_id: str) -> Optional[Collection]:
        """Retrieve a collection by ID.
        
        Args:
            collection_id: The unique identifier of the collection.
            
        Returns:
            Optional[Collection]: The collection if found, None otherwise.
        """
        return self._collections.get(collection_id)
    
    def get_all_collections(self) -> List[Collection]:
        """Retrieve all collections.
        
        Returns:
            List[Collection]: List of all stored collections.
        """
        return list(self._collections.values())
    
    def delete_collection(self, collection_id: str) -> bool:
        """Delete a collection by ID.
        
        When a collection is deleted, all prompts that reference it have their
        collection_id set to None (becoming orphaned prompts).
        
        Args:
            collection_id: The unique identifier of the collection to delete.
            
        Returns:
            bool: True if the collection was deleted, False if not found.
        """
        if collection_id in self._collections:
            # Remove the collection
            del self._collections[collection_id]

            # Orphan prompts that referenced this collection by setting collection_id to None
            for pid, p in list(self._prompts.items()):
                try:
                    if p.collection_id == collection_id:
                        try:
                            newp = p.model_copy(update={"collection_id": None})
                        except Exception:
                            # fallback to attribute assignment
                            p.collection_id = None
                            newp = p
                        self._prompts[pid] = newp
                except Exception:
                    # If prompt object shape unexpected, skip
                    continue

            return True
        return False
    
    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        """Get all prompts belonging to a specific collection.
        
        Args:
            collection_id: The unique identifier of the collection.
            
        Returns:
            List[Prompt]: List of prompts in the specified collection.
        """
        return [p for p in self._prompts.values() if p.collection_id == collection_id]
    
    # ============== Utility ==============
    
    def clear(self):
        """Clear all stored data.
        
        This method is primarily used for testing to reset the storage
        to a clean state between test runs.
        """
        self._prompts.clear()
        self._collections.clear()


# Global storage instance
# This singleton is imported and used throughout the application
storage = Storage()
