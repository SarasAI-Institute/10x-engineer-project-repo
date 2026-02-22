# Feature Specification: Search and Filter

## 1. Overview

### Feature Name
Search and Filter Prompts

### Description
Enable users to find prompts quickly using text search and collection-based filtering. Supports searching across prompt titles and descriptions, and filtering by collection membership.

### Business Value
- Reduce time to find relevant prompts
- Improve user productivity
- Enable discovery of existing prompts (reduce duplication)
- Support large prompt libraries (100+ prompts)

### Use Cases
- **As a user**, I want to search for prompts by keyword so I can find what I need quickly
- **As a team member**, I want to filter prompts by collection so I can see only relevant prompts
- **As a developer**, I want to combine search and filters to narrow down results efficiently

---

## 2. Requirements

### Functional Requirements

**FR-1: Text Search**
- Users can search prompts by providing a query string
- Search matches against:
  - Prompt title (case-insensitive)
  - Prompt description (case-insensitive)
- Search uses substring matching (contains)
- Empty search returns all prompts

**FR-2: Collection Filter**
- Users can filter prompts by collection ID
- Only prompts with matching collection_id are returned
- Invalid collection_id returns empty results (not an error)
- Null collection_id filters orphaned prompts

**FR-3: Combined Filters**
- Users can combine search and collection filters
- Filters are applied as AND conditions
- Results are sorted newest first

**FR-4: Case Insensitivity**
- Search is case-insensitive
- "email" matches "Email", "EMAIL", "EmAiL"

**FR-5: Sorting**
- All results are sorted by created_at descending (newest first)
- Sorting is consistent across all filter combinations

### Non-Functional Requirements

**NFR-1: Performance**
- Search/filter operation: < 100ms for 1000 prompts
- Linear search is acceptable for in-memory implementation
- Future: Index-based search for 10,000+ prompts

**NFR-2: Usability**
- Simple query string parameters
- Intuitive, predictable behavior
- Works with GET request (no POST body)

**NFR-3: Scalability**
- Future: Support pagination (limit/offset)
- Future: Support advanced search (regex, tags)
- Future: Support sorting options (by date, by title, by relevance)

### User Stories

```
Story 1: Search by Keyword
As a user
I want to search prompts by keyword
So that I can quickly find relevant templates

Acceptance Criteria:
- I can add ?search=keyword to /prompts
- Results include prompts with keyword in title or description
- Search is case-insensitive
- Results are sorted newest first
```

```
Story 2: Filter by Collection
As a user
I want to filter prompts by collection
So that I can see only prompts from a specific project

Acceptance Criteria:
- I can add ?collection_id=uuid to /prompts
- Only prompts in that collection are returned
- Invalid collection_id returns empty list (not error)
- Results are sorted newest first
```

```
Story 3: Combined Search and Filter
As a power user
I want to search within a specific collection
So that I can find prompts more precisely

Acceptance Criteria:
- I can use ?collection_id=uuid&search=keyword
- Results match both conditions (AND logic)
- Still sorted newest first
```

---

## 3. Technical Design

### API Endpoints

#### Search Prompts
```
GET /prompts?search=email

Response: 200 OK
{
  "prompts": [
    {
      "id": "uuid-1",
      "title": "Email Template",  // Matches!
      "content": "...",
      ...
    },
    {
      "id": "uuid-2",
      "title": "Contact Form",
      "description": "Send email notifications",  // Matches!
      ...
    }
  ],
  "total": 2
}
```

#### Filter by Collection
```
GET /prompts?collection_id=marketing-uuid

Response: 200 OK
{
  "prompts": [
    // Only prompts with collection_id = marketing-uuid
  ],
  "total": 5
}
```

#### Combined Search and Filter
```
GET /prompts?collection_id=marketing-uuid&search=campaign

Response: 200 OK
{
  "prompts": [
    // Prompts in marketing collection with "campaign" in title/description
  ],
  "total": 3
}
```

