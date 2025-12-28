# Implementation Plan: Console Todo Application - Phase I

**Branch**: `001-console-todo-app` | **Date**: 2025-12-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-console-todo-app/spec.md`

---

## Summary

A command-line todo application that allows users to manage tasks through a menu-driven interface. The application implements 5 core operations (add, view, update, delete, toggle status) with in-memory storage. All code resides in a single `todo.py` file following the layered architecture defined in the constitution.

**Primary Requirement**: Users can manage tasks (create, read, update, delete, toggle status) through a console interface with clear feedback.

**Technical Approach**: Layered architecture with explicit data flow through Command, Validation, Data, and Display layers. All state is passed explicitly; no global mutable state.

---

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: None (standard library only: `datetime` for timestamps)
**Storage**: In-memory (Python `list[dict]`)
**Testing**: Manual testing via console (no automated tests in Phase I)
**Target Platform**: Cross-platform (Windows, macOS, Linux)
**Project Type**: Single file (`todo.py`)
**Performance Goals**: All operations complete instantly (<100ms)
**Constraints**: No external dependencies, no file I/O, no persistence
**Scale/Scope**: Single user, single session, hundreds of tasks maximum

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Check | Status |
|-----------|-------|--------|
| I. Simplicity First | Single file, no abstractions, YAGNI | PASS |
| II. Code Quality | Type hints, docstrings, 88-char lines | PLANNED |
| III. User Experience | Clear prompts, error messages with remediation | PLANNED |
| IV. Data Integrity | Unique IDs, validation before modification | PLANNED |
| V. Explicit Over Implicit | No hidden side effects, explicit state | PLANNED |
| VI. Fail Fast and Clearly | Validate at entry, clear error messages | PLANNED |
| VII. Functional Style | Pure functions where practical, explicit data | PLANNED |
| VIII. Separation of Concerns | 4-layer architecture | PLANNED |
| IX. Testability | Small functions, injectable dependencies | PLANNED |

**Technical Constraints Check**:
- [x] Python 3.13+ only
- [x] No external dependencies
- [x] Single file implementation
- [x] In-memory storage only
- [x] No forbidden patterns (file I/O, network, threading, etc.)

---

## 1. Architecture Overview

### High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        APPLICATION LAYER                         │
│                          main() loop                             │
│  - Initialize tasks list and ID counter                         │
│  - Display menu, read user choice                                │
│  - Dispatch to appropriate command function                      │
│  - Loop until exit                                               │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                        COMMAND LAYER (cmd_*)                     │
│  cmd_add, cmd_list, cmd_update, cmd_delete, cmd_toggle          │
│  - Parse user input                                              │
│  - Call validation layer                                         │
│  - Call data layer on success                                    │
│  - Call display layer to show results                            │
└───────────┬─────────────────────────────────┬───────────────────┘
            │                                 │
            ▼                                 ▼
┌───────────────────────────┐   ┌─────────────────────────────────┐
│   VALIDATION LAYER        │   │         DATA LAYER               │
│   validate_description    │   │   create_task, get_task_by_id   │
│   validate_task_id        │   │   update_task_description        │
│   validate_task_exists    │   │   delete_task, toggle_task_status│
│                           │   │   get_next_id                    │
│   Returns: (bool, str)    │   │   Returns: dict | bool | None   │
└───────────────────────────┘   └─────────────────────────────────┘
                                              │
                                              ▼
                              ┌─────────────────────────────────┐
                              │        DISPLAY LAYER            │
                              │   display_menu, display_tasks   │
                              │   display_success, display_error│
                              │   format_task_row               │
                              │                                 │
                              │   Prints to stdout              │
                              └─────────────────────────────────┘
```

### Component Breakdown

