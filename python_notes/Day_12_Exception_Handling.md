# Day 12 – Exception Handling

**Duration:** 50–60 Minutes

### Learning Outcomes
- Tell the difference between **syntax errors** and **runtime exceptions**.
- Recognise Python's **common built-in exceptions** and what triggers them.
- Handle errors gracefully with **`try` / `except` / `else` / `finally`**.
- **`raise`** exceptions yourself and use **`assert`** for sanity checks.
- Design and use your own **custom exceptions**.
- Follow professional error-handling best practices.

## 1. Errors vs Exceptions

| | **Syntax Error** | **Exception (Runtime Error)** |
|---|---|---|
| When | Before the program runs (parsing) | While the program is running |
| Cause | Invalid Python grammar | A valid statement fails on some input |
| Fixable at runtime? | ❌ You must fix the code | ✅ Can be caught and handled |
| Example | `print("hi"` (missing `)`) | `10 / 0` → `ZeroDivisionError` |

**Key Notes:**
- A **syntax error** stops the file from running at all — you edit the code to fix it.
- An **exception** happens during execution and *can be caught* so the program keeps going.
- An **unhandled** exception crashes the program and prints a **traceback**.

## 2. Why Exception Handling?

Without handling, one bad input crashes the whole program. With handling, we **fail gracefully**:
show a friendly message, use a fallback, log the problem, and keep running.

```text
Without try/except:      With try/except:
  bad input              bad input
     |                       |
   CRASH  X               caught -> friendly message -> continue
```

Typical uses: user input, file access, network calls, parsing, division — anywhere the outside
world can surprise you.

## 3. Common Built-in Exceptions (Categorized)

### Value / type problems
| Exception | Triggered when |
|---|---|
| `ValueError` | Right type, wrong value — `int("abc")` |
| `TypeError` | Wrong type — `"2" + 2` |

### Lookup problems
| Exception | Triggered when |
|---|---|
| `IndexError` | List index out of range — `[1,2][5]` |
| `KeyError` | Missing dict key — `d["missing"]` |

### Arithmetic
| Exception | Triggered when |
|---|---|
| `ZeroDivisionError` | Dividing by zero — `10 / 0` |

### Names / attributes / imports
| Exception | Triggered when |
|---|---|
| `NameError` | Using an undefined variable |
| `AttributeError` | Object has no such attribute/method |
| `ImportError` / `ModuleNotFoundError` | Import fails |

### Files / OS
| Exception | Triggered when |
|---|---|
| `FileNotFoundError` | Opening a missing file in read mode |
| `PermissionError` | No permission for the operation |

**Key Notes:** all of these inherit from the base class **`Exception`**.

```python
# Each of these lines WOULD raise the named exception (shown safely via try/except)
tests = [
    ("ValueError",        lambda: int("abc")),
    ("TypeError",         lambda: "2" + 2),
    ("IndexError",        lambda: [1, 2][5]),
    ("KeyError",          lambda: {"a": 1}["b"]),
    ("ZeroDivisionError", lambda: 10 / 0),
]
for name, fn in tests:
    try:
        fn()
    except Exception as e:
        print(f"{name:18} -> {type(e).__name__}: {e}")
```

**Output:**
```text
ValueError         -> ValueError: invalid literal for int() with base 10: 'abc'
TypeError          -> TypeError: can only concatenate str (not "int") to str
IndexError         -> IndexError: list index out of range
KeyError           -> KeyError: 'b'
ZeroDivisionError  -> ZeroDivisionError: division by zero
```

## 4. `try` / `except` — The Basics

**Syntax**
```python
try:
    # risky code that might raise
    ...
except SomeError:
    # runs only if that error occurred
    ...
```

**Flow**
```text
   try block
      |
   error? --no--> finish normally, skip except
      |
     yes --> jump to matching except --> handle --> continue
```

**Key Notes:**
- Only the code **after** the failing line is skipped; control jumps to `except`.
- If no exception occurs, the `except` block is skipped entirely.

```python
try:
    x = 10 / 0            # raises ZeroDivisionError
    print("this line is skipped")
except ZeroDivisionError:
    print("Cannot divide by zero!")

print("program continues normally")
```

**Output:**
```text
Cannot divide by zero!
program continues normally
```

## 5. Catch *Specific* Exceptions

Always catch the **narrowest** exception you expect. A bare `except:` hides bugs and makes
debugging painful.

```text
GOOD: except ValueError:        # precise
BAD : except:                   # swallows EVERYTHING, even typos
```

