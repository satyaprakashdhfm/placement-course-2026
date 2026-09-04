# Day 9 – Functions (Fundamentals)

**Duration:** 50–60 Minutes

### Learning Outcomes
- Understand what a function is and why functions matter in real programs.
- Write functions using `def`, parameters, arguments and the `return` statement.
- Distinguish positional, keyword, default, `*args` and `**kwargs` arguments.
- Understand variable scope (local, global) and the `global` keyword.
- Write docstrings and follow professional function best practices.
- Solve small DSA-style problems by breaking them into reusable functions.

## 1. Python Data Structure Revision

Before starting functions, revise the core Python data structures. Functions will
constantly accept these as arguments and return them as results, so knowing their
properties (ordering, mutability, hashability) is essential.

| Feature      | List | Tuple | Set | Dictionary          | String |
|--------------|:----:|:-----:|:---:|:-------------------:|:------:|
| Indexing     | ✅   | ✅    | ❌  | ✅ (by key)         | ✅     |
| Ordered      | ✅   | ✅    | ❌  | ✅ (Python 3.7+)    | ✅     |
| Mutable      | ✅   | ❌    | ✅  | ✅                  | ❌     |
| Hashable     | ❌   | ✅\* | ❌  | ❌                  | ✅     |
| Duplicates   | ✅   | ✅    | ❌  | keys ❌ / values ✅ | ✅     |

\* A tuple is hashable **only if** every element inside it is also hashable.

**Key Notes:**
- *Mutable* = can be changed in place after creation (list, set, dict).
- *Immutable* = cannot be changed after creation (tuple, string, int).
- *Hashable* objects can be used as dictionary keys or set elements.
- Ordering means items keep the position/insertion order you gave them.

```python
# Quick proof of mutability and hashability

nums = [1, 2, 3]        # list  -> mutable
nums[0] = 99            # allowed
print("List after change:", nums)

point = (10, 20)        # tuple -> immutable
# point[0] = 99         # would raise TypeError, so we leave it commented

# Hashable objects can be dictionary keys / set elements
seen = {point, "hi", 5} # tuple, string, int are all hashable
print("Set of hashables:", seen)
```

**Output:**
```text
List after change: [99, 2, 3]
Set of hashables: {'hi', 5, (10, 20)}
```

## 2. What is a Function?

A **function** is a named, reusable block of code that performs one specific task.
You *define* it once and then *call* (use) it as many times as you like.

### Real-Life Analogy
Think of a **coffee machine**. You press one button (the function *call*), the machine
does all the internal work (the function *body*), and you receive a cup of coffee
(the *return value*). You do not care *how* it works internally — you only use it.

- **Input** → beans + water (the *arguments*)
- **Process** → brewing (the function *body*)
- **Output** → cup of coffee (the *return value*)

**Key Notes:**
- A function groups instructions under a single name.
- "Define once, use many times" is the whole point of a function.
- Functions hide complexity behind a simple, meaningful name.

## 3. Why Functions? (Advantages)

Functions are the foundation of clean, professional code.

- **Reusability** – write the logic once, reuse it everywhere.
- **Readability** – a good function name explains *what* the code does.
- **Maintenance** – fix a bug in one place instead of many copies.
- **Modularity** – break a big problem into small, independent pieces.
- **Testing** – small functions are easy to test in isolation.

The demo below shows the *problem* (repeated code) and the *solution* (a function).

```python
# BEFORE using a function: the same logic is copy-pasted (hard to maintain)

# area of rectangle 1
length1, breadth1 = 10, 5
print("Area 1:", length1 * breadth1)

# area of rectangle 2
length2, breadth2 = 8, 3
print("Area 2:", length2 * breadth2)

# area of rectangle 3
length3, breadth3 = 7, 7
print("Area 3:", length3 * breadth3)
```

**Output:**
```text
Area 1: 50
Area 2: 24
Area 3: 49
```

```python
# AFTER using a function: one definition, reused three times (clean + reusable)

def area(length, breadth):
    return length * breadth        # single source of truth for the formula

print("Area 1:", area(10, 5))
print("Area 2:", area(8, 3))
print("Area 3:", area(7, 7))
```

**Output:**
```text
Area 1: 50
Area 2: 24
Area 3: 49
```

## 4. Function Execution Flow

When a function is called, Python pauses the current line, jumps into the function,
runs its body, then returns to exactly where it left off.

```text
   CALLER                         FUNCTION
 -----------                    ------------
 result = area(10, 5)  ──call──▶  def area(length, breadth):
      │                               body runs...
      │                               return length * breadth
      │                                     │
      ▼                                     │
 result now = 50   ◀────────return 50───────┘
      │
      ▼
 continue with next line
```

**Key Notes:**
- The call *transfers control* into the function.
- `return` sends a value back **and** exits the function immediately.
- After returning, execution continues at the line that made the call.

## 5. Function Syntax

