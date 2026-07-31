"""Person and Student - abstraction, inheritance, encapsulation (Days 13-15).

Fill in every TODO. Do not rename anything - main.py already expects
these names.
"""

from abc import ABC, abstractmethod

from code.exceptions import InvalidMarkError

# TODO: a SET of the three subject names, all lowercase
SUBJECTS = set()

# TODO: a TUPLE of (cutoff, letter) pairs, highest first:
#       90 -> "A", 75 -> "B", 60 -> "C", 40 -> "D", 0 -> "F"
GRADE_BANDS = ()


class Person(ABC):
    """Abstract base class - cannot be created directly."""

    count = 0                                   # class variable

    def __init__(self, name):
        # TODO: clean the name with .strip().title(), store it in self.name,
        #       and add 1 to Person.count
        pass

    @abstractmethod
    def role(self):
        """Every subclass must say what it is."""


class Student(Person):

    def __init__(self, roll_no, name, marks=None):
        # TODO: call super().__init__(name), store self.roll_no as int,
        #       create the PRIVATE dict self.__marks,
        #       then loop over `marks` and call self.set_mark(...)
        pass

    def role(self):
        # TODO: return "Student"
        pass

    @property
    def marks(self):
        # TODO: return a COPY of the private dict
        pass

    def set_mark(self, subject, mark):
        # TODO: convert mark with float(); if that fails, or it is not
        #       between 0 and 100, raise InvalidMarkError(mark).
        #       Otherwise store it under subject.lower()
        pass

    @property
    def average(self):
        # TODO: 0.0 when there are no marks, else round(sum/count, 2)
        pass

    @property
    def grade(self):
        # TODO: loop over GRADE_BANDS, return the first letter that fits
        pass

    def __str__(self):
        # TODO: "102   Anita Sharma     91.33  A     PASS"
        #       Use f"{self.roll_no:<6}{self.name:<16}{self.average:>6}  "
        #           f"{self.grade:<6}{result}"   where result is PASS or FAIL
        pass

    def to_dict(self):
        # TODO: {"name": ..., "marks": ...}
        pass

    @classmethod
    def from_dict(cls, roll_no, data):
        # TODO: build a Student from the dict made by to_dict()
        pass
