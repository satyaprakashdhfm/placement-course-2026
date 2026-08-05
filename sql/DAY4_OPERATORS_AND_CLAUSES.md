# Operators and Clauses in MySQL

In this section, we will learn the operators that make `WHERE` powerful:
`IN`, `BETWEEN`, `LIKE`, `EXISTS`, and how `AND`, `OR` and `NOT` combine.

---

# Why These Operators?

You already know `=`, `>`, `<` from the previous topic. They are enough for
simple conditions, but they become clumsy quickly.

Some important points:

* `IN` replaces a long chain of `OR`.
* `BETWEEN` replaces two conditions joined by `AND`.
* `LIKE` searches for a **pattern** instead of an exact value.
* `EXISTS` checks whether related rows exist in another table.
* Each one makes the query shorter **and** easier to read.

---

# Table Used in This Section

Run this once before starting.

```sql
CREATE DATABASE IF NOT EXISTS training;
USE training;

DROP TABLE IF EXISTS students;

CREATE TABLE students (
    student_id INT PRIMARY KEY,
    name       VARCHAR(50) NOT NULL,
    city       VARCHAR(50),
    age        INT,
    course     VARCHAR(50),
    marks      INT,
    joined_on  DATE
);

INSERT INTO students VALUES
(101,'Rahul Verma','Hyderabad',21,'Python',78,'2025-01-15'),
(102,'Anita Sharma','Chennai',22,'SQL',95,'2025-01-20'),
(103,'Karan Patel','Hyderabad',20,'Python',38,'2025-02-01'),
(104,'Priya Nair','Kochi',23,'Java',66,'2025-02-10'),
(105,'Vikram Rao','Hyderabad',21,'SQL',81,'2025-03-05'),
(106,'Sneha Iyer','Chennai',22,'Java',54,'2025-03-12'),
(107,'Arjun Mehta','Pune',24,'DSA',90,'2025-04-02'),
(108,'Divya Menon','Kochi',20,'Python',45,'2025-04-18'),
(109,'Rohit Sinha','Pune',23,NULL,78,'2025-05-01'),
(110,'Meera Nair','Chennai',21,'DSA',NULL,'2025-05-20');
```

---

# 1. The IN Operator

`IN` checks whether a value matches **any value in a list**.

### Syntax

```sql
SELECT column_list
FROM table_name
WHERE column_name IN (value1, value2, value3);
```

### Example

```sql
SELECT name, course FROM students WHERE course IN ('Python','SQL');
```

### Expected Output

```
+--------------+--------+
| name         | course |
+--------------+--------+
| Rahul Verma  | Python |
| Anita Sharma | SQL    |
| Karan Patel  | Python |
| Vikram Rao   | SQL    |
| Divya Menon  | Python |
+--------------+--------+
```

### The Same Query Without IN

```sql
SELECT name, course FROM students
WHERE course = 'Python' OR course = 'SQL';
```

Both give the same result. `IN` is shorter, and stays readable when the list
grows to ten values.

---

# 2. The NOT IN Operator

`NOT IN` returns rows that match **none** of the values in the list.

### Syntax

```sql
SELECT column_list
FROM table_name
WHERE column_name NOT IN (value1, value2);
```

### Example

```sql
SELECT name, course FROM students WHERE course NOT IN ('Python','SQL');
```

### Expected Output

```
+-------------+--------+
| name        | course |
+-------------+--------+
| Priya Nair  | Java   |
| Sneha Iyer  | Java   |
| Arjun Mehta | DSA    |
| Meera Nair  | DSA    |
+-------------+--------+
```

> **Note:** `Rohit Sinha` is **missing** from this result, even though his course
> is not Python or SQL. His course is `NULL`, and `NULL` can never be compared.
> This is explained again in Common Errors below.

---

# 3. The BETWEEN Operator

`BETWEEN` checks whether a value falls inside a range. Both ends are
**included**.

### Syntax

```sql
SELECT column_list
FROM table_name
WHERE column_name BETWEEN low_value AND high_value;
```

### Example

```sql
SELECT name, age FROM students WHERE age BETWEEN 21 AND 22;
```

### Expected Output

```
+--------------+------+
| name         | age  |
+--------------+------+
| Rahul Verma  |   21 |
| Anita Sharma |   22 |
| Vikram Rao   |   21 |
| Sneha Iyer   |   22 |
| Meera Nair   |   21 |
+--------------+------+
```

Students aged exactly 21 and exactly 22 are both included.

### The Same Query Without BETWEEN

```sql
SELECT name, age FROM students WHERE age >= 21 AND age <= 22;
```

> **Note:** The **smaller** value must come first. `BETWEEN 22 AND 21` returns
> nothing at all.

---

# 4. The NOT BETWEEN Operator

### Example

```sql
SELECT name, marks FROM students WHERE marks NOT BETWEEN 50 AND 90;
```

