# Day 10 – Advanced Functions

**Duration:** 50–60 Minutes

### Learning Outcomes
- Treat functions as first-class objects (pass, return, store them).
- Write **lambda** (anonymous) functions and know when *not* to.
- Use functional tools: `map()`, `filter()`, `reduce()`, `zip()`, `enumerate()`, `sorted()`.
- Master common built-ins: `any()`, `all()`, `abs()`, `round()`, `sum()`, `max()`, `min()`.
- Understand **recursion** — base case, recursive case and the call stack.
- Solve classic problems recursively and know recursion vs iteration trade-offs.

## 1. Revision of Day 9

Before we go advanced, recall the fundamentals from Day 9.

| Concept | Meaning |
|---|---|
| `def name(params):` | Defines a function |
| **Parameter** | Variable in the definition |
| **Argument** | Actual value passed in the call |
| `return` | Sends a value back to the caller (ends the function) |
| `*args` / `**kwargs` | Variable positional / keyword arguments |
| **Local scope** | Names created inside a function |
| **Global scope** | Names created at module level |

**Key Notes:**
- A function with no `return` gives back `None`.
- `return` *sends a value back*; `print` only *displays* it.
- Today we build **on top of** these ideas — no need to repeat them.

```python
# Quick warm-up recap from Day 9
def add(a, b):        # a, b are parameters
    return a + b      # return sends the value back

result = add(10, 20)  # 10, 20 are arguments
print(result)
```

**Output:**
```text
30
```

## 2. First-Class Functions

In Python, **functions are objects** — just like `int`, `str` or `list`. This is called being
*first-class*. It means a function can be:

1. **Assigned** to a variable.
2. **Passed** as an argument to another function.
3. **Returned** from another function.
4. **Stored** inside a list or dictionary.

This single idea is what makes `map()`, `filter()`, `sorted(key=...)` and decorators possible.

**Key Notes:**
- Use the function *name without* `()` to refer to the object itself.
- Use `()` to actually **call** it.

```python
def greet(name):
    return "Hello, " + name

# 1. Assign the function to another variable (no parentheses!)
say = greet
print(say("Ravi"))        # calling through the new name

# Proof it is an object with a type
print(type(greet))
print(greet.__name__)
```

**Output:**
```text
Hello, Ravi
<class 'function'>
greet
```

```python
# 2. Pass a function as an argument to another function
def shout(text):
    return text.upper() + "!"

def apply(func, value):   # func is a function passed in
    return func(value)    # call whatever was passed

print(apply(shout, "hello"))
print(apply(len, "python"))   # built-ins work too
```

**Output:**
```text
HELLO!
6
```

```python
# 3. Return a function from a function (a "function factory")
def multiplier(n):
    def inner(x):         # inner remembers n (closure)
        return x * n
    return inner          # return the function object

double = multiplier(2)
triple = multiplier(3)
print(double(10))         # 20
print(triple(10))         # 30
```

**Output:**
```text
20
30
```

```python
# 4. Store functions in a dictionary (a mini calculator / dispatch table)
ops = {
    "add": lambda a, b: a + b,
    "sub": lambda a, b: a - b,
    "mul": lambda a, b: a * b,
}
print(ops["add"](4, 5))
print(ops["mul"](4, 5))
```

**Output:**
```text
9
20
```

## 3. Lambda Functions — What & Why

A **lambda** is a small **anonymous** function (a function with no name) written in a single line.
It is used for short, throwaway logic — usually where a function is expected *as an argument*
(e.g. inside `map`, `filter`, `sorted`).

**Why lambda?**
- Saves writing a full `def` for a one-line operation.
- Keeps the logic *right where it is used* (readable for tiny operations).
- Perfect as the `key=` for sorting or as the transform in `map`.

## 4. Lambda Syntax

**Syntax**
```python
lambda arg1, arg2, ... : expression
```

- No `def`, no name, no `return` keyword.
- The value of the **expression** is returned automatically.
- Can take any number of arguments but only **one expression**.

### `def` vs `lambda`

