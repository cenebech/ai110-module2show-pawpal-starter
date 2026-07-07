from datetime import date, timedelta

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


def test_scheduler_sorts_tasks_by_time():
    scheduler = Scheduler()
    morning_task = Task("Morning walk", date(2026, 7, 7), "08:00", "Daily")
    afternoon_task = Task("Vet visit", date(2026, 7, 7), "14:00", "Monthly")
    evening_task = Task("Dinner", date(2026, 7, 7), "18:00", "Daily")

    sorted_tasks = scheduler.sort_by_time([evening_task, afternoon_task, morning_task])

    assert sorted_tasks == [morning_task, afternoon_task, evening_task]


def test_scheduler_filters_tasks_by_completion_status_or_pet_name():
    owner, dog, cat, shower, nails, vitamin = make_owner_with_pets_and_tasks()
    scheduler = Scheduler(owner=owner)
    shower.mark_complete()

    assert scheduler.filter_tasks(completion_status="completed") == [shower]
    assert scheduler.filter_tasks(completion_status="pending") == [nails, vitamin]
    assert scheduler.filter_tasks(pet_name=dog.name_of_pet) == [shower, nails]
    assert scheduler.filter_tasks(completion_status=False, pet_name=cat.name_of_pet) == [vitamin]


def test_scheduler_completes_daily_task_and_creates_next_occurrence():
    owner = Owner(name="Nuela")
    dog = Pet("Dog", "Buddy", "Golden Retriever", 4)
    daily_task = Task("Morning walk", date(2026, 7, 7), "08:00", "Daily")
    dog.add_task(daily_task)
    owner.add_pet(dog)
    scheduler = Scheduler(owner=owner)

    next_task = scheduler.complete_task(daily_task)

    assert daily_task.is_complete is True
    assert next_task is not None
    assert next_task.description == daily_task.description
    assert next_task.scheduled_date == date.today() + timedelta(days=1)
    assert next_task.is_complete is False
    assert dog.tasks == [daily_task, next_task]


def test_scheduler_completes_weekly_task_and_creates_next_occurrence():
    owner = Owner(name="Nuela")
    cat = Pet("Cat", "Milo", "Tabby", 2)
    weekly_task = Task("Brush fur", date(2026, 7, 7), "14:00", "Weekly")
    cat.add_task(weekly_task)
    owner.add_pet(cat)
    scheduler = Scheduler(owner=owner)

    next_task = scheduler.complete_task(weekly_task)

    assert next_task is not None
    assert next_task.scheduled_date == date(2026, 7, 14)
    assert cat.tasks == [weekly_task, next_task]


def test_scheduler_does_not_create_next_occurrence_for_monthly_task():
    owner = Owner(name="Nuela")
    dog = Pet("Dog", "Buddy", "Golden Retriever", 4)
    monthly_task = Task("Grooming", date(2026, 7, 7), "14:00", "Monthly")
    dog.add_task(monthly_task)
    owner.add_pet(dog)
    scheduler = Scheduler(owner=owner)

    next_task = scheduler.complete_task(monthly_task)

    assert monthly_task.is_complete is True
    assert next_task is None
    assert dog.tasks == [monthly_task]


def test_scheduler_saves_selected_day_time_and_pet():
    owner, dog, *_ = make_owner_with_pets_and_tasks()
    scheduler = Scheduler(owner=owner)

    message = scheduler.schedule_pet_care("Tuesday", "10:30 AM", dog)

    assert scheduler.selected_day == "Tuesday"
    assert scheduler.selected_time == "10:30 AM"
    assert scheduler.selected_pet == dog
    assert message == "Day and time has now been scheduled for pet care."


def test_scheduler_sorts_filters_and_finds_next_task():
    owner = Owner(name="Nuela")
    dog = Pet("Dog", "Buddy", "Golden Retriever", 4)
    cat = Pet("Cat", "Milo", "Tabby", 2)
    low_task = Task("Brush fur", date(2026, 7, 8), "11:00 AM", "Weekly", priority="Low")
    high_task = Task("Give medicine", date(2026, 7, 8), "9:00 AM", "Daily", priority="High")
    completed_task = Task("Clean bowl", date(2026, 7, 8), "8:00 AM", "Daily")

    completed_task.mark_complete()
    dog.add_task(low_task)
    dog.add_task(high_task)
    cat.add_task(completed_task)
    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(owner=owner)

    entries = scheduler.build_schedule_entries()

    assert [entry["task"] for entry in entries] == [high_task, low_task]
    assert scheduler.get_next_task_due()["task"] == high_task
    assert scheduler.build_schedule_entries(pet_name="Milo") == []
    assert scheduler.build_schedule_entries(include_completed=True)[0]["task"] == completed_task