### Expected Output

```
+--------------+-------+
| name         | marks |
+--------------+-------+
| Anita Sharma |    95 |
| Karan Patel  |    38 |
| Divya Menon  |    45 |
+--------------+-------+
```

Students **outside** the range 50 to 90 — one above it and two below it.

---

# 5. BETWEEN with Dates

`BETWEEN` works on dates in exactly the same way. This is its most common use.

### Example

Students who joined in January or February 2025.

```sql
SELECT name, joined_on FROM students
WHERE joined_on BETWEEN '2025-01-01' AND '2025-02-28';
```

### Expected Output

```
+--------------+------------+
| name         | joined_on  |
+--------------+------------+
| Rahul Verma  | 2025-01-15 |
| Anita Sharma | 2025-01-20 |
| Karan Patel  | 2025-02-01 |
| Priya Nair   | 2025-02-10 |
+--------------+------------+
```

Dates must be written in `'YYYY-MM-DD'` format, inside single quotes.

---

# 6. The LIKE Operator

`LIKE` searches for a **pattern** instead of an exact value.

Two wildcard characters are used:

| Wildcard | Meaning                                    |
| -------- | ------------------------------------------ |
| `%`      | Any number of characters (including none)  |
| `_`      | Exactly one character                      |

### Syntax

```sql
SELECT column_list
FROM table_name
WHERE column_name LIKE 'pattern';
```

---

# 7. LIKE — Starts With

### Example

Names starting with `R`.

```sql
SELECT name FROM students WHERE name LIKE 'R%';
```

### Expected Output

```
+-------------+
| name        |
+-------------+
| Rahul Verma |
| Rohit Sinha |
+-------------+
```

---

# 8. LIKE — Ends With

### Example

Names ending with `Nair`.

```sql
SELECT name FROM students WHERE name LIKE '%Nair';
```

### Expected Output

```
+------------+
| name       |
+------------+
| Priya Nair |
| Meera Nair |
+------------+
```

---

# 9. LIKE — Contains

### Example

Names containing the letter `a` anywhere.

```sql
SELECT name FROM students WHERE name LIKE '%a%' LIMIT 4;
```

### Expected Output

```
+--------------+
| name         |
+--------------+
| Rahul Verma  |
| Anita Sharma |
| Karan Patel  |
| Priya Nair   |
+--------------+
```

---

# 10. LIKE — Using the Underscore

`_` stands for exactly one character. So `'_a%'` means *the second letter is
`a`*.

### Example

```sql
SELECT name FROM students WHERE name LIKE '_a%';
```

### Expected Output

```
+-------------+
| name        |
+-------------+
| Rahul Verma |
| Karan Patel |
+-------------+
```

`R-a-hul` and `K-a-ran` both have `a` as the second letter.

---

# 11. Pattern Reference

| Pattern     | Meaning                              |
| ----------- | ------------------------------------ |
| `'R%'`      | Starts with R                        |
| `'%a'`      | Ends with a                          |
| `'%Nair%'`  | Contains Nair anywhere               |
| `'_a%'`     | Second character is a                |
| `'__a%'`    | Third character is a                 |
| `'R%a'`     | Starts with R and ends with a        |

> **Note:** In MySQL, `LIKE` is **not** case sensitive by default, so `'r%'`
> also finds `Rahul`. Do not rely on this in other databases.

---

# 12. Combining LIKE with OR

### Example

Names starting with `A` or `V`.

```sql
SELECT name FROM students
WHERE name LIKE 'A%' OR name LIKE 'V%';
```

### Expected Output

```
+--------------+
| name         |
+--------------+
| Anita Sharma |
| Vikram Rao   |
| Arjun Mehta  |
+--------------+
```

Both `A` names and the one `V` name are returned. `LIKE` conditions combine with
`AND`, `OR` and `NOT` exactly like any other condition.

---

# 13. The AND Operator

Both conditions must be true.

### Example

```sql
SELECT name, city, marks FROM students
WHERE city = 'Hyderabad' AND marks > 60;
```

### Expected Output

```
+-------------+-----------+-------+
| name        | city      | marks |
+-------------+-----------+-------+
| Rahul Verma | Hyderabad |    78 |
| Vikram Rao  | Hyderabad |    81 |
+-------------+-----------+-------+
```

`Karan Patel` is from Hyderabad but scored 38, so he fails the second condition.

---

# 14. The OR Operator

Any one condition must be true.

### Example

```sql
SELECT name, city FROM students
WHERE city = 'Kochi' OR city = 'Pune';
```

### Expected Output

```
+-------------+-------+
| name        | city  |
+-------------+-------+
| Priya Nair  | Kochi |
| Arjun Mehta | Pune  |
| Divya Menon | Kochi |
| Rohit Sinha | Pune  |
+-------------+-------+
```

