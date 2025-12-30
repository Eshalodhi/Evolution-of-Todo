# Data Model: Console Todo Application - Phase I

**Feature**: 001-console-todo-app
**Level**: INTERMEDIATE (10 features)
**Date**: 2025-12-28
**Updated**: 2025-12-29
**Source**: [spec.md](./spec.md), [plan.md](./plan.md)

---

## Overview

The Console Todo Application uses a simple in-memory data model with a single entity: **Task**. All tasks are stored in a Python list of dictionaries, with no persistence between sessions.

**INTERMEDIATE Level**: Enhanced from 5 fields to 7 fields (added `priority` and `tags`).

---

## Entity: Task

### Definition

A Task represents a unit of work that the user wants to track, with priority level and optional tags for categorization.

### Schema

```python
Task = {
    "id": int,
    "title": str,
    "description": str,
    "completed": bool,
    "created_at": str,
    "priority": str,      # NEW in INTERMEDIATE
    "tags": list[str]     # NEW in INTERMEDIATE
}
```

### Field Specifications

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `id` | `int` | Yes | Auto-generated | Unique identifier for the task |
| `title` | `str` | Yes | - | User-provided title of the task |
| `description` | `str` | Yes | `""` | User-provided description (can be empty) |
| `completed` | `bool` | Yes | `False` | Whether the task is completed |
| `created_at` | `str` | Yes | Auto-generated | ISO 8601 timestamp when task was created |
| `priority` | `str` | Yes | `"medium"` | Priority level: high/medium/low |
| `tags` | `list[str]` | Yes | `[]` | List of tag strings |

### Field Constraints

#### id
- **Type**: Positive integer
- **Generation**: Auto-incremented using `max(existing_ids) + 1`
- **Uniqueness**: Must be unique within the session
- **Reuse**: Never reused, even after deletion
- **Default**: First task gets ID `1`

#### title
- **Type**: String
- **Length**: 1-100 characters (after whitespace trimming)
- **Trimming**: Leading and trailing whitespace is automatically removed
- **Content**: Any printable characters including Unicode
- **Validation**: Cannot be empty or whitespace-only

#### description
- **Type**: String
- **Length**: 0-500 characters (after whitespace trimming)
- **Default**: Empty string `""`
- **Content**: Any printable characters including Unicode
- **Validation**: Can be empty (optional field)

#### completed
- **Type**: Boolean
- **Valid Values**: `True` or `False`
- **Default**: `False` (set on creation)
- **Display**: `✓` (complete) or `○` (incomplete)

#### created_at
- **Type**: ISO 8601 formatted string
- **Format**: `"YYYY-MM-DDTHH:MM:SS"` (e.g., `"2025-12-29T10:30:00"`)
- **Generation**: Automatically set at task creation time
- **Mutability**: Never changes after creation

#### priority (NEW - INTERMEDIATE)
- **Type**: String literal
- **Valid Values**: `"high"`, `"medium"`, `"low"` only
- **Default**: `"medium"` (set on creation)
- **Case-insensitive Input**: User can enter "HIGH", "High", etc.
- **Normalized Storage**: Always stored in lowercase
- **Display Colors**:
  - `"high"` → Red (`\033[91m`)
  - `"medium"` → Yellow (`\033[93m`)
  - `"low"` → Green (`\033[92m`)

#### tags (NEW - INTERMEDIATE)
- **Type**: List of strings
- **Default**: Empty list `[]`
- **Maximum Tags**: Unlimited (but practical limit for display)
- **Tag Constraints**:
  - Length: 1-20 characters each
  - Characters: Alphanumeric and hyphens only (`[a-zA-Z0-9-]`)
  - No leading/trailing hyphens
  - No consecutive hyphens
  - Case-insensitive input, stored lowercase
  - No duplicates within a task

---

## Constants

