# Subqueries and Window Functions

In this section, we will learn how to write a query inside another query, and how
to calculate across rows without losing them.

---

# What is a Subquery?

A **subquery** is a `SELECT` written **inside** another `SELECT`.

Some important points:

* The **inner** query runs first, and its result is used by the **outer** query.
* A subquery is always written inside **brackets**.
* It can appear in `WHERE`, `SELECT`, `FROM` or `HAVING`.
* It lets one query depend on a value it calculates for itself.

### Why not just type the number?

```sql
SELECT ROUND(AVG(marks),2) AS class_average FROM students;
```

```
+---------------+
| class_average |
+---------------+
|         69.44 |
+---------------+
```

You could now write `WHERE marks > 69.44`. But tomorrow a new student joins and
that number is wrong. A subquery recalculates it every time.

---

# Table Used in This Section

Run this once before starting.

```sql
CREATE DATABASE IF NOT EXISTS training;
USE training;

DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS employees;

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

CREATE TABLE students (
    student_id INT PRIMARY KEY,
    name       VARCHAR(50),
    city       VARCHAR(50),
    course_id  INT,
    marks      INT,
    joined_on  DATE
);

INSERT INTO students VALUES
(101,'Rahul Verma','Hyderabad',1,78,'2025-01-15'),
(102,'Anita Sharma','Chennai',2,95,'2025-01-20'),
(103,'Karan Patel','Hyderabad',1,38,'2025-02-01'),
(104,'Priya Nair','Kochi',3,66,'2025-02-10'),
(105,'Vikram Rao','Hyderabad',2,81,'2025-03-05'),
(106,'Sneha Iyer','Chennai',3,54,'2025-03-12'),
(107,'Arjun Mehta','Pune',4,90,'2025-04-02'),
(108,'Divya Menon','Kochi',1,45,'2025-04-18'),
(109,'Rohit Sinha','Pune',NULL,78,'2025-05-01'),
(110,'Meera Nair','Chennai',4,NULL,'2025-05-20');

CREATE TABLE employees (
    emp_id     INT PRIMARY KEY,
    emp_name   VARCHAR(50),
    manager_id INT,
    salary     INT
);

INSERT INTO employees VALUES
(1,'Anil',NULL,90000),
(2,'Bhavna',1,70000),
(3,'Chetan',1,65000),
(4,'Deepa',2,50000),
(5,'Esha',2,52000);
```

Note that **Rahul Verma and Rohit Sinha both scored 78**. That tie is used later
to explain the three ranking functions.

---

# PART 1 — SUBQUERIES

---

# Three Types of Subquery

| Type            | Returns                      | Used with        |
| --------------- | ---------------------------- | ---------------- |
| **Scalar**      | One single value             | `=`, `>`, `<`    |
| **Multi-row**   | One column, many rows        | `IN`, `EXISTS`   |
| **Correlated**  | Re-runs for every outer row  | `EXISTS`, `SELECT` |

---

# 1. Scalar Subquery — Returns One Value

### Syntax

```sql
SELECT columns
FROM table_name
WHERE column_name > (SELECT aggregate_function(column) FROM table_name);
```

### Example

Students who scored above the class average.

```sql
SELECT name, marks
FROM students
WHERE marks > (SELECT AVG(marks) FROM students)
ORDER BY marks DESC;
```

### Expected Output

```
+--------------+-------+
| name         | marks |
+--------------+-------+
| Anita Sharma |    95 |
| Arjun Mehta  |    90 |
| Vikram Rao   |    81 |
| Rahul Verma  |    78 |
| Rohit Sinha  |    78 |
+--------------+-------+
```

The inner query returned `69.44`, so the outer query became
`WHERE marks > 69.44`.

---

# 2. Scalar Subquery with MAX

### Example

The student with the highest marks.

```sql
SELECT name, marks FROM students WHERE marks = (SELECT MAX(marks) FROM students);
```

### Expected Output

```
+--------------+-------+
| name         | marks |
+--------------+-------+
| Anita Sharma |    95 |
+--------------+-------+
```

> **Note:** If two students tied for the top, **both** would appear. That is
> usually what you want — unlike `LIMIT 1`, which picks only one arbitrarily.

