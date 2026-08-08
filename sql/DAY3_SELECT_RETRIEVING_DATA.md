# Retrieving Data using SELECT

In this section, we will learn how to read data from a table using the `SELECT`
statement, how to filter rows, how to sort the result, and how to limit the
number of rows returned.

---

# What is SELECT?

The `SELECT` statement is used to **read** data from one or more tables.

Some important points:

* `SELECT` does not change the data in the table.
* It always returns a **result set** (rows and columns).
* It is the most frequently used command in SQL.
* The result of a `SELECT` is temporary and is not stored anywhere.

---

# The Full Shape of a SELECT

```sql
SELECT   column_list
FROM     table_name
WHERE    condition
ORDER BY column_name
LIMIT    number;
```

Only `SELECT` and `FROM` are compulsory. Everything else is optional.

---

# Order in Which MySQL Runs a SELECT

You **write** the query in one order, but MySQL **runs** it in another order.

| Step | Clause     | What it does           |
| ---- | ---------- | ---------------------- |
| 1    | `FROM`     | Picks up the table     |
| 2    | `WHERE`    | Removes unwanted rows  |
| 3    | `SELECT`   | Picks the columns      |
| 4    | `ORDER BY` | Sorts the result       |
| 5    | `LIMIT`    | Keeps only a few rows  |

This single table explains two rules you will see later:

* `WHERE` cannot use a column alias, because `SELECT` has not run yet.
* `ORDER BY` **can** use a column alias, because it runs after `SELECT`.

---

# Table Used in This Section

Run this once before starting. Every example below uses this table.

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

Two rows are deliberately incomplete:

* `Rohit Sinha` has **no course**.
* `Meera Nair` has **no marks**.

These are used later to explain `NULL`.

---

# 1. Select All Columns

The `*` symbol means **all columns**.

### Syntax

```sql
SELECT * FROM table_name;
```

### Example

```sql
SELECT * FROM students;
```

### Expected Output

```
+------------+--------------+-----------+------+--------+-------+------------+
| student_id | name         | city      | age  | course | marks | joined_on  |
+------------+--------------+-----------+------+--------+-------+------------+
|        101 | Rahul Verma  | Hyderabad |   21 | Python |    78 | 2025-01-15 |
|        102 | Anita Sharma | Chennai   |   22 | SQL    |    95 | 2025-01-20 |
|        103 | Karan Patel  | Hyderabad |   20 | Python |    38 | 2025-02-01 |
|        104 | Priya Nair   | Kochi     |   23 | Java   |    66 | 2025-02-10 |
|        105 | Vikram Rao   | Hyderabad |   21 | SQL    |    81 | 2025-03-05 |
|        106 | Sneha Iyer   | Chennai   |   22 | Java   |    54 | 2025-03-12 |
|        107 | Arjun Mehta  | Pune      |   24 | DSA    |    90 | 2025-04-02 |
|        108 | Divya Menon  | Kochi     |   20 | Python |    45 | 2025-04-18 |
|        109 | Rohit Sinha  | Pune      |   23 | NULL   |    78 | 2025-05-01 |
|        110 | Meera Nair   | Chennai   |   21 | DSA    |  NULL | 2025-05-20 |
+------------+--------------+-----------+------+--------+-------+------------+
```

> **Note:** `SELECT *` is useful while learning, but avoid it in real projects.
> You get columns you do not need, and the query changes silently when someone
> adds a column to the table.

---

# 2. Select Specific Columns

List the columns you want, separated by commas.

### Syntax

```sql
SELECT column1, column2 FROM table_name;
```

### Example

```sql
SELECT name, city FROM students;
```

### Expected Output

```
+--------------+-----------+
| name         | city      |
+--------------+-----------+
| Rahul Verma  | Hyderabad |
| Anita Sharma | Chennai   |
| Karan Patel  | Hyderabad |
| Priya Nair   | Kochi     |
| Vikram Rao   | Hyderabad |
| Sneha Iyer   | Chennai   |
| Arjun Mehta  | Pune      |
| Divya Menon  | Kochi     |
| Rohit Sinha  | Pune      |
| Meera Nair   | Chennai   |
+--------------+-----------+
```

