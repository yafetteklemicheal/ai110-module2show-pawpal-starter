import pytest
from datetime import date, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler

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


# --- Sorting Correctness ---

def test_sort_tasks_by_time_returns_chronological_order():
    scheduler = Scheduler()
    tasks = [
        Task(name='Evening Walk', duration=30, priority='medium', time_of_day='18:00'),
        Task(name='Morning Feed', duration=10, priority='high', time_of_day='07:00'),
        Task(name='Afternoon Meds', duration=5, priority='high', time_of_day='12:00'),
    ]

    sorted_tasks = scheduler.sort_tasks_by_time(tasks)

    assert [t.time_of_day for t in sorted_tasks] == ['07:00', '12:00', '18:00']


def test_sort_tasks_places_no_time_tasks_last():
    scheduler = Scheduler()
    tasks = [
        Task(name='Walk', duration=30, priority='medium', time_of_day='08:00'),
        Task(name='Grooming', duration=20, priority='low', time_of_day=None),
        Task(name='Feed', duration=10, priority='high', time_of_day='07:00'),
    ]

    sorted_tasks = scheduler.sort_tasks_by_time(tasks)

    assert sorted_tasks[-1].name == 'Grooming'


# --- Recurrence Logic ---

def test_completing_daily_task_creates_new_task():
    task = Task(name='Feed', duration=10, priority='high', frequency='daily')

    next_task = task.mark_completed()

    assert next_task is not None
    assert next_task.name == task.name
    assert not next_task.is_completed


def test_completing_daily_task_sets_next_due_date():
    today = date.today()
    task = Task(name='Feed', duration=10, priority='high', frequency='daily', due_date=today)

    next_task = task.mark_completed()

    assert next_task.due_date == today + timedelta(days=1)


def test_completing_weekly_task_creates_new_task():
    today = date.today()
    task = Task(name='Bath', duration=30, priority='medium', frequency='weekly', due_date=today)

    next_task = task.mark_completed()

    assert next_task is not None
    assert next_task.due_date == today + timedelta(weeks=1)


def test_completing_non_recurring_task_returns_none():
    # frequency='as-needed' is non-recurring per PRIORITY_RANK logic in mark_completed
    task = Task(name='Vet Visit', duration=60, priority='high', frequency='as-needed')

    next_task = task.mark_completed()

    assert next_task is None


# --- Conflict Detection ---

def test_detect_scheduling_conflicts_flags_duplicate_times():
    scheduler = Scheduler()
    owner = Owner(name='Alex', preferences={}, available_time=120)
    pet = Pet(name='Buddy', type='dog')
    pet.add_task(Task(name='Feed', duration=10, priority='high', time_of_day='08:00'))
    pet.add_task(Task(name='Meds', duration=5, priority='high', time_of_day='08:00'))
    owner.add_pet(pet)

    warnings = scheduler.detect_scheduling_conflicts(owner)

    assert len(warnings) == 1
    assert '08:00' in warnings[0]


def test_detect_scheduling_conflicts_returns_empty_when_no_conflicts():
    scheduler = Scheduler()
    owner = Owner(name='Alex', preferences={}, available_time=120)
    pet = Pet(name='Buddy', type='dog')
    pet.add_task(Task(name='Feed', duration=10, priority='high', time_of_day='08:00'))
    pet.add_task(Task(name='Walk', duration=30, priority='medium', time_of_day='09:00'))
    owner.add_pet(pet)

    warnings = scheduler.detect_scheduling_conflicts(owner)

    assert len(warnings) == 0


def test_detect_conflicts_across_multiple_pets():
    scheduler = Scheduler()
    owner = Owner(name='Alex', preferences={}, available_time=120)
    pet1 = Pet(name='Buddy', type='dog')
    pet2 = Pet(name='Milo', type='cat')
    pet1.add_task(Task(name='Feed', duration=10, priority='high', time_of_day='08:00'))
    pet2.add_task(Task(name='Feed', duration=10, priority='high', time_of_day='08:00'))
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    warnings = scheduler.detect_scheduling_conflicts(owner)

    assert len(warnings) == 1
    assert 'Buddy' in warnings[0] and 'Milo' in warnings[0]