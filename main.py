from pawpal_system import PawPalApp, Task


def main():
    app = PawPalApp()

    # Setup owner
    owner = app.enter_owner_info(name='Alex', available_time=120, preferences={'preferred_categories': ['feeding', 'walking']})

    # Add pets
    dog = app.enter_pet_info('Rex', 'dog')
    cat = app.enter_pet_info('Luna', 'cat')

    # Add tasks
    app.add_edit_tasks('Rex', Task(name='Morning walk', duration=30, priority='high', category='walking'))
    app.add_edit_tasks('Rex', Task(name='Grooming', duration=20, priority='medium', category='grooming'))
    app.add_edit_tasks('Luna', Task(name='Feed kibble', duration=10, priority='high', category='feeding'))
    app.add_edit_tasks('Luna', Task(name='Play session', duration=25, priority='low', category='enrichment'))

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
