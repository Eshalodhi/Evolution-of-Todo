# Feature Specification: Console Todo Application - Phase I (INTERMEDIATE Level)

**Feature Branch**: `001-console-todo-app`
**Created**: 2025-12-28
**Updated**: 2025-12-29
**Status**: Draft
**Level**: INTERMEDIATE (10 features)
**Input**: Phase I console todo application for Panaversity Hackathon II - INTERMEDIATE upgrade

---

## 1. Project Overview

### Description

A command-line todo application that enables developers to manage their tasks directly from the terminal. The application provides a menu-driven interface with 10 features: 5 BASIC features (add, view, update, delete, toggle status) and 5 INTERMEDIATE features (set priority, manage tags, search, filter, sort). All data is stored in memory during the session.

### Target User

Developers and technical users who prefer working in the console environment and want a lightweight, feature-rich task management solution without external dependencies.

### Feature Summary

| Level | Features | Description |
|-------|----------|-------------|
| BASIC (1-5) | Add, View, Update, Delete, Toggle | Core task management |
| INTERMEDIATE (6-10) | Priority, Tags, Search, Filter, Sort | Enhanced organization and discovery |

### Success Criteria for Phase I INTERMEDIATE

- Users can perform all 10 operations without errors
- The application runs from a single Python file with no external dependencies
- All user interactions provide clear feedback with color-coded messages
- Priority displays with color coding (red/yellow/green)
- Status displays with symbols (○ incomplete, ✓ complete)
- Tags display as comma-separated list
- Search, filter, and sort work correctly without mutating original data
- The application handles all edge cases gracefully without crashing

---

## 2. User Scenarios & Testing

### BASIC Features (P1) - Reference

The following BASIC features are already implemented and remain unchanged:

- **Journey 1**: Adding a Task (P1) - Add task with title and optional description
- **Journey 2**: Viewing All Tasks (P1) - Display all tasks in formatted table (NOTE: Now includes Priority and Tags columns)
- **Journey 3**: Marking Complete/Incomplete (P2) - Toggle task completion status
- **Journey 4**: Updating a Task (P3) - Modify task description
- **Journey 5**: Deleting a Task (P3) - Remove task from list

---

### User Story 6 - Setting Task Priority (Priority: P2)

As a user, I want to set a priority level for my tasks so that I can focus on what's most important.

**Why this priority**: Priority management is fundamental to task organization. Users need to distinguish urgent tasks from routine ones.

**Independent Test**: Add a task, set its priority to "high", view tasks to verify priority displays in red.

**Acceptance Scenarios**:

1. **Given** a task with ID 1 exists, **When** user selects "Set Priority", enters "1", then enters "high", **Then** system sets priority to high and displays "Task 1 'Buy groceries' priority set to HIGH" in green

2. **Given** the priority prompt, **When** user enters "MEDIUM" (uppercase), **Then** system accepts it (case-insensitive) and sets priority to "medium"

3. **Given** the priority prompt, **When** user enters "urgent", **Then** system displays "Error: Priority must be high, medium, or low" in red and returns to menu

4. **Given** the priority prompt, **When** user enters empty input, **Then** system displays "Error: Priority must be high, medium, or low" in red

5. **Given** viewing tasks, **When** a task has priority "high", **Then** the priority displays in red with text "HIGH"

6. **Given** viewing tasks, **When** a task has priority "medium", **Then** the priority displays in yellow with text "medium"

7. **Given** viewing tasks, **When** a task has priority "low", **Then** the priority displays in green with text "low"

**Edge Cases**:

| Scenario | Input | Expected Behavior |
|----------|-------|-------------------|
| Invalid task ID | "999" | "Error: Task 999 not found. Use 'View Tasks' to see available task IDs." |
| Non-numeric ID | "abc" | "Error: Task ID must be a positive number." |
| Empty task list | - | "Error: No tasks available. Add a task first." |
| Whitespace priority | "  high  " | Accept (trimmed), set to "high" |
| Current priority shown | - | Display "Current priority: medium" before asking for new |

---

### User Story 7 - Managing Tags (Priority: P2)

