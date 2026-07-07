"""Logic layer for the PawPal pet care app."""

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta


PRIORITY_RANK = {"High": 0, "Medium": 1, "Low": 2}
CARE_SUGGESTIONS = {
    "Dog": ["Morning walk", "Feeding", "Fresh water", "Grooming", "Medication"],
    "Cat": ["Feeding", "Fresh water", "Clean litter box", "Brushing", "Playtime"],
    "Other": ["Feeding", "Fresh water", "Habitat cleaning", "Health check", "Enrichment"],
}


def parse_task_time(time_text):
    """Parse a task time string into a ``datetime.time`` value.

    PawPal accepts both 24-hour strings such as ``"14:00"`` and
    12-hour strings such as ``"2:00 PM"`` so terminal demos and
    Streamlit inputs can share the same scheduling logic.
    """
    if "AM" in time_text.upper() or "PM" in time_text.upper():
        return datetime.strptime(time_text, "%I:%M %p").time()
    return datetime.strptime(time_text, "%H:%M").time()


@dataclass
class Task:
    """Represents one pet care activity."""

    description: str
    scheduled_date: date | None = None
    time: str = ""
    frequency: str = ""
    is_complete: bool = False
    duration_minutes: int = 15
    priority: str = "Medium"

    def mark_complete(self):
        """Mark this task as completed."""
        self.is_complete = True

    def mark_incomplete(self):
        """Mark this task as not completed."""
        self.is_complete = False

    def update_task(
        self,
        description=None,
        scheduled_date=None,
        time=None,
        frequency=None,
        duration_minutes=None,
        priority=None,
    ):
        """Update the task fields that were provided."""
        if description is not None:
            self.description = description
        if scheduled_date is not None:
            self.scheduled_date = scheduled_date
        if time is not None:
            self.time = time
        if frequency is not None:
            self.frequency = frequency
        if duration_minutes is not None:
            self.duration_minutes = duration_minutes
        if priority is not None:
            self.priority = priority

    def get_formatted_date(self):
        """Return the scheduled date in a readable format."""
        if self.scheduled_date is None:
            return "No date selected"

        day = self.scheduled_date.day
        if 10 <= day % 100 <= 20:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")

        weekday = self.scheduled_date.strftime("%A")
        month = self.scheduled_date.strftime("%B")
        year = self.scheduled_date.year
        return f"{weekday}, {day}{suffix} {month} {year}"

    def get_formatted_time(self):
        """Return the scheduled time in a compact readable format."""
        if not self.time:
            return "No time selected"

        task_time = parse_task_time(self.time)
        return task_time.strftime("%I:%M%p").lstrip("0").lower()

    def get_scheduled_datetime(self):
        """Return a sortable datetime for this task, or datetime.max if incomplete."""
        if self.scheduled_date is None or not self.time:
            return datetime.max
        return datetime.combine(self.scheduled_date, parse_task_time(self.time))

    def get_end_datetime(self):
        """Return the scheduled end time based on task duration."""
        return self.get_scheduled_datetime() + timedelta(minutes=self.duration_minutes)

    def get_task_details(self):
        """Return this task's details as a dictionary."""
        return {
            "description": self.description,
            "scheduled_date": self.scheduled_date,
            "time": self.time,
            "frequency": self.frequency,
            "is_complete": self.is_complete,
            "duration_minutes": self.duration_minutes,
            "priority": self.priority,
        }


@dataclass
class Pet:
    """Stores pet details and that pet's care tasks."""

    type_of_pet: str = ""
    name_of_pet: str = ""
    breed_of_pet: str = ""
    age_of_pet: int = 0
    tasks: list[Task] = field(default_factory=list)

    def update_pet_info(self, type_of_pet, name_of_pet, breed_of_pet, age_of_pet):
        """Update this pet's basic information."""
        self.type_of_pet = type_of_pet
        self.name_of_pet = name_of_pet
        self.breed_of_pet = breed_of_pet
        self.age_of_pet = age_of_pet

    def add_task(self, task):
        """Add a care task to this pet."""
        self.tasks.append(task)

    def remove_task(self, task):
        """Remove a care task from this pet if it exists."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self):
        """Return all tasks for this pet."""
        return self.tasks

    def get_pending_tasks(self):
        """Return this pet's incomplete tasks."""
        return [task for task in self.tasks if not task.is_complete]

    def get_completed_tasks(self):
        """Return this pet's completed tasks."""
        return [task for task in self.tasks if task.is_complete]

    def get_pet_details(self):
        """Return this pet's details as a dictionary."""
        return {
            "type_of_pet": self.type_of_pet,
            "name_of_pet": self.name_of_pet,
            "breed_of_pet": self.breed_of_pet,
            "age_of_pet": self.age_of_pet,
            "tasks": self.tasks,
        }


