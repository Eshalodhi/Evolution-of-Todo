# Implementation Plan: Console Todo Application - Phase I (INTERMEDIATE Level)

**Branch**: `001-console-todo-app` | **Date**: 2025-12-29 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-console-todo-app/spec.md`
**Level**: INTERMEDIATE (10 features, ~41 functions)

---

## Summary

A command-line todo application that allows users to manage tasks through a menu-driven interface. The application implements 10 operations:
- **BASIC (1-5)**: Add, View, Update, Delete, Toggle Status
- **INTERMEDIATE (6-10)**: Set Priority, Manage Tags, Search, Filter, Sort

All code resides in a single `todo.py` file following the 5-layer architecture defined in the constitution. Data is stored in-memory with no persistence.

**Primary Requirement**: Users can manage tasks with priority levels and tags, search by keyword, filter by criteria, and sort by various fields through a console interface with color-coded feedback.

**Technical Approach**: Layered architecture with explicit data flow through Application, Command, Validation, Data, and Display layers. All state is passed explicitly; no global mutable state. Sort/filter/search operations return new lists without mutating originals.

---

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: None (standard library only: `datetime` for timestamps)
**Storage**: In-memory (Python `list[dict]`)
**Testing**: Manual testing via console (no automated tests in Phase I)
**Target Platform**: Cross-platform (Windows, macOS, Linux)
**Project Type**: Single file (`todo.py`)
**Performance Goals**: All operations complete instantly (<100ms, search/sort <500ms for 1000+ tasks)
**Constraints**: No external dependencies, no file I/O, no persistence
**Scale/Scope**: Single user, single session, up to 10,000 tasks

---

## Constitution Check

*GATE: Must pass before implementation. All checks passed.*

| Principle | Check | Status |
|-----------|-------|--------|
| I. Simplicity First | Single file, no premature abstractions | PASS |
| II. Code Quality | Type hints, docstrings, 88-char lines, ≤50 lines/function | PLANNED |
| III. User Experience | Clear prompts, color-coded messages, ○/✓ symbols | PLANNED |
| IV. Data Integrity | Unique IDs, validation before modification, no mutation in search/filter/sort | PLANNED |
| V. Explicit Over Implicit | No hidden side effects, explicit state passing | PLANNED |
| VI. Fail Fast and Clearly | Validate at entry, clear error messages | PLANNED |
| VII. Functional Style | Pure functions for data operations, new lists for sort/filter | PLANNED |
| VIII. Separation of Concerns | 5-layer architecture | PLANNED |
| IX. Testability | Small functions, injectable dependencies | PLANNED |
| X. Backward Compatibility | BASIC features unchanged, sensible defaults | PLANNED |

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
┌─────────────────────────────────────────────────────────────────────────┐
│                         APPLICATION LAYER                                │
│                             main()                                       │
│  - Initialize tasks list                                                 │
│  - Display 11-option menu                                               │
│  - Dispatch to appropriate command function                              │
│  - Loop until exit                                                       │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         COMMAND LAYER (cmd_*)                            │
│  BASIC:        cmd_add, cmd_list, cmd_update, cmd_delete, cmd_toggle    │
│  INTERMEDIATE: cmd_set_priority, cmd_manage_tags, cmd_search,           │
│                cmd_filter, cmd_sort                                      │
│  - Parse user input                                                      │
│  - Call validation layer                                                 │
│  - Call data layer on success                                            │
│  - Call display layer to show results                                    │
└───────────┬───────────────────────────────────────────┬─────────────────┘
            │                                           │
            ▼                                           ▼
┌─────────────────────────────────┐   ┌───────────────────────────────────┐
│      VALIDATION LAYER           │   │          DATA LAYER                │
│  BASIC:                         │   │  BASIC:                            │
│   validate_title                │   │   get_next_id, create_task         │
│   validate_description          │   │   get_task_by_id, delete_task      │
│   validate_task_id              │   │   update_task_description          │
│   validate_task_exists          │   │   toggle_task_status               │
│  INTERMEDIATE:                  │   │  INTERMEDIATE:                     │
│   validate_priority             │   │   set_priority, add_tag            │
│   validate_tag                  │   │   remove_tag, search_tasks         │
│   validate_tag_not_duplicate    │   │   filter_tasks, sort_tasks         │
│   validate_tag_exists           │   │                                    │
│                                 │   │                                    │
│  Returns: (bool, str | value)   │   │  Returns: dict|list|bool|None      │
└─────────────────────────────────┘   └───────────────────────────────────┘
                                                        │
                                                        ▼
                                      ┌───────────────────────────────────┐
                                      │         DISPLAY LAYER              │
                                      │  display_menu, display_header      │
                                      │  display_tasks (with colors)       │
                                      │  display_priority_with_color       │
                                      │  display_success, display_error    │
                                      │  format_task_row, truncate_text    │
                                      │                                    │
                                      │  Prints to stdout with ANSI colors │
                                      └───────────────────────────────────┘
```