A function definition has five parts: the `def` keyword, a name, parentheses with
optional parameters, a colon, and an indented body that may `return` a value.

**Syntax:**
```python
def function_name(parameter1, parameter2):
    """Optional docstring describing the function."""
    # function body (indented)
    return value          # optional
```

**Key Notes:**
- The body **must** be indented (4 spaces is standard).
- Parentheses are required even if there are no parameters.
- A function with no `return` gives back `None`.

```python
# Minimal function: no parameters, no return value

def greet():
    print("Welcome to Python Functions")   # this is the body

greet()   # calling the function actually runs the body
```

**Output:**
```text
Welcome to Python Functions
```

## 6. Function Anatomy (Labelled)

The diagram below labels every part of a function so the vocabulary is clear.

```text
def   greet   (name)   :
 │      │        │     │
 │      │        │     └── colon ends the header line
 │      │        └──────── parameter(s) inside parentheses
 │      └───────────────── function name (snake_case)
 └──────────────────────── the 'def' keyword

    "Hello " + name          <- function body (indented)
    return message           <- return statement (optional)
```

**Key Notes:**
- **Header** = `def` + name + parentheses + colon.
- **Body** = the indented block below the header.
- **Signature** = the name plus its parameter list.

```python
# Every labelled part in one function
def greet(name):                 # header: def + name + (parameter) + colon
    message = "Hello " + name    # body line 1
    return message               # return statement

print(greet("Ravi"))             # call with an argument -> Hello Ravi
```

**Output:**
```text
Hello Ravi
```

## 7. Function Naming Rules

Function names follow the same rules as variable names. The Python convention
(PEP 8) is **snake_case**: lowercase words joined by underscores.

| Rule                                   | Valid ✅            | Invalid ❌         |
|----------------------------------------|--------------------|--------------------|
| Use lowercase snake_case               | `calculate_area`   | `CalculateArea`    |
| May contain letters, digits, `_`       | `sum_of_2`         | `sum-of-2`         |
| Must **not** start with a digit        | `student_marks`    | `2nd_marks`        |
| No spaces allowed                       | `get_total`        | `get total`        |
| Cannot be a Python keyword             | `my_class`         | `class`            |
| Should be descriptive (a verb)         | `count_vowels`     | `x` / `func1`      |

**Key Notes:**
- Prefer verbs/verb-phrases: `send_email`, `find_max`, `is_prime`.
- Avoid shadowing built-ins (do not name your function `list`, `sum`, `len`).
- A reader should guess what a function does *from its name alone*.

```python
# Valid, descriptive function names in action

def calculate_area(length, breadth):
    return length * breadth

def is_positive(number):
    return number > 0

print(calculate_area(4, 6))   # 24
print(is_positive(-3))        # False
```

**Output:**
```text
24
False
```

## 8. Built-in vs User-defined Functions

Python ships with many ready-made **built-in functions**. You can also create your
own **user-defined functions** for logic that Python does not provide.

| Aspect        | Built-in Functions            | User-defined Functions       |
|---------------|-------------------------------|------------------------------|
| Who wrote it  | Python itself                 | You (the programmer)         |
| Availability  | Always ready to use           | Only after you `def` it      |
| Examples      | `len()`, `sum()`, `max()`     | `square()`, `is_prime()`     |
| Customisable  | No                            | Yes, fully                   |

**Key Notes:**
- Do not reinvent what Python already gives you (`sum`, `max`, `sorted`).
- Write your own functions for domain-specific / repeated logic.

```python
# Built-in functions
data = [3, 8, 1, 9, 4]
print("Length :", len(data))   # count of items
print("Sum    :", sum(data))   # total
print("Max    :", max(data))   # largest
print("Min    :", min(data))   # smallest

# User-defined function
def square(n):
    return n * n

print("Square :", square(5))   # 25
```

**Output:**
```text
Length : 5
Sum    : 25
Max    : 9
Min    : 1
Square : 25
```

## 9. Calling (Invoking) Functions

Defining a function does **not** run it. You must *call* it using its name followed
by parentheses. You can define once and call as many times as you like.

**Syntax:**
```python
def function_name(...):    # definition (runs nothing yet)
    ...

function_name(...)         # call (this actually executes the body)
```

**Key Notes:**
- Definition = writing the recipe. Call = actually cooking.
- You can call the same function repeatedly with different arguments.
- **Order matters:** a function must be defined *before* it is called.
  Calling it earlier raises `NameError: name '...' is not defined`.

```python
# Define ONCE, call MANY times

def wish(name):
    print("Hello,", name)

wish("Ravi")     # call 1
wish("Alice")    # call 2
wish("Bob")      # call 3
```

**Output:**
```text
Hello, Ravi
Hello, Alice
Hello, Bob
```

## 10. Parameters vs Arguments

These two words are often confused. The difference is simply *definition time* vs
*call time*.