As a user, I want to add and remove tags on my tasks so that I can categorize and organize them.

**Why this priority**: Tags enable flexible categorization beyond simple priority. Essential for organizing tasks by project, context, or type.

**Independent Test**: Add a task, add tags "work" and "urgent", view tasks to verify tags display. Remove "urgent" tag, verify it's gone.

**Submenu Flow**:

```
===== MANAGE TAGS =====
1. Add Tag
2. Remove Tag
3. View Task Tags
4. Back to Main Menu

Enter your choice (1-4):
```

**Acceptance Scenarios - Add Tag**:

1. **Given** a task with ID 1 and no tags, **When** user selects "Add Tag", enters task ID "1", enters tag "work", **Then** system adds tag and displays "Tag 'work' added to task 1 'Buy groceries'" in green

2. **Given** a task with tags ["work"], **When** user adds tag "URGENT" (uppercase), **Then** system normalizes to "urgent" and adds it

3. **Given** a task with tags ["work"], **When** user tries to add "work" again, **Then** system displays "Error: Tag 'work' already exists on this task."

4. **Given** the add tag prompt, **When** user enters "my tag" (with space), **Then** system displays "Error: Tag must be alphanumeric and hyphens only. No spaces allowed."

5. **Given** the add tag prompt, **When** user enters "a" * 21 (21 chars), **Then** system displays "Error: Tag must be 1-20 characters."

**Acceptance Scenarios - Remove Tag**:

1. **Given** a task with tags ["work", "urgent"], **When** user removes "work", **Then** system removes tag and displays "Tag 'work' removed from task 1 'Buy groceries'" in green

2. **Given** a task with tags ["work"], **When** user tries to remove "urgent", **Then** system displays "Error: Tag 'urgent' not found on this task."

3. **Given** a task with no tags, **When** user tries to remove any tag, **Then** system displays "Error: This task has no tags."

**Acceptance Scenarios - View Tags**:

1. **Given** a task with tags ["work", "urgent", "phase-1"], **When** user views tags for task 1, **Then** system displays "Task 1 'Buy groceries' tags: work, urgent, phase-1"

2. **Given** a task with no tags, **When** user views tags, **Then** system displays "Task 1 'Buy groceries' has no tags"

**Edge Cases**:

| Scenario | Input | Expected Behavior |
|----------|-------|-------------------|
| Invalid tag format | "work@home" | "Error: Tag must be alphanumeric and hyphens only." |
| Empty tag | "" | "Error: Tag cannot be empty." |
| Tag with hyphen | "phase-1" | Accept - hyphens are allowed |
| Tag numbers only | "123" | Accept - alphanumeric includes numbers |
| Duplicate tag | existing tag | "Error: Tag 'X' already exists on this task." |
| Case normalization | "WORK" | Stored and displayed as "work" |

---

### User Story 8 - Searching Tasks (Priority: P2)

As a user, I want to search my tasks by keyword so that I can quickly find specific tasks.

**Why this priority**: As task lists grow, searching becomes essential for productivity. Case-insensitive search ensures usability.

**Independent Test**: Add 5 tasks with various titles/descriptions, search for a keyword, verify only matching tasks display.

**Acceptance Scenarios**:

1. **Given** tasks with titles "Buy groceries", "Buy milk", "Review code", **When** user searches for "buy", **Then** system displays 2 matching tasks (case-insensitive)

2. **Given** tasks with descriptions containing "urgent meeting", **When** user searches for "URGENT", **Then** system finds tasks with "urgent" in title OR description

3. **Given** no tasks match the search query, **When** user searches for "xyz123", **Then** system displays "No tasks found matching 'xyz123'"

4. **Given** the search prompt, **When** user enters empty query, **Then** system displays "Error: Search query cannot be empty."

5. **Given** search results, **When** displayed, **Then** results show in same table format as View Tasks with all columns

**Edge Cases**:

