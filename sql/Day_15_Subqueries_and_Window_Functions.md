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
      GROUP BY city) AS city_stats
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

> ⚠️ **MySQL requires the alias** (`AS city_stats`). Leave it out and you get
> *"Every derived table must have its own alias"*. 📌 SQLite and PostgreSQL
> allow an unnamed derived table — another reason SQLite code fails on MySQL.

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

> ⚠️ **Window functions need MySQL 8.0+.** On MySQL 5.7 they are a syntax
> error, and you emulate ranking with user variables — an ugly trick you may
> still meet on older systems. 📌 SQLite has had them since 3.25, PostgreSQL
> since 8.4.

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
      WHERE marks IS NOT NULL) AS ranked
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

## 12. 🔺 ADVANCED — Teacher Reference

*Not in the student handout. Use these when the class is ahead, or to answer
"can SQL do X?" questions.*

### 12.1 CTEs — naming a subquery (`WITH`)

A **Common Table Expression** is a subquery given a name up front. Same result
as a derived table, far easier to read, and it can be referenced twice.

```sql
WITH city_stats AS (
    SELECT city, ROUND(AVG(marks),2) AS avg_marks, COUNT(*) AS n
    FROM students WHERE marks IS NOT NULL GROUP BY city
)
SELECT c.city, c.avg_marks, c.n
FROM city_stats c
WHERE c.avg_marks > (SELECT AVG(avg_marks) FROM city_stats)
ORDER BY c.avg_marks DESC;
```

```text
+---------+-----------+---+
| city    | avg_marks | n |
+---------+-----------+---+
| Pune    |     84.00 | 2 |
| Chennai |     74.50 | 2 |
+---------+-----------+---+
```

`city_stats` is used **twice** — once in `FROM`, once inside the `WHERE`. A
derived table would have to be written out twice.

**Teaching point:** CTE vs derived table vs view — *CTE = named for one query ·
derived table = anonymous, inline · view = stored permanently.* Needs MySQL 8.0+.

### 12.2 Recursive CTEs — hierarchies of unknown depth

The one thing plain SQL genuinely cannot do without recursion.

```sql
WITH RECURSIVE org AS (
    SELECT emp_id, emp_name, manager_id, 1 AS level,
           CAST(emp_name AS CHAR(200)) AS path
    FROM employees WHERE manager_id IS NULL            -- anchor: the top
    UNION ALL
    SELECT e.emp_id, e.emp_name, e.manager_id, o.level + 1,
           CONCAT(o.path, ' > ', e.emp_name)
    FROM employees e JOIN org o ON e.manager_id = o.emp_id   -- recursive part
)
SELECT level, emp_name, path FROM org ORDER BY level, emp_name;
```

```text
+-------+----------+-----------------------+
| level | emp_name | path                  |
+-------+----------+-----------------------+
|     1 | Anil     | Anil                  |
|     2 | Bhavna   | Anil > Bhavna         |
|     2 | Chetan   | Anil > Chetan         |
|     3 | Deepa    | Anil > Bhavna > Deepa |
|     3 | Esha     | Anil > Bhavna > Esha  |
+-------+----------+-----------------------+
```

**Shape to memorise:** anchor query → `UNION ALL` → recursive query joining back
to the CTE's own name.

⚠️ The `CAST(... AS CHAR(200))` is **required**. Without it MySQL fixes the
column width from the anchor row and silently truncates longer paths. Runaway
recursion stops at `cte_max_recursion_depth` (default 1000).

### 12.3 The rest of the window functions

| Function | Gives |
|---|---|
| `LAG(col, n)` | value from **n rows back** |
| `LEAD(col, n)` | value **n rows ahead** |
| `FIRST_VALUE` / `LAST_VALUE` | first / last in the window |
| `NTILE(n)` | split rows into n buckets |
| `PERCENT_RANK()` | relative standing, 0 to 1 |
| `CUME_DIST()` | cumulative distribution |

```sql
SELECT name, marks,
       LAG(marks)  OVER (ORDER BY marks DESC) AS above,
       LEAD(marks) OVER (ORDER BY marks DESC) AS below,
       marks - LEAD(marks) OVER (ORDER BY marks DESC) AS lead_over_next
FROM students WHERE marks IS NOT NULL ORDER BY marks DESC;
```

```text
+--------------+-------+-------+-------+----------------+
| name         | marks | above | below | lead_over_next |
+--------------+-------+-------+-------+----------------+
| Anita Sharma |    95 |  NULL |    90 |              5 |
| Arjun Mehta  |    90 |    95 |    81 |              9 |
| Vikram Rao   |    81 |    90 |    78 |              3 |
| Rahul Verma  |    78 |    81 |    78 |              0 |
| Rohit Sinha  |    78 |    78 |    66 |             12 |
| Priya Nair   |    66 |    78 |    54 |             12 |
| Sneha Iyer   |    54 |    66 |    45 |              9 |
| Divya Menon  |    45 |    54 |    38 |              7 |
| Karan Patel  |    38 |    45 |  NULL |           NULL |
+--------------+-------+-------+-------+----------------+
```