### Data Flow Through Layers

```
User Input → Application → Command → Validation → Data → Display → User Output
                 ↑                        ↓
                 └────────── Loop ────────┘
```

---

## 2. Module Breakdown

### 2.1 Constants (Module-Level)

```python
# Status constants (boolean in data, symbols in display)
SYMBOL_INCOMPLETE: str = "○"
SYMBOL_COMPLETE: str = "✓"

# Priority constants
PRIORITY_HIGH: str = "high"
PRIORITY_MEDIUM: str = "medium"
PRIORITY_LOW: str = "low"
VALID_PRIORITIES: list[str] = [PRIORITY_HIGH, PRIORITY_MEDIUM, PRIORITY_LOW]

# Color constants (ANSI escape codes)
COLOR_RED: str = "\033[91m"      # High priority, errors
COLOR_YELLOW: str = "\033[93m"   # Medium priority
COLOR_GREEN: str = "\033[92m"    # Low priority, success
COLOR_RESET: str = "\033[0m"     # Reset to default

# Validation constants
MAX_TITLE_LENGTH: int = 100
MAX_DESCRIPTION_LENGTH: int = 200
MAX_TAG_LENGTH: int = 20
MIN_TAG_LENGTH: int = 1
DISPLAY_TRUNCATE_LENGTH: int = 20

# Menu constants (11 options)
MENU_ADD: str = "1"
MENU_LIST: str = "2"
MENU_UPDATE: str = "3"
MENU_DELETE: str = "4"
MENU_TOGGLE: str = "5"
MENU_SET_PRIORITY: str = "6"
MENU_MANAGE_TAGS: str = "7"
MENU_SEARCH: str = "8"
MENU_FILTER: str = "9"
MENU_SORT: str = "10"
MENU_EXIT: str = "11"

VALID_MENU_CHOICES: list[str] = [
    MENU_ADD, MENU_LIST, MENU_UPDATE, MENU_DELETE, MENU_TOGGLE,
    MENU_SET_PRIORITY, MENU_MANAGE_TAGS, MENU_SEARCH, MENU_FILTER,
    MENU_SORT, MENU_EXIT
]

# Display constants
SEPARATOR: str = "=" * 72
```

### 2.2 Layer Summary Table

| Layer | Functions | BASIC | INTERMEDIATE | Total |
|-------|-----------|-------|--------------|-------|
| Application | main | 1 | 0 (update) | 1 |
| Command | cmd_* | 5 | 5 | 10 |
| Validation | validate_* | 4 | 4 | 8 |
| Data | CRUD + ops | 7 | 6 | 13 |
| Display | display_* | 7 | 2 | 9 |
| **Total** | | **24** | **17** | **41** |

---

## 3. Complete Function Signatures

### 3.1 NEW Functions (INTERMEDIATE)

#### Data Layer - Priority

```python
def set_priority(tasks: list[dict], task_id: int, priority: str) -> bool:
    """Set the priority of a task.

    Args:
        tasks: The list of task dictionaries.
        task_id: The ID of the task to update.
        priority: The new priority value (must be pre-validated).

    Returns:
        True if task found and priority updated, False if task not found.

    Side Effects:
        Mutates the task's priority field in the tasks list.

    Example:
        >>> set_priority(tasks, 1, "high")
        True
    """
```

#### Data Layer - Tags

```python
def add_tag(tasks: list[dict], task_id: int, tag: str) -> bool:
    """Add a tag to a task.

    Args:
        tasks: The list of task dictionaries.
        task_id: The ID of the task.
        tag: The tag to add (must be pre-validated, lowercase, no duplicates).

    Returns:
        True if tag added successfully, False if task not found.

    Side Effects:
        Appends tag to the task's tags list.

    Example:
        >>> add_tag(tasks, 1, "work")
        True
    """


def remove_tag(tasks: list[dict], task_id: int, tag: str) -> bool:
    """Remove a tag from a task.

    Args:
        tasks: The list of task dictionaries.
        task_id: The ID of the task.
        tag: The tag to remove (case-insensitive match).

    Returns:
        True if tag found and removed, False if task/tag not found.

    Side Effects:
        Removes tag from the task's tags list.

    Example:
        >>> remove_tag(tasks, 1, "work")
        True
    """
```

