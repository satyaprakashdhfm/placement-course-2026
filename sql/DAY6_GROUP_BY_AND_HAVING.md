# Grouping Data using GROUP BY and HAVING

In this section, we will learn how to summarise data by group instead of by row,
and how to filter those groups.

---

# Why Grouping?

In the previous topic, an aggregate function collapsed the **whole table** into
one row:

```sql
SELECT AVG(marks) FROM students;      -- one number for everybody
```

That answers *"what is the class average?"* but not
*"what is the average in each city?"*

`GROUP BY` answers the second question. It splits the rows into groups and
applies the aggregate **separately to each group**.

---

# How GROUP BY Works

```text
   10 students                          4 cities
   +----------------+                 +------------------+
   | Hyderabad  78  |                 | Hyderabad  65.67 |
   | Chennai    95  |    GROUP BY     | Chennai    74.50 |
   | Hyderabad  38  |  ------------>  | Kochi      55.50 |
   | Kochi      66  |     city        | Pune       84.00 |
   | ...            |                 +------------------+
   +----------------+
```

Some important points:

* One row comes out **per group**.
* The aggregate is calculated **inside** each group.
* `GROUP BY` always comes **after** `WHERE`.
* Grouping by more columns creates more, smaller groups.

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

# 1. Basic GROUP BY

### Syntax

```sql
SELECT column_name, aggregate_function(column_name)
FROM table_name
GROUP BY column_name;
```

### Example

```sql
SELECT city, COUNT(*) AS students FROM students GROUP BY city;
```

### Expected Output

```
+-----------+----------+
| city      | students |
+-----------+----------+
| Hyderabad |        3 |
| Chennai   |        3 |
| Kochi     |        2 |
| Pune      |        2 |
+-----------+----------+
```

Ten students became four rows — one per city.

> **Note:** `GROUP BY` does not sort the result. Add `ORDER BY` if you need a
> particular order.

---

# 2. GROUP BY with Several Aggregates

You can use as many aggregate functions as you like in one query.

### Example

```sql
SELECT city, COUNT(*) AS students, ROUND(AVG(marks),2) AS avg_marks
FROM students
GROUP BY city
ORDER BY avg_marks DESC;
```

### Expected Output

```
+-----------+----------+-----------+
| city      | students | avg_marks |
+-----------+----------+-----------+
| Pune      |        2 |     84.00 |
| Chennai   |        3 |     74.50 |
| Hyderabad |        3 |     65.67 |
| Kochi     |        2 |     55.50 |
+-----------+----------+-----------+
```

Chennai shows **3 students** but its average is calculated from only **2**,
because `Meera Nair` has no marks and `AVG` ignores `NULL`.

---

# 3. The Golden Rule of GROUP BY

> Every column in `SELECT` must either be **inside an aggregate function**, or
> **listed in the `GROUP BY`**.

### Why?

```sql
SELECT city, name, COUNT(*) FROM students GROUP BY city;
```

Hyderabad has three students. Which **one** name should the single Hyderabad row
show? The question has no answer, so MySQL refuses.

### Error

```text
ERROR 1055 (42000): Expression #2 of SELECT list is not in GROUP BY clause and
contains nonaggregated column 'training.students.name' which is not functionally
dependent on columns in GROUP BY clause; this is incompatible with
sql_mode=only_full_group_by
```

### Correct

```sql
SELECT city, COUNT(*) AS students FROM students GROUP BY city;
```

---

# 4. Grouping and NULL

`GROUP BY` puts **all `NULL` values into one group**.

### Example

```sql
SELECT course, COUNT(*) AS students FROM students GROUP BY course ORDER BY course;
```

### Expected Output

```
+--------+----------+
| course | students |
+--------+----------+
| NULL   |        1 |
| DSA    |        2 |
| Java   |        2 |
| Python |        3 |
| SQL    |        2 |
+--------+----------+
```

`Rohit Sinha`, who has no course, forms his own `NULL` group.

> **Note:** This is different from `=`, which never matches `NULL`. `GROUP BY`
> treats all `NULL`s as equal to each other.

---

# 5. Building Calculations from Aggregates

Aggregates are ordinary expressions — you can do arithmetic with them.

### Example

