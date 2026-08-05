# Joins and Set Operations in MySQL

In this section, we will learn how to combine rows from more than one table using
joins, and how to stack results from two queries using `UNION`.

---

# Why Do We Need Joins?

Real data is deliberately split across several tables.

```text
   students                          courses
   +----------------------+          +-------------------------+
   | student_id  name     |          | course_id  course_name  |
   | course_id  ----------|--------->| duration   fee          |
   +----------------------+          +-------------------------+
```

Some important points:

* Storing the course name against every student would repeat `'Python'` many
  times.
* If the course fee changes, you would have to edit many rows.
* Splitting the data removes this repetition — this is **normalisation**.
* A **join** puts the data back together only when you need it.

---

# Table Used in This Section

Run this once before starting. This section uses **three** tables.

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
    marks      INT
);

INSERT INTO students VALUES
(101,'Rahul Verma','Hyderabad',1,78),
(102,'Anita Sharma','Chennai',2,95),
(103,'Karan Patel','Hyderabad',1,38),
(104,'Priya Nair','Kochi',3,66),
(105,'Vikram Rao','Hyderabad',2,81),
(106,'Sneha Iyer','Chennai',3,54),
(107,'Arjun Mehta','Pune',4,90),
(108,'Divya Menon','Kochi',1,45),
(109,'Rohit Sinha','Pune',NULL,78),
(110,'Meera Nair','Chennai',4,NULL);

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

Two rows are deliberately unmatched:

* `Rohit Sinha` has **no course**.
* `Cloud` has **no students**.

These are used to show the difference between the join types.

---

# Types of Joins

| Join         | Keeps                                |
| ------------ | ------------------------------------ |
| `INNER JOIN` | Only rows matching in **both** tables |
| `LEFT JOIN`  | **All** left rows + matches           |
| `RIGHT JOIN` | **All** right rows + matches          |
| `CROSS JOIN` | Every possible combination            |
| `SELF JOIN`  | A table joined to itself              |

```text
   INNER            LEFT             RIGHT            CROSS
   +---+---+        +---+---+        +---+---+        every row
   |   |###|        |###|###|        |   |###|        paired with
   |   |###|        |###|###|        |   |###|        every row
   +---+---+        +---+---+        +---+---+
   only matches     all left         all right        10 x 5 = 50
```

---

# 1. INNER JOIN

Returns only the rows that match in **both** tables.

### Syntax

```sql
SELECT columns
FROM table1
INNER JOIN table2 ON table1.column = table2.column;
```

### Example

```sql
SELECT s.name, c.course_name
FROM students s
INNER JOIN courses c ON s.course_id = c.course_id;
```

### Expected Output

```
+--------------+-------------+
| name         | course_name |
+--------------+-------------+
| Rahul Verma  | Python      |
| Anita Sharma | SQL         |
| Karan Patel  | Python      |
| Priya Nair   | Java        |
| Vikram Rao   | SQL         |
| Sneha Iyer   | Java        |
| Arjun Mehta  | DSA         |
| Divya Menon  | Python      |
| Meera Nair   | DSA         |
+--------------+-------------+
```

**Nine rows, not ten.** `Rohit Sinha` is missing because his `course_id` is
`NULL` and matches nothing. `Cloud` is also missing because no student has
joined it.

**Key Notes:**

* `s` and `c` are **table aliases**. Without them you would write
  `students.course_id` every time.
* `ON` tells MySQL how the two tables line up — usually foreign key = primary key.
* `INNER` is optional. Writing just `JOIN` means `INNER JOIN`.

---

# 2. LEFT JOIN

Keeps **every** row from the left table, even when there is no match.

### Syntax

```sql
SELECT columns
FROM table1
LEFT JOIN table2 ON table1.column = table2.column;
```

### Example

```sql
SELECT s.name, c.course_name
FROM students s
LEFT JOIN courses c ON s.course_id = c.course_id;
```

### Expected Output

```
+--------------+-------------+
| name         | course_name |
+--------------+-------------+
| Rahul Verma  | Python      |
| Anita Sharma | SQL         |
| Karan Patel  | Python      |
| Priya Nair   | Java        |
| Vikram Rao   | SQL         |
| Sneha Iyer   | Java        |
| Arjun Mehta  | DSA         |
| Divya Menon  | Python      |
| Rohit Sinha  | NULL        |
| Meera Nair   | DSA         |
+--------------+-------------+
```

All **ten** students appear. `Rohit Sinha` has no course, so MySQL fills that
column with `NULL`.

