# Problem Statement

**Author:** Avika Jain
**Registration No.:** 26BCE10206
**University:** VIT Bhopal University
**Program:** 1st Year BTech CSE Core

## Problem statement

Students juggling multiple subjects and assignments often lose track of
what's due, how urgent each task really is, and how much time it will
actually take to finish everything. Without a structured system, easy or
low-priority tasks can end up eating time that overdue, high-importance
work needed instead. SmartStudy solves this by giving each task a
measurable urgency score based on its deadline and importance, using that
score to suggest what to work on next, and summarizing overall progress so
the student can see exactly where they stand.

## Scope of the project

SmartStudy is a command-line, single-user Python application built around
two classes — `Task` and `StudyManager` — that together provide:

- Full CRUD management of subjects and tasks
- An algorithmic planner that ranks tasks by urgency and fits a suggested
  study order into the time the student has available
- A workload and progress analyzer that reports completion percentages,
  subject-wise progress, pending hours, and a weekly summary

Data persists across sessions through a CSV file the student can save to
and load from. The project does not include a graphical interface,
multi-user accounts, or a full database — these are outside the scope of
a first-year, single-file Python project.

## Target users

Students who want a structured, priority-driven way to manage study tasks
across multiple subjects instead of relying on memory or an unordered
to-do list.

## High-level features

1. **Task & Subject Management** — add, edit, delete, and view subjects
   and tasks, with full input validation.
2. **Algorithmic Study Planner** — urgency-based sorting, overdue
   detection, and a suggested task order that fits available time.
3. **Workload & Progress Analyzer** — completion percentage, subject-wise
   progress chart, pending hours, and weekly workload summary.
