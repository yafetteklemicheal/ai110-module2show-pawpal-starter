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

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
