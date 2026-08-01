"""Person and Student - abstraction, inheritance, encapsulation (Days 13-15).

WHAT THIS FILE IS
-----------------
The heart of the project. Two classes:

    Person   - ABSTRACT. Holds what every person has (a name).
               Nobody can create a Person directly.
    Student  - a real person, who also has a roll number and marks.

WHO USES WHAT YOU WRITE HERE
----------------------------
Nothing here is unused - open main.py and follow along:

    Student(...)        main.py -> add_student()      creating a new student
    .name               main.py -> add_student(), view_student(), show_summary()
    .roll_no            main.py -> view_student()
    .role()             main.py -> view_student()     prints "(Student)"
    .marks              main.py -> view_student()     loops over the marks
    .set_mark()         main.py -> add_marks()
    .average, .grade    main.py -> add_marks(), view_student()
                        code/report.py -> rank_list(), class_summary()
    __str__             main.py -> show_summary()     via print(student)
    .to_dict()          code/storage.py -> save_students()
    .from_dict()        code/storage.py -> load_students()
    Person.count        main.py -> show_summary()     last line of the summary

Do NOT rename anything - all of the above already call these exact names.

SELF-CHECK (run from the project folder, the one with main.py):

    python -c "from code.models import Student; s = Student(1, 'ravi kumar', {'maths': 80, 'physics': 90, 'chemistry': 70}); print(s.average, s.grade); print(s)"

Expected output:
    80.0 B
    1     Ravi Kumar        80.0  B     PASS
"""

from abc import ABC, abstractmethod

from code.exceptions import InvalidMarkError

# GIVEN. A SET: the order does not matter and each subject appears once.
SUBJECTS = {"maths", "physics", "chemistry"}

# GIVEN. A TUPLE of (cutoff, letter) pairs, BIGGEST FIRST - a tuple because
# these rules must never change while the program runs.
GRADE_BANDS = (
    (90, "A"), (75, "B"), (60, "C"), (40, "D"), (0, "F"),
)


class Person(ABC):
    """Abstract base class. `ABC` means it cannot be created directly."""

    count = 0                   # CLASS variable - shared by every Person ever made
                                # USED BY: main.py -> show_summary(), last line

    def __init__(self, name):
        """Runs when any Person (so also any Student) is created."""
        # TODO 1: two lines.
        #   a) clean the name and save it:  self.name = name.strip().title()
        #      .strip() removes spaces at the ends, .title() turns
        #      "ravi kumar" into "Ravi Kumar"
        #   b) add one to the shared counter: Person.count += 1
        #      Write Person.count, NOT self.count - it belongs to the CLASS,
        #      so all students share one counter.
        pass

    @abstractmethod
    def role(self):
        """Abstract: no body here. Every subclass MUST write its own."""


class Student(Person):
    """A student: a Person who also has a roll number and marks."""

    def __init__(self, roll_no, name, marks=None):
        """USED BY: main.py -> add_student(), and Student.from_dict() below."""
        # TODO 2: four steps.
        #   a) run the parent's __init__ so the name is handled there:
        #        super().__init__(name)
        #   b) self.roll_no = int(roll_no)
        #   c) create the PRIVATE marks dictionary, empty:
        #        self.__marks = {}
        #      Two underscores in front = private. Code outside this class
        #      cannot reach it, so marks can only change through set_mark().
        #   d) `marks` may be None, so use `(marks or {})`. Loop over its
        #      .items() and call self.set_mark(subject, mark) for each pair,
        #      so even loaded marks go through the same validation.
        pass

    def role(self):
        """USED BY: main.py -> view_student(), which prints "(Student)"."""
        # TODO 3: one line - return the text "Student".
        #         This fills in the abstract method from Person. Without it,
        #         Python refuses to create a Student at all.
        pass

    @property
    def marks(self):
        """Read-only view of the marks.

        @property means the caller writes `student.marks` with NO brackets,
        even though this is a function. Look at main.py -> view_student():

            for subject, mark in sorted(student.marks.items()):

        USED BY: main.py -> view_student(), and to_dict() below.
        """
        # TODO 4: return a COPY, not the real dictionary:
        #           return dict(self.__marks)
        #         A copy means outside code cannot secretly change our marks.
        pass

    def set_mark(self, subject, mark):
        """The ONLY way a mark gets in. Validates first.

        USED BY: main.py -> add_marks(), and __init__ above.
        """
        # TODO 5: four steps.
        #   a) try to convert:   mark = float(mark)
        #   b) if that raises (TypeError, ValueError) -> raise InvalidMarkError(mark)
        #   c) if not 0 <= mark <= 100                -> raise InvalidMarkError(mark)
        #   d) otherwise store it: self.__marks[subject.lower()] = mark
        pass

    @property
    def average(self):
        """Average of all marks, rounded to 2 decimals.

        USED BY: main.py -> add_marks(), view_student();
                 code/report.py -> rank_list(), class_summary();
                 and .grade below.
        """
        # TODO 6: two steps.
        #   a) GUARD CLAUSE: if there are no marks yet, return 0.0
        #      (without this, a new student with no marks would crash on
        #       divide-by-zero the moment show_summary() runs)
        #   b) otherwise: round(sum(...) / len(...), 2) on self.__marks.values()
        pass

    @property
    def grade(self):
        """One letter, decided by the average.

        USED BY: main.py -> add_marks(), view_student();
                 code/report.py -> class_summary(); and __str__ below.
        """
        # TODO 7: loop over GRADE_BANDS. It is already biggest-first, so the
        #         FIRST band the average reaches is the right one:
        #             for cutoff, letter in GRADE_BANDS:
        #                 if self.average >= cutoff:
        #                     return letter
        #         Return "F" at the end as a safety net.
        pass

    def __str__(self):
        """What print(student) shows - one neat table row.

        USED BY: main.py -> show_summary(), in the line `print(f"  {student}")`.
        A dunder method: you never call __str__ yourself, print() does.
        """
        # TODO 8: two steps.
        #   a) result = "FAIL" if self.grade == "F" else "PASS"
        #   b) return this exact f-string (the widths line the columns up
        #      under the header main.py prints):
        #        f"{self.roll_no:<6}{self.name:<16}{self.average:>6}  "
        #        f"{self.grade:<6}{result}"
        #      :<6  pad to 6 characters, text on the left
        #      :>6  pad to 6 characters, text on the right
        pass

    def to_dict(self):
        """Turn this object into plain data, ready for JSON.

        USED BY: code/storage.py -> save_students().
        """
        # TODO 9: return {"name": self.name, "marks": self.marks}
        pass

    @classmethod
    def from_dict(cls, roll_no, data):
        """Build a Student back from that plain data.

        @classmethod receives the CLASS as `cls` instead of an object as
        `self`, so it can create one: cls(...) means the same as Student(...).

        USED BY: code/storage.py -> load_students().
        """
        # TODO 10: return cls(roll_no, data["name"], data["marks"])
        pass
