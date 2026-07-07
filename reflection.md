# PawPal+ Project Reflection

## 1. System Design

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

classes:
Owner:
	Name
	Address
	Amount of pets
Pets:
	Type of Pet
	Name of Pet
	Breed of Pet
	Age of Pet
Task:
	Shower Pet
	Cut Pet Nails
	Cut Pet Hair
	Give pets a vitamin booster

Scheduler
	Show list of days that the pet office is open (Monday - Friday- 10:00 a.m.- 4:30p.m)
	Allow the pet owner to fill out the information about the pet
	When the owner hits done or submit/ Show a confirmation message saying that the "Day and time has now been scheduled for pet care"


**b. Design changes**

class Owner: Represents a pet owner.
class Pet: Represents a pet receiving care.
class Task: Represents pet care tasks selected by the owner.
class Scheduler: Schedules pet care appointments.

- Did your design change during implementation?
yes I did 
- If yes, describe at least one change and why you made it.
 The main missing relationships are: Pet should probably hold tasks, and Scheduler should probably hold the appointment’s owner, pet, and selected tasks. The biggest logic bottleneck is keeping amount_of_pets in sync manually.



---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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