The columns appear in the order **you** listed them, not the order they were
created in the table.

---

# 3. Remove Duplicates Using DISTINCT

`DISTINCT` removes repeated rows from the result.

### Syntax

```sql
SELECT DISTINCT column_name FROM table_name;
```

### Example

```sql
SELECT DISTINCT city FROM students;
```

### Expected Output

```
+-----------+
| city      |
+-----------+
| Hyderabad |
| Chennai   |
| Kochi     |
| Pune      |
+-----------+
```

Ten students, but only four different cities.

> **Note:** `DISTINCT` applies to **all** selected columns together.
> `SELECT DISTINCT city, age` returns every unique *combination* of city and
> age, not just unique cities.

---

# 4. Filter Rows Using WHERE

`WHERE` decides **which rows** appear in the result.

### Syntax

```sql
SELECT column_list
FROM table_name
WHERE condition;
```

### Example

```sql
SELECT name, marks FROM students WHERE marks > 70;
```

### Expected Output

```
+--------------+-------+
| name         | marks |
+--------------+-------+
| Rahul Verma  |    78 |
| Anita Sharma |    95 |
| Vikram Rao   |    81 |
| Arjun Mehta  |    90 |
| Rohit Sinha  |    78 |
+--------------+-------+
```

Five students out of ten passed the condition.

---

# 5. Filter Using a Text Value

Text values must be written inside **single quotes**.

### Syntax

```sql
SELECT column_list
FROM table_name
WHERE column_name = 'value';
```

### Example

```sql
SELECT name, city FROM students WHERE city = 'Chennai';
```

### Expected Output

```
+--------------+---------+
| name         | city    |
+--------------+---------+
| Anita Sharma | Chennai |
| Sneha Iyer   | Chennai |
| Meera Nair   | Chennai |
+--------------+---------+
```

> **Note:** In MySQL, text comparison is **not** case sensitive by default, so
> `'chennai'` also works. Do not depend on this — other databases behave
> differently.

---

# 6. Comparison Operators

| Operator     | Meaning                  | Example              |
| ------------ | ------------------------ | -------------------- |
| `=`          | Equal to                 | `marks = 78`         |
| `<>` or `!=` | Not equal to             | `city <> 'Pune'`     |
| `>`          | Greater than             | `marks > 70`         |
| `<`          | Less than                | `age < 21`           |
| `>=`         | Greater than or equal to | `marks >= 50`        |
| `<=`         | Less than or equal to    | `age <= 22`          |

> **Note:** SQL uses a **single** `=` for comparison, not `==`.

---

# 7. Combine Conditions Using AND / OR

### Syntax

```sql
SELECT column_list
FROM table_name
WHERE condition1 AND condition2;
```

### Example

```sql
SELECT name, city, age
FROM students
WHERE city = 'Hyderabad' AND age < 21;
```

### Expected Output

```
+-------------+-----------+------+
| name        | city      | age  |
+-------------+-----------+------+
| Karan Patel | Hyderabad |   20 |
+-------------+-----------+------+
```

* `AND` — **both** conditions must be true.
* `OR` — **any one** condition must be true.

> **Note:** `AND` is evaluated **before** `OR`. When you mix them, always use
> brackets so the meaning is clear.

---

# 8. Sort the Result Using ORDER BY

### Syntax

```sql
SELECT column_list
FROM table_name
ORDER BY column_name [ASC | DESC];
```

* `ASC` — ascending (smallest first). This is the default.
* `DESC` — descending (largest first).

### Example

```sql
SELECT name, marks FROM students ORDER BY marks DESC;
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
| Sneha Iyer   |    54 |
| Divya Menon  |    45 |
| Karan Patel  |    38 |
| Meera Nair   |  NULL |
+--------------+-------+
```

