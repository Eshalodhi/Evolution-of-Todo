"""Console Todo Application - Phase I.

A command-line todo application that allows users to manage tasks through
a menu-driven interface. Implements add, view, update, delete, and toggle
status operations with in-memory storage.

Panaversity Hackathon II - Spec-Driven Development
"""

from datetime import datetime


# =============================================================================
# CONSTANTS
# =============================================================================

# Status constants
STATUS_PENDING: str = "pending"
STATUS_COMPLETED: str = "completed"

# Status symbol constants (T036)
SYMBOL_INCOMPLETE: str = "○"
SYMBOL_COMPLETE: str = "✓"

# Color constants (T034)
COLOR_RED: str = "\033[91m"
COLOR_YELLOW: str = "\033[93m"
COLOR_GREEN: str = "\033[92m"
COLOR_RESET: str = "\033[0m"

# Legacy color aliases for backward compatibility
GREEN: str = COLOR_GREEN
RESET: str = COLOR_RESET

# Priority constants (T033)
PRIORITY_HIGH: str = "high"
PRIORITY_MEDIUM: str = "medium"
PRIORITY_LOW: str = "low"
VALID_PRIORITIES: list[str] = [PRIORITY_HIGH, PRIORITY_MEDIUM, PRIORITY_LOW]

# Priority display colors mapping
PRIORITY_COLORS: dict[str, str] = {
    PRIORITY_HIGH: COLOR_RED,
    PRIORITY_MEDIUM: COLOR_YELLOW,
    PRIORITY_LOW: COLOR_GREEN,
}

# Priority sort order (high=0, medium=1, low=2)
PRIORITY_ORDER: dict[str, int] = {
    PRIORITY_HIGH: 0,
    PRIORITY_MEDIUM: 1,
    PRIORITY_LOW: 2,
}

# Validation constants
MAX_TITLE_LENGTH: int = 100
MAX_DESCRIPTION_LENGTH: int = 200
DISPLAY_TRUNCATE_LENGTH: int = 50

# Tag validation constants (T035)
MAX_TAG_LENGTH: int = 20
MIN_TAG_LENGTH: int = 1

# Menu constants (T037)
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
SEPARATOR: str = "=" * 100
TABLE_HEADER: str = (
    "ID  | Status | Priority | Title              | Description        | Tags         | Created"
)
TABLE_DIVIDER: str = (
    "----|--------|----------|--------------------|--------------------|--------------|----------------"
)


# =============================================================================
# DISPLAY LAYER
# =============================================================================