| Term          | When            | Meaning                                   | Example            |
|---------------|-----------------|-------------------------------------------|--------------------|
| **Parameter** | Definition time | Placeholder name in the `def` line        | `def add(a, b)`    |
| **Argument**  | Call time       | Actual value you pass in                  | `add(10, 20)`      |

Memory hook: **P**arameter = **P**laceholder, **A**rgument = **A**ctual value.

**Key Notes:**
- `a` and `b` are parameters; `10` and `20` are arguments.
- Arguments are copied into parameters when the call happens.

```python
# a, b are PARAMETERS (placeholders in the definition)
def add(a, b):
    return a + b

# 10, 20 are ARGUMENTS (actual values passed at the call)
print(add(10, 20))   # 30
print(add(3, 4))     # 7
```

**Output:**
```text
30
7
```

## 11. Positional Arguments

**Positional arguments** are matched to parameters **by their position/order**.
The first argument fills the first parameter, the second fills the second, and so on.

**Key Notes:**
- Order is everything — swapping arguments changes the meaning.
- Number of positional arguments must match the number of parameters.

```python
def divide(a, b):
    return a / b

# Position decides the meaning: a=10, b=2
print(divide(10, 2))   # 5.0

# Swapped order -> different result: a=2, b=10
print(divide(2, 10))   # 0.2
```

**Output:**
```text
5.0
0.2
```

## 12. Keyword Arguments

**Keyword arguments** are passed as `name=value`. Because each value is tied to a
parameter name, the **order no longer matters**.

**Syntax:**
```python
function_name(param2=value2, param1=value1)
```

**Key Notes:**
- Keyword arguments improve readability at the call site.
- Positional arguments must come **before** any keyword arguments.

```python
def introduce(name, age, city):
    print(f"{name} is {age} years old and lives in {city}.")

# Order does NOT matter when using keywords
introduce(age=21, city="Pune", name="Alice")

# Mixing: positional first, then keyword
introduce("Bob", city="Delhi", age=25)
```

**Output:**
```text
Alice is 21 years old and lives in Pune.
Bob is 25 years old and lives in Delhi.
```

## 13. Default Parameters

A parameter can have a **default value**, used automatically when the caller does not
supply an argument for it. This makes some arguments optional.

**Syntax:**
```python
def function_name(required, optional=default_value):
    ...
```

**Key Notes:**
- Parameters **with** defaults must come **after** parameters without defaults.
- Defaults make functions flexible without forcing every caller to pass everything.

```python
def greet(name, greeting="Hello"):
    print(greeting, name)

greet("Ravi")                  # uses default -> Hello Ravi
greet("Alice", "Welcome")      # overrides default -> Welcome Alice
```

**Output:**
```text
Hello Ravi
Welcome Alice
```

### ⚠️ Pitfall: Mutable Default Arguments

A very common interview trap: **never use a mutable object (list/dict) as a default
value**. The default is created **once** when the function is defined and is then
*shared across every call* — so it "remembers" previous calls.

The cell below shows the bug: the list keeps growing across calls even though we
seem to start fresh each time.

```python
# BUG: the default list is shared between calls
def add_item(item, bag=[]):     # <-- mutable default (dangerous)
    bag.append(item)
    return bag

print(add_item("apple"))        # ['apple']            (looks fine)
print(add_item("banana"))       # ['apple', 'banana']  (SURPRISE! old data kept)
print(add_item("cherry"))       # ['apple', 'banana', 'cherry']
```

**Output:**
```text
['apple']
['apple', 'banana']
['apple', 'banana', 'cherry']
```

```python
# FIX: use None as the default, then create a fresh list inside
def add_item(item, bag=None):
    if bag is None:             # make a NEW list on every call
        bag = []
    bag.append(item)
    return bag

print(add_item("apple"))        # ['apple']
print(add_item("banana"))       # ['banana']   (correct: independent)
print(add_item("cherry"))       # ['cherry']
```

**Output:**
```text
['apple']
['banana']
['cherry']
```

## 14. Keyword-Only Arguments

Anything written **after a bare `*`** in the parameter list must be passed **by
keyword**, never positionally. This is useful to force clear, self-documenting calls.

**Syntax:**
```python
def func(a, b, *, option):   # 'option' MUST be given as option=...
    ...
```

**Key Notes:**
- The bare `*` marks the boundary; everything after it is keyword-only.
- Trying to pass a keyword-only argument positionally raises `TypeError`.

```python
def create_user(name, *, active=True, role="user"):
    print(f"{name} | active={active} | role={role}")

# 'active' and 'role' MUST be passed by keyword
create_user("Alice")
create_user("Bob", active=False, role="admin")
# create_user("Bob", False)  # would raise TypeError (positional not allowed)
```

**Output:**
```text
Alice | active=True | role=user
Bob | active=False | role=admin
```

## 15. `*args` – Variable-Length Positional Arguments

Sometimes you do not know how many arguments will be passed. `*args` collects any
number of **positional** arguments into a **tuple**.

