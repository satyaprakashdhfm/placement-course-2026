"""Class reports - lambda, sorted, filter, max (Day 10)."""

from code.exceptions import StudentNotFoundError


def get_student(students, roll_no):
    """Return one student or raise our custom exception."""
    if roll_no not in students:
        raise StudentNotFoundError(roll_no)
    return students[roll_no]


def rank_list(students):
    """Students sorted by average, best first (sorted + lambda)."""
    return sorted(students.values(), key=lambda s: s.average, reverse=True)


def class_summary(students):
    """Return the few numbers we show for the whole class."""
    if not students:
        return {"count": 0, "average": 0.0, "pass_percent": 0.0, "topper": None}

    passed = list(filter(lambda s: s.grade != "F", students.values()))
    averages = [s.average for s in students.values()]        # comprehension
    return {
        "count": len(students),
        "average": round(sum(averages) / len(averages), 2),
        "pass_percent": round(len(passed) / len(students) * 100, 2),
        "topper": max(students.values(), key=lambda s: s.average),
    }
