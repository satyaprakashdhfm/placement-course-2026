"""Student Result Management System - menu driven console app.

Run it with:  python main.py
"""

from srms import analytics, storage
from srms.exceptions import DuplicateStudentError, SRMSError, StudentNotFoundError
from srms.models import SUBJECTS, Student, Teacher
from srms.utils import ask_int, ask_text, banner, log_action

CLASS_TEACHER = Teacher("Meera Nair", "maths")

MENU = """
1. Add student           5. Class statistics
2. Add / update marks    6. Search by name
3. View one student      7. Export report (CSV)
4. Rank list             8. Backup database (threaded)
                         0. Save & exit
"""


# ---------------------------------------------------------------- actions
@log_action
def add_student(students: dict) -> None:
    banner("add student")
    roll_no = ask_int("Roll number : ", 1, 9999)
    if roll_no in students:
        raise DuplicateStudentError(roll_no)
    name = ask_text("Full name   : ")
    students[roll_no] = Student(roll_no, name)
    print(f"  Added {students[roll_no].name}.")


@log_action
def add_marks(students: dict) -> None:
    banner("add / update marks")
    roll_no = ask_int("Roll number : ", 1, 9999)
    student = analytics.get_student(students, roll_no)      # may raise
    print(f"  Entering marks for {student.name}")
    for subject in sorted(SUBJECTS):
        mark = ask_int(f"   {subject.title():<10}: ", 0, 100)
        student.set_mark(subject, mark)
    print(f"  Saved. Average {student.average}, grade {student.grade}.")


def view_student(students: dict) -> None:
    banner("student details")
    roll_no = ask_int("Roll number : ", 1, 9999)
    student = analytics.get_student(students, roll_no)
    print(f"\n  Roll number : {student.roll_no}")
    print(f"  Name        : {student.name}")
    print(f"  Subjects    : {len(student)}")               # __len__
    for subject, mark in sorted(student.marks.items()):
        print(f"    {subject.title():<10} {mark:>6}")
    print(f"  Total       : {student.total}")
    print(f"  Average     : {student.average}")
    print(f"  Grade       : {student.grade}")
    print(f"  Result      : {'PASS' if student.passed else 'FAIL'}")


def show_rank_list(students: dict) -> None:
    banner("rank list")
    if not students:
        print("  No students yet.")
        return
    print(f"  {'RANK':<6}{'ROLL':<7}{'NAME':<18}{'AVG':>7}  GRADE  RESULT")
    print("  " + "-" * 50)
    for position, student in enumerate(analytics.rank_list(students), start=1):
        result = "PASS" if student.passed else "FAIL"
        print(f"  {position:<6}{student.roll_no:<7}{student.name:<18}"
              f"{student.average:>7}  {student.grade:<6} {result}")


def show_statistics(students: dict) -> None:
    banner("class statistics")
    if not students:
        print("  No students yet.")
        return

    best = analytics.topper(students)
    print(f"  Students        : {len(students)}")
    print(f"  Class average   : {analytics.class_average(students)}")
    print(f"  Pass percentage : {analytics.pass_percentage(students)} %")
    print(f"  Topper          : {best.name} ({best.average})")

    print("\n  Subject averages:")
    for subject, avg in analytics.subject_averages(students).items():
        bar = "#" * int(avg // 5)                          # tiny text chart
        print(f"    {subject.title():<10} {avg:>6}  {bar}")

    print("\n  Grade distribution:")
    for grade, count in sorted(analytics.grade_distribution(students).items()):
        print(f"    {grade:<4} {'*' * count} ({count})")

    # POLYMORPHISM: one loop, two different classes, same .describe()
    print("\n  People in this class:")
    people = [CLASS_TEACHER] + analytics.rank_list(students)
    for person in people:
        print(f"    - {person.describe()}")


def search_students(students: dict) -> None:
    banner("search")
    term = ask_text("Name contains : ")
    found = analytics.search_by_name(students, term)
    if not found:
        print("  Nothing found.")
        return
    for student in found:
        print(f"  {student}")                              # uses __str__


def export_report(students: dict) -> None:
    banner("export report")
    if not students:
        print("  Nothing to export.")
        return
    path = storage.export_csv(students)
    print(f"  Written to {path}")


def run_backup() -> None:
    banner("backup")
    thread = storage.backup_in_background()
    print("  Backup started in the background...")
    thread.join()                                          # wait for it
    print("  Backup finished.")


# ---------------------------------------------------------------- main loop
def main() -> None:
    banner("student result management system")
    students = storage.load_students()

    actions = {                                            # dict as a switch
        1: lambda: add_student(students),
        2: lambda: add_marks(students),
        3: lambda: view_student(students),
        4: lambda: show_rank_list(students),
        5: lambda: show_statistics(students),
        6: lambda: search_students(students),
        7: lambda: export_report(students),
        8: run_backup,
    }

    while True:
        print(MENU)
        choice = ask_int("Choice: ", 0, 8)

        if choice == 0:
            storage.save_students(students)
            print("\n  Saved. Goodbye!")
            break

        try:
            actions[choice]()
        except (StudentNotFoundError, DuplicateStudentError) as e:
            print(f"  ! {e}")
        except SRMSError as e:                             # any other project error
            print(f"  ! {e}")


if __name__ == "__main__":                                 # Day 16
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n  Interrupted. Bye!")
