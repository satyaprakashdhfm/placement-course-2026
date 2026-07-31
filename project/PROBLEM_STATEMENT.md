# Mini Project — Student Result Management System

**Course:** Python (Day 1–16)  ·  **Mode:** Individual  ·  **Time:** 6–8 hours

---

## 1. Problem Statement

A college needs a small console application to manage the results of one class.

The office staff must be able to add students, enter marks for three subjects,
see who topped the class, check the pass percentage, and export a report.
The data must **survive after the program is closed**, so it is stored in a file.

Build this as a **menu-driven command-line program in pure Python** — no GUI and
no third-party libraries.

---

## 2. What the Program Must Do

| # | Feature | Description |
|---|---|---|
| 1 | **Add student** | Take a roll number and name. Reject a roll number that already exists. |
| 2 | **Add / update marks** | Enter marks for **maths, physics, chemistry**. Reject anything outside 0–100. |
| 3 | **View one student** | Show all marks, total, average, grade and PASS/FAIL. |
| 4 | **Rank list** | All students sorted by average, highest first, with rank numbers. |
| 5 | **Class statistics** | Class average, pass percentage, topper, subject-wise averages, grade counts. |
| 6 | **Search by name** | Partial, case-insensitive — typing `ra` should find `Rahul` and `Karan`. |
| 7 | **Export report** | Write a `report.csv` file with one row per student. |
| 8 | **Backup** *(bonus)* | Copy the database file using a **thread**. |
| 0 | **Save & exit** | Write everything back to `students.json`. |

### Rules

- **Grade** is based on the average:

  | Average | 90+ | 80–89 | 70–79 | 60–69 | 50–59 | below 50 |
  |---|---|---|---|---|---|---|
  | Grade | A+ | A | B | C | D | F |

- **PASS** only if **every** subject is **40 or above**. One subject below 40 = FAIL.
- The program must **never crash**. Wrong input must print a clear message and ask again.

---

## 3. Required Folder Structure

Your submission **must** use exactly this layout — the marks include it.

```text
student_result_system/
├── requirements.txt
├── main.py                 <- menu loop, uses if __name__ == "__main__"
├── data/
│   └── students.json       <- your database (auto-created)
└── srms/                   <- your PACKAGE
    ├── __init__.py
    ├── models.py           <- Person (abstract), Student, Teacher
    ├── exceptions.py       <- your custom exception classes
    ├── storage.py          <- JSON load/save + CSV export
    ├── analytics.py        <- rank, topper, averages, search
    └── utils.py            <- decorator + input helpers
```

**`main.py` must contain no business logic** — it only prints menus, reads input,
and calls functions from the `srms` package.

---

## 4. Concepts You Must Use

Each one is checked while marking.

| Concept | Where to use it |
|---|---|
| **Variables, type conversion, f-strings** | Reading and printing menu input |
| **if / elif / else, loops, break** | Grade bands, menu loop |
| **String methods** | Clean names with `.strip()` / `.title()`, search with `.lower()` |
| **List** | Marks and ranked students |
| **Tuple** | `GRADE_BANDS` — configuration that must not change |
| **Set** | `SUBJECTS` — the allowed subject names |
| **Dictionary** | `{roll_no: Student}` and `{subject: mark}` |
| **Functions** | Every module; use default arguments and docstrings |
| **`*args` / `**kwargs`** | Inside the decorator |
| **lambda + `map` / `filter` / `sorted` / `reduce`** | Rank list, pass list, class average, name tags |
| **Recursion** | `ask_int()` re-asks itself on wrong input |
| **Decorator** | `@log_action` writes every action to `data/actions.log` |
| **File handling (`with`, JSON, CSV)** | `storage.py` |
| **Exceptions** | `try / except / else / finally` + **4 custom exception classes** |
| **Classes, `__init__`, dunder methods** | `Student` with `__str__`, `__repr__`, `__eq__`, `__len__` |
| **Class variable + `@classmethod`** | `total_people` counter, `Student.from_dict()` |
| **Inheritance + `super()`** | `Student(Person)`, `Teacher(Person)` |
| **Encapsulation + `@property`** | Private `__marks`; `average`, `grade`, `passed` as properties |
| **Abstraction (`ABC`)** | `Person` with an abstract `role()` |
| **Polymorphism** | One loop calling `.describe()` on both `Student` and `Teacher` |
| **Modules & packages** | The `srms/` package and its `__init__.py` |
| **Virtual environment** | Create one, and submit `requirements.txt` |
| **Threading** *(bonus)* | Background backup |

