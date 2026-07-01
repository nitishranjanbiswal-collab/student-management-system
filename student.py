"""
Student Management System
--------------------------
A console-based application to Add, View, Search, Update, and Delete
student records. Data is persisted in a JSON file so records survive
between program runs.

Run with:  python student_management.py
"""

import json
import os
import re

DATA_FILE = "students.json"


# ----------------------------- Data Layer ----------------------------- #

def load_students():
    """Load student records from the JSON data file."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            return json.loads(content) if content else []
    except (json.JSONDecodeError, IOError):
        print("Warning: data file was unreadable or corrupted. Starting fresh.")
        return []


def save_students(students):
    """Persist the list of student records to the JSON data file."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(students, f, indent=4)


def get_next_id(students):
    """Generate the next sequential student ID."""
    if not students:
        return 1
    return max(s["id"] for s in students) + 1


# ----------------------------- Validation ----------------------------- #

def is_valid_email(email):
    pattern = r"^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def prompt_non_empty(label):
    while True:
        value = input(label).strip()
        if value:
            return value
        print("This field cannot be empty. Please try again.")


def prompt_age():
    while True:
        value = input("Age: ").strip()
        if value.isdigit() and 0 < int(value) < 120:
            return int(value)
        print("Please enter a valid age (a whole number between 1 and 119).")


def prompt_email():
    while True:
        value = input("Email: ").strip()
        if is_valid_email(value):
            return value
        print("Please enter a valid email address (e.g. name@example.com).")


def prompt_grade():
    return prompt_non_empty("Grade/Class (e.g. 10th, A, Freshman): ")


# ----------------------------- Core Features ----------------------------- #

def add_student(students):
    print("\n--- Add New Student ---")
    name = prompt_non_empty("Full Name: ")
    age = prompt_age()
    grade = prompt_grade()
    email = prompt_email()

    student = {
        "id": get_next_id(students),
        "name": name,
        "age": age,
        "grade": grade,
        "email": email,
    }
    students.append(student)
    save_students(students)
    print(f"\nStudent '{name}' added successfully with ID {student['id']}.")


def view_all_students(students):
    print("\n--- All Students ---")
    if not students:
        print("No student records found.")
        return
    print_table(students)


def print_table(students):
    header = f"{'ID':<5}{'Name':<22}{'Age':<6}{'Grade':<12}{'Email':<28}"
    print(header)
    print("-" * len(header))
    for s in students:
        print(f"{s['id']:<5}{s['name']:<22}{s['age']:<6}{s['grade']:<12}{s['email']:<28}")


def find_matches(students, keyword):
    keyword = keyword.lower().strip()
    matches = []
    for s in students:
        if (keyword == str(s["id"])
                or keyword in s["name"].lower()
                or keyword in s["email"].lower()):
            matches.append(s)
    return matches


def search_student(students):
    print("\n--- Search Student ---")
    if not students:
        print("No student records found.")
        return
    keyword = input("Enter student ID, name, or email to search: ").strip()
    matches = find_matches(students, keyword)
    if matches:
        print(f"\nFound {len(matches)} matching record(s):")
        print_table(matches)
    else:
        print("No matching student found.")


def select_student(students):
    """Helper to locate a single student by ID, with disambiguation if needed."""
    keyword = input("Enter student ID, name, or email: ").strip()
    matches = find_matches(students, keyword)
    if not matches:
        print("No matching student found.")
        return None
    if len(matches) == 1:
        return matches[0]
    print(f"\nMultiple matches found ({len(matches)}):")
    print_table(matches)
    chosen_id = input("Enter the exact ID of the student you mean: ").strip()
    for s in matches:
        if str(s["id"]) == chosen_id:
            return s
    print("Invalid ID selection.")
    return None


def update_student(students):
    print("\n--- Update Student ---")
    if not students:
        print("No student records found.")
        return
    student = select_student(students)
    if not student:
        return

    print(f"\nUpdating record for: {student['name']} (ID {student['id']})")
    print("Press Enter to keep the current value shown in brackets.\n")

    new_name = input(f"Full Name [{student['name']}]: ").strip()
    if new_name:
        student["name"] = new_name

    new_age = input(f"Age [{student['age']}]: ").strip()
    if new_age:
        if new_age.isdigit() and 0 < int(new_age) < 120:
            student["age"] = int(new_age)
        else:
            print("Invalid age entered; keeping previous value.")

    new_grade = input(f"Grade/Class [{student['grade']}]: ").strip()
    if new_grade:
        student["grade"] = new_grade

    new_email = input(f"Email [{student['email']}]: ").strip()
    if new_email:
        if is_valid_email(new_email):
            student["email"] = new_email
        else:
            print("Invalid email entered; keeping previous value.")

    save_students(students)
    print("\nStudent record updated successfully.")


def delete_student(students):
    print("\n--- Delete Student ---")
    if not students:
        print("No student records found.")
        return
    student = select_student(students)
    if not student:
        return

    confirm = input(
        f"Are you sure you want to delete '{student['name']}' (ID {student['id']})? (y/n): "
    ).strip().lower()
    if confirm == "y":
        students.remove(student)
        save_students(students)
        print("Student record deleted successfully.")
    else:
        print("Deletion cancelled.")


# ----------------------------- Menu / Main Loop ----------------------------- #

MENU = """
========================================
       STUDENT MANAGEMENT SYSTEM
========================================
1. Add Student
2. View All Students
3. Search Student
4. Update Student
5. Delete Student
6. Exit
========================================
"""


def main():
    students = load_students()
    while True:
        print(MENU)
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            view_all_students(students)
        elif choice == "3":
            search_student(students)
        elif choice == "4":
            update_student(students)
        elif choice == "5":
            delete_student(students)
        elif choice == "6":
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
