# Mini Project — Student Result Management System

**Course:** Python (Day 1–16)  ·  **Mode:** Individual  ·  **Time:** 3–4 hours

---

## 1. What You Are Building

A small **menu-driven console program** that stores the students of one class,
records their marks in three subjects, and prints a class summary. The data is
saved in a JSON file, so it **survives after the program closes**.

Pure Python — no GUI, no `pip install` of anything.

You are given a **starter folder**. `main.py`, `__init__.py` and `utils.py`
are already written. Your job is the 17 `TODO`s in the other four files.

---

## 2. The Menu

| # | Option | What it does |
|---|---|---|
| 1 | **Add student** | Ask roll number + name. Reject a roll number that already exists. |
| 2 | **Add marks** | Ask marks for maths, physics, chemistry. |
| 3 | **View one student** | Show that student's marks, average and grade. |
| 4 | **Class summary** | Rank list + student count, class average, pass %, topper. |
| 0 | **Save & exit** | Write everything back to `students.json`. |

### Rules

| Average | 90+ | 75–89 | 60–74 | 40–59 | below 40 |
|---|---|---|---|---|---|
| **Grade** | A | B | C | D | F |

- **PASS** if the grade is not `F` (average 40 or more).
- A **mark** must be a number **0 to 100**.
- A **name** must be **letters and spaces only** — reject `123`, `Anil@`, blanks.
- The program must **never crash**. Bad input prints a message and asks again.

---

## 3. The Files

```text
starter/
├── main.py                 <- GIVEN. Do not change it.
├── data/
│   └── students.json       <- GIVEN. 3 students. Do not change it.
└── code/                   <- the package you complete
    ├── __init__.py         <- GIVEN
    ├── exceptions.py       <-  2 TODOs
    ├── models.py           <- 10 TODOs   (the big one)
    ├── storage.py          <-  2 TODOs
    ├── report.py           <-  3 TODOs
    └── utils.py            <- GIVEN
```

### What each file must contain

| File | You write | Purpose |
|---|---|---|
| `exceptions.py` | `StudentNotFoundError`, `InvalidMarkError` | 2 custom exception classes |
| `models.py` | `Person` (abstract), `Student` | The 2 classes that hold the data. `SUBJECTS` and `GRADE_BANDS` are given |
| `storage.py` | `load_students()`, `save_students()` | Read and write `students.json` |
| `report.py` | `get_student()`, `rank_list()`, `class_summary()` | Answer questions about the class |
| `utils.py` | *nothing — given* | The `@log_action` decorator and the input helpers. Read it |

**Limits:** at most **5 functions** and **2 classes** per file. `main.py` holds
no logic — it only shows the menu and calls your package.

> ⚠️ The folder is named `code`, which is also a standard-library module name,
> so it **shadows** it (the Day 16 §3 trap). `python main.py` works fine, but
> **do not start Jupyter or a debugger from inside this folder.**

---

## 4. Suggested Order

Do them in this order — each file only needs the ones above it.

1. **`exceptions.py`** — 2 tiny classes. 10 minutes.
2. **`models.py`** — `Person` then `Student`. The longest file, take your time.
3. **`storage.py`** — `load_students` first, then `save_students`.
4. **`report.py`** — the 3 report functions.
5. **Run `python main.py`** and try every option.
6. **Break it on purpose** — letters where numbers go, marks of 500, roll `999`.

Every file has a **SELF-CHECK** command in its docstring at the top. Run it as
soon as you finish that file — do not move on until it prints what it should.

---

## 5. Expected Output

With the `students.json` you were given, `python main.py` then `4` must print
**exactly** this:

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
  (Person objects created this run: 3)
```

Option `3` for roll `102` must print:

```text
  Anita Sharma (Student) - roll 102
    chemistry    90.0
    maths        95.0
    physics      89.0
  Average 91.33, grade A
```

**Bad input must be handled, not crash:**

```text
Choice: abc
  ! Numbers only.
Choice: 9
  ! Enter 0 to 4.

Name        : 123
  ! Letters only - no digits or symbols.

Roll number : 101
  ! That roll number already exists.

Roll number : 999
  ! No student with roll number 999

  maths     : 120
  ! Enter 0 to 100.
```

---

## 6. Concepts Being Tested

| Concept | Where you use it |
|---|---|
| **Set** | `SUBJECTS` |
| **Tuple** | `GRADE_BANDS` |
| **Dictionary** | `{roll_no: Student}` and `{subject: mark}` |
| String methods | `.strip()`, `.title()`, `.isalpha()` on names |
| if / elif / loops / guard clauses | Grade bands, empty-class checks |
| Functions, default arguments, docstrings | Every file |
| `*args` / `**kwargs` | Inside the decorator |
| **lambda + `sorted` / `filter` / `max`** | `report.py` |
| **Recursion** | `ask_int()` and `ask_text()` — given, but you must be able to explain them |
| **Decorator** | `@log_action` — given, but you must be able to explain it |
| **File handling + JSON** | `storage.py` |
| **Exceptions** | `try / except / else` + 2 custom classes |
| **Class, `__init__`, `__str__`** | `Student` |
| **Class variable + `@classmethod`** | `Person.count`, `Student.from_dict()` |
| **Inheritance + `super()`** | `Student(Person)` |
| **Encapsulation + `@property`** | Private `__marks`; `average`, `grade` |
| **Abstraction (`ABC`)** | `Person` with abstract `role()` |
| **Package** | The `code/` folder and its `__init__.py` |

---

## 7. Submission & Marking

Submit a zip named `rollno_name_python_project.zip` containing your folder
(no `venv/`), plus a 5-line `README.md` saying how to run it.

| Area | Marks |
|---|---|
| `models.py` — `Person` (ABC) + `Student`, inheritance, `@property`, private data, `__str__` | 35 |
| `report.py` — lambda with `sorted` / `filter` / `max` | 20 |
| `storage.py` — JSON save and load | 15 |
| Data structures used correctly (set / tuple / dict) | 15 |
| `exceptions.py` + the program never crashes | 10 |
| Clean code: names, docstrings, no repetition | 5 |
| **Total** | **100** |

Copied submissions get zero. You must be able to explain any line you wrote.
