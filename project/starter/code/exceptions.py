"""Custom exceptions (Day 12).

TODO: give each class an __init__ that stores the value and builds a clear
message by calling super().__init__(...).
"""


class StudentNotFoundError(Exception):
    """Raised when a roll number does not exist."""
    # TODO: accept roll_no, store it as self.roll_no,
    #       message: "No student with roll number 999"
    pass


class InvalidMarkError(Exception):
    """Raised when a mark is not a number from 0 to 100."""
    # TODO: accept mark, store it as self.mark,
    #       message: "Invalid mark 'abc' - must be 0 to 100"
    pass