| Scenario | Input | Expected Behavior |
|----------|-------|-------------------|
| Empty query | "" | "Error: Search query cannot be empty." |
| Whitespace query | "   " | "Error: Search query cannot be empty." |
| Partial match | "gro" | Matches "groceries" |
| No matches | "xyz" | "No tasks found matching 'xyz'" |
| Empty task list | any | "No tasks available to search." |
| Special chars in query | "c++" | Search literally for "c++" |

---

### User Story 9 - Filtering Tasks (Priority: P2)

As a user, I want to filter my tasks by status, priority, or tag so that I can focus on specific subsets.

**Why this priority**: Filtering enables focused work views. Essential for managing larger task lists effectively.

**Filter Menu**:

```
===== FILTER TASKS =====
1. Filter by Status (Complete/Incomplete)
2. Filter by Priority (High/Medium/Low)
3. Filter by Tag
4. Show All Tasks
5. Back to Main Menu

Enter your choice (1-5):
```

**Acceptance Scenarios - Filter by Status**:

1. **Given** 3 complete and 2 incomplete tasks, **When** user filters by "incomplete", **Then** system displays only the 2 incomplete tasks

2. **Given** 3 complete and 2 incomplete tasks, **When** user filters by "complete", **Then** system displays only the 3 complete tasks

**Acceptance Scenarios - Filter by Priority**:

1. **Given** tasks with mixed priorities, **When** user filters by "high", **Then** system displays only high-priority tasks

2. **Given** no high-priority tasks exist, **When** user filters by "high", **Then** system displays "No tasks found with priority 'high'"

**Acceptance Scenarios - Filter by Tag**:

1. **Given** tasks with various tags, **When** user filters by tag "work", **Then** system displays only tasks that have "work" tag

2. **Given** no tasks have tag "personal", **When** user filters by "personal", **Then** system displays "No tasks found with tag 'personal'"

**Edge Cases**:

| Scenario | Input | Expected Behavior |
|----------|-------|-------------------|
| Empty task list | any filter | "No tasks available to filter." |
| No matches | filter with 0 results | "No tasks found matching filter." |
| Invalid status choice | "3" (not 1 or 2) | "Error: Please select 1 for Complete or 2 for Incomplete." |
| Invalid priority | "urgent" | "Error: Priority must be high, medium, or low." |
| Non-existent tag | "nonexistent" | "No tasks found with tag 'nonexistent'" |
| Case-insensitive | "HIGH" | Matches "high" priority tasks |

---

### User Story 10 - Sorting Tasks (Priority: P3)

As a user, I want to sort my tasks by date, priority, or title so that I can view them in a meaningful order.

**Why this priority**: Sorting is a convenience feature that enhances usability but isn't essential for basic task management.

**Sort Menu**:

```
===== SORT TASKS =====
1. Sort by Creation Date (Newest First)
2. Sort by Creation Date (Oldest First)
3. Sort by Priority (High to Low)
4. Sort by Priority (Low to High)
5. Sort by Title (A-Z)
6. Sort by Title (Z-A)
7. Back to Main Menu

Enter your choice (1-7):
```

**Acceptance Scenarios**:

1. **Given** 5 tasks created at different times, **When** user sorts by "Newest First", **Then** system displays tasks with most recent first

2. **Given** 5 tasks with mixed priorities, **When** user sorts by "Priority (High to Low)", **Then** system displays high, then medium, then low priority tasks

3. **Given** 5 tasks, **When** user sorts by "Title (A-Z)", **Then** system displays tasks alphabetically by title

4. **Given** the original task list, **When** user sorts, **Then** original list order is NOT mutated (sort returns new list)

5. **Given** sorted results, **When** displayed, **Then** results show in same table format as View Tasks

**Edge Cases**:

| Scenario | Input | Expected Behavior |
|----------|-------|-------------------|
| Empty task list | any sort | "No tasks available to sort." |
| Single task | any sort | Display the one task (trivial sort) |
| Invalid menu choice | "8" | "Error: Please select a valid option (1-7)." |
| Same priority tasks | priority sort | Maintain relative order (stable sort) |
| Same title initial | title sort | Full title comparison (not just first letter) |
| Original unchanged | after sort | Original list order preserved |

---

## 3. Functional Requirements

