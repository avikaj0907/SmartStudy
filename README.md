# SmartStudy — Algorithmic Study Planner & Workload Analyzer

**Author:** Avika Jain
**Registration No.:** 26BCE10206
**University:** VIT Bhopal University
**Program:** 1st Year BTech CSE Core
**Course submission:** VITyarthi — Build Your Own Project

## Overview

SmartStudy is a menu-driven, object-oriented Python program that helps a
student manage subjects and study tasks, plan which tasks to tackle first,
and track overall progress. It is built around a `Task` class and a
`StudyManager` class that provides full CRUD operations, and it saves and
loads all data to a CSV file so nothing is lost between runs.

## Features

### Module 1 — Task & Subject Management
- Add, edit, and delete subjects
- Create tasks with a title, subject, deadline, estimated hours, and
  importance (1–5)
- Mark tasks as Pending or Completed
- View tasks filtered by subject or by status
- Built with a `Task` class and a `StudyManager` class, dictionaries for
  progress lookups, and input validation on every field

### Module 2 — Algorithmic Study Planner
- Sorts pending tasks by an urgency score combining deadline and
  importance, using a manually written selection sort
- Identifies overdue tasks automatically
- Calculates total estimated study hours still pending
- Generates a suggested task order that fits inside the hours the student
  says they actually have available right now

### Module 3 — Workload & Progress Analyzer
- Overall task completion percentage
- Subject-wise progress, shown as both numbers and a text-based bar chart
- Total pending study hours
- A weekly workload summary — tasks due in the next 7 days and the hours
  they need

## Technologies / tools used

- Python 3
- Built-in `csv`, `os`, and `datetime` modules (no external dependencies)

## How to install & run

1. Make sure Python 3 is installed (`python3 --version`).
2. Download or clone this repository.
3. Run the program from a terminal:
   ```
   python3 smartstudy.py
   ```
4. Use the numbered main menu to manage subjects and tasks, run the
   planner, or view your progress. Use option 5 to save your data to
   `smartstudy_data.csv` and option 6 to load it back in on your next run.

## Instructions for testing

1. Add at least two subjects, then add a few tasks under each — include
   one with a deadline in the past to confirm it's flagged as overdue.
2. Try invalid input on purpose: a blank subject name, a task added under
   a subject that doesn't exist, a non-numeric deadline, hours of 0 or
   negative, an importance outside 1–5 — the program should re-prompt
   instead of crashing.
3. Mark one task Completed, then open the Workload & Progress Analyzer and
   confirm the completion percentage and subject-wise chart update
   correctly.
4. Run the Algorithmic Study Planner, enter a small number of available
   hours, and confirm the suggested task order fits within that budget.
5. Save to CSV, restart the program, load from CSV, and confirm every
   subject and task reappears exactly as it was.

## Project structure

```
smartstudy/
├── smartstudy.py           # Main program (Task class, StudyManager class, all 3 modules)
├── README.md
├── statement.md
└── smartstudy_data.csv     # Generated after you choose "Save data to CSV"
```

## Future enhancements

- A graphical or web front end instead of the console menu
- Recurring/repeating tasks (e.g. a weekly lab report)
- Exporting the subject-wise progress chart as an actual image using a
  charting library
