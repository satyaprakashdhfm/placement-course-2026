"""Data models - abstraction, inheritance, encapsulation (Days 13, 14, 15).

Fill in every TODO. Do not change the function/property names - the menu in
main.py already expects them.
"""

from abc import ABC, abstractmethod

from srms.exceptions import InvalidMarkError, InvalidSubjectError

# TODO: SUBJECTS must be a SET of three subject names (lowercase)
SUBJECTS = set()

# TODO: GRADE_BANDS must be a TUPLE of (cutoff, letter) pairs, highest first
#       90 -> "A+", 80 -> "A", 70 -> "B", 60 -> "C", 50 -> "D", 0 -> "F"
GRADE_BANDS = ()

PASS_MARK = 40


class Person(ABC):
    """Abstract base class - cannot be instantiated directly."""

    total_people = 0            # class variable shared by every Person

    def __init__(self, name: str):
        # TODO: reject an empty name, clean it with .strip().title(),
        #       store it in self.name, and increase Person.total_people
        pass

    @abstractmethod
    def role(self) -> str:
        """Every subclass must say what it is."""
        pass

    def describe(self) -> str:
        # TODO: return "Name (Role)"
        pass


class Student(Person):

    def __init__(self, roll_no: int, name: str, marks: dict | None = None):
        # TODO: call super().__init__(name), store roll_no as int,
        #       create the PRIVATE dict self.__marks, then add any given marks
        pass

    def role(self) -> str:
        # TODO
        pass

    @property
    def marks(self) -> dict:
        """Read-only COPY of the private marks dict."""
        # TODO
        pass

    def set_mark(self, subject: str, mark) -> None:
        """Validate then store one subject mark.

        Raise InvalidSubjectError if the subject is not in SUBJECTS.
        Raise InvalidMarkError if the mark is not a number from 0 to 100.
        """
        # TODO
        pass

    @property
    def total(self) -> float:
        # TODO
        pass

    @property
    def average(self) -> float:
        # TODO: return 0.0 when there are no marks, else round(total/count, 2)
        pass

    @property
    def grade(self) -> str:
        # TODO: loop over GRADE_BANDS and return the first letter that fits
        pass

    @property
    def passed(self) -> bool:
        # TODO: True only if EVERY subject mark is >= PASS_MARK
        pass

    # ---- dunder methods ---------------------------------------------------
    def __str__(self) -> str:
        # TODO: e.g. "101 | Rahul Verma    | avg   78.0 | B"
        pass

    def __repr__(self) -> str:
        # TODO
        pass

    def __eq__(self, other) -> bool:
        # TODO: two students are equal when their roll numbers match
        pass

    def __hash__(self) -> int:
        return hash(self.roll_no)

    def __len__(self) -> int:
        # TODO: number of subjects recorded
        pass

    # ---- serialisation ----------------------------------------------------
    def to_dict(self) -> dict:
        # TODO: {"name": ..., "marks": ...}
        pass

    @classmethod
    def from_dict(cls, roll_no, data: dict) -> "Student":
        # TODO: build a Student from the dict produced by to_dict()
        pass


class Teacher(Person):
    """Second subclass - used to demonstrate polymorphism."""

    def __init__(self, name: str, subject: str):
        # TODO
        pass

    def role(self) -> str:
        # TODO: return "Teacher of Maths" style text
        pass
