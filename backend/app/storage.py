"""In-memory storage for PromptLab

This module provides simple in-memory storage for prompts and collections.
In a production environment, this would be replaced with a database.
"""

from typing import Dict, List, Optional
from app.models import Prompt, Collection


class Storage:
    def __init__(self):
        """Initializes the storage for prompts and collections.

        This constructor sets up two dictionaries to hold prompts and collections,
        associating string keys with their respective Prompt and Collection objects.

        Attributes:
            _prompts (Dict[str, Prompt]): A dictionary to store prompt objects, keyed by their unique identifiers.
            _collections (Dict[str, Collection]): A dictionary to store collection objects, keyed by their unique identifiers.

        Usage example:
            obj = YourClassName()
            prompt_obj = Prompt()
            obj._prompts['prompt_key'] = prompt_obj

            collection_obj = Collection()
            obj._collections['collection_key'] = collection_obj
        """
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
    
    # ============== Prompt Operations ==============
    
    def create_prompt(self, prompt: Prompt) -> Prompt:
        """Adds a new prompt to the storage.

        This function takes a `Prompt` object and adds it to the internal storage
        using the prompt's unique identifier. It returns the stored `Prompt` object.

        Args:
            prompt (Prompt): The `Prompt` object to be added to storage.

        Returns:
            Prompt: The `Prompt` object that was added to storage.

        Usage examples:
            prompt_instance = Prompt(id="123", text="Example prompt")
            stored_prompt = storage_instance.create_prompt(prompt_instance)
        """
        self._prompts[prompt.id] = prompt
        return prompt
    
    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """Retrieves a prompt from storage by its unique identifier.

        Args:
            prompt_id (str): The unique identifier of the prompt to retrieve.

        Returns:
            Optional[Prompt]: The Prompt object if found, otherwise None.

        Example:
            storage = Storage()  # Assuming Storage is the class containing this method
            prompt = storage.get_prompt("12345")
            if prompt:
                print("Prompt found:", prompt.text)
            else:
                print("Prompt not found.")
        """
        return self._prompts.get(prompt_id)
    
    def get_all_prompts(self) -> List[Prompt]:
        """Retrieves all stored prompts as a list.

        This method collects all the prompts stored within the instance and
        returns them in a list format. It accesses the internal dictionary
        `_prompts`, which is presumed to map prompt identifiers to Prompt
        objects, and converts its values to a list.

        Returns:
            List[Prompt]: A list containing all Prompt objects stored within the instance.

        Usage example:
            storage = YourStorageClass()
            all_prompts = storage.get_all_prompts()
            for prompt in all_prompts:
                print(prompt)
        """
        return list(self._prompts.values())
    
    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        """Updates an existing prompt with the given prompt data.

        This method updates the prompt identified by `prompt_id` with new information
        provided in the `prompt` parameter. If the `prompt_id` does not exist in the
        storage, the method returns None.

        Args:
            prompt_id (str): The unique identifier for the prompt to update.
            prompt (Prompt): The new prompt data to replace the existing prompt.

        Returns:
            Optional[Prompt]: The updated prompt if the `prompt_id` exists, otherwise None.

        Usage examples:
            >>> storage = Storage()
            >>> existing_prompt = storage.update_prompt("123", new_prompt)
            >>> if existing_prompt:
            ...     print("Prompt updated successfully.")
            ... else:
            ...     print("Prompt ID does not exist.")
        """
        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        return prompt
    
    def delete_prompt(self, prompt_id: str) -> bool:
        """Deletes a prompt from the storage by its ID.

        This method checks if a prompt with the given ID exists in the storage.
        If the prompt exists, it is deleted, and the method returns True.
        If the prompt does not exist, the method returns False.

        Args:
            prompt_id (str): The unique identifier of the prompt to be deleted.
        Returns:
            bool: True if the prompt was successfully deleted, False otherwise.

        Examples:
            >>> storage = PromptStorage()
            >>> storage.add_prompt("123", "Sample prompt text")
            >>> storage.delete_prompt("123")
            True
            >>> storage.delete_prompt("456")
            False
        """
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            return True
        return False
    
    # ============== Collection Operations ==============
    
    def create_collection(self, collection: Collection) -> Collection:
        """Creates and stores a collection within the storage system.

        This method takes a `Collection` object, assigns it to the storage
        dictionary using its `id` as the key, and then returns the collection.

        Args:
            collection (Collection): The collection object to be stored. It must
                have a unique `id` property which will be used as the storage key.

        Returns:
            Collection: The same collection object that was input, confirming that
            it has been successfully stored.

        Usage Example:
            collection = Collection(id='123', name='Sample Collection', data=[])
            storage = Storage()
            stored_collection = storage.create_collection(collection)
            assert stored_collection.id == '123'
        """
        self._collections[collection.id] = collection
        return collection
    
    def get_collection(self, collection_id: str) -> Optional[Collection]:
        """Retrieve a collection by its ID.

        This method fetches a collection from the internal store using the provided
        collection ID. If the collection ID exists, it returns the corresponding
        `Collection` object; otherwise, it returns `None`.

        Args:
            collection_id (str): The unique identifier for the collection to retrieve.

        Returns:
            Optional[Collection]: The collection object if found, otherwise `None`.

        Usage example:
            collection = storage_instance.get_collection("collection123")
            if collection:
                print("Collection found:", collection)
            else:
                print("Collection not found.")
        """
        return self._collections.get(collection_id)
    
    def get_all_collections(self) -> List[Collection]:
        """Retrieve all collections stored in the system.

        This method compiles all collections currently stored within the instance
        and returns them as a list. It accesses the internal dictionary `_collections`,
        which maps collection identifiers to `Collection` objects, and converts its
        values to a list format.

        Returns:
            List[Collection]: A list containing all `Collection` objects stored
            within the instance.

        Usage example:
            storage = Storage()
            all_collections = storage.get_all_collections()
            for collection in all_collections:
                print(collection.name, collection.id)
        """
        return list(self._collections.values())
    
    def delete_collection(self, collection_id: str) -> bool:
        """Deletes a collection by its ID.

        Args:
            collection_id (str): The ID of the collection to delete.
        Returns:
            bool: True if the collection was successfully deleted, False if the collection was not found.

        Usage Example:
            storage = Storage()
            success = storage.delete_collection("12345")
            if success:
                print("Collection was deleted successfully.")
            else:
                print("Collection not found.")
        """
        if collection_id in self._collections:
            del self._collections[collection_id]
            return True
        return False
    
    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        """Retrieve prompts associated with a specific collection.

        This method filters and returns a list of prompts that belong to the given
        collection identifier. It searches within the internally stored collection
        of prompts and extracts only those that match the provided collection ID.

        Args:
            collection_id (str): The unique identifier of the collection for which
                prompts are to be retrieved.

        Returns:
            List[Prompt]: A list of `Prompt` objects that belong to the specified
            collection. If no prompts are found for the collection ID, an empty list
            is returned.

        Usage Example:
            storage = Storage()
            prompts = storage.get_prompts_by_collection('collection_123')
            for prompt in prompts:
                print(prompt.name)
        """
        return [p for p in self._prompts.values() if p.collection_id == collection_id]
    
    # ============== Utility ==============
    
    def clear(self):
        """Clears all stored prompts and collections.

        This method is used to empty the current storage of all prompts and
        collections. It effectively resets the storage instance to its initial
        empty state.

        Usage example:
            storage = Storage()  # Initialize the storage instance
            storage.create_prompt(Prompt(id="1", text="Sample prompt"))
            storage.create_collection(Collection(id="1", name="Sample collection"))

            # Clear all stored data
            storage.clear()
            assert len(storage.get_all_prompts()) == 0  # True, as all prompts are cleared
            assert len(storage.get_all_collections()) == 0  # True, as all collections are cleared
        """
        self._prompts.clear()
        self._collections.clear()


# Global storage instance
storage = Storage()