---

# 3. Changing the Inner Query Changes the Question

The subquery is the **definition of the threshold**. Filter it, and the whole
meaning changes without touching the outer query.

### Example

Students who scored above the **Hyderabad** average.

```sql
SELECT name, marks
FROM students
WHERE marks > (SELECT AVG(marks) FROM students WHERE city = 'Hyderabad')
ORDER BY marks DESC;
```

### Expected Output

```
+--------------+-------+
| name         | marks |
+--------------+-------+
| Anita Sharma |    95 |
| Arjun Mehta  |    90 |
| Vikram Rao   |    81 |
| Rahul Verma  |    78 |
| Rohit Sinha  |    78 |
| Priya Nair   |    66 |
+--------------+-------+
```

**Six students now, not five.** The Hyderabad average is 65.67, lower than the
class average of 69.44, so the bar dropped and Priya Nair qualified.

---

# 4. Multi-Row Subquery — Use IN, Not =

When the inner query returns **many rows**, you must use `IN`.

### Syntax

```sql
SELECT columns
FROM table_name
WHERE column_name IN (SELECT column FROM another_table WHERE condition);
```

### Example

Students on any course longer than 40 days.

```sql
SELECT name FROM students
WHERE course_id IN (SELECT course_id FROM courses WHERE duration > 40);
```

### Expected Output

```
+-------------+
| name        |
+-------------+
| Rahul Verma |
| Karan Patel |
| Priya Nair  |
| Sneha Iyer  |
| Arjun Mehta |
| Divya Menon |
| Meera Nair  |
+-------------+
```

The inner query returned three course ids (Python, Java, DSA). Using `=` instead
of `IN` here would fail — see Common Errors.

---

# 5. Correlated Subquery — Depends on the Outer Query

A **correlated** subquery mentions a column from the outer query, so it cannot
run on its own. It runs **once per outer row**.

### Example

```sql
SELECT c.course_name,
       (SELECT COUNT(*) FROM students s WHERE s.course_id = c.course_id) AS enrolled
FROM courses c;
```

### Expected Output

```
+-------------+----------+
| course_name | enrolled |
+-------------+----------+
| Python      |        3 |
| SQL         |        2 |
| Java        |        2 |
| DSA         |        2 |
| Cloud       |        0 |
+-------------+----------+
```

Notice `c.course_id` inside the inner query — that comes from the **outer** query.
The inner query runs five times, once for each course.

> **Note:** The same answer can be produced by a `LEFT JOIN` with `GROUP BY`
> (Day 7). The join is usually faster because it reads the table once. Know both.

---

# 6. Correlated Subquery — Compare a Row to Its Own Group

This is the pattern for *"the best student in each city"* before window functions
existed.

### Example

```sql
SELECT name, city, marks
FROM students s1
WHERE marks = (SELECT MAX(marks) FROM students s2 WHERE s2.city = s1.city)
ORDER BY city;
```

### Expected Output

```
+--------------+-----------+-------+
| name         | city      | marks |
+--------------+-----------+-------+
| Anita Sharma | Chennai   |    95 |
| Vikram Rao   | Hyderabad |    81 |
| Priya Nair   | Kochi     |    66 |
| Arjun Mehta  | Pune      |    90 |
+--------------+-----------+-------+
```

The two aliases `s1` and `s2` are what make it work — `s2` is filtered using
`s1`'s city.

---

# 7. Subquery in FROM — A Derived Table

You can treat the result of a query as a temporary table.

### Syntax

```sql
SELECT columns
FROM (SELECT columns FROM table_name GROUP BY column) AS alias_name
WHERE condition;
```

### Example

Cities whose average marks are above 70.

```sql
SELECT city, avg_marks
FROM (SELECT city, ROUND(AVG(marks),2) AS avg_marks
      FROM students GROUP BY city) AS city_avg
WHERE avg_marks > 70;
```

### Expected Output

```
+---------+-----------+
| city    | avg_marks |
+---------+-----------+
| Chennai |     74.50 |
| Pune    |     84.00 |
+---------+-----------+
```

**Key Notes:**

