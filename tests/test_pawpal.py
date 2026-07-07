from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def make_owner_with_pets_and_tasks():
    owner = Owner(name="Nuela", address="123 PawPal Lane")

    dog = Pet("Dog", "Buddy", "Golden Retriever", 4)
    cat = Pet("Cat", "Milo", "Tabby", 2)

    shower = Task("Shower pet", date(2026, 7, 7), "10:30 AM", "Monthly")
    nails = Task("Cut pet nails", date(2026, 7, 7), "11:00 AM", "Every 2 weeks")
    vitamin = Task("Give vitamin booster", date(2026, 7, 7), "2:00 PM", "Weekly")

    dog.add_task(shower)
    dog.add_task(nails)
    cat.add_task(vitamin)

    owner.add_pet(dog)
    owner.add_pet(cat)

    return owner, dog, cat, shower, nails, vitamin


def test_task_formats_date_and_time():
    task = Task("Shower pet", date(2026, 7, 7), "10:30 AM", "Monthly")

    assert task.get_formatted_date() == "Tuesday, 7th July 2026"
    assert task.get_formatted_time() == "10:30am"


def test_task_completion_changes_status():
    task = Task("Shower pet", date(2026, 7, 7), "10:30 AM", "Monthly")

    assert task.is_complete is False

    task.mark_complete()

    assert task.is_complete is True


def test_adding_task_to_pet_increases_task_count():
    pet = Pet("Dog", "Buddy", "Golden Retriever", 4)
    task = Task("Cut pet nails", date(2026, 7, 7), "11:00 AM", "Every 2 weeks")

    starting_task_count = len(pet.tasks)
    pet.add_task(task)

    assert len(pet.tasks) == starting_task_count + 1


def test_pet_tracks_pending_and_completed_tasks():
    pet = Pet("Dog", "Buddy", "Golden Retriever", 4)
    shower = Task("Shower pet", date(2026, 7, 7), "10:30 AM", "Monthly")
    nails = Task("Cut pet nails", date(2026, 7, 7), "11:00 AM", "Every 2 weeks")

    pet.add_task(shower)
    pet.add_task(nails)
    shower.mark_complete()

    assert pet.get_completed_tasks() == [shower]
    assert pet.get_pending_tasks() == [nails]


def test_owner_collects_tasks_from_all_pets():
    owner, dog, cat, shower, nails, vitamin = make_owner_with_pets_and_tasks()

    assert owner.get_pet_count() == 2
    assert owner.get_all_tasks() == [shower, nails, vitamin]
    assert owner.get_tasks_by_pet() == {
        dog.name_of_pet: [shower, nails],
        cat.name_of_pet: [vitamin],
    }


def test_scheduler_retrieves_organizes_and_completes_tasks():
    owner, dog, cat, shower, nails, vitamin = make_owner_with_pets_and_tasks()
    scheduler = Scheduler(owner=owner)

    assert scheduler.retrieve_all_tasks() == [shower, nails, vitamin]
    assert scheduler.organize_tasks_by_pet() == {
        dog.name_of_pet: [shower, nails],
        cat.name_of_pet: [vitamin],
    }

    scheduler.complete_task(shower)

    assert scheduler.get_completed_tasks() == [shower]
    assert scheduler.get_pending_tasks() == [nails, vitamin]


def test_scheduler_saves_selected_day_time_and_pet():
    owner, dog, *_ = make_owner_with_pets_and_tasks()
    scheduler = Scheduler(owner=owner)

    message = scheduler.schedule_pet_care("Tuesday", "10:30 AM", dog)

    assert scheduler.selected_day == "Tuesday"
    assert scheduler.selected_time == "10:30 AM"
    assert scheduler.selected_pet == dog
    assert message == "Day and time has now been scheduled for pet care."