```python
# Status display symbols
STATUS_INCOMPLETE: str = "○"
STATUS_COMPLETE: str = "✓"

# Priority values
PRIORITY_HIGH: str = "high"
PRIORITY_MEDIUM: str = "medium"
PRIORITY_LOW: str = "low"
VALID_PRIORITIES: list[str] = [PRIORITY_HIGH, PRIORITY_MEDIUM, PRIORITY_LOW]

# ANSI color codes for priority display
COLOR_RED: str = "\033[91m"      # high priority
COLOR_YELLOW: str = "\033[93m"   # medium priority
COLOR_GREEN: str = "\033[92m"    # low priority
COLOR_RESET: str = "\033[0m"     # reset to default

# Priority color mapping
PRIORITY_COLORS: dict[str, str] = {
    PRIORITY_HIGH: COLOR_RED,
    PRIORITY_MEDIUM: COLOR_YELLOW,
    PRIORITY_LOW: COLOR_GREEN
}

# Priority sort order (for sorting high-to-low)
PRIORITY_ORDER: dict[str, int] = {
    PRIORITY_HIGH: 0,
    PRIORITY_MEDIUM: 1,
    PRIORITY_LOW: 2
}

# Validation limits
MAX_TITLE_LENGTH: int = 100
MIN_TITLE_LENGTH: int = 1
MAX_DESCRIPTION_LENGTH: int = 500
MIN_DESCRIPTION_LENGTH: int = 0
MAX_TAG_LENGTH: int = 20
MIN_TAG_LENGTH: int = 1

# Display formatting
DISPLAY_TRUNCATE_LENGTH: int = 50
```

---

## Storage Structure

### Tasks Collection

```python
tasks: list[dict] = []
```

The tasks list is:
- Initialized as an empty list at application startup
- Passed explicitly to all functions (no global state)
- Mutated only by data layer functions
- Lost when the application exits (no persistence)

### Example Data

```python
tasks = [
    {
        "id": 1,
        "title": "Buy groceries",
        "description": "Milk, eggs, bread",
        "completed": False,
        "created_at": "2025-12-29T10:30:00",
        "priority": "high",
        "tags": ["shopping", "urgent"]
    },
    {
        "id": 2,
        "title": "Review pull request",
        "description": "Check the authentication changes",
        "completed": True,
        "created_at": "2025-12-29T09:15:00",
        "priority": "medium",
        "tags": ["work", "code-review"]
    },
    {
        "id": 5,  # Note: ID 3 and 4 were deleted
        "title": "Write documentation",
        "description": "",
        "completed": False,
        "created_at": "2025-12-29T11:45:00",
        "priority": "low",
        "tags": []
    }
]
```

---

## State Transitions

### Task Lifecycle

```
                    ┌─────────────────────┐
                    │       Created       │
                    │ completed=False     │
                    │ priority="medium"   │
                    │ tags=[]             │
                    └──────────┬──────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         │           │         │         │           │
         ▼           ▼         ▼         ▼           ▼
    ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
    │ Update  │ │ Toggle  │ │ Set     │ │ Manage  │ │ Delete  │
    │ (title) │ │ (done)  │ │ Priority│ │ Tags    │ │         │
    └─────────┘ └────┬────┘ └─────────┘ └─────────┘ └─────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
   ┌───────────────┐     ┌───────────────┐
   │   incomplete  │ ◄─► │   complete    │
   │      (○)      │     │      (✓)      │
   └───────────────┘     └───────────────┘
```

### Status Transition Matrix

| Current State | Action | New State |
|---------------|--------|-----------|
| incomplete | toggle | complete |
| complete | toggle | incomplete |
| any | update title | (unchanged status) |
| any | set priority | (status unchanged) |
| any | add/remove tag | (status unchanged) |
| any | delete | (removed) |

### Priority Transition Matrix

| Current Priority | Action | New Priority |
|------------------|--------|--------------|
| any | set "high" | high |
| any | set "medium" | medium |
| any | set "low" | low |

---

## Validation Rules

### Title Validation

```python
def validate_title(title: str) -> tuple[bool, str]:
    """
    Rules:
    1. Trim leading/trailing whitespace
    2. Must not be empty after trimming
    3. Must be <= 100 characters after trimming

    Returns:
        (True, trimmed_title) on success
        (False, error_message) on failure
    """
    trimmed = title.strip()

    if not trimmed:
        return False, "Error: Title cannot be empty."

    if len(trimmed) > MAX_TITLE_LENGTH:
        return False, f"Error: Title too long ({len(trimmed)} chars). Maximum is 100."

    return True, trimmed
```

### Description Validation

```python
def validate_description(description: str) -> tuple[bool, str]:
    """
    Rules:
    1. Trim leading/trailing whitespace
    2. Can be empty (optional field)
    3. Must be <= 500 characters after trimming

    Returns:
        (True, trimmed_description) on success
        (False, error_message) on failure
    """
    trimmed = description.strip()

    if len(trimmed) > MAX_DESCRIPTION_LENGTH:
        return False, f"Error: Description too long ({len(trimmed)} chars). Maximum is 500."

    return True, trimmed
```

### Task ID Validation

