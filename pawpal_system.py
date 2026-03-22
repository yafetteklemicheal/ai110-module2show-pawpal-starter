from dataclasses import dataclass, field
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
    
    def get_priority_value(self) -> int:
        """Returns numeric priority for comparison. Higher = more urgent."""
        return PRIORITY_RANK.get(self.priority, 1)


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
        pass
    
    def explain_plan(self) -> str:
        """Returns the reasoning behind the schedule."""
        pass


class Scheduler:
    """Handles scheduling logic."""
    
    def generate_plan(self, owner: Owner, pet: Pet) -> Schedule:
        """Generates a daily schedule based on owner and pet constraints."""
        pass
    
    def validate_time_fit(self, tasks: List[Task], available_time: int) -> bool:
        """Check if all tasks fit within available time."""
        total_duration = sum(task.duration for task in tasks)
        return total_duration <= available_time
    
    def prioritize_tasks(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by priority (highest first)."""
        return sorted(tasks, key=lambda t: t.get_priority_value(), reverse=True)


class PawPalApp:
    """Streamlit app interface."""
    def __init__(self):
        self.owner: Optional[Owner] = None
        self.scheduler = Scheduler()
    
    def run(self):
        """Run the Streamlit app."""
        pass
    
    def enter_owner_info(self) -> None:
        """Collect owner information from user input."""
        pass
    
    def enter_pet_info(self) -> None:
        """Collect pet information from user input."""
        pass
    
    def add_edit_tasks(self) -> None:
        """Allow user to add or edit tasks."""
        pass
    
    def generate_plan(self) -> None:
        """Generate a daily schedule."""
        pass
    
    def display_plan(self) -> None:
        """Display the generated plan."""
        pass