```sql
SELECT city, COUNT(*) AS n,
       MIN(marks) AS lowest,
       MAX(marks) AS highest,
       MAX(marks) - MIN(marks) AS spread
FROM students
WHERE marks IS NOT NULL
GROUP BY city
ORDER BY spread DESC;
```

### Expected Output

```
+-----------+---+--------+---------+--------+
| city      | n | lowest | highest | spread |
+-----------+---+--------+---------+--------+
| Hyderabad | 3 |     38 |      81 |     43 |
| Chennai   | 2 |     54 |      95 |     41 |
| Kochi     | 2 |     45 |      66 |     21 |
| Pune      | 2 |     78 |      90 |     12 |
+-----------+---+--------+---------+--------+
```

**Spread** tells you how consistent a group is. Pune's students are close
together; Hyderabad's are far apart. The average alone hides that.

---

# 6. Grouping by Two Columns

### Example

```sql
SELECT city, age, COUNT(*) AS students
FROM students
GROUP BY city, age
ORDER BY city, age;
```

### Expected Output

```
+-----------+------+----------+
| city      | age  | students |
+-----------+------+----------+
| Chennai   |   21 |        1 |
| Chennai   |   22 |        2 |
| Hyderabad |   20 |        1 |
| Hyderabad |   21 |        2 |
| Kochi     |   20 |        1 |
| Kochi     |   23 |        1 |
| Pune      |   23 |        1 |
| Pune      |   24 |        1 |
+-----------+------+----------+
```

One row per **combination** of city and age. Four cities became eight groups.

> **Note:** More grouping columns means more groups, each containing fewer rows.

---

# 7. The HAVING Clause

`HAVING` filters **groups**, the same way `WHERE` filters **rows**.

### Syntax

```sql
SELECT column_name, aggregate_function(column_name)
FROM table_name
GROUP BY column_name
HAVING condition_on_aggregate;
```

### Example

Cities with more than two students.

```sql
SELECT city, COUNT(*) AS students
FROM students
GROUP BY city
HAVING COUNT(*) > 2;
```

### Expected Output

```
+-----------+----------+
| city      | students |
+-----------+----------+
| Hyderabad |        3 |
| Chennai   |        3 |
+-----------+----------+
```

Kochi and Pune have only two students each, so those groups were removed.

---

# 8. WHERE vs HAVING

This is the most important comparison in this topic.

| Point                  | `WHERE`               | `HAVING`             |
| ---------------------- | --------------------- | -------------------- |
| Filters                | Individual **rows**   | Whole **groups**     |
| Runs                   | **Before** grouping   | **After** grouping   |
| Aggregates allowed     | ❌ No                 | ✅ Yes               |
| Needs `GROUP BY`       | No                    | Almost always        |

### Proof

```sql
SELECT city, COUNT(*) FROM students WHERE COUNT(*) > 2 GROUP BY city;
```

### Error

```text
ERROR 1111 (HY000): Invalid use of group function
```

`WHERE` runs before the groups exist, so `COUNT(*)` has no meaning yet.

---

# 9. HAVING with an Average

### Example

Cities whose average marks are above 70.

```sql
SELECT city, ROUND(AVG(marks),1) AS avg_marks
FROM students
GROUP BY city
HAVING AVG(marks) > 70
ORDER BY avg_marks DESC;
```

### Expected Output

```
+---------+-----------+
| city    | avg_marks |
+---------+-----------+
| Pune    |      84.0 |
| Chennai |      74.5 |
+---------+-----------+
```

---

# 10. Using WHERE and HAVING Together

They work at different stages, so a query often needs both.

### Example

*Among students who passed, show the average per city, for cities with at least
two such students.*

```sql
SELECT city, COUNT(*) AS passed, ROUND(AVG(marks),2) AS avg_marks
FROM students
WHERE marks >= 50          -- 1. keep only passing students
GROUP BY city              -- 2. group what is left
HAVING COUNT(*) >= 2       -- 3. keep cities with 2 or more of them
ORDER BY avg_marks DESC;
```

### Expected Output

```
+-----------+--------+-----------+
| city      | passed | avg_marks |
+-----------+--------+-----------+
| Pune      |      2 |     84.00 |
| Hyderabad |      2 |     79.50 |
| Chennai   |      2 |     74.50 |
+-----------+--------+-----------+
```