| Layer | Responsibility | Functions |
|-------|----------------|-----------|
| Application | Main loop, menu dispatch | `main()` |
| Command | Parse input, orchestrate operations | `cmd_add`, `cmd_list`, `cmd_update`, `cmd_delete`, `cmd_toggle` |
| Validation | Validate all user input | `validate_description`, `validate_task_id`, `validate_task_exists` |
| Data | CRUD operations on tasks | `create_task`, `get_task_by_id`, `update_task_description`, `delete_task`, `toggle_task_status`, `get_next_id` |
| Display | Format and print output | `display_menu`, `display_tasks`, `display_success`, `display_error`, `display_header`, `format_task_row`, `truncate_text` |

### Design Principles Applied

1. **Single Responsibility**: Each layer has one job
2. **Dependency Inversion**: Command layer depends on abstractions (function signatures), not implementations
3. **Explicit State**: Tasks list passed as parameter, never global
4. **Fail Fast**: Validation happens before any data modification
5. **Pure Functions**: Data layer functions are pure where possible

---

## 2. Module Breakdown

### 2.1 Constants (Module-Level)

```python
# Status constants
STATUS_PENDING: str = "pending"
STATUS_COMPLETED: str = "completed"

# Validation constants
MAX_DESCRIPTION_LENGTH: int = 200
DISPLAY_TRUNCATE_LENGTH: int = 50

# Menu constants
MENU_ADD: str = "1"
MENU_LIST: str = "2"
MENU_UPDATE: str = "3"
MENU_DELETE: str = "4"
MENU_TOGGLE: str = "5"
MENU_EXIT: str = "6"
VALID_MENU_CHOICES: list[str] = [MENU_ADD, MENU_LIST, MENU_UPDATE,
                                  MENU_DELETE, MENU_TOGGLE, MENU_EXIT]
```

### 2.2 Data Layer

**Purpose**: Manage task data storage and retrieval. Pure functions where possible.

**Functions**:
- `get_next_id(tasks)` - Calculate next available task ID
- `create_task(tasks, description, next_id)` - Create and add new task
- `get_task_by_id(tasks, task_id)` - Find task by ID
- `update_task_description(tasks, task_id, new_description)` - Update description
- `delete_task(tasks, task_id)` - Remove task from list
- `toggle_task_status(tasks, task_id)` - Toggle pending/completed

**Dependencies**: None (pure functions)

**Why This Layer Exists**: Encapsulates all data operations, making them testable and reusable. The command layer doesn't need to know how tasks are stored.

### 2.3 Validation Layer

**Purpose**: Validate all user input before processing.

**Functions**:
- `validate_description(description)` - Check description length and content
- `validate_task_id(task_id_str)` - Check if input is valid positive integer
- `validate_task_exists(tasks, task_id)` - Check if task with ID exists

**Dependencies**: None (pure functions)

**Why This Layer Exists**: Separates validation logic from command logic. Ensures consistent error messages and validation rules across all commands.

### 2.4 Display Layer

**Purpose**: Format and print all output to the user.

**Functions**:
- `display_menu()` - Show main menu
- `display_header(title)` - Show section header
- `display_tasks(tasks)` - Show formatted task table
- `display_success(message)` - Show success message
- `display_error(message)` - Show error message
- `format_task_row(task)` - Format single task as table row
- `truncate_text(text, max_length)` - Truncate long text with "..."

**Dependencies**: None (output only)

**Why This Layer Exists**: Centralizes all output formatting. If we later want to change the display format, only this layer changes.

### 2.5 Command Layer

**Purpose**: Handle user commands by orchestrating validation, data operations, and display.

**Functions**:
- `cmd_add(tasks)` - Handle add task command
- `cmd_list(tasks)` - Handle list tasks command
- `cmd_update(tasks)` - Handle update task command
- `cmd_delete(tasks)` - Handle delete task command
- `cmd_toggle(tasks)` - Handle toggle status command

**Dependencies**: Validation Layer, Data Layer, Display Layer

**Why This Layer Exists**: Orchestrates the flow for each user action. Knows the sequence of operations but delegates specifics to other layers.