def test_scheduler_detects_conflicts_and_open_hours():
    pet = Pet("Dog", "Buddy", "Golden Retriever", 4)
    scheduler = Scheduler()
    existing_task = Task("Walk", date(2026, 7, 8), "10:00 AM", "Daily", duration_minutes=30)
    overlapping_task = Task("Groom", date(2026, 7, 8), "10:15 AM", "Weekly", duration_minutes=30)
    late_task = Task("Late grooming", date(2026, 7, 8), "4:20 PM", "Weekly", duration_minutes=30)

    pet.add_task(existing_task)

    assert scheduler.find_conflict(pet, overlapping_task) == existing_task
    assert scheduler.add_task_to_pet(pet, overlapping_task) is False
    assert scheduler.is_within_open_hours(existing_task) is True
    assert scheduler.is_within_open_hours(late_task) is False


def test_scheduler_detects_same_time_conflicts_for_same_pet():
    owner = Owner(name="Nuela")
    dog = Pet("Dog", "Buddy", "Golden Retriever", 4)
    existing_task = Task("Morning walk", date(2026, 7, 8), "08:00", "Daily")
    same_time_task = Task("Breakfast", date(2026, 7, 8), "08:00", "Daily")
    dog.add_task(existing_task)
    owner.add_pet(dog)
    scheduler = Scheduler(owner=owner)

    conflicts = scheduler.find_same_time_conflicts(same_time_task, selected_pet=dog)

    assert conflicts == [{"pet": dog, "task": existing_task}]
    assert scheduler.add_task_to_pet(dog, same_time_task) is False


def test_scheduler_flags_duplicate_times_with_warning():
    owner = Owner(name="Nuela")
    dog = Pet("Dog", "Buddy", "Golden Retriever", 4)
    existing_task = Task("Morning walk", date(2026, 7, 8), "08:00", "Daily")
    duplicate_time_task = Task("Breakfast", date(2026, 7, 8), "08:00", "Daily")
    dog.add_task(existing_task)
    owner.add_pet(dog)
    scheduler = Scheduler(owner=owner)

    warning = scheduler.get_conflict_warning(duplicate_time_task, selected_pet=dog)

    assert warning is not None
    assert "already has 'Morning walk'" in warning


def test_scheduler_detects_same_time_conflicts_for_different_pets():
    owner = Owner(name="Nuela")
    dog = Pet("Dog", "Buddy", "Golden Retriever", 4)
    cat = Pet("Cat", "Milo", "Tabby", 2)
    dog_task = Task("Morning walk", date(2026, 7, 8), "08:00", "Daily")
    cat_task = Task("Breakfast", date(2026, 7, 8), "08:00", "Daily")
    dog.add_task(dog_task)
    owner.add_pet(dog)
    owner.add_pet(cat)
    scheduler = Scheduler(owner=owner)

    conflicts = scheduler.find_same_time_conflicts(cat_task, selected_pet=cat)

    assert conflicts == [{"pet": dog, "task": dog_task}]
    assert scheduler.add_task_to_pet(cat, cat_task) is False


def test_scheduler_treats_24_hour_and_am_pm_times_as_same_time():
    owner = Owner(name="Nuela")
    dog = Pet("Dog", "Buddy", "Golden Retriever", 4)
    existing_task = Task("Morning walk", date(2026, 7, 8), "08:00", "Daily")
    same_time_task = Task("Breakfast", date(2026, 7, 8), "8:00 AM", "Daily")
    dog.add_task(existing_task)
    owner.add_pet(dog)
    scheduler = Scheduler(owner=owner)

    conflicts = scheduler.find_same_time_conflicts(same_time_task, selected_pet=dog)

    assert conflicts == [{"pet": dog, "task": existing_task}]