### BASIC Features (FR-001 to FR-036) - Retained

All BASIC functional requirements from the original spec remain unchanged. The following requirements are additions for INTERMEDIATE level.

---

### Priority Management (FR-037 to FR-043)

- **FR-037**: System MUST allow users to set task priority to "high", "medium", or "low"
- **FR-038**: System MUST default new tasks to priority "medium"
- **FR-039**: System MUST validate priority input (case-insensitive, trimmed)
- **FR-040**: System MUST display error for invalid priority values
- **FR-041**: System MUST display priority with color coding in task list
- **FR-042**: Priority "high" MUST display in red, "medium" in yellow, "low" in green
- **FR-043**: System MUST show current priority before prompting for new priority

### Tag Management (FR-044 to FR-053)

- **FR-044**: System MUST allow users to add tags to tasks
- **FR-045**: System MUST allow users to remove tags from tasks
- **FR-046**: System MUST default new tasks to empty tags list
- **FR-047**: System MUST validate tag format: 1-20 characters, alphanumeric and hyphens only
- **FR-048**: System MUST normalize tags to lowercase
- **FR-049**: System MUST prevent duplicate tags on the same task
- **FR-050**: System MUST display tags as comma-separated list in task view
- **FR-051**: System MUST show current tags before tag operations
- **FR-052**: System MUST provide tag management submenu (add/remove/view)
- **FR-053**: System MUST display error for invalid tag format with specific reason

### Search Functionality (FR-054 to FR-058)

- **FR-054**: System MUST allow users to search tasks by keyword
- **FR-055**: System MUST search both title and description fields
- **FR-056**: System MUST perform case-insensitive search
- **FR-057**: System MUST support partial string matching
- **FR-058**: System MUST display "no results" message when no tasks match

### Filter Functionality (FR-059 to FR-064)

- **FR-059**: System MUST allow filtering by completion status (complete/incomplete)
- **FR-060**: System MUST allow filtering by priority (high/medium/low)
- **FR-061**: System MUST allow filtering by tag
- **FR-062**: System MUST provide "show all" option to clear filter
- **FR-063**: System MUST display filtered results in standard table format
- **FR-064**: System MUST NOT mutate original task list when filtering

### Sort Functionality (FR-065 to FR-071)

- **FR-065**: System MUST allow sorting by creation date (ascending/descending)
- **FR-066**: System MUST allow sorting by priority (high-to-low/low-to-high)
- **FR-067**: System MUST allow sorting by title (A-Z/Z-A)
- **FR-068**: System MUST use stable sort (preserve relative order of equal elements)
- **FR-069**: System MUST display sorted results in standard table format
- **FR-070**: System MUST NOT mutate original task list when sorting
- **FR-071**: Priority sort order: high > medium > low

### Menu Updates (FR-072 to FR-074)

- **FR-072**: System MUST display 11-option menu (5 BASIC + 5 INTERMEDIATE + Exit)
- **FR-073**: System MUST accept input 1-11 for menu selection
- **FR-074**: System MUST display "Enter your choice (1-11):" prompt

---

## 4. Non-Functional Requirements

### Performance (NFR-001 to NFR-003) - Retained

- **NFR-001**: All operations MUST complete within 100 milliseconds
- **NFR-002**: Application MUST start within 1 second
- **NFR-003**: Memory usage MUST remain reasonable for typical usage

### Additional Performance (NFR-016 to NFR-018)

- **NFR-016**: Search operation MUST handle 1000+ tasks without noticeable delay
- **NFR-017**: Sort operation MUST handle 1000+ tasks within 500ms
- **NFR-018**: Filter operation MUST handle 1000+ tasks within 100ms

### Usability (NFR-004 to NFR-007) - Retained

### Display (NFR-019 to NFR-022)

- **NFR-019**: Color coding MUST work in terminals supporting ANSI escape codes
- **NFR-020**: Priority colors MUST be distinguishable: red (high), yellow (medium), green (low)
- **NFR-021**: Status symbols MUST be clear: ○ (incomplete), ✓ (complete)
- **NFR-022**: Tags MUST display as comma-separated list without brackets

