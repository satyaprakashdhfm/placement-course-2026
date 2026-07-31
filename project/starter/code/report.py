"""Class reports - lambda, sorted, filter, max (Day 10).

Each function must use the built-in named in its docstring.
"""

from code.exceptions import StudentNotFoundError


def get_student(students, roll_no):
    """Return one student, or raise StudentNotFoundError."""
    # TODO
    pass


def rank_list(students):
    """Use sorted() + lambda: highest average first."""
    # TODO
    pass


def class_summary(students):
    """Return {"count", "average", "pass_percent", "topper"}.

    - count        -> how many students
    - average      -> average of every student's average, rounded to 2
    - pass_percent -> % of students whose grade is not "F"  (use filter + lambda)
    - topper       -> the student with the best average     (use max + lambda)

    For an empty class return count 0, average 0.0, pass_percent 0.0, topper None.
    """
    # TODO
    pass
