"""Decorator and safe input (Days 9, 10).

This whole file is GIVEN to you - there is nothing to write here.

Read it anyway: `log_action` is a working decorator and `ask_int` is a
working example of RECURSION, a function that calls itself. You are expected
to be able to explain both.
"""

import functools
from datetime import datetime
from pathlib import Path

LOG_FILE = Path(__file__).resolve().parent.parent / "data" / "actions.log"


def log_action(func):
    """DECORATOR: record every call in data/actions.log.

    USED BY: main.py -> add_student() and add_marks(), written as @log_action
             on the line above each of them.

    A decorator is a function that WRAPS another function. In main.py you
    will see:

        @log_action
        def add_student(students): ...

    which means: add_student = log_action(add_student). From then on, every
    call to add_student really runs `wrapper` below, which does the extra
    work (logging) and then hands back the real result.

    CHECK IT WORKS: run the program, add a student, then open
    data/actions.log. It will contain a line like:

        [2026-01-31 20:15:00] add_student
    """

    @functools.wraps(func)          # keeps the original name in error messages
    def wrapper(*args, **kwargs):   # *args/**kwargs accept ANY arguments
        result = func(*args, **kwargs)          # run the real function first
        LOG_FILE.parent.mkdir(exist_ok=True)
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a", encoding="utf-8") as f:    # "a" appends
            f.write(f"[{stamp}] {func.__name__}\n")         # e.g. add_student
        return result

    return wrapper


def ask_int(prompt, low, high):
    """Ask for a number in a range. Re-asks itself using RECURSION.

    Given to you as a worked example. Notice the shape:
      - a BASE CASE   -> the answer is good, return it and stop
      - RECURSIVE CASES -> the answer is bad, call myself again
    """
    try:
        value = int(input(prompt).strip())
    except ValueError:                             # they typed letters
        print("  ! Numbers only.")
        return ask_int(prompt, low, high)          # recursive case
    if not low <= value <= high:                   # out of range
        print(f"  ! Enter {low} to {high}.")
        return ask_int(prompt, low, high)          # recursive case
    return value                                   # base case


def ask_text(prompt):
    """Ask for a name: letters and spaces only, never empty."""
    text = input(prompt).strip()
    if not text.replace(" ", "").isalpha():        # .isalpha() - Day 5
        print("  ! Letters only - no digits or symbols.")
        return ask_text(prompt)                    # recursive case
    return text
