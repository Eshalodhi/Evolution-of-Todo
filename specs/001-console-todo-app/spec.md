# Feature Specification: Console Todo Application - Phase I

**Feature Branch**: `001-console-todo-app`
**Created**: 2025-12-28
**Status**: Draft
**Input**: Phase I console todo application for Panaversity Hackathon II

---

## 1. Project Overview

### Description

A command-line todo application that enables developers to manage their tasks directly from the terminal. The application provides a simple, menu-driven interface for creating, viewing, updating, completing, and deleting tasks. All data is stored in memory during the session.

### Target User

Developers and technical users who prefer working in the console environment and want a lightweight, no-frills task management solution without external dependencies or complex setup.

### Success Criteria for Phase I

- Users can perform all 5 core operations (add, view, update, delete, toggle status) without errors
- The application runs from a single Python file with no external dependencies
- All user interactions provide clear feedback (success messages, error messages with remediation)
- The application handles all edge cases gracefully without crashing

---

## 2. User Scenarios & Testing

### User Story 1 - Adding a Task (Priority: P1)

As a user, I want to add a new task to my list so that I can track work I need to complete.

**Why this priority**: Adding tasks is the foundational operation. Without it, the application has no purpose. This must work before any other feature can be used.

**Independent Test**: Run the app, select "Add Task", enter a description, verify the task appears in the list with a unique ID and "pending" status.

**Acceptance Scenarios**:

1. **Given** the main menu is displayed, **When** user selects "Add Task" and enters "Buy groceries", **Then** system creates a task with unique ID, description "Buy groceries", status "pending", and displays confirmation "Task 1 added: Buy groceries"

2. **Given** the add task prompt, **When** user enters a description with leading/trailing whitespace "  Clean room  ", **Then** system trims whitespace and creates task with description "Clean room"

3. **Given** the add task prompt, **When** user enters an empty description or only whitespace, **Then** system displays "Error: Description cannot be empty. Please provide a task description." and returns to menu

4. **Given** the add task prompt, **When** user enters a description longer than 200 characters, **Then** system displays "Error: Description too long (X chars). Maximum is 200 characters." and returns to menu

---

### User Story 2 - Viewing All Tasks (Priority: P1)

As a user, I want to see all my tasks in a formatted list so that I can understand what I need to do.

**Why this priority**: Viewing tasks is essential to understand current state. Tied with P1 because adding tasks without viewing them is not useful.

**Independent Test**: Add several tasks, select "View Tasks", verify all tasks display with ID, description, status, and creation time in a readable format.

**Acceptance Scenarios**:

1. **Given** 3 tasks exist in the list, **When** user selects "View Tasks", **Then** system displays a formatted table showing all tasks with columns: ID, Description, Status, Created

2. **Given** no tasks exist, **When** user selects "View Tasks", **Then** system displays "No tasks found. Use 'Add Task' to create your first task."

3. **Given** tasks with mixed statuses exist, **When** user selects "View Tasks", **Then** completed tasks show status as "completed" and pending tasks show status as "pending"

---

### User Story 3 - Marking Task Complete/Incomplete (Priority: P2)

As a user, I want to toggle a task's completion status so that I can track my progress.

**Why this priority**: After adding and viewing, marking completion is the most common operation. It provides immediate value by tracking progress.

**Independent Test**: Add a task, mark it complete, view tasks to verify status changed to "completed", toggle again to verify it returns to "pending".

**Acceptance Scenarios**:

1. **Given** a pending task with ID 1 exists, **When** user selects "Toggle Complete" and enters "1", **Then** system marks task as completed and displays "Task 1 marked as completed."

2. **Given** a completed task with ID 1 exists, **When** user selects "Toggle Complete" and enters "1", **Then** system marks task as pending and displays "Task 1 marked as pending."

3. **Given** no task with ID 99 exists, **When** user selects "Toggle Complete" and enters "99", **Then** system displays "Error: Task 99 not found. Use 'View Tasks' to see available task IDs."

4. **Given** the toggle prompt, **When** user enters non-numeric input "abc", **Then** system displays "Error: Task ID must be a number. Please enter a valid ID like '1' or '2'."