| Feature | `def` function | `lambda` |
|---|---|---|
| Name | Has a name | Anonymous |
| Body | Many statements | Single expression |
| `return` | Written explicitly | Implicit (auto) |
| Docstring | Yes | No |
| Best for | Reusable, complex logic | Short, one-off logic |

## 5. Lambda Examples

```python
square = lambda x: x * x          # one argument
print(square(5))

add = lambda a, b: a + b          # two arguments
print(add(10, 20))

greater = lambda a, b: a if a > b else b   # ternary inside lambda
print(greater(8, 3))
```

**Output:**
```text
25
30
8
```

```python
# The SAME function written both ways
def cube_def(x):
    return x ** 3

cube_lambda = lambda x: x ** 3

print(cube_def(3), cube_lambda(3))   # identical result
```

**Output:**
```text
27 27
```

```python
# Most common real use: as the key for sorting
words = ["banana", "kiwi", "watermelon", "fig"]
by_length = sorted(words, key=lambda w: len(w))
print(by_length)
```

**Output:**
```text
['fig', 'kiwi', 'banana', 'watermelon']
```

## 6. `map()` — Transform Every Item

`map()` applies a function to **every item** of an iterable and returns a `map` object
(a lazy iterator). Wrap it in `list()` to see the results.

**Syntax**
```python
map(function, iterable)
```

**Key Notes:**
- The function is applied item-by-item; the output has the **same length** as the input.
- `map()` is lazy — you must convert it (e.g. `list(...)`) to view/reuse it.

```python
nums = [1, 2, 3, 4]

# With a lambda
squares = list(map(lambda x: x * x, nums))
print(squares)

# With a named function
def to_celsius(f):
    return round((f - 32) * 5 / 9, 1)

temps = [32, 212, 98.6]
print(list(map(to_celsius, temps)))
```

**Output:**
```text
[1, 4, 9, 16]
[0.0, 100.0, 37.0]
```

```python
# map over two iterables at once (function takes 2 args)
a = [1, 2, 3]
b = [10, 20, 30]
print(list(map(lambda x, y: x + y, a, b)))
```

**Output:**
```text
[11, 22, 33]
```

## 7. `filter()` — Keep Items That Pass a Test

`filter()` keeps only the items for which the function returns **True**.

**Syntax**
```python
filter(function, iterable)
```

**Key Notes:**
- The function must return a boolean (truthy/falsy).
- Output length is **≤** input length (only the passing items survive).
- Like `map`, it is lazy — wrap in `list()`.

```python
nums = [1, 2, 3, 4, 5, 6]

evens = list(filter(lambda x: x % 2 == 0, nums))
print(evens)

positives = list(filter(lambda x: x > 0, [-3, 5, -1, 8, 0]))
print(positives)
```

**Output:**
```text
[2, 4, 6]
[5, 8]
```

```python
# Remove empty / blank strings
names = ["Ravi", "", "Alice", "   ", "Bob"]
clean = list(filter(lambda s: s.strip() != "", names))
print(clean)
```

**Output:**
```text
['Ravi', 'Alice', 'Bob']
```

## 8. `reduce()` — Boil a Sequence Down to One Value

`reduce()` repeatedly combines items **pair by pair**, carrying the result forward, until a
single value remains. It lives in the **`functools`** module, so it must be imported.

**Syntax**
```python
from functools import reduce
reduce(function, iterable[, initializer])
```

**Key Notes:**
- The function takes **two** arguments: the running result and the next item.
- Great for product, running total, max-by-hand, etc.
- For a plain sum, prefer the built-in `sum()`.

```python
from functools import reduce

# Product of all numbers: ((1*2)*3)*4 = 24
product = reduce(lambda acc, x: acc * x, [1, 2, 3, 4])
print(product)

# Sum with an initial value of 100
total = reduce(lambda acc, x: acc + x, [1, 2, 3], 100)
print(total)
```

**Output:**
```text
24
106
```

## 9. `zip()` — Pair Up Iterables

`zip()` pairs items from two (or more) iterables position-by-position, producing tuples.

**Syntax**
```python
zip(iterable1, iterable2, ...)
```

