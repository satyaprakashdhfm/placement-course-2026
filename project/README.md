# Mini Project — Student Result Management System

Capstone for the Python course (Day 1–16). Console app, standard library only.

## What is in this folder

| Path | Who it is for | What it is |
|---|---|---|
| [PROBLEM_STATEMENT.md](PROBLEM_STATEMENT.md) | **Students** | The handout — features, rules, folder structure, expected output, marking scheme |
| [starter/](starter/) | **Students** | Skeleton with every function signature and `TODO` comments. `main.py` is given complete |
| [solution/](solution/) | **Teacher** | Complete working reference implementation |

## Run the reference solution

```bash
cd solution
python main.py
```

It loads three sample students from `data/students.json`, so options 4 and 5
show real output immediately.

## Run the starter

```bash
cd starter
python main.py
```

The menu appears, but any option raises an error until the `TODO`s in `srms/`
are filled in — that is the exercise. The first one students hit is
`AttributeError: 'Student' object has no attribute 'name'`, which points at the
unfinished `Person.__init__`.

## Topic coverage

| Day | Topic | Where it appears |
|---|---|---|
| 1–2 | Variables, types, I/O, venv | Menu input, `requirements.txt` |
| 4 | Conditions & loops | Grade bands, menu loop |
| 5 | Strings | Name cleaning, partial search |
| 6–8 | List / tuple / set / dict | Ranked list, `GRADE_BANDS`, `SUBJECTS`, `{roll: Student}` |
| 9 | Functions | Every module, `*args`/`**kwargs` in the decorator |
| 10 | Lambda, map/filter/sorted/reduce, recursion, decorator | `analytics.py`, `ask_int()`, `@log_action` |
| 11 | File handling | JSON database, CSV export |
| 12 | Exceptions | 4 custom classes, full `try/except/else/finally` |
| 13 | Classes & dunder methods | `Student.__str__`, `__eq__`, `__len__`, `from_dict` |
| 14 | Inheritance & encapsulation | `Student(Person)`, private `__marks`, `@property` |
| 15 | Polymorphism & abstraction | `Person(ABC)`, one loop over `Student` + `Teacher` |
| 16 | Modules, packages, threading | The `srms/` package, threaded backup |