**Syntax:**
```python
def function_name(*args):
    # args is a tuple of all extra positional arguments
    ...
```

**Key Notes:**
- The name `args` is a convention; the `*` is what matters.
- Inside the function, `args` behaves like a normal tuple (loop, `sum`, `len`, ...).

```python
# Sum any number of values using *args
def add_all(*numbers):
    print("Received tuple:", numbers)   # numbers is a tuple
    return sum(numbers)

print(add_all(1, 2, 3))            # 6
print(add_all(5, 10, 15, 20))      # 50
print(add_all())                   # 0  (empty tuple)
```

**Output:**
```text
Received tuple: (1, 2, 3)
6
Received tuple: (5, 10, 15, 20)
50
Received tuple: ()
0
```

```python
# Average using *args (guard against division by zero)
def average(*numbers):
    if len(numbers) == 0:
        return 0
    return sum(numbers) / len(numbers)

print(average(10, 20, 30))     # 20.0
print(average(4, 8))           # 6.0
```

**Output:**
```text
20.0
6.0
```

## 16. `**kwargs` – Variable-Length Keyword Arguments

`**kwargs` collects any number of **keyword** arguments into a **dictionary**
(`{name: value}`). Use it when the caller may pass extra named options.

**Syntax:**
```python
def function_name(**kwargs):
    # kwargs is a dict of all extra keyword arguments
    ...
```

**Key Notes:**
- The name `kwargs` is a convention; the `**` is what matters.
- Iterate with `kwargs.items()` just like any dictionary.

```python
# Print a profile from any number of keyword arguments
def make_profile(**details):
    print("Type:", type(details).__name__)   # dict
    for key, value in details.items():
        print(f"  {key}: {value}")

make_profile(name="Alice", age=20, city="Bengaluru")
print("---")
make_profile(name="Bob", role="Developer")
```

**Output:**
```text
Type: dict
  name: Alice
  age: 20
  city: Bengaluru
---
Type: dict
  name: Bob
  role: Developer
```

## 17. Unpacking Arguments at the Call Site

The `*` and `**` operators also work **when calling** a function. `*` unpacks a
list/tuple into positional arguments; `**` unpacks a dict into keyword arguments.

**Syntax:**
```python
func(*a_list)        # spread list items as positional args
func(**a_dict)       # spread dict pairs as keyword args
```

**Key Notes:**
- The list length must match the number of parameters when using `*`.
- The dict keys must match the parameter names when using `**`.

```python
def rectangle(length, breadth):
    return length * breadth

dims_list = [4, 5]              # -> length=4, breadth=5
print("From list:", rectangle(*dims_list))

dims_dict = {"length": 6, "breadth": 3}
print("From dict:", rectangle(**dims_dict))
```

**Output:**
```text
From list: 20
From dict: 18
```

## 18. Parameter Ordering Rule

When you mix argument types in one definition, Python enforces a strict order:

```text
def f( positional , *args , default=value , **kwargs ):
        (1)          (2)        (3)             (4)
```

| Order | Kind                      | Collects              |
|-------|---------------------------|-----------------------|
| 1     | Positional / required     | fixed values          |
| 2     | `*args`                   | extra positionals → tuple |
| 3     | Keyword with default      | optional named values |
| 4     | `**kwargs`                | extra keywords → dict |

**Key Notes:**
- Get the order wrong and Python raises a `SyntaxError`.
- A simple memory aid: **required → \*args → defaults → \*\*kwargs**.

```python
# One function using all four kinds together
def order_demo(item, *extras, discount=0, **info):
    print("item     :", item)      # required positional
    print("extras   :", extras)    # tuple from *args
    print("discount :", discount)  # keyword with default
    print("info     :", info)      # dict from **kwargs

order_demo("Laptop", "Mouse", "Bag", discount=10, brand="Dell", warranty="2y")
```

**Output:**
```text
item     : Laptop
extras   : ('Mouse', 'Bag')
discount : 10
info     : {'brand': 'Dell', 'warranty': '2y'}
```

## 19. The `return` Statement (return vs print)

This is one of the **most important** distinctions for beginners.

- `print()` only **shows** a value on the screen — it gives nothing back to the program.
- `return` **sends a value back** to the caller so it can be stored and reused.

**Key Notes:**
- A `print`-only function returns `None`, so `x = show(...)` stores `None`.
- Use `return` whenever the result must be used later (stored, added, compared).
- `return` also **immediately exits** the function.

```python
# Function that PRINTS (cannot be reused)
def add_print(a, b):
    print(a + b)          # only displays

# Function that RETURNS (result can be reused)
def add_return(a, b):
    return a + b          # hands the value back

add_print(2, 3)                       # shows 5
result = add_return(2, 3)             # captures 5
print("Reused result * 10 =", result * 10)   # 50

# Capturing the print version gives None
captured = add_print(1, 1)            # shows 2
print("Captured from print version:", captured)   # None
```