### 2.6 Application Layer

**Purpose**: Main entry point and loop.

**Functions**:
- `main()` - Initialize state, run main loop

**Dependencies**: Command Layer, Display Layer

**Why This Layer Exists**: Single entry point. Owns the tasks list and dispatches to commands.

---

## 3. Complete Function Signatures

### 3.1 Data Layer Functions

```python
def get_next_id(tasks: list[dict]) -> int:
    """Calculate the next available task ID.

    Uses max(existing_ids) + 1 to ensure deleted IDs are never reused.
    Returns 1 if no tasks exist.

    Args:
        tasks: The list of task dictionaries.

    Returns:
        The next available unique task ID.
    """
```

```python
def create_task(tasks: list[dict], description: str, next_id: int) -> dict:
    """Create a new task and add it to the task list.

    Args:
        tasks: The list of task dictionaries (will be mutated).
        description: The task description (should be pre-validated).
        next_id: The unique ID to assign to this task.

    Returns:
        The newly created task dictionary.
    """
```

```python
def get_task_by_id(tasks: list[dict], task_id: int) -> dict | None:
    """Find a task by its ID.

    Args:
        tasks: The list of task dictionaries to search.
        task_id: The ID of the task to find.

    Returns:
        The task dictionary if found, None otherwise.
    """
```

```python
def update_task_description(
    tasks: list[dict],
    task_id: int,
    new_description: str
) -> bool:
    """Update a task's description.

    Args:
        tasks: The list of task dictionaries.
        task_id: The ID of the task to update.
        new_description: The new description (should be pre-validated).

    Returns:
        True if task was found and updated, False otherwise.
    """
```

```python
def delete_task(tasks: list[dict], task_id: int) -> bool:
    """Remove a task from the list.

    Args:
        tasks: The list of task dictionaries (will be mutated).
        task_id: The ID of the task to delete.

    Returns:
        True if task was found and deleted, False otherwise.
    """
```

```python
def toggle_task_status(tasks: list[dict], task_id: int) -> tuple[bool, str]:
    """Toggle a task's status between pending and completed.

    Args:
        tasks: The list of task dictionaries.
        task_id: The ID of the task to toggle.

    Returns:
        Tuple of (success, new_status). On failure, new_status is empty string.
    """
```

### 3.2 Validation Layer Functions

```python
def validate_description(description: str) -> tuple[bool, str]:
    """Validate a task description.

    Checks that description is non-empty (after trimming) and within length limit.

    Args:
        description: The raw description input from user.

    Returns:
        (True, trimmed_description) on success.
        (False, error_message) on failure.
    """
```

```python
def validate_task_id(task_id_str: str) -> tuple[bool, int | str]:
    """Validate and parse a task ID string.

    Args:
        task_id_str: The raw task ID input from user.

    Returns:
        (True, parsed_id) on success where parsed_id is int.
        (False, error_message) on failure where error_message is str.
    """
```

```python
def validate_task_exists(tasks: list[dict], task_id: int) -> tuple[bool, str]:
    """Check if a task with the given ID exists.

    Args:
        tasks: The list of task dictionaries.
        task_id: The ID to check.

    Returns:
        (True, "") on success.
        (False, error_message) on failure.
    """
```

### 3.3 Display Layer Functions

```python
def display_menu() -> None:
    """Display the main menu with all available options."""
```

```python
def display_header(title: str) -> None:
    """Display a section header with decorative borders.

    Args:
        title: The title text to display centered.
    """
```

```python
def display_tasks(tasks: list[dict]) -> None:
    """Display all tasks in a formatted table.

    Shows appropriate message if no tasks exist.

    Args:
        tasks: The list of task dictionaries to display.
    """
```

```python
def display_success(message: str) -> None:
    """Display a success message.

    Args:
        message: The success message to display.
    """
```

```python
def display_error(message: str) -> None:
    """Display an error message.

    Args:
        message: The error message to display.
    """
```

