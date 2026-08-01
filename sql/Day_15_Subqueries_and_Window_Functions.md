# Day 15 · Subqueries & Window Functions

**Duration:** 50–60 Minutes

### Learning Outcomes
- Write **subqueries** in `WHERE`, `SELECT` and `FROM`.
- Tell a **scalar**, **multi-row** and **correlated** subquery apart.
- Use **window functions**: `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`.
- Know exactly how those three differ when values **tie**.
- Split windows with **`PARTITION BY`**.

---

## 1. What is a Subquery?

A **query inside another query**. The inner one runs first, and its result is
used by the outer one.

```sql
SELECT name, marks
FROM students
WHERE marks > (SELECT AVG(marks) FROM students);
```

```text
name         | marks
-------------+------
Rahul Verma  | 78
Anita Sharma | 95
Vikram Rao   | 81
Arjun Mehta  | 90
Rohit Sinha  | 78
```

The inner query returns `69.44`; the outer becomes `WHERE marks > 69.44`.

**Why not just type 69.44?** Because the average changes every time the data
changes. The subquery is always right.

---

## 2. Three Kinds of Subquery

| Kind | Returns | Used with |
|---|---|---|
| **Scalar** | one single value | `=`, `>`, `<` |
| **Multi-row** | one column, many rows | `IN`, `EXISTS` |
| **Correlated** | re-runs for each outer row | `EXISTS`, `SELECT` |

### Scalar

```sql
SELECT name, marks FROM students WHERE marks = (SELECT MAX(marks) FROM students);
```

```text
name         | marks
-------------+------
Anita Sharma | 95
```

### Multi-row — needs `IN`, not `=`

```sql
SELECT name
FROM students
WHERE course_id IN (SELECT course_id FROM courses WHERE duration > 40);
```

```text
name
-----------
Rahul Verma
Karan Patel
Priya Nair
Sneha Iyer
Arjun Mehta
Divya Menon
Meera Nair
```

Using `=` here fails, because the inner query returns three course ids.

### Correlated — the inner query depends on the outer

```sql
SELECT c.course_name,
       (SELECT COUNT(*) FROM students s WHERE s.course_id = c.course_id) AS enrolled
FROM courses c;
```

```text
course_name | enrolled
------------+---------
Python      | 3
SQL         | 2
Java        | 2
DSA         | 2
Cloud       | 0
```

Notice the inner query mentions `c.course_id` — a column from the **outer**
query. It cannot run on its own; it runs once **per course**.

**Key Note:** correlated subqueries are slower, because they run repeatedly. The
same answer usually comes from a `LEFT JOIN` + `GROUP BY` (Day 13). Know both.

---

## 3. Subquery in FROM — a Derived Table

Treat a query's result as a temporary table:

```sql
SELECT city, avg_marks
FROM (SELECT city, ROUND(AVG(marks), 2) AS avg_marks
      FROM students
      GROUP BY city)
WHERE avg_marks > 70;
```

```text
city    | avg_marks
--------+----------
Chennai | 74.5
Pune    | 84.0
```

This is how you filter on an aggregate of an aggregate, or apply two levels of
grouping.

---

## 4. Where Subqueries Can Go

| Position | Example | Purpose |
|---|---|---|
| `WHERE` | `WHERE marks > (SELECT AVG…)` | compare against a computed value |
| `SELECT` | `(SELECT COUNT(*) …) AS n` | add a calculated column |
| `FROM` | `FROM (SELECT …)` | query a result set |
| `HAVING` | `HAVING AVG(marks) > (SELECT …)` | compare groups |

---

## 5. Window Functions — Keeping the Rows

An **aggregate** collapses rows. A **window function** performs the same kind of
calculation but **keeps every row**:

```text
   AGGREGATE                        WINDOW
   10 rows -> 1 row                 10 rows -> 10 rows
   (you lose the detail)            (detail + the calculation)
```

The syntax is a function followed by **`OVER (...)`**:

```sql
function() OVER (PARTITION BY column ORDER BY column)
```

- `PARTITION BY` — split into groups (optional). Like `GROUP BY`, but rows stay.
- `ORDER BY` — the order **inside** each window.

---

## 6. ROW_NUMBER, RANK, DENSE_RANK

All three number the rows. They differ **only when values tie** — and that is
the whole exam question.

```sql
SELECT name, marks,
       ROW_NUMBER() OVER (ORDER BY marks DESC) AS row_number,
       RANK()       OVER (ORDER BY marks DESC) AS rank,
       DENSE_RANK() OVER (ORDER BY marks DESC) AS dense_rank
FROM students
WHERE marks IS NOT NULL;
```

```text
name         | marks | row_number | rank | dense_rank
-------------+-------+------------+------+-----------
Anita Sharma | 95    | 1          | 1    | 1
Arjun Mehta  | 90    | 2          | 2    | 2
Vikram Rao   | 81    | 3          | 3    | 3
Rahul Verma  | 78    | 4          | 4    | 4
Rohit Sinha  | 78    | 5          | 4    | 4
Priya Nair   | 66    | 6          | 6    | 5
Sneha Iyer   | 54    | 7          | 7    | 6
Divya Menon  | 45    | 8          | 8    | 7
Karan Patel  | 38    | 9          | 9    | 8
```

**Rahul and Rohit both scored 78.** Look at that pair, then the row after:

| Function | On the tie | Next value | In words |
|---|---|---|---|
| `ROW_NUMBER()` | **4, 5** | 6 | always different, ties broken arbitrarily |
| `RANK()` | **4, 4** | **6** | same rank, then **skips** a number |
| `DENSE_RANK()` | **4, 4** | **5** | same rank, **no gap** |

