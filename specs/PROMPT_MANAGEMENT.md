# Feature Specification: Prompt Management

## 1. Overview

### Feature Name
Prompt Management (CRUD Operations)

### Description
Allow users to create, read, update, and delete AI prompt templates. Prompts are the core entity in PromptLab, containing template text with optional variables.

### Business Value
- Enable users to store and organize their AI prompts
- Provide a centralized repository for prompt templates
- Support reusability and standardization of prompts

### Use Cases
- **As a developer**, I want to create prompt templates so I can reuse them across projects
- **As a content writer**, I want to update existing prompts when I improve them
- **As a team lead**, I want to view all prompts in our system
- **As a user**, I want to delete outdated prompts to keep the system clean

---

## 2. Requirements

### Functional Requirements

**FR-1:** Create Prompt
- Users can create a new prompt with title, content, description, and optional collection
- System generates unique ID and timestamps automatically
- Title is required (1-200 characters)
- Content is required (minimum 1 character)
- Description is optional (max 500 characters)
- Collection ID is optional (must reference existing collection)

**FR-2:** Read Prompt
- Users can retrieve a single prompt by ID
- Users can retrieve all prompts
- System returns 404 if prompt doesn't exist
- Response includes all prompt fields

**FR-3:** Update Prompt (Full)
- Users can replace all prompt fields via PUT
- Unprovided fields fall back to existing values
- System updates the `updated_at` timestamp
- Validation rules apply (same as create)

**FR-4:** Update Prompt (Partial)
- Users can update specific fields via PATCH
- Only provided fields are modified
- System updates the `updated_at` timestamp
- Validation rules apply to provided fields only

**FR-5:** Delete Prompt
- Users can permanently delete a prompt by ID
- System returns 404 if prompt doesn't exist
- Deletion is immediate and irreversible
- No cascade effects (collections remain intact)

### Non-Functional Requirements

**NFR-1: Performance**
- Create operation: < 100ms
- Read operation: < 50ms
- Update operation: < 100ms
- Delete operation: < 50ms

**NFR-2: Reliability**
- 99.9% uptime for API
- Data consistency guaranteed
- Proper error handling

**NFR-3: Usability**
- Clear error messages
- RESTful API design
- Auto-generated API documentation

### User Stories

```
Story 1: Create a Prompt
As a developer
I want to create a new prompt template
So that I can reuse it in my applications

Acceptance Criteria:
- I can POST to /prompts with title and content
- System generates ID and timestamps
- I receive 201 Created with the new prompt
- Invalid data returns 422 with error details
```

```
Story 2: View My Prompts
As a user
I want to see all my prompts
So that I can find the one I need

Acceptance Criteria:
- I can GET /prompts to see all prompts
- Prompts are sorted newest first
- Each prompt includes all fields
- Response includes total count
```

```
Story 3: Update a Prompt
As a content writer
I want to update an existing prompt
So that I can improve it over time

Acceptance Criteria:
- I can PUT /prompts/{id} to replace all fields
- I can PATCH /prompts/{id} to update specific fields
- updated_at timestamp is refreshed
- Non-existent prompts return 404
```

```
Story 4: Delete a Prompt
As a user
I want to delete outdated prompts
So that my workspace stays clean

Acceptance Criteria:
- I can DELETE /prompts/{id}
- System returns 204 No Content
- Prompt is permanently removed
- Non-existent prompts return 404
```

---

## 3. Technical Design

### API Endpoints

#### Create Prompt
```
POST /prompts
Content-Type: application/json

Request Body:
{
  "title": "Email Template",
  "content": "Hello {{name}}, regarding {{subject}}...",
  "description": "Generic email template",
  "collection_id": "uuid-string"  // optional
}

Response: 201 Created
{
  "id": "generated-uuid",
  "title": "Email Template",
  "content": "Hello {{name}}, regarding {{subject}}...",
  "description": "Generic email template",
  "collection_id": "uuid-string",
  "created_at": "2026-02-20T10:30:00Z",
  "updated_at": "2026-02-20T10:30:00Z"
}
```

#### Get Prompt
```
GET /prompts/{prompt_id}

Response: 200 OK
{
  "id": "prompt-uuid",
  "title": "Email Template",
  ...
}

Error: 404 Not Found
{
  "detail": "Prompt not found"
}
```

#### List Prompts
```
GET /prompts

Response: 200 OK
{
  "prompts": [...],
  "total": 10
}
```

#### Update Prompt (Full)
```
PUT /prompts/{prompt_id}
Content-Type: application/json

Request Body:
{
  "title": "Updated Title",
  "content": "Updated content",
  "description": "Updated description",
  "collection_id": "new-collection-id"
}

Response: 200 OK
{
  "id": "same-id",
  "updated_at": "2026-02-22T15:45:00Z",  // Updated!
  ...
}
```

