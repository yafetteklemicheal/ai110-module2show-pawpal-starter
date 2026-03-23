from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List, Dict, Optional


# Priority ranking for comparison
PRIORITY_RANK = {'high': 3, 'medium': 2, 'low': 1}


@dataclass
class Task:
    """Represents a pet care task."""
    name: str
    duration: int  # in minutes
    priority: str  # e.g., 'high', 'medium', 'low'
    category: str = 'general'  # e.g., 'walking', 'feeding', 'meds', 'grooming', 'enrichment'
    frequency: str = 'daily'  # e.g., 'daily', 'weekly', 'as-needed'
    time_of_day: Optional[str] = None  # optional scheduled time in HH:MM format
    due_date: Optional[date] = None  # next date task is due
    is_completed: bool = False
    
    def get_priority_value(self) -> int:
        """Returns numeric priority for comparison. Higher = more urgent."""
        return PRIORITY_RANK.get(self.priority, 1)
    
    def mark_completed(self) -> Optional['Task']:
        """Mark this task as completed and create next occurrence if recurring."""
        self.is_completed = True

        if self.frequency not in ['daily', 'weekly']:
            return None

        if self.due_date is None:
            next_due_date = date.today()
        else:
            next_due_date = self.due_date

        if self.frequency == 'daily':
            next_due_date += timedelta(days=1)
        elif self.frequency == 'weekly':
            next_due_date += timedelta(weeks=1)

        next_task = Task(
            name=self.name,
            duration=self.duration,
            priority=self.priority,
            category=self.category,
            frequency=self.frequency,
            time_of_day=self.time_of_day,
            due_date=next_due_date,
            is_completed=False,
        )
        return next_task
    
    def set_priority(self, priority: str) -> None:
        """Update the priority of this task."""
        if priority in PRIORITY_RANK:
            self.priority = priority
        else:
            raise ValueError(f"Invalid priority: {priority}. Must be one of {list(PRIORITY_RANK.keys())}")
    
    def __str__(self) -> str:
        """String representation of the task."""
        status = "✓" if self.is_completed else "○"
        return f"{status} {self.name} ({self.duration}min, {self.priority} priority)"


@dataclass
class Pet:
    """Represents a pet."""
    name: str
    type: str  # e.g., 'dog', 'cat', 'rabbit'
    tasks: List[Task] = field(default_factory=list)
    
    def add_task(self, task: Task) -> None:
        """Add a task to the pet's task list."""
        self.tasks.append(task)
    
    def remove_task(self, task_name: str) -> bool:
        """Remove a task by name. Returns True if removed, False if not found."""
        self.tasks = [t for t in self.tasks if t.name != task_name]
        return True
    
    def get_tasks(self) -> List[Task]:
        """Returns the list of tasks."""
        return self.tasks
    
    def get_task_by_name(self, task_name: str) -> Optional[Task]:
        """Retrieve a specific task by name."""
        for task in self.tasks:
            if task.name == task_name:
                return task
        return None


class Owner:
    """Represents a pet owner."""
    def __init__(self, name: str, preferences: dict, available_time: int):
        self.name = name
        self.preferences = preferences  # dict of owner preferences
        self.available_time = available_time  # in minutes
        self.pets: List[Pet] = []
    
    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's collection."""
        self.pets.append(pet)
    
    def remove_pet(self, pet_name: str) -> bool:
        """Remove a pet by name. Returns True if removed, False if not found."""
        self.pets = [p for p in self.pets if p.name != pet_name]
        return True
    
    def get_pets(self) -> List[Pet]:
        """Returns the list of pets."""
        return self.pets
    
    def get_pet_by_name(self, pet_name: str) -> Optional[Pet]:
        """Retrieve a specific pet by name."""
        for pet in self.pets:
            if pet.name == pet_name:
                return pet
        return None


class Schedule:
    """Represents a daily schedule."""
    def __init__(self, owner: Owner, pet: Pet, tasks: List[Task] = None):
        self.owner = owner
        self.pet = pet
        self.tasks = tasks if tasks else []
        self.explanations: Dict[str, str] = {}  # Maps task name -> explanation
    
    def add_task(self, task: Task, explanation: str = "") -> None:
        """Add a task to the schedule with an optional explanation."""
        self.tasks.append(task)
        if explanation:
            self.explanations[task.name] = explanation
    
    def get_total_duration(self) -> int:
        """Calculate total duration of all scheduled tasks."""
        return sum(task.duration for task in self.tasks)
    
    def get_plan(self) -> str:
        """Returns the daily plan as a formatted string."""
        if not self.tasks:
            return f"Daily Plan for {self.pet.name}:\nNo tasks scheduled."
        
        plan = f"Daily Plan for {self.pet.name} ({self.pet.type})\n"
        plan += f"Owner: {self.owner.name}\n"
        plan += f"Available time: {self.owner.available_time} minutes\n"
        plan += f"Scheduled time: {self.get_total_duration()} minutes\n"
        plan += "\n📋 Tasks:\n"
        
        for i, task in enumerate(self.tasks, 1):
            plan += f"  {i}. {task.name} ({task.duration}min) - {task.priority} priority - {task.category}\n"
        
        return plan
    
    def explain_plan(self) -> str:
        """Returns the reasoning behind the schedule."""
        if not self.explanations:
            return "No explanations available."
        
        explanation = f"Planning Reasoning for {self.pet.name}:\n\n"
        
        # Show task-level explanations
        for task in self.tasks:
            if task.name in self.explanations:
                explanation += f"  • {self.explanations[task.name]}\n"
        
        # Show summary
        if "summary" in self.explanations:
            explanation += f"\n📊 {self.explanations['summary']}\n"
        
        return explanation


