# Day 2 - Python Basics

## Topics
- Variables
- Variable Naming Rules
- Keywords
- Comments
- Input & Output
- Data Types
- Type Conversion
- Operators
- Practice Questions

## 1. Revision
- What is Programming?
- Compiled vs Interpreted?
- Python Execution Flow
- Python Virtual Machine (PVM)
- Virtual Environment

## 2. Variables
A variable is a named memory location used to store data.

```python
name="Satya"
age=22
height=5.8
print(name,age,height)
```

## 3. Variable Naming Rules

Valid: student_name, age2, _marks, totalAmount

Invalid: 2age, student-name, class

```python
student_name="Ram"
age2=20
_marks=95
totalAmount=100
```

## 4. Python Keywords

```python
import keyword
print(keyword.kwlist)
print(len(keyword.kwlist))
```

**Output:**
```text
['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield']
35
```

## 5. Comments

```python
# Single-line comment

"""
Multi-line comment
"""
```

---
---
---

## 6. Input and Output

```python
name=input("Enter your name: ")
print(name)
print(type(name))
```

### Input in Python

**Why?**
`input()` is used to take input from the user. By default, it always returns a **string (`str`)**.


### 1. Take String Input

```python
name = input("Enter your name: ")

print(name)
print(type(name))
```



### 2. Take Integer Input

```python
age = int(input("Enter your age: "))

print(age)
print(type(age))
```



### 3. Take Float Input

```python
height = float(input("Enter your height: "))

print(height)
print(type(height))
```



### 4. Remove Extra Spaces (`strip()`)

```python
name = input("Enter your name: ").strip()

print(name)
```

**Example**

```
Input :    Satya
Output: Satya
```



### 5. Take Multiple Values in a List

```python
numbers = list(map(int, input("Enter numbers: ").split()))

print(numbers)
```

**Input**

```text
10 20 30 40
```

**Output**

```text
[10, 20, 30, 40]
```



### Bonus: Take Multiple Variables

```python
a, b = map(int, input("Enter two numbers: ").split())

print(a)
print(b)
```

**Input**

```text
10 20
```

**Output**

```text
10
20
```

These are the most commonly used input patterns in Python.

## 7. Data Types

---
---
---

# Data Types in Python

## What is a Data Type?

A **data type** specifies:

* What kind of value is stored.
* What operations can be performed on it.
* How Python treats that value in memory.

**Example**

* `25` → Integer
* `"Python"` → String
* `True` → Boolean



## Why Do We Need Data Types?

Different data types support different operations.

```python
age = 22
print(age + 10)
```

**Output**

```text
32
```

```python
name = "Satya"
print(name + 10)
```

**Output**

```text
TypeError
```

Python does not allow operations between incompatible data types.



## Built-in Data Types

| Category | Data Types                |
| -------- | ------------------------- |
| Numeric  | `int`, `float`, `complex` |
| Boolean  | `bool`                    |
| Text     | `str`                     |
| Sequence | `list`, `tuple`, `range`  |
| Set      | `set`                     |
| Mapping  | `dict`                    |
| Special  | `NoneType`                |


## Integer (`int`)

Stores whole numbers.

```python
x = 10
print(type(x))
```

**Output**

```text
<class 'int'>
```


## Float (`float`)

Stores decimal numbers.

```python
price = 99.99
print(type(price))
```

**Output**

```text
<class 'float'>
```



## Complex (`complex`)

Stores numbers with a real and imaginary part.

```python
z = 2 + 3j

print(z.real)
print(z.imag)
print(type(z))
```



## Boolean (`bool`)

Stores only two values:

* `True`
* `False`

```python
is_student = True

print(type(is_student))
```



## String (`str`)

Stores text.

```python
name = "Python"

print(type(name))
print(len(name))
print(name.upper())
print(name.lower())
```


## List (`list`)

An **ordered, mutable** collection.

```python
numbers = [10, 20, 30]

numbers.append(40)

print(numbers)
```



## Tuple (`tuple`)

An **ordered, immutable** collection.

```python
marks = (95, 90, 80)

print(type(marks))
```



## Set (`set`)

Stores **unique** values.

```python
items = {1, 2, 3, 2, 1}

print(items)
```

**Output**

```text
{1, 2, 3}
```



## Dictionary (`dict`)

Stores data as **key-value pairs**.

```python
student = {
    "name": "Satya",
    "age": 22
}

print(student["name"])
```



## NoneType

Represents the absence of a value.

```python
x = None

print(type(x))
```

**Output**

```text
<class 'NoneType'>
```



## Data Type vs Data Structure

| Data Type                            | Data Structure                           |
| ------------------------------------ | ---------------------------------------- |
| Defines what kind of data is stored. | Defines how data is organized in memory. |
| Example: `int`, `str`, `list`        | Example: List, Stack, Queue, Tree        |

**Note:** In Python, `list` is both a built-in **data type** and a commonly used **data structure**.



## Memory Representation

Every object in Python has:

* **Value** → Actual data
* **Type** → Data type
* **ID** → Unique object identifier (memory reference)

```text
Variable
   │
   ▼
Reference
   │
   ▼
Object
 ├── Value
 ├── Type
 └── ID
```

**Example**

```python
a = 10

print(a)
print(type(a))
print(id(a))
```

**Functions**

* `type(obj)` → Returns the data type.
* `id(obj)` → Returns the object's unique identifier.
* `value` → The actual stored data (e.g., `10`).
---
---
---

