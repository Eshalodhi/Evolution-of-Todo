# Quick Start Guide: Console Todo Application

**Version**: Phase I
**Date**: 2025-12-28

---

## Prerequisites

- Python 3.13 or higher installed
- Terminal/Command Prompt access

## Installation

No installation required. The application is a single Python file with no external dependencies.

```bash
# Clone the repository (if applicable)
git clone <repository-url>
cd TODO_APP

# Or simply ensure you have todo.py in your current directory
```

## Running the Application

```bash
python todo.py
```

Or on some systems:

```bash
python3 todo.py
```

## Basic Usage

When you start the application, you'll see the main menu:

```
========================================
           TODO APPLICATION
========================================

1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Toggle Complete/Incomplete
6. Exit

Enter your choice (1-6):
```

### Adding a Task

1. Select option `1` from the menu
2. Enter your task description (1-200 characters)
3. The system confirms with the assigned task ID

```
Enter your choice (1-6): 1
Enter task description: Buy groceries

Task 1 added: Buy groceries
```

### Viewing Tasks

Select option `2` to see all your tasks:

```
Enter your choice (1-6): 2

========================================
              YOUR TASKS
========================================
ID  | Description                        | Status    | Created
----|------------------------------------|-----------|-----------------
1   | Buy groceries                      | pending   | 2025-12-28 10:30
2   | Review pull request                | completed | 2025-12-28 09:15
========================================
Total: 2 tasks (1 pending, 1 completed)
```

### Marking a Task Complete

1. Select option `5` from the menu
2. Enter the task ID
3. The status toggles between pending and completed

```
Enter your choice (1-6): 5
Enter task ID to toggle: 1

Task 1 marked as completed.
```

### Updating a Task

1. Select option `3` from the menu
2. Enter the task ID
3. Enter the new description

```
Enter your choice (1-6): 3
Enter task ID to update: 1
Enter new description: Buy organic groceries

Task 1 updated: Buy organic groceries
```

### Deleting a Task

1. Select option `4` from the menu
2. Enter the task ID

```
Enter your choice (1-6): 4
Enter task ID to delete: 2

Task 2 deleted successfully.
```

### Exiting

Select option `6` to exit:

```
Enter your choice (1-6): 6
Goodbye!
```

## Important Notes

1. **No Persistence**: All tasks are stored in memory only. When you exit the application, all tasks are lost.

2. **Task IDs**: Each task gets a unique ID that is never reused, even after deletion.

3. **Description Length**: Task descriptions must be between 1 and 200 characters.

4. **Status Toggle**: The toggle command switches a task between "pending" and "completed" states.

## Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "Description cannot be empty" | Empty or whitespace-only description | Enter at least one character |
| "Description too long" | Over 200 characters | Shorten your description |
| "Task ID must be a number" | Non-numeric input for ID | Enter a number like 1 or 2 |
| "Task X not found" | ID doesn't exist | Use 'View Tasks' to see valid IDs |
| "No tasks available" | Empty task list | Add a task first |

## Keyboard Shortcuts

There are no keyboard shortcuts. All interaction is through the numbered menu system.

## Troubleshooting

### Python version error

If you see syntax errors, ensure you're using Python 3.13+:

```bash
python --version
```

### Permission denied

On Unix systems, you may need to make the file executable:

```bash
chmod +x todo.py
./todo.py
```

Or run with python explicitly:

```bash
python todo.py
```

## Next Steps

After Phase I, future phases may include:
- File persistence (save/load tasks)
- Due dates and priorities
- Categories and tags
- Search and filter functionality