**Key Notes:**
- Stops at the **shortest** iterable (extra items are ignored).
- Commonly used to build a dict from two lists, or to loop over two lists together.
- `zip(*pairs)` **unzips** back into separate sequences.

```python
fruits = ["Apple", "Banana", "Cherry"]
prices = [50, 30, 80]

# Pair them
print(list(zip(fruits, prices)))

# Loop over both together
for fruit, price in zip(fruits, prices):
    print(fruit, "->", price)
```

**Output:**
```text
[('Apple', 50), ('Banana', 30), ('Cherry', 80)]
Apple -> 50
Banana -> 30
Cherry -> 80
```

```python
# Build a dictionary from two lists
fruits = ["Apple", "Banana", "Cherry"]
prices = [50, 30, 80]
menu = dict(zip(fruits, prices))
print(menu)

# Unequal lengths: stops at the shortest
print(list(zip([1, 2, 3], ["a", "b"])))
```

**Output:**
```text
{'Apple': 50, 'Banana': 30, 'Cherry': 80}
[(1, 'a'), (2, 'b')]
```

```python
# Unzip with the * operator
pairs = [("Apple", 50), ("Banana", 30)]
names, costs = zip(*pairs)
print(names)
print(costs)
```

**Output:**
```text
('Apple', 'Banana')
(50, 30)
```

## 10. `enumerate()` — Index + Value Together

`enumerate()` gives you both the **index** and the **value** while looping — cleaner than
manually maintaining a counter.

**Syntax**
```python
enumerate(iterable, start=0)
```

**Key Notes:**
- Default index starts at `0`; pass `start=1` to begin at 1.
- Avoids the clumsy `for i in range(len(x))` pattern.

```python
fruits = ["Apple", "Banana", "Cherry"]

for i, fruit in enumerate(fruits):
    print(i, fruit)

print("---- start at 1 ----")
for rank, fruit in enumerate(fruits, start=1):
    print(rank, fruit)
```

**Output:**
```text
0 Apple
1 Banana
2 Cherry
---- start at 1 ----
1 Apple
2 Banana
3 Cherry
```

## 11. `sorted()` — Return a New Sorted List

`sorted()` returns a **new** sorted list and works on any iterable. It does **not** modify the
original. Compare with `list.sort()`, which sorts **in place** and returns `None`.

**Syntax**
```python
sorted(iterable, key=None, reverse=False)
```

| | `sorted(x)` | `x.sort()` |
|---|---|---|
| Works on | any iterable | lists only |
| Returns | a new list | `None` |
| Original | unchanged | modified in place |

**Key Notes:**
- `key=` accepts a function deciding *what to sort by*.
- `reverse=True` sorts high → low.

```python
nums = [4, 2, 8, 1]
print(sorted(nums))              # new sorted list
print(sorted(nums, reverse=True))
print(nums)                      # original unchanged
```

**Output:**
```text
[1, 2, 4, 8]
[8, 4, 2, 1]
[4, 2, 8, 1]
```

```python
# Sort by a custom key
words = ["banana", "kiwi", "fig", "watermelon"]
print(sorted(words, key=len))            # by length

# Sort a list of tuples by the 2nd element (price)
items = [("Apple", 50), ("Banana", 30), ("Cherry", 80)]
print(sorted(items, key=lambda t: t[1]))

# Sort a list of dicts by a field
students = [{"name": "Ravi", "marks": 88},
            {"name": "Alice", "marks": 95},
            {"name": "Bob", "marks": 72}]
print(sorted(students, key=lambda s: s["marks"], reverse=True))
```

**Output:**
```text
['fig', 'kiwi', 'banana', 'watermelon']
[('Banana', 30), ('Apple', 50), ('Cherry', 80)]
[{'name': 'Alice', 'marks': 95}, {'name': 'Ravi', 'marks': 88}, {'name': 'Bob', 'marks': 72}]
```

## 12. Essential Built-in Functions

Python ships with small, fast helpers you should reach for instead of writing loops.

