"""Reading and writing the JSON database (Days 11, 12).

WHY THIS FILE EXISTS
--------------------
Without it, everything you type is lost when the program closes. These two
functions are the only place that touches the disk.

The file on disk looks like this:

    {
      "101": {"name": "Rahul Verma", "marks": {"maths": 78.0, ...}},
      ...
    }

In memory we want this instead:

    {101: <Student object>, ...}

So loading = read JSON  ->  build Student objects.
   Saving  = Student objects  ->  plain dicts  ->  write JSON.

Watch out: JSON keys are ALWAYS strings, so "101" must become int 101.

SELF-CHECK (run from the project folder, the one with main.py):

    python -c "from code.storage import load_students; print(load_students())"

Expected output:
      Loaded 3 student(s).
    {101: ..., 102: ..., 103: ...}
"""

import json
from pathlib import Path

from code.models import Student

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DB_FILE = DATA_DIR / "students.json"


def load_students():
    """Read students.json and return {roll_no: Student}."""
    students = {}
    # TODO 1: use the full try / except / except / else shape.
    #
    #   try:
    #       open DB_FILE with `with open(DB_FILE, encoding="utf-8") as f:`
    #       then  raw = json.load(f)      -> raw is a plain dict
    #
    #   except FileNotFoundError:         -> first ever run, no file yet
    #       print("  (no database yet - starting empty)")
    #
    #   except json.JSONDecodeError:      -> file exists but is damaged
    #       print("  ! students.json is damaged - starting empty")
    #
    #   else:                             -> runs ONLY if there was no error
    #       for roll_no, data in raw.items():
    #           students[int(roll_no)] = Student.from_dict(int(roll_no), data)
    #       print(f"  Loaded {len(students)} student(s).")
    #
    # Note: `students` starts empty above, so if the file is missing we simply
    # return an empty dictionary and the program still runs.
    return students


def save_students(students):
    """Write every student back to students.json."""
    # TODO 2: three steps.
    #   a) make sure the folder exists:  DATA_DIR.mkdir(exist_ok=True)
    #   b) turn the objects back into plain data with a dict comprehension:
    #        payload = {str(roll): s.to_dict() for roll, s in students.items()}
    #      (str(roll) because JSON keys must be strings)
    #   c) write it:
    #        with open(DB_FILE, "w", encoding="utf-8") as f:
    #            json.dump(payload, f, indent=2)
    #      "w" overwrites the whole file. indent=2 keeps it readable.
    pass
