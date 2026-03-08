"""In-memory storage for PromptLab"""

from typing import Optional
from app.models import Prompt, Collection, Tag, PromptTag, get_current_time
from uuid import uuid4, UUID


class Storage:
    def __init__(self):
        self._prompts: dict[str, Prompt] = {}
        self._collections: dict[str, Collection] = {}
        self._tags: dict[UUID, Tag] = {}
        self._prompt_tags: dict[UUID, PromptTag] = {}

    # ================= TAG OPERATIONS =================

    def create_tag(self, name: str, created_by: str) -> Tag:
        """Create a new tag and add it to the storage.

        Args:
            name (str): The name of the tag to be created.
            created_by (str): The identifier for the user who created the tag.

        Returns:
            Tag: The newly created tag object, including id, name, created_by, created_at, and updated_at fields.

        Example usage:
            >>> storage.create_tag("Urgent", "admin")
            Tag(id=UUID('...'), name='Urgent', created_by='admin', created_at=datetime(...), updated_at=datetime(...))
        """
        tag_id = uuid4()
        tag = Tag(
            id=tag_id,
            name=name,
            created_by=created_by,
            created_at=get_current_time(),
            updated_at=get_current_time(),
        )
        self._tags[tag_id] = tag
        return tag

    def get_tags(self) -> list[Tag]:
        return list(self._tags.values())

    def update_tag_name(self, tag_id: UUID, new_name: str) -> Tag:
        """Update the name of an existing tag identified by `tag_id`.

        Args:
            tag_id (UUID): The unique identifier of the tag to update.
            new_name (str): The new name for the tag.

        Returns:
            Tag: The updated tag object with the new name and updated timestamp.

        Raises:
            ValueError: If the tag is not found or if the new name already exists for another tag.

        Example usage:
            >>> storage.update_tag_name(UUID('...'), "New Tag Name")
            Tag(id=UUID('...'), name='New Tag Name', created_by='user1', created_at=datetime(...), updated_at=datetime(...))
        """
        if tag_id not in self._tags:
            raise ValueError("Tag not found")

        if any(t.name.lower() == new_name.lower() for t in self._tags.values()):
            raise ValueError("Duplicate tag name")

        tag = self._tags[tag_id]
        tag.name = new_name
        tag.updated_at = get_current_time()
        return tag

    def _validate_tag_assignment(self, prompt_id: str, tag_id: UUID) -> None:
        if prompt_id not in self._prompts:
            raise ValueError("Prompt not found")
        if tag_id not in self._tags:
            raise ValueError("Tag not found")
        if any(
            pt.prompt_id == prompt_id and pt.tag_id == tag_id
            for pt in self._prompt_tags.values()
        ):
            raise ValueError("Tag already assigned to prompt")

    def assign_tag_to_prompt(self, prompt_id: str, tag_id: UUID) -> PromptTag:
        """Assign a tag to a prompt using their IDs.

        Args:
            prompt_id (str): The ID of the prompt to which the tag will be assigned.
            tag_id (UUID): The ID of the tag to assign to the prompt.

        Returns:
            PromptTag: The newly created association between the prompt and the tag.

        Raises:
            ValueError: If the prompt or tag is not found, or if the tag is already assigned to the prompt.

        Example usage:
            >>> storage.assign_tag_to_prompt("prompt1", UUID('...'))
            PromptTag(id=UUID('...'), prompt_id='prompt1', tag_id=UUID('...'), created_at=datetime(...))
        """
        self._validate_tag_assignment(prompt_id, tag_id)

        prompt_tag_id = uuid4()
        prompt_tag = PromptTag(
            id=prompt_tag_id,
            prompt_id=prompt_id,
            tag_id=tag_id,
            created_at=get_current_time(),
        )

        self._prompt_tags[prompt_tag_id] = prompt_tag
        return prompt_tag

    def remove_tag_from_prompt(self, prompt_id: str, tag_id: UUID) -> PromptTag:
        """Remove a tag from a specific prompt by their IDs.

        Args:
            prompt_id (str): The ID of the prompt from which the tag will be removed.
            tag_id (UUID): The ID of the tag to remove from the prompt.

        Returns:
            PromptTag: The removed tag association.

        Raises:
            ValueError: If the tag is not assigned to the given prompt.

        Example usage:
            >>> storage.remove_tag_from_prompt("prompt1", UUID('...'))
            PromptTag(id=UUID('...'), prompt_id='prompt1', tag_id=UUID('...'), created_at=datetime(...))
        """
        # Iterate over the dictionary items to find the matching prompt and tag IDs
        for prompt_tag_id, prompt_tag in list(self._prompt_tags.items()):
            if prompt_tag.prompt_id == prompt_id and prompt_tag.tag_id == tag_id:
                del self._prompt_tags[prompt_tag_id]
                return prompt_tag

        # Raise an error if the tag is not found for the given prompt
        raise ValueError("Tag not assigned to prompt")

    # ================= PROMPT OPERATIONS =================

    def create_prompt(self, prompt: Prompt) -> Prompt:
        """Create a new prompt and add it to the storage.

        Args:
            prompt (Prompt): The prompt object containing all necessary details to be stored.
        Returns:
            Prompt: The newly created prompt object.

        Example usage:
            >>> storage.create_prompt(Prompt(id='prompt1', title='New Prompt', ...))
            Prompt(id='prompt1', title='New Prompt', ...)
        """
        self._prompts[prompt.id] = prompt
        return prompt

    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """Retrieve a specific prompt by its ID.

        Args:
            prompt_id (str): The ID of the prompt to retrieve.

        Returns:
            Optional[Prompt]: The prompt with the specified ID, or None if it does not exist.

        Example usage:
            >>> storage.get_prompt('prompt1')
            Prompt(id='prompt1', title='Sample Prompt', ...)
        """
        # Return the prompt associated with the given prompt_id
        return self._prompts.get(prompt_id)

    def get_all_prompts(self) -> list[Prompt]:
        """Retrieve all prompts stored in the system.

        Returns:
            list[Prompt]: A list of all prompt objects currently stored.

        Example usage:
            >>> storage.get_all_prompts()
            [Prompt(id='prompt1', title='Sample Prompt', ...), Prompt(id='prompt2', title='Another Prompt', ...), ...]
        """
        return list(self._prompts.values())

    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        """Update an existing prompt with new details.

        Args:
            prompt_id (str): The ID of the prompt to update.
            prompt (Prompt): The prompt object containing updated details.

        Returns:
            Optional[Prompt]: The updated prompt object if it exists; otherwise, None.

        Example usage:
            >>> storage.update_prompt('prompt1', Prompt(id='prompt1', title='Updated Title', ...))
            Prompt(id='prompt1', title='Updated Title', ...)
        """
        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        return prompt

    def delete_prompt(self, prompt_id: str) -> bool:
        """Delete a prompt by its ID.

        Args:
            prompt_id (str): The ID of the prompt to delete.
        Returns:
            bool: True if the prompt was successfully deleted, False if the prompt did not exist.

        Example usage:
            >>> storage.delete_prompt('prompt1')
            True
        """
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            return True
        return False

    # ================= COLLECTION OPERATIONS =================

    def create_collection(self, collection: Collection) -> Collection:
        """Create a new collection and add it to the storage.

        Args:
            collection (Collection): The collection object containing all necessary details to be stored.

        Returns:
            Collection: The newly created collection object.

        Example usage:
            >>> storage.create_collection(Collection(id='collection1', name='New Collection', ...))
            Collection(id='collection1', name='New Collection', ...)
        """
        self._collections[collection.id] = collection
        return collection

    def get_collection(self, collection_id: str) -> Optional[Collection]:
        """Retrieve a specific collection by its ID.

        Args:
            collection_id (str): The ID of the collection to retrieve.

        Returns:
            Optional[Collection]: The collection with the specified ID, or None if it does not exist.

        Example usage:
            >>> storage.get_collection('collection1')
            Collection(id='collection1', name='Sample Collection', ...)
        """
        return self._collections.get(collection_id)

    def get_all_collections(self) -> list[Collection]:
        """Retrieve all collections stored in the system.

        Returns:
            list[Collection]: A list of all collection objects currently stored.

        Example usage:
            >>> storage.get_all_collections()
            [Collection(id='collection1', name='Collection One', ...), Collection(id='collection2', name='Collection Two', ...), ...]
        """
        return list(self._collections.values())

    def delete_collection(self, collection_id: str) -> bool:
        """Delete a collection by its ID.

        Args:
            collection_id (str): The ID of the collection to delete.
        Returns:
            bool: True if the collection was successfully deleted, False if the collection did not exist.

        Example usage:
            >>> storage.delete_collection('collection1')
            True
        """
        if collection_id in self._collections:
            del self._collections[collection_id]
            return True
        return False

    # ================= UTILITY =================

    def clear(self):
        """Clear all data from prompts, collections, tags, and prompt-tag associations.

        Args:
            None

        Returns:
            None

        Example usage:
            >>> storage.clear()
        """
        self._prompts.clear()
        self._collections.clear()
        self._tags.clear()
        self._prompt_tags.clear()

    def get_prompts_by_collection(self, collection_id: str) -> list[Prompt]:
        """Retrieve all prompts associated with a specific collection ID.

        Args:
            collection_id (str): The ID of the collection to filter prompts.

        Returns:
            list[Prompt]: A list of prompts associated with the specified collection ID.

        Example usage:
            >>> storage.get_prompts_by_collection('collection1')
            [Prompt(id='prompt1', title='Sample Prompt', collection_id='collection1', ...), ...]
        """
        return [p for p in self._prompts.values() if p.collection_id == collection_id]


# Global instance
storage = Storage()