**Functions:** `any()`, `all()`, `abs()`, `round()`, `sum()`, `max()`, `min()`

**Input:** an iterable (for `any/all/sum/max/min`) or a number (for `abs/round`).

**Output:**
- `any(iterable)` → `True` if **at least one** item is truthy.
- `all(iterable)` → `True` if **every** item is truthy.
- `abs(n)` → absolute (non-negative) value.
- `round(n, digits)` → number rounded to `digits` decimals.
- `sum(iterable)` → total.
- `max(iterable)` / `min(iterable)` → largest / smallest.

```python
nums = [4, 2, 8, 1]
print("sum :", sum(nums))
print("max :", max(nums))
print("min :", min(nums))
print("abs :", abs(-10))
print("round:", round(4.5678, 2))
```

**Output:**
```text
sum : 15
max : 8
min : 1
abs : 10
round: 4.57
```

```python
# any() and all() are perfect for validation
flags = [True, True, False]
print("any:", any(flags))   # at least one True -> True
print("all:", all(flags))   # not all True      -> False

marks = [45, 60, 90]
print("everyone passed?", all(m >= 35 for m in marks))
print("anyone failed?", any(m < 35 for m in marks))
```

**Output:**
```text
any: True
all: False
everyone passed? True
anyone failed? False
```

## 13. `max()` / `min()` With a `key`

Like `sorted`, `max` and `min` accept a `key=` function so you can find the item that is
"biggest/smallest **by** something" — e.g. the longest word.

```python
words = ["fig", "banana", "kiwi", "watermelon"]
print("longest :", max(words, key=len))
print("shortest:", min(words, key=len))

students = [{"name": "Ravi", "marks": 88}, {"name": "Alice", "marks": 95}]
topper = max(students, key=lambda s: s["marks"])
print("topper  :", topper["name"])
```

**Output:**
```text
longest : watermelon
shortest: fig
topper  : Alice
```

## 14. Recursion — A Function That Calls Itself

**Recursion** is when a function solves a problem by calling **itself** on a smaller version of
the same problem, until it reaches a case simple enough to answer directly.

Every recursive function needs two parts:

1. **Base case** — the stopping condition (no further recursion). *Mandatory.*
2. **Recursive case** — the function calls itself on a smaller input, moving toward the base case.

**Key Notes:**
- Think: *"Assume it already works for the smaller problem — how do I build the answer from that?"*
- Many problems (factorial, Fibonacci, tree traversal) are naturally recursive.

## 15. Base Case vs Recursive Case

```text
def factorial(n):
    if n == 0 or n == 1:     # <-- BASE CASE (stops the recursion)
        return 1
    return n * factorial(n-1)  # <-- RECURSIVE CASE (smaller input)
```

**Why the base case is mandatory:** without it, the function keeps calling itself forever.
Python protects you with a recursion limit (~1000 deep) and raises a
**`RecursionError: maximum recursion depth exceeded`** instead of freezing.

⚠️ *We never run infinite recursion here — the point is: every recursive call must move
**closer** to the base case.*

## 16. The Call Stack — How Recursion Really Runs

Each call is paused and stacked until the base case returns, then results **unwind** back up.

```text
factorial(3)
  -> 3 * factorial(2)
         -> 2 * factorial(1)
                -> returns 1          (base case)
         -> 2 * 1 = 2   returns 2
  -> 3 * 2 = 6          returns 6

WIND DOWN (calls pile up)      UNWIND (results come back)
  factorial(3)                   factorial(1) = 1
    factorial(2)                 factorial(2) = 2
      factorial(1)  <-- base --> factorial(3) = 6
```

**Key Notes:**
- Every pending call uses memory on the **stack** — deep recursion can be costly.
- The last call made is the first to finish (Last-In, First-Out).

## 17. Factorial (Recursive)

`n! = n × (n-1) × ... × 1`, and `0! = 1`.

**Dry run of `factorial(4)`:**
```text
4 * factorial(3)
4 * (3 * factorial(2))
4 * (3 * (2 * factorial(1)))
4 * (3 * (2 * 1))  = 24
```