```python
def format_task_row(task: dict) -> str:
    """Format a single task as a table row.

    Args:
        task: The task dictionary to format.

    Returns:
        A formatted string representing the task as a table row.
    """
```

```python
def truncate_text(text: str, max_length: int) -> str:
    """Truncate text to a maximum length, adding '...' if truncated.

    Args:
        text: The text to potentially truncate.
        max_length: Maximum length including the '...' suffix.

    Returns:
        The original text if short enough, or truncated text with '...'.
    """
```

### 3.4 Command Layer Functions

```python
def cmd_add(tasks: list[dict]) -> None:
    """Handle the add task command.

    Prompts for description, validates, creates task, displays result.

    Args:
        tasks: The list of task dictionaries (will be mutated on success).
    """
```

```python
def cmd_list(tasks: list[dict]) -> None:
    """Handle the list tasks command.

    Displays all tasks in a formatted table.

    Args:
        tasks: The list of task dictionaries to display.
    """
```

```python
def cmd_update(tasks: list[dict]) -> None:
    """Handle the update task command.

    Prompts for task ID and new description, validates, updates, displays result.

    Args:
        tasks: The list of task dictionaries (will be mutated on success).
    """
```

```python
def cmd_delete(tasks: list[dict]) -> None:
    """Handle the delete task command.

    Prompts for task ID, validates, deletes, displays result.

    Args:
        tasks: The list of task dictionaries (will be mutated on success).
    """
```

```python
def cmd_toggle(tasks: list[dict]) -> None:
    """Handle the toggle status command.

    Prompts for task ID, validates, toggles status, displays result.

    Args:
        tasks: The list of task dictionaries (will be mutated on success).
    """
```

### 3.5 Application Layer Functions

```python
def main() -> None:
    """Main entry point for the todo application.

    Initializes the task list, runs the main menu loop until exit.
    """
```

---

## 4. Data Structures

### 4.1 Task Dictionary

```python
Task = {
    "id": int,           # Unique, positive, auto-incrementing, never reused
    "description": str,  # 1-200 characters, whitespace trimmed
    "status": str,       # "pending" or "completed"
    "created_at": str,   # ISO 8601 format: "2025-12-28T10:30:00"
}
```

### 4.2 Tasks List

```python
tasks: list[dict] = []  # List of Task dictionaries
```

### 4.3 Constants

```python
# Status values
STATUS_PENDING = "pending"
STATUS_COMPLETED = "completed"

# Validation limits
MAX_DESCRIPTION_LENGTH = 200
DISPLAY_TRUNCATE_LENGTH = 50

# Menu options
MENU_ADD = "1"
MENU_LIST = "2"
MENU_UPDATE = "3"
MENU_DELETE = "4"
MENU_TOGGLE = "5"
MENU_EXIT = "6"
VALID_MENU_CHOICES = [MENU_ADD, MENU_LIST, MENU_UPDATE,
                      MENU_DELETE, MENU_TOGGLE, MENU_EXIT]

# Display constants
SEPARATOR = "=" * 40
TABLE_HEADER = "ID  | Description                        | Status    | Created"
TABLE_DIVIDER = "----|------------------------------------|-----------|-----------------"
```

---

## 5. Data Flow Diagrams

### 5.1 Add Task Flow

```
User Input: "1" (Add Task)
    │
    ▼
┌──────────────────────────────────────────────────────────────┐
│ main() dispatches to cmd_add(tasks)                          │
└──────────────────────────────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────────────────────────────┐
│ cmd_add():                                                    │
│   1. Prompt: "Enter task description: "                       │
│   2. Read user input                                          │
│   3. Call validate_description(input)                         │
└──────────────────────────────────────────────────────────────┘
    │
    ├─── Validation FAILS ───┐
    │                        │
    ▼                        ▼
┌────────────────────┐  ┌────────────────────────────────────────┐
│ Validation PASSES  │  │ display_error(error_message)            │
│                    │  │ Return to menu                          │
└────────────────────┘  └────────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────────────────────────────┐
│ cmd_add():                                                    │
│   4. next_id = get_next_id(tasks)                            │
│   5. task = create_task(tasks, description, next_id)         │
│   6. display_success(f"Task {id} added: {description}")      │
└──────────────────────────────────────────────────────────────┘
    │
    ▼
Return to main menu
```