```python
def validate_task_id(task_id_str: str) -> tuple[bool, int | str]:
    """
    Rules:
    1. Must be numeric
    2. Must be a positive integer (> 0)

    Returns:
        (True, int_id) on success
        (False, error_message) on failure
    """
    stripped = task_id_str.strip()

    if not stripped.isdigit() or stripped == "0":
        return False, "Error: Task ID must be a positive number."

    return True, int(stripped)
```

### Priority Validation (NEW - INTERMEDIATE)

```python
def validate_priority(priority: str) -> tuple[bool, str]:
    """
    Rules:
    1. Trim and convert to lowercase
    2. Must be one of: "high", "medium", "low"

    Returns:
        (True, normalized_priority) on success
        (False, error_message) on failure
    """
    normalized = priority.strip().lower()

    if normalized not in VALID_PRIORITIES:
        return False, "Error: Invalid priority. Use: high, medium, or low."

    return True, normalized
```

### Tag Validation (NEW - INTERMEDIATE)

```python
def validate_tag(tag: str) -> tuple[bool, str]:
    """
    Rules:
    1. Trim and convert to lowercase
    2. Must be 1-20 characters
    3. Must be alphanumeric with hyphens only
    4. Cannot start or end with hyphen
    5. Cannot have consecutive hyphens

    Returns:
        (True, normalized_tag) on success
        (False, error_message) on failure
    """
    normalized = tag.strip().lower()

    if not normalized:
        return False, "Error: Tag cannot be empty."

    if len(normalized) > MAX_TAG_LENGTH:
        return False, f"Error: Tag too long ({len(normalized)} chars). Maximum is 20."

    if normalized.startswith("-") or normalized.endswith("-"):
        return False, "Error: Tag cannot start or end with hyphen."

    if "--" in normalized:
        return False, "Error: Tag cannot contain consecutive hyphens."

    import re
    if not re.match(r'^[a-z0-9-]+$', normalized):
        return False, "Error: Tag must contain only letters, numbers, and hyphens."

    return True, normalized
```

### Duplicate Tag Check

```python
def validate_tag_not_duplicate(task: dict, tag: str) -> tuple[bool, str]:
    """
    Rules:
    1. Tag must not already exist in task's tags

    Returns:
        (True, "") on success
        (False, error_message) on failure
    """
    if tag in task["tags"]:
        return False, f"Error: Tag '{tag}' already exists on this task."

    return True, ""
```

---

## Operations

### Create Task (Updated for INTERMEDIATE)

```python
def create_task(
    tasks: list[dict],
    title: str,
    description: str = ""
) -> dict:
    """
    Preconditions:
    - title is validated (non-empty, <= 100 chars)
    - description is validated (<= 500 chars)

    Effects:
    - New task added to tasks list with defaults:
      - completed = False
      - priority = "medium"
      - tags = []
    - Returns the created task
    """
    next_id = get_next_id(tasks)
    task = {
        "id": next_id,
        "title": title,
        "description": description,
        "completed": False,
        "created_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "priority": PRIORITY_MEDIUM,
        "tags": []
    }
    tasks.append(task)
    return task
```

### Set Priority (NEW - INTERMEDIATE)

```python
def set_task_priority(
    tasks: list[dict],
    task_id: int,
    priority: str
) -> bool:
    """
    Preconditions:
    - task_id exists in tasks
    - priority is validated ("high", "medium", or "low")

    Effects:
    - Task priority is updated
    - All other fields preserved

    Returns:
    - True if updated, False if not found
    """
```

### Add Tag (NEW - INTERMEDIATE)

```python
def add_tag_to_task(
    tasks: list[dict],
    task_id: int,
    tag: str
) -> bool:
    """
    Preconditions:
    - task_id exists in tasks
    - tag is validated (format and uniqueness)

    Effects:
    - Tag appended to task's tags list
    - All other fields preserved

    Returns:
    - True if added, False if not found
    """
```

### Remove Tag (NEW - INTERMEDIATE)

```python
def remove_tag_from_task(
    tasks: list[dict],
    task_id: int,
    tag: str
) -> bool:
    """
    Preconditions:
    - task_id exists in tasks
    - tag exists on the task

    Effects:
    - Tag removed from task's tags list
    - All other fields preserved

    Returns:
    - True if removed, False if not found
    """
```

### Search Tasks (NEW - INTERMEDIATE)

```python
def search_tasks(
    tasks: list[dict],
    query: str
) -> list[dict]:
    """
    Preconditions:
    - query is non-empty

    Algorithm:
    - Case-insensitive partial match
    - Search in title AND description
    - Return new list (no mutation)

    Returns:
    - List of matching tasks (may be empty)
    """
```

