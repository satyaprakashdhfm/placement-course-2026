# Day 7 – Tuples & Sets

**Duration:** 55–60 Minutes

# Part 1 – Tuple

## What is a Tuple?

A **Tuple** is an ordered collection of elements. Unlike a list, its elements cannot be modified after creation.

### Characteristics
- **Ordered** – Elements are stored in a fixed order.
- **Immutable** – Elements cannot be modified.
- **Iterable** – Can be traversed using loops.
- **Supports Indexing** – Access elements using indexes.
- **Supports Slicing** – Extract a portion of the tuple.
- **Allows Duplicates** – Duplicate values are allowed.
- **Hashable** – Tuples containing only immutable values can be dictionary keys.

```python
# Creating tuples
numbers=(10,20,30)
names=("Alice","Bob")
single=(100,)
empty=tuple()
print(numbers,names,single,empty)

# Indexing & Slicing
print(numbers[0],numbers[-1])
print(numbers[:2],numbers[::-1])

# Tuples are immutable
# numbers[0]=99  # Error

for item in numbers:
    print(item)
```

**Output:**
```text
(10, 20, 30) ('Alice', 'Bob') (100,) ()
10 30
(10, 20) (30, 20, 10)
10
20
30
```

## Tuple Searching Methods

These methods search for elements inside a tuple.

**Functions:** `count()`, `index()`

**Input:** `item (Any)`, `start (int, Optional)`, `end (int, Optional)`

**Output:** `count()` → `int`, `index()` → `int`

```python
values=(10,20,30,20,20)

# Count occurrences
print(values.count(20))

# Find first occurrence
print(values.index(30))
```

**Output:**
```text
3
2
```

# Part 2 – Set

## What is a Set?

A **Set** is an unordered collection of unique elements. It automatically removes duplicate values and is useful for mathematical set operations.

### Characteristics
- **Unordered** – Elements do not have a fixed order.
- **Mutable** – Elements can be added or removed.
- **Unindexed** – Indexing and slicing are not supported.
- **Unique** – Duplicate values are automatically removed.
- **Iterable** – Can be traversed using loops.
- **Not Hashable** – Cannot be used as a dictionary key.

```python
# Creating sets
numbers={10,20,30}
duplicates={1,2,2,3}
empty=set()

print(numbers)
print(duplicates)
print(empty)

for item in numbers:
    print(item)
```

**Output:**
```text
{10, 20, 30}
{1, 2, 3}
set()
10
20
30
```

## Insertion Method

These methods are used for insertion method.

**Functions:** `add()`

**Input:** element (Any)

**Output:** None → Modifies the original set.

```python
fruits={"Apple","Banana"}
fruits.add("Orange")
print(fruits)
```

**Output:**
```text
{'Banana', 'Apple', 'Orange'}
```

## Deletion Methods

These methods are used for deletion methods.

**Functions:** `remove(), discard(), pop(), clear()`

**Input:** element (Any)

**Output:** remove/discard/clear → None, pop() → Removed element

```python
data={10,20,30,40}
data.remove(20)
data.discard(100)
print(data.pop())
print(data)
data.clear()
print(data)
```

**Output:**
```text
40
{10, 30}
set()
```

## Copy Method

These methods are used for copy method.

**Functions:** `copy()`

**Input:** None

**Output:** set → Returns a new set.

```python
a={1,2,3}
b=a.copy()
b.add(4)
print(a)
print(b)
```

**Output:**
```text
{1, 2, 3}
{1, 2, 3, 4}
```

## Relationship Methods

These methods are used for relationship methods.

**Functions:** `isdisjoint(), issubset(), issuperset()`

**Input:** other (set)

**Output:** bool → Returns True or False.

```python
A={1,2}
B={1,2,3}
C={5,6}
print(A.issubset(B))
print(B.issuperset(A))
print(A.isdisjoint(C))
```

**Output:**
```text
True
True
True
```

## Intersection Method

These methods are used for intersection method.

**Functions:** `intersection()`

**Input:** other (set or iterable)

**Output:** set → Returns common elements.

```python
A={1,2,3,4}
B={3,4,5}
print(A.intersection(B))
```

**Output:**
```text
{3, 4}
```

## Mini DSA Examples

```python
# Remove duplicates
nums=[1,2,2,3,4,4]
print(set(nums))

# Common elements
A={10,20,30}
B={20,30,40}
print(A.intersection(B))

# Tuple unpacking
point=(5,10)
x,y=point
print(x,y)
```

**Output:**
```text
{1, 2, 3, 4}
{20, 30}
5 10
```

## Practice Questions

1. Count the occurrences of an element in a tuple.
2. Find the index of an element in a tuple.
3. Remove duplicate values from a list using a set.
4. Find the common elements between two sets.
5. Check whether one set is a subset of another.
