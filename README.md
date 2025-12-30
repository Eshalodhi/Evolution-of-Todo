# Evolution of Todo

A command-line todo application built with Python for **Panaversity Hackathon II**.

![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Level](https://img.shields.io/badge/Level-INTERMEDIATE-orange.svg)

## Quick Start

```bash
# Clone the repository
git clone https://github.com/Eshalodhi/Evolution-of-Todo.git
cd Evolution-of-Todo

# Run the application
uv run todo.py
# or
python todo.py
```

## Features

### BASIC Features (1-5)

| Feature | Description |
|---------|-------------|
| Add Task | Create tasks with title and optional description |
| View Tasks | Display all tasks in a formatted table with colors |
| Update Task | Modify task title and description |
| Delete Task | Remove tasks by ID |
| Toggle Status | Mark tasks complete/incomplete |

### INTERMEDIATE Features (6-10)

| Feature | Description |
|---------|-------------|
| Set Priority | Assign high/medium/low priority with color coding |
| Manage Tags | Add/remove multiple tags per task |
| Search Tasks | Find tasks by keyword (case-insensitive) |
| Filter Tasks | Filter by status, priority, or tag |
| Sort Tasks | Sort by date, priority, or title |

## Demo

```
====================================================================================================
                                         TODO APPLICATION
====================================================================================================

ID  | Status        | Priority       | Title              | Description        | Tags         | Created
----------------------------------------------------------------------------------------------------
1   | ✓             | HIGH           | Buy groceries      | Milk, eggs, bread  | shopping     | 2025-12-31 10:30
2   | ○             | MEDIUM         | Write report       | Q4 summary         | work, urgent | 2025-12-31 11:00
3   | ○             | LOW            | Call mom           | —                  |              | 2025-12-31 12:15

====================================================================================================
                                              MENU
====================================================================================================
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
====================================================================================================

Enter your choice (1-11):
```

### Color Coding

- **Priority**: HIGH (red), MEDIUM (yellow), LOW (green)
- **Status**: Complete ✓ (green), Incomplete ○ (red)

## Tech Stack

- **Language:** Python 3.13+
- **Dependencies:** None (standard library only)
- **Storage:** In-memory
- **Architecture:** 5-layer (Application, Command, Validation, Data, Display)

## Project Structure

```
Evolution-of-Todo/
├── todo.py                     # Main application (41 functions)
├── README.md                   # Documentation
├── specs/                      # Specifications
│   └── 001-console-todo-app/
│       ├── spec.md             # Requirements
│       ├── plan.md             # Architecture
│       ├── data-model.md       # Data model (7 fields)
│       └── tasks.md            # Implementation tasks (72 tasks)
├── history/                    # Development history
│   └── prompts/                # Prompt History Records
└── .specify/                   # SpecKit Plus templates
    └── memory/
        └── constitution.md     # Project principles
```

## Data Model

Each task contains 7 fields:

| Field | Type | Description |
|-------|------|-------------|
| id | int | Unique identifier (auto-increment) |
| title | str | Task title (1-100 chars) |
| description | str | Optional description (0-500 chars) |
| status | str | "incomplete" or "completed" |
| created_at | str | ISO timestamp |
| priority | str | "high", "medium", or "low" |
| tags | list | List of tags (alphanumeric, 1-20 chars each) |

## Development Methodology

This project follows **Spec-Driven Development (SDD)**:

1. **Constitution** - Project principles and standards
2. **Specify** - Feature requirements and acceptance criteria
3. **Plan** - Architecture and function signatures
4. **Tasks** - Actionable implementation tasks
5. **Implement** - Code generation and testing

## Author

**Esha Lodhi** - Panaversity Hackathon II

## License

This project is licensed under the MIT License.
