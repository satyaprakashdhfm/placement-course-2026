"""Person and Student - abstraction, inheritance, encapsulation (Days 13-15)."""

from abc import ABC, abstractmethod

from code.exceptions import InvalidMarkError

SUBJECTS = {"maths", "physics", "chemistry"}       # SET - unique subject names

GRADE_BANDS = (                                     # TUPLE - fixed config
    (90, "A"), (75, "B"), (60, "C"), (40, "D"), (0, "F"),
)


class Person(ABC):
    """Abstract base class - cannot be created directly."""

    count = 0                                       # class variable

    def __init__(self, name):
        self.name = name.strip().title()            # string methods
        Person.count += 1

    @abstractmethod
    def role(self):
        """Every subclass must say what it is."""


class Student(Person):
    """One student and their marks."""

    def __init__(self, roll_no, name, marks=None):
        super().__init__(name)                      # run the parent __init__
        self.roll_no = int(roll_no)
        self.__marks = {}                           # PRIVATE dict
        for subject, mark in (marks or {}).items():
            self.set_mark(subject, mark)

    def role(self):
        return "Student"

    @property
    def marks(self):
        """Read-only copy of the private marks."""
        return dict(self.__marks)

    def set_mark(self, subject, mark):
        """Validate, then store one subject mark."""
        try:
            mark = float(mark)
        except (TypeError, ValueError):
            raise InvalidMarkError(mark)
        if not 0 <= mark <= 100:
            raise InvalidMarkError(mark)
        self.__marks[subject.lower()] = mark

    @property
    def average(self):
        if not self.__marks:                        # guard clause
            return 0.0
        return round(sum(self.__marks.values()) / len(self.__marks), 2)

    @property
    def grade(self):
        for cutoff, letter in GRADE_BANDS:          # loop over the tuple
            if self.average >= cutoff:
                return letter
        return "F"

    def __str__(self):
        result = "FAIL" if self.grade == "F" else "PASS"
        return (f"{self.roll_no:<6}{self.name:<16}{self.average:>6}  "
                f"{self.grade:<6}{result}")

    def to_dict(self):
        return {"name": self.name, "marks": self.marks}

    @classmethod
    def from_dict(cls, roll_no, data):
        """Alternative constructor (@classmethod)."""
        return cls(roll_no, data["name"], data["marks"])