**Output:**
```text
5
Reused result * 10 = 50
2
Captured from print version: None
```

## 20. Early Return / Guard Clauses

`return` exits the function immediately. A **guard clause** uses an early `return` to
handle invalid or special cases first, keeping the main logic flat and readable.

**Key Notes:**
- Any code after a `return` in the same branch never runs (dead code).
- Guard clauses reduce deep nesting (fewer `else` blocks).

```python
def safe_divide(a, b):
    if b == 0:
        return "Error: cannot divide by zero"   # guard clause exits early
    return a / b                                 # main logic

print(safe_divide(10, 2))   # 5.0
print(safe_divide(10, 0))   # Error: cannot divide by zero
```

**Output:**
```text
5.0
Error: cannot divide by zero
```

## 21. Returning Multiple Values

A function can return several values at once by separating them with commas. Python
packs them into a **tuple**, which you can **unpack** into separate variables.

**Key Notes:**
- `return a, b, c` actually returns the tuple `(a, b, c)`.
- Unpack with matching variables: `x, y, z = func()`.

```python
def arithmetic(a, b):
    add = a + b
    sub = a - b
    mul = a * b
    return add, sub, mul          # returns a tuple

# Unpack the returned tuple into three variables
s, d, p = arithmetic(8, 4)
print("Sum:", s, "| Diff:", d, "| Product:", p)

# Or keep it as a single tuple
result = arithmetic(8, 4)
print("As tuple:", result)
```

**Output:**
```text
Sum: 12 | Diff: 4 | Product: 32
As tuple: (12, 4, 32)
```

## 22. Returning Lists, Tuples and Dictionaries

Functions can return any object, including whole collections. This is common when a
function produces *many* results.

**Key Notes:**
- Return a **list** for an ordered, changeable sequence of results.
- Return a **tuple** for fixed grouped results.
- Return a **dictionary** for labelled (key → value) results.

```python
# Returning a LIST
def even_numbers(limit):
    result = []
    for n in range(1, limit + 1):
        if n % 2 == 0:
            result.append(n)
    return result

print(even_numbers(10))   # [2, 4, 6, 8, 10]
```

**Output:**
```text
[2, 4, 6, 8, 10]
```

```python
# Returning a TUPLE (min and max together)
def min_max(values):
    return min(values), max(values)

low, high = min_max([7, 2, 9, 4])
print("Min:", low, "| Max:", high)
```

**Output:**
```text
Min: 2 | Max: 9
```

```python
# Returning a DICTIONARY (labelled results)
def circle_info(radius):
    return {
        "radius": radius,
        "area": round(3.14159 * radius * radius, 2),
        "circumference": round(2 * 3.14159 * radius, 2),
    }

print(circle_info(5))
```

**Output:**
```text
{'radius': 5, 'area': 78.54, 'circumference': 31.42}
```

## 23. Functions With No `return` (return `None`)

If a function has no `return` statement (or a bare `return`), it automatically
returns the special value `None`.

**Key Notes:**
- `None` represents "no value / nothing".
- A function whose job is only a *side effect* (like printing) usually returns `None`.

```python
def log_message(msg):
    print("LOG:", msg)      # no return statement

value = log_message("Saved successfully")
print("Returned value:", value)          # None
print("Type of value :", type(value))    # <class 'NoneType'>
```

**Output:**
```text
LOG: Saved successfully
Returned value: None
Type of value : <class 'NoneType'>
```

## 24. Local Scope

**Scope** is the region where a variable is visible. A variable created **inside** a
function lives in its **local scope** and is destroyed when the function ends.

**Key Notes:**
- Local variables cannot be accessed from outside the function.
- Each call gets its own fresh set of local variables.

```python
def show():
    message = "I am local"     # local variable
    print("Inside function:", message)

show()

# Trying to read 'message' out here would raise NameError,
# because it only exists inside show(). We show the safe part only:
print("Outside function: 'message' does not exist here")
```

**Output:**
```text
Inside function: I am local
Outside function: 'message' does not exist here
```

## 25. Global Scope

A variable defined at the top level of a file (outside any function) has **global
scope**. It can be **read** from inside functions.

**Key Notes:**
- Functions can freely *read* global variables.
- To *reassign* a global from inside a function you need the `global` keyword (next section).

```python
pi = 3.14159        # global variable

def area_of_circle(radius):
    # reads the global 'pi' without any special keyword
    return pi * radius * radius

print("pi (global):", pi)
print("Area:", round(area_of_circle(2), 2))
```

**Output:**
```text
pi (global): 3.14159
Area: 12.57
```

## 26. The `global` Keyword

By default, assigning to a variable inside a function creates a **new local**
variable. To modify the *global* variable instead, declare it with `global`.

**Key Notes:**
- Without `global`, the assignment only changes a local copy.
- With `global`, the assignment changes the real global variable.
- Overusing `global` is discouraged — prefer returning values instead.