> **This is the most used join in real work.** "Show me all customers, with their
> orders if they have any" is a `LEFT JOIN`.

---

# 3. RIGHT JOIN

Keeps **every** row from the right table.

### Example

```sql
SELECT s.name, c.course_name
FROM students s
RIGHT JOIN courses c ON s.course_id = c.course_id;
```

### Expected Output

```
+--------------+-------------+
| name         | course_name |
+--------------+-------------+
| Divya Menon  | Python      |
| Karan Patel  | Python      |
| Rahul Verma  | Python      |
| Vikram Rao   | SQL         |
| Anita Sharma | SQL         |
| Sneha Iyer   | Java        |
| Priya Nair   | Java        |
| Meera Nair   | DSA         |
| Arjun Mehta  | DSA         |
| NULL         | Cloud       |
+--------------+-------------+
```

Now `Cloud` appears with a `NULL` student name, and `Rohit Sinha` has
disappeared.

> **Note:** `A RIGHT JOIN B` gives exactly the same result as `B LEFT JOIN A`.
> Many teams avoid `RIGHT JOIN` altogether because swapping the tables and using
> `LEFT JOIN` reads more clearly.

---

# 4. Finding Unmatched Rows

A `LEFT JOIN` plus `IS NULL` finds rows that have **no match**. This is one of
the most useful patterns in SQL.

### Example — Students with No Course

```sql
SELECT s.name
FROM students s
LEFT JOIN courses c ON s.course_id = c.course_id
WHERE c.course_id IS NULL;
```

### Expected Output

```
+-------------+
| name        |
+-------------+
| Rohit Sinha |
+-------------+
```

### Example — Courses with No Students

```sql
SELECT c.course_name
FROM courses c
LEFT JOIN students s ON s.course_id = c.course_id
WHERE s.student_id IS NULL;
```

### Expected Output

```
+-------------+
| course_name |
+-------------+
| Cloud       |
+-------------+
```

> **Note:** Always test `IS NULL` on a column that can **never** be `NULL` in the
> other table — usually its primary key. Testing a nullable column cannot tell
> the difference between "no match" and "matched, but the value was `NULL`".

---

# 5. SELF JOIN

A **self join** joins a table to itself. It is used when a row points to another
row in the same table.

In the `employees` table, `manager_id` points to another `emp_id`.

### Example

```sql
SELECT e.emp_name AS employee, m.emp_name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.emp_id;
```

### Expected Output

```
+----------+---------+
| employee | manager |
+----------+---------+
| Anil     | NULL    |
| Bhavna   | Anil    |
| Chetan   | Anil    |
| Deepa    | Bhavna  |
| Esha     | Bhavna  |
+----------+---------+
```

**Key Notes:**

* Aliases are **compulsory** here. `e` and `m` are the same table, and without
  two different names MySQL cannot tell them apart.
* `LEFT JOIN` keeps `Anil`, the top manager, whose `manager_id` is `NULL`. An
  `INNER JOIN` would drop him.

---

# 6. CROSS JOIN

A `CROSS JOIN` pairs **every** row of one table with **every** row of the other.

### Example

```sql
SELECT COUNT(*) AS cross_rows FROM students CROSS JOIN courses;
```

### Expected Output

```
+------------+
| cross_rows |
+------------+
|         50 |
+------------+
```

10 students × 5 courses = **50 rows**.

> **Warning:** You almost never want this. If you forget the `ON` condition in a
> normal join, MySQL produces a cross join, and the row count explodes. On two
> tables of 10,000 rows that is 100 million rows.

---

# 7. Joining with WHERE

A join can be filtered like any other query.

### Example

```sql
SELECT s.name, c.course_name, c.fee
FROM students s
JOIN courses c ON s.course_id = c.course_id
WHERE c.fee > 15000
ORDER BY c.fee DESC;
```

### Expected Output

```
+-------------+-------------+-------+
| name        | course_name | fee   |
+-------------+-------------+-------+
| Arjun Mehta | DSA         | 25000 |
| Meera Nair  | DSA         | 25000 |
| Priya Nair  | Java        | 20000 |
| Sneha Iyer  | Java        | 20000 |
+-------------+-------------+-------+
```

The `WHERE` uses a column from the **second** table, which is only possible
because the tables are joined.

---

# 8. Joining with GROUP BY

Joins and grouping are used together constantly.

### Example