* A derived table **must** be given an alias — here `city_avg`. MySQL will not
  accept it otherwise.
* Notice we can filter on `avg_marks`, a column that did not exist in the
  original table.

---

# 8. Where Subqueries Can Be Used

| Position | Purpose                              |
| -------- | ------------------------------------ |
| `WHERE`  | Compare against a calculated value   |
| `SELECT` | Add an extra calculated column       |
| `FROM`   | Query the result of another query    |
| `HAVING` | Compare groups against a value       |

---

# PART 2 — WINDOW FUNCTIONS

---

# 9. What is a Window Function?

An **aggregate** collapses rows. A **window function** performs a similar
calculation but **keeps every row**.

```text
   AGGREGATE                     WINDOW FUNCTION
   10 rows  ->  1 row            10 rows  ->  10 rows
   detail is lost                detail is kept, plus the calculation
```

### Syntax

```sql
function() OVER (PARTITION BY column ORDER BY column)
```

| Part           | Meaning                                          |
| -------------- | ------------------------------------------------ |
| `OVER`         | Marks this as a window function                  |
| `PARTITION BY` | Splits the rows into groups (optional)           |
| `ORDER BY`     | The order **inside** each group                  |

> **Note:** Window functions need **MySQL 8.0 or later**. They do not work in
> MySQL 5.7.

---

# 10. ROW_NUMBER, RANK and DENSE_RANK

All three number the rows. They differ **only when values tie** — and that
difference is asked in almost every interview.

### Example

```sql
SELECT name, marks,
       ROW_NUMBER() OVER (ORDER BY marks DESC) AS row_num,
       RANK()       OVER (ORDER BY marks DESC) AS rnk,
       DENSE_RANK() OVER (ORDER BY marks DESC) AS dense_rnk
FROM students
WHERE marks IS NOT NULL;
```

### Expected Output

```
+--------------+-------+---------+-----+-----------+
| name         | marks | row_num | rnk | dense_rnk |
+--------------+-------+---------+-----+-----------+
| Anita Sharma |    95 |       1 |   1 |         1 |
| Arjun Mehta  |    90 |       2 |   2 |         2 |
| Vikram Rao   |    81 |       3 |   3 |         3 |
| Rahul Verma  |    78 |       4 |   4 |         4 |
| Rohit Sinha  |    78 |       5 |   4 |         4 |
| Priya Nair   |    66 |       6 |   6 |         5 |
| Sneha Iyer   |    54 |       7 |   7 |         6 |
| Divya Menon  |    45 |       8 |   8 |         7 |
| Karan Patel  |    38 |       9 |   9 |         8 |
+--------------+-------+---------+-----+-----------+
```

**Look at the two students on 78, then at the row after them.**

| Function       | On the tie   | Next value | In words                             |
| -------------- | ------------ | ---------- | ------------------------------------ |
| `ROW_NUMBER()` | **4, 5**     | 6          | Always different, tie broken at random |
| `RANK()`       | **4, 4**     | **6**      | Same rank, then **skips** a number   |
| `DENSE_RANK()` | **4, 4**     | **5**      | Same rank, **no gap**                |

> **Remember it as:** *"`RANK` leaves a hole, `DENSE_RANK` does not."*

---

# 11. PARTITION BY — Restart the Numbering per Group

### Example

Rank the students **within each city**.

```sql
SELECT name, city, marks,
       RANK() OVER (PARTITION BY city ORDER BY marks DESC) AS rank_in_city
FROM students
WHERE marks IS NOT NULL;
```

### Expected Output

```
+--------------+-----------+-------+--------------+
| name         | city      | marks | rank_in_city |
+--------------+-----------+-------+--------------+
| Anita Sharma | Chennai   |    95 |            1 |
| Sneha Iyer   | Chennai   |    54 |            2 |
| Vikram Rao   | Hyderabad |    81 |            1 |
| Rahul Verma  | Hyderabad |    78 |            2 |
| Karan Patel  | Hyderabad |    38 |            3 |
| Priya Nair   | Kochi     |    66 |            1 |
| Divya Menon  | Kochi     |    45 |            2 |
| Arjun Mehta  | Pune      |    90 |            1 |
| Rohit Sinha  | Pune      |    78 |            2 |
+--------------+-----------+-------+--------------+
```