```python
# WITHOUT global: the global 'count' is NOT changed
count = 0

def increment_local():
    count = 1           # creates a brand-new LOCAL variable
    return count

print("Function returned:", increment_local())   # 1
print("Global count is  :", count)               # still 0
```

**Output:**
```text
Function returned: 1
Global count is  : 0
```

```python
# WITH global: the global 'count' IS changed
count = 0

def increment_global():
    global count        # refer to the global variable
    count += 1
    return count

print("Function returned:", increment_global())  # 1
print("Global count is  :", count)               # now 1
```

**Output:**
```text
Function returned: 1
Global count is  : 1
```

## 27. Nested (Helper) Functions

A function can be defined **inside** another function. The inner function is a private
helper, visible only within the outer function's body.

**Key Notes:**
- The inner function can read variables from the enclosing function (Enclosing scope).
- Nesting is handy for small helpers that are not needed elsewhere.

```python
def make_greeting(name):
    prefix = "Hello, "          # enclosing-scope variable

    def build():                # nested helper function
        return prefix + name    # reads 'prefix' and 'name' from enclosing scope

    return build()

print(make_greeting("Alice"))   # Hello, Alice
```

**Output:**
```text
Hello, Alice
```

## 28. The LEGB Rule

When Python looks up a name, it searches four scopes in this order and stops at the
first match:

```text
   L  ──▶  Local         (inside the current function)
   E  ──▶  Enclosing      (any outer function wrapping this one)
   G  ──▶  Global         (top level of the module/file)
   B  ──▶  Built-in        (names like len, print, sum)
```

**Key Notes:**
- Search goes inside-out: Local first, Built-in last.
- **Enclosing** scope appears when one function is defined inside another.

```python
x = "global"            # G

def outer():
    x = "enclosing"     # E (for inner)
    def inner():
        # no local x, so Python finds the ENCLOSING x
        print("inner sees:", x)
    inner()

outer()                 # inner sees: enclosing
print("module sees:", x)   # module sees: global

# 'len' below is resolved from the Built-in scope (B)
print("len built-in:", len("python"))
```

**Output:**
```text
inner sees: enclosing
module sees: global
len built-in: 6
```

## 29. Type Hints / Annotations (Brief)

Python lets you **annotate** the expected types of parameters and the return value.
These hints are *optional documentation* — Python does **not** enforce them at runtime.

**Syntax:**
```python
def function_name(param: type) -> return_type:
    ...
```

**Key Notes:**
- Hints improve readability and help tools (editors, `mypy`) catch mistakes.
- They are stored in `func.__annotations__` but do not change behaviour.

```python
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b

print("add(3, 4) =", add(3, 4))
print("annotations:", add.__annotations__)
# Note: hints are NOT enforced -> this still runs and concatenates strings
print("not enforced:", add("Py", "thon"))
```

**Output:**
```text
add(3, 4) = 7
annotations: {'a': <class 'int'>, 'b': <class 'int'>, 'return': <class 'int'>}
not enforced: Python
```

## 30. Docstrings

A **docstring** is a triple-quoted string written as the **first line inside** a
function. It documents what the function does. Tools read it via `help()` and the
`__doc__` attribute.

**Syntax:**
```python
def func(...):
    """One-line summary of what the function does."""
    ...
```

**Key Notes:**
- Place the docstring immediately after the `def` line.
- `help(func)` and `func.__doc__` both display it.
- Good docstrings describe purpose, parameters and return value.

```python
def area_of_rectangle(length, breadth):
    """Return the area of a rectangle given its length and breadth."""
    return length * breadth

# Access the docstring two ways
print(area_of_rectangle.__doc__)
print("Area:", area_of_rectangle(4, 5))
```

**Output:**
```text
Return the area of a rectangle given its length and breadth.
Area: 20
```

```python
# help() prints the full signature + docstring
def is_prime(n):
    """Return True if n is a prime number, else False.

    A prime number is greater than 1 and divisible only by 1 and itself.
    """
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

help(is_prime)
```

**Output:**
```text
Help on function is_prime in module __main__:

is_prime(n)
    Return True if n is a prime number, else False.

    A prime number is greater than 1 and divisible only by 1 and itself.
```

## 31. Pass by Object Reference

Python passes **references to objects**, not copies. What happens next depends on
whether the object is **mutable** or **immutable** — a classic interview point.

- **Mutable** (list, dict, set): changes *inside* the function are visible outside.
- **Immutable** (int, str, tuple): rebinding inside the function does *not* affect the caller.

**Key Notes:**
- Mutating in place (`list.append`) affects the original object.
- Reassigning a parameter (`x = x + 1`) only changes the local name.

```python
# MUTABLE argument: the original list IS modified in place
def add_zero(items):
    items.append(0)        # mutates the same list object

my_list = [1, 2, 3]
add_zero(my_list)
print("List after call:", my_list)   # [1, 2, 3, 0]  -> changed!
```