### 5.2 List Tasks Flow

```
User Input: "2" (View Tasks)
    │
    ▼
┌──────────────────────────────────────────────────────────────┐
│ main() dispatches to cmd_list(tasks)                         │
└──────────────────────────────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────────────────────────────┐
│ cmd_list():                                                   │
│   1. Call display_tasks(tasks)                                │
└──────────────────────────────────────────────────────────────┘
    │
    ├─── tasks is empty ────┐
    │                       │
    ▼                       ▼
┌────────────────────┐  ┌────────────────────────────────────────┐
│ Tasks exist        │  │ Display: "No tasks found. Use 'Add     │
│                    │  │ Task' to create your first task."      │
└────────────────────┘  └────────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────────────────────────────┐
│ display_tasks():                                              │
│   1. display_header("YOUR TASKS")                            │
│   2. Print table header                                       │
│   3. For each task: format_task_row(task) and print          │
│   4. Print summary (total, pending, completed counts)        │
└──────────────────────────────────────────────────────────────┘
    │
    ▼
Return to main menu
```

### 5.3 Update Task Flow

```
User Input: "3" (Update Task)
    │
    ▼
┌──────────────────────────────────────────────────────────────┐
│ main() dispatches to cmd_update(tasks)                       │
└──────────────────────────────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────────────────────────────┐
│ cmd_update():                                                 │
│   1. Check if tasks list is empty                            │
│      → If empty: display_error("No tasks available...")      │
│   2. Prompt: "Enter task ID to update: "                     │
│   3. Call validate_task_id(input)                            │
│      → If fails: display_error, return                       │
│   4. Call validate_task_exists(tasks, task_id)               │
│      → If fails: display_error, return                       │
│   5. Prompt: "Enter new description: "                       │
│   6. Call validate_description(input)                        │
│      → If fails: display_error, return                       │
│   7. Call update_task_description(tasks, task_id, desc)      │
│   8. display_success(f"Task {id} updated: {desc}")           │
└──────────────────────────────────────────────────────────────┘
    │
    ▼
Return to main menu
```

### 5.4 Delete Task Flow

```
User Input: "4" (Delete Task)
    │
    ▼
┌──────────────────────────────────────────────────────────────┐
│ cmd_delete():                                                 │
│   1. Check if tasks list is empty                            │
│      → If empty: display_error("No tasks available...")      │
│   2. Prompt: "Enter task ID to delete: "                     │
│   3. Call validate_task_id(input)                            │
│      → If fails: display_error, return                       │
│   4. Call validate_task_exists(tasks, task_id)               │
│      → If fails: display_error, return                       │
│   5. Call delete_task(tasks, task_id)                        │
│   6. display_success(f"Task {id} deleted successfully.")     │
└──────────────────────────────────────────────────────────────┘
    │
    ▼
Return to main menu
```

### 5.5 Toggle Status Flow

```
User Input: "5" (Toggle Complete/Incomplete)
    │
    ▼
┌──────────────────────────────────────────────────────────────┐
│ cmd_toggle():                                                 │
│   1. Check if tasks list is empty                            │
│      → If empty: display_error("No tasks available...")      │
│   2. Prompt: "Enter task ID to toggle: "                     │
│   3. Call validate_task_id(input)                            │
│      → If fails: display_error, return                       │
│   4. Call validate_task_exists(tasks, task_id)               │
│      → If fails: display_error, return                       │
│   5. Call toggle_task_status(tasks, task_id)                 │
│   6. If new_status == "completed":                           │
│        display_success(f"Task {id} marked as completed.")    │
│      Else:                                                    │
│        display_success(f"Task {id} marked as pending.")      │
└──────────────────────────────────────────────────────────────┘
    │
    ▼
Return to main menu
```