#### Data Layer - Search/Filter/Sort

```python
def search_tasks(tasks: list[dict], query: str) -> list[dict]:
    """Search tasks by title or description.

    Performs case-insensitive partial matching on both title and description.

    Args:
        tasks: The list of task dictionaries to search.
        query: The search string (case-insensitive).

    Returns:
        New list containing matching tasks (does NOT mutate original).

    Example:
        >>> results = search_tasks(tasks, "buy")
        >>> len(results)  # Tasks with "buy" in title or description
        2
    """


def filter_tasks(
    tasks: list[dict],
    status: bool | None = None,
    priority: str | None = None,
    tag: str | None = None
) -> list[dict]:
    """Filter tasks by status, priority, and/or tag.

    All provided filters are combined with AND logic.

    Args:
        tasks: The list of task dictionaries to filter.
        status: Filter by completed status (True/False) or None for any.
        priority: Filter by priority ("high"/"medium"/"low") or None for any.
        tag: Filter by tag or None for any.

    Returns:
        New list containing matching tasks (does NOT mutate original).

    Example:
        >>> filter_tasks(tasks, status=False, priority="high")
        [{"id": 1, "completed": False, "priority": "high", ...}]
    """


def sort_tasks(
    tasks: list[dict],
    key: str,
    reverse: bool = False
) -> list[dict]:
    """Sort tasks by a specified key.

    Args:
        tasks: The list of task dictionaries to sort.
        key: Sort key - "date", "priority", or "title".
        reverse: If True, sort in descending order.

    Returns:
        New sorted list (does NOT mutate original).

    Notes:
        - "date" sorts by created_at
        - "priority" uses order: high=1, medium=2, low=3
        - "title" uses alphabetical order (case-insensitive)

    Example:
        >>> sorted_tasks = sort_tasks(tasks, "priority", reverse=False)
        # Returns high priority first, then medium, then low
    """
```

#### Validation Layer - Priority & Tags

```python
def validate_priority(priority: str) -> tuple[bool, str]:
    """Validate a priority value.

    Checks that priority is one of: high, medium, low (case-insensitive).

    Args:
        priority: The raw priority input from user.

    Returns:
        (True, normalized_priority) on success where priority is lowercase.
        (False, error_message) on failure.

    Example:
        >>> validate_priority("HIGH")
        (True, "high")
        >>> validate_priority("urgent")
        (False, "Error: Priority must be high, medium, or low")
    """


def validate_tag(tag: str) -> tuple[bool, str]:
    """Validate a tag format and length.

    Args:
        tag: The raw tag input from user.

    Returns:
        (True, normalized_tag) on success where tag is lowercase.
        (False, error_message) on failure.

    Rules:
        - 1-20 characters after trimming
        - Alphanumeric and hyphens only
        - No spaces
        - Converted to lowercase

    Example:
        >>> validate_tag("WORK")
        (True, "work")
        >>> validate_tag("has space")
        (False, "Error: Tag must be alphanumeric and hyphens only.")
    """


def validate_tag_not_duplicate(task: dict, tag: str) -> tuple[bool, str]:
    """Check if tag already exists on task.

    Args:
        task: The task dictionary.
        tag: The normalized tag to check.

    Returns:
        (True, "") if tag is not a duplicate.
        (False, error_message) if tag already exists.

    Example:
        >>> validate_tag_not_duplicate(task, "work")
        (False, "Error: Tag 'work' already exists on this task.")
    """


def validate_tag_exists(task: dict, tag: str) -> tuple[bool, str]:
    """Check if tag exists on task (for removal).

    Args:
        task: The task dictionary.
        tag: The normalized tag to check.

    Returns:
        (True, "") if tag exists.
        (False, error_message) if tag not found.

    Example:
        >>> validate_tag_exists(task, "urgent")
        (False, "Error: Tag 'urgent' not found on this task.")
    """
```

#### Command Layer - New Commands