**Output:**
```text
List after call: [1, 2, 3, 0]
```

```python
# IMMUTABLE argument: the original int is NOT changed
def add_one(number):
    number = number + 1    # rebinds the LOCAL name only
    print("Inside function:", number)

my_number = 10
add_one(my_number)
print("Outside function:", my_number)   # still 10 -> unchanged
```

**Output:**
```text
Inside function: 11
Outside function: 10
```

## 32. Best Practices

Professional functions follow a few simple rules:

- **Single Responsibility** – each function should do exactly one thing.
- **Descriptive Names** – use clear verb-based names (`calculate_total`, not `ct`).
- **Write Docstrings** – document purpose, parameters and return value.
- **Return, don't print** – return results so callers can reuse them.
- **Avoid globals** – pass data in as arguments and return results out.
- **Keep them small** – if a function is very long, split it into smaller ones.
- **Use defaults wisely** – and never use a mutable default value.
- **Validate inputs** – guard against bad values (e.g. empty lists, zero divisor).

## 33. Common Mistakes (Wrong vs Right)

Below are the most frequent beginner errors. The wrong code is shown as **text only**
(so it does not break the notebook); the fixes run in the next code cell.

**1. Forgetting `return` (function silently returns `None`)**
```python
# WRONG                     # RIGHT
def square(n):              def square(n):
    n * n                       return n * n
```

**2. Calling a function before it is defined**
```python
# WRONG                     # RIGHT
greet()                     def greet():
def greet():                    print("Hi")
    print("Hi")             greet()
# NameError!
```

**3. Mutable default argument**
```python
# WRONG                     # RIGHT
def f(x, bag=[]):           def f(x, bag=None):
    bag.append(x)               if bag is None:
    return bag                      bag = []
                                bag.append(x)
                                return bag
```

### Common Mistakes (continued)

**4. Shadowing built-in names**
```python
# WRONG                     # RIGHT
list = [1, 2, 3]            numbers = [1, 2, 3]
# list() is now broken      # built-in list() still works
```

**5. Wrong number of arguments**
```python
# WRONG                     # RIGHT
def add(a, b):              def add(a, b):
    return a + b                return a + b
add(5)                      add(5, 3)
# TypeError: missing 'b'
```

**6. Wrong indentation of the body**
```python
# WRONG                     # RIGHT
def greet():                def greet():
print("Hi")                     print("Hi")
# IndentationError
```

**Key Notes:**
- Most of these raise clear errors (`NameError`, `TypeError`, `IndentationError`).
- The mutable-default one is silent and dangerous — watch for it.

```python
# The RIGHT versions, running cleanly
def square(n):
    return n * n            # fix #1: return the result

def add(a, b):
    return a + b

numbers = [1, 2, 3]         # fix #4: don't shadow built-in 'list'

print("square(6) =", square(6))     # 36
print("add(5, 3) =", add(5, 3))     # 8
print("built-in list still works:", list("abc"))
print("numbers list:", numbers)
```

**Output:**
```text
square(6) = 36
add(5, 3) = 8
built-in list still works: ['a', 'b', 'c']
numbers list: [1, 2, 3]
```

## 34. Mini DSA Examples

Below are small, self-contained functions — the kind you meet in placement rounds.
Each has a docstring and a printed test. All are **iterative** (recursion is covered
on Day 10).

```python
# 1) Factorial (iterative): n! = 1*2*...*n
def factorial(n):
    """Return n! computed with a loop."""
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

print("factorial(5) =", factorial(5))   # 120
```

**Output:**
```text
factorial(5) = 120
```

```python
# 2) Even check
def is_even(n):
    """Return True if n is even."""
    return n % 2 == 0

print("is_even(12) =", is_even(12))   # True
print("is_even(7)  =", is_even(7))    # False
```

**Output:**
```text
is_even(12) = True
is_even(7)  = False
```

```python
# 3) Maximum of two numbers
def max_of_two(a, b):
    """Return the larger of two numbers."""
    return a if a > b else b

print("max_of_two(10, 25) =", max_of_two(10, 25))   # 25
```

**Output:**
```text
max_of_two(10, 25) = 25
```

```python
# 4) Maximum of three numbers
def max_of_three(a, b, c):
    """Return the largest of three numbers."""
    largest = a
    if b > largest:
        largest = b
    if c > largest:
        largest = c
    return largest

print("max_of_three(4, 9, 7) =", max_of_three(4, 9, 7))   # 9
```

**Output:**
```text
max_of_three(4, 9, 7) = 9
```

```python
# 5) Count vowels in a string
def count_vowels(text):
    """Return the number of vowels in text."""
    vowels = "aeiouAEIOU"
    count = 0
    for ch in text:
        if ch in vowels:
            count += 1
    return count

print("count_vowels('Education') =", count_vowels("Education"))   # 5
```

**Output:**
```text
count_vowels('Education') = 5
```

