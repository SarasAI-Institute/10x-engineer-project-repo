# Feature Specification: Collection Management

## 1. Overview

### Feature Name
Collection Management (CRUD Operations)

### Description
Collections are containers for organizing related prompts. Users can group prompts by category, project, or any logical grouping to maintain an organized prompt library.

### Business Value
- Enable logical organization of prompts
- Improve prompt discoverability
- Support team collaboration through shared collections
- Facilitate project-based prompt management

### Use Cases
- **As a developer**, I want to organize prompts by project so I can find them easily
- **As a team**, we want to create shared collections for different use cases (marketing, support, etc.)
- **As a manager**, I want to view all collections to understand our prompt organization
- **As a user**, I want to delete obsolete collections when projects end

---

## 2. Requirements

### Functional Requirements

**FR-1: Create Collection**
- Users can create a new collection with name and optional description
- Name is required (1-100 characters)
- Description is optional (max 500 characters)
- System generates unique ID and timestamp

**FR-2: Read Collection**
- Users can retrieve a single collection by ID
- Users can retrieve all collections
- System returns 404 if collection doesn't exist

**FR-3: List Collections**
- Users can view all collections
- Response includes collection count
- Collections include metadata (ID, name, description, created_at)

**FR-4: Delete Collection**
- Users can delete a collection by ID
- Prompts in deleted collections become orphaned (collection_id = null)
- Deletion is permanent and irreversible
- System returns 404 if collection doesn't exist

**FR-5: Collection-Prompt Relationship**
- One collection can contain many prompts
- One prompt can belong to zero or one collection
- Prompts can exist without a collection (orphaned)

### Non-Functional Requirements

**NFR-1: Performance**
- Create: < 50ms
- Read: < 50ms
- List: < 100ms
- Delete: < 100ms (including orphaning prompts)

**NFR-2: Data Integrity**
- Collection names must be unique (future enhancement)
- Deleting collection doesn't delete prompts
- Orphaned prompts remain accessible

**NFR-3: Usability**
- Clear naming conventions
- Descriptive error messages
- RESTful API design

### User Stories

```
Story 1: Create a Collection
As a team lead
I want to create a collection for my project
So that team members can find relevant prompts easily

Acceptance Criteria:
- I can POST to /collections with name and description
- System generates ID and timestamp
- I receive 201 Created with the new collection
- Invalid data returns 422 with validation errors
```

```
Story 2: View All Collections
As a user
I want to see all available collections
So that I can choose where to organize my prompts

Acceptance Criteria:
- I can GET /collections to see all collections
- Each collection shows name, description, and creation date
- Response includes total count
```

```
Story 3: Delete Old Collection
As a user
I want to delete a collection when a project ends
So that my workspace stays organized

Acceptance Criteria:
- I can DELETE /collections/{id}
- Prompts in the collection become orphaned (not deleted)
- I can still access the orphaned prompts
- System returns 204 No Content
```

---

## 3. Technical Design

### API Endpoints

#### Create Collection
```
POST /collections
Content-Type: application/json

Request Body:
{
  "name": "Marketing Prompts",
  "description": "All marketing-related prompt templates"
}

Response: 201 Created
{
  "id": "generated-uuid",
  "name": "Marketing Prompts",
  "description": "All marketing-related prompt templates",
  "created_at": "2026-02-22T10:00:00Z"
}
```

#### Get Collection
```
GET /collections/{collection_id}

Response: 200 OK
{
  "id": "collection-uuid",
  "name": "Marketing Prompts",
  "description": "All marketing-related prompt templates",
  "created_at": "2026-02-22T10:00:00Z"
}

Error: 404 Not Found
{
  "detail": "Collection not found"
}
```

#### List Collections
```
GET /collections

Response: 200 OK
{
  "collections": [
    {
      "id": "uuid-1",
      "name": "Marketing Prompts",
      "description": "Marketing templates",
      "created_at": "2026-02-22T10:00:00Z"
    },
    {
      "id": "uuid-2",
      "name": "Customer Support",
      "description": "Support response templates",
      "created_at": "2026-02-22T11:00:00Z"
    }
  ],
  "total": 2
}
```

#### Delete Collection
```
DELETE /collections/{collection_id}

Response: 204 No Content

Note: All prompts with this collection_id will have it set to null
```

### Data Models

```python
class CollectionBase(BaseModel):
    """Base collection fields."""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

class CollectionCreate(CollectionBase):
    """Data for creating a collection."""
    pass

class Collection(CollectionBase):
    """Full collection with generated fields."""
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)
```

### Implementation Details

**Storage Layer:**
- Separate dictionary: `{collection_id: Collection}`
- O(1) lookups by ID
- Returns None if not found

