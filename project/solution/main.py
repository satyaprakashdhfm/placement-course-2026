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

# TWO DIFFERENT IMPORT STYLES (Day 16 section 2) - both are used on purpose.
#
# 1. Import the MODULE itself. You then write report.rank_list(...), so the
#    name always says where the function came from. Good for functions whose
#    name alone would be vague: rank_list(...) could be anything, but
#    report.rank_list(...) is obvious.
from code import report, storage

# 2. Import NAMES out of a module. You then write Student(...) directly, with
#    no prefix. Good for things used constantly, where the prefix would only
#    add noise: models.Student(...) every time would be tiring to read.
from code.exceptions import InvalidMarkError, StudentNotFoundError
from code.models import SUBJECTS, Person, Student
from code.utils import ask_int, ask_text, log_action

# A third form works too: because code/__init__.py re-exports these names,
# `from code import Student` is also valid - that is what __init__.py is for.
#
# Never write `from code.models import *`. It hides where names came from and
# can silently overwrite your own variables.

MENU = """
1. Add student        3. View one student
2. Add marks          4. Class summary        0. Save & exit
"""


@log_action                                    # decorator -> logs every call
def add_student(students):
    """Menu option 1. Put a new Student into the dictionary."""
    roll_no = ask_int("Roll number : ", 1, 9999)      # utils: re-asks if bad
    if roll_no in students:                           # dict membership check
        print("  ! That roll number already exists.")
        return                                        # early return, nothing added

    # ask_text rejects digits and symbols, so the name is always clean here.
    # Student(...) runs Student.__init__, which runs Person.__init__.
    students[roll_no] = Student(roll_no, ask_text("Name        : "))
    print(f"  Added {students[roll_no].name}.")       # .name comes from Person


@log_action
def add_marks(students):
    """Menu option 2. Set all three marks for one student."""
    # get_student raises StudentNotFoundError if the roll number is unknown;
    # main() catches it at the bottom of this file.
    student = report.get_student(students, ask_int("Roll number : ", 1, 9999))

    # SUBJECTS is a set, so sorted() gives a predictable order every time.
    for subject in sorted(SUBJECTS):
        # set_mark validates the number and stores it in the private dict
        student.set_mark(subject, ask_int(f"  {subject:<10}: ", 0, 100))

    # .average and .grade are @property, so no brackets after them
    print(f"  Saved. Average {student.average}, grade {student.grade}.")


def view_student(students):
    """Menu option 3. Print one student's full details."""
    student = report.get_student(students, ask_int("Roll number : ", 1, 9999))

    # .role() IS a method, so it needs brackets - compare with .average below
    print(f"\n  {student.name} ({student.role()}) - roll {student.roll_no}")

    # .marks is a @property returning a copy of the private dict
    for subject, mark in sorted(student.marks.items()):
        print(f"    {subject:<10} {mark:>6}")

    print(f"  Average {student.average}, grade {student.grade}")


def show_summary(students):
    """Menu option 4. Rank list, then the class numbers."""
    summary = report.class_summary(students)          # a dict of 4 values
    if not summary["count"]:                          # empty class
        print("  No students yet.")
        return

    print(f"\n  {'ROLL':<6}{'NAME':<16}{'AVG':>6}  {'GRADE':<6}RESULT")
    for student in report.rank_list(students):        # sorted best first
        print(f"  {student}")                         # print() calls __str__

    print(f"\n  Students {summary['count']}  |  "
          f"Class average {summary['average']}  |  "
          f"Pass {summary['pass_percent']}%")
    print(f"  Topper: {summary['topper'].name}")

    # Person.count is a CLASS variable - one counter shared by every Person
    print(f"  (Person objects created this run: {Person.count})")


def main():
    """Load the data, run the menu until the user exits, then save."""
    print("\n===== STUDENT RESULT MANAGEMENT SYSTEM =====")
    students = storage.load_students()             # disk -> Student objects

    # A dictionary used as a switch: menu number -> function to run.
    # Every one of these takes `students`, so main() can call them the same way.
    actions = {1: add_student, 2: add_marks, 3: view_student, 4: show_summary}

    while True:
        print(MENU)
        choice = ask_int("Choice: ", 0, 4)          # only 0-4 can get through

        if choice == 0:
            storage.save_students(students)         # Student objects -> disk
            print("  Saved. Goodbye!")
            break                                   # leave the while loop

        try:
            actions[choice](students)               # run the chosen function
        except (StudentNotFoundError, InvalidMarkError) as e:
            # Our own exceptions from code/exceptions.py. Catching them here
            # means one bad entry never kills the program.
            print(f"  ! {e}")


if __name__ == "__main__":          # only runs when you do `python main.py`,
    try:                            # not when something imports this file
        main()
    except (KeyboardInterrupt, EOFError):           # Ctrl+C or end of input
        print("\n  Interrupted.")
