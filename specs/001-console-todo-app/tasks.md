# Tasks: Console Todo Application - Phase I

**Input**: Design documents from `/specs/001-console-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md
**Tests**: Manual testing only (no automated tests in Phase I per spec)
**Organization**: Tasks are grouped by user story to enable independent implementation and testing

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US5)
- Include exact file paths in descriptions

## Path Conventions

- **Single file implementation**: All code in `todo.py` at repository root
- No separate directories for source code (constitution requirement)

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Create file structure and define constants

- [x] T001 Create todo.py file at repository root with module docstring and imports (datetime)
- [x] T002 [P] Define status constants (STATUS_PENDING, STATUS_COMPLETED) in todo.py
- [x] T003 [P] Define validation constants (MAX_DESCRIPTION_LENGTH=200, DISPLAY_TRUNCATE_LENGTH=50) in todo.py
- [x] T004 [P] Define menu constants (MENU_ADD through MENU_EXIT, VALID_MENU_CHOICES) in todo.py
- [x] T005 [P] Define display constants (SEPARATOR, TABLE_HEADER, TABLE_DIVIDER) in todo.py

---

## Phase 2: Foundational (Display Layer - No Dependencies)

**Purpose**: Core display functions that ALL user stories depend on

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 [P] Implement truncate_text(text, max_length) -> str in todo.py
- [x] T007 [P] Implement display_header(title) -> None in todo.py
- [x] T008 [P] Implement display_error(message) -> None in todo.py
- [x] T009 [P] Implement display_success(message) -> None in todo.py
- [x] T010 Implement format_task_row(task) -> str in todo.py (depends on T006)
- [x] T011 Implement display_menu() -> None in todo.py (depends on T007)

**Checkpoint**: Display layer ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Add Task (Priority: P1) - MVP

**Goal**: Users can add new tasks with descriptions and view confirmation

**Independent Test**: Run app, select "1" (Add Task), enter "Buy groceries", verify "Task 1 added: Buy groceries" displays

### Implementation for User Story 1

- [x] T012 [P] [US1] Implement validate_description(description) -> tuple[bool, str] in todo.py
- [x] T013 [P] [US1] Implement get_next_id(tasks) -> int in todo.py
- [x] T014 [US1] Implement create_task(tasks, description, next_id) -> dict in todo.py (depends on T012, T013)
- [x] T015 [US1] Implement cmd_add(tasks) -> None in todo.py (depends on T012, T013, T014, T008, T009)

**Checkpoint**: User Story 1 (Add Task) should be testable - can add tasks with validation

---

## Phase 4: User Story 2 - View Tasks (Priority: P1) - MVP

**Goal**: Users can see all tasks in a formatted table

**Independent Test**: Add 2-3 tasks, select "2" (View Tasks), verify table displays with ID, Description, Status, Created columns

### Implementation for User Story 2

- [x] T016 [US2] Implement display_tasks(tasks) -> None in todo.py (depends on T007, T010)
- [x] T017 [US2] Implement cmd_list(tasks) -> None in todo.py (depends on T016)

**Checkpoint**: User Stories 1 AND 2 should work together - can add and view tasks

---

## Phase 5: User Story 3 - Toggle Complete/Incomplete (Priority: P2)

**Goal**: Users can toggle task status between pending and completed

**Independent Test**: Add task, select "5" (Toggle), enter task ID, verify status changes. Toggle again to verify it returns to original status

### Implementation for User Story 3

- [x] T018 [P] [US3] Implement validate_task_id(task_id_str) -> tuple[bool, int | str] in todo.py
- [x] T019 [P] [US3] Implement get_task_by_id(tasks, task_id) -> dict | None in todo.py
- [x] T020 [US3] Implement validate_task_exists(tasks, task_id) -> tuple[bool, str] in todo.py (depends on T019)
- [x] T021 [US3] Implement toggle_task_status(tasks, task_id) -> tuple[bool, str] in todo.py (depends on T019)
- [x] T022 [US3] Implement cmd_toggle(tasks) -> None in todo.py (depends on T018, T020, T021, T008, T009)

**Checkpoint**: User Stories 1, 2, AND 3 should work - can add, view, and toggle tasks

---

## Phase 6: User Story 4 - Update Task (Priority: P3)

**Goal**: Users can update a task's description

**Independent Test**: Add task with "Buy milk", select "3" (Update), enter task ID, enter "Buy almond milk", verify description changed via View Tasks

### Implementation for User Story 4

- [x] T023 [US4] Implement update_task_description(tasks, task_id, new_description) -> bool in todo.py (depends on T019)
- [x] T024 [US4] Implement cmd_update(tasks) -> None in todo.py (depends on T012, T018, T020, T023, T008, T009)

**Checkpoint**: User Stories 1-4 should work - can add, view, toggle, and update tasks

---

## Phase 7: User Story 5 - Delete Task (Priority: P3)

**Goal**: Users can delete tasks by ID

**Independent Test**: Add task, note ID, select "4" (Delete), enter ID, verify task removed via View Tasks. Add new task, verify it gets new ID (not reused)

### Implementation for User Story 5

- [x] T025 [US5] Implement delete_task(tasks, task_id) -> bool in todo.py
- [x] T026 [US5] Implement cmd_delete(tasks) -> None in todo.py (depends on T018, T020, T025, T008, T009)

**Checkpoint**: All 5 user stories should work independently - complete todo application minus main loop

---

## Phase 8: Application Layer & Polish

**Purpose**: Main loop and final integration

- [x] T027 Implement main() -> None with menu loop in todo.py (depends on T011, T015, T017, T022, T024, T026)
- [x] T028 Add if __name__ == "__main__": main() entry point in todo.py
- [x] T029 Verify all functions have type hints per constitution
- [x] T030 Verify all functions have Google-format docstrings per constitution
- [x] T031 Verify all lines are <= 88 characters per constitution
- [x] T032 Manual end-to-end testing: Run complete workflow (add, view, toggle, update, delete, exit)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup (T001-T005) - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational (Phase 2)
- **User Story 2 (Phase 4)**: Depends on Foundational (Phase 2) + format_task_row from T010
- **User Story 3 (Phase 5)**: Depends on Foundational (Phase 2)
- **User Story 4 (Phase 6)**: Depends on validation from US1 (T012) and US3 (T018, T019, T020)
- **User Story 5 (Phase 7)**: Depends on validation from US3 (T018, T019, T020)
- **Application Layer (Phase 8)**: Depends on all user stories complete

### User Story Dependencies

- **User Story 1 (Add Task)**: Independent after Foundational
- **User Story 2 (View Tasks)**: Independent after Foundational (uses format_task_row)
- **User Story 3 (Toggle)**: Independent after Foundational
- **User Story 4 (Update)**: Reuses validate_description (US1) and validate_task_id/exists (US3)
- **User Story 5 (Delete)**: Reuses validate_task_id/exists (US3)

### Parallel Opportunities Per Phase

**Phase 1 (Setup)**: T002, T003, T004, T005 can run in parallel
**Phase 2 (Foundational)**: T006, T007, T008, T009 can run in parallel
**Phase 3 (US1)**: T012, T013 can run in parallel
**Phase 5 (US3)**: T018, T019 can run in parallel

---

## Parallel Example: Phase 2 Foundational

```bash
# Launch all independent display functions together:
Task: "Implement truncate_text(text, max_length) in todo.py"
Task: "Implement display_header(title) in todo.py"
Task: "Implement display_error(message) in todo.py"
Task: "Implement display_success(message) in todo.py"
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (Add Task)
4. Complete Phase 4: User Story 2 (View Tasks)
5. **STOP and VALIDATE**: Can add and view tasks
6. Deploy/demo if ready

