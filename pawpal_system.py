"""Logic layer for the PawPal pet care app."""

from dataclasses import dataclass, field
from datetime import date, datetime


@dataclass
class Task:
    """Represents one pet care activity."""

    description: str
    scheduled_date: date | None = None
    time: str = ""
    frequency: str = ""
    is_complete: bool = False

    def mark_complete(self):
        """Mark this task as completed."""
        self.is_complete = True

    def mark_incomplete(self):
        """Mark this task as not completed."""
        self.is_complete = False

    def update_task(self, description=None, scheduled_date=None, time=None, frequency=None):
        """Update the task fields that were provided."""
        if description is not None:
            self.description = description
        if scheduled_date is not None:
            self.scheduled_date = scheduled_date
        if time is not None:
            self.time = time
        if frequency is not None:
            self.frequency = frequency

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

        task_time = datetime.strptime(self.time, "%I:%M %p")
        return task_time.strftime("%I:%M%p").lstrip("0").lower()

    def get_task_details(self):
        """Return this task's details as a dictionary."""
        return {
            "description": self.description,
            "scheduled_date": self.scheduled_date,
            "time": self.time,
            "frequency": self.frequency,
            "is_complete": self.is_complete,
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
        """Add a task to the selected pet."""
        pet.add_task(task)

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

    def get_pending_tasks(self):
        """Return all incomplete tasks across the owner's pets."""
        return [task for task in self.retrieve_all_tasks() if not task.is_complete]

    def get_completed_tasks(self):
        """Return all completed tasks across the owner's pets."""
        return [task for task in self.retrieve_all_tasks() if task.is_complete]

    def complete_task(self, task):
        """Mark the given task as complete."""
        task.mark_complete()

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
