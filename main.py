"""Terminal demo for PawPal sorting and filtering logic."""

from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def print_tasks(title, tasks):
    """Print a list of tasks in a readable terminal format."""
    print(title)
    print("=" * len(title))

    if not tasks:
        print("No tasks found.")
        print()
        return

    for task in tasks:
        status = "complete" if task.is_complete else "pending"
        print(f"{task.time} - {task.description} ({status})")
    print()


def main():
    owner = Owner(name="Nuela", address="123 PawPal Lane")
    dog = Pet("Dog", "Buddy", "Golden Retriever", 4)
    cat = Pet("Cat", "Milo", "Tabby", 2)
    schedule_date = date(2026, 7, 7)

    # Add tasks out of order on purpose so sorting is easy to see.
    dog.add_task(Task("Dinner", schedule_date, "18:00", "Daily"))
    dog.add_task(Task("Morning walk", schedule_date, "08:00", "Daily"))
    dog.add_task(Task("Grooming", schedule_date, "14:00", "Weekly"))
    cat.add_task(Task("Clean litter box", schedule_date, "11:30", "Daily"))
    cat.add_task(Task("Breakfast", schedule_date, "07:30", "Daily"))

    dog.tasks[2].mark_complete()
    cat.tasks[0].mark_complete()

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(owner=owner)

    print(f"PawPal Terminal Demo for {owner.name}")
    print()

    print_tasks("All Tasks Sorted By Time", scheduler.sort_by_time(owner.get_all_tasks()))
    print_tasks("Pending Tasks Only", scheduler.filter_tasks(completion_status="pending"))
    print_tasks("Completed Tasks Only", scheduler.filter_tasks(completion_status="completed"))
    print_tasks("Buddy's Tasks", scheduler.filter_tasks(pet_name="Buddy"))
    print_tasks(
        "Milo's Pending Tasks",
        scheduler.filter_tasks(completion_status="pending", pet_name="Milo"),
    )

    same_time_task = Task("Breakfast", schedule_date, "08:00", "Daily")
    warning = scheduler.get_conflict_warning(same_time_task, selected_pet=dog)

    print("Conflict Warning Demo")
    print("=====================")
    if warning:
        print(warning)
    else:
        print("No conflict found.")


if __name__ == "__main__":
    main()
