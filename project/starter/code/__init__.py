"""Student Result Management System.

This file turns the folder into a PACKAGE (Day 16).
It runs once, the first time anything from `code` is imported.

IS THIS FILE NEEDED FOR MAIN.PY TO IMPORT? No.
Even if this file were completely EMPTY, both lines in main.py would
still work - a module inside the folder is always importable:

    from code import report, storage     the modules themselves
    from code.models import Student      a name inside a module

The 2 lines below add ONE extra thing: a shortcut. They lift those
names up to the package, so a SHORT form also becomes legal:

    from code import Student             short  - only because of below
    from code.models import Student      long   - always works

main.py uses the long form everywhere, so it never needs this file to
have anything in it. We fill it in to show what a package CAN do.
"""

from code.models import SUBJECTS, Person, Student  # our main classes
from code.exceptions import InvalidMarkError, StudentNotFoundError  # our errors

__version__ = "1.0"
__all__ = ["Person", "Student", "SUBJECTS",
           "StudentNotFoundError", "InvalidMarkError"]