```python
def cmd_set_priority(tasks: list[dict]) -> None:
    """Handle the set priority command.

    Flow:
        1. Check if tasks exist
        2. Prompt for task ID
        3. Validate task ID and existence
        4. Show current priority
        5. Prompt for new priority
        6. Validate priority
        7. Update task
        8. Display success message

    Args:
        tasks: The list of task dictionaries (mutated on success).

    Side Effects:
        - Reads from stdin (input prompts)
        - Writes to stdout (prompts, success/error messages)
        - Mutates task priority on success
    """


def cmd_manage_tags(tasks: list[dict]) -> None:
    """Handle the manage tags command with submenu.

    Submenu options:
        1. Add Tag
        2. Remove Tag
        3. View Task Tags
        4. Back to Main Menu

    Args:
        tasks: The list of task dictionaries (mutated on add/remove).

    Side Effects:
        - Reads from stdin
        - Writes to stdout
        - Mutates task tags list on add/remove
    """


def cmd_search_tasks(tasks: list[dict]) -> None:
    """Handle the search tasks command.

    Flow:
        1. Check if tasks exist
        2. Prompt for search query
        3. Validate query not empty
        4. Search tasks by title and description
        5. Display matching tasks or "no matches" message

    Args:
        tasks: The list of task dictionaries (NOT mutated).

    Side Effects:
        - Reads from stdin
        - Writes to stdout
    """


def cmd_filter_tasks(tasks: list[dict]) -> None:
    """Handle the filter tasks command with submenu.

    Submenu options:
        1. Filter by Status (Complete/Incomplete)
        2. Filter by Priority (High/Medium/Low)
        3. Filter by Tag
        4. Show All Tasks
        5. Back to Main Menu

    Args:
        tasks: The list of task dictionaries (NOT mutated).

    Side Effects:
        - Reads from stdin
        - Writes to stdout
    """


def cmd_sort_tasks(tasks: list[dict]) -> None:
    """Handle the sort tasks command with submenu.

    Submenu options:
        1. Sort by Creation Date (Newest First)
        2. Sort by Creation Date (Oldest First)
        3. Sort by Priority (High to Low)
        4. Sort by Priority (Low to High)
        5. Sort by Title (A-Z)
        6. Sort by Title (Z-A)
        7. Back to Main Menu

    Args:
        tasks: The list of task dictionaries (NOT mutated).

    Side Effects:
        - Reads from stdin
        - Writes to stdout (displays sorted results)
    """
```

#### Display Layer - New Functions

```python
def display_priority_with_color(priority: str) -> str:
    """Format priority with appropriate ANSI color.

    Args:
        priority: The priority value (high, medium, low).

    Returns:
        Colored priority string for terminal display.

    Example:
        >>> display_priority_with_color("high")
        '\033[91mHIGH\033[0m'  # Red "HIGH"
    """


def display_submenu(title: str, options: list[str]) -> None:
    """Display a submenu with header and options.

    Args:
        title: The submenu title (e.g., "MANAGE TAGS").
        options: List of option strings to display.

    Side Effects:
        Prints submenu to stdout.
    """
```

### 3.2 UPDATED Functions (BASIC → INTERMEDIATE)

```python
def create_task(
    tasks: list[dict],
    title: str,
    next_id: int,
    description: str = ""
) -> dict:
    """Create a new task and add it to the task list.

    UPDATED: Now includes priority and tags fields with defaults.

    Args:
        tasks: The list of task dictionaries (will be mutated).
        title: The task title (should be pre-validated).
        next_id: The unique ID to assign to this task.
        description: Optional task description.

    Returns:
        The newly created task dictionary with all 7 fields.

    Side Effects:
        Appends new task to tasks list.

    Default Values:
        - priority: "medium"
        - tags: []
        - completed: False
    """


def display_tasks(tasks: list[dict]) -> None:
    """Display all tasks in a formatted table.

    UPDATED: Now includes Priority and Tags columns with color coding.

    Table format:
        ID | Status | Priority | Title | Tags | Created

    Args:
        tasks: The list of task dictionaries to display.

    Side Effects:
        Prints formatted table to stdout.

    Notes:
        - Status shows ○ (incomplete) or ✓ (complete)
        - Priority shows colored text (RED/YELLOW/GREEN)
        - Tags are comma-separated
        - Title truncated to 20 chars
    """


def display_menu() -> None:
    """Display the main menu with all available options.

    UPDATED: Now shows 11 options instead of 6.

    Side Effects:
        Prints menu to stdout.
    """


def format_task_row(task: dict) -> str:
    """Format a single task as a table row.

    UPDATED: Now includes priority (colored) and tags columns.

    Args:
        task: The task dictionary to format.

    Returns:
        Formatted string for the table row.
    """
```

### 3.3 RETAINED Functions (BASIC - Unchanged)

The following functions remain unchanged from BASIC level:

**Data Layer:**
- `get_next_id(tasks: list[dict]) -> int`
- `get_task_by_id(tasks: list[dict], task_id: int) -> dict | None`
- `update_task_description(tasks: list[dict], task_id: int, new_description: str) -> bool`
- `delete_task(tasks: list[dict], task_id: int) -> bool`
- `toggle_task_status(tasks: list[dict], task_id: int) -> tuple[bool, str]`