The rank **restarts at 1** in every city. Four "top of the class" answers from
one query.

---

# 12. GROUP BY vs PARTITION BY

| Point         | `GROUP BY`          | `PARTITION BY`      |
| ------------- | ------------------- | ------------------- |
| Rows returned | One per group       | **All of them**     |
| Detail        | Lost                | Kept                |
| Written in    | The query itself    | Inside `OVER ()`    |

---

# 13. Aggregates as Window Functions

Any aggregate can take an `OVER` clause. This shows a group total **beside** each
row.

### Example

```sql
SELECT name, city, marks,
       ROUND(AVG(marks) OVER (PARTITION BY city),2) AS city_avg
FROM students
WHERE marks IS NOT NULL;
```

### Expected Output

```
+--------------+-----------+-------+----------+
| name         | city      | marks | city_avg |
+--------------+-----------+-------+----------+
| Anita Sharma | Chennai   |    95 |    74.50 |
| Sneha Iyer   | Chennai   |    54 |    74.50 |
| Rahul Verma  | Hyderabad |    78 |    65.67 |
| Karan Patel  | Hyderabad |    38 |    65.67 |
| Vikram Rao   | Hyderabad |    81 |    65.67 |
| Priya Nair   | Kochi     |    66 |    55.50 |
| Divya Menon  | Kochi     |    45 |    55.50 |
| Arjun Mehta  | Pune      |    90 |    84.00 |
| Rohit Sinha  | Pune      |    78 |    84.00 |
+--------------+-----------+-------+----------+
```

Every student is still listed, **and** each one can be compared to their city's
average. `GROUP BY` alone cannot do this — you would lose the names.

---

# 14. Top N Per Group — The Most Useful Pattern

A window function is calculated **after** `WHERE`, so you cannot filter on it in
the same query. You must wrap the query and filter outside.

### Example

The top student in each city.

```sql
SELECT name, city, marks
FROM (SELECT name, city, marks,
             RANK() OVER (PARTITION BY city ORDER BY marks DESC) AS r
      FROM students WHERE marks IS NOT NULL) AS ranked
WHERE r = 1;
```

### Expected Output

```
+--------------+-----------+-------+
| name         | city      | marks |
+--------------+-----------+-------+
| Anita Sharma | Chennai   |    95 |
| Vikram Rao   | Hyderabad |    81 |
| Priya Nair   | Kochi     |    66 |
| Arjun Mehta  | Pune      |    90 |
+--------------+-----------+-------+
```

**Learn this two-level shape.** It answers a huge number of real questions:
the latest order per customer, the highest-paid employee per department, the most
recent reading per device.

---

# 15. Second Highest Value

A very common interview question, with two good answers.

### Using LIMIT and OFFSET

```sql
SELECT DISTINCT marks FROM students WHERE marks IS NOT NULL
ORDER BY marks DESC LIMIT 1 OFFSET 1;
```

### Expected Output

```
+-------+
| marks |
+-------+
|    90 |
+-------+
```

### Using a Subquery

```sql
SELECT MAX(marks) AS second_highest FROM students
WHERE marks < (SELECT MAX(marks) FROM students);
```

```
+----------------+
| second_highest |
+----------------+
|             90 |
+----------------+
```

> **Note:** `DISTINCT` matters in the first version. Without it, two students
> tied for first place would make the "second" row still show the top mark.

---

# Common Errors

## Error 1: Using = with a Multi-Row Subquery

```sql
SELECT name FROM students
WHERE course_id = (SELECT course_id FROM courses WHERE duration > 40);
```

### Error

```text
ERROR 1242 (21000): Subquery returns more than 1 row
```

### Reason

`=` can only compare against **one** value, but the subquery returned three.

### Solution

```sql
SELECT name FROM students
WHERE course_id IN (SELECT course_id FROM courses WHERE duration > 40);
```

---

## Error 2: Derived Table Without an Alias

```sql
SELECT city FROM (SELECT city, AVG(marks) FROM students GROUP BY city);
```

