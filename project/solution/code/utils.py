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
        LOG_FILE.parent.mkdir(exist_ok=True)
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{stamp}] {func.__name__}\n")
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
    """Ask for text that is not empty."""
    text = input(prompt).strip()
    return text if text else ask_text(prompt)