---

### User Story 4 - Updating a Task (Priority: P3)

As a user, I want to update a task's description so that I can correct mistakes or add details.

**Why this priority**: Updating is less common than adding or completing but still important for correcting mistakes.

**Independent Test**: Add a task with description "Buy milk", update it to "Buy almond milk", view tasks to verify the description changed.

**Acceptance Scenarios**:

1. **Given** a task with ID 1 and description "Buy milk" exists, **When** user selects "Update Task", enters "1", then enters "Buy almond milk", **Then** system updates description and displays "Task 1 updated: Buy almond milk"

2. **Given** the update prompt, **When** user enters a new description that is empty, **Then** system displays "Error: Description cannot be empty. Task not updated."

3. **Given** the update prompt, **When** user enters an invalid task ID, **Then** system displays appropriate error message with remediation

4. **Given** the update prompt for task ID, **When** user enters an ID that doesn't exist, **Then** system displays "Error: Task X not found. Use 'View Tasks' to see available task IDs."

---

### User Story 5 - Deleting a Task (Priority: P3)

As a user, I want to delete a task so that I can remove items I no longer need to track.

**Why this priority**: Deletion is a destructive operation and less common. Users typically complete tasks rather than delete them.

**Independent Test**: Add a task, delete it by ID, view tasks to verify it no longer appears in the list.

**Acceptance Scenarios**:

1. **Given** a task with ID 1 exists, **When** user selects "Delete Task" and enters "1", **Then** system removes the task and displays "Task 1 deleted successfully."

2. **Given** the delete prompt, **When** user enters an ID that doesn't exist, **Then** system displays "Error: Task X not found. Use 'View Tasks' to see available task IDs."

3. **Given** the delete prompt, **When** user enters non-numeric input, **Then** system displays "Error: Task ID must be a number. Please enter a valid ID like '1' or '2'."

4. **Given** a task is deleted, **When** a new task is added, **Then** the new task receives a new unique ID (deleted IDs are not reused)

---

### Edge Cases

- **Empty task list operations**: When list is empty, view/update/delete/toggle operations display appropriate "no tasks" message
- **Maximum description length**: Descriptions over 200 characters are rejected with clear error
- **Whitespace handling**: Leading/trailing whitespace in descriptions is trimmed; whitespace-only input is rejected
- **Invalid menu choice**: Non-menu inputs display "Invalid choice. Please select a number from the menu."
- **ID reuse prevention**: Deleted task IDs are never reassigned to new tasks
- **Numeric ID validation**: Non-numeric IDs show clear error with example of valid input

---

## 3. Functional Requirements

### Task Creation

- **FR-001**: System MUST allow users to create a new task by entering a description
- **FR-002**: System MUST assign a unique, auto-incrementing integer ID to each new task
- **FR-003**: System MUST set the initial status of new tasks to "pending"
- **FR-004**: System MUST record the creation timestamp in ISO 8601 format
- **FR-005**: System MUST trim leading and trailing whitespace from task descriptions
- **FR-006**: System MUST reject empty descriptions with a user-friendly error message

### Task Display

- **FR-007**: System MUST display all tasks in a formatted table with columns: ID, Description, Status, Created
- **FR-008**: System MUST display a friendly message when no tasks exist
- **FR-009**: System MUST truncate long descriptions in the display to maintain table formatting (show first 50 chars with "...")
- **FR-010**: System MUST display task status as human-readable text ("pending" or "completed")

### Task Modification

- **FR-011**: System MUST allow users to update a task's description by specifying its ID
- **FR-012**: System MUST validate that the new description is not empty
- **FR-013**: System MUST preserve the task's ID, status, and creation time when updating description
- **FR-014**: System MUST display confirmation after successful update

### Task Deletion

- **FR-015**: System MUST allow users to delete a task by specifying its ID
- **FR-016**: System MUST display confirmation after successful deletion
- **FR-017**: System MUST NOT reuse deleted task IDs for new tasks
- **FR-018**: System MUST display error if task ID does not exist

### Status Management

