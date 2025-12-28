# Data Model: Console Todo Application - Phase I

**Feature**: 001-console-todo-app
**Date**: 2025-12-28
**Source**: [spec.md](./spec.md), [plan.md](./plan.md)

---

## Overview

The Console Todo Application uses a simple in-memory data model with a single entity: **Task**. All tasks are stored in a Python list of dictionaries, with no persistence between sessions.

---

## Entity: Task

### Definition

A Task represents a unit of work that the user wants to track.

### Schema

```python
Task = {
    "id": int,
    "description": str,
    "status": str,
    "created_at": str
}
```

### Field Specifications

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `int` | Yes | Unique identifier for the task |
| `description` | `str` | Yes | User-provided description of the task |
| `status` | `str` | Yes | Current completion status |
| `created_at` | `str` | Yes | Timestamp when task was created |

### Field Constraints

#### id
- **Type**: Positive integer
- **Generation**: Auto-incremented using `max(existing_ids) + 1`
- **Uniqueness**: Must be unique within the session
- **Reuse**: Never reused, even after deletion
- **Default**: First task gets ID `1`

#### description
- **Type**: String
- **Length**: 1-200 characters (after whitespace trimming)
- **Trimming**: Leading and trailing whitespace is automatically removed
- **Content**: Any printable characters including Unicode
- **Validation**: Cannot be empty or whitespace-only

#### status
- **Type**: String literal
- **Valid Values**: `"pending"` or `"completed"` only
- **Default**: `"pending"` (set on creation)
- **Transitions**: Can toggle between `pending` ↔ `completed`

#### created_at
- **Type**: ISO 8601 formatted string
- **Format**: `"YYYY-MM-DDTHH:MM:SS"` (e.g., `"2025-12-28T10:30:00"`)
- **Generation**: Automatically set at task creation time
- **Mutability**: Never changes after creation

---

## Constants

```python
# Status values
STATUS_PENDING: str = "pending"
STATUS_COMPLETED: str = "completed"
VALID_STATUSES: list[str] = [STATUS_PENDING, STATUS_COMPLETED]

# Validation limits
MAX_DESCRIPTION_LENGTH: int = 200
MIN_DESCRIPTION_LENGTH: int = 1

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
        "description": "Buy groceries",
        "status": "pending",
        "created_at": "2025-12-28T10:30:00"
    },
    {
        "id": 2,
        "description": "Review pull request",
        "status": "completed",
        "created_at": "2025-12-28T09:15:00"
    },
    {
        "id": 5,  # Note: ID 3 and 4 were deleted
        "description": "Write documentation",
        "status": "pending",
        "created_at": "2025-12-28T11:45:00"
    }
]
```

---

## State Transitions

### Task Lifecycle

```
                    ┌─────────────────┐
                    │     Created     │
                    │ (status=pending)│
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
        ┌──────────┐   ┌──────────┐   ┌──────────┐
        │  Update  │   │  Toggle  │   │  Delete  │
        │  (desc)  │   │ (status) │   │          │
        └──────────┘   └────┬─────┘   └──────────┘
                            │
              ┌─────────────┴─────────────┐
              │                           │
              ▼                           ▼
        ┌───────────────┐         ┌───────────────┐
        │    pending    │ ◄─────► │   completed   │
        └───────────────┘ toggle  └───────────────┘
```

### Status Transition Matrix

| Current Status | Action | New Status |
|----------------|--------|------------|
| pending | toggle | completed |
| completed | toggle | pending |
| any | update | (unchanged) |
| any | delete | (removed) |

---

## Validation Rules

### Description Validation

```python
def validate_description(description: str) -> tuple[bool, str]:
    """
    Rules:
    1. Trim leading/trailing whitespace
    2. Must not be empty after trimming
    3. Must be <= 200 characters after trimming
    """
    trimmed = description.strip()

    if not trimmed:
        return False, "Error: Description cannot be empty."

    if len(trimmed) > MAX_DESCRIPTION_LENGTH:
        return False, f"Error: Description too long ({len(trimmed)} chars). Maximum is 200."

    return True, trimmed
```