### Reliability (NFR-008 to NFR-010) - Retained

### Data Integrity (NFR-023 to NFR-025)

- **NFR-023**: Sort operations MUST NOT modify original task list
- **NFR-024**: Filter operations MUST NOT modify original task list
- **NFR-025**: Search operations MUST NOT modify original task list

---

## 5. Acceptance Criteria by Feature

### Feature: Set Priority (Menu Option 6)

- [ ] User can set priority by entering task ID
- [ ] User can set priority to "high", "medium", or "low"
- [ ] Priority input is case-insensitive (HIGH, High, high all work)
- [ ] Priority input is whitespace-trimmed
- [ ] Invalid priority shows error: "Priority must be high, medium, or low"
- [ ] Invalid task ID shows error with remediation
- [ ] Current priority is displayed before prompting for new
- [ ] Success message shows task title and new priority
- [ ] High priority displays in RED in task list
- [ ] Medium priority displays in YELLOW in task list
- [ ] Low priority displays in GREEN in task list
- [ ] New tasks default to "medium" priority
- [ ] Empty task list shows "No tasks available" error

### Feature: Manage Tags (Menu Option 7)

- [ ] User sees submenu with Add/Remove/View/Back options
- [ ] User can add tag by entering task ID then tag
- [ ] Tag is validated: 1-20 characters, alphanumeric + hyphen only
- [ ] Tags are normalized to lowercase
- [ ] Duplicate tags are rejected with clear error
- [ ] User can remove existing tag from task
- [ ] Removing non-existent tag shows clear error
- [ ] User can view all tags on a task
- [ ] Task with no tags shows "has no tags" message
- [ ] Tags display as comma-separated in View Tasks
- [ ] New tasks default to empty tags list []
- [ ] Invalid tag format shows specific error reason
- [ ] Back option returns to main menu

### Feature: Search Tasks (Menu Option 8)

- [ ] User is prompted "Enter search query:"
- [ ] Search matches title content (partial match)
- [ ] Search matches description content (partial match)
- [ ] Search is case-insensitive
- [ ] Empty query shows error
- [ ] Matching tasks display in standard table format
- [ ] No matches shows "No tasks found matching 'query'"
- [ ] Empty task list shows "No tasks available to search"
- [ ] Original task list is not modified

### Feature: Filter Tasks (Menu Option 9)

- [ ] User sees filter submenu with 5 options
- [ ] Filter by Status shows complete OR incomplete tasks
- [ ] Filter by Priority shows tasks matching selected priority
- [ ] Filter by Tag shows tasks containing selected tag
- [ ] Show All clears filter and shows all tasks
- [ ] Filtered results display in standard table format
- [ ] No matches shows appropriate "No tasks found" message
- [ ] Empty task list shows "No tasks available to filter"
- [ ] Original task list is not modified
- [ ] Filter inputs are case-insensitive

### Feature: Sort Tasks (Menu Option 10)

- [ ] User sees sort submenu with 7 options
- [ ] Sort by Date (Newest First) works correctly
- [ ] Sort by Date (Oldest First) works correctly
- [ ] Sort by Priority (High to Low) works correctly
- [ ] Sort by Priority (Low to High) works correctly
- [ ] Sort by Title (A-Z) works correctly
- [ ] Sort by Title (Z-A) works correctly
- [ ] Back returns to main menu
- [ ] Sorted results display in standard table format
- [ ] Original task list order is preserved (not mutated)
- [ ] Empty task list shows "No tasks available to sort"
- [ ] Single task list sorts without error

### Feature: Updated View Tasks (Menu Option 2)

- [ ] Table includes ID column
- [ ] Table includes Status column with ○/✓ symbols
- [ ] Table includes Priority column with color coding
- [ ] Table includes Title column (truncated if needed)
- [ ] Table includes Tags column (comma-separated)
- [ ] Table includes Created column
- [ ] Summary shows total, pending, and completed counts

---

## 6. Data Model

### Task Entity (INTERMEDIATE - 7 Fields)