Notice that `Meera Nair`, whose marks are `NULL`, appears **last** in descending
order. MySQL treats `NULL` as the smallest value.

> **Note:** Without `ORDER BY`, MySQL does **not** guarantee any order. If the
> order matters, you must say so.

---

# 9. Sort by Two Columns

The second column only breaks ties inside the first.

### Example

```sql
SELECT name, city, marks
FROM students
ORDER BY city, marks DESC;
```

### Expected Output

```
+--------------+-----------+-------+
| name         | city      | marks |
+--------------+-----------+-------+
| Anita Sharma | Chennai   |    95 |
| Sneha Iyer   | Chennai   |    54 |
| Meera Nair   | Chennai   |  NULL |
| Vikram Rao   | Hyderabad |    81 |
| Rahul Verma  | Hyderabad |    78 |
| Karan Patel  | Hyderabad |    38 |
| Priya Nair   | Kochi     |    66 |
| Divya Menon  | Kochi     |    45 |
| Arjun Mehta  | Pune      |    90 |
| Rohit Sinha  | Pune      |    78 |
+--------------+-----------+-------+
```

Cities are in ascending order, and **within each city** the marks are in
descending order. The marks list restarts for every city.

---

# 10. Limit the Number of Rows

### Syntax

```sql
SELECT column_list
FROM table_name
LIMIT number;
```

### Example

Show the top 3 students.

```sql
SELECT name, marks FROM students ORDER BY marks DESC LIMIT 3;
```

### Expected Output

```
+--------------+-------+
| name         | marks |
+--------------+-------+
| Anita Sharma |    95 |
| Arjun Mehta  |    90 |
| Vikram Rao   |    81 |
+--------------+-------+
```

> **Note:** `LIMIT` must be used together with `ORDER BY`. Without a sort,
> "top 3" has no meaning — you simply get any 3 rows.

---

# 11. Skip Rows Using OFFSET

`OFFSET` skips a number of rows before returning results. This is how
pagination works.

### Syntax

```sql
SELECT column_list
FROM table_name
ORDER BY column_name
LIMIT number OFFSET number;
```

### Example

Show students ranked 4th, 5th and 6th.

```sql
SELECT name, marks FROM students ORDER BY marks DESC LIMIT 3 OFFSET 3;
```

### Expected Output

```
+-------------+-------+
| name        | marks |
+-------------+-------+
| Rahul Verma |    78 |
| Rohit Sinha |    78 |
| Priya Nair  |    66 |
+-------------+-------+
```

The first 3 rows were skipped, then the next 3 were returned.

---

### Selecting Multiple Record Ranges

If we want to retrieve **records from 3rd to 7th and again from 11th to 12th**, `LIMIT` and `OFFSET` alone cannot directly select two separate ranges.

#### Method 1: Using `ROW_NUMBER()`

First assign a row number based on the required order, and then filter the required ranges.

```sql
SELECT *
FROM (
    SELECT *,
           ROW_NUMBER() OVER (ORDER BY marks DESC) AS rn
    FROM students
) t
WHERE rn BETWEEN 3 AND 7
   OR rn BETWEEN 11 AND 12;
```

**In simple words:**
`ROW_NUMBER()` assigns a sequential number to each record. We can then use `WHERE` to select multiple ranges, such as **3–7 and 11–12**.

---

#### Method 2: Using `UNION ALL`

We can write separate queries for each range and combine their results using `UNION ALL`.

```sql
SELECT *
FROM students
ORDER BY marks DESC
LIMIT 5 OFFSET 2

UNION ALL

SELECT *
FROM students
ORDER BY marks DESC
LIMIT 2 OFFSET 10;
```

**In simple words:**
Run one query to get records **3–7**, another query to get **11–12**, and combine both result sets using `UNION ALL`.

