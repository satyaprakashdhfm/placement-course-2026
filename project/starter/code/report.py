"""Class reports - lambda, sorted, filter, max (Day 10).

WHAT THIS FILE IS
-----------------
Three small functions that ANSWER QUESTIONS about the class. None of them
print anything - they return values, and main.py does the printing. That is
why the same function can be reused anywhere.

Everywhere below, `students` is the dictionary {roll_no: Student}, so
`students.values()` gives you the Student objects.

SELF-CHECK (run from the project folder, the one with main.py):

    python -c "from code.storage import load_students; from code.report import class_summary; s = class_summary(load_students()); print(s['count'], s['average'], s['pass_percent'], s['topper'].name)"

Expected output (with the 3 students you were given):
      Loaded 3 student(s).
    3 69.11 66.67 Anita Sharma
"""

from code.exceptions import StudentNotFoundError  # our own error class


def get_student(students, roll_no):
    """Return one Student, or raise StudentNotFoundError.

    USED BY: main.py -> add_marks() and view_student().
    """
    # TODO 1: two lines.
    #   a) if roll_no is not in students -> raise StudentNotFoundError(roll_no)
    #   b) otherwise return students[roll_no]
    #
    # Every other part of the program looks students up through this function,
    # so the "not found" message is written in only ONE place.
    pass


def rank_list(students):
    """All students sorted by average, best first.

    USED BY: main.py -> show_summary(), the loop that prints the table.
    """
    # TODO 2: one line, using sorted() with a lambda as the key:
    #
    #     sorted(students.values(), key=lambda s: s.average, reverse=True)
    #
    #   key=lambda s: s.average  tells sorted WHAT to compare (each student's
    #                            average, not the student object itself)
    #   reverse=True             makes it biggest first
    pass


def class_summary(students):
    """Return the few numbers shown for the whole class.

    USED BY: main.py -> show_summary(), which reads all 4 keys.

    Must return a dictionary with exactly these 4 keys:

        {"count": 3, "average": 69.11, "pass_percent": 66.67, "topper": <Student>}
    """
    # TODO 3: start with the empty case, then the real one.
    #
    #   a) GUARD CLAUSE - if `students` is empty there is nothing to divide by:
    #        return {"count": 0, "average": 0.0, "pass_percent": 0.0, "topper": None}
    #
    #   b) who passed?  filter() keeps only the items where the test is True:
    #        passed = list(filter(lambda s: s.grade != "F", students.values()))
    #
    #   c) every average, as a list comprehension:
    #        averages = [s.average for s in students.values()]
    #
    #   d) build and return the dictionary:
    #        "count"        -> len(students)
    #        "average"      -> round(sum(averages) / len(averages), 2)
    #        "pass_percent" -> round(len(passed) / len(students) * 100, 2)
    #        "topper"       -> max(students.values(), key=lambda s: s.average)
    #
    #      max() with a key works just like sorted() with a key: it compares
    #      the averages but gives you back the whole Student.
    pass
