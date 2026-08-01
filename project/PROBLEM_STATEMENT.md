# Mini Project — Student Result Management System

**Course:** Python (Day 1–16)  ·  **Mode:** Individual  ·  **Time:** 3–4 hours

---

## 1. Problem Statement

Build a small **menu-driven console program** that stores the students of one
class, records their marks in three subjects, and prints a class summary.

The data must **survive after the program closes**, so it is saved in a JSON file.

Pure Python only — no GUI, no third-party libraries.

---

## 2. What the Program Must Do

| # | Option | Description |
|---|---|---|
| 1 | **Add student** | Ask for roll number and name. Reject a roll number that already exists. |
| 2 | **Add marks** | Ask for **maths, physics, chemistry**. Reject anything outside 0–100. |
| 3 | **View one student** | Show that student's marks, average and grade. |
| 4 | **Class summary** | Rank list + total students, class average, pass %, topper. |
| 0 | **Save & exit** | Write everything back to `students.json`. |

### Rules

| Average | 90+ | 75–89 | 60–74 | 40–59 | below 40 |
|---|---|---|---|---|---|
| Grade | A | B | C | D | F |

- **PASS** if the grade is not `F` (average 40 or more).
- A **name must be letters and spaces only** — reject `123`, `Anil@` and blanks.
- The program must **never crash**. Wrong input prints a message and asks again.

---

## 3. Required Folder Structure

```text
student_result_system/
├── main.py                 <- menu only (5 functions)
├── data/
│   └── students.json       <- GIVEN TO YOU with 3 students
└── code/                   <- your PACKAGE
    ├── __init__.py
    ├── models.py           <- Person (abstract) + Student
    ├── exceptions.py       <- 2 custom exceptions
    ├── storage.py          <- load / save JSON
    ├── report.py           <- rank list + summary
    └── utils.py            <- decorator + input helpers
```

**Limits:** at most **5 functions per file** and at most **2 classes per file**.
`main.py` holds **no logic** — it only shows the menu and calls the package.

> ⚠️ `code` is also a standard-library module name, so this folder shadows it
> (the Day 16 §3 trap). `python main.py` works fine, but **do not start Jupyter
> or a debugger from inside this folder** — keep any test notebook outside it.

---

## 4. Concepts You Must Use

| Concept | Where |
|---|---|
| Type conversion, f-strings | Menu input and printing |
| if / elif / loops / break | Grade bands, menu loop |
| String methods | `.strip().title()` on names |
| **Set** | `SUBJECTS` |
| **Tuple** | `GRADE_BANDS` |
| **Dictionary** | `{roll_no: Student}` and `{subject: mark}` |
| Functions, default arguments, docstrings | Every file |
| `*args` / `**kwargs` | Inside the decorator |
| **lambda + `sorted` / `filter` / `max`** | `report.py` |
| **Recursion** | `ask_int()` re-asks itself |
| **Decorator** | `@log_action` writes `data/actions.log` |
| **File handling + JSON** | `storage.py` |
| **Exceptions** | `try / except / else` + 2 custom exception classes |
| **Class, `__init__`, `__str__`** | `Student` |
| **Class variable + `@classmethod`** | `Person.count`, `Student.from_dict()` |
| **Inheritance + `super()`** | `Student(Person)` |
| **Encapsulation + `@property`** | Private `__marks`; `average` and `grade` |
| **Abstraction (`ABC`)** | `Person` with abstract `role()` |
| **Package** | The `code/` folder and its `__init__.py` |

---

## 5. Expected Output

You are given `data/students.json`. **Do not change it.** When your program is
correct, running `python main.py` and pressing `4` must print *exactly* this.

```json
{
  "101": {"name": "Rahul Verma",  "marks": {"maths": 78.0, "physics": 71.0, "chemistry": 85.0}},
  "102": {"name": "Anita Sharma", "marks": {"maths": 95.0, "physics": 89.0, "chemistry": 90.0}},
  "103": {"name": "Karan Patel",  "marks": {"maths": 38.0, "physics": 32.0, "chemistry": 44.0}}
}
```

```text
===== STUDENT RESULT MANAGEMENT SYSTEM =====
  Loaded 3 student(s).

1. Add student        3. View one student
2. Add marks          4. Class summary        0. Save & exit

Choice: 4

  ROLL  NAME               AVG  GRADE RESULT
  102   Anita Sharma     91.33  A     PASS
  101   Rahul Verma       78.0  B     PASS
  103   Karan Patel       38.0  F     FAIL

  Students 3  |  Class average 69.11  |  Pass 66.67%
  Topper: Anita Sharma
```

**Wrong input must be handled, not crash:**

```text
Choice: abc
  ! Numbers only.
Choice: 9
  ! Enter 0 to 4.

Roll number : 101
  ! That roll number already exists.

Roll number : 999
  ! No student with roll number 999

Name        : 123
  ! Letters only - no digits or symbols.

  maths     : 120
  ! Enter 0 to 100.
```

---

## 6. Suggested Order

1. **`exceptions.py`** — 2 classes. Smallest file, do it first.
2. **`models.py`** — `Person` (ABC) → `Student`. Test with a small `test.py`.
3. **`utils.py`** — the `@log_action` decorator.
4. **`storage.py`** — load, then save.
5. **`report.py`** — `get_student`, `rank_list`, `class_summary`.
6. **Break your own program** — letters, negative marks, missing roll numbers.

---

## 7. Submission & Marking

Submit a zip named `rollno_name_python_project.zip` with the folder above
(no `venv/`) and a 5-line `README.md` saying how to run it.

| Area | Marks |
|---|---|
| Folder structure, package, `__init__.py`, `if __name__ == "__main__"` | 10 |
| `Person` (ABC) + `Student`: inheritance, `@property`, private data, `__str__` | 30 |
| Data structures used correctly (set / tuple / dict) | 15 |
| Functions, lambda, `sorted` / `filter` / `max`, recursion, decorator | 20 |
| JSON save and load | 15 |
| 2 custom exceptions, program never crashes | 10 |
| **Total** | **100** |

Copied submissions get zero. You must be able to explain any line you wrote.