- **FR-019**: System MUST allow users to toggle a task's status between "pending" and "completed"
- **FR-020**: System MUST display confirmation showing the new status after toggle
- **FR-021**: System MUST validate that the task ID exists before toggling

### Menu and Navigation

- **FR-022**: System MUST display a numbered menu with all available operations
- **FR-023**: System MUST accept numeric input to select menu options
- **FR-024**: System MUST provide an "Exit" option to quit the application
- **FR-025**: System MUST display the menu again after each operation completes
- **FR-026**: System MUST handle invalid menu selections with a clear error message

### Error Handling

- **FR-027**: System MUST validate all user input before processing
- **FR-028**: System MUST display error messages that explain what went wrong
- **FR-029**: System MUST include remediation instructions in all error messages
- **FR-030**: System MUST never crash due to invalid user input
- **FR-031**: System MUST NOT display stack traces to users

---

## 4. Non-Functional Requirements

### Performance

- **NFR-001**: All operations MUST complete within 100 milliseconds (perceived as instant)
- **NFR-002**: Application MUST start within 1 second
- **NFR-003**: Memory usage MUST remain reasonable for typical usage (hundreds of tasks)

### Usability

- **NFR-004**: Menu options MUST be clearly labeled and numbered
- **NFR-005**: All prompts MUST clearly indicate what input is expected
- **NFR-006**: Error messages MUST be understandable by non-technical users
- **NFR-007**: Success messages MUST confirm what action was taken

### Reliability

- **NFR-008**: Application MUST handle any user input without crashing
- **NFR-009**: Data MUST remain consistent after any operation (no partial updates)
- **NFR-010**: Invalid operations MUST NOT affect existing data

### Maintainability

- **NFR-011**: Code MUST follow constitution.md standards (type hints, docstrings, etc.)
- **NFR-012**: Code MUST be organized into clear layers (command, validation, data, display)
- **NFR-013**: All code MUST reside in a single todo.py file

---

## 5. Acceptance Criteria by Feature

### Feature: Add Task

- [x] User can add a task by entering a description
- [x] System assigns a unique auto-incrementing ID starting from 1
- [x] System sets status to "pending" automatically
- [x] System records creation timestamp
- [x] System trims whitespace from description
- [x] System rejects empty descriptions with clear error
- [x] System rejects descriptions over 200 characters with clear error
- [x] System displays confirmation with task ID after successful add

### Feature: View Tasks

- [x] User can view all tasks in a formatted table
- [x] Table shows ID, Description (truncated if needed), Status, Created columns
- [x] System displays friendly message when no tasks exist
- [x] Pending tasks show "pending" status
- [x] Completed tasks show "completed" status

### Feature: Update Task

- [x] User can update a task's description by specifying ID
- [x] System validates task ID exists
- [x] System validates new description is not empty
- [x] System validates new description is not over 200 characters
- [x] System preserves task ID, status, and creation time
- [x] System displays confirmation after successful update
- [x] System displays error for invalid ID with remediation

### Feature: Delete Task

- [x] User can delete a task by specifying ID
- [x] System validates task ID exists
- [x] System removes task from list
- [x] System displays confirmation after successful delete
- [x] Deleted IDs are never reused
- [x] System displays error for invalid ID with remediation

### Feature: Toggle Complete/Incomplete

- [x] User can toggle status by specifying task ID
- [x] Pending tasks become completed
- [x] Completed tasks become pending
- [x] System validates task ID exists
- [x] System displays confirmation with new status
- [x] System displays error for invalid ID with remediation

### Feature: Menu Navigation

- [x] Main menu displays all options with numbers
- [x] User can select option by entering number
- [x] Invalid selection shows clear error
- [x] Menu redisplays after each operation
- [x] Exit option terminates application cleanly

---

## 6. Data Model

### Task Entity

| Field        | Type   | Required | Constraints                          | Default     |
| ------------ | ------ | -------- | ------------------------------------ | ----------- |
| id           | int    | Yes      | Positive integer, unique, never reused | Auto-assigned |
| description  | str    | Yes      | 1-200 characters, trimmed            | N/A         |
| status       | str    | Yes      | "pending" or "completed" only        | "pending"   |
| created_at   | str    | Yes      | ISO 8601 format (YYYY-MM-DDTHH:MM:SS) | Current time |