```python
# 6) Reverse a string
def reverse_string(text):
    """Return the reversed string using slicing."""
    return text[::-1]

print("reverse_string('python') =", reverse_string("python"))   # nohtyp
```

**Output:**
```text
reverse_string('python') = nohtyp
```

```python
# 7) Palindrome check
def is_palindrome(text):
    """Return True if text reads the same forwards and backwards."""
    return text == text[::-1]

print("is_palindrome('madam') =", is_palindrome("madam"))   # True
print("is_palindrome('hello') =", is_palindrome("hello"))   # False
```

**Output:**
```text
is_palindrome('madam') = True
is_palindrome('hello') = False
```

```python
# 8) Sum of digits of a number
def sum_of_digits(n):
    """Return the sum of the digits of a non-negative integer."""
    total = 0
    n = abs(n)
    while n > 0:
        total += n % 10   # last digit
        n //= 10          # drop last digit
    return total

print("sum_of_digits(1234) =", sum_of_digits(1234))   # 10
```

**Output:**
```text
sum_of_digits(1234) = 10
```

```python
# 9) Prime check
def is_prime(n):
    """Return True if n is a prime number."""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

print("is_prime(29) =", is_prime(29))   # True
print("is_prime(15) =", is_prime(15))   # False
```

**Output:**
```text
is_prime(29) = True
is_prime(15) = False
```

```python
# 10) GCD using the Euclidean algorithm (iterative)
def gcd(a, b):
    """Return the greatest common divisor of a and b."""
    while b != 0:
        a, b = b, a % b
    return a

print("gcd(48, 18) =", gcd(48, 18))   # 6
```

**Output:**
```text
gcd(48, 18) = 6
```

```python
# 11) First n Fibonacci numbers as a list
def fibonacci_list(n):
    """Return a list of the first n Fibonacci numbers."""
    seq = []
    a, b = 0, 1
    for _ in range(n):
        seq.append(a)
        a, b = b, a + b
    return seq

print("fibonacci_list(8) =", fibonacci_list(8))   # [0,1,1,2,3,5,8,13]
```

**Output:**
```text
fibonacci_list(8) = [0, 1, 1, 2, 3, 5, 8, 13]
```

```python
# 12) Count words in a sentence
def count_words(sentence):
    """Return the number of words in a sentence."""
    return len(sentence.split())

print("count_words('I love Python programming') =",
      count_words("I love Python programming"))   # 4
```

**Output:**
```text
count_words('I love Python programming') = 4
```

```python
# 13) Leap year check
def is_leap_year(year):
    """Return True if year is a leap year."""
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

print("is_leap_year(2024) =", is_leap_year(2024))   # True
print("is_leap_year(1900) =", is_leap_year(1900))   # False
```

**Output:**
```text
is_leap_year(2024) = True
is_leap_year(1900) = False
```

```python
# 14) Second largest number in a list
def second_largest(values):
    """Return the second largest distinct value in a list."""
    unique = sorted(set(values))     # remove duplicates and sort ascending
    if len(unique) < 2:
        return None                  # not enough distinct values
    return unique[-2]

print("second_largest([4, 1, 7, 7, 3]) =", second_largest([4, 1, 7, 7, 3]))   # 4
```

**Output:**
```text
second_largest([4, 1, 7, 7, 3]) = 4
```

## 35. Summary

- A **function** is a named, reusable block of code that does one task.
- Define with `def name(params):` and run it with `name(args)`.
- **Parameters** are placeholders; **arguments** are the actual values.
- Arguments can be **positional**, **keyword**, or **default**; a bare `*` makes the
  following parameters **keyword-only**.
- `*args` collects extra positionals into a **tuple**; `**kwargs` collects extra
  keywords into a **dict**. Order: positional → `*args` → defaults → `**kwargs`.
- `return` sends a value back (and exits); `print` only displays. No `return` → `None`.
- Functions can return single values, multiple values (tuple), or whole collections.
- **Scope**: local variables live inside a function; use `global` to modify globals.
- Name lookup follows the **LEGB** rule (Local → Enclosing → Global → Built-in).
- Write **docstrings**, add optional **type hints**, follow best practices, and avoid
  mutable default arguments.

## 36. Practice Questions

1. Write a function `square(n)` that returns the square of a number.
2. Write a function that returns the **largest of two** numbers.
3. Write a function `count_vowels(text)` that counts vowels in a string.
4. Write a function using `*args` that returns the **sum** of any number of values.
5. Write a function `area(length, breadth)` that returns the area of a rectangle.
6. Write a function with a **default parameter** (e.g. `greet(name, msg="Hello")`).
7. Write a function that returns **both** the quotient and remainder of two numbers.
8. Write a function `is_palindrome(text)` that checks whether a string is a palindrome.
9. Write a function using `**kwargs` that prints a student profile.
10. Write a function `factorial(n)` (iterative) and test it for `n = 6`.
