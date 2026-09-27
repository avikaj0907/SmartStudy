"""
SmartStudy - Algorithmic Study Planner & Workload Analyzer
------------------------------------------------------------
Author       : Avika Jain
Registration : 26BCE10206
University   : VIT Bhopal University
Program      : 1st Year BTech CSE Core

This program is organized into three modules, matching the project
specification:

  Module 1 - Task & Subject Management
             Add/edit/delete subjects and tasks, mark tasks pending or
             completed, view tasks by subject or status.

  Module 2 - Algorithmic Study Planner
             Sorts tasks by deadline and importance, flags overdue tasks,
             totals estimated study hours, and suggests a task order that
             fits inside the time the student actually has available.

  Module 3 - Workload & Progress Analyzer
             Calculates completion percentage, subject-wise progress,
             pending hours, and a weekly workload summary, and displays
             the results as simple console tables/charts.

Data is kept in memory for the session and can be saved to / loaded from
a CSV file so progress isn't lost between runs.
"""

import csv
import os
from datetime import date, datetime, timedelta


# ============================================================
# MODULE 1: Task & Subject Management (data model, OOP + CRUD)
# ============================================================

class Task:
    """Represents a single study task belonging to a subject."""

    def __init__(self, task_id, title, subject, deadline, estimated_hours,
                 importance, status="Pending"):
        self.task_id = task_id
        self.title = title
        self.subject = subject
        self.deadline = deadline              # a datetime.date object
        self.estimated_hours = estimated_hours
        self.importance = importance          # 1 (low) to 5 (high)
        self.status = status                  # "Pending" or "Completed"

    def is_overdue(self, today):
        """A task is overdue if it's still pending and its deadline has passed."""
        return self.status == "Pending" and self.deadline < today

    def to_row(self):
        """Converts the task into a list of values, for printing or CSV export."""
        return [
            self.task_id, self.title, self.subject, self.deadline.isoformat(),
            self.estimated_hours, self.importance, self.status
        ]