Compare Hyderabad here — **79.50** — with the 65.67 in section 2. Karan Patel's
38 was removed by `WHERE` **before** the average was calculated.

> **The order of operations changes the answer.** This is the single best example
> to explain why `WHERE` and `HAVING` are not interchangeable.

---

# 11. Order in Which MySQL Runs the Query

| Step | Clause     | What happens             |
| ---- | ---------- | ------------------------ |
| 1    | `FROM`     | Fetch the table          |
| 2    | `WHERE`    | Drop unwanted **rows**   |
| 3    | `GROUP BY` | Form the groups          |
| 4    | `HAVING`   | Drop unwanted **groups** |
| 5    | `SELECT`   | Work out the columns     |
| 6    | `ORDER BY` | Sort                     |
| 7    | `LIMIT`    | Cut                      |

This table explains three rules you have already met:

* `WHERE` cannot use an aggregate — they do not exist until step 3.
* `HAVING` can, because step 4 is after grouping.
* `ORDER BY` can use a `SELECT` alias (6 is after 5); `WHERE` cannot (2 is before 5).

---

# 12. Finding Duplicates — The Classic Pattern

`GROUP BY` with `HAVING COUNT(*) > 1` is how you find repeated values. This
appears in almost every SQL interview.

### Example

```sql
SELECT course, COUNT(*) AS n
FROM students
GROUP BY course
HAVING COUNT(*) > 1
ORDER BY n DESC;
```

### Expected Output

```
+--------+---+
| course | n |
+--------+---+
| Python | 3 |
| SQL    | 2 |
| Java   | 2 |
| DSA    | 2 |
+--------+---+
```

To find duplicate **emails** in a real table, the query is exactly the same
shape:

```sql
SELECT email, COUNT(*) FROM users GROUP BY email HAVING COUNT(*) > 1;
```

---

# 13. Grouping by a CASE Expression

You can group by a calculated value, not just a column.

### Example

Count students in each grade band.

```sql
SELECT CASE WHEN marks >= 75   THEN 'Distinction'
            WHEN marks >= 50   THEN 'Pass'
            WHEN marks IS NULL THEN 'Not graded'
            ELSE 'Fail'
       END AS band,
       COUNT(*) AS students
FROM students
GROUP BY band
ORDER BY students DESC, band;
```

### Expected Output

```
+-------------+----------+
| band        | students |
+-------------+----------+
| Distinction |        5 |
| Fail        |        2 |
| Pass        |        2 |
| Not graded  |        1 |
+-------------+----------+
```

Note that `GROUP BY band` uses the **alias**. This works because `GROUP BY` is
allowed to see `SELECT` aliases in MySQL.

> **Note:** `Pass` and `Fail` are tied on 2. The `ORDER BY students DESC, band`
> makes the order predictable — without the second sort key, either could come
> first.

---

# 14. WITH ROLLUP — Adding a Total Row

`WITH ROLLUP` adds a grand-total row automatically.

### Example

```sql
SELECT city, COUNT(*) AS n FROM students GROUP BY city WITH ROLLUP;
```

### Expected Output

```
+-----------+----+
| city      | n  |
+-----------+----+
| Chennai   |  3 |
| Hyderabad |  3 |
| Kochi     |  2 |
| Pune      |  2 |
| NULL      | 10 |
+-----------+----+
```

The last row, with `city` shown as `NULL`, is the **total** — all 10 students.

> **Note:** The total row is marked by `NULL` in the grouped column, which is
> confusing if the column itself contains `NULL`s. Use `GROUPING()` to tell them
> apart.

---

# Common Errors

## Error 1: Selecting a Column That Is Not Grouped

```sql
SELECT city, name, COUNT(*) FROM students GROUP BY city;
```

### Error

```text
ERROR 1055 (42000): Expression #2 of SELECT list is not in GROUP BY clause and
contains nonaggregated column 'training.students.name' which is not functionally
dependent on columns in GROUP BY clause; this is incompatible with
sql_mode=only_full_group_by
```

### Solution

Either remove the column, put it in `GROUP BY`, or wrap it in an aggregate.

```sql
SELECT city, COUNT(*) AS students FROM students GROUP BY city;
```

---

