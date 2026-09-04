# Day 8 – Dictionaries

**Duration:** 50–60 Minutes

### Learning Outcomes
- Understand the Dictionary data structure.
- Create, access, update and delete dictionary elements.
- Learn commonly used dictionary methods.
- Solve simple DSA-style problems using dictionaries.

## 1. What is a Dictionary?

A **Dictionary** is a collection of **key-value pairs**. Each key is unique and is used to access its corresponding value.

Dictionaries are one of the fastest data structures in Python because they use **hashing** for quick lookups.

### Real-Life Examples
- Student → Marks
- Product → Price
- Employee → Salary

### Characteristics

- **Key-Value Pair** – Every item consists of a key and its value.
- **Ordered** – Items maintain insertion order (Python 3.7+).
- **Mutable** – Keys and values can be added, updated or removed.
- **Unique Keys** – Duplicate keys are not allowed.
- **Duplicate Values** – Multiple keys can have the same value.
- **Hash-Based** – Provides fast searching using keys.
- **Iterable** – Can be traversed using loops.
- **Dynamic Size** – Can grow or shrink during execution.

## 2. Dictionary Structure

```text
student = {
    "name": "Alice",
    "age": 20,
    "marks": 95
}

+---------+---------+
| Key     | Value   |
+---------+---------+
| name    | Alice   |
| age     | 20      |
| marks   | 95      |
+---------+---------+
```

## 3. Creating Dictionaries

```python
# Empty dictionary
student = {}

# Using {}
employee = {
    "id": 101,
    "name": "Alice",
    "salary": 50000
}

# Using dict()
marks = dict(Math=90, Science=85)

# Nested dictionary
college = {
    "student": {
        "name": "Bob",
        "age": 21
    }
}

print(employee)
print(marks)
print(college)
```

**Output:**
```text
{'id': 101, 'name': 'Alice', 'salary': 50000}
{'Math': 90, 'Science': 85}
{'student': {'name': 'Bob', 'age': 21}}
```

## 4. Accessing Values

Values can be accessed using the key.

- `[]` raises **KeyError** if the key is missing.
- `get()` returns a default value instead of an error.

```python
student = {
    "name": "Alice",
    "age": 20
}

print(student["name"])
print(student.get("age"))
print(student.get("marks", "Not Available"))
```

**Output:**
```text
Alice
20
Not Available
```

## 5. Adding & Updating Elements

```python
student = {"name":"Alice"}

# Add a new key
student["age"] = 20

# Update an existing key
student["age"] = 21

print(student)
```

**Output:**
```text
{'name': 'Alice', 'age': 21}
```

## 6. Iterating Through a Dictionary

```python
student = {
    "name":"Alice",
    "age":20,
    "city":"Bengaluru"
}

# Iterate over keys
for key in student:
    print(key)

# Iterate over key-value pairs
for key, value in student.items():
    print(key, ":", value)
```

**Output:**
```text
name
age
city
name : Alice
age : 20
city : Bengaluru
```

## Access Methods

These methods are used to access keys, values and key-value pairs from a dictionary.

**Functions:** `get()`, `keys()`, `values()`, `items()`

**Input:** `key (Hashable)`, `default (Any, Optional)`

**Output:** `get()` → Value, `keys()` → `dict_keys`, `values()` → `dict_values`, `items()` → `dict_items`.

```python
student={"name":"Alice","age":20,"city":"Bengaluru"}

print(student.get("name"))
print(student.get("marks","Not Found"))

print(student.keys())
print(student.values())
print(student.items())
```

**Output:**
```text
Alice
Not Found
dict_keys(['name', 'age', 'city'])
dict_values(['Alice', 20, 'Bengaluru'])
dict_items([('name', 'Alice'), ('age', 20), ('city', 'Bengaluru')])
```

## Modification Methods

These methods add new key-value pairs or update existing ones.

**Functions:** `update()`, `setdefault()`

**Input:** Dictionary or key and default value.

**Output:** `update()` → None, `setdefault()` → Value.

```python
student={"name":"Alice","age":20}

student.update({"city":"Bengaluru"})
student.update({"age":21})

print(student)

print(student.setdefault("marks",95))
print(student)
```

**Output:**
```text
{'name': 'Alice', 'age': 21, 'city': 'Bengaluru'}
95
{'name': 'Alice', 'age': 21, 'city': 'Bengaluru', 'marks': 95}
```

## Deletion Methods

These methods remove one or more key-value pairs from a dictionary.

**Functions:** `pop()`, `popitem()`, `clear()`

**Input:** `key (Hashable)`, `default (Optional)`

**Output:** `pop()` → Value, `popitem()` → Tuple, `clear()` → None.

```python
student={"name":"Alice","age":20,"city":"Bengaluru"}

print(student.pop("age"))
print(student)

print(student.popitem())
print(student)

student.clear()
print(student)
```

**Output:**
```text
20
{'name': 'Alice', 'city': 'Bengaluru'}
('city', 'Bengaluru')
{'name': 'Alice'}
{}
```

## Copy Method

This method creates a shallow copy of a dictionary.

**Functions:** `copy()`

**Input:** None

**Output:** `dict` → Returns a new dictionary.

```python
student={"name":"Alice","age":20}

new_student=student.copy()
new_student["age"]=25

print(student)
print(new_student)
```

**Output:**
```text
{'name': 'Alice', 'age': 20}
{'name': 'Alice', 'age': 25}
```

## Creation Method

This method creates a new dictionary using a collection of keys.

**Functions:** `fromkeys()`

**Input:** `iterable`, `value (Optional)`

**Output:** `dict` → Returns a new dictionary.

```python
subjects=["Math","Science","English"]

marks=dict.fromkeys(subjects,0)

print(marks)
```

**Output:**
```text
{'Math': 0, 'Science': 0, 'English': 0}
```

## 7. Nested Dictionary

```python
students={
    101:{"name":"Alice","marks":90},
    102:{"name":"Bob","marks":85}
}

print(students[101]["name"])
print(students[102]["marks"])
```

**Output:**
```text
Alice
85
```

## 8. Dictionary vs List

| Feature | Dictionary | List |
|---|---|---|
| Storage | Key-Value Pair | Values Only |
| Ordered | Yes | Yes |
| Mutable | Yes | Yes |
| Indexing | By Key | By Index |
| Duplicate Keys | No | Yes |

## 9. Mini DSA Examples

```python
# Count frequency of characters
text="banana"
freq={}

for ch in text:
    freq[ch]=freq.get(ch,0)+1

print(freq)

# Student lookup
students={"Alice":90,"Bob":85}
print(students.get("Bob"))

# Merge dictionaries
a={"A":1}
b={"B":2}

a.update(b)
print(a)
```

**Output:**
```text
{'b': 1, 'a': 3, 'n': 2}
85
{'A': 1, 'B': 2}
```

## 10. Summary

- Dictionary stores data as **key-value pairs**.
- Keys must be **unique** and **hashable**.
- Values can be of any data type.
- Dictionaries are mutable.
- Dictionary lookup is very fast using keys.

## Practice Questions

1. Create a dictionary of five students and their marks.
2. Count the frequency of each character in a string.
3. Merge two dictionaries.
4. Find the student with the highest marks.
5. Check whether a key exists in a dictionary.