```sql
SELECT c.course_name, COUNT(s.student_id) AS enrolled
FROM courses c
LEFT JOIN students s ON s.course_id = c.course_id
GROUP BY c.course_name
ORDER BY enrolled DESC;
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

`Cloud` correctly shows **0**.

---

# 9. Why COUNT(*) Is Wrong Here

This is a very common mistake, and a favourite interview question.

### The Wrong Version

```sql
SELECT c.course_name, COUNT(*) AS wrong_count
FROM courses c
LEFT JOIN students s ON s.course_id = c.course_id
GROUP BY c.course_name
ORDER BY wrong_count DESC;
```

### Output

```
+-------------+-------------+
| course_name | wrong_count |
+-------------+-------------+
| Python      |           3 |
| SQL         |           2 |
| Java        |           2 |
| DSA         |           2 |
| Cloud       |           1 |
+-------------+-------------+
```

`Cloud` shows **1**, but no student has joined it.

### Reason

The `LEFT JOIN` produces **one row** for `Cloud`, with all the student columns
filled with `NULL`. `COUNT(*)` counts that row. `COUNT(s.student_id)` skips it
because the value is `NULL`.

> **Rule:** With a `LEFT JOIN` and `GROUP BY`, always count a **column from the
> right-hand table**, never `*`.

---

# 10. ON vs WHERE on an Outer Join

For an `INNER JOIN`, putting a condition in `ON` or in `WHERE` gives the same
result. For a `LEFT JOIN` they are **completely different**.

### Wrong — This Turns the LEFT JOIN into an INNER JOIN

```sql
SELECT c.course_name, s.name
FROM courses c
LEFT JOIN students s ON s.course_id = c.course_id
WHERE s.marks >= 50;
```

`Cloud` disappears. Its `s.marks` is `NULL`, and `NULL >= 50` is not true, so the
row is thrown away **after** the join.

### Correct — Put the Condition in the Join

```sql
SELECT c.course_name, s.name
FROM courses c
LEFT JOIN students s ON s.course_id = c.course_id AND s.marks >= 50;
```

Now the condition decides **what counts as a match**, and unmatched courses are
still kept.

| Clause  | Meaning on an outer join           |
| ------- | ---------------------------------- |
| `ON`    | What counts as a match             |
| `WHERE` | Which rows survive **after** the join |

---

# 11. UNION — Stacking Results

A **join** adds columns (makes the result wider). A **union** adds rows (makes it
taller).

```text
   JOIN                    UNION
   +----+----+             +----+
   | A  | B  |             | A  |
   +----+----+             +----+
   wider                   | B  |
                           +----+
                           taller
