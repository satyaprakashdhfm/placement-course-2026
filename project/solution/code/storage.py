"""Reading and writing the JSON database (Days 11, 12)."""

import json
from pathlib import Path

from code.models import Student

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DB_FILE = DATA_DIR / "students.json"


def load_students():
    """Read students.json and return {roll_no: Student}."""
    students = {}
    try:
        with open(DB_FILE, encoding="utf-8") as f:      # `with` closes the file
            raw = json.load(f)
    except FileNotFoundError:
        print("  (no database yet - starting empty)")
    except json.JSONDecodeError:
        print("  ! students.json is damaged - starting empty")
    else:
        for roll_no, data in raw.items():               # JSON keys are strings
            students[int(roll_no)] = Student.from_dict(int(roll_no), data)
        print(f"  Loaded {len(students)} student(s).")
    return students


def save_students(students):
    """Write every student back to students.json."""
    DATA_DIR.mkdir(exist_ok=True)
    payload = {str(roll): s.to_dict() for roll, s in students.items()}
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