def test_scheduler_returns_warning_message_for_conflict():
    owner = Owner(name="Nuela")
    dog = Pet("Dog", "Buddy", "Golden Retriever", 4)
    existing_task = Task("Morning walk", date(2026, 7, 8), "08:00", "Daily")
    new_task = Task("Breakfast", date(2026, 7, 8), "08:00", "Daily")
    dog.add_task(existing_task)
    owner.add_pet(dog)
    scheduler = Scheduler(owner=owner)

    warning = scheduler.get_conflict_warning(new_task, selected_pet=dog)

    assert warning == (
        "Warning: Buddy already has 'Morning walk' scheduled near 08:00."
    )


def test_scheduler_returns_no_warning_when_task_does_not_conflict():
    owner = Owner(name="Nuela")
    dog = Pet("Dog", "Buddy", "Golden Retriever", 4)
    existing_task = Task("Morning walk", date(2026, 7, 8), "08:00", "Daily")
    new_task = Task("Dinner", date(2026, 7, 8), "18:00", "Daily")
    dog.add_task(existing_task)
    owner.add_pet(dog)
    scheduler = Scheduler(owner=owner)

    assert scheduler.get_conflict_warning(new_task, selected_pet=dog) is None


def test_scheduler_returns_warning_for_invalid_time_format():
    owner = Owner(name="Nuela")
    dog = Pet("Dog", "Buddy", "Golden Retriever", 4)
    existing_task = Task("Morning walk", date(2026, 7, 8), "08:00", "Daily")
    invalid_task = Task("Breakfast", date(2026, 7, 8), "breakfast time", "Daily")
    dog.add_task(existing_task)
    owner.add_pet(dog)
    scheduler = Scheduler(owner=owner)

    warning = scheduler.get_conflict_warning(invalid_task, selected_pet=dog)

    assert warning == (
        "Warning: this task has an invalid time format, so PawPal could not check conflicts."
    )


def test_scheduler_groups_schedule_entries_by_day():
    owner = Owner(name="Nuela")
    dog = Pet("Dog", "Buddy", "Golden Retriever", 4)
    today_task = Task("Morning walk", date(2026, 7, 8), "08:00", "Daily")
    tomorrow_task = Task("Dinner", date(2026, 7, 9), "18:00", "Daily")
    dog.add_task(tomorrow_task)
    dog.add_task(today_task)
    owner.add_pet(dog)
    scheduler = Scheduler(owner=owner)

    tasks_by_day = scheduler.organize_tasks_by_day()

    assert list(tasks_by_day.keys()) == [date(2026, 7, 8), date(2026, 7, 9)]
    assert tasks_by_day[date(2026, 7, 8)][0]["task"] == today_task
    assert tasks_by_day[date(2026, 7, 9)][0]["task"] == tomorrow_task


def test_scheduler_skips_conflicting_recurring_task_copies():
    owner = Owner(name="Nuela")
    dog = Pet("Dog", "Buddy", "Golden Retriever", 4)
    existing_task = Task("Medication", date(2026, 7, 9), "08:00", "Daily")
    recurring_task = Task("Morning walk", date(2026, 7, 8), "08:00", "Daily")
    dog.add_task(existing_task)
    owner.add_pet(dog)
    scheduler = Scheduler(owner=owner)

    added_tasks, skipped_conflicts = scheduler.add_recurring_tasks_to_pet(
        dog,
        recurring_task,
        count=3,
    )

    assert [task.scheduled_date for task in added_tasks] == [
        date(2026, 7, 8),
        date(2026, 7, 10),
    ]
    assert skipped_conflicts[0][0].scheduled_date == date(2026, 7, 9)
    assert skipped_conflicts[0][1] == existing_task


def test_scheduler_creates_recurring_tasks_and_suggestions():
    scheduler = Scheduler()
    dog = Pet("Dog", "Buddy", "Golden Retriever", 4)
    task = Task("Walk", date(2026, 7, 8), "10:00 AM", "Daily", duration_minutes=20, priority="High")

    recurring_tasks = scheduler.create_recurring_tasks(task, count=3)

    assert [task.scheduled_date for task in recurring_tasks] == [
        date(2026, 7, 8),
        date(2026, 7, 9),
        date(2026, 7, 10),
    ]
    assert all(task.priority == "High" for task in recurring_tasks)
    assert "Morning walk" in scheduler.get_task_suggestions(dog)