---

## 6. Error Handling Architecture

### 6.1 Error Propagation Pattern

```
┌─────────────────────────────────────────────────────────────┐
│ VALIDATION LAYER                                             │
│ Returns: tuple[bool, str]                                    │
│   - (True, cleaned_value) on success                        │
│   - (False, error_message) on failure                       │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ COMMAND LAYER                                                │
│ Checks validation result:                                    │
│   if not success:                                            │
│       display_error(error_message)                           │
│       return  # Early exit                                   │
│   else:                                                       │
│       proceed with data operation                            │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ DATA LAYER                                                   │
│ Returns: bool (success/failure) or dict | None              │
│   - Assumes input is pre-validated                          │
│   - Returns False/None only for "not found" cases           │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ DISPLAY LAYER                                                │
│ display_error(message) - Prints error to stdout             │
│ display_success(message) - Prints success to stdout         │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 Validation Points

| Validation | Layer | When Called |
|------------|-------|-------------|
| Description not empty | Validation | Before create/update |
| Description length <= 200 | Validation | Before create/update |
| Task ID is numeric | Validation | Before update/delete/toggle |
| Task ID is positive | Validation | Before update/delete/toggle |
| Task ID exists | Validation | Before update/delete/toggle |
| Menu choice is valid | Command | In main loop |
| Tasks list not empty | Command | Before update/delete/toggle |

### 6.3 Error Message Format

All error messages follow this pattern from the constitution:

```
Error: [What went wrong]. [How to fix it].
```

Examples:
- `Error: Description cannot be empty. Please provide a task description.`
- `Error: Task ID must be a number. Please enter a valid ID like '1' or '2'.`
- `Error: Task 5 not found. Use 'View Tasks' to see available task IDs.`

---

## 7. Implementation Sequence

### Phase 1: Foundation (No Dependencies)

1. **Constants** - Define all constants first
2. **truncate_text()** - Pure utility function
3. **display_header()** - Simple output function
4. **display_error()** - Simple output function
5. **display_success()** - Simple output function

### Phase 2: Display Layer

6. **format_task_row()** - Depends on truncate_text
7. **display_tasks()** - Depends on format_task_row, display_header
8. **display_menu()** - Depends on display_header

### Phase 3: Validation Layer

9. **validate_description()** - Pure validation
10. **validate_task_id()** - Pure validation
11. **validate_task_exists()** - Depends on get_task_by_id

### Phase 4: Data Layer

12. **get_next_id()** - Pure function
13. **get_task_by_id()** - Pure function
14. **create_task()** - Depends on datetime
15. **update_task_description()** - Depends on get_task_by_id
16. **delete_task()** - Pure mutation
17. **toggle_task_status()** - Depends on get_task_by_id

### Phase 5: Command Layer

18. **cmd_add()** - Uses validation, data, display
19. **cmd_list()** - Uses display
20. **cmd_update()** - Uses validation, data, display
21. **cmd_delete()** - Uses validation, data, display
22. **cmd_toggle()** - Uses validation, data, display

### Phase 6: Application Layer

23. **main()** - Uses command, display layers

### Dependency Graph

```
Constants
    │
    ├── truncate_text()
    │       │
    │       └── format_task_row()
    │               │
    │               └── display_tasks()
    │
    ├── display_header()
    │       │
    │       ├── display_menu()
    │       └── display_tasks()
    │
    ├── display_error()
    │       │
    │       └── [All cmd_* functions]
    │
    ├── display_success()
    │       │
    │       └── [All cmd_* functions]
    │
    ├── validate_description()
    │       │
    │       ├── cmd_add()
    │       └── cmd_update()
    │
    ├── validate_task_id()
    │       │
    │       ├── cmd_update()
    │       ├── cmd_delete()
    │       └── cmd_toggle()
    │
    ├── get_task_by_id()
    │       │
    │       ├── validate_task_exists()
    │       ├── update_task_description()
    │       └── toggle_task_status()
    │
    ├── get_next_id()
    │       │
    │       └── cmd_add() → create_task()
    │
    └── main()
            │
            ├── display_menu()
            ├── cmd_add()
            ├── cmd_list()
            ├── cmd_update()
            ├── cmd_delete()
            └── cmd_toggle()
