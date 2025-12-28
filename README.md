# Evolution of Todo

A command-line todo application built with Python for **Panaversity Hackathon II**.

![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## Quick Start

```bash
# Clone the repository
git clone https://github.com/Eshalodhi/Evolution-of-Todo.git
cd Evolution-of-Todo

# Run the application
python todo.py
```

## Features

| Feature | Description |
|---------|-------------|
| Add Task | Create tasks with title and optional description |
| View Tasks | Display all tasks in a formatted table |
| Update Task | Modify task descriptions |
| Delete Task | Remove tasks by ID |
| Toggle Status | Mark tasks complete/incomplete |

## Demo

```
========================================================================
                        TODO APPLICATION
========================================================================

1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Toggle Complete/Incomplete
6. Exit

Enter your choice (1-6): 1
Enter title: Buy groceries
Enter description (optional, press Enter to skip): Milk, eggs, bread

Task #1 'Buy groceries' created!
```

## Tech Stack

- **Language:** Python 3.13+
- **Dependencies:** None (standard library only)
- **Storage:** In-memory
- **Architecture:** 4-layer (Application, Command, Validation/Data, Display)

## Project Structure

```
Evolution-of-Todo/
├── todo.py                     # Main application
├── README.md                   # Documentation
├── specs/                      # Specifications
│   └── 001-console-todo-app/
│       ├── spec.md             # Requirements
│       ├── plan.md             # Architecture
│       └── tasks.md            # Implementation tasks
└── history/                    # Development history
```

## Author

**Esha Lodhi** - Panaversity Hackathon II

## License

This project is licensed under the MIT License.
