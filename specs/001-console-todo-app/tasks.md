# Tasks: Console Todo Application - INTERMEDIATE Level

**Input**: Design documents from `/specs/001-console-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md
**Level**: INTERMEDIATE (10 features, 41 functions)

**Tests**: Manual testing only (no automated tests in Phase I as per spec)

**Organization**: Tasks grouped by implementation phase and user story for incremental delivery.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different code sections, no dependencies)
- **[Story]**: Which user story this task belongs to (US6-US10 for INTERMEDIATE)
- Include exact file paths and function names in descriptions

## Path Conventions

- **Single file implementation**: All code in `todo.py` at repository root
- All 41 functions reside in one file following 5-layer architecture

---

## BASIC Level Tasks (T001-T032) - COMPLETED

All BASIC level tasks (Phases 1-8) are complete. The following tasks extend the application to INTERMEDIATE level.

**Completed BASIC Features**:
- [x] T001-T005: Setup (constants, file structure)
- [x] T006-T011: Foundational (display layer)
- [x] T012-T015: US1 - Add Task
- [x] T016-T017: US2 - View Tasks
- [x] T018-T022: US3 - Toggle Complete/Incomplete
- [x] T023-T024: US4 - Update Task
- [x] T025-T026: US5 - Delete Task
- [x] T027-T032: Application Layer & Polish

---

## Phase 9: INTERMEDIATE Setup (Data Model Enhancement)

**Purpose**: Upgrade data model from BASIC (5 fields) to INTERMEDIATE (7 fields)

- [x] T033 Add priority constants to todo.py (PRIORITY_HIGH="high", PRIORITY_MEDIUM="medium", PRIORITY_LOW="low", VALID_PRIORITIES list)
- [x] T034 [P] Add color constants to todo.py (COLOR_RED="\033[91m", COLOR_YELLOW="\033[93m", COLOR_GREEN="\033[92m", COLOR_RESET="\033[0m")
- [x] T035 [P] Add tag validation constants to todo.py (MAX_TAG_LENGTH=20, MIN_TAG_LENGTH=1)
- [x] T036 [P] Add status symbol constants to todo.py (SYMBOL_INCOMPLETE="○", SYMBOL_COMPLETE="✓")
- [x] T037 Update menu constants in todo.py (MENU_SET_PRIORITY="6" through MENU_EXIT="11", update VALID_MENU_CHOICES to ["1"-"11"])
- [x] T038 Update create_task() function to include priority="medium" and tags=[] default fields in todo.py

**Checkpoint**: Data model ready for INTERMEDIATE features ✓

---

## Phase 10: INTERMEDIATE Foundational (New Validation Functions)

**Purpose**: Core validation functions that all INTERMEDIATE commands depend on

**CRITICAL**: Must complete before any INTERMEDIATE command layer functions

- [x] T039 [P] Implement validate_priority(priority: str) -> tuple[bool, str] in todo.py (accepts high/medium/low case-insensitive, returns normalized lowercase)
- [x] T040 [P] Implement validate_tag(tag: str) -> tuple[bool, str] in todo.py (1-20 chars, alphanumeric+hyphens, normalized lowercase)
- [x] T041 [P] Implement validate_tag_not_duplicate(task: dict, tag: str) -> tuple[bool, str] in todo.py (checks if tag already on task)
- [x] T042 [P] Implement validate_tag_exists(task: dict, tag: str) -> tuple[bool, str] in todo.py (checks if tag exists for removal)

**Checkpoint**: All INTERMEDIATE validation functions ready ✓

---

## Phase 11: User Story 6 - Set Priority (Priority: P2)

**Goal**: Users can set task priority to high/medium/low with color-coded display

**Independent Test**: Add task, set priority to "high", view tasks to verify RED color display

### Data Layer for US6

- [x] T043 [US6] Implement set_priority(tasks: list[dict], task_id: int, priority: str) -> bool in todo.py (updates task priority field)

### Display Layer for US6

- [x] T044 [US6] Implement display_priority_with_color(priority: str) -> str in todo.py (returns ANSI-colored priority string: red=high, yellow=medium, green=low)

### Command Layer for US6

- [x] T045 [US6] Implement cmd_set_priority(tasks: list[dict]) -> None in todo.py (prompts for ID, shows current priority, validates new priority, updates, shows success)

**Checkpoint**: Priority feature complete - can set and view colored priorities ✓

---

## Phase 12: User Story 7 - Manage Tags (Priority: P2)

**Goal**: Users can add/remove tags on tasks via submenu

**Independent Test**: Add task, add tags "work" and "urgent", view tasks to verify tags display, remove "urgent" tag, verify removed

### Data Layer for US7

- [x] T046 [P] [US7] Implement add_tag(tasks: list[dict], task_id: int, tag: str) -> bool in todo.py (appends tag to task's tags list)
- [x] T047 [P] [US7] Implement remove_tag(tasks: list[dict], task_id: int, tag: str) -> bool in todo.py (removes tag from task's tags list)

### Display Layer for US7

- [x] T048 [US7] Implement display_submenu(title: str, options: list[str]) -> None in todo.py (displays formatted submenu with header and numbered options)

### Command Layer for US7

- [x] T049 [US7] Implement cmd_manage_tags(tasks: list[dict]) -> None in todo.py (submenu with 4 options: Add Tag, Remove Tag, View Task Tags, Back to Main Menu)

**Checkpoint**: Tags feature complete - can add, remove, view tags on tasks ✓

---

## Phase 13: User Story 8 - Search Tasks (Priority: P2)

**Goal**: Users can search tasks by keyword in title or description (case-insensitive, partial match)

**Independent Test**: Add 5 tasks with various titles/descriptions, search for keyword, verify only matching tasks display

### Data Layer for US8

- [x] T050 [US8] Implement search_tasks(tasks: list[dict], query: str) -> list[dict] in todo.py (case-insensitive partial match on title AND description, returns NEW list)

### Command Layer for US8

- [x] T051 [US8] Implement cmd_search_tasks(tasks: list[dict]) -> None in todo.py (prompts for query, validates not empty, displays results or "no matches" message)

**Checkpoint**: Search feature complete - can find tasks by keyword ✓

---

## Phase 14: User Story 9 - Filter Tasks (Priority: P2)

**Goal**: Users can filter tasks by status, priority, or tag via submenu

**Independent Test**: Add tasks with various properties, filter by each criterion, verify correct subset displays

### Data Layer for US9

- [x] T052 [US9] Implement filter_tasks(tasks: list[dict], status: bool|None=None, priority: str|None=None, tag: str|None=None) -> list[dict] in todo.py (AND logic for multiple filters, returns NEW list)

### Command Layer for US9

- [x] T053 [US9] Implement cmd_filter_tasks(tasks: list[dict]) -> None in todo.py (submenu with 5 options: Filter by Status, Filter by Priority, Filter by Tag, Show All, Back)

**Checkpoint**: Filter feature complete - can view filtered subsets of tasks ✓

---

## Phase 15: User Story 10 - Sort Tasks (Priority: P3)

**Goal**: Users can sort tasks by date/priority/title via submenu without mutating original list

**Independent Test**: Add 5 tasks, sort by each criterion, verify correct order, verify original list unchanged when viewing again

### Data Layer for US10

- [x] T054 [US10] Implement sort_tasks(tasks: list[dict], key: str, reverse: bool=False) -> list[dict] in todo.py (key="date"|"priority"|"title", returns NEW sorted list, stable sort)

### Command Layer for US10

- [x] T055 [US10] Implement cmd_sort_tasks(tasks: list[dict]) -> None in todo.py (submenu with 7 options: Date Newest/Oldest, Priority H-L/L-H, Title A-Z/Z-A, Back)

**Checkpoint**: Sort feature complete - can view tasks in various sorted orders ✓

---

## Phase 16: Display Layer Updates

**Purpose**: Update existing display functions for INTERMEDIATE features

- [x] T056 Update format_task_row(task: dict) -> str to include Status symbol (○/✓), Priority with color, Tags column (comma-separated) in todo.py
- [x] T057 Update display_tasks(tasks: list[dict]) -> None to show 6-column header (ID | Status | Priority | Title | Tags | Created) in todo.py
- [x] T058 Update display_menu() -> None to show 11 options (add options 6-11 for Priority, Tags, Search, Filter, Sort, Exit) in todo.py

---

## Phase 17: Main Application Integration

**Purpose**: Wire all new commands into main() loop

- [x] T059 Update main() to handle menu choices 6-10 dispatching to cmd_set_priority, cmd_manage_tags, cmd_search_tasks, cmd_filter_tasks, cmd_sort_tasks in todo.py
- [x] T060 Update main() to use choice "11" for Exit (was "6") in todo.py
- [x] T061 Update input prompt to "Enter your choice (1-11):" in todo.py

---

## Phase 18: Polish & Validation

**Purpose**: Final validation and code cleanup for INTERMEDIATE level

- [x] T062 Verify all new functions have type hints per constitution in todo.py
- [x] T063 Verify all new functions have Google-format docstrings per constitution in todo.py
- [x] T064 Verify no function exceeds 50 lines per constitution in todo.py
- [x] T065 Manual test: Set Priority feature (high=red, medium=yellow, low=green, case-insensitive input)
- [x] T066 Manual test: Manage Tags feature (add, remove, view, duplicate prevention, format validation)
- [x] T067 Manual test: Search feature (case-insensitive, partial match, title+description, empty query error)
- [x] T068 Manual test: Filter feature (by status, by priority, by tag, show all, no matches message)
- [x] T069 Manual test: Sort feature (6 sort options, original list unchanged after sort)
- [x] T070 Manual test: BASIC features (1-5) still work correctly with new data model
- [x] T071 Verify color coding displays correctly in terminal (red/yellow/green)
- [x] T072 Verify status symbols display correctly (○/✓)

---

## Dependencies & Execution Order

### Phase Dependencies

```
BASIC Complete (T001-T032)
           │
           ▼