```

---

## 8. Testing Strategy

### 8.1 Layer Testing Approach

| Layer | Testing Method | Isolation |
|-------|---------------|-----------|
| Data | Unit tests with mock data | Pass test tasks list |
| Validation | Unit tests with edge cases | Pure functions, no dependencies |
| Display | Visual inspection | Capture stdout if needed |
| Command | Integration tests | Use all layers together |
| Application | End-to-end manual testing | Full application |

### 8.2 Example Test Cases

**validate_description()**:
```python
# Success cases
assert validate_description("Buy milk") == (True, "Buy milk")
assert validate_description("  Buy milk  ") == (True, "Buy milk")
assert validate_description("x") == (True, "x")
assert validate_description("x" * 200) == (True, "x" * 200)

# Failure cases
assert validate_description("")[0] == False
assert validate_description("   ")[0] == False
assert validate_description("x" * 201)[0] == False
```

**validate_task_id()**:
```python
# Success cases
assert validate_task_id("1") == (True, 1)
assert validate_task_id("42") == (True, 42)

# Failure cases
assert validate_task_id("abc")[0] == False
assert validate_task_id("0")[0] == False
assert validate_task_id("-1")[0] == False
assert validate_task_id("")[0] == False
```

**get_next_id()**:
```python
assert get_next_id([]) == 1
assert get_next_id([{"id": 1}]) == 2
assert get_next_id([{"id": 1}, {"id": 5}]) == 6
assert get_next_id([{"id": 3}]) == 4  # Gap doesn't matter
```

### 8.3 Edge Cases to Test

| Category | Edge Cases |
|----------|------------|
| Empty list | View, update, delete, toggle with no tasks |
| Boundaries | 1-char description, 200-char description, 201-char description |
| ID handling | First task (ID=1), gaps in IDs after deletion, large IDs |
| Input | Whitespace-only, leading/trailing whitespace, special characters |
| Status | Toggle pending→completed, toggle completed→pending |

---

## 9. Design Decisions

### 9.1 Why Layered Architecture?

**Decision**: 4-layer architecture (Application, Command, Validation/Data, Display)

**Rationale**:
- **Testability**: Each layer can be tested independently
- **Maintainability**: Changes to display don't affect data logic
- **Clarity**: Clear responsibilities for each function
- **Constitution Compliance**: Matches "VIII. Separation of Concerns"

**Alternatives Rejected**:
- Monolithic: Too hard to test and maintain
- MVC: Overcomplicated for console app

### 9.2 Why Pass Tasks List Explicitly?

**Decision**: Pass `tasks: list[dict]` as parameter to all functions

**Rationale**:
- **Constitution Compliance**: "No global mutable state"
- **Testability**: Easy to test with mock data
- **Explicit**: Clear what data a function uses
- **Thread-safe**: (Not needed now, but good practice)

**Alternatives Rejected**:
- Global variable: Violates constitution, hard to test
- Class-based: Overcomplicated for Phase I

### 9.3 How to Generate IDs?

**Decision**: Use `max(task["id"] for task in tasks) + 1`, defaulting to 1 if empty

**Rationale**:
- **Never reuses IDs**: Even after deletion
- **Simple**: No separate counter needed
- **Stateless**: Calculated from current data

**Alternatives Rejected**:
- Auto-increment counter: Would need to be passed around or stored
- UUID: Overcomplicated, not user-friendly for console input

### 9.4 How to Handle ID Reuse After Deletion?

**Decision**: Deleted IDs are never reused

**Rationale**:
- **Spec Requirement**: FR-017 states "System MUST NOT reuse deleted task IDs"
- **User Clarity**: "Task 5" always refers to the same task
- **Simple**: Just use max ID + 1

### 9.5 Case Sensitivity for Menu Input?

**Decision**: Menu accepts exact numeric input only ("1", "2", etc.)

**Rationale**:
- **Simple**: No ambiguity
- **Clear**: Menu shows exact options
- **Consistent**: Same validation pattern throughout

### 9.6 How to Truncate Long Titles in Display?

**Decision**: Truncate at 50 characters with "..." suffix

**Rationale**:
- **Readability**: Keeps table formatted
- **Information**: Shows start of description
- **Configurable**: DISPLAY_TRUNCATE_LENGTH constant

**Implementation**:
```python
def truncate_text(text: str, max_length: int = 50) -> str:
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."
```

---

## 10. Integration Points

### 10.1 Main Loop Structure

```python
def main() -> None:
    tasks: list[dict] = []

    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice == MENU_ADD:
            cmd_add(tasks)
        elif choice == MENU_LIST:
            cmd_list(tasks)
        elif choice == MENU_UPDATE:
            cmd_update(tasks)
        elif choice == MENU_DELETE:
            cmd_delete(tasks)
        elif choice == MENU_TOGGLE:
            cmd_toggle(tasks)
        elif choice == MENU_EXIT:
            print("Goodbye!")
            break
        else:
            display_error("Invalid choice. Please select a number from the menu.")
