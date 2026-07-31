"""Helpers - decorators and safe input (Days 9, 10, 12)."""

import functools
from datetime import datetime
from pathlib import Path

# Path to the project root (the folder that holds main.py)
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOG_FILE = DATA_DIR / "actions.log"


def log_action(func):
    """DECORATOR: record every call to the wrapped function in a log file."""

    @functools.wraps(func)                      # keeps the original name/docstring
    def wrapper(*args, **kwargs):               # *args / **kwargs (Day 9)
        result = func(*args, **kwargs)
        DATA_DIR.mkdir(exist_ok=True)
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{stamp}] {func.__name__}\n")
        return result

    return wrapper


def ask_int(prompt: str, low: int, high: int) -> int:
    """Ask for a whole number in a range.

    Uses RECURSION (Day 10): if the answer is wrong, the function calls
    itself again instead of using a while loop.
    """
    try:
        value = int(input(prompt).strip())
    except ValueError:
        print("  ! Numbers only, please.")
        return ask_int(prompt, low, high)        # recursive case

    if not low <= value <= high:
        print(f"  ! Enter a number between {low} and {high}.")
        return ask_int(prompt, low, high)        # recursive case

    return value                                 # base case


def ask_text(prompt: str) -> str:
    """Ask for non-empty text."""
    text = input(prompt).strip()
    if not text:
        print("  ! This cannot be empty.")
        return ask_text(prompt)
    return text


def banner(title: str, width: int = 52) -> None:
    """Print a centred heading (string methods, Day 5)."""
    print("\n" + "=" * width)
    print(title.upper().center(width))
    print("=" * width)