```python
def parse_int(text):
    try:
        return int(text)
    except ValueError:
        return f"'{text}' is not a valid integer"

print(parse_int("42"))
print(parse_int("hello"))
```

**Output:**
```text
42
'hello' is not a valid integer
```

## 6. Multiple `except` Blocks

A single `try` can have several `except` blocks. Python checks them **top-to-bottom** and runs
the **first** one that matches.

```python
def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: division by zero"
    except TypeError:
        return "Error: both arguments must be numbers"

print(divide(10, 2))
print(divide(10, 0))
print(divide(10, "x"))
```

**Output:**
```text
5.0
Error: division by zero
Error: both arguments must be numbers
```

## 7. Catching Multiple Exceptions Together

If several errors should be handled the **same way**, group them in a **tuple**.

```python
def to_number(x):
    try:
        return float(x)
    except (ValueError, TypeError) as e:      # one handler, two error types
        return f"conversion failed: {type(e).__name__}"

print(to_number("3.14"))
print(to_number("abc"))
print(to_number(None))
```

**Output:**
```text
3.14
conversion failed: ValueError
conversion failed: TypeError
```

## 8. The Exception Object (`as e`)

Use `as e` to capture the exception object. It carries the error **message** and **type**, which
are invaluable for logging and debugging.

**Key Notes:**
- `type(e).__name__` → the exception's class name.
- `str(e)` → the human-readable message.
- `e.args` → the tuple of arguments passed to the exception.

```python
try:
    numbers = [1, 2, 3]
    print(numbers[10])
except IndexError as e:
    print("Type   :", type(e).__name__)
    print("Message:", e)
    print("Args   :", e.args)
```

**Output:**
```text
Type   : IndexError
Message: list index out of range
Args   : ('list index out of range',)
```

## 9. The `else` Clause

`else` runs **only if the `try` block did NOT raise**. It keeps the "success path" separate from
the risky line.

```text
try  -> risky code
except -> runs on failure
else -> runs on success (no exception)
```

```python
def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("cannot divide by zero")
    else:
        print("success! result =", result)   # only when no error

safe_divide(10, 2)
safe_divide(10, 0)
```

**Output:**
```text
success! result = 5.0
cannot divide by zero
```

## 10. The `finally` Clause

`finally` **always** runs — whether or not an exception occurred, and even if one is re-raised.
It is used for **cleanup** (closing files, releasing resources).

```python
def read_config():
    try:
        print("opening resource...")
        raise ValueError("bad config value")
    except ValueError as e:
        print("handled:", e)
    finally:
        print("cleanup runs no matter what")   # always executes

read_config()
```

**Output:**
```text
opening resource...
handled: bad config value
cleanup runs no matter what
```

## 11. Full Flow: `try` / `except` / `else` / `finally`

```text
        +-------------------------------+
        |            try                |
        +-------------------------------+
           |                     |
     no exception            exception
           |                     |
        +------+           +-----------+
        | else |           |  except   |
        +------+           +-----------+
           |                     |
           +----------+----------+
                      |
                 +---------+
                 | finally |   <-- ALWAYS runs
                 +---------+
```

**Order of execution:** `try` → (`except` on error **or** `else` on success) → `finally`.

```python
def demo(x):
    try:
        print("try   :", 100 / x)
    except ZeroDivisionError:
        print("except: divided by zero")
    else:
        print("else  : no error occurred")
    finally:
        print("finally: done\n")

demo(5)   # success path -> try, else, finally
demo(0)   # error path   -> try, except, finally
```

**Output:**
```text
try   : 20.0
else  : no error occurred
finally: done

except: divided by zero
finally: done
```

## 12. Nested `try` Blocks

A `try` can live inside another. The inner one gets the first chance to handle an error; if it
can't, the error propagates outward to the enclosing `try`.

```python
def process(data, index):
    try:
        value = data[index]          # may raise IndexError
        try:
            return 100 / value       # may raise ZeroDivisionError
        except ZeroDivisionError:
            return "inner: value was zero"
    except IndexError:
        return "outer: index out of range"

print(process([10, 0, 5], 0))   # 10.0
print(process([10, 0, 5], 1))   # inner handler
print(process([10, 0, 5], 9))   # outer handler
```

**Output:**
```text
10.0
inner: value was zero
outer: index out of range
```

## 13. Raising Exceptions Yourself — `raise`

Use `raise` to signal an error **on purpose** — e.g. when an argument is invalid. This is how you
enforce rules in your own functions.

**Syntax**
```python
raise ExceptionType("message")
```