class StudyManager:
    """
    Holds all subjects and tasks and provides the CRUD, planning, and
    analysis operations used by the menu system below.
    """

    def __init__(self):
        self.subjects = []      # list of subject name strings
        self.tasks = []         # list of Task objects
        self.next_task_id = 1

    # ---------------- Subject CRUD ----------------

    def add_subject(self, name):
        if name in self.subjects:
            return False, "That subject already exists."
        self.subjects.append(name)
        return True, "Subject added."

    def edit_subject(self, old_name, new_name):
        if old_name not in self.subjects:
            return False, "Subject not found."
        if new_name in self.subjects:
            return False, "A subject with the new name already exists."
        index = self.subjects.index(old_name)
        self.subjects[index] = new_name
        for task in self.tasks:
            if task.subject == old_name:
                task.subject = new_name
        return True, "Subject renamed."

    def delete_subject(self, name):
        if name not in self.subjects:
            return False, "Subject not found."
        self.subjects.remove(name)
        remaining_tasks = []
        for task in self.tasks:
            if task.subject != name:
                remaining_tasks.append(task)
        self.tasks = remaining_tasks
        return True, "Subject and its tasks were deleted."

    # ---------------- Task CRUD ----------------

    def add_task(self, title, subject, deadline, estimated_hours, importance):
        if subject not in self.subjects:
            return False, "Subject does not exist. Add the subject first."
        task = Task(self.next_task_id, title, subject, deadline,
                    estimated_hours, importance)
        self.tasks.append(task)
        self.next_task_id = self.next_task_id + 1
        return True, "Task added."

    def edit_task(self, task_id, title=None, deadline=None,
                  estimated_hours=None, importance=None):
        task = self.find_task(task_id)
        if task is None:
            return False, "Task not found."
        if title is not None:
            task.title = title
        if deadline is not None:
            task.deadline = deadline
        if estimated_hours is not None:
            task.estimated_hours = estimated_hours
        if importance is not None:
            task.importance = importance
        return True, "Task updated."

    def delete_task(self, task_id):
        task = self.find_task(task_id)
        if task is None:
            return False, "Task not found."
        self.tasks.remove(task)
        return True, "Task deleted."

    def mark_status(self, task_id, status):
        task = self.find_task(task_id)
        if task is None:
            return False, "Task not found."
        task.status = status
        return True, "Task marked as " + status + "."

    def find_task(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

    def tasks_by_subject(self, subject):
        result = []
        for task in self.tasks:
            if task.subject == subject:
                result.append(task)
        return result

    def tasks_by_status(self, status):
        result = []
        for task in self.tasks:
            if task.status == status:
                result.append(task)
        return result

    # ---------------- Persistence (CSV) ----------------

    def save_to_csv(self, filename="smartstudy_data.csv"):
        try:
            with open(filename, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Subjects"])
                for subject in self.subjects:
                    writer.writerow([subject])
                writer.writerow([])
                writer.writerow(["TaskID", "Title", "Subject", "Deadline",
                                  "EstimatedHours", "Importance", "Status"])
                for task in self.tasks:
                    writer.writerow(task.to_row())
            return True, "Saved to " + filename + "."
        except OSError as error:
            return False, "Could not save file: " + str(error)

    def load_from_csv(self, filename="smartstudy_data.csv"):
        if not os.path.exists(filename):
            return False, "No saved file found."
        try:
            with open(filename, "r", newline="") as file:
                reader = list(csv.reader(file))

            self.subjects = []
            self.tasks = []
            max_id = 0

            i = 1  # row 0 is the "Subjects" header
            while i < len(reader) and reader[i] and reader[i][0] != "":
                self.subjects.append(reader[i][0])
                i = i + 1

            # skip the blank row and the task header row
            i = i + 2
            while i < len(reader):
                row = reader[i]
                if row:
                    task_id = int(row[0])
                    title = row[1]
                    subject = row[2]
                    deadline = datetime.strptime(row[3], "%Y-%m-%d").date()
                    estimated_hours = float(row[4])
                    importance = int(row[5])
                    status = row[6]
                    task = Task(task_id, title, subject, deadline,
                                estimated_hours, importance, status)
                    self.tasks.append(task)
                    if task_id > max_id:
                        max_id = task_id
                i = i + 1

            self.next_task_id = max_id + 1
            return True, "Loaded from " + filename + "."
        except (OSError, ValueError, IndexError) as error:
            return False, "Could not load file: " + str(error)


# ============================================================
# MODULE 2: Algorithmic Study Planner
# ============================================================

def priority_score(task, today):
    """
    Higher score = more urgent.
    Overdue tasks always rank above tasks that are still on time.
    Otherwise, higher importance and fewer days left both raise the score.
    """
    days_left = (task.deadline - today).days
    if days_left <= 0:
        return 1000 + (task.importance * 10)
    return (task.importance * 10) / days_left


def sort_tasks_by_priority(tasks, today):
    """
    Returns a NEW list of pending tasks sorted from most to least urgent,
    using a manual selection sort so the ranking logic stays visible.
    """
    pending = []
    for task in tasks:
        if task.status == "Pending":
            pending.append(task)

    n = len(pending)
    for i in range(n):
        best_index = i
        best_score = priority_score(pending[i], today)
        for j in range(i + 1, n):
            score = priority_score(pending[j], today)
            if score > best_score:
                best_index = j
                best_score = score
        pending[i], pending[best_index] = pending[best_index], pending[i]

    return pending


def get_overdue_tasks(tasks, today):
    overdue = []
    for task in tasks:
        if task.is_overdue(today):
            overdue.append(task)
    return overdue


def total_estimated_hours(tasks, status="Pending"):
    total = 0
    for task in tasks:
        if task.status == status:
            total = total + task.estimated_hours
    return total


def suggested_task_order(sorted_pending_tasks, available_hours):
    """
    Walks the priority-sorted task list and greedily fits as many tasks as
    possible into the hours the student says they have available.
    Skips a task that would overflow the remaining budget and checks the
    next one, so smaller lower-priority tasks can still fill gaps.
    """
    plan = []
    remaining_hours = available_hours
    for task in sorted_pending_tasks:
        if task.estimated_hours <= remaining_hours:
            plan.append(task)
            remaining_hours = remaining_hours - task.estimated_hours
    return plan, remaining_hours


# ============================================================
# MODULE 3: Workload & Progress Analyzer
# ============================================================

def completion_percentage(tasks):
    if len(tasks) == 0:
        return 0
    completed = 0
    for task in tasks:
        if task.status == "Completed":
            completed = completed + 1
    return round((completed / len(tasks)) * 100, 1)


def subject_wise_progress(tasks, subjects):
    """Returns a dict: subject -> (completed_count, total_count, percent)."""
    progress = {}
    for subject in subjects:
        total = 0
        completed = 0
        for task in tasks:
            if task.subject == subject:
                total = total + 1
                if task.status == "Completed":
                    completed = completed + 1
        if total == 0:
            percent = 0
        else:
            percent = round((completed / total) * 100, 1)
        progress[subject] = (completed, total, percent)
    return progress


def pending_hours(tasks):
    return total_estimated_hours(tasks, status="Pending")


def weekly_summary(tasks, today):
    """Returns tasks due within the next 7 days (inclusive) and their total hours."""
    week_end = today + timedelta(days=7)
    due_this_week = []
    for task in tasks:
        if task.status == "Pending" and today <= task.deadline <= week_end:
            due_this_week.append(task)
    total_hours = 0
    for task in due_this_week:
        total_hours = total_hours + task.estimated_hours
    return due_this_week, total_hours


def print_progress_chart(progress):
    """Prints a simple text bar chart of subject-wise completion percentage."""
    print("\nSubject-wise Progress")
    for subject in progress:
        completed, total, percent = progress[subject]
        bar_length = int(percent / 5)  # 1 block per 5%
        bar = "#" * bar_length
        print(subject + ": [" + bar.ljust(20) + "] " + str(percent) + "% ("
              + str(completed) + "/" + str(total) + " tasks)")


# ============================================================
# Input helpers
# ============================================================

def ask_text(prompt, allow_empty=False):
    while True:
        value = input(prompt).strip()
        if value != "" or allow_empty:
            return value
        print("This field cannot be empty.")


def ask_positive_number(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than 0.")
                continue
            return value
        except ValueError:
            print("That doesn't look like a number. Try again.")


def ask_importance(prompt):
    while True:
        try:
            value = int(input(prompt))
            if 1 <= value <= 5:
                return value
            print("Importance must be between 1 and 5.")
        except ValueError:
            print("Please enter a whole number from 1 to 5.")


def ask_date(prompt):
    while True:
        text = input(prompt).strip()
        try:
            return datetime.strptime(text, "%Y-%m-%d").date()
        except ValueError:
            print("Please use the format YYYY-MM-DD, e.g. 2026-10-05.")


def ask_task_id(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid task ID number.")


# ============================================================
# Menu / UI layer
# ============================================================

def print_task_table(tasks):
    if not tasks:
        print("No tasks to show.")
        return
    print("{:<4}{:<20}{:<12}{:<12}{:<8}{:<6}{:<10}".format(
        "ID", "Title", "Subject", "Deadline", "Hours", "Imp", "Status"))
    for task in tasks:
        print("{:<4}{:<20}{:<12}{:<12}{:<8}{:<6}{:<10}".format(
            task.task_id, task.title[:19], task.subject[:11],
            task.deadline.isoformat(), task.estimated_hours,
            task.importance, task.status))


def subject_menu(manager):
    print("\n--- Manage Subjects ---")
    print("1. Add subject | 2. Edit subject | 3. Delete subject | 4. View subjects | 0. Back")
    choice = input("Choose an option: ").strip()

    if choice == "1":
        name = ask_text("Subject name: ")
        ok, message = manager.add_subject(name)
        print(message)
    elif choice == "2":
        old_name = ask_text("Existing subject name: ")
        new_name = ask_text("New subject name: ")
        ok, message = manager.edit_subject(old_name, new_name)
        print(message)
    elif choice == "3":
        name = ask_text("Subject name to delete: ")
        ok, message = manager.delete_subject(name)
        print(message)
    elif choice == "4":
        if manager.subjects:
            for subject in manager.subjects:
                print("- " + subject)
        else:
            print("No subjects yet.")


def task_menu(manager):
    print("\n--- Manage Tasks ---")
    print("1. Add task | 2. Edit task | 3. Delete task | 4. Mark complete/pending")
    print("5. View by subject | 6. View by status | 0. Back")
    choice = input("Choose an option: ").strip()

    if choice == "1":
        if not manager.subjects:
            print("Add a subject first.")
            return
        title = ask_text("Task title: ")
        subject = ask_text("Subject (must already exist): ")
        deadline = ask_date("Deadline (YYYY-MM-DD): ")
        hours = ask_positive_number("Estimated hours: ")
        importance = ask_importance("Importance (1-5): ")
        ok, message = manager.add_task(title, subject, deadline, hours, importance)
        print(message)

    elif choice == "2":
        task_id = ask_task_id("Task ID to edit: ")
        print("Leave a field blank to keep it unchanged.")
        title = ask_text("New title: ", allow_empty=True)
        hours_text = input("New estimated hours: ").strip()
        importance_text = input("New importance (1-5): ").strip()
        ok, message = manager.edit_task(
            task_id,
            title=title if title != "" else None,
            estimated_hours=float(hours_text) if hours_text != "" else None,
            importance=int(importance_text) if importance_text != "" else None
        )
        print(message)

    elif choice == "3":
        task_id = ask_task_id("Task ID to delete: ")
        ok, message = manager.delete_task(task_id)
        print(message)

    elif choice == "4":
        task_id = ask_task_id("Task ID: ")
        status = ask_text("New status (Pending/Completed): ")
        ok, message = manager.mark_status(task_id, status)
        print(message)

    elif choice == "5":
        subject = ask_text("Subject: ")
        print_task_table(manager.tasks_by_subject(subject))

    elif choice == "6":
        status = ask_text("Status (Pending/Completed): ")
        print_task_table(manager.tasks_by_status(status))


def planner_menu(manager):
    today = date.today()
    print("\n--- Algorithmic Study Planner ---")
    sorted_tasks = sort_tasks_by_priority(manager.tasks, today)

    print("\nTasks ranked by urgency (most urgent first):")
    print_task_table(sorted_tasks)

    overdue = get_overdue_tasks(manager.tasks, today)
    print("\nOverdue tasks: " + str(len(overdue)))
    if overdue:
        print_task_table(overdue)

    total_hours = total_estimated_hours(manager.tasks, status="Pending")
    print("\nTotal pending study hours needed: " + str(total_hours))

    available = ask_positive_number("\nHow many hours do you have available right now? ")
    plan, leftover = suggested_task_order(sorted_tasks, available)
    print("\nSuggested task order for your available time:")
    print_task_table(plan)
    print("Hours left unused: " + str(round(leftover, 2)))


def analyzer_menu(manager):
    today = date.today()
    print("\n--- Workload & Progress Analyzer ---")

    percent = completion_percentage(manager.tasks)
    print("Overall completion: " + str(percent) + "%")

    progress = subject_wise_progress(manager.tasks, manager.subjects)
    print_progress_chart(progress)

    pending = pending_hours(manager.tasks)
    print("\nTotal pending hours: " + str(pending))

    due_this_week, week_hours = weekly_summary(manager.tasks, today)
    print("\nTasks due in the next 7 days: " + str(len(due_this_week)))
    print_task_table(due_this_week)
    print("Hours needed this week: " + str(week_hours))


def main():
    manager = StudyManager()
    print("=== SmartStudy: Algorithmic Study Planner & Workload Analyzer ===")
    print("Avika Jain | 26BCE10206 | VIT Bhopal University | 1st Year BTech CSE Core")

    while True:
        print("\n===== MAIN MENU =====")
        print("1. Manage Subjects")
        print("2. Manage Tasks")
        print("3. Algorithmic Study Planner")
        print("4. Workload & Progress Analyzer")
        print("5. Save data to CSV")
        print("6. Load data from CSV")
        print("0. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            subject_menu(manager)
        elif choice == "2":
            task_menu(manager)
        elif choice == "3":
            planner_menu(manager)
        elif choice == "4":
            analyzer_menu(manager)
        elif choice == "5":
            ok, message = manager.save_to_csv()
            print(message)
        elif choice == "6":
            ok, message = manager.load_from_csv()
            print(message)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    main()