**Validation Layer:**
- `validate_title(title: str) -> tuple[bool, str]`
- `validate_description(description: str) -> tuple[bool, str]`
- `validate_task_id(task_id_str: str) -> tuple[bool, int | str]`
- `validate_task_exists(tasks: list[dict], task_id: int) -> tuple[bool, str]`

**Display Layer:**
- `display_header(title: str) -> None`
- `display_success(message: str) -> None`
- `display_error(message: str) -> None`
- `truncate_text(text: str, max_length: int) -> str`

**Command Layer:**
- `cmd_add(tasks: list[dict]) -> None`
- `cmd_list(tasks: list[dict]) -> None`
- `cmd_update(tasks: list[dict]) -> None`
- `cmd_delete(tasks: list[dict]) -> None`
- `cmd_toggle(tasks: list[dict]) -> None`

---

## 4. Data Flow Diagrams

### 4.1 Set Priority Flow

```
┌──────────────────────────────────────────────────────────────────┐
│                    cmd_set_priority(tasks)                        │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │ tasks empty?        │──Yes──► display_error()
                   └─────────────────────┘         "No tasks available"
                              │ No                        │
                              ▼                           │
                   ┌─────────────────────┐                │
                   │ input("Task ID: ")  │                │
                   └─────────────────────┘                │
                              │                           │
                              ▼                           │
                   ┌─────────────────────┐                │
                   │ validate_task_id()  │──Fail──► display_error()
                   └─────────────────────┘                │
                              │ Pass                      │
                              ▼                           │
                   ┌─────────────────────┐                │
                   │ validate_task_exists│──Fail──► display_error()
                   └─────────────────────┘                │
                              │ Pass                      │
                              ▼                           │
                   ┌─────────────────────┐                │
                   │ Show current priority│               │
                   │ "Current: medium"    │               │
                   └─────────────────────┘                │
                              │                           │
                              ▼                           │
                   ┌─────────────────────┐                │
                   │ input("Priority: ") │                │
                   └─────────────────────┘                │
                              │                           │
                              ▼                           │
                   ┌─────────────────────┐                │
                   │ validate_priority() │──Fail──► display_error()
                   └─────────────────────┘                │
                              │ Pass                      │
                              ▼                           │
                   ┌─────────────────────┐                │
                   │ set_priority(task)  │                │
                   └─────────────────────┘                │
                              │                           │
                              ▼                           │
                   ┌─────────────────────┐                │
                   │ display_success()   │                │
                   │ "✓ Priority set"    │◄───────────────┘
                   └─────────────────────┘
                              │
                              ▼
                       Return to menu
```

### 4.2 Add Tag Flow

```
┌──────────────────────────────────────────────────────────────────┐
│                 cmd_manage_tags → Add Tag                         │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │ input("Task ID: ")  │
                   └─────────────────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │ validate_task_id()  │──Fail──► display_error()
                   └─────────────────────┘                │
                              │ Pass                      │
                              ▼                           │
                   ┌─────────────────────┐                │
                   │ validate_task_exists│──Fail──► display_error()
                   └─────────────────────┘                │
                              │ Pass                      │
                              ▼                           │
                   ┌─────────────────────┐                │
                   │ Show current tags   │                │
                   └─────────────────────┘                │
                              │                           │
                              ▼                           │
                   ┌─────────────────────┐                │
                   │ input("Tag: ")      │                │
                   └─────────────────────┘                │
                              │                           │
                              ▼                           │
                   ┌─────────────────────┐                │
                   │ validate_tag()      │──Fail──► display_error()
                   └─────────────────────┘     (format error)
                              │ Pass                      │
                              ▼                           │
                   ┌─────────────────────┐                │
                   │ validate_tag_not_   │──Fail──► display_error()
                   │ duplicate()         │     (duplicate error)
                   └─────────────────────┘                │
                              │ Pass                      │
                              ▼                           │
                   ┌─────────────────────┐                │
                   │ add_tag(task, tag)  │                │
                   └─────────────────────┘                │
                              │                           │
                              ▼                           │
                   ┌─────────────────────┐                │
                   │ display_success()   │◄───────────────┘
                   │ "✓ Tag added"       │
                   └─────────────────────┘
```

### 4.3 Search Tasks Flow

