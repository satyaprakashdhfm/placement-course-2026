"""Saving and loading - files, JSON, CSV, exceptions (Days 11, 12)."""

import csv
import json
import shutil
import threading
from pathlib import Path

from srms.models import SUBJECTS, Student
from srms.utils import DATA_DIR, log_action

DB_FILE = DATA_DIR / "students.json"
CSV_FILE = DATA_DIR / "report.csv"
BACKUP_FILE = DATA_DIR / "students_backup.json"


@log_action
def load_students() -> dict:
    """Read data/students.json and return {roll_no: Student}.

    Use the FULL try / except / else / finally shape:
      try     -> open and json.load
      except  -> FileNotFoundError  (first run - just start empty)
      except  -> json.JSONDecodeError (corrupted file - start empty)
      else    -> build the Student objects (JSON keys are strings -> int())
      finally -> make sure the data folder exists
    """
    students = {}
    # TODO
    return students


@log_action
def save_students(students: dict) -> None:
    """Write every student to data/students.json using `with open(...)`."""
    # TODO: build {str(roll): student.to_dict()} and json.dump it with indent=2
    pass


@log_action
def export_csv(students: dict) -> Path:
    """Write data/report.csv and return its path.

    Header: roll_no, name, <one column per subject>, total, average, grade, result
    """
    # TODO: use the csv module, newline="" and sort students by roll number
    pass


# ------------------------------------------------------------------ bonus
def backup_in_background() -> threading.Thread:
    """BONUS (Day 16): copy students.json in a separate thread.

    Create the thread with threading.Thread(target=...), start it,
    and return it so the caller can .join().
    """
    # TODO
    pass
