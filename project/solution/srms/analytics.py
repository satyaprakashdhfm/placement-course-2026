"""Reports and statistics - lambda, map, filter, sorted (Day 10)."""

from functools import reduce

from srms.exceptions import StudentNotFoundError
from srms.models import SUBJECTS


def get_student(students: dict, roll_no: int):
    """Fetch one student or raise our custom exception."""
    if roll_no not in students:
        raise StudentNotFoundError(roll_no)
    return students[roll_no]


def rank_list(students: dict) -> list:
    """Students sorted by average, highest first (sorted + lambda)."""
    return sorted(students.values(), key=lambda s: s.average, reverse=True)


def topper(students: dict):
    """Highest average. Returns None for an empty class."""
    if not students:
        return None
    return max(students.values(), key=lambda s: s.average)


def class_average(students: dict) -> float:
    """Average of all averages, using reduce()."""
    averages = [s.average for s in students.values()]      # list comprehension
    if not averages:
        return 0.0
    total = reduce(lambda a, b: a + b, averages)
    return round(total / len(averages), 2)


def pass_list(students: dict) -> list:
    """Only the students who passed (filter + lambda)."""
    return list(filter(lambda s: s.passed, students.values()))


def pass_percentage(students: dict) -> float:
    if not students:
        return 0.0
    return round(len(pass_list(students)) / len(students) * 100, 2)


def subject_averages(students: dict) -> dict:
    """Average mark per subject (dictionary comprehension)."""
    result = {}
    for subject in sorted(SUBJECTS):
        marks = [s.marks[subject] for s in students.values() if subject in s.marks]
        result[subject] = round(sum(marks) / len(marks), 2) if marks else 0.0
    return result


def grade_distribution(students: dict) -> dict:
    """How many students got each grade."""
    counts = {}
    for student in students.values():
        counts[student.grade] = counts.get(student.grade, 0) + 1
    return counts


def search_by_name(students: dict, term: str) -> list:
    """Case-insensitive partial name search (string methods, Day 5)."""
    term = term.strip().lower()
    return [s for s in students.values() if term in s.name.lower()]


def name_tags(students: dict) -> list:
    """Small map() demo: 'ROLL-NAME' labels for every student."""
    return list(map(lambda s: f"{s.roll_no}-{s.name.upper()}", students.values()))