| Field       | Type       | Required | Constraints                           | Default         |
|-------------|------------|----------|---------------------------------------|-----------------|
| id          | int        | Yes      | Positive integer, unique, never reused | Auto-assigned   |
| title       | str        | Yes      | 1-100 characters, trimmed             | N/A             |
| description | str        | No       | 0-200 characters, trimmed             | ""              |
| completed   | bool       | Yes      | True or False                         | False           |
| created_at  | str        | Yes      | ISO 8601 format                       | Current time    |
| priority    | str        | Yes      | "high", "medium", or "low"            | "medium"        |
| tags        | list[str]  | Yes      | List of valid tag strings             | []              |

### Example Task Objects

```python
# Newly created task with defaults
{
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": False,
    "created_at": "2025-12-29T10:30:00",
    "priority": "medium",
    "tags": []
}

# High priority task with tags
{
    "id": 2,
    "title": "Complete hackathon project",
    "description": "Submit before midnight",
    "completed": False,
    "created_at": "2025-12-29T08:00:00",
    "priority": "high",
    "tags": ["work", "urgent", "hackathon"]
}

# Completed low priority task
{
    "id": 3,
    "title": "Review documentation",
    "description": "",
    "completed": True,
    "created_at": "2025-12-28T14:00:00",
    "priority": "low",
    "tags": ["docs", "review"]
}
```

### Priority Constants

| Value    | Display  | Color   | Sort Order |
|----------|----------|---------|------------|
| "high"   | HIGH     | Red     | 1 (highest)|
| "medium" | medium   | Yellow  | 2          |
| "low"    | low      | Green   | 3 (lowest) |

### Status Display

| Value | Symbol | Meaning    |
|-------|--------|------------|
| False | ○      | Incomplete |
| True  | ✓      | Complete   |

---

## 7. Validation Rules

### Priority Validation

| Rule               | Validation                                    | Error Message |
|--------------------|-----------------------------------------------|---------------|
| Not empty          | len(priority.strip()) > 0                     | "Error: Priority must be high, medium, or low" |
| Valid value        | priority.lower() in ["high", "medium", "low"] | "Error: Priority must be high, medium, or low" |
| Case handling      | Convert to lowercase                          | N/A (automatic) |
| Whitespace         | Trim before validation                        | N/A (automatic) |

### Tag Validation

| Rule               | Validation                                    | Error Message |
|--------------------|-----------------------------------------------|---------------|
| Not empty          | len(tag.strip()) > 0                          | "Error: Tag cannot be empty." |
| Min length         | len(tag.strip()) >= 1                         | "Error: Tag cannot be empty." |
| Max length         | len(tag.strip()) <= 20                        | "Error: Tag must be 1-20 characters." |
| Valid characters   | all(c.isalnum() or c == '-' for c in tag)     | "Error: Tag must be alphanumeric and hyphens only." |
| No spaces          | ' ' not in tag                                | "Error: Tag must be alphanumeric and hyphens only." |
| Case handling      | Convert to lowercase                          | N/A (automatic) |
| No duplicates      | tag not in task["tags"]                       | "Error: Tag 'X' already exists on this task." |

### Tag Examples

```python
# Valid tags
"work"       # -> "work"
"URGENT"     # -> "urgent" (normalized)
"phase-1"    # -> "phase-1" (hyphen allowed)
"todo123"    # -> "todo123" (numbers allowed)
"a"          # -> "a" (min 1 char)

# Invalid tags
""           # Empty
"   "        # Whitespace only
"a" * 21     # Too long (21 chars)
"has space"  # Contains space
"work@home"  # Contains special char
"tag!"       # Contains special char
```

---

## 8. User Interface Specification

### Main Menu Layout (11 Options)

```
========================================================================
                         TODO APPLICATION
========================================================================

1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Toggle Complete/Incomplete
6. Set Priority
7. Manage Tags
8. Search Tasks
9. Filter Tasks
10. Sort Tasks
11. Exit

Enter your choice (1-11):
```

### Task List Display Format (INTERMEDIATE)

