"""Person and Student - abstraction, inheritance, encapsulation (Days 13-15).

WHAT THIS FILE IS
-----------------
The heart of the project. Two classes:

    Person   - ABSTRACT. Holds what every person has (a name).
               Nobody can create a Person directly.
    Student  - a real person, who also has a roll number and marks.

Do NOT rename anything. main.py, storage.py and report.py already call
these exact names.

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

    def __init__(self, name):
        # TODO 1: three lines.
        #   a) clean the name and save it:  self.name = name.strip().title()
        #      .strip() removes spaces at the ends, .title() makes "ravi kumar"
        #      into "Ravi Kumar"
        #   b) add one to the shared counter: Person.count += 1
        #      (write Person.count, NOT self.count - it belongs to the class)
        pass

    @abstractmethod
    def role(self):
        """Abstract: it has no body here. Every subclass MUST write its own."""


class Student(Person):
    """A student: a Person who also has a roll number and marks."""

    def __init__(self, roll_no, name, marks=None):
        # TODO 2: four steps.
        #   a) run the parent's __init__ so the name is handled there:
        #        super().__init__(name)
        #   b) self.roll_no = int(roll_no)
        #   c) create the PRIVATE marks dictionary, empty:
        #        self.__marks = {}
        #      Two underscores in front = private. Code outside this class
        #      cannot touch it directly.
        #   d) `marks` may be None, so use `(marks or {})`. Loop over its
        #      .items() and call self.set_mark(subject, mark) for each pair,
        #      so every mark goes through the same validation.
        pass

    def role(self):
        # TODO 3: one line - return the text "Student".
        #         This is the abstract method from Person, now filled in.
        pass

    @property
    def marks(self):
        """Read-only view of the marks.

        @property means you write `student.marks`, not `student.marks()`.
        """
        # TODO 4: return a COPY, not the real dictionary:  return dict(self.__marks)
        #         A copy means outside code cannot secretly change our marks.
        pass

    def set_mark(self, subject, mark):
        """The ONLY way a mark gets in. Validates first."""
        # TODO 5: four steps.
        #   a) try to convert:   mark = float(mark)
        #   b) if that raises (TypeError, ValueError) -> raise InvalidMarkError(mark)
        #   c) if not 0 <= mark <= 100                -> raise InvalidMarkError(mark)
        #   d) otherwise store it: self.__marks[subject.lower()] = mark
        pass

    @property
    def average(self):
        """Average of all marks, rounded to 2 decimals."""
        # TODO 6: two steps.
        #   a) GUARD CLAUSE: if there are no marks yet, return 0.0
        #      (without this you would divide by zero)
        #   b) otherwise: round(sum(...) / len(...), 2) using self.__marks.values()
        pass

    @property
    def grade(self):
        """One letter, decided by the average."""
        # TODO 7: loop over GRADE_BANDS. It is already sorted biggest first,
        #         so the FIRST band the average reaches is the right one:
        #             for cutoff, letter in GRADE_BANDS:
        #                 if self.average >= cutoff:
        #                     return letter
        #         Return "F" at the end as a safety net.
        pass

    def __str__(self):
        """What print(student) shows - one neat table row."""
        # TODO 8: two steps.
        #   a) result = "FAIL" if self.grade == "F" else "PASS"
        #   b) return this exact f-string (the numbers line the columns up):
        #        f"{self.roll_no:<6}{self.name:<16}{self.average:>6}  "
        #        f"{self.grade:<6}{result}"
        #      :<6  means pad to 6 characters on the left
        #      :>6  means pad to 6 characters on the right
        pass

    def to_dict(self):
        """Turn this object into plain data, ready for JSON."""
        # TODO 9: return {"name": self.name, "marks": self.marks}
        pass

    @classmethod
    def from_dict(cls, roll_no, data):
        """Build a Student back from that plain data.

        @classmethod receives the CLASS as `cls` instead of an object as
        `self`, so it can create one: cls(...) is the same as Student(...).
        """
        # TODO 10: return cls(roll_no, data["name"], data["marks"])
        pass
