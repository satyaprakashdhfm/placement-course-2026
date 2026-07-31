"""srms - Student Result Management System.

This file turns the folder into a PACKAGE (Day 16).
It runs once, the first time anything from `srms` is imported.

Re-exporting the common names here lets users write the short form:
    from srms import Student
instead of the long form:
    from srms.models import Student
"""

from srms.models import GRADE_BANDS, SUBJECTS, Person, Student, Teacher
from srms.exceptions import (
    DuplicateStudentError,
    InvalidMarkError,
    InvalidSubjectError,
    SRMSError,
    StudentNotFoundError,
)

__version__ = "1.0"

__all__ = [
    "Person", "Student", "Teacher", "SUBJECTS", "GRADE_BANDS",
    "SRMSError", "StudentNotFoundError", "DuplicateStudentError",
    "InvalidMarkError", "InvalidSubjectError",
]