### Example Task Objects

```python
# Newly created task
{
    "id": 1,
    "description": "Buy groceries",
    "status": "pending",
    "created_at": "2025-12-28T10:30:00"
}

# Completed task
{
    "id": 2,
    "description": "Review pull request",
    "status": "completed",
    "created_at": "2025-12-28T09:15:00"
}

# Task with maximum length description
{
    "id": 3,
    "description": "This is a task with exactly two hundred characters which is the maximum allowed length for a task description in this application and should be accepted by the validation layer without errors",
    "status": "pending",
    "created_at": "2025-12-28T11:00:00"
}
```

### Status Constants

| Constant          | Value       | Description                    |
| ----------------- | ----------- | ------------------------------ |
| STATUS_PENDING    | "pending"   | Task not yet completed         |
| STATUS_COMPLETED  | "completed" | Task finished                  |

---

## 7. Validation Rules

### Title/Description Validation

| Rule                  | Validation                                      | Error Message                                                    |
| --------------------- | ----------------------------------------------- | ---------------------------------------------------------------- |
| Not empty             | len(description.strip()) > 0                    | "Error: Description cannot be empty. Please provide a task description." |
| Maximum length        | len(description.strip()) <= 200                 | "Error: Description too long (X chars). Maximum is 200 characters." |
| Whitespace handling   | description = description.strip()               | N/A (automatic trimming)                                         |

### Task ID Validation

| Rule                  | Validation                                      | Error Message                                                    |
| --------------------- | ----------------------------------------------- | ---------------------------------------------------------------- |
| Numeric format        | input.isdigit() or int(input) works             | "Error: Task ID must be a number. Please enter a valid ID like '1' or '2'." |
| Positive integer      | int(input) > 0                                  | "Error: Task ID must be a positive number."                      |
| Task exists           | task with ID exists in list                     | "Error: Task X not found. Use 'View Tasks' to see available task IDs." |

### Menu Input Validation

| Rule                  | Validation                                      | Error Message                                                    |
| --------------------- | ----------------------------------------------- | ---------------------------------------------------------------- |
| Valid menu option     | input in valid_options                          | "Invalid choice. Please select a number from the menu."          |
| Numeric format        | input.isdigit()                                 | "Invalid choice. Please select a number from the menu."          |

---

## 8. User Interface Specification

### Main Menu Layout

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

### Task List Display Format

```
========================================
              YOUR TASKS
========================================
ID  | Description                        | Status    | Created
----|------------------------------------|-----------|-----------------
1   | Buy groceries                      | pending   | 2025-12-28 10:30
2   | Review pull request                | completed | 2025-12-28 09:15
3   | This is a long description that... | pending   | 2025-12-28 11:00
========================================
Total: 3 tasks (2 pending, 1 completed)
```

### Empty Task List Display

```
========================================
              YOUR TASKS
========================================
No tasks found. Use 'Add Task' to create your first task.
========================================
```

### Input Prompts

| Operation              | Prompt Text                                      |
| ---------------------- | ------------------------------------------------ |
| Add Task               | "Enter task description: "                       |
| Update Task (ID)       | "Enter task ID to update: "                      |
| Update Task (Desc)     | "Enter new description: "                        |
| Delete Task            | "Enter task ID to delete: "                      |
| Toggle Status          | "Enter task ID to toggle: "                      |

### Success Messages

| Operation              | Message Format                                   |
| ---------------------- | ------------------------------------------------ |
| Add Task               | "Task {id} added: {description}"                 |
| Update Task            | "Task {id} updated: {new_description}"           |
| Delete Task            | "Task {id} deleted successfully."                |
| Mark Complete          | "Task {id} marked as completed."                 |
| Mark Pending           | "Task {id} marked as pending."                   |

### Error Messages

