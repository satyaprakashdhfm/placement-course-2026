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
    """Read the JSON database and rebuild Student objects.

    Returns a DICTIONARY {roll_no: Student} - O(1) lookup by roll number.
    """
    students = {}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except FileNotFoundError:
        print(f"  (no database yet - starting empty)")
    except json.JSONDecodeError as e:
        print(f"  ! {DB_FILE.name} is corrupted ({e}) - starting empty")
    else:
        # JSON keys are always strings, so convert back to int
        for roll_no, data in raw.items():
            students[int(roll_no)] = Student.from_dict(int(roll_no), data)
        print(f"  Loaded {len(students)} student(s).")
    finally:
        DATA_DIR.mkdir(exist_ok=True)
    return students


@log_action
def save_students(students: dict) -> None:
    """Write every student back to the JSON file."""
    DATA_DIR.mkdir(exist_ok=True)
    payload = {str(roll): s.to_dict() for roll, s in students.items()}
    with open(DB_FILE, "w", encoding="utf-8") as f:          # `with` = auto close
        json.dump(payload, f, indent=2)


@log_action
def export_csv(students: dict) -> Path:
    """Export a report card table to CSV."""
    DATA_DIR.mkdir(exist_ok=True)
    subjects = sorted(SUBJECTS)
    header = ["roll_no", "name"] + subjects + ["total", "average", "grade", "result"]

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for student in sorted(students.values(), key=lambda s: s.roll_no):
            marks = student.marks
            row = [student.roll_no, student.name]
            row += [marks.get(sub, "") for sub in subjects]
            row += [student.total, student.average, student.grade,
                    "PASS" if student.passed else "FAIL"]
            writer.writerow(row)
    return CSV_FILE


# ------------------------------------------------------------------ bonus
def backup_in_background() -> threading.Thread:
    """BONUS (Day 16): copy the database in a separate thread.

    Copying a file is I/O-bound, so a thread lets the menu stay responsive
    while the copy happens.
    """

    def _copy():
        if DB_FILE.exists():
            shutil.copy(DB_FILE, BACKUP_FILE)

    thread = threading.Thread(target=_copy, name="backup")
    thread.start()
    return thread
