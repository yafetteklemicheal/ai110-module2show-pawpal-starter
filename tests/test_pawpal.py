import pytest
from pawpal_system import Task, Pet


def test_task_completion_marks_completed():
    task = Task(name='Test feed', duration=10, priority='high')
    assert not task.is_completed

    task.mark_completed()

    assert task.is_completed


def test_adding_task_to_pet_increases_task_count():
    pet = Pet(name='Buddy', type='dog')
    initial_count = len(pet.get_tasks())

    pet.add_task(Task(name='Walk', duration=30, priority='medium'))

    assert len(pet.get_tasks()) == initial_count + 1