### Filter Tasks (NEW - INTERMEDIATE)

```python
def filter_by_status(tasks: list[dict], completed: bool) -> list[dict]:
    """Return tasks matching completion status."""

def filter_by_priority(tasks: list[dict], priority: str) -> list[dict]:
    """Return tasks matching priority level."""

def filter_by_tag(tasks: list[dict], tag: str) -> list[dict]:
    """Return tasks containing the specified tag."""
```

### Sort Tasks (NEW - INTERMEDIATE)

```python
def sort_by_date(tasks: list[dict], ascending: bool = True) -> list[dict]:
    """Sort by created_at (oldest/newest first)."""

def sort_by_priority(tasks: list[dict], high_first: bool = True) -> list[dict]:
    """Sort by priority (high-to-low or low-to-high)."""

def sort_by_title(tasks: list[dict], ascending: bool = True) -> list[dict]:
    """Sort alphabetically by title (A-Z or Z-A)."""
```

### Get Next ID

```python
def get_next_id(tasks: list[dict]) -> int:
    """
    Algorithm:
    - If tasks is empty, return 1
    - Otherwise, return max(all task IDs) + 1

    This ensures deleted IDs are never reused.
    """
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1
```

---

## Invariants

The following conditions must always be true:

1. **ID Uniqueness**: No two tasks have the same ID
2. **ID Positivity**: All task IDs are positive integers (>= 1)
3. **Completed Type**: All task completed values are boolean
4. **Title Non-Empty**: All task titles have length >= 1
5. **Title Length**: All task titles have length <= 100
6. **Description Length**: All task descriptions have length <= 500
7. **Timestamp Format**: All created_at values are valid ISO 8601 strings
8. **ID Non-Reuse**: Once a task is deleted, its ID is never assigned to a new task
9. **Priority Validity**: All task priorities are "high", "medium", or "low"
10. **Tag Format**: All tags are lowercase, alphanumeric with hyphens, 1-20 chars
11. **Tag Uniqueness**: No duplicate tags within a single task

---

## Backward Compatibility

For BASIC → INTERMEDIATE migration:
- Existing tasks with old schema would receive defaults:
  - `priority`: `"medium"`
  - `tags`: `[]`
- BASIC features (1-5) behavior unchanged
- Menu options 1-5 work identically

---

## Example Session

```python
# Application starts
tasks = []

# User adds "Buy groceries" with description
# create_task(tasks, "Buy groceries", "Milk, eggs, bread")
tasks = [
    {"id": 1, "title": "Buy groceries", "description": "Milk, eggs, bread",
     "completed": False, "created_at": "2025-12-29T10:00:00",
     "priority": "medium", "tags": []}
]

# User sets priority to high
# set_task_priority(tasks, 1, "high")
tasks = [
    {"id": 1, "title": "Buy groceries", "description": "Milk, eggs, bread",
     "completed": False, "created_at": "2025-12-29T10:00:00",
     "priority": "high", "tags": []}
]

# User adds tags "shopping" and "urgent"
# add_tag_to_task(tasks, 1, "shopping")
# add_tag_to_task(tasks, 1, "urgent")
tasks = [
    {"id": 1, "title": "Buy groceries", "description": "Milk, eggs, bread",
     "completed": False, "created_at": "2025-12-29T10:00:00",
     "priority": "high", "tags": ["shopping", "urgent"]}
]

# User adds another task
# create_task(tasks, "Write code", "Implement search feature")
tasks = [
    {"id": 1, ...},
    {"id": 2, "title": "Write code", "description": "Implement search feature",
     "completed": False, "created_at": "2025-12-29T10:05:00",
     "priority": "medium", "tags": []}
]

# User searches for "groceries"
# search_tasks(tasks, "groceries") → [task with id=1]

# User filters by high priority
# filter_by_priority(tasks, "high") → [task with id=1]

# User sorts by priority (high first)
# sort_by_priority(tasks, high_first=True) → [id=1, id=2]

# User toggles task 1
# toggle_task_status(tasks, 1) → True
tasks = [
    {"id": 1, ..., "completed": True, ...},
    {"id": 2, ..., "completed": False, ...}
]

# User filters by completed
# filter_by_status(tasks, completed=True) → [id=1]

# Application exits
# tasks list is garbage collected (no persistence)
```

---

## Dependencies

- **datetime**: Standard library module for timestamp generation
- **re**: Standard library module for tag validation regex
- **No external dependencies**: All data operations use built-in Python types
