"""Custom exceptions (Day 12).

WHY THIS FILE EXISTS
--------------------
When something goes wrong we do NOT want to print an error and continue with
broken data. We want to STOP and let the caller decide what to do. A custom
exception is just a normal class that inherits from `Exception`.

You write 2 classes here. Each one:
  1. inherits from Exception
  2. stores the bad value on `self`, so the caller can look at it
  3. calls super().__init__("a clear message") to set the message

SELF-CHECK (run from the project folder, the one with main.py):

    python -c "from code.exceptions import StudentNotFoundError as E; print(E(999))"

Expected output:
    No student with roll number 999
"""


class StudentNotFoundError(Exception):
    """Raised when a roll number is not in the students dictionary.

    RAISED BY: code/report.py -> get_student()
    CAUGHT BY: main.py -> main(), which prints "  ! <message>"
    """

    # TODO 1: write __init__(self, roll_no) that
    #           - stores the number:            self.roll_no = roll_no
    #           - builds the message:           super().__init__(f"...")
    #         The message must read exactly:
    #           No student with roll number 999
    pass


class InvalidMarkError(Exception):
    """Raised when a mark is not a number between 0 and 100.

    RAISED BY: code/models.py -> Student.set_mark()
    CAUGHT BY: main.py -> main(), which prints "  ! <message>"
    """

    # TODO 2: write __init__(self, mark) the same way.
    #         Store it as self.mark.
    #         The message must read exactly (note the quotes around the value,
    #         which you get from the !r format):
    #           Invalid mark 'abc' - must be 0 to 100
    pass