Phase 9 (INTERMEDIATE Setup)
           │
           ▼
Phase 10 (INTERMEDIATE Foundational) ──────────────────────────┐
           │                                                    │
           ├──► Phase 11 (US6: Priority) ──┐                   │
           │                                │                   │
           ├──► Phase 12 (US7: Tags) ──────┤                   │
           │                                │                   │
           ├──► Phase 13 (US8: Search) ────┼──► Phase 16 ─────┤
           │                                │   (Display)       │
           ├──► Phase 14 (US9: Filter) ────┤                   │
           │                                │                   │
           └──► Phase 15 (US10: Sort) ─────┘                   │
                                                                │
                                       Phase 17 ◄───────────────┘
                                       (Integration)
                                            │
                                            ▼
                                       Phase 18 (Polish)
```

### Task Dependencies Within Phases

**Phase 9**: T033 → T034+T035+T036 (parallel) → T037 → T038

**Phase 10**: All [P] tasks can run in parallel (T039, T040, T041, T042)

**Phase 11 (US6)**: T043 → T044 → T045

**Phase 12 (US7)**: T046+T047 (parallel) → T048 → T049

**Phase 13 (US8)**: T050 → T051

**Phase 14 (US9)**: T052 → T053

**Phase 15 (US10)**: T054 → T055

**Phase 16**: T056 → T057 → T058 (can start after Phase 11 display function T044)

**Phase 17**: Depends on all command functions and Phase 16

**Phase 18**: Depends on Phase 17

---

## Parallel Opportunities

### Phase 9: Constants Setup

```bash
# Launch independent constant tasks:
Task: "T034 Add color constants"
Task: "T035 Add tag validation constants"
Task: "T036 Add status symbol constants"
```

### Phase 10: All Validation Functions

```bash
# Launch all validation tasks together:
Task: "T039 validate_priority()"
Task: "T040 validate_tag()"
Task: "T041 validate_tag_not_duplicate()"
Task: "T042 validate_tag_exists()"
```

### Phase 12: Tag Data Functions

```bash
# Launch both tag data functions:
Task: "T046 add_tag()"
Task: "T047 remove_tag()"
```

### User Stories (After Phase 10)

Once Phase 10 completes, user stories US6-US10 can be worked on in any order, though priority order (P2 before P3) is recommended.

---

## Implementation Strategy

### MVP First (BASIC + Priority Only)

1. Complete Phase 9: INTERMEDIATE Setup
2. Complete Phase 10: INTERMEDIATE Foundational
3. Complete Phase 11: User Story 6 (Priority)
4. Update display (partial Phase 16)
5. **STOP and VALIDATE**: Test priority feature end-to-end

### Incremental Delivery Order

1. Setup + Foundational → Core ready
2. Add US6 (Priority) → Test → Demo
3. Add US7 (Tags) → Test → Demo
4. Add US8 (Search) → Test → Demo
5. Add US9 (Filter) → Test → Demo
6. Add US10 (Sort) → Test → Demo
7. Display + Integration → Full menu
8. Polish → Final validation

### Single Developer Flow

Execute phases 9-18 sequentially, using [P] markers to batch parallel work within each phase.

---

## Summary

| Phase | Description | Task Count | Parallel Tasks |
|-------|-------------|------------|----------------|
| 9 | INTERMEDIATE Setup | 6 | 3 |
| 10 | INTERMEDIATE Foundational | 4 | 4 |
| 11 | US6: Set Priority (P2) | 3 | 0 |
| 12 | US7: Manage Tags (P2) | 4 | 2 |
| 13 | US8: Search Tasks (P2) | 2 | 0 |
| 14 | US9: Filter Tasks (P2) | 2 | 0 |
| 15 | US10: Sort Tasks (P3) | 2 | 0 |
| 16 | Display Updates | 3 | 0 |
| 17 | Integration | 3 | 0 |
| 18 | Polish & Validation | 11 | 0 |
| **INTERMEDIATE Total** | | **40** | **9** |
| **Overall Total** | (BASIC + INTERMEDIATE) | **72** | **21** |

### New Functions to Implement (17 total)

| Layer | New Functions | Count |
|-------|---------------|-------|
| Validation | validate_priority, validate_tag, validate_tag_not_duplicate, validate_tag_exists | 4 |
| Data | set_priority, add_tag, remove_tag, search_tasks, filter_tasks, sort_tasks | 6 |
| Display | display_priority_with_color, display_submenu | 2 |
| Command | cmd_set_priority, cmd_manage_tags, cmd_search_tasks, cmd_filter_tasks, cmd_sort_tasks | 5 |

### Updated Functions (4 total)

- create_task() - add priority and tags fields
- format_task_row() - add status symbols, priority colors, tags column
- display_tasks() - update header for 6 columns
- display_menu() - show 11 options
- main() - handle choices 6-11

---

## Notes

- All code in single `todo.py` file (constitution requirement)
- [P] = can run in parallel (no dependencies)
- [US#] = maps to user story for traceability
- Each user story independently testable after completion
- Manual testing only for Phase I
- BASIC features (1-5) must remain functional throughout
- Sort/filter/search return NEW lists (no mutation per constitution)

**Version**: 2.0.0 | **Created**: 2025-12-29 | **Level**: INTERMEDIATE