> **Note:** In practice, `ROW_NUMBER()` is generally cleaner and more flexible when selecting multiple arbitrary ranges from an ordered result.


# 12. Rename Columns Using Aliases

An **alias** changes the column heading in the output. The table is not
affected.

### Syntax

```sql
SELECT column_name AS alias_name FROM table_name;
```

### Example

```sql
SELECT name AS student_name, marks AS score FROM students LIMIT 3;
```

### Expected Output

```
+--------------+-------+
| student_name | score |
+--------------+-------+
| Rahul Verma  |    78 |
| Anita Sharma |    95 |
| Karan Patel  |    38 |
+--------------+-------+
```

> **Note:** `AS` is optional, but keep it — the query reads better. For an
> alias containing a space, use double quotes: `AS "Student Name"`.

---

# 13. Calculated Columns

You can create new columns using expressions. They exist only in the result.

### Example

```sql
SELECT name, marks, marks + 5 AS bonus FROM students LIMIT 3;
```

### Expected Output

```
+--------------+-------+-------+
| name         | marks | bonus |
+--------------+-------+-------+
| Rahul Verma  |    78 |    83 |
| Anita Sharma |    95 |   100 |
| Karan Patel  |    38 |    43 |
+--------------+-------+-------+
```

Available operators: `+`, `-`, `*`, `/`, `%`.

> **Note:** The table is **not** changed. `marks + 5` only affects what is
> displayed. To change stored data, you need `UPDATE`.

---

# 14. Working with NULL

`NULL` means **unknown**. It is not zero, and it is not an empty text.

Any comparison with `NULL` gives an unknown result, so this returns **nothing**:

```sql
SELECT name, marks FROM students WHERE marks = NULL;
```

```
Empty set
```

### Correct Way

Use `IS NULL` and `IS NOT NULL`.

### Syntax

```sql
SELECT column_list FROM table_name WHERE column_name IS NULL;
```

### Example

```sql
SELECT name FROM students WHERE marks IS NULL;
```

### Expected Output

```
+------------+
| name       |
+------------+
| Meera Nair |
+------------+
```

### Example — IS NOT NULL

```sql
SELECT name, course FROM students WHERE course IS NOT NULL LIMIT 3;
```

### Expected Output

```
+--------------+--------+
| name         | course |
+--------------+--------+
| Rahul Verma  | Python |
| Anita Sharma | SQL    |
| Karan Patel  | Python |
+--------------+--------+
```

---

# 15. Replace NULL Using IFNULL

`IFNULL` shows a substitute value wherever a `NULL` appears.

### Syntax

```sql
SELECT IFNULL(column_name, replacement) FROM table_name;
```

### Example

```sql
SELECT name, IFNULL(marks, 0) AS marks FROM students WHERE student_id = 110;
```

### Expected Output

```
+------------+-------+
| name       | marks |
+------------+-------+
| Meera Nair |     0 |
+------------+-------+
```

> **Note:** `COALESCE(marks, 0)` does the same thing and works in every
> database. `IFNULL` is MySQL only.

---

# Common Errors

## Error 1: Unknown Column

```sql
SELECT nam FROM students;
```

### Error

```text
ERROR 1054 (42S22): Unknown column 'nam' in 'field list'
```

### Solution

Check the spelling of the column name.

```sql
DESC students;
```

---

## Error 2: Table Doesn't Exist

```sql
SELECT name FROM student;
```

### Error

```text
ERROR 1146 (42S02): Table 'training.student' doesn't exist
```

### Solution

The table is named `students`, not `student`.

```sql
SHOW TABLES;
```

---

## Error 3: Using an Alias in WHERE

```sql
SELECT name AS score FROM students WHERE score > 50;
```

### Error

```text
ERROR 1054 (42S22): Unknown column 'score' in 'where clause'
```

### Reason

`WHERE` runs **before** `SELECT`, so the alias does not exist yet.

### Solution

Repeat the real column name in `WHERE`.

```sql
SELECT marks AS score FROM students WHERE marks > 50;
```