@dataclass
class Owner:
    """Manages multiple pets and provides access to their tasks."""

    name: str = ""
    address: str = ""
    pets: list[Pet] = field(default_factory=list)

    @property
    def amount_of_pets(self):
        """Return the number of pets owned by this owner."""
        return len(self.pets)

    def add_pet(self, pet):
        """Add a pet to this owner."""
        self.pets.append(pet)

    def remove_pet(self, pet):
        """Remove a pet from this owner if it exists."""
        if pet in self.pets:
            self.pets.remove(pet)

    def update_owner_info(self, name, address):
        """Update this owner's name and address."""
        self.name = name
        self.address = address

    def get_pet_count(self):
        """Return the number of pets owned by this owner."""
        return self.amount_of_pets

    def get_all_tasks(self):
        """Return all tasks from every pet owned by this owner."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def get_tasks_by_pet(self):
        """Return tasks grouped by each pet's name."""
        return {pet.name_of_pet: pet.tasks for pet in self.pets}

    def find_pet_by_name(self, pet_name):
        """Return a pet by name if the owner has one."""
        for pet in self.pets:
            if pet.name_of_pet == pet_name:
                return pet
        return None


@dataclass
class Scheduler:
    """Retrieves, organizes, and manages pet care tasks across pets."""

    owner: Owner | None = None
    open_days: str = "Monday - Friday"
    open_time: str = "10:00 a.m."
    close_time: str = "4:30 p.m."
    selected_day: str = ""
    selected_time: str = ""
    selected_pet: Pet | None = None

    @property
    def open_hours(self):
        """Return the office open and close time as one string."""
        return f"{self.open_time} - {self.close_time}"

    def show_available_days(self):
        """Return the days that the pet office is open."""
        return self.open_days

    def show_available_times(self):
        """Return the hours that the pet office is open."""
        return self.open_hours

    def fill_out_pet_information(self, owner, pet):
        """Store the owner and selected pet for scheduling."""
        self.owner = owner
        self.selected_pet = pet

    def add_task_to_pet(self, pet, task):
        """Add a task to a pet only when it does not conflict.

        Returns ``True`` when the task is added. Returns ``False`` when
        the task overlaps an existing task for the same pet or shares an
        exact date/time with another task in the owner's schedule.
        """
        conflict = self.find_conflict(pet, task)
        same_time_conflicts = self.find_same_time_conflicts(task, selected_pet=pet)
        if conflict is not None or same_time_conflicts:
            return False
        pet.add_task(task)
        return True

    def retrieve_all_tasks(self):
        """Return all tasks from the scheduler's owner."""
        if self.owner is None:
            return []
        return self.owner.get_all_tasks()

    def organize_tasks_by_pet(self):
        """Return the scheduler owner's tasks grouped by pet."""
        if self.owner is None:
            return {}
        return self.owner.get_tasks_by_pet()

    def sort_by_time(self, tasks):
        """Return ``Task`` objects sorted by their ``time`` attribute.

        The sort uses a lambda key and supports both ``"HH:MM"`` and
        ``"HH:MM AM/PM"`` strings. The original task list is not changed.
        """
        return sorted(tasks, key=lambda task: self._time_string_sort_key(task.time))

    def filter_tasks(self, completion_status=None, pet_name="All"):
        """Return tasks filtered by completion status and/or pet name.

        ``completion_status`` may be ``"completed"``, ``"pending"``,
        ``True``, ``False``, or ``None``/``"All"``. ``pet_name`` can be
        a specific pet name or ``"All"``. Results are sorted by time.
        """
        if self.owner is None:
            return []

        expected_status = self._normalize_completion_status(completion_status)
        filtered_tasks = []

        for pet in self.owner.pets:
            if pet_name != "All" and pet.name_of_pet.lower() != pet_name.lower():
                continue
            for task in pet.tasks:
                if expected_status is None or task.is_complete is expected_status:
                    filtered_tasks.append(task)

        return self.sort_by_time(filtered_tasks)

    def build_schedule_entries(self, include_completed=False, pet_name="All"):
        """Build sorted schedule entries that pair each task with its pet.

        Each returned entry is a dictionary containing ``{"pet": pet,
        "task": task}``. Entries are sorted by scheduled date/time,
        priority, pet name, and task description so the UI can display a
        predictable daily plan.
        """
        if self.owner is None:
            return []

        entries = []
        for pet in self.owner.pets:
            if pet_name != "All" and pet.name_of_pet != pet_name:
                continue
            for task in pet.tasks:
                if include_completed or not task.is_complete:
                    entries.append({"pet": pet, "task": task})

        entries.sort(
            key=lambda entry: (
                entry["task"].get_scheduled_datetime(),
                PRIORITY_RANK.get(entry["task"].priority, 1),
                entry["pet"].name_of_pet.lower(),
                entry["task"].description.lower(),
            )
        )
        return entries

    def organize_tasks_by_day(self, include_completed=False, pet_name="All"):
        """Group sorted schedule entries by scheduled date.

        This method reuses ``build_schedule_entries`` so filters and sort
        order stay consistent between the backend and Streamlit display.
        """
        tasks_by_day = {}
        for entry in self.build_schedule_entries(include_completed, pet_name):
            task_date = entry["task"].scheduled_date or "Unscheduled"
            tasks_by_day.setdefault(task_date, []).append(entry)
        return tasks_by_day

    def get_pending_tasks(self):
        """Return all incomplete tasks across the owner's pets."""
        return [task for task in self.retrieve_all_tasks() if not task.is_complete]

    def get_completed_tasks(self):
        """Return all completed tasks across the owner's pets."""
        return [task for task in self.retrieve_all_tasks() if task.is_complete]

    def get_next_task_due(self, pet_name="All"):
        """Return the nearest upcoming incomplete task entry.

        The result is a ``{"pet": pet, "task": task}`` dictionary, or
        ``None`` if no pending task is scheduled for now or later.
        """
        now = datetime.now()
        for entry in self.build_schedule_entries(include_completed=False, pet_name=pet_name):
            if entry["task"].get_scheduled_datetime() >= now:
                return entry
        return None

    def get_task_suggestions(self, pet):
        """Return care task suggestions based on pet type."""
        return CARE_SUGGESTIONS.get(pet.type_of_pet, CARE_SUGGESTIONS["Other"])

    def is_within_open_hours(self, task):
        """Return whether a task starts and ends inside open hours.

        The check accounts for the task's duration, so a task that starts
        before closing but ends after closing is treated as unavailable.
        """
        if task.scheduled_date is None or not task.time:
            return False

        start = task.get_scheduled_datetime().time()
        end = task.get_end_datetime().time()
        open_start = self._parse_scheduler_time(self.open_time)
        open_end = self._parse_scheduler_time(self.close_time)
        return open_start <= start and end <= open_end

    def find_conflict(self, pet, new_task):
        """Return the first overlapping task for the same pet, if any.

        This checks time ranges, not just exact matches. For example, a
        10:15 task conflicts with an existing 10:00 task that lasts 30
        minutes. ``None`` means no overlap was found.
        """
        if new_task.scheduled_date is None or not new_task.time:
            return None

        new_start = new_task.get_scheduled_datetime()
        new_end = new_task.get_end_datetime()
        for existing_task in pet.tasks:
            if existing_task is new_task or existing_task.scheduled_date != new_task.scheduled_date:
                continue
            existing_start = existing_task.get_scheduled_datetime()
            existing_end = existing_task.get_end_datetime()
            if new_start < existing_end and new_end > existing_start:
                return existing_task
        return None

    def find_same_time_conflicts(self, new_task, selected_pet=None):
        """Return tasks scheduled for the same date and exact time.

        When the scheduler has an owner, this scans all pets owned by that
        owner, so it can catch conflicts across different pets. Each
        conflict is returned as ``{"pet": pet, "task": task}``.
        """
        if new_task.scheduled_date is None or not new_task.time:
            return []

        conflicts = []
        pets_to_check = self.owner.pets if self.owner is not None else [selected_pet]

        for pet in pets_to_check:
            if pet is None:
                continue
            for existing_task in pet.tasks:
                if existing_task is new_task:
                    continue
                if self._tasks_have_same_scheduled_time(existing_task, new_task):
                    conflicts.append({"pet": pet, "task": existing_task})

        return conflicts

    def get_conflict_warning(self, new_task, selected_pet=None):
        """Return a friendly warning string for a scheduling conflict.

        This is the lightweight, UI-safe conflict strategy. It catches
        invalid time formats and returns a warning message instead of
        letting parsing errors crash the app. ``None`` means no warning.
        """
        try:
            same_pet_conflict = self.find_conflict(selected_pet, new_task) if selected_pet else None
            same_time_conflicts = self.find_same_time_conflicts(new_task, selected_pet=selected_pet)
        except ValueError:
            return "Warning: this task has an invalid time format, so PawPal could not check conflicts."

        if same_pet_conflict is not None:
            return (
                f"Warning: {selected_pet.name_of_pet} already has "
                f"'{same_pet_conflict.description}' scheduled near {new_task.time}."
            )

        if same_time_conflicts:
            conflict = same_time_conflicts[0]
            pet = conflict["pet"]
            task = conflict["task"]
            return (
                f"Warning: {pet.name_of_pet} already has '{task.description}' "
                f"scheduled at {task.time} on {task.get_formatted_date()}."
            )

        return None

    def create_recurring_tasks(self, task, count=4):
        """Create upcoming copies of a recurring task.

        The original task is included as the first item. Additional copies
        are spaced using the task's frequency, such as daily or weekly.
        Unsupported frequencies return only the original task.
        """
        if task.scheduled_date is None or count <= 1:
            return [task]

        interval = self._frequency_interval(task.frequency)
        if interval is None:
            return [task]

        tasks = [task]
        for step in range(1, count):
            tasks.append(
                Task(
                    description=task.description,
                    scheduled_date=task.scheduled_date + (interval * step),
                    time=task.time,
                    frequency=task.frequency,
                    duration_minutes=task.duration_minutes,
                    priority=task.priority,
                )
            )
        return tasks

    def add_recurring_tasks_to_pet(self, pet, task, count=4):
        """Add recurring task copies to a pet, skipping conflicts.

        Returns ``(added_tasks, skipped_conflicts)``. ``skipped_conflicts``
        stores pairs of ``(task_copy, conflict)`` so callers can show a
        warning without crashing or partially hiding what happened.
        """
        added_tasks = []
        skipped_conflicts = []
        for task_copy in self.create_recurring_tasks(task, count):
            conflict = self.find_conflict(pet, task_copy)
            same_time_conflicts = self.find_same_time_conflicts(task_copy, selected_pet=pet)
            if conflict is None and not same_time_conflicts:
                pet.add_task(task_copy)
                added_tasks.append(task_copy)
            else:
                skipped_conflicts.append((task_copy, conflict or same_time_conflicts[0]))
        return added_tasks, skipped_conflicts

    def complete_task(self, task):
        """Mark a task complete and schedule the next daily or weekly copy.

        Daily tasks are rescheduled for ``date.today() + timedelta(days=1)``.
        Weekly tasks are rescheduled one week after their scheduled date.
        If the next copy would conflict, no new task is added.
        """
        if task.is_complete:
            return None

        task.mark_complete()
        next_task = self.create_next_occurrence(task)
        pet = self.find_pet_for_task(task)

        if pet is None or next_task is None:
            return None

        has_overlap = self.find_conflict(pet, next_task) is not None
        same_time_conflicts = self.find_same_time_conflicts(next_task, selected_pet=pet)

        if not has_overlap and not same_time_conflicts:
            pet.add_task(next_task)
            return next_task

        return None

    def create_next_occurrence(self, task):
        """Create the next pending copy for a daily or weekly task.

        Returns a new incomplete ``Task`` with the same description, time,
        duration, priority, and frequency, or ``None`` for unsupported
        frequencies.
        """
        if task.scheduled_date is None:
            return None

        next_due_date = self._next_completion_date(task.frequency, task.scheduled_date)
        if next_due_date is None:
            return None

        return Task(
            description=task.description,
            scheduled_date=next_due_date,
            time=task.time,
            frequency=task.frequency,
            duration_minutes=task.duration_minutes,
            priority=task.priority,
        )

    def find_pet_for_task(self, task):
        """Return the owner's pet that contains the given task.

        This lets scheduler-level logic, such as auto-rescheduling after
        completion, add the new task back to the correct pet.
        """
        if self.owner is None:
            return None

        for pet in self.owner.pets:
            if task in pet.tasks:
                return pet
        return None

    def schedule_pet_care(self, day, time, pet=None):
        """Save a selected appointment day, time, and optional pet."""
        self.selected_day = day
        self.selected_time = time
        if pet is not None:
            self.selected_pet = pet
        return self.show_confirmation_message()

    def submit_schedule(self):
        """Submit the current schedule and return confirmation."""
        return self.show_confirmation_message()

    def show_confirmation_message(self):
        """Return the pet care scheduling confirmation message."""
        return "Day and time has now been scheduled for pet care."

    def _frequency_interval(self, frequency):
        """Return a ``timedelta`` for a frequency label.

        Used when generating multiple future recurring task copies from a
        single starting task. Unknown labels return ``None``.
        """
        intervals = {
            "Daily": timedelta(days=1),
            "Weekly": timedelta(weeks=1),
            "Every 2 weeks": timedelta(weeks=2),
            "Monthly": timedelta(days=30),
        }
        return intervals.get(frequency)

    def _next_completion_date(self, frequency, scheduled_date):
        """Return the next due date after a task is completed.

        Daily tasks use today's date plus one day. Weekly tasks use the
        completed task's scheduled date plus one week. Other frequencies
        are not auto-rescheduled by completion.
        """
        frequency_text = str(frequency).strip().lower()
        if frequency_text == "daily":
            return date.today() + timedelta(days=1)
        if frequency_text == "weekly":
            return scheduled_date + timedelta(weeks=1)
        return None

    def _parse_scheduler_time(self, raw_time):
        """Parse scheduler office-hour labels such as ``"10:00 a.m."``."""
        normalized = raw_time.replace(".", "").replace(" ", "").upper()
        return datetime.strptime(normalized, "%I:%M%p").time()

    def _time_string_sort_key(self, time_text):
        """Return a sortable ``(hour, minute)`` tuple for task time text."""
        if not time_text:
            return (24, 0)
        parsed_time = parse_task_time(time_text)
        return (parsed_time.hour, parsed_time.minute)

    def _tasks_have_same_scheduled_time(self, first_task, second_task):
        """Return whether two tasks share the same date and exact time.

        This helper normalizes time strings before comparing, so ``"08:00"``
        and ``"8:00 AM"`` are treated as the same scheduled time.
        """
        if (
            first_task.scheduled_date is None
            or second_task.scheduled_date is None
            or not first_task.time
            or not second_task.time
        ):
            return False

        return (
            first_task.scheduled_date == second_task.scheduled_date
            and parse_task_time(first_task.time) == parse_task_time(second_task.time)
        )

    def _normalize_completion_status(self, completion_status):
        """Convert completion filter labels into ``True``, ``False``, or ``None``.

        ``None`` means do not filter by completion status. This keeps
        string labels from the UI and booleans from tests working through
        the same filtering algorithm.
        """
        if completion_status is None or completion_status == "All":
            return None
        if isinstance(completion_status, bool):
            return completion_status

        status_text = str(completion_status).strip().lower()
        if status_text in {"complete", "completed", "done", "true"}:
            return True
        if status_text in {"pending", "incomplete", "not complete", "false"}:
            return False
        return None