### Task ID Validation

```python
def validate_task_id(task_id_str: str) -> tuple[bool, int | str]:
    """
    Rules:
    1. Must be numeric
    2. Must be a positive integer (> 0)
    """
    stripped = task_id_str.strip()

    if not stripped.isdigit() or stripped == "0":
        return False, "Error: Task ID must be a number."

    return True, int(stripped)
```

### Existence Validation

```python
def validate_task_exists(tasks: list[dict], task_id: int) -> tuple[bool, str]:
    """
    Rules:
    1. Task with given ID must exist in the list
    """
    for task in tasks:
        if task["id"] == task_id:
            return True, ""

    return False, f"Error: Task {task_id} not found."
```

---

## Operations

### Create Task

```python
def create_task(tasks: list[dict], description: str, next_id: int) -> dict:
    """
    Preconditions:
    - description is validated (non-empty, <= 200 chars)
    - next_id is calculated from get_next_id()

    Effects:
    - New task added to tasks list
    - Returns the created task
    """
    task = {
        "id": next_id,
        "description": description,
        "status": STATUS_PENDING,
        "created_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    }
    tasks.append(task)
    return task
```

### Read Task

```python
def get_task_by_id(tasks: list[dict], task_id: int) -> dict | None:
    """
    Returns:
    - Task dict if found
    - None if not found
    """
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None
```

### Update Task Description

```python
def update_task_description(
    tasks: list[dict],
    task_id: int,
    new_description: str
) -> bool:
    """
    Preconditions:
    - task_id exists in tasks
    - new_description is validated

    Effects:
    - Task description is updated
    - ID, status, created_at are preserved

    Returns:
    - True if updated, False if not found
    """
```

### Delete Task

```python
def delete_task(tasks: list[dict], task_id: int) -> bool:
    """
    Preconditions:
    - task_id exists in tasks

    Effects:
    - Task is removed from list
    - ID is never reused

    Returns:
    - True if deleted, False if not found
    """
```

### Toggle Status

```python
def toggle_task_status(tasks: list[dict], task_id: int) -> tuple[bool, str]:
    """
    Preconditions:
    - task_id exists in tasks

    Effects:
    - pending → completed
    - completed → pending

    Returns:
    - (True, new_status) if successful
    - (False, "") if task not found
    """
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
3. **Status Validity**: All task statuses are either "pending" or "completed"
4. **Description Non-Empty**: All task descriptions have length >= 1
5. **Description Length**: All task descriptions have length <= 200
6. **Timestamp Format**: All created_at values are valid ISO 8601 strings
7. **ID Non-Reuse**: Once a task is deleted, its ID is never assigned to a new task

---

## Example Session

```python
# Application starts
tasks = []

# User adds "Buy groceries"
# get_next_id(tasks) → 1
# create_task(tasks, "Buy groceries", 1)
tasks = [
    {"id": 1, "description": "Buy groceries", "status": "pending",
     "created_at": "2025-12-28T10:00:00"}
]

# User adds "Write code"
# get_next_id(tasks) → 2
tasks = [
    {"id": 1, "description": "Buy groceries", "status": "pending", ...},
    {"id": 2, "description": "Write code", "status": "pending", ...}
]

# User toggles task 1
# toggle_task_status(tasks, 1) → (True, "completed")
tasks = [
    {"id": 1, "description": "Buy groceries", "status": "completed", ...},
    {"id": 2, "description": "Write code", "status": "pending", ...}
]

# User deletes task 1
# delete_task(tasks, 1) → True
tasks = [
    {"id": 2, "description": "Write code", "status": "pending", ...}
]

# User adds "Review PR"
# get_next_id(tasks) → 3 (NOT 1, because we use max + 1)
tasks = [
    {"id": 2, "description": "Write code", "status": "pending", ...},
    {"id": 3, "description": "Review PR", "status": "pending", ...}
]

# Application exits
# tasks list is garbage collected (no persistence)
```

---

## Dependencies

- **datetime**: Standard library module for timestamp generation
- **No external dependencies**: All data operations use built-in Python types