---

# 15. Operator Precedence — Use Brackets

`AND` is evaluated **before** `OR`. Forgetting this gives wrong results.

### Wrong

We want: *students from Hyderabad or Kochi who scored above 60.*

```sql
SELECT name, city, marks FROM students
WHERE city = 'Hyderabad' OR city = 'Kochi' AND marks > 60;
```

### Output

```
+-------------+-----------+-------+
| name        | city      | marks |
+-------------+-----------+-------+
| Rahul Verma | Hyderabad |    78 |
| Karan Patel | Hyderabad |    38 |
| Priya Nair  | Kochi     |    66 |
| Vikram Rao  | Hyderabad |    81 |
+-------------+-----------+-------+
```

`Karan Patel` scored **38** but still appeared. MySQL read the condition as:

```text
city = 'Hyderabad'   OR   (city = 'Kochi' AND marks > 60)
```

The marks test was applied **only to Kochi**. Every Hyderabad student came
through regardless of marks.

### Correct

```sql
SELECT name, city, marks FROM students
WHERE (city = 'Hyderabad' OR city = 'Kochi') AND marks > 60;
```

### Output

```
+-------------+-----------+-------+
| name        | city      | marks |
+-------------+-----------+-------+
| Rahul Verma | Hyderabad |    78 |
| Priya Nair  | Kochi     |    66 |
| Vikram Rao  | Hyderabad |    81 |
+-------------+-----------+-------+
```

> **Rule:** Whenever a query contains both `AND` and `OR`, **always use
> brackets.** Even when the result happens to be correct, brackets show your
> intention.

---

# 16. The NOT Operator

`NOT` reverses a condition.

### Example

```sql
SELECT name, marks FROM students
WHERE NOT marks > 70
ORDER BY marks DESC;
```

### Expected Output

```
+-------------+-------+
| name        | marks |
+-------------+-------+
| Priya Nair  |    66 |
| Sneha Iyer  |    54 |
| Divya Menon |    45 |
| Karan Patel |    38 |
+-------------+-------+
```

> **Note:** `Meera Nair` is missing. Her marks are `NULL`, so `NULL > 70` is
> unknown, and `NOT unknown` is still unknown — the row is dropped.

---

# 17. The EXISTS Operator

`EXISTS` checks whether a subquery returns **at least one row**. It is used to
test for related data in another table.

First create a second table.

```sql
DROP TABLE IF EXISTS courses;

CREATE TABLE courses (
    course_id   INT PRIMARY KEY,
    course_name VARCHAR(50),
    duration    INT,
    fee         INT
);

INSERT INTO courses VALUES
(1,'Python',45,15000),
(2,'SQL',30,10000),
(3,'Java',60,20000),
(4,'DSA',90,25000),
(5,'Cloud',30,18000);
```

### Syntax

```sql
SELECT column_list
FROM table_name
WHERE EXISTS (subquery);
```

### Example

Courses that at least one student has joined.

```sql
SELECT course_name FROM courses c
WHERE EXISTS (SELECT 1 FROM students s WHERE s.course = c.course_name);
```

### Expected Output

```
+-------------+
| course_name |
+-------------+
| Python      |
| SQL         |
| Java        |
| DSA         |
+-------------+
```

`Cloud` is missing because no student has joined it.

---

# 18. The NOT EXISTS Operator

### Example

Courses that **no** student has joined.

```sql
SELECT course_name FROM courses c
WHERE NOT EXISTS (SELECT 1 FROM students s WHERE s.course = c.course_name);
```

### Expected Output

```
+-------------+
| course_name |
+-------------+
| Cloud       |
+-------------+
```

> **Note:** `SELECT 1` is used inside `EXISTS` because the values do not matter.
> `EXISTS` only checks **whether** rows come back, not what is in them.

---

# 19. IN vs EXISTS

| Point            | `IN`                        | `EXISTS`                       |
| ---------------- | --------------------------- | ------------------------------ |
| Compares         | A value against a list      | Whether rows exist             |
| Subquery returns | One column                  | Anything (`SELECT 1`)          |
| Handles `NULL`   | ❌ `NOT IN` breaks           | ✅ Safe                        |
| Better when      | The list is small           | The subquery is large          |

**Simple rule:** use `IN` for a short list of values, `EXISTS` when checking
another table.

---

# Common Errors

## Error 1: NOT IN with a NULL Value

```sql
SELECT name FROM students WHERE course NOT IN ('Python','SQL',NULL);
```

### Result

```
Empty set
```

### Reason

The condition becomes:

```text
course <> 'Python'  AND  course <> 'SQL'  AND  course <> NULL
                                               └── always unknown
```

Since SQL cannot prove a value differs from an unknown, **no row can ever
pass**. There is no error message, which makes this hard to spot.

### Solution