```python
def set_age(age):
    if not isinstance(age, int):
        raise TypeError("age must be an integer")
    if age < 0:
        raise ValueError("age cannot be negative")
    return f"age set to {age}"

# Caught here so the notebook runs cleanly
for test in [25, -5, "old"]:
    try:
        print(set_age(test))
    except (TypeError, ValueError) as e:
        print(f"rejected: {type(e).__name__}: {e}")
```

**Output:**
```text
age set to 25
rejected: ValueError: age cannot be negative
rejected: TypeError: age must be an integer
```

## 14. Re-raising an Exception

Sometimes you want to **log** an error but still let it propagate (or convert it into a different
error). A bare `raise` inside an `except` re-throws the **same** exception.

```python
def load(value):
    try:
        return int(value)
    except ValueError:
        print("logging the problem before re-raising...")
        raise                       # re-raise the SAME ValueError

# Re-raised error is caught by the outer handler
try:
    load("oops")
except ValueError as e:
    print("outer caught:", e)
```

**Output:**
```text
logging the problem before re-raising...
outer caught: invalid literal for int() with base 10: 'oops'
```

## 15. The `assert` Statement

`assert` checks a condition that **should** be true; if it's false it raises `AssertionError`.
Great for catching programming bugs and validating assumptions during development.

**Syntax**
```python
assert condition, "message if it fails"
```

**Key Notes:**
- Use assertions for internal sanity checks, **not** for validating user input (use `raise`).
- Assertions can be disabled globally with the `python -O` flag, so never rely on them for
  security-critical checks.

```python
def average(numbers):
    assert len(numbers) > 0, "list must not be empty"
    return sum(numbers) / len(numbers)

print(average([10, 20, 30]))

# A failing assert, caught so the notebook stays clean
try:
    average([])
except AssertionError as e:
    print("AssertionError:", e)
```

**Output:**
```text
20.0
AssertionError: list must not be empty
```

## 16. Custom Exceptions

For domain-specific errors, define your **own** exception by subclassing `Exception`. This makes
error handling readable (`except InsufficientFundsError`) and lets callers catch *exactly* your
error.

**Syntax**
```python
class MyError(Exception):
    pass
```

**Key Notes:**
- Always inherit from `Exception` (or a subclass), never from `BaseException` directly.
- Naming convention: end the class name with **`Error`**.

```python
# A simple custom exception
class InvalidAgeError(Exception):
    pass

def register(age):
    if age < 18:
        raise InvalidAgeError(f"age {age} is below the minimum of 18")
    return "registered"

for a in [25, 15]:
    try:
        print(register(a))
    except InvalidAgeError as e:
        print("InvalidAgeError:", e)
```

**Output:**
```text
registered
InvalidAgeError: age 15 is below the minimum of 18
```

## 17. Custom Exceptions With Extra Data

A custom exception can carry **attributes** so the handler has all the context it needs. Override
`__init__` and call `super().__init__()` with a message.

```python
class InsufficientFundsError(Exception):
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        self.shortfall = amount - balance
        super().__init__(
            f"cannot withdraw {amount}: balance is only {balance}"
        )

def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFundsError(balance, amount)
    return balance - amount

try:
    withdraw(500, 800)
except InsufficientFundsError as e:
    print("message  :", e)
    print("shortfall:", e.shortfall)   # extra data from the exception object
```

**Output:**
```text
message  : cannot withdraw 800: balance is only 500
shortfall: 300
```

## 18. The Exception Hierarchy

All exceptions form a class tree. Catching a **parent** also catches its **children**.

```text
BaseException
 +-- SystemExit, KeyboardInterrupt, GeneratorExit   (do NOT catch these casually)
 +-- Exception                 <-- catch THIS family in normal code
      +-- ArithmeticError
      |    +-- ZeroDivisionError
      +-- LookupError
      |    +-- IndexError
      |    +-- KeyError
      +-- ValueError
      +-- TypeError
      +-- OSError
           +-- FileNotFoundError
           +-- PermissionError
```

**Key Notes:**
- `except Exception:` catches almost everything you normally care about.
- Because `ZeroDivisionError` is an `ArithmeticError`, `except ArithmeticError` catches it too.

```python
# Catching a parent class also catches the child
try:
    result = 10 / 0
except ArithmeticError as e:          # parent of ZeroDivisionError
    print("caught via parent class:", type(e).__name__)

# LookupError is the parent of both IndexError and KeyError
for action in [lambda: [1, 2][9], lambda: {"a": 1}["z"]]:
    try:
        action()
    except LookupError as e:
        print("LookupError caught:", type(e).__name__)
```