---

## Error 4: Missing Quotes Around Text

```sql
SELECT name FROM students WHERE city = Chennai;
```

### Error

```text
ERROR 1054 (42S22): Unknown column 'Chennai' in 'where clause'
```

### Reason

Without quotes, MySQL thinks `Chennai` is a **column name**.

### Solution

```sql
SELECT name FROM students WHERE city = 'Chennai';
```

---

## Error 5: Missing BY in ORDER BY

```sql
SELECT name FROM students ORDER marks;
```

### Error

```text
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual
that corresponds to your MySQL server version for the right syntax to use
near 'marks' at line 1
```

### Solution

```sql
SELECT name FROM students ORDER BY marks;
```

---

## Error 6: Comparing with NULL

```sql
SELECT name FROM students WHERE marks = NULL;
```

### Result

```
Empty set
```

There is **no error message**, which makes this harder to spot than a real
error. The query simply returns nothing.

### Solution

```sql
SELECT name FROM students WHERE marks IS NULL;
```

---

# Commands Covered

| Command                     | Purpose                                |
| --------------------------- | -------------------------------------- |
| `SELECT *`                  | Shows all columns                      |
| `SELECT col1, col2`         | Shows selected columns                 |
| `SELECT DISTINCT`           | Removes duplicate rows                 |
| `WHERE`                     | Filters rows                           |
| `AND` / `OR`                | Combines conditions                    |
| `ORDER BY ... ASC / DESC`   | Sorts the result                       |
| `LIMIT`                     | Restricts the number of rows           |
| `LIMIT ... OFFSET`          | Skips rows, then restricts             |
| `AS`                        | Renames a column in the output         |
| `IS NULL` / `IS NOT NULL`   | Tests for missing values               |
| `IFNULL(col, value)`        | Replaces `NULL` with another value     |

---

# Summary

| Clause     | Question it answers          |
| ---------- | ---------------------------- |
| `SELECT`   | Which columns do I want?     |
| `FROM`     | Which table are they in?     |
| `WHERE`    | Which rows do I want?        |
| `ORDER BY` | In what order?               |
| `LIMIT`    | How many rows?               |

Rules worth remembering:

* Text values need **single quotes**; column names do not.
* Comparison uses a **single** `=`.
* `NULL` needs `IS NULL`, never `= NULL`.
* An alias works in `ORDER BY` but **not** in `WHERE`.
* `LIMIT` is meaningless without `ORDER BY`.

---

# Practice Questions

1. Display all columns from the `students` table.
2. Display only `name`, `course` and `marks`.
3. Display the distinct courses.
4. Display students whose marks are greater than 60.
5. Display students from `Kochi`.
6. Display students from `Hyderabad` whose age is less than 21.
7. Display all students sorted by name in ascending order.
8. Display the top 5 students by marks.
9. Display students ranked 3rd to 5th by marks.
10. Display `name` with the heading `Student` and `marks` with the heading `Score`.
11. Add a column showing marks out of 200 (`marks * 2`).
12. Display students whose marks are missing.
13. Display students whose course is missing.
14. Display all students, showing `0` where marks are missing.
15. Explain why `WHERE marks = NULL` returns nothing.

---

# Class Summary

In this notebook, you learned:

* Reading all columns and selected columns using `SELECT`
* Removing duplicate rows using `DISTINCT`
* Filtering rows using `WHERE` with comparison operators
* Combining conditions using `AND` and `OR`
* Sorting results using `ORDER BY`, including sorting by two columns
* Restricting rows using `LIMIT` and `OFFSET`
* Renaming output columns using aliases
* Creating calculated columns using expressions
* Handling missing values using `IS NULL`, `IS NOT NULL` and `IFNULL`
* The order in which MySQL actually runs a `SELECT`

You are now ready to learn the next topic: **Operators and Clauses — `IN`,
`BETWEEN`, `LIKE` and `EXISTS`**.
