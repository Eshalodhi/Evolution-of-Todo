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

# Color constants
GREEN: str = "\033[92m"
RESET: str = "\033[0m"

# Validation constants
MAX_TITLE_LENGTH: int = 100
MAX_DESCRIPTION_LENGTH: int = 200
DISPLAY_TRUNCATE_LENGTH: int = 50

# Menu constants
MENU_ADD: str = "1"
MENU_LIST: str = "2"
MENU_UPDATE: str = "3"
MENU_DELETE: str = "4"
MENU_TOGGLE: str = "5"
MENU_EXIT: str = "6"
VALID_MENU_CHOICES: list[str] = [
    MENU_ADD, MENU_LIST, MENU_UPDATE, MENU_DELETE, MENU_TOGGLE, MENU_EXIT
]

# Display constants
SEPARATOR: str = "=" * 72
TABLE_HEADER: str = (
    "ID  | Title                | Description            | Status    | Created"
)
TABLE_DIVIDER: str = (
    "----|----------------------|------------------------|-----------|-----------------"
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


def format_task_row(task: dict) -> str:
    """Format a single task as a table row.

    Args:
        task: The task dictionary to format.

    Returns:
        A formatted string representing the task as a table row.
    """
    task_id = task["id"]
    title = truncate_text(task["title"], 20)
    description = truncate_text(task.get("description", ""), 22)
    status = task["status"]
    created_at = task["created_at"][:16].replace("T", " ")
    return f"{task_id:<4}| {title:<20} | {description:<22} | {status:<9} | {created_at}"


def display_menu() -> None:
    """Display the main menu with all available options."""
    display_header("TODO APPLICATION")
    print()
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Toggle Complete/Incomplete")
    print("6. Exit")
    print()


def display_tasks(tasks: list[dict]) -> None:
    """Display all tasks in a formatted table.

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
        The newly created task dictionary.
    """
    task = {
        "id": next_id,
        "title": title,
        "description": description,
        "status": STATUS_PENDING,
        "created_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
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


# =============================================================================
# APPLICATION LAYER
# =============================================================================

def main() -> None:
    """Main entry point for the todo application.

    Initializes the task list, runs the main menu loop until exit.
    """
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
            print(f"\n{GREEN}Thank you for using the Console Todo Application. "
                  f"Goodbye!{RESET}")
            break
        else:
            display_error(
                "Error: Invalid choice. Please select a number from the menu (1-6)."
            )


if __name__ == "__main__":
    main()