#### Edge Cases

**No Results:**
```
GET /prompts?search=nonexistent

Response: 200 OK
{
  "prompts": [],
  "total": 0
}
```

**Invalid Collection ID:**
```
GET /prompts?collection_id=fake-uuid

Response: 200 OK
{
  "prompts": [],
  "total": 0
}
```

**No Parameters (All Prompts):**
```
GET /prompts

Response: 200 OK
{
  "prompts": [...],  // All prompts, newest first
  "total": 20
}
```

### Implementation Details

**Query Parameter Parsing:**
```python
@app.get("/prompts", response_model=PromptList)
def list_prompts(
    collection_id: Optional[str] = None,
    search: Optional[str] = None
):
    prompts = storage.get_all_prompts()
    
    # Apply filters
    if collection_id:
        prompts = filter_prompts_by_collection(prompts, collection_id)
    
    if search:
        prompts = search_prompts(prompts, search)
    
    # Sort
    prompts = sort_prompts_by_date(prompts, descending=True)
    
    return PromptList(prompts=prompts, total=len(prompts))
```

**Search Implementation:**
```python
def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
    """Search prompts by title or description."""
    query_lower = query.lower()
    return [
        p for p in prompts 
        if query_lower in p.title.lower() or 
           (p.description and query_lower in p.description.lower())
    ]
```

**Filter Implementation:**
```python
def filter_prompts_by_collection(
    prompts: List[Prompt], 
    collection_id: str
) -> List[Prompt]:
    """Filter prompts by collection ID."""
    return [p for p in prompts if p.collection_id == collection_id]
```

**Sort Implementation:**
```python
def sort_prompts_by_date(
    prompts: List[Prompt], 
    descending: bool = True
) -> List[Prompt]:
    """Sort prompts by creation date."""
    return sorted(prompts, key=lambda p: p.created_at, reverse=descending)
```

---

## 4. Acceptance Criteria

### Definition of Done

- [ ] Search parameter works correctly
- [ ] Collection filter works correctly
- [ ] Filters can be combined
- [ ] Results are sorted newest first
- [ ] Case-insensitive search
- [ ] Tests passing (80%+ coverage)
- [ ] Documentation updated

### Test Scenarios

**Test 1: Search by Title**
```python
def test_search_by_title():
    # Create prompts
    POST /prompts {"title": "Email Template", "content": "..."}
    POST /prompts {"title": "SMS Template", "content": "..."}
    
    # Search
    response = GET /prompts?search=email
    assert response.json()["total"] == 1
    assert response.json()["prompts"][0]["title"] == "Email Template"
```

**Test 2: Search by Description**
```python
def test_search_by_description():
    # Create prompt
    POST /prompts {
        "title": "Template",
        "content": "...",
        "description": "For email campaigns"
    }
    
    # Search
    response = GET /prompts?search=email
    assert response.json()["total"] == 1
```

**Test 3: Case Insensitive Search**
```python
def test_search_case_insensitive():
    POST /prompts {"title": "Email Template", "content": "..."}
    
    response1 = GET /prompts?search=EMAIL
    response2 = GET /prompts?search=email
    response3 = GET /prompts?search=EmAiL
    
    assert response1.json()["total"] == 1
    assert response2.json()["total"] == 1
    assert response3.json()["total"] == 1
```

**Test 4: Filter by Collection**
```python
def test_filter_by_collection():
    # Create collection and prompts
    collection = POST /collections {"name": "Marketing"}
    collection_id = collection.json()["id"]
    
    POST /prompts {"title": "P1", "content": "...", "collection_id": collection_id}
    POST /prompts {"title": "P2", "content": "...", "collection_id": collection_id}
    POST /prompts {"title": "P3", "content": "..."}  // No collection
    
    # Filter
    response = GET /prompts?collection_id={collection_id}
    assert response.json()["total"] == 2
```