Use `NOT EXISTS`, or remove the `NULL` first.

---

## Error 2: BETWEEN with the Larger Value First

```sql
SELECT name, age FROM students WHERE age BETWEEN 22 AND 21;
```

### Result

```
Empty set
```

### Reason

`BETWEEN 22 AND 21` means `age >= 22 AND age <= 21`, which is impossible.

### Solution

```sql
SELECT name, age FROM students WHERE age BETWEEN 21 AND 22;
```

---

## Error 3: Missing Quotes in the IN List

```sql
SELECT name FROM students WHERE course IN (Python, Java);
```

### Error

```text
ERROR 1054 (42S22): Unknown column 'Python' in 'where clause'
```

### Reason

Without quotes, MySQL thinks `Python` is a **column name**.

### Solution

```sql
SELECT name FROM students WHERE course IN ('Python','Java');
```

### A Different Error for the Same Mistake

```sql
SELECT name FROM students WHERE course IN (Python, SQL);
```

```text
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual
that corresponds to your MySQL server version for the right syntax to use
near 'SQL)' at line 1
```

The same missing quotes, but a **syntax error** this time instead of "unknown
column". The reason is that `SQL` is a **reserved word** in MySQL, so it cannot
be read as a column name at all.

> **Note:** This is why quoting text is not optional. Depending on the word you
> forget to quote, you get one of two completely different error messages.

---

## Error 4: Using = Instead of LIKE

```sql
SELECT name FROM students WHERE name = 'R%';
```

### Result

```
Empty set
```

### Reason

`=` compares the **exact text** `R%`. Wildcards only work with `LIKE`.

### Solution

```sql
SELECT name FROM students WHERE name LIKE 'R%';
```

---

## Error 5: Mixing AND and OR Without Brackets

Covered in section 15. It produces **no error** — only a wrong answer, which is
worse. Always bracket mixed conditions.

---

# Commands Covered

| Operator          | Purpose                                     |
| ----------------- | ------------------------------------------- |
| `IN`              | Matches any value in a list                 |
| `NOT IN`          | Matches none of the values in a list        |
| `BETWEEN`         | Matches a range, both ends included         |
| `NOT BETWEEN`     | Matches outside a range                     |
| `LIKE`            | Matches a pattern using `%` and `_`         |
| `%`               | Any number of characters                    |
| `_`               | Exactly one character                       |
| `AND`             | Both conditions must be true                |
| `OR`              | Any one condition must be true              |
| `NOT`             | Reverses a condition                        |
| `EXISTS`          | True if the subquery returns any row         |
| `NOT EXISTS`      | True if the subquery returns no rows         |

---

# Summary

| If you want to...                     | Use                       |
| ------------------------------------- | ------------------------- |
| Match one of several values           | `IN`                      |
| Match a numeric or date range         | `BETWEEN`                 |
| Search for part of a text             | `LIKE`                    |
| Check another table for related rows  | `EXISTS`                  |
| Require two conditions                | `AND`                     |
| Accept either condition               | `OR`                      |

Rules worth remembering:

* `BETWEEN` includes **both** ends, and the smaller value comes first.
* `%` is many characters, `_` is exactly one.
* `AND` runs before `OR` — **use brackets**.
* `NOT IN` fails silently when the list contains `NULL`; `NOT EXISTS` is safe.

---

# Practice Questions

1. Display students whose course is `Java` or `DSA` using `IN`.
2. Rewrite question 1 using `OR`.
3. Display students whose course is **not** `Python`.
4. Display students aged between 20 and 22.
5. Display students whose marks are **not** between 40 and 80.
6. Display students who joined between March and May 2025.
7. Display students whose name starts with `A`.
8. Display students whose name ends with `a`.
9. Display students whose name contains `Me`.
10. Display students whose name has `i` as the second letter.
11. Display students from Chennai or Pune who scored above 70, with brackets.
12. Run question 11 without brackets and explain the difference.
13. Display courses that at least one student has joined, using `EXISTS`.
14. Display courses nobody has joined, using `NOT EXISTS`.
15. Explain why `NOT IN` with a `NULL` in the list returns nothing.

---

# Class Summary

In this notebook, you learned:

* Matching a list of values using `IN` and `NOT IN`
* Matching ranges of numbers and dates using `BETWEEN` and `NOT BETWEEN`
* Searching text patterns using `LIKE` with `%` and `_`
* Combining conditions using `AND`, `OR` and `NOT`
* Why `AND` is evaluated before `OR`, and why brackets matter
* Checking related tables using `EXISTS` and `NOT EXISTS`
* When to prefer `IN` and when to prefer `EXISTS`
* Two silent failures: `NOT IN` with `NULL`, and mixed `AND`/`OR`

You are now ready to learn the next topic: **SQL Functions — String, Numeric,
Date and Aggregate functions**.