```
┌──────────────────────────────────────────────────────────────────┐
│                    cmd_search_tasks(tasks)                        │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │ tasks empty?        │──Yes──► display_error()
                   └─────────────────────┘         "No tasks to search"
                              │ No                        │
                              ▼                           │
                   ┌─────────────────────┐                │
                   │ input("Query: ")    │                │
                   └─────────────────────┘                │
                              │                           │
                              ▼                           │
                   ┌─────────────────────┐                │
                   │ query.strip() empty?│──Yes──► display_error()
                   └─────────────────────┘     "Query cannot be empty"
                              │ No                        │
                              ▼                           │
                   ┌─────────────────────┐                │
                   │ search_tasks(query) │                │
                   │ (returns new list)  │                │
                   └─────────────────────┘                │
                              │                           │
                              ▼                           │
                   ┌─────────────────────┐                │
                   │ results empty?      │──Yes──► print "No matches"
                   └─────────────────────┘                │
                              │ No                        │
                              ▼                           │
                   ┌─────────────────────┐                │
                   │ display_tasks(      │◄───────────────┘
                   │   results)          │
                   └─────────────────────┘
```

### 4.4 Filter Tasks Flow

```
┌──────────────────────────────────────────────────────────────────┐
│                    cmd_filter_tasks(tasks)                        │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │ Display filter menu │
                   │ 1. Status           │
                   │ 2. Priority         │
                   │ 3. Tag              │
                   │ 4. Show All         │
                   │ 5. Back             │
                   └─────────────────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │ choice == "1"?      │──Yes──► prompt for status
                   └─────────────────────┘         filter_tasks(status=X)
                              │ No                 display_tasks(results)
                              ▼
                   ┌─────────────────────┐
                   │ choice == "2"?      │──Yes──► prompt for priority
                   └─────────────────────┘         validate_priority()
                              │ No                 filter_tasks(priority=X)
                              ▼
                   ┌─────────────────────┐
                   │ choice == "3"?      │──Yes──► prompt for tag
                   └─────────────────────┘         filter_tasks(tag=X)
                              │ No
                              ▼
                   ┌─────────────────────┐
                   │ choice == "4"?      │──Yes──► display_tasks(tasks)
                   └─────────────────────┘
                              │ No
                              ▼
                       Return to menu
```

### 4.5 Sort Tasks Flow

```
┌──────────────────────────────────────────────────────────────────┐
│                     cmd_sort_tasks(tasks)                         │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │ Display sort menu   │
                   │ 1. Date (Newest)    │
                   │ 2. Date (Oldest)    │
                   │ 3. Priority (H→L)   │
                   │ 4. Priority (L→H)   │
                   │ 5. Title (A-Z)      │
                   │ 6. Title (Z-A)      │
                   │ 7. Back             │
                   └─────────────────────┘
                              │
                              ▼
                   ┌─────────────────────────────────────┐
                   │ Map choice to (key, reverse):      │
                   │ 1 → ("date", True)                 │
                   │ 2 → ("date", False)                │
                   │ 3 → ("priority", False)            │
                   │ 4 → ("priority", True)             │
                   │ 5 → ("title", False)               │
                   │ 6 → ("title", True)                │
                   └─────────────────────────────────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │ sorted_tasks =      │
                   │ sort_tasks(tasks,   │
                   │   key, reverse)     │
                   │ (returns new list)  │
                   └─────────────────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │ display_tasks(      │
                   │   sorted_tasks)     │
                   └─────────────────────┘
                              │
                              ▼
                       Return to menu
```

---

## 5. Implementation Sequence

### Phase-by-Phase Order

| Phase | Description | Functions | Dependencies |
|-------|-------------|-----------|--------------|
| 1 | Enhanced Data Model | update `create_task` | None |
| 2 | New Validations | `validate_priority`, `validate_tag`, `validate_tag_not_duplicate`, `validate_tag_exists` | None |
| 3 | Data Ops - Priority | `set_priority` | Phase 2 |
| 4 | Data Ops - Tags | `add_tag`, `remove_tag` | Phase 2 |
| 5 | Data Ops - Search/Filter/Sort | `search_tasks`, `filter_tasks`, `sort_tasks` | None |
| 6 | Display Enhancements | update `display_tasks`, `display_priority_with_color`, `format_task_row` | None |
| 7 | Command - Priority | `cmd_set_priority` | Phases 2, 3, 6 |
| 8 | Command - Tags | `cmd_manage_tags` | Phases 2, 4, 6 |
| 9 | Command - Search/Filter/Sort | `cmd_search_tasks`, `cmd_filter_tasks`, `cmd_sort_tasks` | Phases 5, 6 |
| 10 | Main Menu Update | update `display_menu`, `main` | Phases 7, 8, 9 |

### Detailed Phase Breakdown