**Test 5: Combined Search and Filter**
```python
def test_combined_search_and_filter():
    # Create collection and prompts
    collection = POST /collections {"name": "Marketing"}
    cid = collection.json()["id"]
    
    POST /prompts {"title": "Email Campaign", "content": "...", "collection_id": cid}
    POST /prompts {"title": "SMS Campaign", "content": "...", "collection_id": cid}
    POST /prompts {"title": "Email Report", "content": "..."}  // Different collection
    
    # Search within collection
    response = GET /prompts?collection_id={cid}&search=email
    assert response.json()["total"] == 1
    assert response.json()["prompts"][0]["title"] == "Email Campaign"
```

**Test 6: Results Sorted Newest First**
```python
def test_results_sorted_newest_first():
    # Create prompts with delay
    p1 = POST /prompts {"title": "First", "content": "..."}
    time.sleep(0.1)
    p2 = POST /prompts {"title": "Second", "content": "..."}
    time.sleep(0.1)
    p3 = POST /prompts {"title": "Third", "content": "..."}
    
    # List all
    response = GET /prompts
    prompts = response.json()["prompts"]
    
    assert prompts[0]["title"] == "Third"   // Newest
    assert prompts[1]["title"] == "Second"
    assert prompts[2]["title"] == "First"   // Oldest
```

**Test 7: No Results**
```python
def test_search_no_results():
    POST /prompts {"title": "Test", "content": "..."}
    
    response = GET /prompts?search=nonexistent
    assert response.status_code == 200
    assert response.json()["total"] == 0
    assert response.json()["prompts"] == []
```

---

## 5. Dependencies

### Prerequisites
- Prompt management feature
- Collection management feature
- Utility functions (utils.py)

### Related Features
- **Pagination:** Future enhancement for large result sets
- **Advanced Search:** Tags, regex, date ranges
- **Prompt Tagging:** Additional filter dimension

---

## 6. Future Enhancements

### Version 0.2.0: Pagination
```
GET /prompts?limit=20&offset=40

Response:
{
  "prompts": [...],  // 20 items
  "total": 150,      // Total matching items
  "limit": 20,
  "offset": 40,
  "has_more": true
}
```

### Version 0.3.0: Advanced Search

**Tag-based Filtering:**
```
GET /prompts?tags=newsletter,automation
```

**Date Range Filtering:**
```
GET /prompts?created_after=2026-01-01&created_before=2026-02-01
```

**Regex Search:**
```
GET /prompts?search_regex=email.*template
```

**Full-Text Search:**
```
GET /prompts?q=email+template&search_mode=fulltext
```

### Version 0.4.0: Sorting Options

```
GET /prompts?sort_by=title&order=asc
GET /prompts?sort_by=updated_at&order=desc
GET /prompts?sort_by=relevance  // With search query
```

### Version 0.5.0: Saved Searches

```
POST /saved-searches
{
  "name": "My Marketing Emails",
  "filters": {
    "collection_id": "marketing-uuid",
    "search": "email"
  }
}

GET /saved-searches/{id}/execute
```

---

## Performance Optimization

### Current Implementation
- **Time Complexity:** O(n) where n = number of prompts
- **Space Complexity:** O(n) for result list
- **Acceptable for:** < 10,000 prompts

### Future Optimizations

**1. Database Indexes:**
```sql
CREATE INDEX idx_prompts_title ON prompts(title);
CREATE INDEX idx_prompts_collection ON prompts(collection_id);
CREATE INDEX idx_prompts_created ON prompts(created_at DESC);
```

**2. Full-Text Search:**
```sql
CREATE INDEX idx_prompts_fts ON prompts 
USING GIN (to_tsvector('english', title || ' ' || description));
```

**3. Caching:**
- Cache popular search queries (Redis)
- Cache collection filter results
- Invalidate on prompt create/update/delete

**4. Elasticsearch Integration:**
- Index all prompts in Elasticsearch
- Sub-second search for millions of prompts
- Advanced features: fuzzy search, highlighting, relevance scoring

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