#### Update Prompt (Partial)
```
PATCH /prompts/{prompt_id}
Content-Type: application/json

Request Body:
{
  "title": "New Title Only"
}

Response: 200 OK
{
  "id": "same-id",
  "title": "New Title Only",  // Updated
  "content": "original content",  // Unchanged
  "updated_at": "2026-02-22T15:45:00Z",  // Updated!
  ...
}
```

#### Delete Prompt
```
DELETE /prompts/{prompt_id}

Response: 204 No Content
```

### Data Models

```python
class PromptBase(BaseModel):
    """Base prompt fields."""
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None

class PromptCreate(PromptBase):
    """Data for creating a prompt."""
    pass

class PromptUpdate(BaseModel):
    """Data for updating a prompt (all optional)."""
    title: Optional[str] = None
    content: Optional[str] = None
    description: Optional[str] = None
    collection_id: Optional[str] = None

class Prompt(PromptBase):
    """Full prompt with generated fields."""
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)
```

### Implementation Details

**Storage Layer:**
- In-memory dictionary: `{prompt_id: Prompt}`
- O(1) lookups by ID
- Returns None if not found

**Validation:**
- Pydantic handles all validation automatically
- Custom validation for collection_id (must exist)
- Timestamps generated/updated by system

**Error Handling:**
- 404: Prompt not found
- 400: Invalid collection_id
- 422: Validation errors

---

## 4. Acceptance Criteria

### Definition of Done

- [ ] All endpoints implemented
- [ ] Input validation working
- [ ] Error handling complete
- [ ] Tests passing (80%+ coverage)
- [ ] Documentation updated
- [ ] Code reviewed

### Test Scenarios

**Test 1: Create Valid Prompt**
```python
def test_create_prompt():
    response = POST /prompts {
        "title": "Test",
        "content": "Hello {{name}}"
    }
    assert response.status_code == 201
    assert response.json()["id"] is not None
    assert response.json()["created_at"] is not None
```

**Test 2: Create with Invalid Collection**
```python
def test_create_prompt_invalid_collection():
    response = POST /prompts {
        "title": "Test",
        "content": "Hello",
        "collection_id": "non-existent"
    }
    assert response.status_code == 400
    assert "Collection not found" in response.json()["detail"]
```

**Test 3: Get Non-Existent Prompt**
```python
def test_get_nonexistent_prompt():
    response = GET /prompts/fake-id
    assert response.status_code == 404
```

**Test 4: Update Updates Timestamp**
```python
def test_update_refreshes_timestamp():
    # Create prompt
    create_response = POST /prompts {...}
    original_updated_at = create_response.json()["updated_at"]
    
    # Wait and update
    time.sleep(0.1)
    update_response = PUT /prompts/{id} {...}
    new_updated_at = update_response.json()["updated_at"]
    
    assert new_updated_at > original_updated_at
```

**Test 5: PATCH Only Updates Provided Fields**
```python
def test_patch_partial_update():
    # Create prompt
    create_response = POST /prompts {
        "title": "Original",
        "content": "Original content"
    }
    
    # Update only title
    patch_response = PATCH /prompts/{id} {
        "title": "New Title"
    }
    
    assert patch_response.json()["title"] == "New Title"
    assert patch_response.json()["content"] == "Original content"
```

**Test 6: Delete Prompt**
```python
def test_delete_prompt():
    # Create prompt
    create_response = POST /prompts {...}
    prompt_id = create_response.json()["id"]
    
    # Delete it
    delete_response = DELETE /prompts/{prompt_id}
    assert delete_response.status_code == 204
    
    # Verify it's gone
    get_response = GET /prompts/{prompt_id}
    assert get_response.status_code == 404
```

---

## 5. Dependencies

### Prerequisites
- FastAPI framework installed
- Pydantic models defined
- Storage layer implemented

### Related Features
- **Collection Management:** Referenced by `collection_id`
- **Search and Filter:** Uses prompts as data source
- **Prompt Versioning (Future):** Will extend this feature

---

## 6. Future Enhancements

### Version 0.2.0
- **Soft Delete:** Mark prompts as deleted instead of removing
- **Audit Trail:** Track who created/updated each prompt
- **Bulk Operations:** Create/update/delete multiple prompts at once

### Version 0.3.0
- **Prompt Templates:** Predefined templates for common use cases
- **Validation Rules:** Custom validation for prompt content
- **Rich Text Support:** Markdown formatting in descriptions

### Version 0.4.0
- **Prompt Versioning:** Full version history with rollback
- **Collaboration:** Comments and discussions on prompts
- **Analytics:** Track usage and popularity of prompts

---

## Change Log

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-02-22 | Initial specification | Team |
| 1.1 | 2026-02-22 | Added PATCH endpoint spec | Team |

---

## Approval

- [ ] Product Owner
- [ ] Tech Lead
- [ ] Engineering Team
- [ ] QA Lead