Remember it as: *"RANK leaves a hole, DENSE_RANK does not."* This is asked in
almost every SQL interview.

---

## 7. PARTITION BY — Restarting the Numbering

```sql
SELECT name, city, marks,
       RANK() OVER (PARTITION BY city ORDER BY marks DESC) AS rank_in_city
FROM students
WHERE marks IS NOT NULL;
```

```text
name         | city      | marks | rank_in_city
-------------+-----------+-------+-------------
Anita Sharma | Chennai   | 95    | 1
Sneha Iyer   | Chennai   | 54    | 2
Vikram Rao   | Hyderabad | 81    | 1
Rahul Verma  | Hyderabad | 78    | 2
Karan Patel  | Hyderabad | 38    | 3
Priya Nair   | Kochi     | 66    | 1
Divya Menon  | Kochi     | 45    | 2
Arjun Mehta  | Pune      | 90    | 1
Rohit Sinha  | Pune      | 78    | 2
```

The numbering **restarts at 1 in every city** — four separate "top of the
class" answers, in one query.

### GROUP BY vs PARTITION BY

| | `GROUP BY` | `PARTITION BY` |
|---|---|---|
| Rows returned | one per group | **all of them** |
| Detail | lost | kept |
| Used in | the query itself | inside `OVER ()` |

---

## 8. Aggregates as Window Functions

Any aggregate can take an `OVER` clause — showing a total *beside* each row:

```sql
SELECT name, city, marks,
       ROUND(AVG(marks) OVER (PARTITION BY city), 2) AS city_avg,
       ROUND(marks - AVG(marks) OVER (PARTITION BY city), 2) AS diff
FROM students
WHERE marks IS NOT NULL;
```

```text
name         | city      | marks | city_avg | diff
-------------+-----------+-------+----------+-------
Anita Sharma | Chennai   | 95    | 74.5     | 20.5
Sneha Iyer   | Chennai   | 54    | 74.5     | -20.5
Rahul Verma  | Hyderabad | 78    | 65.67    | 12.33
Karan Patel  | Hyderabad | 38    | 65.67    | -27.67
Vikram Rao   | Hyderabad | 81    | 65.67    | 15.33
Priya Nair   | Kochi     | 66    | 55.5     | 10.5
Divya Menon  | Kochi     | 45    | 55.5     | -10.5
Arjun Mehta  | Pune      | 90    | 84.0     | 6.0
Rohit Sinha  | Pune      | 78    | 84.0     | -6.0
```

> ⚠️ Round the **whole** subtraction, not just the average. Writing
> `marks - ROUND(AVG(...), 2)` leaks floating-point noise like
> `12.329999999999998` into your output.

Doing this with `GROUP BY` alone is impossible — you would lose the individual
names. That is the point of window functions.

---

## 9. Top-N Per Group

The classic use: *"the best student in each city."* A window function is
computed **after** `WHERE`, so it must be wrapped in a subquery to filter on:

```sql
SELECT name, city, marks
FROM (SELECT name, city, marks,
             RANK() OVER (PARTITION BY city ORDER BY marks DESC) AS r
      FROM students
      WHERE marks IS NOT NULL)
WHERE r = 1;
```

```text
name         | city      | marks
-------------+-----------+------
Anita Sharma | Chennai   | 95
Vikram Rao   | Hyderabad | 81
Priya Nair   | Kochi     | 66
Arjun Mehta  | Pune      | 90
```

**Key Note:** `WHERE r = 1` cannot go in the inner query — window functions run
after `WHERE`. Learn this two-level shape; it answers a huge class of questions.

---

## 10. Common Mistakes

**1. `=` with a multi-row subquery** — use `IN`.

**2. Filtering a window function in `WHERE`** — it does not exist yet. Wrap the
query and filter outside.

**3. Confusing `RANK` and `DENSE_RANK`** — `RANK` skips numbers after a tie.

**4. Expecting `ROW_NUMBER` to be stable on ties** — the order between equal
rows is arbitrary unless you add a tie-breaker: `ORDER BY marks DESC, id`.

**5. Using a correlated subquery where a join is far faster.**

**6. Forgetting NULLs** — `WHERE marks IS NOT NULL` keeps Meera Nair out of the
rankings. Without it she would be ranked too.

---

## 11. Summary

- A **subquery** is a query inside a query: **scalar** (one value),
  **multi-row** (use `IN`), or **correlated** (re-runs per outer row).
- Subqueries can sit in `WHERE`, `SELECT`, `FROM` and `HAVING`.
- **Window functions** calculate across rows **without collapsing them**, using
  `OVER (PARTITION BY … ORDER BY …)`.
- On a tie: `ROW_NUMBER` = 4,5 · `RANK` = 4,4 then **6** · `DENSE_RANK` = 4,4
  then **5**.
- `PARTITION BY` restarts the calculation per group but keeps every row.
- **Top-N per group** = window function inside a subquery, filtered outside.

---

## 12. Practice Questions

1. Students scoring above the class average.
2. The student with the highest marks, using a subquery.
3. Students on any course longer than 40 days.
4. Add a column to `courses` showing how many students each has.
5. Cities whose average marks are above 70, using a subquery in `FROM`.
6. Number every student from best to worst with `ROW_NUMBER()`.
7. Add `RANK()` and `DENSE_RANK()` and explain the two ties.
8. Why does `RANK` jump from 4 to 6?
9. Rank the students **within each city**.
10. Show each student beside their city's average.
11. Find the top student in every city.
12. Find the **second** highest mark overall (two ways).
13. Why can `WHERE rank = 1` not go in the same query as the `RANK()`?
14. What is the difference between `GROUP BY` and `PARTITION BY`?
