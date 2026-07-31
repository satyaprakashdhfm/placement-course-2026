"""Helpers - decorator and safe input (Days 9, 10, 12).

This file is given to you COMPLETE, except the decorator body.
"""

import functools
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOG_FILE = DATA_DIR / "actions.log"


def log_action(func):
    """DECORATOR: append the function name + timestamp to data/actions.log."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        # TODO: make sure DATA_DIR exists, then APPEND one line to LOG_FILE:
        #       "[2026-01-31 20:15:00] function_name"
        #       (use datetime.now().strftime(...) and func.__name__)
        return result

    return wrapper


def ask_int(prompt: str, low: int, high: int) -> int:
    """Ask for a whole number in a range, using RECURSION to re-ask."""
    try:
        value = int(input(prompt).strip())
    except ValueError:
        print("  ! Numbers only, please.")
        return ask_int(prompt, low, high)

    if not low <= value <= high:
        print(f"  ! Enter a number between {low} and {high}.")
        return ask_int(prompt, low, high)

    return value


def ask_text(prompt: str) -> str:
    """Ask for non-empty text."""
    text = input(prompt).strip()
    if not text:
        print("  ! This cannot be empty.")
        return ask_text(prompt)
    return text


def banner(title: str, width: int = 52) -> None:
    print("\n" + "=" * width)
    print(title.upper().center(width))
    print("=" * width)