def truncate_text(text: str, max_length: int) -> str:
    """Truncate text to a maximum length, adding '...' if truncated.

    Args:
        text: The text to potentially truncate.
        max_length: Maximum length including the '...' suffix.

    Returns:
        The original text if short enough, or truncated text with '...'.
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def display_header(title: str) -> None:
    """Display a section header with decorative borders.

    Args:
        title: The title text to display centered.
    """
    print()
    print(SEPARATOR)
    print(f"{title:^40}")
    print(SEPARATOR)


def display_error(message: str) -> None:
    """Display an error message.

    Args:
        message: The error message to display.
    """
    print(f"\n{message}")


def display_success(message: str) -> None:
    """Display a success message.

    Args:
        message: The success message to display.
    """
    print(f"\n{message}")


def display_priority_with_color(priority: str) -> str:
    """Return priority string with ANSI color coding.

    Args:
        priority: The priority value (high, medium, low).

    Returns:
        Colored priority string: red=high, yellow=medium, green=low.
    """
    color = PRIORITY_COLORS.get(priority, COLOR_RESET)
    display_text = priority.upper() if priority == PRIORITY_HIGH else priority
    return f"{color}{display_text:<8}{COLOR_RESET}"


def display_submenu(title: str, options: list[str]) -> None:
    """Display a formatted submenu with header and numbered options.

    Args:
        title: The submenu title to display.
        options: List of option strings to display numbered.
    """
    print()
    print(SEPARATOR)
    print(f"{title:^72}")
    print(SEPARATOR)
    print()
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    print()


def format_task_row(task: dict) -> str:
    """Format a single task as a table row with status, priority, description, and tags.

    Args:
        task: The task dictionary to format.

    Returns:
        A formatted string representing the task as a table row.
    """
    task_id = task["id"]
    # Status symbol with color
    if task["status"] == STATUS_COMPLETED:
        status_symbol = f"{COLOR_GREEN}{SYMBOL_COMPLETE}{COLOR_RESET}"
    else:
        status_symbol = f"{COLOR_RED}{SYMBOL_INCOMPLETE}{COLOR_RESET}"
    # Priority with color
    priority = task.get("priority", PRIORITY_MEDIUM)
    priority_display = display_priority_with_color(priority)
    # Title truncated
    title = truncate_text(task["title"], 18)
    # Description - show "—" if empty
    description = task.get("description", "")
    description_display = truncate_text(description, 18) if description else "—"
    # Tags comma-separated
    tags = task.get("tags", [])
    tags_display = ", ".join(tags) if tags else ""
    tags_display = truncate_text(tags_display, 12)
    # Created timestamp
    created_at = task["created_at"][:16].replace("T", " ")
    return (
        f"{task_id:<4}| {status_symbol:<15} | {priority_display} | {title:<18} | "
        f"{description_display:<18} | {tags_display:<12} | {created_at}"
    )


def display_menu() -> None:
    """Display the main menu with all available options (11 options)."""
    display_header("TODO APPLICATION")
    print()
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Toggle Complete/Incomplete")
    print("6. Set Priority")
    print("7. Manage Tags")
    print("8. Search Tasks")
    print("9. Filter Tasks")
    print("10. Sort Tasks")
    print("11. Exit")
    print()


def display_tasks(tasks: list[dict]) -> None:
    """Display all tasks in a formatted table with 6 columns.

    Shows appropriate message if no tasks exist.

    Args:
        tasks: The list of task dictionaries to display.
    """
    display_header("YOUR TASKS")

    if not tasks:
        print()
        print("No tasks found. Use 'Add Task' to create your first task.")
        return

    print(TABLE_HEADER)
    print(TABLE_DIVIDER)

    for task in tasks:
        print(format_task_row(task))

    print(SEPARATOR)

    pending_count = sum(1 for t in tasks if t["status"] == STATUS_PENDING)
    completed_count = len(tasks) - pending_count
    print(f"Total: {len(tasks)} tasks ({pending_count} pending, "
          f"{completed_count} completed)")


# =============================================================================
# VALIDATION LAYER
# =============================================================================

def validate_title(title: str) -> tuple[bool, str]:
    """Validate a task title.

    Checks that title is non-empty (after trimming) and within length limit.

    Args:
        title: The raw title input from user.

    Returns:
        (True, trimmed_title) on success.
        (False, error_message) on failure.
    """
    trimmed = title.strip()

    if not trimmed:
        return (
            False,
            "Error: Title cannot be empty. Please provide a task title."
        )

    if len(trimmed) > MAX_TITLE_LENGTH:
        return (
            False,
            f"Error: Title too long ({len(trimmed)} chars). "
            f"Maximum is {MAX_TITLE_LENGTH}."
        )

    return True, trimmed


def validate_description(description: str) -> tuple[bool, str]:
    """Validate a task description.

    Checks that description is non-empty (after trimming) and within length
    limit.

    Args:
        description: The raw description input from user.

    Returns:
        (True, trimmed_description) on success.
        (False, error_message) on failure.
    """
    trimmed = description.strip()

    if not trimmed:
        return (
            False,
            "Error: Description cannot be empty. Please provide a task description."
        )

    if len(trimmed) > MAX_DESCRIPTION_LENGTH:
        return (
            False,
            f"Error: Description too long ({len(trimmed)} chars). "
            f"Maximum is {MAX_DESCRIPTION_LENGTH}."
        )

    return True, trimmed


def validate_task_id(task_id_str: str) -> tuple[bool, int | str]:
    """Validate and parse a task ID string.

    Args:
        task_id_str: The raw task ID input from user.

    Returns:
        (True, parsed_id) on success where parsed_id is int.
        (False, error_message) on failure where error_message is str.
    """
    stripped = task_id_str.strip()

    if not stripped:
        return False, "Error: Task ID cannot be empty. Please enter a valid ID."

    if not stripped.isdigit() or stripped == "0":
        return (
            False,
            "Error: Task ID must be a positive number. "
            "Please enter a valid ID like '1' or '2'."
        )

    return True, int(stripped)


def validate_task_exists(tasks: list[dict], task_id: int) -> tuple[bool, str]:
    """Check if a task with the given ID exists.

    Args:
        tasks: The list of task dictionaries.
        task_id: The ID to check.

    Returns:
        (True, "") on success.
        (False, error_message) on failure.
    """
    for task in tasks:
        if task["id"] == task_id:
            return True, ""

    return (
        False,
        f"Error: Task {task_id} not found. Use 'View Tasks' to see available task IDs."
    )


def validate_priority(priority: str) -> tuple[bool, str]:
    """Validate a priority value.

    Accepts high/medium/low case-insensitive, returns normalized lowercase.

    Args:
        priority: The raw priority input from user.

    Returns:
        (True, normalized_priority) on success.
        (False, error_message) on failure.
    """
    normalized = priority.strip().lower()

    if not normalized:
        return False, "Error: Priority must be high, medium, or low."

    if normalized not in VALID_PRIORITIES:
        return False, "Error: Priority must be high, medium, or low."

    return True, normalized


def validate_tag(tag: str) -> tuple[bool, str]:
    """Validate a tag format.

    Tags must be 1-20 characters, alphanumeric and hyphens only.

    Args:
        tag: The raw tag input from user.

    Returns:
        (True, normalized_tag) on success.
        (False, error_message) on failure.
    """
    normalized = tag.strip().lower()

    if not normalized:
        return False, "Error: Tag cannot be empty."

    if len(normalized) > MAX_TAG_LENGTH:
        return (
            False,
            f"Error: Tag must be 1-20 characters. Got {len(normalized)}."
        )

    # Check alphanumeric and hyphens only
    for char in normalized:
        if not (char.isalnum() or char == '-'):
            return (
                False,
                "Error: Tag must be alphanumeric and hyphens only. No spaces allowed."
            )

    return True, normalized


def validate_tag_not_duplicate(task: dict, tag: str) -> tuple[bool, str]:
    """Check if a tag already exists on a task.

    Args:
        task: The task dictionary to check.
        tag: The normalized tag to check for.

    Returns:
        (True, "") if tag does not exist (valid to add).
        (False, error_message) if tag already exists.
    """
    if tag in task.get("tags", []):
        return False, f"Error: Tag '{tag}' already exists on this task."
    return True, ""


def validate_tag_exists(task: dict, tag: str) -> tuple[bool, str]:
    """Check if a tag exists on a task for removal.

    Args:
        task: The task dictionary to check.
        tag: The normalized tag to check for.

    Returns:
        (True, "") if tag exists (valid to remove).
        (False, error_message) if tag does not exist.
    """
    tags = task.get("tags", [])
    if not tags:
        return False, "Error: This task has no tags."
    if tag not in tags:
        return False, f"Error: Tag '{tag}' not found on this task."
    return True, ""


# =============================================================================
# DATA LAYER
# =============================================================================

def get_next_id(tasks: list[dict]) -> int:
    """Calculate the next available task ID.

    Uses max(existing_ids) + 1 to ensure deleted IDs are never reused.
    Returns 1 if no tasks exist.

    Args:
        tasks: The list of task dictionaries.

    Returns:
        The next available unique task ID.
    """
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


def get_task_by_id(tasks: list[dict], task_id: int) -> dict | None:
    """Find a task by its ID.

    Args:
        tasks: The list of task dictionaries to search.
        task_id: The ID of the task to find.

    Returns:
        The task dictionary if found, None otherwise.
    """
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def create_task(
    tasks: list[dict],
    title: str,
    next_id: int,
    description: str = ""
) -> dict:
    """Create a new task and add it to the task list.

    Args:
        tasks: The list of task dictionaries (will be mutated).
        title: The task title (should be pre-validated).
        next_id: The unique ID to assign to this task.
        description: The optional task description (should be pre-validated).

    Returns:
        The newly created task dictionary with priority and tags defaults.
    """
    task = {
        "id": next_id,
        "title": title,
        "description": description,
        "status": STATUS_PENDING,
        "created_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "priority": PRIORITY_MEDIUM,
        "tags": []
    }
    tasks.append(task)
    return task


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
    task = get_task_by_id(tasks, task_id)
    if task is None:
        return False
    task["description"] = new_description
    return True


def delete_task(tasks: list[dict], task_id: int) -> bool:
    """Remove a task from the list.

    Args:
        tasks: The list of task dictionaries (will be mutated).
        task_id: The ID of the task to delete.

    Returns:
        True if task was found and deleted, False otherwise.
    """
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return True
    return False


def toggle_task_status(tasks: list[dict], task_id: int) -> tuple[bool, str]:
    """Toggle a task's status between pending and completed.

    Args:
        tasks: The list of task dictionaries.
        task_id: The ID of the task to toggle.

    Returns:
        Tuple of (success, new_status). On failure, new_status is empty string.
    """
    task = get_task_by_id(tasks, task_id)
    if task is None:
        return False, ""

    if task["status"] == STATUS_PENDING:
        task["status"] = STATUS_COMPLETED
    else:
        task["status"] = STATUS_PENDING

    return True, task["status"]


def set_priority(tasks: list[dict], task_id: int, priority: str) -> bool:
    """Set a task's priority level.

    Args:
        tasks: The list of task dictionaries.
        task_id: The ID of the task to update.
        priority: The new priority value (should be pre-validated).

    Returns:
        True if task was found and updated, False otherwise.
    """
    task = get_task_by_id(tasks, task_id)
    if task is None:
        return False
    task["priority"] = priority
    return True


def add_tag(tasks: list[dict], task_id: int, tag: str) -> bool:
    """Add a tag to a task.

    Args:
        tasks: The list of task dictionaries.
        task_id: The ID of the task to update.
        tag: The normalized tag to add (should be pre-validated).

    Returns:
        True if task was found and tag added, False otherwise.
    """
    task = get_task_by_id(tasks, task_id)
    if task is None:
        return False
    if "tags" not in task:
        task["tags"] = []
    task["tags"].append(tag)
    return True


def remove_tag(tasks: list[dict], task_id: int, tag: str) -> bool:
    """Remove a tag from a task.

    Args:
        tasks: The list of task dictionaries.
        task_id: The ID of the task to update.
        tag: The normalized tag to remove (should be pre-validated).

    Returns:
        True if task was found and tag removed, False otherwise.
    """
    task = get_task_by_id(tasks, task_id)
    if task is None:
        return False
    if "tags" in task and tag in task["tags"]:
        task["tags"].remove(tag)
        return True
    return False


def search_tasks(tasks: list[dict], query: str) -> list[dict]:
    """Search tasks by keyword in title or description.

    Case-insensitive partial match on both title and description.

    Args:
        tasks: The list of task dictionaries to search.
        query: The search query string.

    Returns:
        A NEW list of matching tasks (does not mutate original).
    """
    query_lower = query.lower()
    results = []
    for task in tasks:
        title_match = query_lower in task["title"].lower()
        desc_match = query_lower in task.get("description", "").lower()
        if title_match or desc_match:
            results.append(task)
    return results


def filter_tasks(
    tasks: list[dict],
    status: bool | None = None,
    priority: str | None = None,
    tag: str | None = None
) -> list[dict]:
    """Filter tasks by status, priority, and/or tag.

    Uses AND logic when multiple filters are specified.

    Args:
        tasks: The list of task dictionaries to filter.
        status: If True, show completed. If False, show pending. None = no filter.
        priority: Filter by priority value (high/medium/low). None = no filter.
        tag: Filter by tag. None = no filter.

    Returns:
        A NEW list of matching tasks (does not mutate original).
    """
    results = []
    for task in tasks:
        # Status filter
        if status is not None:
            task_completed = task["status"] == STATUS_COMPLETED
            if task_completed != status:
                continue
        # Priority filter
        if priority is not None:
            if task.get("priority", PRIORITY_MEDIUM) != priority:
                continue
        # Tag filter
        if tag is not None:
            if tag not in task.get("tags", []):
                continue
        results.append(task)
    return results


def sort_tasks(
    tasks: list[dict],
    key: str,
    reverse: bool = False
) -> list[dict]:
    """Sort tasks by date, priority, or title.

    Uses stable sort to preserve relative order of equal elements.

    Args:
        tasks: The list of task dictionaries to sort.
        key: Sort key - "date", "priority", or "title".
        reverse: If True, sort in descending order.

    Returns:
        A NEW sorted list (does not mutate original).
    """
    if key == "date":
        return sorted(tasks, key=lambda t: t["created_at"], reverse=reverse)
    elif key == "priority":
        # Use priority order mapping: high=0, medium=1, low=2
        return sorted(
            tasks,
            key=lambda t: PRIORITY_ORDER.get(
                t.get("priority", PRIORITY_MEDIUM), 1
            ),
            reverse=reverse
        )
    elif key == "title":
        return sorted(
            tasks,
            key=lambda t: t["title"].lower(),
            reverse=reverse
        )
    return list(tasks)  # Return a copy if unknown key


# =============================================================================
# COMMAND LAYER
# =============================================================================

def cmd_add(tasks: list[dict]) -> None:
    """Handle the add task command.

    Prompts for title (required) and description (optional), validates,
    creates task, displays result.

    Args:
        tasks: The list of task dictionaries (will be mutated on success).
    """
    # Get and validate title (required)
    title_input = input("Enter title: ")

    valid, result = validate_title(title_input)
    if not valid:
        display_error(result)
        return

    title = result

    # Get and validate description (optional)
    description_input = input("Enter description (optional, press Enter to skip): ")
    description = ""

    if description_input.strip():
        valid, result = validate_description(description_input)
        if not valid:
            display_error(result)
            return
        description = result

    # Create the task
    next_id = get_next_id(tasks)
    task = create_task(tasks, title, next_id, description)

    display_success(f"{GREEN}Task #{task['id']} '{title}' created!{RESET}")


def cmd_list(tasks: list[dict]) -> None:
    """Handle the list tasks command.

    Displays all tasks in a formatted table.

    Args:
        tasks: The list of task dictionaries to display.
    """
    display_tasks(tasks)


def cmd_update(tasks: list[dict]) -> None:
    """Handle the update task command.

    Prompts for task ID and new description, validates, updates, displays
    result.

    Args:
        tasks: The list of task dictionaries (will be mutated on success).
    """
    if not tasks:
        display_error("Error: No tasks available. Add a task first.")
        return

    task_id_input = input("Enter task ID to update: ")

    valid, result = validate_task_id(task_id_input)
    if not valid:
        display_error(result)
        return

    task_id = result

    exists, error_msg = validate_task_exists(tasks, task_id)
    if not exists:
        display_error(error_msg)
        return

    description_input = input("Enter new description: ")

    valid, result = validate_description(description_input)
    if not valid:
        display_error(result)
        return

    new_description = result
    update_task_description(tasks, task_id, new_description)

    display_success(f"Task {task_id} updated: {new_description}")


def cmd_delete(tasks: list[dict]) -> None:
    """Handle the delete task command.

    Prompts for task ID, validates, deletes, displays result.

    Args:
        tasks: The list of task dictionaries (will be mutated on success).
    """
    if not tasks:
        display_error("Error: No tasks available. Add a task first.")
        return

    task_id_input = input("Enter task ID to delete: ")

    valid, result = validate_task_id(task_id_input)
    if not valid:
        display_error(result)
        return

    task_id = result

    exists, error_msg = validate_task_exists(tasks, task_id)
    if not exists:
        display_error(error_msg)
        return

    delete_task(tasks, task_id)

    display_success(f"Task {task_id} deleted successfully.")


def cmd_toggle(tasks: list[dict]) -> None:
    """Handle the toggle status command.

    Prompts for task ID, shows confirmation with task title, toggles status
    on confirmation, displays result.

    Args:
        tasks: The list of task dictionaries (will be mutated on success).
    """
    if not tasks:
        display_error("Error: No tasks available. Add a task first.")
        return

    task_id_input = input("Enter task ID to toggle: ")

    valid, result = validate_task_id(task_id_input)
    if not valid:
        display_error(result)
        return

    task_id = result

    exists, error_msg = validate_task_exists(tasks, task_id)
    if not exists:
        display_error(error_msg)
        return

    # Get the task to show title and current status
    task = get_task_by_id(tasks, task_id)
    title = task["title"]
    current_status = task["status"]

    # Ask for confirmation based on current status
    if current_status == STATUS_PENDING:
        confirm = input(f"Mark task '{title}' as completed? (Y/n): ")
        new_status_word = "completed"
    else:
        confirm = input(f"Mark task '{title}' as incomplete? (Y/n): ")
        new_status_word = "incomplete"

    # Check confirmation (y/yes/Enter = yes, anything else = cancel)
    confirm_lower = confirm.strip().lower()
    if confirm_lower not in ("", "y", "yes"):
        print("\nOperation cancelled.")
        return

    # Toggle the status
    success, new_status = toggle_task_status(tasks, task_id)

    display_success(f"{GREEN}Task '{title}' marked as {new_status_word}!{RESET}")


def cmd_set_priority(tasks: list[dict]) -> None:
    """Handle the set priority command.

    Prompts for task ID, shows current priority, validates new priority,
    updates, and shows success message.

    Args:
        tasks: The list of task dictionaries (will be mutated on success).
    """
    if not tasks:
        display_error("Error: No tasks available. Add a task first.")
        return

    task_id_input = input("Enter task ID: ")

    valid, result = validate_task_id(task_id_input)
    if not valid:
        display_error(result)
        return

    task_id = result

    exists, error_msg = validate_task_exists(tasks, task_id)
    if not exists:
        display_error(error_msg)
        return

    task = get_task_by_id(tasks, task_id)
    current_priority = task.get("priority", PRIORITY_MEDIUM)
    print(f"\nCurrent priority: {current_priority}")

    priority_input = input("Enter new priority (high/medium/low): ")

    valid, result = validate_priority(priority_input)
    if not valid:
        display_error(result)
        return

    new_priority = result
    set_priority(tasks, task_id, new_priority)

    priority_display = new_priority.upper() if new_priority == PRIORITY_HIGH else new_priority
    display_success(
        f"{COLOR_GREEN}✓ Task {task_id} '{task['title']}' priority set to "
        f"{priority_display}{COLOR_RESET}"
    )


def cmd_manage_tags(tasks: list[dict]) -> None:
    """Handle the manage tags command with submenu.

    Provides submenu with options to add, remove, view tags, or return.

    Args:
        tasks: The list of task dictionaries (will be mutated on add/remove).
    """
    if not tasks:
        display_error("Error: No tasks available. Add a task first.")
        return

    while True:
        display_submenu("MANAGE TAGS", [
            "Add Tag",
            "Remove Tag",
            "View Task Tags",
            "Back to Main Menu"
        ])

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            # Add Tag
            task_id_input = input("Enter task ID: ")
            valid, result = validate_task_id(task_id_input)
            if not valid:
                display_error(result)
                continue
            task_id = result
            exists, error_msg = validate_task_exists(tasks, task_id)
            if not exists:
                display_error(error_msg)
                continue
            task = get_task_by_id(tasks, task_id)

            tag_input = input("Enter tag to add: ")
            valid, result = validate_tag(tag_input)
            if not valid:
                display_error(result)
                continue
            tag = result

            valid, error_msg = validate_tag_not_duplicate(task, tag)
            if not valid:
                display_error(error_msg)
                continue

            add_tag(tasks, task_id, tag)
            display_success(
                f"{COLOR_GREEN}✓ Tag '{tag}' added to task {task_id} "
                f"'{task['title']}'{COLOR_RESET}"
            )

        elif choice == "2":
            # Remove Tag
            task_id_input = input("Enter task ID: ")
            valid, result = validate_task_id(task_id_input)
            if not valid:
                display_error(result)
                continue
            task_id = result
            exists, error_msg = validate_task_exists(tasks, task_id)
            if not exists:
                display_error(error_msg)
                continue
            task = get_task_by_id(tasks, task_id)

            tag_input = input("Enter tag to remove: ")
            valid, result = validate_tag(tag_input)
            if not valid:
                display_error(result)
                continue
            tag = result

            valid, error_msg = validate_tag_exists(task, tag)
            if not valid:
                display_error(error_msg)
                continue

            remove_tag(tasks, task_id, tag)
            display_success(
                f"{COLOR_GREEN}✓ Tag '{tag}' removed from task {task_id} "
                f"'{task['title']}'{COLOR_RESET}"
            )

        elif choice == "3":
            # View Task Tags
            task_id_input = input("Enter task ID: ")
            valid, result = validate_task_id(task_id_input)
            if not valid:
                display_error(result)
                continue
            task_id = result
            exists, error_msg = validate_task_exists(tasks, task_id)
            if not exists:
                display_error(error_msg)
                continue
            task = get_task_by_id(tasks, task_id)
            tags = task.get("tags", [])
            if tags:
                print(f"\nTask {task_id} '{task['title']}' tags: {', '.join(tags)}")
            else:
                print(f"\nTask {task_id} '{task['title']}' has no tags")

        elif choice == "4":
            # Back to Main Menu
            break

        else:
            display_error("Error: Please select a valid option (1-4).")


def cmd_search_tasks(tasks: list[dict]) -> None:
    """Handle the search tasks command.

    Prompts for search query, validates, searches, displays results.

    Args:
        tasks: The list of task dictionaries (not mutated).
    """
    if not tasks:
        display_error("Error: No tasks available to search.")
        return

    query = input("Enter search query: ").strip()

    if not query:
        display_error("Error: Search query cannot be empty.")
        return

    results = search_tasks(tasks, query)

    if not results:
        print(f"\nNo tasks found matching '{query}'")
        return

    print(f"\n{COLOR_GREEN}Found {len(results)} task(s) matching '{query}'{COLOR_RESET}")
    display_tasks(results)


def cmd_filter_tasks(tasks: list[dict]) -> None:
    """Handle the filter tasks command with submenu.

    Provides submenu with filter options by status, priority, tag, or show all.

    Args:
        tasks: The list of task dictionaries (not mutated).
    """
    if not tasks:
        display_error("Error: No tasks available to filter.")
        return

    while True:
        display_submenu("FILTER TASKS", [
            "Filter by Status (Complete/Incomplete)",
            "Filter by Priority (High/Medium/Low)",
            "Filter by Tag",
            "Show All Tasks",
            "Back to Main Menu"
        ])

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            # Filter by Status
            status_choice = input("Select: 1. Complete  2. Incomplete: ").strip()
            if status_choice == "1":
                results = filter_tasks(tasks, status=True)
                filter_desc = "completed"
            elif status_choice == "2":
                results = filter_tasks(tasks, status=False)
                filter_desc = "incomplete"
            else:
                display_error("Error: Please select 1 for Complete or 2 for Incomplete.")
                continue

            if not results:
                print(f"\nNo {filter_desc} tasks found.")
            else:
                print(f"\n{COLOR_GREEN}Showing {len(results)} {filter_desc} task(s){COLOR_RESET}")
                display_tasks(results)

        elif choice == "2":
            # Filter by Priority
            priority_input = input("Enter priority (high/medium/low): ")
            valid, result = validate_priority(priority_input)
            if not valid:
                display_error(result)
                continue
            priority = result
            results = filter_tasks(tasks, priority=priority)

            if not results:
                print(f"\nNo tasks found with priority '{priority}'")
            else:
                print(f"\n{COLOR_GREEN}Showing {len(results)} task(s) with priority '{priority}'{COLOR_RESET}")
                display_tasks(results)

        elif choice == "3":
            # Filter by Tag
            tag_input = input("Enter tag to filter by: ")
            valid, result = validate_tag(tag_input)
            if not valid:
                display_error(result)
                continue
            tag = result
            results = filter_tasks(tasks, tag=tag)

            if not results:
                print(f"\nNo tasks found with tag '{tag}'")
            else:
                print(f"\n{COLOR_GREEN}Showing {len(results)} task(s) with tag '{tag}'{COLOR_RESET}")
                display_tasks(results)

        elif choice == "4":
            # Show All Tasks
            display_tasks(tasks)

        elif choice == "5":
            # Back to Main Menu
            break

        else:
            display_error("Error: Please select a valid option (1-5).")


def cmd_sort_tasks(tasks: list[dict]) -> None:
    """Handle the sort tasks command with submenu.

    Provides submenu with 7 sort options. Returns a sorted view without
    mutating the original list.

    Args:
        tasks: The list of task dictionaries (not mutated).
    """
    if not tasks:
        display_error("Error: No tasks available to sort.")
        return

    while True:
        display_submenu("SORT TASKS", [
            "Sort by Creation Date (Newest First)",
            "Sort by Creation Date (Oldest First)",
            "Sort by Priority (High to Low)",
            "Sort by Priority (Low to High)",
            "Sort by Title (A-Z)",
            "Sort by Title (Z-A)",
            "Back to Main Menu"
        ])

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            # Date Newest First
            results = sort_tasks(tasks, key="date", reverse=True)
            print(f"\n{COLOR_GREEN}Tasks sorted by date (newest first){COLOR_RESET}")
            display_tasks(results)

        elif choice == "2":
            # Date Oldest First
            results = sort_tasks(tasks, key="date", reverse=False)
            print(f"\n{COLOR_GREEN}Tasks sorted by date (oldest first){COLOR_RESET}")
            display_tasks(results)

        elif choice == "3":
            # Priority High to Low
            results = sort_tasks(tasks, key="priority", reverse=False)
            print(f"\n{COLOR_GREEN}Tasks sorted by priority (high to low){COLOR_RESET}")
            display_tasks(results)

        elif choice == "4":
            # Priority Low to High
            results = sort_tasks(tasks, key="priority", reverse=True)
            print(f"\n{COLOR_GREEN}Tasks sorted by priority (low to high){COLOR_RESET}")
            display_tasks(results)

        elif choice == "5":
            # Title A-Z
            results = sort_tasks(tasks, key="title", reverse=False)
            print(f"\n{COLOR_GREEN}Tasks sorted by title (A-Z){COLOR_RESET}")
            display_tasks(results)

        elif choice == "6":
            # Title Z-A
            results = sort_tasks(tasks, key="title", reverse=True)
            print(f"\n{COLOR_GREEN}Tasks sorted by title (Z-A){COLOR_RESET}")
            display_tasks(results)

        elif choice == "7":
            # Back to Main Menu
            break

        else:
            display_error("Error: Please select a valid option (1-7).")


# =============================================================================
# APPLICATION LAYER
# =============================================================================

def main() -> None:
    """Main entry point for the todo application.

    Initializes the task list, runs the main menu loop until exit.
    Handles all 11 menu options for INTERMEDIATE level.
    """
    tasks: list[dict] = []

    while True:
        display_menu()
        choice = input("Enter your choice (1-11): ").strip()

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
            print(f"\n{COLOR_GREEN}Thank you for using the Console Todo Application. "
                  f"Goodbye!{COLOR_RESET}")
            break
        else:
            display_error(
                "Error: Invalid choice. Please select a number from the menu (1-11)."
            )


if __name__ == "__main__":
    main()