class Scheduler:
    """Handles scheduling logic."""
    
    def generate_plan(self, owner: Owner, pet: Pet) -> Schedule:
        """Build a schedule from pet tasks and owner constraints."""
        schedule = Schedule(owner, pet)
        
        # Get all tasks for the pet
        tasks = pet.get_tasks()
        
        if not tasks:
            schedule.explanations["general"] = "No tasks to schedule."
            return schedule
        
        # Sort tasks by priority (highest first), then by scheduled time (HH:MM if provided)
        sorted_tasks = self.prioritize_tasks(tasks)
        sorted_tasks = self.sort_tasks_by_time(sorted_tasks)
        
        # Fit tasks into available time
        remaining_time = owner.available_time
        scheduled_count = 0
        
        for task in sorted_tasks:
            if remaining_time >= task.duration:
                schedule.add_task(task, explanation=self._generate_task_explanation(task, owner, pet))
                remaining_time -= task.duration
                scheduled_count += 1
            else:
                # Task doesn't fit
                if remaining_time > 0:
                    schedule.explanations[task.name] = (
                        f"'{task.name}' skipped: requires {task.duration}min, only {remaining_time}min available."
                    )
                else:
                    schedule.explanations[task.name] = (
                        f"'{task.name}' skipped: out of available time (duration: {task.duration}min)."
                    )
        
        # Summary explanation
        total_scheduled = schedule.get_total_duration()
        schedule.explanations["summary"] = (
            f"Scheduled {scheduled_count}/{len(tasks)} tasks for {pet.name}. "
            f"Total time: {total_scheduled}/{owner.available_time} minutes."
        )
        
        return schedule
    
    def _generate_task_explanation(self, task: Task, owner: Owner, pet: Pet) -> str:
        """Generate a reason why this task was scheduled."""
        reason = f"Scheduled '{task.name}' ({task.duration}min) for {pet.name}"
        
        if task.priority == 'high':
            reason += " - HIGH priority task requires attention."
        elif task.category in owner.preferences.get('preferred_categories', []):
            reason += " - aligns with your preferences."
        else:
            reason += " - fits within available time."
        
        return reason
    
    def validate_time_fit(self, tasks: List[Task], available_time: int) -> bool:
        """Check if all tasks fit within available time."""
        total_duration = sum(task.duration for task in tasks)
        return total_duration <= available_time
    
    def prioritize_tasks(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by priority (highest first), then by duration (shortest first)."""
        return sorted(
            tasks,
            key=lambda t: (-t.get_priority_value(), t.duration)
        )

    def sort_tasks_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by time of day in HH:MM format. Tasks without a time go last.

            Args:
                tasks (List[Task]): The list of tasks to sort.

            Returns:
                List[Task]: Tasks sorted by scheduled time."""

        def parse_time(task: Task):
            if task.time_of_day is None:
                return float('inf')
            try:
                hours, minutes = map(int, task.time_of_day.split(':'))
                return hours * 60 + minutes
            except Exception:
                return float('inf')

        return sorted(tasks, key=lambda t: parse_time(t))
    
    def get_all_tasks(self, owner: Owner) -> List[Task]:
        """Retrieve all tasks across all of owner's pets."""
        all_tasks = []
        for pet in owner.get_pets():
            all_tasks.extend(pet.get_tasks())
        return all_tasks

    def complete_task(self, owner: Owner, pet_name: str, task_name: str) -> Optional[Task]:
        """Mark a task as complete for a pet and add a follow-up if recurring.

            Args:
                owner (Owner): The owner containing the pet.
                pet_name (str): The name of the pet.
                task_name (str): The name of the task to complete.

            Returns:
                Optional[Task]: The next recurring task, or None.

            Raises:
                ValueError: If the pet or task is not found."""
        
        pet = owner.get_pet_by_name(pet_name)
        if not pet:
            raise ValueError(f"Pet '{pet_name}' not found.")

        task = pet.get_task_by_name(task_name)
        if not task:
            raise ValueError(f"Task '{task_name}' not found for {pet_name}.")

        next_task = task.mark_completed()

        if next_task is not None:
            pet.add_task(next_task)

        return next_task
    
    def filter_tasks(self, owner: Owner, completed: Optional[bool] = None, pet_name: Optional[str] = None) -> List[Task]:
        """Filter tasks by completion status and/or pet name.

            Args:
                owner (Owner): The owner whose tasks are being filtered.
                completed (Optional[bool]): True for completed, False for incomplete, None for all.
                pet_name (Optional[str]): Filter by pet name, or None for all pets.

            Returns:
                List[Task]: A list of tasks matching the filter criteria."""
        
        filtered = []
        for pet in owner.get_pets():
            if pet_name is not None and pet.name != pet_name:
                continue
            for task in pet.get_tasks():
                if completed is not None and task.is_completed != completed:
                    continue
                filtered.append(task)
        return filtered
    
    def get_tasks_by_category(self, owner: Owner, category: str) -> List[Task]:
        """Get all tasks of a specific category across all pets."""
        all_tasks = self.get_all_tasks(owner)
        return [task for task in all_tasks if task.category == category]
    
    def summarize_tasks(self, owner: Owner) -> str:
        """Provide a summary of all tasks across owner's pets."""
        all_tasks = self.get_all_tasks(owner)
        
        if not all_tasks:
            return "No tasks scheduled for any pet."
        
        summary = f"Summary for {owner.name}:\n"
        for pet in owner.get_pets():
            pet_tasks = pet.get_tasks()
            total_time = sum(t.duration for t in pet_tasks)
            summary += f"  {pet.name} ({pet.type}): {len(pet_tasks)} tasks, {total_time}min total\n"
        
        return summary

    def detect_scheduling_conflicts(self, owner: Owner, pet_name: Optional[str] = None) -> List[str]:
        """Detect tasks scheduled at the same time and return conflict warnings.

            Args:
                owner (Owner): The owner to check conflicts for.
                pet_name (Optional[str]): Check a specific pet, or None for all pets.

            Returns:
                List[str]: Warning messages for each conflict found, or empty list if none."""
        
        warnings = []
        time_slots = {}  # Maps time_of_day -> list of (pet_name, task_name) tuples

        # Collect all tasks with scheduled times
        if pet_name:
            pet = owner.get_pet_by_name(pet_name)
            if pet:
                for task in pet.get_tasks():
                    if task.time_of_day:
                        if task.time_of_day not in time_slots:
                            time_slots[task.time_of_day] = []
                        time_slots[task.time_of_day].append((pet.name, task.name))
        else:
            # Check across all pets
            for pet in owner.get_pets():
                for task in pet.get_tasks():
                    if task.time_of_day:
                        if task.time_of_day not in time_slots:
                            time_slots[task.time_of_day] = []
                        time_slots[task.time_of_day].append((pet.name, task.name))

        # Flag conflicts
        for time_slot, tasks in time_slots.items():
            if len(tasks) > 1:
                task_list = ", ".join([f"{t[0]}'s '{t[1]}'" for t in tasks])
                warnings.append(f"⚠️ CONFLICT at {time_slot}: {task_list}")

        return warnings



class PawPalApp:
    """Streamlit app interface."""
    def __init__(self):
        self.owner: Optional[Owner] = None
        self.scheduler = Scheduler()
    
    def run(self):
        """Start the app workflow."""
        # This would be implemented in Streamlit
        pass
    
    def enter_owner_info(self, name: str, available_time: int, preferences: dict = None) -> Owner:
        """Create an owner with provided information."""
        if preferences is None:
            preferences = {}
        self.owner = Owner(name, preferences, available_time)
        return self.owner
    
    def enter_pet_info(self, pet_name: str, pet_type: str) -> Optional[Pet]:
        """Add a pet to the current owner."""
        if not self.owner:
            raise ValueError("Owner not set. Call enter_owner_info first.")
        
        pet = Pet(pet_name, pet_type)
        self.owner.add_pet(pet)
        return pet
    
    def add_edit_tasks(self, pet_name: str, task: Task) -> None:
        """Add a task to a specific pet."""
        if not self.owner:
            raise ValueError("Owner not set.")
        
        pet = self.owner.get_pet_by_name(pet_name)
        if not pet:
            raise ValueError(f"Pet '{pet_name}' not found.")
        
        pet.add_task(task)
    
    def generate_plan(self, pet_name: str) -> Schedule:
        """Generate a schedule for a specific pet."""
        if not self.owner:
            raise ValueError("Owner not set.")
        
        pet = self.owner.get_pet_by_name(pet_name)
        if not pet:
            raise ValueError(f"Pet '{pet_name}' not found.")
        
        return self.scheduler.generate_plan(self.owner, pet)
    
    def display_plan(self, schedule: Schedule) -> str:
        """Display a schedule as a string."""
        output = schedule.get_plan()
        output += "\n" + schedule.explain_plan()
        return output