---

## 5. Expected Output

```text
====================================================
          STUDENT RESULT MANAGEMENT SYSTEM
====================================================
  Loaded 3 student(s).

1. Add student           5. Class statistics
2. Add / update marks    6. Search by name
3. View one student      7. Export report (CSV)
4. Rank list             8. Backup database (threaded)
                         0. Save & exit

Choice: 4

====================================================
                     RANK LIST
====================================================
  RANK  ROLL   NAME                  AVG  GRADE  RESULT
  --------------------------------------------------
  1     102    Anita Sharma        91.33  A+     PASS
  2     101    Rahul Verma          78.0  B      PASS
  3     103    Karan Patel         44.67  F      FAIL

Choice: 5

====================================================
                  CLASS STATISTICS
====================================================
  Students        : 3
  Class average   : 71.33
  Pass percentage : 66.67 %
  Topper          : Anita Sharma (91.33)

  Subject averages:
    Chemistry    73.0  ##############
    Maths       70.33  ##############
    Physics     70.67  ##############

  Grade distribution:
    A+   * (1)
    B    * (1)
    F    * (1)

  People in this class:
    - Meera Nair (Teacher of Maths)
    - Anita Sharma (Student)
    - Rahul Verma (Student)
    - Karan Patel (Student)
```

**Wrong input must be handled, not crash:**

```text
Choice: abc
  ! Numbers only, please.
Choice: 9
  ! Enter a number between 0 and 8.

Roll number : 101
  ! Student with roll number 101 already exists

   Maths     : 120
  ! Enter a number between 0 and 100.
```

**`data/report.csv` after Export:**

```text
roll_no,name,chemistry,maths,physics,total,average,grade,result
101,Rahul Verma,85.0,78.0,71.0,234.0,78.0,B,PASS
102,Anita Sharma,90.0,95.0,89.0,274.0,91.33,A+,PASS
103,Karan Patel,44.0,38.0,52.0,134.0,44.67,F,FAIL
```

---

## 6. How to Do It (suggested order)

1. **Set up** — make the folders, create a virtual environment, run `python main.py`.
2. **`exceptions.py`** — the four exception classes. Smallest file, do it first.
3. **`models.py`** — `Person` (ABC) → `Student`, `Teacher`. Test in a notebook before moving on.
4. **`utils.py`** — the `@log_action` decorator and the recursive `ask_int()`.
5. **`storage.py`** — load and save JSON first; add CSV export after.
6. **`analytics.py`** — rank, topper, averages, search.
7. **`main.py`** — wire the menu to the functions.
8. **Break your own program** — enter letters, negative marks, missing roll numbers. Fix every crash.
9. **Bonus** — the threaded backup.

---

## 7. Submission & Marking

**Submit** a zip named `rollno_name_python_project.zip` containing the folder above,
**without** the `venv/` folder, plus a 5-line `README.md` saying how to run it.

| Area | Marks |
|---|---|
| Correct folder structure, package, `__init__.py`, `if __name__ == "__main__"` | 10 |
| Classes: inheritance, `@property`, private data, ABC, dunder methods | 25 |
| Data structures used correctly (list / tuple / set / dict) | 15 |
| Functions, lambda, `map` / `filter` / `sorted`, recursion, decorator | 20 |
| File handling — JSON save/load + CSV export | 15 |
| Exception handling + 4 custom exceptions, program never crashes | 10 |
| Clean code: names, docstrings, no repetition | 5 |
| **Bonus** — threaded backup | +5 |
| **Total** | **100 (+5)** |

---

## 8. Rules

- Standard library only. No `pandas`, no `numpy`, no GUI.
- Copied submissions get zero. You must be able to explain any line you wrote.
- Marks are for **working, readable** code — not for extra features.
