"""Custom exceptions (Day 12).

TODO: Create one base class and four specific exceptions below.
Each specific exception should INHERIT from SRMSError.
"""


class SRMSError(Exception):
    """Base class for every error in this project."""
    pass


class StudentNotFoundError(SRMSError):
    """Raised when a roll number does not exist."""
    # TODO: accept roll_no in __init__, store it, and build a clear message
    pass


class DuplicateStudentError(SRMSError):
    """Raised when adding a roll number that already exists."""
    # TODO
    pass


class InvalidMarkError(SRMSError):
    """Raised when a mark is not a number between 0 and 100."""
    # TODO
    pass


class InvalidSubjectError(SRMSError):
    """Raised when a subject is not in SUBJECTS."""
    # TODO
    pass
