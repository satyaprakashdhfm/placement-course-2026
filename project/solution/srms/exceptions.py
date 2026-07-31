"""Custom exceptions for the Student Result Management System (Day 12)."""


class SRMSError(Exception):
    """Base class for every error raised by this project.

    Having one base class means a caller can catch *all* our errors with a
    single `except SRMSError:` while still being able to catch specific ones.
    """
    pass


class StudentNotFoundError(SRMSError):
    """Raised when a roll number does not exist in the registry."""

    def __init__(self, roll_no):
        self.roll_no = roll_no                      # extra data on the exception
        super().__init__(f"No student found with roll number {roll_no}")


class DuplicateStudentError(SRMSError):
    """Raised when adding a roll number that already exists."""

    def __init__(self, roll_no):
        self.roll_no = roll_no
        super().__init__(f"Student with roll number {roll_no} already exists")


class InvalidMarkError(SRMSError):
    """Raised when a mark is not a number between 0 and 100."""

    def __init__(self, mark):
        self.mark = mark
        super().__init__(f"Invalid mark {mark!r} - must be a number from 0 to 100")


class InvalidSubjectError(SRMSError):
    """Raised when a subject is not part of the syllabus."""

    def __init__(self, subject, allowed):
        self.subject = subject
        super().__init__(
            f"Unknown subject {subject!r} - allowed: {', '.join(sorted(allowed))}"
        )
