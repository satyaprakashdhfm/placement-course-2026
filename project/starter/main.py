"""Student Result Management System - menu driven console app.

Run it with:  python main.py
"""

from code import report, storage
from code.exceptions import InvalidMarkError, StudentNotFoundError
from code.models import SUBJECTS, Student
from code.utils import ask_int, ask_text, log_action

MENU = """
1. Add student        3. View one student
2. Add marks          4. Class summary        0. Save & exit
"""


@log_action
def add_student(students):
    roll_no = ask_int("Roll number : ", 1, 9999)
    if roll_no in students:
        print("  ! That roll number already exists.")
        return
    students[roll_no] = Student(roll_no, ask_text("Name        : "))
    print(f"  Added {students[roll_no].name}.")


@log_action
def add_marks(students):
    student = report.get_student(students, ask_int("Roll number : ", 1, 9999))
    for subject in sorted(SUBJECTS):
        student.set_mark(subject, ask_int(f"  {subject:<10}: ", 0, 100))
    print(f"  Saved. Average {student.average}, grade {student.grade}.")


def view_student(students):
    student = report.get_student(students, ask_int("Roll number : ", 1, 9999))
    print(f"\n  {student.name} (roll {student.roll_no})")
    for subject, mark in sorted(student.marks.items()):
        print(f"    {subject:<10} {mark:>6}")
    print(f"  Average {student.average}, grade {student.grade}")


def show_summary(students):
    """Rank list + the few class numbers."""
    summary = report.class_summary(students)
    if not summary["count"]:
        print("  No students yet.")
        return

    print(f"\n  {'ROLL':<6}{'NAME':<16}{'AVG':>6}  {'GRADE':<6}RESULT")
    for student in report.rank_list(students):
        print(f"  {student}")                       # uses __str__

    print(f"\n  Students {summary['count']}  |  "
          f"Class average {summary['average']}  |  "
          f"Pass {summary['pass_percent']}%")
    print(f"  Topper: {summary['topper'].name}")


def main():
    print("\n===== STUDENT RESULT MANAGEMENT SYSTEM =====")
    students = storage.load_students()
    actions = {1: add_student, 2: add_marks, 3: view_student, 4: show_summary}

    while True:
        print(MENU)
        choice = ask_int("Choice: ", 0, 4)
        if choice == 0:
            storage.save_students(students)
            print("  Saved. Goodbye!")
            break
        try:
            actions[choice](students)
        except (StudentNotFoundError, InvalidMarkError) as e:
            print(f"  ! {e}")


if __name__ == "__main__":                          # Day 16
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n  Interrupted.")