### Incremental Delivery

1. Setup + Foundational → Framework ready
2. Add US1 (Add Task) → Test: Can add tasks with validation
3. Add US2 (View Tasks) → Test: Can see task table → **MVP Demo!**
4. Add US3 (Toggle) → Test: Can toggle status
5. Add US4 (Update) → Test: Can update descriptions
6. Add US5 (Delete) → Test: Can delete tasks
7. Add Application Layer → Test: Full menu loop
8. Polish → Final validation

### Single Developer Strategy

Execute in order: T001 → T002-T005 (parallel) → T006-T009 (parallel) → T010-T011 → T012-T015 → T016-T017 → T018-T022 → T023-T024 → T025-T026 → T027-T032

---

## Task Summary

| Phase | User Story | Task Count | Parallel Tasks |
|-------|------------|------------|----------------|
| 1 | Setup | 5 | 4 |
| 2 | Foundational | 6 | 4 |
| 3 | US1: Add Task (P1) | 4 | 2 |
| 4 | US2: View Tasks (P1) | 2 | 0 |
| 5 | US3: Toggle (P2) | 5 | 2 |
| 6 | US4: Update (P3) | 2 | 0 |
| 7 | US5: Delete (P3) | 2 | 0 |
| 8 | Application & Polish | 6 | 0 |
| **Total** | | **32** | **12** |

---

## Notes

- All code goes in single `todo.py` file (constitution requirement)
- [P] tasks = can run in parallel (no dependencies)
- [US#] label = maps to user story for traceability
- Each user story should be independently testable after completion
- Manual testing only for Phase I (no automated tests)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