```
========================================================================
                           YOUR TASKS
========================================================================
ID  | Status | Priority | Title                | Tags           | Created
----|--------|----------|----------------------|----------------|------------------
1   | ○      | HIGH     | Complete project     | work, urgent   | 2025-12-29 10:30
2   | ✓      | medium   | Review code          | review         | 2025-12-29 11:00
3   | ○      | low      | Update docs          |                | 2025-12-29 12:00
========================================================================
Total: 3 tasks (2 pending, 1 completed)
```

Notes:
- Status uses symbols: ○ (incomplete), ✓ (complete)
- Priority "HIGH" displays in red, "medium" in yellow, "low" in green
- Tags are comma-separated, empty shows as blank
- Title truncated to 20 chars with "..." if needed

### Submenu: Manage Tags

```
========================================================================
                         MANAGE TAGS
========================================================================

1. Add Tag
2. Remove Tag
3. View Task Tags
4. Back to Main Menu

Enter your choice (1-4):
```

### Submenu: Filter Tasks

```
========================================================================
                         FILTER TASKS
========================================================================

1. Filter by Status (Complete/Incomplete)
2. Filter by Priority (High/Medium/Low)
3. Filter by Tag
4. Show All Tasks
5. Back to Main Menu

Enter your choice (1-5):
```

### Submenu: Sort Tasks

```
========================================================================
                          SORT TASKS
========================================================================

1. Sort by Creation Date (Newest First)
2. Sort by Creation Date (Oldest First)
3. Sort by Priority (High to Low)
4. Sort by Priority (Low to High)
5. Sort by Title (A-Z)
6. Sort by Title (Z-A)
7. Back to Main Menu

Enter your choice (1-7):
```

### Input Prompts (INTERMEDIATE Features)

| Operation              | Prompt Text                                      |
|------------------------|--------------------------------------------------|
| Set Priority (ID)      | "Enter task ID: "                                |
| Set Priority (Value)   | "Enter new priority (high/medium/low): "         |
| Add Tag (ID)           | "Enter task ID: "                                |
| Add Tag (Value)        | "Enter tag to add: "                             |
| Remove Tag (ID)        | "Enter task ID: "                                |
| Remove Tag (Value)     | "Enter tag to remove: "                          |
| View Tags (ID)         | "Enter task ID: "                                |
| Search                 | "Enter search query: "                           |
| Filter by Status       | "Select: 1. Complete  2. Incomplete: "           |
| Filter by Priority     | "Enter priority (high/medium/low): "             |
| Filter by Tag          | "Enter tag to filter by: "                       |

### Success Messages (Green with ✓)

| Operation           | Message Format                                              |
|---------------------|-------------------------------------------------------------|
| Set Priority        | "✓ Task {id} '{title}' priority set to {PRIORITY}"         |
| Add Tag             | "✓ Tag '{tag}' added to task {id} '{title}'"               |
| Remove Tag          | "✓ Tag '{tag}' removed from task {id} '{title}'"           |
| Search (found)      | "Found {n} task(s) matching '{query}'"                     |
| Filter (found)      | "Showing {n} task(s) matching filter"                      |
| Sort                | "Tasks sorted by {criteria}"                               |

### Error Messages (Red)

| Scenario                   | Message                                                    |
|----------------------------|------------------------------------------------------------|
| Invalid priority           | "Error: Priority must be high, medium, or low"             |
| Empty tag                  | "Error: Tag cannot be empty."                              |
| Tag too long               | "Error: Tag must be 1-20 characters."                      |
| Invalid tag chars          | "Error: Tag must be alphanumeric and hyphens only."        |
| Duplicate tag              | "Error: Tag '{tag}' already exists on this task."          |
| Tag not found              | "Error: Tag '{tag}' not found on this task."               |
| No tags on task            | "Error: This task has no tags."                            |
| Empty search query         | "Error: Search query cannot be empty."                     |
| No search results          | "No tasks found matching '{query}'"                        |
| No filter results          | "No tasks found matching filter."                          |
| No tasks to search         | "Error: No tasks available to search."                     |
| No tasks to filter         | "Error: No tasks available to filter."                     |
| No tasks to sort           | "Error: No tasks available to sort."                       |

