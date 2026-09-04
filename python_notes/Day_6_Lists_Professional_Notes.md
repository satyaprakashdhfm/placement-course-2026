# Day 6 – Lists

**Duration:** 55–60 Minutes

**Learning Outcomes**
- Understand the List data structure.
- Learn indexing and slicing.
- Learn common list methods.
- Solve beginner DSA problems using lists.

## What is a List?

A **List** is an ordered collection of elements. A list can store values of the same or different data types and allows you to add, modify, remove, and access elements easily.

Lists are one of the most commonly used data structures in Python and are widely used in DSA.

### Characteristics

- **Ordered** – Elements are stored in a fixed order.
- **Mutable** – Elements can be modified after the list is created.
- **Iterable** – Elements can be accessed one by one using loops.
- **Supports Indexing** – Individual elements can be accessed using an index.
- **Supports Slicing** – A portion of the list can be extracted.
- **Allows Duplicates** – Duplicate values are allowed.
- **Heterogeneous** – Can store different data types in the same list.

## Creating Lists

```python
# Creating lists

numbers = [10, 20, 30]
names = ["Alice", "Bob"]
mixed = [10, "Python", 3.14, True]

# Create using list()
values = list((1, 2, 3))

print(numbers)
print(names)
print(mixed)
print(values)
```

**Output:**
```text
[10, 20, 30]
['Alice', 'Bob']
[10, 'Python', 3.14, True]
[1, 2, 3]
```

## Indexing

```
List  : [10, 20, 30, 40, 50]
Index :  0   1   2   3   4
NegIdx:-5  -4  -3  -2  -1
```

```python
numbers = [10,20,30,40,50]

# Positive indexing
print(numbers[0])
print(numbers[3])

# Negative indexing
print(numbers[-1])
print(numbers[-2])
```

**Output:**
```text
10
40
50
40
```

## Slicing

```python
numbers = [10,20,30,40,50,60]

print(numbers[:])
print(numbers[:3])
print(numbers[2:5])
print(numbers[3:])
print(numbers[::2])
print(numbers[::-1])
```

**Output:**
```text
[10, 20, 30, 40, 50, 60]
[10, 20, 30]
[30, 40, 50]
[40, 50, 60]
[10, 30, 50]
[60, 50, 40, 30, 20, 10]
```

## Mutability

Lists are **mutable**, which means their elements can be changed after the list is created.
Unlike strings, the original list is modified directly.

```python
numbers = [10,20,30]

# Modify an element
numbers[1] = 100

print(numbers)
```

**Output:**
```text
[10, 100, 30]
```

## Iterating Through a List

```python
fruits = ["Apple","Banana","Orange"]

# Using for loop
for fruit in fruits:
    print(fruit)
```

**Output:**
```text
Apple
Banana
Orange
```

```python
fruits = ["Apple","Banana","Orange"]

# Using while loop
i = 0
while i < len(fruits):
    print(fruits[i])
    i += 1
```

**Output:**
```text
Apple
Banana
Orange
```

## Membership Operators

```python
fruits = ["Apple","Banana","Orange"]

print("Apple" in fruits)
print("Mango" not in fruits)
```

**Output:**
```text
True
True
```

## Useful Built-in Functions

These functions work with lists and return useful information without modifying the original list (except `sorted()` returns a new sorted list).

**Functions:** `len()`, `min()`, `max()`, `sum()`, `sorted()`

**Input:** `list`

**Output:** Returns `int`, `float`, or `list` depending on the function.

```python
numbers = [8,3,6,1,9]

print(len(numbers))
print(min(numbers))
print(max(numbers))
print(sum(numbers))
print(sorted(numbers))
```

**Output:**
```text
5
1
9
27
[1, 3, 6, 8, 9]
```

## Insertion Methods

These methods are used to add one or more elements to a list.

**Functions:** `append()`, `extend()`, `insert()`

**Input:** `append(item)`, `extend(iterable)`, `insert(index, item)`.

**Output:** `None` → Modifies the original list.

```python
# Original list
fruits = ["Apple", "Banana"]

# Add one item
fruits.append("Orange")

# Add multiple items
fruits.extend(["Mango", "Grapes"])

# Insert at a specific position
fruits.insert(1, "Kiwi")

print(fruits)
```

**Output:**
```text
['Apple', 'Kiwi', 'Banana', 'Orange', 'Mango', 'Grapes']
```

## Deletion Methods

These methods are used to remove elements from a list.

**Functions:** `remove()`, `pop()`, `clear()`

**Input:** `remove(item)`, `pop(index=None)`, `clear()`.

**Output:** `remove()` and `clear()` → `None`, `pop()` → Returns removed element.

```python
numbers = [10,20,30,40]

numbers.remove(20)
print(numbers)

removed = numbers.pop()
print(removed)
print(numbers)

numbers.clear()
print(numbers)
```

**Output:**
```text
[10, 30, 40]
40
[10, 30]
[]
```

## Searching Methods

These methods help find elements and count their occurrences.

**Functions:** `index()`, `count()`

**Input:** `item (Any)`.

**Output:** `index()` → `int`, `count()` → `int`.

```python
numbers = [10,20,30,20,20]

print(numbers.index(30))
print(numbers.count(20))
```

**Output:**
```text
2
3
```

## Ordering Methods

These methods arrange or reverse the elements in a list.

**Functions:** `sort()`, `reverse()`

**Input:** `sort(reverse=False)`, `reverse()`.

**Output:** `None` → Modifies the original list.

```python
numbers = [8,2,5,1]

numbers.sort()
print(numbers)

numbers.reverse()
print(numbers)
```

**Output:**
```text
[1, 2, 5, 8]
[8, 5, 2, 1]
```

## Copy Method

This method creates a shallow copy of a list.

**Functions:** `copy()`

**Input:** None.

**Output:** `list` → Returns a new list.

```python
a = [1,2,3]

b = a.copy()

b.append(4)

print(a)
print(b)
```

**Output:**
```text
[1, 2, 3]
[1, 2, 3, 4]
```

## Nested Lists

```python
matrix = [
    [1,2,3],
    [4,5,6],
    [7,8,9]
]

print(matrix)
print(matrix[1][2])
```

**Output:**
```text
[[1, 2, 3], [4, 5, 6], [7, 8, 9]]
6
```

## Mini DSA Examples

```python
# Find the largest element
numbers = [12,45,8,90]
print(max(numbers))

# Count even numbers
count = 0
for num in numbers:
    if num % 2 == 0:
        count += 1
print(count)

# Reverse a list
print(numbers[::-1])

# Linear Search
target = 45
print(target in numbers)
```

**Output:**
```text
90
3
[90, 8, 45, 12]
True
```

## Practice Questions

1. Find the largest element in a list.
2. Count even and odd numbers in a list.
3. Reverse a list without using `reverse()`.
4. Remove duplicate elements from a list.
5. Search for a given element using a loop.
