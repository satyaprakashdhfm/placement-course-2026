"""Decorator and safe input (Days 9, 10)."""

import functools
from datetime import datetime
from pathlib import Path

LOG_FILE = Path(__file__).resolve().parent.parent / "data" / "actions.log"


def log_action(func):
    """DECORATOR: record every call in data/actions.log."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):                  # *args / **kwargs
        result = func(*args, **kwargs)
        # TODO: make sure the data folder exists, then APPEND one line
        #       to LOG_FILE:  "[2026-01-31 20:15:00] add_student"
        #       (use datetime.now().strftime(...) and func.__name__)
        return result

    return wrapper


def ask_int(prompt, low, high):
    """Ask for a number in a range. Re-asks itself using RECURSION."""
    try:
        value = int(input(prompt).strip())
    except ValueError:
        print("  ! Numbers only.")
        return ask_int(prompt, low, high)          # recursive case
    if not low <= value <= high:
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