**Output:**
```text
caught via parent class: ZeroDivisionError
LookupError caught: IndexError
LookupError caught: KeyError
```

## 19. Best Practices

- **Catch specific exceptions**, not bare `except:` — don't hide bugs.
- **Keep the `try` block small** — wrap only the line that can fail.
- **Never swallow silently** (`except: pass`) — at least log it.
- Use **`finally`** (or `with`) for cleanup so resources are always released.
- Use **`raise`** for invalid input in your functions; **`assert`** only for internal checks.
- Prefer **custom exceptions** for domain errors so callers can catch precisely.
- Add a **helpful message** to every exception you raise.

## 20. Common Mistakes

**1. Bare `except` hides everything**
```python
# WRONG - even a typo'd variable name is silently swallowed
try:
    risky()
except:
    pass
# RIGHT
try:
    risky()
except ValueError as e:
    log(e)
```

**2. `try` block too large** — wrap only the risky line so you know *what* failed.

**3. Catching a parent before a child** — a broad `except Exception` placed *above* a specific
handler means the specific one never runs. Order handlers **specific → general**.

**4. Using exceptions for normal control flow** — don't `try/except` where a simple `if` works.

**5. Losing the original error** — re-raise with a bare `raise`, or use
`raise NewError(...) from e` to keep the chain.

```python
# Correct ordering: specific handler first, general last
def handle(x):
    try:
        return 10 / int(x)
    except ValueError:                 # specific
        return "not a number"
    except ZeroDivisionError:          # specific
        return "cannot divide by zero"
    except Exception:                  # general fallback LAST
        return "unexpected error"

print(handle("2"))
print(handle("abc"))
print(handle("0"))
```

**Output:**
```text
5.0
not a number
cannot divide by zero
```

## 21. Mini Practical Examples

```python
# 1) Safe division helper
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None

print(safe_divide(10, 2))
print(safe_divide(10, 0))
```

**Output:**
```text
5.0
None
```

```python
# 2) Safe dictionary access with a fallback
student = {"name": "Alice", "marks": 95}
def get_field(d, key):
    try:
        return d[key]
    except KeyError:
        return f"'{key}' not found"

print(get_field(student, "name"))
print(get_field(student, "age"))
```

**Output:**
```text
Alice
'age' not found
```

```python
# 3) Retry parsing a list of inputs, collecting only the valid numbers
raw = ["10", "abc", "20", "", "30x", "40"]
valid = []
for item in raw:
    try:
        valid.append(int(item))
    except ValueError:
        print(f"skipping invalid input: {item!r}")
print("valid numbers:", valid)
```

**Output:**
```text
skipping invalid input: 'abc'
skipping invalid input: ''
skipping invalid input: '30x'
valid numbers: [10, 20, 40]
```

```python
# 4) Custom exception in a mini validation function
class PasswordTooShortError(Exception):
    pass

def set_password(pw):
    if len(pw) < 8:
        raise PasswordTooShortError("password must be at least 8 characters")
    return "password accepted"

for pw in ["secret", "supersecret"]:
    try:
        print(set_password(pw))
    except PasswordTooShortError as e:
        print("rejected:", e)
```

**Output:**
```text
rejected: password must be at least 8 characters
password accepted
```

## 22. Summary

- **Syntax errors** stop compilation; **exceptions** happen at runtime and *can be handled*.
- Wrap risky code in **`try`**; handle failures in **`except`** (specific first, general last).
- **`else`** runs on success, **`finally`** always runs (cleanup).
- Capture details with **`as e`** (`type(e).__name__`, `str(e)`, `e.args`).
- **`raise`** signals errors deliberately; **`assert`** checks internal assumptions.
- Define **custom exceptions** (subclass `Exception`) for clear, domain-specific error handling.
- Catching a **parent** exception also catches its **children**.

## 23. Practice Questions

1. Write a program that asks for two numbers and divides them, handling `ZeroDivisionError`.
2. Convert a list of strings to integers, skipping the ones that fail with `ValueError`.
3. Access a dictionary key safely and return a default when the key is missing.
4. Open a file that may not exist and handle `FileNotFoundError` gracefully.
5. Write a function that uses `else` and `finally` to report success and always print "done".
6. Raise a `ValueError` if a function receives a negative number.
7. Create a custom exception `NegativeNumberError` and use it in a square-root function.
8. Create a custom exception that stores extra data (e.g. the invalid value) as an attribute.
9. Demonstrate that catching `Exception` also catches `ZeroDivisionError`.
10. Rewrite a bare `except:` into properly ordered specific handlers.
