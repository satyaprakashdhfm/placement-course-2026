"""Custom exceptions (Day 12)."""


class StudentNotFoundError(Exception):
    """Raised when a roll number does not exist."""

    def __init__(self, roll_no):
        self.roll_no = roll_no                 # extra data on the exception
        super().__init__(f"No student with roll number {roll_no}")


class InvalidMarkError(Exception):
    """Raised when a mark is not a number from 0 to 100."""

    def __init__(self, mark):
        self.mark = mark
        super().__init__(f"Invalid mark {mark!r} - must be 0 to 100")
