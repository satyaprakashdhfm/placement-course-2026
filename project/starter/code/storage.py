"""Reading and writing the JSON database (Days 11, 12)."""

import json
from pathlib import Path

from code.models import Student

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DB_FILE = DATA_DIR / "students.json"


def load_students():
    """Read students.json and return {roll_no: Student}.

    Use the full try / except / else shape:
      try     -> open DB_FILE with `with`, then json.load
      except  -> FileNotFoundError  -> print "  (no database yet - starting empty)"
      except  -> json.JSONDecodeError -> print "  ! students.json is damaged - starting empty"
      else    -> build the Students (JSON keys are strings, so use int())
                 and print "  Loaded N student(s)."
    """
    students = {}
    # TODO
    return students


def save_students(students):
    """Write every student back to students.json."""
    # TODO: make sure DATA_DIR exists, build {str(roll): student.to_dict()},
    #       then json.dump it with indent=2 inside a `with open(...)`
    pass
