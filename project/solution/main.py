"""Student Result Management System - the menu (Day 16).

Run it with:  python main.py

HOW THE PROGRAM IS PUT TOGETHER
-------------------------------
This file is the only one the user talks to. It holds NO logic - it just
prints menus, reads input, and calls the `code` package:

    main.py  ->  code/utils.py    ask_int, ask_text, @log_action
             ->  code/storage.py  load_students, save_students
             ->  code/report.py   get_student, rank_list, class_summary
             ->  code/models.py   Student (and everything on it)

`students` is passed around everywhere. It is a DICTIONARY:

    {101: <Student>, 102: <Student>, 103: <Student>}

so students[101] finds a student instantly, without searching.
"""

# Two import styles (Day 16): whole module -> report.rank_list(), names -> Student().
from code import report, storage
from code.exceptions import InvalidMarkError, StudentNotFoundError
from code.models import SUBJECTS, Person, Student
from code.utils import ask_int, ask_text, log_action

MENU = """
1. Add student        3. View one student
2. Add marks          4. Class summary        0. Save & exit
"""


@log_action
def add_student(students):
    """Menu option 1. Put a new Student into the dictionary.

    ask_int and ask_text keep asking until the input is valid, so by the time
    we build the Student the roll number is a number and the name is letters.
    A roll number already in `students` is rejected with an early return.
    """
    roll_no = ask_int("Roll number : ", 1, 9999)
    if roll_no in students:
        print("  ! That roll number already exists.")
        return

    students[roll_no] = Student(roll_no, ask_text("Name        : "))
    print(f"  Added {students[roll_no].name}.")


@log_action
def add_marks(students):
    """Menu option 2. Set all three marks for one student.

    get_student raises StudentNotFoundError for an unknown roll number, and
    set_mark raises InvalidMarkError for a bad mark - both are caught in
    main() below. SUBJECTS is a set, so sorted() gives a predictable order.
    .average and .grade are properties, so they need no brackets.
    """
    student = report.get_student(students, ask_int("Roll number : ", 1, 9999))
    for subject in sorted(SUBJECTS):
        student.set_mark(subject, ask_int(f"  {subject:<10}: ", 0, 100))
    print(f"  Saved. Average {student.average}, grade {student.grade}.")


def view_student(students):
    """Menu option 3. Print one student's full details.

    Note the difference: .role() is a normal method so it takes brackets,
    while .marks, .average and .grade are properties and take none.
    """
    student = report.get_student(students, ask_int("Roll number : ", 1, 9999))
    print(f"\n  {student.name} ({student.role()}) - roll {student.roll_no}")
    for subject, mark in sorted(student.marks.items()):
        print(f"    {subject:<10} {mark:>6}")
    print(f"  Average {student.average}, grade {student.grade}")


def show_summary(students):
    """Menu option 4. Rank list, then the class numbers.

    print(student) calls Student.__str__ to draw each row. Person.count is a
    class variable - one counter shared by every Person object ever created.
    """
    summary = report.class_summary(students)
    if not summary["count"]:
        print("  No students yet.")
        return

    print(f"\n  {'ROLL':<6}{'NAME':<16}{'AVG':>6}  {'GRADE':<6}RESULT")
    for student in report.rank_list(students):
        print(f"  {student}")

    print(f"\n  Students {summary['count']}  |  "
          f"Class average {summary['average']}  |  "
          f"Pass {summary['pass_percent']}%")
    print(f"  Topper: {summary['topper'].name}")
    print(f"  (Person objects created this run: {Person.count})")


def main():
    """Load the data, run the menu until the user exits, then save.

    `actions` is a dictionary used as a switch: menu number -> function. Every
    one of them takes `students`, so they can all be called the same way.
    Catching our own exceptions here means one bad entry never stops the
    program - it prints the message and shows the menu again.
    """
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


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n  Interrupted.")
