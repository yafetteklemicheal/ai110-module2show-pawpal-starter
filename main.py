from pawpal_system import PawPalApp, Task


def main():
    app = PawPalApp()

    # Setup owner
    owner = app.enter_owner_info(name='Alex', available_time=120, preferences={'preferred_categories': ['feeding', 'walking']})

    # Add pets
    dog = app.enter_pet_info('Rex', 'dog')
    cat = app.enter_pet_info('Luna', 'cat')

    # Add tasks out of order with HH:MM times to test sorting
    app.add_edit_tasks('Rex', Task(name='Evening check', duration=15, priority='low', category='enrichment', time_of_day='18:00'))
    app.add_edit_tasks('Rex', Task(name='Morning walk', duration=30, priority='high', category='walking', time_of_day='07:30'))
    app.add_edit_tasks('Rex', Task(name='Midday feeding', duration=20, priority='medium', category='feeding', time_of_day='12:00'))
    app.add_edit_tasks('Luna', Task(name='Play session', duration=25, priority='low', category='enrichment', time_of_day='16:00'))
    app.add_edit_tasks('Luna', Task(name='Feed kibble', duration=10, priority='high', category='feeding', time_of_day='08:00'))
    
    # Add conflicting tasks at same time to test conflict detection
    app.add_edit_tasks('Rex', Task(name='Nap time', duration=45, priority='medium', category='enrichment', time_of_day='12:00'))
    app.add_edit_tasks('Luna', Task(name='Vet call', duration=20, priority='high', category='meds', time_of_day='08:00'))

    print('\n--> All tasks before filtering / sorting:')
    for pet in [dog, cat]:
        print(f"{pet.name}'s tasks:")
        for t in pet.get_tasks():
            print(f"  {t.time_of_day} {t.name} - {t.priority}")

    print('\n--> Tasks after sorting by time (via scheduler):')
    rex_sorted = app.scheduler.sort_tasks_by_time(dog.get_tasks())
    for t in rex_sorted:
        print(f"  {t.time_of_day} {t.name} - {t.priority}")

    # Filter examples
    print('\n--> Filter Rex tasks by high priority (partial via list comprehension):')
    rex_high = [t for t in dog.get_tasks() if t.priority == 'high']
    for t in rex_high:
        print(f"  {t.time_of_day} {t.name}")

    print('\n--> Filter all incomplete tasks using scheduler.filter_tasks:')
    incomplete = app.scheduler.filter_tasks(app.owner, completed=False)
    for t in incomplete:
        print(f"  {t.time_of_day or '--:--'} {t.name} ({t.priority}) on {next(p.name for p in app.owner.get_pets() if t in p.get_tasks())}")

    print('\n--> Detecting scheduling conflicts:')
    conflicts = app.scheduler.detect_scheduling_conflicts(app.owner)
    if conflicts:
        for warning in conflicts:
            print(warning)
    else:
        print("No conflicts detected.")

    # Generate and print schedule for dog
    dog_schedule = app.generate_plan('Rex')
    print("--- Today's Schedule for Rex ---")
    print(app.display_plan(dog_schedule))

    # Generate and print schedule for cat
    cat_schedule = app.generate_plan('Luna')
    print("--- Today's Schedule for Luna ---")
    print(app.display_plan(cat_schedule))


if __name__ == '__main__':
    main()
