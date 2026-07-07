# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## Testing PawPal+

Run the full test suite with:

```bash
python -m pytest
```

The tests cover the core PawPal+ logic, including task formatting, task
completion, owner and pet task tracking, chronological sorting, filtering by pet
or completion status, conflict detection, recurring task creation, automatic
daily/weekly rescheduling, and warning messages for duplicate times.

Successful test run:

```text
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\nuela\OneDrive - purdue.edu\CodingPath\AI_Classes\AI_101\ai110-module2show-pawpal-starter
plugins: anyio-4.14.1
collected 24 items

tests\test_pawpal.py ........................                            [100%]

============================= 24 passed in 0.05s ==============================
```

Confidence Level: 5/5 stars

Because all 24 tests pass and the tests cover sorting, filtering, recurrence,
conflict detection, and warning behavior, I am highly confident in the current
logic layer.

## 📐 Smarter Scheduling

PawPal+ includes several lightweight scheduling algorithms in `pawpal_system.py`
to make the app more useful for a pet owner.

| Feature | Method(s) | What it does |
|---------|-----------|--------------|
| Sorting behavior | `Scheduler.sort_by_time()`, `Scheduler.build_schedule_entries()` | Sorts `Task` objects by their `time` value. `build_schedule_entries()` also sorts schedule entries by date/time, priority, pet name, and task description for a stable daily plan. |
| Filtering behavior | `Scheduler.filter_tasks()`, `Scheduler.get_pending_tasks()`, `Scheduler.get_completed_tasks()` | Filters tasks by completion status, pet name, or both. For example, it can return only pending tasks for one pet. |
| Conflict detection logic | `Scheduler.find_conflict()`, `Scheduler.find_same_time_conflicts()`, `Scheduler.get_conflict_warning()`, `Scheduler.add_task_to_pet()` | Detects overlapping tasks for the same pet and exact same-time conflicts across one or more pets. The warning method returns a friendly message instead of crashing the app. |
| Recurring task logic | `Scheduler.create_recurring_tasks()`, `Scheduler.add_recurring_tasks_to_pet()`, `Scheduler.complete_task()`, `Scheduler.create_next_occurrence()` | Creates repeated task copies for daily, weekly, every-two-weeks, and monthly schedules. When a daily or weekly task is completed, the scheduler can automatically create the next pending occurrence. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