`LAG`/`LEAD` are how you compare a row to its neighbour — month-on-month growth,
price changes, time between events — **with no self-join**.

```sql
SELECT name, marks,
       NTILE(4) OVER (ORDER BY marks DESC) AS quartile,
       ROUND(PERCENT_RANK() OVER (ORDER BY marks DESC),3) AS pct_rank
FROM students WHERE marks IS NOT NULL;
```

```text
+--------------+-------+----------+----------+
| name         | marks | quartile | pct_rank |
+--------------+-------+----------+----------+
| Anita Sharma |    95 |        1 |        0 |
| Arjun Mehta  |    90 |        1 |    0.125 |
| Vikram Rao   |    81 |        1 |     0.25 |
| Rahul Verma  |    78 |        2 |    0.375 |
| Rohit Sinha  |    78 |        2 |    0.375 |
| Priya Nair   |    66 |        3 |    0.625 |
| Sneha Iyer   |    54 |        3 |     0.75 |
| Divya Menon  |    45 |        4 |    0.875 |
| Karan Patel  |    38 |        4 |        1 |
+--------------+-------+----------+----------+
```

`NTILE(4)` is how you say "top quartile"; `PERCENT_RANK` is how you say "top 10%".

### 12.4 Frame clauses — running totals and moving averages

`OVER (...)` can take a **frame**: which rows around the current one to include.

```sql
SELECT name, joined_on, marks,
       SUM(marks) OVER (ORDER BY joined_on
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total,
       ROUND(AVG(marks) OVER (ORDER BY joined_on
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW),2)      AS moving_avg_3
FROM students WHERE marks IS NOT NULL ORDER BY joined_on;
```

```text
+--------------+------------+-------+---------------+--------------+
| name         | joined_on  | marks | running_total | moving_avg_3 |
+--------------+------------+-------+---------------+--------------+
| Rahul Verma  | 2025-01-15 |    78 |            78 |        78.00 |
| Anita Sharma | 2025-01-20 |    95 |           173 |        86.50 |
| Karan Patel  | 2025-02-01 |    38 |           211 |        70.33 |
| Priya Nair   | 2025-02-10 |    66 |           277 |        66.33 |
| Vikram Rao   | 2025-03-05 |    81 |           358 |        61.67 |
| Sneha Iyer   | 2025-03-12 |    54 |           412 |        67.00 |
| Arjun Mehta  | 2025-04-02 |    90 |           502 |        75.00 |
| Divya Menon  | 2025-04-18 |    45 |           547 |        63.00 |
| Rohit Sinha  | 2025-05-01 |    78 |           625 |        71.00 |
+--------------+------------+-------+---------------+--------------+
```

| Frame | Meaning |
|---|---|
| `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` | running total |
| `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` | 3-row moving average |
| `ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING` | remaining total |
| `RANGE BETWEEN ...` | by **value**, not row count — ties share a frame |

⚠️ **The default frame is `RANGE ... CURRENT ROW`**, which lumps tied values
together. If `SUM(x) OVER (ORDER BY y)` jumps unexpectedly on ties, that is why.
Write `ROWS` explicitly when you mean row counts.

### 12.5 Median — the "SQL has no MEDIAN" answer

```sql
SELECT AVG(marks) AS median FROM (
    SELECT marks,
           ROW_NUMBER() OVER (ORDER BY marks) AS rn,
           COUNT(*)     OVER ()               AS total
    FROM students WHERE marks IS NOT NULL
) t
WHERE rn IN (FLOOR((total+1)/2), CEIL((total+1)/2));
```

```text
+---------+
| median  |
+---------+
| 78.0000 |
+---------+
```

Taking `FLOOR` **and** `CEIL` handles both cases: for an odd count they are the
same row; for an even count they are the middle two, and `AVG` averages them.

Note `COUNT(*) OVER ()` — an **empty** `OVER ()` means "the whole result set",
which is how you get a grand total beside every row.

### 12.6 Subquery vs JOIN — what the optimiser actually does

MySQL 8 rewrites most `IN (subquery)` into a **semi-join**, so the old advice
"always rewrite `IN` as a `JOIN`" is largely obsolete. What still matters:

| Pattern | Watch for |
|---|---|
| **Correlated subquery in `SELECT`** | Runs once **per row** — usually replace with `LEFT JOIN` + `GROUP BY` |
| `NOT IN (subquery)` | Silently returns nothing if the subquery yields `NULL` — use `NOT EXISTS` |
| Derived table in `FROM` | May be materialised into a temp table; check `EXPLAIN` |
| `EXISTS` | Short-circuits at the first match — usually the best anti/semi-join |

**Rule of thumb to teach:** *use a join to combine data, a subquery to filter by
something computed, and `EXISTS` to test existence.*

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