```python
def factorial(n):
    if n == 0 or n == 1:       # base case
        return 1
    return n * factorial(n - 1)  # recursive case

print(factorial(4))
print(factorial(5))
```

**Output:**
```text
24
120
```

## 18. Fibonacci (Recursive) + Memoization

Fibonacci: `0, 1, 1, 2, 3, 5, 8, ...` where each number is the sum of the previous two.

The naive recursion is elegant but **slow** — `fib(n)` recomputes the same values many times
(exponential number of calls). **Memoization** (caching results in a dict) fixes this.

```python
# Naive recursive Fibonacci (fine for small n)
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

print([fib(i) for i in range(10)])
```

**Output:**
```text
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

```python
# Memoized version: remember answers so each n is computed once
def fib_memo(n, cache={}):
    if n <= 1:
        return n
    if n in cache:              # already computed?
        return cache[n]
    cache[n] = fib_memo(n - 1, cache) + fib_memo(n - 2, cache)
    return cache[n]

print(fib_memo(30))   # instant, unlike the naive version
```

**Output:**
```text
832040
```

## 19. Sum of Digits (Recursive)

Break the number: last digit is `n % 10`, the rest is `n // 10`.
```text
sum_digits(123) = 3 + sum_digits(12)
                = 3 + (2 + sum_digits(1))
                = 3 + 2 + 1 = 6
```

```python
def sum_digits(n):
    n = abs(n)
    if n < 10:            # base case: single digit
        return n
    return n % 10 + sum_digits(n // 10)

print(sum_digits(123))
print(sum_digits(9875))
```

**Output:**
```text
6
29
```

## 20. Reverse a String (Recursive)

Take the first character and append it *after* the reverse of the rest.

```python
def reverse(s):
    if len(s) <= 1:        # base case
        return s
    return reverse(s[1:]) + s[0]

print(reverse("python"))
print(reverse("MADAM"))
```

**Output:**
```text
nohtyp
MADAM
```

## 21. Power Function (Recursive)

Compute `x ** n` using `x**n = x * x**(n-1)`, with `x**0 = 1`.

```python
def power(x, n):
    if n == 0:            # base case
        return 1
    return x * power(x, n - 1)

print(power(2, 5))    # 32
print(power(3, 3))    # 27
```

**Output:**
```text
32
27
```

## 22. Recursion vs Iteration

| Aspect | Recursion | Iteration (loops) |
|---|---|---|
| Readability | Elegant for naturally-recursive problems | Straightforward for counting/accumulating |
| Memory | Uses the call stack (extra memory per call) | Constant extra memory |
| Speed | Usually slower (call overhead) | Usually faster |
| Risk | `RecursionError` if too deep | Safe for large inputs |
| Best for | Trees, divide-and-conquer, backtracking | Simple repetition |

**Key Notes:**
- Anything recursive can be rewritten iteratively (and vice-versa).
- Choose recursion when it makes the code **clearer**, iteration when you need **speed/scale**.

## 23. Decorators (Bonus / Advanced)

A **decorator** is a function that *wraps* another function to add behaviour **without changing
its code**. It works because functions are first-class (Section 2). The `@name` syntax above a
function applies the decorator.

**Syntax**
```python
@decorator_name
def some_function():
    ...
```

*This is a gentle intro — decorators are covered in depth later.*

```python
# A simple decorator that announces calls
def announce(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}...")
        result = func(*args, **kwargs)
        print(f"Done with {func.__name__}.")
        return result
    return wrapper

@announce                 # same as: greet = announce(greet)
def greet(name):
    return f"Hello, {name}!"

print(greet("Ravi"))
```

**Output:**
```text
Calling greet...
Done with greet.
Hello, Ravi!
```

## 24. Mini DSA Examples

Small problems that combine today's tools. Each is self-contained and printed.

```python
# 1) Squares of a list using map
nums = [1, 2, 3, 4, 5]
print(list(map(lambda x: x * x, nums)))
```

**Output:**
```text
[1, 4, 9, 16, 25]
```

```python
# 2) Filter prime numbers
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

print(list(filter(is_prime, range(2, 20))))
```