```

### 10.2 Command Function Pattern

All command functions follow this pattern:

```python
def cmd_<action>(tasks: list[dict]) -> None:
    # 1. Early exit if tasks list is empty (for update/delete/toggle)
    if not tasks:
        display_error("No tasks available. Add a task first.")
        return

    # 2. Get user input
    user_input = input("Prompt: ").strip()

    # 3. Validate input
    success, result = validate_<type>(user_input)
    if not success:
        display_error(result)
        return

    # 4. Perform data operation
    data_result = data_operation(tasks, result)

    # 5. Display result
    display_success(f"Action completed: {details}")
```

### 10.3 Layer Dependencies

```
Application Layer
       │
       │ calls
       ▼
Command Layer ───────────────────────────────────────┐
       │                                              │
       │ calls                                        │ calls
       ▼                                              ▼
Validation Layer                              Display Layer
       │                                              │
       │ calls                                        │ outputs
       ▼                                              ▼
Data Layer                                    stdout (user)
       │
       │ uses
       ▼
Python datetime module (standard library)
```

---

## Project Structure

### Documentation (this feature)

```text
specs/001-console-todo-app/
├── spec.md              # Feature specification
├── plan.md              # This file (implementation plan)
├── data-model.md        # Data model documentation
├── quickstart.md        # Quick start guide
└── tasks.md             # Task list (created by /sp.tasks)
```

### Source Code (repository root)

```text
todo.py                  # Single-file implementation (all code here)
```

**Structure Decision**: Single file implementation as required by constitution. No separate directories for source code. All functions organized within the file by layer (constants → display → validation → data → command → main).

---

## Complexity Tracking

No complexity violations. This implementation follows the simplest possible approach:

| Aspect | Choice | Justification |
|--------|--------|---------------|
| Architecture | 4 layers | Required by constitution for separation of concerns |
| Storage | In-memory list | Required by spec (no persistence) |
| File structure | Single file | Required by constitution |
| Dependencies | None | Required by constitution |
| ID generation | max + 1 | Simplest approach that meets requirements |

---

## Next Steps

1. Run `/sp.tasks` to generate implementation tasks from this plan
2. Implement functions in the order specified in Section 7
3. Test each layer independently before integration
4. Run end-to-end manual testing before delivery
