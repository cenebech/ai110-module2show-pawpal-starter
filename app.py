from datetime import date

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+, a pet care planning assistant that helps organize care tasks
by date, time, priority, and pet.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

if "owner" not in st.session_state:
    st.session_state.owner = Owner()

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(owner=st.session_state.owner)

owner = st.session_state.owner
scheduler = st.session_state.scheduler


def build_task_table_rows(tasks):
    rows = []
    for task in tasks:
        task_pet = scheduler.find_pet_for_task(task)
        rows.append(
            {
                "Time": task.get_formatted_time(),
                "Pet": task_pet.name_of_pet if task_pet else "Unknown pet",
                "Task": task.description,
                "Date": task.get_formatted_date(),
                "Duration": f"{task.duration_minutes} min",
                "Priority": task.priority,
                "Status": "Complete" if task.is_complete else "Pending",
                "Frequency": task.frequency,
            }
        )
    return rows


st.subheader("Owner Information")
owner_name = st.text_input("Owner name", value=owner.name)
owner_address = st.text_input("Owner address", value=owner.address)
owner.update_owner_info(owner_name, owner_address)

st.subheader("Add a Pet")
pet_col1, pet_col2 = st.columns(2)
with pet_col1:
    pet_name = st.text_input("Pet name", value="Mochi")
    pet_type = st.selectbox("Type of pet", ["Dog", "Cat", "Other"])
with pet_col2:
    pet_breed = st.text_input("Breed", value="")
    pet_age = st.number_input("Age", min_value=0, max_value=50, value=1)

if st.button("Add pet"):
    pet = Pet(
        type_of_pet=pet_type,
        name_of_pet=pet_name,
        breed_of_pet=pet_breed,
        age_of_pet=int(pet_age),
    )
    owner.add_pet(pet)
    st.success(f"Added {pet.name_of_pet} to {owner.name}'s pets.")

if owner.pets:
    st.write("Current pets:")
    st.table(
        [
            {
                "Name": pet.name_of_pet,
                "Type": pet.type_of_pet,
                "Breed": pet.breed_of_pet,
                "Age": pet.age_of_pet,
                "Tasks": len(pet.tasks),
            }
            for pet in owner.pets
        ]
    )

    sorted_tasks = scheduler.sort_by_time(owner.get_all_tasks())
    if sorted_tasks:
        st.success("Tasks are sorted chronologically by time.")
        st.table(build_task_table_rows(sorted_tasks))
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Schedule a Task")
st.caption("Tasks can include priority, duration, recurrence, and conflict checks.")

if owner.pets:
    pet_names = [pet.name_of_pet for pet in owner.pets]
    selected_pet_name = st.selectbox("Choose pet", pet_names)
    selected_pet = next(pet for pet in owner.pets if pet.name_of_pet == selected_pet_name)

    suggestions = scheduler.get_task_suggestions(selected_pet)
    description_options = suggestions + ["Custom task"]

    task_col1, task_col2 = st.columns(2)
    with task_col1:
        selected_description = st.selectbox("Suggested care task", description_options)
    with task_col2:
        custom_description = st.text_input("Custom task description", value="")

    task_title = custom_description if selected_description == "Custom task" else selected_description

    task_col1, task_col2, task_col3 = st.columns(3)
    with task_col1:
        task_date = st.date_input("Task date")
    with task_col2:
        task_time = st.time_input("Task time")
    with task_col3:
        task_duration = st.number_input("Duration", min_value=5, max_value=240, value=15, step=5)

    task_col1, task_col2, task_col3 = st.columns(3)
    with task_col1:
        frequency = st.selectbox("Frequency", ["One time", "Daily", "Weekly", "Every 2 weeks", "Monthly"])
    with task_col2:
        priority = st.selectbox("Priority", ["High", "Medium", "Low"], index=1)
    with task_col3:
        recurring_count = st.number_input("Occurrences", min_value=1, max_value=12, value=1)

    if st.button("Schedule task"):
        task = Task(
            description=task_title,
            scheduled_date=task_date,
            time=task_time.strftime("%I:%M %p"),
            frequency=frequency,
            duration_minutes=int(task_duration),
            priority=priority,
        )

        if not task.description.strip():
            st.error("Add a task description before scheduling.")
        elif not scheduler.is_within_open_hours(task):
            st.error(
                f"That task is outside available hours "
                f"({scheduler.show_available_times()})."
            )
        else:
            conflict_warning = scheduler.get_conflict_warning(task, selected_pet=selected_pet)
            if conflict_warning:
                st.warning(conflict_warning)
            else:
                added_tasks, skipped_conflicts = scheduler.add_recurring_tasks_to_pet(
                    selected_pet,
                    task,
                    int(recurring_count),
                )
                if added_tasks:
                    scheduler.schedule_pet_care(
                        added_tasks[0].get_formatted_date(),
                        added_tasks[0].get_formatted_time(),
                        selected_pet,
                    )
                    st.success(f"Scheduled {len(added_tasks)} task(s) for {selected_pet.name_of_pet}.")
                if skipped_conflicts:
                    st.warning(
                        f"Skipped {len(skipped_conflicts)} conflicting task(s). "
                        "Choose a different time if you want to add them."
                    )
else:
    st.info("Add a pet before scheduling a task.")

st.divider()

st.subheader("Manage Tasks")

pending_entries = scheduler.build_schedule_entries(include_completed=False)
if pending_entries:
    for index, entry in enumerate(pending_entries):
        pet = entry["pet"]
        task = entry["task"]
        complete_label = (
            f"Complete {task.description} for {pet.name_of_pet} "
            f"on {task.get_formatted_date()} at {task.get_formatted_time()}"
        )
        if st.checkbox(complete_label, key=f"complete-{index}"):
            scheduler.complete_task(task)
            st.success(f"Marked {task.description} complete.")
else:
    st.info("No pending tasks to complete.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a sorted plan, group it by day, and filter by pet or completion status.")

filter_col1, filter_col2, filter_col3 = st.columns(3)
with filter_col1:
    schedule_pet_filter = st.selectbox("Schedule filter", ["All"] + pet_names if owner.pets else ["All"])
with filter_col2:
    include_completed = st.checkbox("Include completed tasks", value=False)
with filter_col3:
    completion_filter = st.selectbox("Completion filter", ["All", "pending", "completed"])

if st.button("Generate schedule"):
    next_entry = scheduler.get_next_task_due(schedule_pet_filter)
    if next_entry:
        next_task = next_entry["task"]
        next_pet = next_entry["pet"]
        st.info(
            f"Next up: {next_task.description} for {next_pet.name_of_pet} "
            f"on {next_task.get_formatted_date()} at {next_task.get_formatted_time()}."
        )

    filtered_tasks = scheduler.filter_tasks(
        completion_status=completion_filter,
        pet_name=schedule_pet_filter,
    )
    if filtered_tasks:
        st.success(f"Found {len(filtered_tasks)} task(s) matching your filters.")
        st.table(build_task_table_rows(filtered_tasks))
    else:
        st.warning("No tasks match those filters.")

    tasks_by_day = scheduler.organize_tasks_by_day(
        include_completed=include_completed,
        pet_name=schedule_pet_filter,
    )

    if not tasks_by_day:
        st.warning("No scheduled tasks yet.")
    else:
        for task_day, entries in tasks_by_day.items():
            day_label = task_day.strftime("%A, %B %d, %Y") if isinstance(task_day, date) else task_day
            st.markdown(f"**{day_label}**")
            st.table(build_task_table_rows([entry["task"] for entry in entries]))