## Error 2: Using an Aggregate in WHERE

```sql
SELECT city, COUNT(*) FROM students WHERE COUNT(*) > 2 GROUP BY city;
```

### Error

```text
ERROR 1111 (HY000): Invalid use of group function
```

### Solution

```sql
SELECT city, COUNT(*) FROM students GROUP BY city HAVING COUNT(*) > 2;
```

---

## Error 3: Using HAVING Where WHERE Would Do

```sql
SELECT city, COUNT(*) FROM students GROUP BY city HAVING city = 'Pune';
```

This **works**, but it is wrong practice. MySQL groups **all** the cities first
and then throws almost all of them away.

### Better

```sql
SELECT city, COUNT(*) FROM students WHERE city = 'Pune' GROUP BY city;
```

**Rule:** filter rows as early as possible. Use `WHERE` for columns, `HAVING`
only for aggregates.

---

## Error 4: Expecting COUNT(*) to Skip NULLs

```sql
SELECT COUNT(*) AS rows_total, COUNT(marks) AS with_marks FROM students;
```

### Result

```
+------------+------------+
| rows_total | with_marks |
+------------+------------+
|         10 |          9 |
+------------+------------+
```

There is no error — just a wrong answer if you assumed they were the same.
`COUNT(*)` counts rows; `COUNT(column)` skips `NULL`.

---

# Commands Covered

| Command                     | Purpose                                       |
| --------------------------- | --------------------------------------------- |
| `GROUP BY column`           | Creates one row per group                     |
| `GROUP BY col1, col2`       | Creates one row per combination               |
| `HAVING condition`          | Filters the groups                            |
| `WHERE` + `GROUP BY`        | Filters rows before grouping                  |
| `GROUP BY` on a `CASE`      | Groups by a calculated value                  |
| `WITH ROLLUP`               | Adds a grand-total row                        |
| `HAVING COUNT(*) > 1`       | Finds duplicate values                        |

---

# Summary

| If you want to...                      | Use                          |
| -------------------------------------- | ---------------------------- |
| Summarise the whole table              | Aggregate alone              |
| Summarise per group                    | `GROUP BY`                   |
| Remove unwanted rows first             | `WHERE`                      |
| Remove unwanted groups after           | `HAVING`                     |
| Find repeated values                   | `GROUP BY … HAVING COUNT(*) > 1` |
| Add a total row                        | `WITH ROLLUP`                |

Rules worth remembering:

* Every selected column must be **grouped** or **aggregated**.
* `WHERE` filters rows **before** grouping; `HAVING` filters groups **after**.
* Only `HAVING` may contain an aggregate.
* All `NULL`s form a **single** group.
* Filtering with `WHERE` first can change the aggregate result — as Hyderabad's
  average showed.

---

# Practice Questions

1. Count the students in each city.
2. Show the average marks per city, highest average first.
3. Show the highest and lowest marks in each city.
4. Count the students in each course.
5. Which group does `Rohit Sinha` fall into, and why?
6. Show the number of students per age.
7. Show the spread (highest minus lowest) of marks in each city.
8. Count students grouped by city **and** age.
9. Show cities with more than two students.
10. Show cities whose average marks are above 70.
11. Among students scoring 50 or more, show the average per city for cities with
    at least two such students.
12. Explain why Hyderabad's average changes between questions 2 and 11.
13. Find every course taken by more than one student.
14. Count students in each grade band using `CASE`.
15. Add a grand-total row to question 1 using `WITH ROLLUP`.
16. Why does `WHERE COUNT(*) > 2` fail but `HAVING COUNT(*) > 2` work?

---

# Class Summary

In this notebook, you learned:

* Summarising data per group using `GROUP BY`
* The golden rule — every selected column must be grouped or aggregated
* How `GROUP BY` treats `NULL` values as one group
* Building calculations from aggregates, such as spread
* Grouping by more than one column
* Filtering groups using `HAVING`
* The difference between `WHERE` and `HAVING`, and why the order changes results
* The full clause execution order of a `SELECT`
* Finding duplicates using `GROUP BY … HAVING COUNT(*) > 1`
* Grouping by a `CASE` expression
* Adding a total row using `WITH ROLLUP`

You are now ready to learn the next topic: **Joins — combining data from more
than one table**.