---

## 9. Edge Cases & Error Scenarios

### Empty Task List Scenarios

| Operation        | Behavior                                         |
|------------------|--------------------------------------------------|
| Set Priority     | "Error: No tasks available. Add a task first."   |
| Manage Tags      | "Error: No tasks available. Add a task first."   |
| Search Tasks     | "Error: No tasks available to search."           |
| Filter Tasks     | "Error: No tasks available to filter."           |
| Sort Tasks       | "Error: No tasks available to sort."             |

### Invalid Input Scenarios (INTERMEDIATE)

| Input Type       | Invalid Examples            | Handling                                    |
|------------------|-----------------------------|---------------------------------------------|
| Priority         | "urgent", "1", ""           | Show "Priority must be high, medium, or low"|
| Tag              | "", "has space", "a@b"      | Show specific validation error              |
| Search query     | "", "   "                   | Show "Search query cannot be empty"         |
| Menu choice      | "12", "abc", "-1"           | Show "Please select a valid option"         |

### Boundary Conditions (INTERMEDIATE)

| Boundary                 | Value          | Behavior                              |
|--------------------------|----------------|---------------------------------------|
| Tag min length           | 1 char         | Accept                                |
| Tag max length           | 20 chars       | Accept                                |
| Tag over max             | 21+ chars      | Reject with length error              |
| Max tags per task        | No limit       | Accept (reasonable use)               |
| Search in 1000+ tasks    | Large list     | Complete within 500ms                 |
| Sort 1000+ tasks         | Large list     | Complete within 500ms                 |

### Data Integrity Scenarios

| Scenario                     | Expected Behavior                                |
|------------------------------|--------------------------------------------------|
| Sort then view original      | Original order unchanged                         |
| Filter then add task         | New task appears when filter cleared             |
| Search then modify result    | Original list unaffected                         |
| Multiple filters             | Each filter independent                          |

---

## 10. Out of Scope (INTERMEDIATE Level)

The following features are explicitly **NOT** included in Phase I INTERMEDIATE:

### ADVANCED Level Features (Phase I)
- Due dates and deadlines
- Reminders and notifications
- Recurring/repeating tasks
- Task dependencies
- Subtasks

### Phase II Features
- Data persistence (file/database)
- User authentication
- Web interface
- API endpoints
- Multi-user support

### Phase III+ Features
- Cloud sync
- Mobile app
- Collaboration features
- Calendar integration
- Export/import

---

## 11. Assumptions

1. **Terminal support**: User's terminal supports ANSI color codes for priority display
2. **Unicode support**: Terminal can display ○ and ✓ symbols correctly
3. **Single session**: Data is not persisted between sessions (in-memory only)
4. **Reasonable usage**: Task count stays below 10,000 for performance
5. **Tag conventions**: Users will use consistent tag naming (system helps with normalization)

---

## 12. Success Criteria

### Measurable Outcomes (INTERMEDIATE)

- **SC-001**: Users can complete add-priority-tag-search workflow in under 60 seconds
- **SC-002**: 100% of operations complete without application crashes
- **SC-003**: All error scenarios display user-friendly messages with remediation
- **SC-004**: Application starts and displays menu within 1 second
- **SC-005**: Task list displays correctly with up to 100 tasks with all columns
- **SC-006**: All 10 features function correctly (5 BASIC + 5 INTERMEDIATE)
- **SC-007**: Priority colors display correctly in terminal (red/yellow/green)
- **SC-008**: Status symbols display correctly (○/✓)
- **SC-009**: Search finds matching tasks in under 500ms for 1000+ tasks
- **SC-010**: Sort operations do not mutate original task list

---

## Backward Compatibility

All BASIC level features (menu options 1-5) MUST continue to work exactly as before:
- Add Task: Creates task with default priority="medium" and tags=[]
- View Tasks: Updated display includes new columns but behavior unchanged
- Update Task: Updates description only (priority/tags unchanged)
- Delete Task: Removes task completely
- Toggle Complete: Toggles completed boolean

New tasks created through "Add Task" will have default values for new fields.
