# PawPal+ Project Reflection

## 1. System Design

The initial design needs to includes the 4 major components described in the readme file, and all the tasks detailed in what the final version of the app should look like. The app needs to allow users to add and update owner, pet, and task info. The app will need to generate a schedule that is within the constraints of the owners prefernces and available time.

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

I have added as classes, and they are Owner, Pet, Schedule, and Scheduler. The attributes and responsibilities are as follows:

Owner: name, preferences, available_time
Pet: name, type of pet, pet care tasks
Task: name, duration of task, priority
Schedule: listing pet care tasks
Scheduler: generating a schedule

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

After reviewing the design, one major missing relationship was between the owner and pet class which did not ahve a way of associating which pet belonged to which owner. By adding a list of pets for each owner, we can have a way of adding, removing, and retrieving all the pets that belong to that specific owner.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler considers time, priority, duration, preferences, and scheduled time. I decided that time is the constraint that matters most because it defines how we go about creating the schedule. It tells us how many tasks we may or may not be able to add to the schedule. Priority is second place becuase once we know how much time we have to work with, then we can triage the tasks based on priority to take care of high priority tasks first.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The scheduler focuses on adding the most important tasks first, even if this comes at the cost of some less important tasks that could fit together better. This is reasonable because we want to make sure critical tasks like feeding or medication are always included, even if it means not doing every single optional task.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used Copilot and Claude throughout this project, with most of that usage going to assisting with designing, generating, debugging, and refactoring code. Its a powerful assistant to have but its also one that requires supervision. The AI does best when prompts are structured and specific from the beginning, rather than adding things I forgot afterwards. It really does help to take a moment to pause and think what I really want the AI to do for me with the prompt I'm submitting.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

The initial UML diagram the AI generated was slightly out of scope because it allowed the user to add an address for the owner. During my reivew I removed this part because the app just needs to allow users to add basic owner info and in my judgement adding address info for the owner was extensive and unnecessary.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

The behaviors tested were task completion, pet task management, time-based sorting, daily and weekly recurrence, and conflict detection. These tests were important because they cover the core scheduling behaviors the app depends on, and if any of these do not function as expected, then the app would produce incorrect or unexpected results.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

After performing end user testing to verify everything works as expected, I am confident that the app is performing as expected. Given more time, I would test edge cases where tasks are created with invalid time formats or unexpected values, and recurring tasks with no set due dates. I would also add some tests to cover name conflicts that may occur with an owner using the same name for different pets, as this could make the final schedule confusing since the owner wouldnt know which task belong to which pet.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am very satisfied with how the app turned out overall, and particularly happy with the tests that check for each edge case. It really cut down the amount of time I spent performing end user testing on the app since I could run the tests and see if anything is broken before even running the app itself.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would work on properly validating the time formats and verifying there are no naming conflicts when creating a new pet for an owner. Currently a name conflict breaks the filtering logic as a cat and dog with the same name but different tasks will return a combined list. 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

I learned that system design is a critical task that cannot be brushed aside. It is the foundation for all the work that comes after and any misstep during system design will inevitably cascade into issue downstream. This will force the engineer to revisit this step before proceeding further. It is absolutely worth it to spend some extra time on the design phase to get ahead of any issues that may arise later.