"""In-memory storage for PromptLab

This module provides simple in-memory storage for prompts and collections.
In a production environment, this would be replaced with a database.
"""

from typing import Dict, List, Optional
from app.models import Prompt, Collection, get_current_time


class Storage:
    def __init__(self):
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
    
    # ============== Prompt Operations ==============
    
    def create_prompt(self, prompt: Prompt) -> Prompt:
        self._prompts[prompt.id] = prompt
        return prompt
    
    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        return self._prompts.get(prompt_id)
    
    def get_all_prompts(self) -> List[Prompt]:
        return list(self._prompts.values())
    
    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
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
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            return True
        return False
    
    # ============== Collection Operations ==============
    
    def create_collection(self, collection: Collection) -> Collection:
        self._collections[collection.id] = collection
        return collection
    
    def get_collection(self, collection_id: str) -> Optional[Collection]:
        return self._collections.get(collection_id)
    
    def get_all_collections(self) -> List[Collection]:
        return list(self._collections.values())
    
    def delete_collection(self, collection_id: str) -> bool:
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
        return [p for p in self._prompts.values() if p.collection_id == collection_id]
    
    # ============== Utility ==============
    
    def clear(self):
        self._prompts.clear()
        self._collections.clear()


# Global storage instance
storage = Storage()