**Output:**
```text
[2, 3, 5, 7, 11, 13, 17, 19]
```

```python
# 3) Sum of a list using reduce
from functools import reduce
print(reduce(lambda acc, x: acc + x, [10, 20, 30, 40]))
```

**Output:**
```text
100
```

```python
# 4) GCD (Greatest Common Divisor) using recursion (Euclid's algorithm)
def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)

print(gcd(48, 18))   # 6
```

**Output:**
```text
6
```

```python
# 5) Count occurrences of a target in a list using recursion
def count(lst, target):
    if not lst:                       # base case: empty list
        return 0
    first = 1 if lst[0] == target else 0
    return first + count(lst[1:], target)

print(count([1, 2, 2, 3, 2, 4], 2))   # 3
```

**Output:**
```text
3
```

```python
# 6) Word frequency using map/zip-style tools
sentence = "the cat sat on the mat the cat"
words = sentence.split()
freq = {w: words.count(w) for w in set(words)}
# Most frequent word using max with key
print(freq)
print("most common:", max(freq, key=freq.get))
```

**Output:**
```text
{'sat': 1, 'on': 1, 'mat': 1, 'cat': 2, 'the': 3}
most common: the
```

## 25. Common Mistakes

**1. Missing base case (infinite recursion)**
```python
# WRONG - never stops, raises RecursionError
def bad(n):
    return n + bad(n - 1)      # no base case!

# RIGHT
def good(n):
    if n == 0:                 # base case
        return 0
    return n + good(n - 1)
```

**2. Forgetting `list()` around `map` / `filter`**
```python
# WRONG - prints a map object, not the values
print(map(lambda x: x*2, [1, 2, 3]))   # <map object at 0x...>
# RIGHT
print(list(map(lambda x: x*2, [1, 2, 3])))   # [2, 4, 6]
```

**3. Overusing lambda for complex logic** — if it needs multiple steps or a docstring, use `def`.

**4. Mutating a list while iterating over it** — build a new list (via `filter`/comprehension)
instead of deleting items mid-loop.

**5. Consuming a `map`/`filter` iterator twice** — it is empty after the first pass; store it in
a `list` if you need it again.

```python
# Demonstrating fixes (all correct versions run cleanly)
def good(n):
    if n == 0:
        return 0
    return n + good(n - 1)
print(good(5))                              # 15

print(list(map(lambda x: x * 2, [1, 2, 3])))  # [2, 4, 6]

nums = [1, 2, 3, 4, 5, 6]
print(list(filter(lambda x: x % 2 == 0, nums)))  # build new list, no mutation
```

**Output:**
```text
15
[2, 4, 6]
[2, 4, 6]
```

## 26. Summary

- **Functions are first-class objects** — store, pass and return them.
- **Lambda** = anonymous one-expression function; great as a `key=` or inside `map`/`filter`.
- **`map`** transforms every item, **`filter`** keeps items passing a test, **`reduce`** folds to one value.
- **`zip`** pairs iterables, **`enumerate`** gives index+value, **`sorted`** returns a new ordered list.
- Built-ins **`any/all/abs/round/sum/max/min`** replace many manual loops.
- **Recursion** needs a **base case** + a **recursive case**; watch the **call stack** and depth.
- Prefer **iteration** for speed/scale, **recursion** for naturally-recursive problems.

## 27. Practice Questions

1. Use `map()` to convert a list of Celsius temperatures to Fahrenheit.
2. Use `filter()` to keep only words longer than 4 letters from a list.
3. Use `reduce()` to find the product of all numbers in a list.
4. Write a lambda that returns the last digit of a number, and apply it with `map()`.
5. Given two lists (names, marks), build a dictionary using `zip()`.
6. Sort a list of `(name, age)` tuples by age using `sorted(key=...)`.
7. Write a recursive function to compute the factorial of `n`.
8. Write a recursive function to find the sum of a list of numbers.
9. Write a recursive function to check whether a string is a palindrome.
10. Write a recursive function for the n-th Fibonacci number, then speed it up with memoization.
