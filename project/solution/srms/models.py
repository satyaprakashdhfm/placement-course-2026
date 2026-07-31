"""Data models - abstraction, inheritance, encapsulation (Days 13, 14, 15)."""

from abc import ABC, abstractmethod

from srms.exceptions import InvalidMarkError, InvalidSubjectError

# ---------------------------------------------------------------- constants
# A SET: unordered, unique - perfect for "is this subject allowed?" (Day 7)
SUBJECTS = {"maths", "physics", "chemistry"}

# A TUPLE of tuples: immutable configuration that must never change (Day 7)
GRADE_BANDS = (
    (90, "A+"),
    (80, "A"),
    (70, "B"),
    (60, "C"),
    (50, "D"),
    (0, "F"),
)

PASS_MARK = 40


# ---------------------------------------------------------------- abstract base
class Person(ABC):
    """Abstract base class - cannot be created directly (Day 15)."""

    total_people = 0                      # CLASS variable, shared by all objects

    def __init__(self, name: str):
        if not name.strip():
            raise ValueError("Name cannot be empty")
        self.name = name.strip().title()  # string methods (Day 5)
        Person.total_people += 1

    @abstractmethod
    def role(self) -> str:
        """Every subclass MUST say what it is."""
        pass

    def describe(self) -> str:
        """Concrete method shared by all subclasses."""
        return f"{self.name} ({self.role()})"


# ---------------------------------------------------------------- concrete
class Student(Person):
    """One student and their marks."""

    def __init__(self, roll_no: int, name: str, marks: dict | None = None):
        super().__init__(name)                    # run the parent constructor
        self.roll_no = int(roll_no)
        self.__marks: dict[str, float] = {}       # PRIVATE - name mangled
        for subject, mark in (marks or {}).items():
            self.set_mark(subject, mark)

    # ---- polymorphism -----------------------------------------------------
    def role(self) -> str:
        return "Student"

    # ---- encapsulation ----------------------------------------------------
    @property
    def marks(self) -> dict:
        """Read-only view. Returns a COPY so nobody can edit our private dict."""
        return dict(self.__marks)

    def set_mark(self, subject: str, mark) -> None:
        """Add or update one subject mark, with validation."""
        subject = subject.strip().lower()
        if subject not in SUBJECTS:
            raise InvalidSubjectError(subject, SUBJECTS)
        try:
            mark = float(mark)
        except (TypeError, ValueError):
            raise InvalidMarkError(mark)
        if not 0 <= mark <= 100:
            raise InvalidMarkError(mark)
        self.__marks[subject] = mark

    # ---- computed properties ---------------------------------------------
    @property
    def total(self) -> float:
        return sum(self.__marks.values())

    @property
    def average(self) -> float:
        if not self.__marks:                       # guard clause (Day 9)
            return 0.0
        return round(self.total / len(self.__marks), 2)

    @property
    def grade(self) -> str:
        for cutoff, letter in GRADE_BANDS:         # loop over tuple config
            if self.average >= cutoff:
                return letter
        return "F"

    @property
    def passed(self) -> bool:
        """Passed only if EVERY subject is at or above the pass mark."""
        if not self.__marks:
            return False
        return all(m >= PASS_MARK for m in self.__marks.values())

    # ---- dunder methods (Day 13) -----------------------------------------
    def __str__(self) -> str:
        return f"{self.roll_no} | {self.name:<15} | avg {self.average:>6} | {self.grade}"

    def __repr__(self) -> str:
        return f"Student(roll_no={self.roll_no}, name={self.name!r})"

    def __eq__(self, other) -> bool:
        return isinstance(other, Student) and self.roll_no == other.roll_no

    def __hash__(self) -> int:
        return hash(self.roll_no)                  # keeps Student usable in sets

    def __len__(self) -> int:
        return len(self.__marks)                   # len(student) -> subject count

    # ---- serialisation (used by storage.py) ------------------------------
    def to_dict(self) -> dict:
        return {"name": self.name, "marks": self.marks}

    @classmethod
    def from_dict(cls, roll_no, data: dict) -> "Student":
        """Alternative constructor (Day 13 - @classmethod)."""
        return cls(roll_no, data["name"], data.get("marks", {}))


class Teacher(Person):
    """Second subclass - proves the same interface works for a different type."""

    def __init__(self, name: str, subject: str):
        super().__init__(name)
        self.subject = subject

    def role(self) -> str:
        return f"Teacher of {self.subject.title()}"
