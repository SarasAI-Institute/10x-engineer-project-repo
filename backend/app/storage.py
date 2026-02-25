"""In-memory storage for PromptLab"""

from typing import Dict, List, Optional
from app.models import Prompt, Collection, Tag, PromptTag
from uuid import uuid4, UUID
from datetime import datetime


class Storage:
    def __init__(self):
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
        self.tags: Dict[UUID, Tag] = {}
        self.prompt_tags: Dict[UUID, PromptTag] = {}

    # ================= TAG OPERATIONS =================

    def create_tag(self, name: str, created_by: str) -> Tag:
        tag_id = uuid4()
        tag = Tag(
            id=tag_id,
            name=name,
            created_by=created_by,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.tags[tag_id] = tag
        return tag

    def get_tags(self) -> List[Tag]:
        return list(self.tags.values())

    def update_tag_name(self, tag_id: UUID, new_name: str) -> Tag:
        if tag_id not in self.tags:
            raise ValueError("Tag not found")

        if any(t.name.lower() == new_name.lower() for t in self.tags.values()):
            raise ValueError("Duplicate tag name")

        tag = self.tags[tag_id]
        tag.name = new_name
        tag.updated_at = datetime.utcnow()
        return tag

    def assign_tag_to_prompt(self, prompt_id: str, tag_id: UUID) -> PromptTag:
        if prompt_id not in self._prompts:
            raise ValueError("Prompt not found")

        if tag_id not in self.tags:
            raise ValueError("Tag not found")

        if any(
            pt.prompt_id == prompt_id and pt.tag_id == tag_id
            for pt in self.prompt_tags.values()
        ):
            raise ValueError("Tag already assigned to prompt")

        pt_id = uuid4()
        prompt_tag = PromptTag(
            id=pt_id,
            prompt_id=prompt_id,
            tag_id=tag_id,
            created_at=datetime.utcnow(),
        )

        self.prompt_tags[pt_id] = prompt_tag
        return prompt_tag

    def remove_tag_from_prompt(self, prompt_id: str, tag_id: UUID):
        for pt_id, pt in list(self.prompt_tags.items()):
            if pt.prompt_id == prompt_id and pt.tag_id == tag_id:
                del self.prompt_tags[pt_id]
                return pt

        raise ValueError("Tag not assigned to prompt")

    # ================= PROMPT OPERATIONS =================

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
        self._prompts[prompt_id] = prompt
        return prompt

    def delete_prompt(self, prompt_id: str) -> bool:
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            return True
        return False

    # ================= COLLECTION OPERATIONS =================

    def create_collection(self, collection: Collection) -> Collection:
        self._collections[collection.id] = collection
        return collection

    def get_collection(self, collection_id: str) -> Optional[Collection]:
        return self._collections.get(collection_id)

    def get_all_collections(self) -> List[Collection]:
        return list(self._collections.values())

    def delete_collection(self, collection_id: str) -> bool:
        if collection_id in self._collections:
            del self._collections[collection_id]
            return True
        return False

    # ================= UTILITY =================

    def clear(self):
        self._prompts.clear()
        self._collections.clear()
        self.tags.clear()
        self.prompt_tags.clear()

    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        return [p for p in self._prompts.values() if p.collection_id == collection_id]


# Global instance
storage = Storage()