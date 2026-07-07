"""Temporary terminal testing ground for PawPal logic."""

from datetime import date, datetime

from pawpal_system import Owner, Pet, Task


def sort_task_entry(task_entry):
    task = task_entry["task"]
    task_time = datetime.strptime(task.time, "%I:%M %p").time()
    return datetime.combine(task.scheduled_date, task_time)


def main():
    owner = Owner(name="Nuela", address="123 PawPal Lane")

    dog = Pet(
        type_of_pet="Dog",
        name_of_pet="Buddy",
        breed_of_pet="Golden Retriever",
        age_of_pet=4,
    )
    cat = Pet(
        type_of_pet="Cat",
        name_of_pet="Milo",
        breed_of_pet="Tabby",
        age_of_pet=2,
    )

    schedule_date = date(2026, 7, 7)

    dog.add_task(Task("Shower pet", schedule_date, "10:30 AM", "Monthly"))
    dog.add_task(Task("Cut pet nails", schedule_date, "11:00 AM", "Every 2 weeks"))
    cat.add_task(Task("Give vitamin booster", schedule_date, "2:00 PM", "Weekly"))

    owner.add_pet(dog)
    owner.add_pet(cat)

    schedule_entries = []
    for pet in owner.pets:
        for task in pet.tasks:
            schedule_entries.append({"pet": pet, "task": task})

    schedule_entries.sort(key=sort_task_entry)

    print("Today's Schedule")
    print("================")
    print(f"Owner: {owner.name}")
    print()

    for entry in schedule_entries:
        pet = entry["pet"]
        task = entry["task"]
        print(
            f"{task.get_formatted_date()}, {task.get_formatted_time()} - "
            f"{pet.name_of_pet} the {pet.type_of_pet}: {task.description}"
        )
        print(f"Frequency: {task.frequency}")
        print()


if __name__ == "__main__":
    main()