## 8. Type Conversion

---
---
---

````markdown
# Type Conversion in Python

## Why?

Type conversion changes a value from one data type to another so it can be processed correctly.

## Built-in Type Conversion Functions

```python
int(x)      # Convert to integer
float(x)    # Convert to float
str(x)      # Convert to string
bool(x)     # Convert to boolean
````

## Number Conversion Functions

> `math` is a built-in module. No installation is required.

```python
from math import floor, ceil
```

```python
round(x)    # Round to the nearest integer
floor(x)    # Round down
ceil(x)     # Round up
```

## Example

```python
from math import floor, ceil

x = 10.7

print(int(x))      # 10
print(float(5))    # 5.0
print(str(100))    # '100'
print(bool(1))     # True

print(round(x))    # 11
print(floor(x))    # 10
print(ceil(x))     # 11
```

## Output

```text
10
5.0
100
True
11
10
11
```

```

This is short, neat, and covers both **type conversion** (`int`, `float`, `str`, `bool`) and **rounding functions** (`round`, `floor`, `ceil`).
```
---
---
---

## 9. Operators

---
---
---

# Operators in Python

## What are Operators?

Operators are special symbols used to perform operations on variables and values.

## Why?

Operators help us:
- Perform calculations
- Compare values
- Combine conditions
- Assign values
- Check object identity

## Types of Operators

| Operator Type | Purpose |
|--------------|---------|
| Arithmetic | Mathematical calculations |
| Comparison | Compare two values |
| Logical | Combine conditions |
| Assignment | Assign or update values |
| Identity | Check whether two variables refer to the same object |

---

## 1. Arithmetic Operators

Used to perform mathematical operations.

```python
a = 10
b = 3

print("Addition       :", a + b)
print("Subtraction    :", a - b)
print("Multiplication :", a * b)
print("Division       :", a / b)
print("Modulus        :", a % b)
print("Floor Division :", a // b)
print("Exponent       :", a ** b)
```

**Output**

```text
Addition       : 13
Subtraction    : 7
Multiplication : 30
Division       : 3.3333333333333335
Modulus        : 1
Floor Division : 3
Exponent       : 1000
```

---

## 2. Comparison Operators

Used to compare two values. The result is always `True` or `False`.

```python
a = 10
b = 20

print("a == b :", a == b)
print("a != b :", a != b)
print("a < b  :", a < b)
print("a > b  :", a > b)
print("a <= b :", a <= b)
print("a >= b :", a >= b)
```

**Output**

```text
a == b : False
a != b : True
a < b  : True
a > b  : False
a <= b : True
a >= b : False
```

---

## 3. Logical Operators

Used to combine multiple conditions.

```python
x = True
y = False

print("x and y :", x and y)
print("x or y  :", x or y)
print("not x   :", not x)
```

**Output**

```text
x and y : False
x or y  : True
not x   : False
```

---

## 4. Assignment Operators

Used to assign or update values.

```python
a = 10

a += 5
print("+= :", a)

a -= 3
print("-= :", a)

a *= 2
print("*= :", a)
```

**Output**

```text
+= : 15
-= : 12
*= : 24
```

---

## 5. Identity Operators

Used to check whether two variables refer to the same object in memory.

```python
a = [10, 20]
b = a
c = [10, 20]

print("a is b     :", a is b)
print("a is c     :", a is c)
print("a is not c :", a is not c)
```

**Output**

```text
a is b     : True
a is c     : False
a is not c : True
```

---
---
---

````markdown
# Strings & Escape Characters

## 0. Print with Variables (f-string)

An **f-string** lets you insert variables directly into a string using `{}`.

```python
language = "Python"
year = 1991
version = 3.14

print(f"{language} was released in {year} and its latest version is {version}.")
```

**Output**

```text
Python was released in 1991 and its latest version is 3.14.
```

---

## 1. Backslash (`\\`)

```python
print("This is a backslash: \\")
```

**Output**

```text
This is a backslash: \
```

---

## 2. Single Quote (`\'`)

```python
print('It\'s alright.')
```

**Output**

```text
It's alright.
```

---

## 3. Tab (`\t`)

```python
print("Hello\tWorld")
```

**Output**

```text
Hello    World
```

---

## 4. ASCII Character (`chr()`)

`chr()` converts an ASCII/Unicode value into its corresponding character.

```python
print(chr(72) + chr(101) + chr(108) + chr(108) + chr(111))
```

**Output**

```text
Hello
```
````

---
---
---

````markdown id="m4x8kp"
## Practice Questions

### 1. Student Information

Take the following inputs:

- Name
- Age
- College
- CGPA

Print all the details using an **f-string**.

**Example Output**

```text
My name is Satya. I am 22 years old, studying at ABC College, and my CGPA is 9.15.
```

---

### 2. Employee Details

Take the following inputs:

- Employee Name
- Employee ID
- Department
- Salary

Print the details in a neatly formatted sentence using an **f-string**.

---

### 3. Type Conversion

Take a decimal number as input and display its:

- `int()`
- `float()`
- `str()`
- `bool()`
- `round()`
- `floor()`
- `ceil()`

---

### 4. Diamond Pattern

Print the following pattern:

```text
    *
   ***
  *****
 *******
*********
 *******
  *****
   ***
    *
```

---

### 5. Inverted Right Half Pyramid

Print the following pattern:

```text
*****
 ****
  ***
   **
    *
```
````
