from pawpal_system import PawPalApp, Owner, Pet, Task, Scheduler
import streamlit as st

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
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

# Initialize app and owner in session state
if "app" not in st.session_state:
    st.session_state.app = PawPalApp()

app = st.session_state.app

st.subheader("Owner Information")
col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner name", value="Jordan", key="owner_name")
with col2:
    available_time = st.number_input("Available time (minutes)", min_value=1, max_value=480, value=120, key="available_time")

if st.button("Set Owner Info"):
    owner = app.enter_owner_info(owner_name, available_time, {"preferred_categories": ["feeding", "walking"]})
    st.success(f"Owner {owner.name} set with {owner.available_time} minutes available!")

st.subheader("Pet Information")
if app.owner:
    col1, col2 = st.columns(2)
    with col1:
        pet_name = st.text_input("Pet name", value="Mochi", key="pet_name")
    with col2:
        species = st.selectbox("Species", ["dog", "cat", "rabbit", "other"], key="species")

    if st.button("Add Pet"):
        pet = app.enter_pet_info(pet_name, species)
        if pet:
            st.success(f"Pet {pet.name} ({pet.type}) added!")
        else:
            st.error("Failed to add pet.")
else:
    st.info("Please set owner information first.")

st.markdown("### Tasks")
st.caption("Add tasks for your pets.")

if app.owner and app.owner.get_pets():
    pet_options = [pet.name for pet in app.owner.get_pets()]
    selected_pet = st.selectbox("Select pet for task", pet_options, key="selected_pet")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk", key="task_title")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20, key="duration")
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2, key="priority")
    with col4:
        category = st.selectbox("Category", ["walking", "feeding", "meds", "grooming", "enrichment", "general"], key="category")

    if st.button("Add Task"):
        task = Task(name=task_title, duration=duration, priority=priority, category=category)
        app.add_edit_tasks(selected_pet, task)
        st.success(f"Task '{task.name}' added to {selected_pet}!")
else:
    st.info("Please add a pet first.")

# Display current tasks
if app.owner:
    for pet in app.owner.get_pets():
        if pet.get_tasks():
            st.subheader(f"Tasks for {pet.name}")
            task_data = []
            for task in pet.get_tasks():
                task_data.append({
                    "Task": task.name,
                    "Duration": f"{task.duration} min",
                    "Priority": task.priority,
                    "Category": task.category
                })
            st.table(task_data)

st.divider()

st.subheader("Generate Schedule")
st.caption("Create a daily schedule for one of your pets.")

if app.owner and app.owner.get_pets():
    pet_options = [pet.name for pet in app.owner.get_pets()]
    schedule_pet = st.selectbox("Select pet for schedule", pet_options, key="schedule_pet")

    if st.button("Generate Schedule"):
        try:
            schedule = app.generate_plan(schedule_pet)
            plan_output = app.display_plan(schedule)
            st.success("Schedule generated!")
            st.code(plan_output, language="text")
        except Exception as e:
            st.error(f"Error generating schedule: {str(e)}")
else:
    st.info("Please add pets and tasks first.")

