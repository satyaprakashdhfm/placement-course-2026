# Day 5 – Data Structures Introduction & Strings

**Duration:** 55–60 Minutes

## What is Data?

Data is a collection of raw facts such as names, marks, phone numbers, addresses, prices, etc.

## What is a Data Structure?

A **Data Structure** is a way of storing and organizing data so that it can be accessed, modified and processed efficiently.

### Common Python Data Structures
- String
- List
- Tuple
- Set
- Dictionary

In this lesson we will study **Strings**, one of the most important data structures used in Python and DSA.

## What is a String?

A **String** is a sequence of one or more characters enclosed in single quotes (`' '`), double quotes (`" "`) or triple quotes (`''' '''`).

### Characteristics

- **Ordered** – Elements are stored in a fixed order and can be accessed using their index.
- **Immutable** – The contents of a string cannot be changed after it is created.
- **Iterable** – Each character can be accessed one by one using loops like `for` or `while`.
- **Supports Indexing** – Individual characters can be accessed using positive or negative indices.
- **Supports Slicing** – A part of the string can be extracted using slicing (`start:end:step`).
- **Hashable** – Strings have a fixed hash value, so they can be used as dictionary keys and set elements.

```python
# Creating strings

name = "Python"
city = 'Bengaluru'
message = '''Welcome to Python'''

print(name)
print(city)
print(message)

# Convert an integer to a string
print(str(100))
```

**Output:**
```text
Python
Bengaluru
Welcome to Python
100
```

## Indexing

```
String :  P  y  t  h  o  n
Index  :  0  1  2  3  4  5
NegIdx : -6 -5 -4 -3 -2 -1
```

```python
text = "Python"

# Positive indexing
print(text[0])
print(text[3])

# Negative indexing
print(text[-1])
print(text[-3])
```

**Output:**
```text
P
h
n
h
```

## Slicing

```python
text = "Programming"

print(text[:])
print(text[:6])
print(text[3:8])
print(text[5:])
print(text[::2])
print(text[::-1])
```

**Output:**
```text
Programming
Progra
gramm
amming
Pormig
gnimmargorP
```

## Immutability

Strings are **immutable**, which means their characters cannot be changed after the string is created.

Whenever a string is modified, Python creates a **new string object** instead of changing the original one.

```python
text = "Python"

# text[0] = "J"   # This will produce an error

# Create a new string instead
new_text = "J" + text[1:]

print(text)
print(new_text)
```

**Output:**
```text
Python
Jython
```

## Hashable

Strings are **hashable** because they are immutable.

This allows strings to be used as dictionary keys.

```python
student = {
    "Alice": 90,
    "Bob": 85
}

print(student["Alice"])
```

**Output:**
```text
90
```

# looping through

```python
text="Python"

for ch in text:
    print(ch)

i=0
while i<len(text):
    print(text[i])
    i+=1
```

**Output:**
```text
P
y
t
h
o
n
P
y
t
h
o
n
```

## Conversion Method

Conversion methods are used to convert other Python objects into strings.

Functions: `str()`

**Input:** `object (Any)` → Object to convert.

**Output:** `str` → Returns the string representation of the object.

```python
# Integer to string
number = 123

text = str(number)

print(text)
print(type(text))
```

**Output:**
```text
123
<class 'str'>
```

## Case Conversion Methods

These methods change the letter case of a string. They do not modify the original string because strings are immutable.

Functions: `upper()`, `lower()`, `capitalize()`, `title()`, `casefold()`

**Input:** None

**Output:** `str` → Returns a new string with the requested case conversion.

```python
text = "python programming"

print(text.upper())
print(text.lower())
print(text.capitalize())
print(text.title())
print(text.casefold())
```

**Output:**
```text
PYTHON PROGRAMMING
python programming
Python programming
Python Programming
python programming
```

## Search Methods

These methods search for a substring inside a string and return its position.

Functions: `find()`, `index()`

**Input:** `substring (str)`, `start (int, Optional)`, `end (int, Optional)`

**Output:** `int` → Returns the position of the substring.

```python
text = "Python Programming"

print(text.find("Program"))
print(text.find("Java"))
print(text.index("Python"))
```

**Output:**
```text
7
-1
0
```

## Replace Method

This method replaces one substring with another and returns a new string.

Functions: `replace()`

**Input:** `old (str)`, `new (str)`, `count (int, Optional)`

**Output:** `str` → Returns a new modified string.

```python
text = "I like Java"

print(text.replace("Java", "Python"))
print(text.replace("a", "@"))
```

**Output:**
```text
I like Python
I like J@v@
```

## Whitespace Removal Methods

These methods remove unwanted spaces or characters from the beginning, end or both sides of a string.

Functions: `strip()`, `lstrip()`, `rstrip()`

**Input:** `chars (str, Optional)`

**Output:** `str` → Returns a trimmed string.

```python
text = "   Python   "

print(text.strip())
print(text.lstrip())
print(text.rstrip())
```

**Output:**
```text
Python
Python   
   Python
```

## Split & Join Methods

These methods convert strings into lists or combine multiple strings into one.

Functions: `split()`, `splitlines()`, `join()`

**Input:** `separator (str, Optional)`, `maxsplit (int, Optional)`, `iterable (Iterable[str])`

**Output:** `split()` → `list[str]`, `splitlines()` → `list[str]`, `join()` → `str`.

```python
text = "Apple,Banana,Orange"
print(text.split(","))

lines = "A\nB\nC"
print(lines.splitlines())

items = ["Apple","Banana","Orange"]
print(" - ".join(items))
```

**Output:**
```text
['Apple', 'Banana', 'Orange']
['A', 'B', 'C']
Apple - Banana - Orange
```

## String Checking Methods

These methods check whether a string satisfies a particular condition and return either True or False.

Functions: `isalpha()`, `isdigit()`, `isalnum()`, `islower()`, `isupper()`, `isspace()`, `istitle()`

**Input:** None

**Output:** `bool` → Returns `True` or `False`.

```python
print("Python".isalpha())
print("12345".isdigit())
print("Python123".isalnum())
print("python".islower())
print("PYTHON".isupper())
print("   ".isspace())
print("Hello World".istitle())
```

**Output:**
```text
True
True
True
True
True
True
True
```

## Mini DSA Examples

```python
# Reverse a string
text = "Python"
print(text[::-1])

# Check palindrome
word = "madam"
print(word == word[::-1])

# Count vowels
count = 0
for ch in "education":
    if ch in "aeiou":
        count += 1
print(count)

# Count frequency of a character
print("banana".count("a"))
```

**Output:**
```text
nohtyP
True
5
3
```

## Practice Questions

1. Count the number of vowels in a string.
2. Reverse a string using slicing.
3. Check whether a string is a palindrome.
4. Count uppercase, lowercase, digits and special characters.
5. Find the frequency of a given character in a string.
