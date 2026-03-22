from dataclasses import dataclass
from typing import List


@dataclass
class Task:
    """Represents a pet care task."""
    name: str
    duration: int  # in minutes
    priority: str  # e.g., 'high', 'medium', 'low'


@dataclass
class Pet:
    """Represents a pet."""
    name: str
    type: str  # e.g., 'dog', 'cat', 'rabbit'
    tasks: List[Task] = None
    
    def __post_init__(self):
        if self.tasks is None:
            self.tasks = []


class Owner:
    """Represents a pet owner."""
    def __init__(self, name: str, preferences: dict, available_time: int):
        self.name = name
        self.preferences = preferences  # dict of owner preferences
        self.available_time = available_time  # in minutes


class Schedule:
    """Represents a daily schedule."""
    def __init__(self, tasks: List[Task] = None):
        self.tasks = tasks if tasks else []
    
    def get_plan(self) -> str:
        """Returns the daily plan as a formatted string."""
        pass


class Scheduler:
    """Handles scheduling logic."""
    def generate_plan(self, owner: Owner, pet: Pet) -> Schedule:
        """Generates a daily schedule based on owner and pet constraints."""
        pass


class PawPalApp:
    """Streamlit app interface."""
    def run(self):
        """Run the Streamlit app."""
        pass