**Phase 1: Enhanced Data Model**
```python
# Update create_task to include new fields
task = {
    "id": next_id,
    "title": title,
    "description": description,
    "completed": False,
    "created_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
    "priority": "medium",   # NEW - default
    "tags": []              # NEW - default empty list
}
```

**Phase 2: New Validations**
```python
def validate_priority(priority: str) -> tuple[bool, str]:
    cleaned = priority.strip().lower()
    if cleaned not in VALID_PRIORITIES:
        return False, "Error: Priority must be high, medium, or low"
    return True, cleaned

def validate_tag(tag: str) -> tuple[bool, str]:
    cleaned = tag.strip().lower()
    if not cleaned:
        return False, "Error: Tag cannot be empty."
    if len(cleaned) > MAX_TAG_LENGTH:
        return False, f"Error: Tag must be 1-{MAX_TAG_LENGTH} characters."
    if not all(c.isalnum() or c == '-' for c in cleaned):
        return False, "Error: Tag must be alphanumeric and hyphens only."
    return True, cleaned
```

**Phase 5: Search/Filter/Sort (Pure Functions)**
```python
def search_tasks(tasks: list[dict], query: str) -> list[dict]:
    query_lower = query.lower()
    return [
        task for task in tasks
        if query_lower in task["title"].lower()
        or query_lower in task["description"].lower()
    ]

def sort_tasks(tasks: list[dict], key: str, reverse: bool = False) -> list[dict]:
    if key == "priority":
        priority_order = {"high": 1, "medium": 2, "low": 3}
        return sorted(tasks, key=lambda t: priority_order[t["priority"]],
                     reverse=reverse)
    elif key == "date":
        return sorted(tasks, key=lambda t: t["created_at"], reverse=reverse)
    else:  # title
        return sorted(tasks, key=lambda t: t["title"].lower(), reverse=reverse)
```

---

## 6. Design Decisions

### 6.1 Default Priority = "medium"

**Decision**: New tasks default to priority "medium".

**Rationale**:
- Most common priority level (neutral)
- High and Low are exceptional cases
- Users can adjust if needed
- Matches user expectations

### 6.2 Tags as List[str] not Set[str]

**Decision**: Tags stored as `list[str]` not `set`.

**Rationale**:
- Preserves insertion order (user control)
- JSON-serializable (future persistence)
- Manual duplicate prevention via validation
- Simpler display logic

### 6.3 Case-Insensitive Search

**Decision**: Search is case-insensitive.

**Rationale**:
- Better user experience
- Users don't remember exact casing
- Industry standard behavior
- No performance impact for in-memory data

### 6.4 Sort Returns New List

**Decision**: `sort_tasks()` returns a new list, does not mutate original.

**Rationale**:
- Functional programming principle
- Predictable behavior
- User can view sorted without losing original order
- Prevents accidental data corruption
- Constitution Principle VII requirement

### 6.5 ANSI Color Codes

**Decision**: Use ANSI escape codes for colors.

**Rationale**:
- Works in most terminals (Windows 10+, macOS, Linux)
- No external dependencies
- Easy to disable if needed
- Standard approach

**Color Mapping**:
| Priority | ANSI Code | Color |
|----------|-----------|-------|
| high | `\033[91m` | Red |
| medium | `\033[93m` | Yellow |
| low | `\033[92m` | Green |

---

## 7. Testing Strategy

### 7.1 Manual Testing Checklist

#### Set Priority
- [ ] Set priority to "high" - displays in RED
- [ ] Set priority to "medium" - displays in YELLOW
- [ ] Set priority to "low" - displays in GREEN
- [ ] Case-insensitive input ("HIGH", "High", "high")
- [ ] Invalid priority shows error
- [ ] Invalid task ID shows error
- [ ] Empty task list shows error

#### Manage Tags
- [ ] Add tag to task - appears in View Tasks
- [ ] Add duplicate tag - shows error
- [ ] Add tag with space - shows error
- [ ] Add tag with special chars - shows error
- [ ] Add tag > 20 chars - shows error
- [ ] Remove existing tag - removed from list
- [ ] Remove non-existent tag - shows error
- [ ] View tags on task - shows all tags

#### Search
- [ ] Search matches title
- [ ] Search matches description
- [ ] Search is case-insensitive
- [ ] Partial match works
- [ ] No matches shows message
- [ ] Empty query shows error

#### Filter
- [ ] Filter by complete status
- [ ] Filter by incomplete status
- [ ] Filter by priority
- [ ] Filter by tag
- [ ] Show all clears filter
- [ ] No matches shows message

