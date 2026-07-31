"""Student Result Management System.

This file turns the folder into a PACKAGE (Day 16).
It runs once, the first time anything from `code` is imported.

Re-exporting here lets you write `from code import Student`
instead of `from code.models import Student`.
"""

from code.models import SUBJECTS, Person, Student
from code.exceptions import InvalidMarkError, StudentNotFoundError

__version__ = "1.0"
__all__ = ["Person", "Student", "SUBJECTS",
           "StudentNotFoundError", "InvalidMarkError"]