| Scenario               | Message                                                         |
| ---------------------- | --------------------------------------------------------------- |
| Empty description      | "Error: Description cannot be empty. Please provide a task description." |
| Description too long   | "Error: Description too long ({n} chars). Maximum is 200 characters." |
| Invalid task ID format | "Error: Task ID must be a number. Please enter a valid ID like '1' or '2'." |
| Task not found         | "Error: Task {id} not found. Use 'View Tasks' to see available task IDs." |
| Invalid menu choice    | "Invalid choice. Please select a number from the menu."         |

---

## 9. Edge Cases & Error Scenarios

### Empty Task List Scenarios

| Operation        | Behavior                                                        |
| ---------------- | --------------------------------------------------------------- |
| View Tasks       | Display "No tasks found. Use 'Add Task' to create your first task." |
| Update Task      | Display "No tasks available. Add a task first."                 |
| Delete Task      | Display "No tasks available. Add a task first."                 |
| Toggle Status    | Display "No tasks available. Add a task first."                 |

### Invalid Input Scenarios

| Input Type       | Invalid Input Examples | Handling                                         |
| ---------------- | ---------------------- | ------------------------------------------------ |
| Menu choice      | "7", "abc", "", "-1"   | Show "Invalid choice. Please select a number from the menu." |
| Task ID          | "abc", "0", "-1", ""   | Show "Error: Task ID must be a number..."        |
| Description      | "", "   ", None        | Show "Error: Description cannot be empty..."     |

### Boundary Conditions

| Boundary                 | Value  | Behavior                                        |
| ------------------------ | ------ | ----------------------------------------------- |
| Description min length   | 1 char | Accept (after trim)                             |
| Description max length   | 200 chars | Accept                                       |
| Description over max     | 201+ chars | Reject with length error                    |
| First task ID            | 1      | Auto-assigned to first task                     |
| Task ID after deletion   | N+1    | Continue incrementing, never reuse deleted IDs  |

### Special Character Handling

| Input                    | Behavior                                        |
| ------------------------ | ----------------------------------------------- |
| Unicode characters       | Accept and display correctly                    |
| Special chars (!@#$%)    | Accept in descriptions                          |
| Newlines in description  | Not possible (single-line input)                |
| Very long input (>200)   | Reject with clear length error                  |

---

## 10. Out of Scope for Phase I

The following features are explicitly **NOT** included in Phase I:

### Data Persistence
- No file saving/loading
- No database storage
- Data exists only in memory during session
- All tasks are lost when application exits

### Multi-User Features
- No user accounts
- No authentication
- No authorization
- Single user, single session

### Advanced Task Features
- No due dates
- No priorities (beyond status)
- No categories or tags
- No subtasks
- No task dependencies
- No recurring tasks

### Interface Features
- No web interface
- No API
- No GUI
- Console/terminal only

### Integration Features
- No network communication
- No external service integration
- No import/export functionality
- No notifications

### Advanced Display Features
- No color coding (plain text only)
- No sorting options
- No filtering options
- No search functionality

---

## Assumptions

The following assumptions were made in creating this specification:

1. **Single session usage**: Users understand that data is not persisted between sessions
2. **Console familiarity**: Users are comfortable with command-line interfaces
3. **Standard input**: Users will interact via keyboard input only
4. **Terminal support**: User's terminal supports standard ASCII characters
5. **Python environment**: User has Python 3.13+ installed and accessible

---

## Key Entities

### Task

The primary and only entity in Phase I. Represents a unit of work to be tracked.

**Attributes**:
- Unique identifier (auto-generated)
- Description (user-provided)
- Completion status (system-managed)
- Creation timestamp (system-generated)

**Lifecycle**:
1. Created with description, assigned ID and pending status
2. Can be updated (description only)
3. Can be toggled (status changes)
4. Can be deleted (removed from system)

---

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users can complete the full add-view-complete workflow in under 30 seconds
- **SC-002**: 100% of operations complete without application crashes
- **SC-003**: All error scenarios display user-friendly messages with remediation steps
- **SC-004**: Application starts and displays menu within 1 second
- **SC-005**: Task list displays correctly with up to 100 tasks without performance issues
- **SC-006**: All 5 core features (add, view, update, delete, toggle) function correctly
