# Mini Project — Student Result Management System

Capstone for the Python course (Day 1–16). Small console app, standard library only.

## What is in this folder

| Path | For | What it is |
|---|---|---|
| [PROBLEM_STATEMENT.md](PROBLEM_STATEMENT.md) | **Students** | The handout — features, rules, structure, expected output, marking scheme |
| [starter/](starter/) | **Students** | Skeleton with `TODO`s. `main.py`, `__init__.py` and `utils.py` are given |
| [solution/](solution/) | **Teacher** | Complete working reference |

## Size

6 small files in the package, **max 5 functions and 2 classes per file**.

| File | Contents |
|---|---|
| `code/models.py` | `Person` (ABC), `Student` |
| `code/exceptions.py` | `StudentNotFoundError`, `InvalidMarkError` |
| `code/storage.py` | `load_students`, `save_students` |
| `code/report.py` | `get_student`, `rank_list`, `class_summary` |
| `code/utils.py` | `log_action`, `ask_int`, `ask_text` |
| `main.py` | 4 menu actions + `main` |

## Run

```bash
cd solution
python main.py
```

Loads 3 sample students, so option **4** shows real output immediately.

The starter runs but errors on any option until the `TODO`s in `code/` are done —
that is the exercise.

> ⚠️ The package is named `code`, which shadows the standard-library `code`
> module. `python main.py` is fine, but Jupyter and `python -m pdb` will fail if
> started from inside these folders.

## Topic coverage

| Day | Topic | Where |
|---|---|---|
| 1–2 | Variables, types, I/O | Menu input |
| 4 | Conditions & loops | Grade bands, menu loop |
| 5 | Strings | `.strip().title()` on names |
| 6–8 | Set / tuple / dict | `SUBJECTS`, `GRADE_BANDS`, `{roll: Student}` |
| 9 | Functions | Every file, `*args`/`**kwargs` in the decorator |
| 10 | Lambda, sorted/filter/max, recursion, decorator | `report.py`, `ask_int`, `@log_action` |
| 11 | File handling | JSON load / save |
| 12 | Exceptions | 2 custom classes, `try/except/else` |
| 13 | Classes, `__str__`, `@classmethod` | `Student` |
| 14 | Inheritance & encapsulation | `Student(Person)`, private `__marks`, `@property` |
| 15 | Abstraction | `Person(ABC)` with abstract `role()` |
| 16 | Modules & packages | The `code/` package |