### Error

```text
ERROR 1248 (42000): Every derived table must have its own alias
```

### Solution

Give it a name.

```sql
SELECT city FROM (SELECT city, AVG(marks) FROM students GROUP BY city) AS city_avg;
```

---

## Error 3: Filtering a Window Function in WHERE

```sql
SELECT name, RANK() OVER (ORDER BY marks DESC) AS r FROM students WHERE r = 1;
```

### Error

```text
ERROR 1054 (42S22): Unknown column 'r' in 'where clause'
```

### Reason

Window functions are calculated **after** `WHERE` has already run, so `r` does
not exist yet.

### Solution

Wrap the query and filter outside — see section 14.

---

## Error 4: Using a Window Function in WHERE Directly

```sql
SELECT name FROM students WHERE RANK() OVER (ORDER BY marks DESC) = 1;
```

### Error

```text
ERROR 3593 (HY000): You cannot use the window function 'rank' in this context.'
```

(The stray quote at the end is MySQL's own typo in the message, not yours.)

### Solution

Same as Error 3 — use a derived table.

---

# Commands Covered

| Command                              | Purpose                                |
| ------------------------------------ | -------------------------------------- |
| `(SELECT ...)` in `WHERE`            | Compare against a calculated value     |
| `IN (SELECT ...)`                    | Compare against many values            |
| `(SELECT ...)` in `SELECT`           | Add a calculated column                |
| `FROM (SELECT ...) AS alias`         | Query the result of a query            |
| `ROW_NUMBER() OVER (...)`            | Numbers rows, always different         |
| `RANK() OVER (...)`                  | Same rank on ties, then skips          |
| `DENSE_RANK() OVER (...)`            | Same rank on ties, no gap              |
| `PARTITION BY`                       | Restarts the calculation per group     |
| `AVG(...) OVER (PARTITION BY ...)`   | Group total beside every row           |

---

# Summary

* A **subquery** is a query inside a query. The inner one runs first.
* **Scalar** returns one value (use `=`, `>`); **multi-row** returns many
  (use `IN`); **correlated** re-runs for each outer row.
* A **derived table** in `FROM` must have an alias.
* A **window function** calculates across rows **without collapsing them**.
* On a tie: `ROW_NUMBER` gives 4, 5 · `RANK` gives 4, 4 then **6** ·
  `DENSE_RANK` gives 4, 4 then **5**.
* `PARTITION BY` restarts the calculation per group but keeps every row.
* **Top N per group** = window function inside a derived table, filtered outside.
* You cannot filter a window function in `WHERE`.

---

# Practice Questions

1. Find the class average using a subquery, then list students above it.
2. Find the student with the highest marks using a subquery.
3. List students who scored above the Kochi average.
4. List students on courses shorter than 45 days using `IN`.
5. Add a column to `courses` showing how many students each has.
6. Find cities whose average is above 70 using a derived table.
7. Find the top student in each city using a correlated subquery.
8. Number all students from best to worst using `ROW_NUMBER()`.
9. Add `RANK()` and `DENSE_RANK()` and explain the two tied students.
10. Why does `RANK` jump from 4 to 6?
11. Rank the students within each city.
12. Show each student beside their city's average marks.
13. Find the top student in each city using a window function.
14. Find the second highest marks in two different ways.
15. Explain why `WHERE r = 1` cannot go in the same query as the `RANK()`.
16. What is the difference between `GROUP BY` and `PARTITION BY`?

---

# Class Summary

In this notebook, you learned:

* Writing a query inside another query using **subqueries**
* The three types: **scalar**, **multi-row** and **correlated**
* Why `IN` is needed when a subquery returns many rows
* Using a subquery in `FROM` as a **derived table**, and why it needs an alias
* How changing the inner query changes the whole question
* **Window functions** — calculating across rows without losing them
* `ROW_NUMBER`, `RANK` and `DENSE_RANK`, and exactly how they differ on ties
* `PARTITION BY` to restart a calculation per group
* Showing a group average beside every row
* The **Top N per group** pattern using a derived table
* Two ways to find the second highest value

You are now ready to learn the next topic: **Views, Indexes and Transactions**.