#### Sort
- [ ] Sort by date (newest first)
- [ ] Sort by date (oldest first)
- [ ] Sort by priority (high to low)
- [ ] Sort by priority (low to high)
- [ ] Sort by title (A-Z)
- [ ] Sort by title (Z-A)
- [ ] Original list unchanged after sort

#### Backward Compatibility
- [ ] Add Task creates with priority="medium", tags=[]
- [ ] View Tasks shows new columns
- [ ] Update Task works unchanged
- [ ] Delete Task works unchanged
- [ ] Toggle Complete works unchanged

---

## 8. Backward Compatibility Strategy

### Data Model Extensions

| Field | BASIC | INTERMEDIATE | Backward Compatible |
|-------|-------|--------------|---------------------|
| id | int | int | Yes |
| title | str | str | Yes |
| description | str | str | Yes |
| completed | bool | bool | Yes (was "status") |
| created_at | str | str | Yes |
| priority | - | str | Yes (default "medium") |
| tags | - | list[str] | Yes (default []) |

### Menu Extensions

| Option | BASIC | INTERMEDIATE |
|--------|-------|--------------|
| 1-5 | Add, View, Update, Delete, Toggle | Unchanged |
| 6-10 | - | Priority, Tags, Search, Filter, Sort |
| 11 | Exit (was 6) | Exit |

### Behavior Preservation

- All BASIC commands (1-5) work identically
- New fields have sensible defaults
- No breaking changes to existing data operations
- New features are additive only

---

## 9. Error Handling Architecture

### Validation Layer Pattern

```python
def validate_X(input: str) -> tuple[bool, str]:
    """
    Returns:
        (True, cleaned_value) on success
        (False, error_message) on failure
    """
```

### Command Layer Pattern

```python
def cmd_X(tasks: list[dict]) -> None:
    # 1. Check preconditions
    if not tasks:
        display_error("Error: No tasks available. Add a task first.")
        return

    # 2. Get and validate input
    user_input = input("Enter value: ")
    valid, result = validate_X(user_input)
    if not valid:
        display_error(result)
        return

    # 3. Perform operation
    success = data_operation(tasks, result)

    # 4. Display result
    if success:
        display_success("Operation completed successfully.")
```

### Error Display

```python
def display_error(message: str) -> None:
    """Display error in red."""
    print(f"\n{COLOR_RED}{message}{COLOR_RESET}")

def display_success(message: str) -> None:
    """Display success in green."""
    print(f"\n{COLOR_GREEN}{message}{COLOR_RESET}")
```

---

## 10. Integration Points

### Layer Dependencies

```
Application → Command → Validation
                    └─→ Data
                    └─→ Display

Display ← Command (for output)
```

### Main Loop Integration

```python
def main() -> None:
    tasks: list[dict] = []

    while True:
        display_menu()
        choice = input("Enter your choice (1-11): ").strip()

        if choice == MENU_ADD:
            cmd_add(tasks)
        elif choice == MENU_LIST:
            cmd_list(tasks)
        # ... BASIC commands ...
        elif choice == MENU_SET_PRIORITY:
            cmd_set_priority(tasks)
        elif choice == MENU_MANAGE_TAGS:
            cmd_manage_tags(tasks)
        elif choice == MENU_SEARCH:
            cmd_search_tasks(tasks)
        elif choice == MENU_FILTER:
            cmd_filter_tasks(tasks)
        elif choice == MENU_SORT:
            cmd_sort_tasks(tasks)
        elif choice == MENU_EXIT:
            print(f"\n{COLOR_GREEN}Goodbye!{COLOR_RESET}")
            break
        else:
            display_error("Invalid choice. Please select 1-11.")
```

---

## Project Structure

### Source Code

```text
todo.py                    # Single file with all code (41 functions)
```

### Documentation (this feature)

```text
specs/001-console-todo-app/
├── spec.md               # Requirements specification (INTERMEDIATE)
├── plan.md               # This implementation plan
├── data-model.md         # Data model documentation
├── quickstart.md         # Quick start guide
├── checklists/
│   └── requirements.md   # Spec quality checklist
└── tasks.md              # Implementation tasks (generated by /sp.tasks)
```

---

## Complexity Tracking

No constitution violations. All requirements met with single-file implementation.

| Requirement | Implementation | Status |
|-------------|----------------|--------|
| Single file | todo.py only | PASS |
| No dependencies | Standard library only | PASS |
| Type hints | All functions | PLANNED |
| Docstrings | All functions | PLANNED |
| 88-char lines | Code formatted | PLANNED |
| ≤50 lines/function | Split as needed | PLANNED |

---

**Version**: 2.0.0 | **Created**: 2025-12-29 | **Level**: INTERMEDIATE