```

### Syntax

```sql
SELECT column1 FROM table1
UNION
SELECT column1 FROM table2;
```

### Example

```sql
SELECT name FROM students
UNION
SELECT emp_name FROM employees;
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
| Vikram Rao   |
| Sneha Iyer   |
| Arjun Mehta  |
| Divya Menon  |
| Rohit Sinha  |
| Meera Nair   |
| Anil         |
| Bhavna       |
| Chetan       |
| Deepa        |
| Esha         |
+--------------+
```

**Rules for `UNION`:**

1. Both queries must return the **same number of columns**.
2. The columns must be in the **same order**, with compatible types.
3. The column headings come from the **first** query.
4. `ORDER BY` goes at the very **end**, once, and applies to the whole result.

---

# 12. UNION vs UNION ALL

| Point      | `UNION`                    | `UNION ALL`         |
| ---------- | -------------------------- | ------------------- |
| Duplicates | **Removed**                | **Kept**            |
| Speed      | Slower — it must compare   | Faster              |

### Example

```sql
SELECT city FROM students WHERE city='Pune'
UNION ALL
SELECT city FROM students WHERE city='Pune';
```

### Expected Output

```
+------+
| city |
+------+
| Pune |
| Pune |
| Pune |
| Pune |
+------+
```

With `UNION` instead of `UNION ALL`, this returns **one** row.

> **Rule:** Use `UNION ALL` unless you actually need duplicates removed. `UNION`
> does extra work to compare every row.

---

# Common Errors

## Error 1: Forgetting the ON Condition

This is the most dangerous mistake in this topic, because **there is no error
message at all.**

```sql
SELECT COUNT(*) AS rows_from_join_without_on FROM students s JOIN courses c;
```

### Result

```
+---------------------------+
| rows_from_join_without_on |
+---------------------------+
|                        50 |
+---------------------------+
```

The comma form behaves identically:

```sql
SELECT COUNT(*) AS rows_from_comma FROM students s, courses c;
```

```
+-----------------+
| rows_from_comma |
+-----------------+
|              50 |
+-----------------+
```

### Reason

MySQL **allows** `JOIN` without `ON` and treats it as a `CROSS JOIN`. You expected
9 or 10 rows and got 50. On two large tables this produces millions of rows and
looks like the server has hung.

### Solution

Always write the `ON` condition.

```sql
SELECT s.name, c.course_name FROM students s JOIN courses c ON s.course_id = c.course_id;
```

> **Habit worth teaching:** after writing any join, count the rows. If the number
> is larger than either table, you have lost the `ON` condition.

---

## Error 2: Ambiguous Column Name

```sql
SELECT course_id FROM students s JOIN courses c ON s.course_id = c.course_id;
```

### Error

```text
ERROR 1052 (23000): Column 'course_id' in field list is ambiguous
```

### Reason

Both tables have a column named `course_id`, so MySQL does not know which one you
mean.

### Solution

Say which table it comes from.

```sql
SELECT s.course_id FROM students s JOIN courses c ON s.course_id = c.course_id;
```

---

## Error 3: Different Column Counts in a UNION

```sql
SELECT name, city FROM students
UNION
SELECT emp_name FROM employees;
```

### Error

```text
ERROR 1222 (21000): The used SELECT statements have a different number of columns
```

### Solution

Both sides must select the same number of columns.

---

## Error 4: COUNT(*) with a LEFT JOIN

Covered in section 9. There is **no error** — only a wrong number. Count a
column from the right table instead of `*`.

---

# Commands Covered

| Command                         | Purpose                                    |
| ------------------------------- | ------------------------------------------ |
| `INNER JOIN ... ON`             | Only matching rows                         |
| `LEFT JOIN ... ON`              | All left rows + matches                    |
| `RIGHT JOIN ... ON`             | All right rows + matches                   |
| `CROSS JOIN`                    | Every combination                          |
| Self join with two aliases      | A table joined to itself                   |
| `LEFT JOIN ... WHERE ... IS NULL` | Finds rows with no match                 |
| `UNION`                         | Stacks rows, removes duplicates            |
| `UNION ALL`                     | Stacks rows, keeps duplicates              |

---

# Summary

| If you want...                             | Use                        |
| ------------------------------------------ | -------------------------- |
| Only matched rows                          | `INNER JOIN`               |
| All rows from the first table              | `LEFT JOIN`                |
| Rows that have **no** match                | `LEFT JOIN` + `IS NULL`    |
| Each row's manager or parent               | Self join                  |
| To stack two result sets                   | `UNION ALL`                |

Rules worth remembering:

* Table **aliases** make joins readable, and are compulsory in a self join.
* `A RIGHT JOIN B` = `B LEFT JOIN A`. Prefer `LEFT`.
* With `LEFT JOIN` + `GROUP BY`, count a **column**, never `*`.
* On an outer join, `ON` defines the match, `WHERE` filters after the join.
* Forgetting `ON` gives a cross join and a row explosion.
* `UNION` removes duplicates; `UNION ALL` is faster.

---

# Practice Questions

1. List every student with their course name.
2. List every student **including** those with no course.
3. List every course **including** those with no students.
4. Find students who have no course.
5. Find courses that no student has joined.
6. Show students on courses costing more than ₹15,000.
7. Count the students on each course, including the empty course.
8. Run question 7 with `COUNT(*)` and explain why `Cloud` is wrong.
9. Show the average marks per course name.
10. Show each employee with their manager's name.
11. Which employee has no manager, and which join keeps them?
12. How many rows does `students CROSS JOIN courses` return, and why?
13. Rewrite `students RIGHT JOIN courses` as a `LEFT JOIN`.
14. Stack the student names and employee names into one list.
15. Repeat question 14 with `UNION ALL` and explain the difference.
16. Move a condition from `WHERE` to `ON` in a `LEFT JOIN` and explain what
    changes.

---

# Class Summary

In this notebook, you learned:

* Why data is split across tables, and why joins put it back together
* `INNER JOIN` — only matching rows
* `LEFT JOIN` and `RIGHT JOIN` — keeping unmatched rows
* Finding unmatched rows using `LEFT JOIN` with `IS NULL`
* `SELF JOIN` for rows that point to other rows in the same table
* `CROSS JOIN`, and how forgetting `ON` creates one accidentally
* Using joins together with `WHERE` and `GROUP BY`
* Why `COUNT(*)` gives a wrong answer with a `LEFT JOIN`
* The difference between `ON` and `WHERE` on an outer join
* `UNION` and `UNION ALL` for stacking results

You are now ready to learn the next topic: **Subqueries and Window Functions**.