**Deletion Behavior:**
```python
def delete_collection(collection_id: str) -> bool:
    """Delete collection and orphan its prompts."""
    if collection_id in self._collections:
        # Remove the collection
        del self._collections[collection_id]
        
        # Orphan prompts (set collection_id to None)
        for prompt in self._prompts.values():
            if prompt.collection_id == collection_id:
                prompt.collection_id = None
        
        return True
    return False
```

**Future: Update Collection**
- Not implemented in v0.1.0
- Would allow renaming and updating description
- Will be added in v0.2.0

---

## 4. Acceptance Criteria

### Definition of Done

- [ ] All endpoints implemented
- [ ] Collections can be created and listed
- [ ] Collections can be deleted
- [ ] Deleting collection orphans prompts correctly
- [ ] Tests passing (80%+ coverage)
- [ ] Documentation updated

### Test Scenarios

**Test 1: Create Collection**
```python
def test_create_collection():
    response = POST /collections {
        "name": "Test Collection",
        "description": "Test description"
    }
    assert response.status_code == 201
    assert response.json()["id"] is not None
    assert response.json()["name"] == "Test Collection"
```

**Test 2: List Collections**
```python
def test_list_collections():
    # Create 2 collections
    POST /collections {"name": "Collection 1"}
    POST /collections {"name": "Collection 2"}
    
    # List them
    response = GET /collections
    assert response.status_code == 200
    assert response.json()["total"] == 2
    assert len(response.json()["collections"]) == 2
```

**Test 3: Get Collection by ID**
```python
def test_get_collection():
    # Create collection
    create_response = POST /collections {"name": "Test"}
    collection_id = create_response.json()["id"]
    
    # Get it
    get_response = GET /collections/{collection_id}
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Test"
```

**Test 4: Delete Collection Orphans Prompts**
```python
def test_delete_collection_orphans_prompts():
    # Create collection
    collection = POST /collections {"name": "Test"}
    collection_id = collection.json()["id"]
    
    # Create prompt in collection
    prompt = POST /prompts {
        "title": "Test",
        "content": "Content",
        "collection_id": collection_id
    }
    prompt_id = prompt.json()["id"]
    
    # Delete collection
    delete_response = DELETE /collections/{collection_id}
    assert delete_response.status_code == 204
    
    # Verify prompt still exists but is orphaned
    prompt_response = GET /prompts/{prompt_id}
    assert prompt_response.status_code == 200
    assert prompt_response.json()["collection_id"] is None
```

**Test 5: Delete Non-Existent Collection**
```python
def test_delete_nonexistent_collection():
    response = DELETE /collections/fake-id
    assert response.status_code == 404
```

**Test 6: Validation Errors**
```python
def test_create_collection_validation():
    # Empty name
    response = POST /collections {"name": ""}
    assert response.status_code == 422
    
    # Name too long
    response = POST /collections {"name": "x" * 101}
    assert response.status_code == 422
```

---

## 5. Dependencies

### Prerequisites
- FastAPI framework
- Pydantic models
- Storage layer
- Prompt management feature (for relationships)

### Related Features
- **Prompt Management:** Prompts reference collections
- **Search and Filter:** Can filter prompts by collection
- **Future: Nested Collections:** Collections could contain sub-collections

---

## 6. Future Enhancements

### Version 0.2.0
- **Update Collection:** PUT/PATCH endpoints to rename/update
- **Collection Stats:** Show prompt count per collection
- **Collection Colors:** Visual organization with color coding

### Version 0.3.0
- **Nested Collections:** Collections can contain sub-collections
- **Collection Permissions:** Control who can view/edit collections
- **Smart Collections:** Auto-organize based on rules (like tags)

### Version 0.4.0
- **Collection Templates:** Pre-defined collection structures
- **Collection Sharing:** Share collections with other users/teams
- **Collection Analytics:** Track usage and popular collections

### Potential Deletion Strategies

Currently, deleting a collection orphans prompts. Future versions could offer:

1. **Orphan (Current):** Set collection_id to null
2. **Move to Default:** Move prompts to "Uncategorized" collection
3. **Prevent if Not Empty:** Don't allow deletion if prompts exist
4. **Cascade Delete:** Delete all prompts in collection (dangerous!)

User could choose strategy via query parameter:
```
DELETE /collections/{id}?strategy=orphan  // Default
DELETE /collections/{id}?strategy=prevent
DELETE /collections/{id}?strategy=cascade  // Requires confirmation
```

---

## Change Log

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-02-22 | Initial specification | Team |

---

## Approval

- [ ] Product Owner
- [ ] Tech Lead
- [ ] Engineering Team
- [ ] QA Lead
