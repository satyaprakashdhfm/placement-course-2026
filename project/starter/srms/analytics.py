"""Reports and statistics - lambda, map, filter, sorted, reduce (Day 10).

Every function here must use the built-in tool named in its docstring.
"""

from functools import reduce

from srms.exceptions import StudentNotFoundError
from srms.models import SUBJECTS


def get_student(students: dict, roll_no: int):
    """Return one student, or raise StudentNotFoundError."""
    # TODO
    pass


def rank_list(students: dict) -> list:
    """Use sorted() + lambda: highest average first."""
    # TODO
    pass


def topper(students: dict):
    """Use max() with a key. Return None for an empty class."""
    # TODO
    pass


def class_average(students: dict) -> float:
    """Use a list comprehension + reduce() to average all averages."""
    # TODO
    pass


def pass_list(students: dict) -> list:
    """Use filter() + lambda to keep only students who passed."""
    # TODO
    pass


def pass_percentage(students: dict) -> float:
    """len(pass_list) / len(students) * 100, rounded to 2 decimals."""
    # TODO
    pass


def subject_averages(students: dict) -> dict:
    """Average mark for each subject -> {"maths": 70.33, ...}."""
    # TODO
    pass


def grade_distribution(students: dict) -> dict:
    """Count how many students got each grade -> {"A+": 1, "B": 1, ...}."""
    # TODO
    pass


def search_by_name(students: dict, term: str) -> list:
    """Case-insensitive PARTIAL name search using string methods."""
    # TODO
    pass


def name_tags(students: dict) -> list:
    """Use map() + lambda to build 'ROLL-NAME' labels."""
    # TODO
    pass
