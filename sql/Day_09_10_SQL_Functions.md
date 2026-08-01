# Day 9–10 · SQL Functions

**Duration:** 2 × 50–60 Minutes

### Learning Outcomes
- Use **string**, **numeric** and **date** functions.
- Use **aggregate** functions and know how they treat `NULL`.
- Write **conditional** logic with `CASE`, `IFNULL` and `COALESCE`.
- Tell **scalar** functions from **aggregate** functions.

---

## 1. Two Kinds of Function

| Kind | Works on | Rows in → out | Examples |
|---|---|---|---|
| **Scalar** | one value at a time | 10 → 10 | `UPPER`, `ROUND`, `LENGTH` |
| **Aggregate** | a whole column | 10 → **1** | `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` |

That difference is the single most important idea in these two days. A scalar
function keeps your row count; an aggregate collapses it.

---

## 2. String Functions

| Function | Does | Example → result |
|---|---|---|
| `UPPER(s)` | to capitals | `UPPER('sql')` → `SQL` |
| `LOWER(s)` | to small letters | `LOWER('SQL')` → `sql` |
| `LENGTH(s)` | number of characters | `LENGTH('Rahul')` → `5` |
| `SUBSTR(s, start, n)` | part of a string (**starts at 1**) | `SUBSTR('Rahul',1,3)` → `Rah` |
| `TRIM(s)` | remove outer spaces | `TRIM('  hi  ')` → `hi` |
| `REPLACE(s, a, b)` | swap text | `REPLACE('a-b','-','+')` → `a+b` |
| `INSTR(s, x)` | position of x, else 0 | `INSTR('Rahul','h')` → `3` |
| `s1 \|\| s2` | join two strings | `'a' \|\| 'b'` → `ab` |

```sql
SELECT UPPER(name) AS caps,
       LENGTH(name) AS len,
       SUBSTR(name, 1, 5) AS first5
FROM students
LIMIT 3;
```

```text
caps         | len | first5
-------------+-----+-------
RAHUL VERMA  | 11  | Rahul
ANITA SHARMA | 12  | Anita
KARAN PATEL  | 11  | Karan
```

**Key Note:** SQL strings are **1-indexed**, not 0-indexed like Python.
`SUBSTR(name, 1, 5)` is the *first* five characters.

Other databases: MySQL uses `CONCAT(a, b)` instead of `||`, and both have
`SUBSTRING`. The idea is identical.

---

## 3. Numeric Functions

| Function | Does | Example → result |
|---|---|---|
| `ROUND(n, d)` | round to d decimals | `ROUND(68.777, 2)` → `68.78` |
| `ABS(n)` | remove the sign | `ABS(-18)` → `18` |
| `CEIL(n)` / `FLOOR(n)` | up / down to whole | `FLOOR(4.9)` → `4` |
| `n % m` | remainder | `10 % 3` → `1` |
| `CAST(x AS INTEGER)` | change type | `CAST('42' AS INTEGER)` → `42` |

```sql
SELECT name,
       ROUND(marks * 1.1, 1) AS raised,
       ABS(marks - 60)       AS gap_from_60
FROM students
WHERE marks IS NOT NULL
LIMIT 3;
```

```text
name         | raised | gap_from_60
-------------+--------+------------
Rahul Verma  | 85.8   | 18
Anita Sharma | 104.5  | 35
Karan Patel  | 41.8   | 22
```

> ⚠️ **Integer division.** `SELECT 7 / 2;` gives **3**, not 3.5 — both sides are
> integers. Force a decimal with `7.0 / 2` or `CAST(7 AS REAL) / 2`.

---

## 4. Date Functions

SQLite has no `DATE` type — dates are `TEXT` shaped `'YYYY-MM-DD'`.

| Function | Does |
|---|---|
| `DATE('now')` | today |
| `DATETIME('now')` | today with the time |
| `STRFTIME(fmt, d)` | pull a piece out, or reformat |
| `JULIANDAY(d)` | day number, for subtracting dates |
| `DATE(d, '+30 days')` | date arithmetic |

| `STRFTIME` code | Gives |
|---|---|
| `%Y` | year | 
| `%m` | month | 
| `%d` | day |
| `%W` | week of year |

```sql
SELECT joined_on,
       STRFTIME('%Y', joined_on) AS yr,
       STRFTIME('%m', joined_on) AS mth
FROM students
LIMIT 3;
```

```text
joined_on  | yr   | mth
-----------+------+----
2025-01-15 | 2025 | 01
2025-01-20 | 2025 | 01
2025-02-01 | 2025 | 02
```

Days between two dates:

```sql
SELECT name,
       CAST(JULIANDAY('2025-06-01') - JULIANDAY(joined_on) AS INTEGER) AS days_enrolled
FROM students
LIMIT 3;
```

```text
name         | days_enrolled
-------------+--------------
Rahul Verma  | 137
Anita Sharma | 132
Karan Patel  | 120
```

**Key Note:** MySQL uses `YEAR()`, `MONTH()`, `DATEDIFF()`; Oracle uses
`EXTRACT()` and plain subtraction. Only the function names differ.

---

## 5. Aggregate Functions

| Function | Returns | Ignores NULL? |
|---|---|---|
| `COUNT(*)` | number of **rows** | ❌ counts everything |
| `COUNT(col)` | number of **non-null values** | ✅ |
| `SUM(col)` | total | ✅ |
| `AVG(col)` | average | ✅ |
| `MIN(col)` / `MAX(col)` | smallest / largest | ✅ |

```sql
SELECT COUNT(*)          AS total,
       COUNT(marks)      AS with_marks,
       SUM(marks)        AS total_marks,
       ROUND(AVG(marks),2) AS avg_marks,
       MIN(marks)        AS lowest,
       MAX(marks)        AS highest
FROM students;
```

```text
total | with_marks | total_marks | avg_marks | lowest | highest
------+------------+-------------+-----------+--------+--------
10    | 9          | 625         | 69.44     | 38     | 95
```

Ten rows collapse into **one**.

### ⚠️ AVG ignores NULL — this is exam material

`AVG(marks)` is `625 / 9 = 69.44`, **not** `625 / 10 = 62.5`. The student with
no marks is left out of both the total and the count.

If a missing mark should count as zero, say so explicitly:

```sql
SELECT ROUND(AVG(IFNULL(marks, 0)), 2) AS avg_counting_nulls_as_zero
FROM students;
```

```text
avg_counting_nulls_as_zero
--------------------------
62.5
```

**Two different, both correct answers.** Which one you want depends on the
question — and interviewers ask this deliberately.

---

## 6. COUNT(*) vs COUNT(column) vs COUNT(DISTINCT column)

```sql
SELECT COUNT(*)              AS rows_total,
       COUNT(marks)          AS marks_present,
       COUNT(DISTINCT city)  AS distinct_cities
FROM students;
```

```text
rows_total | marks_present | distinct_cities
-----------+---------------+----------------
10         | 9             | 4
```

---

## 7. Conditional Functions

### CASE — SQL's if/else

```sql
SELECT name, marks,
       CASE WHEN marks >= 75    THEN 'Distinction'
            WHEN marks >= 50    THEN 'Pass'
            WHEN marks IS NULL  THEN 'Not graded'
            ELSE 'Fail'
       END AS result
FROM students;
```

```text
name         | marks | result
-------------+-------+------------
Rahul Verma  | 78    | Distinction
Anita Sharma | 95    | Distinction
Karan Patel  | 38    | Fail
Priya Nair   | 66    | Pass
Vikram Rao   | 81    | Distinction
Sneha Iyer   | 54    | Pass
Arjun Mehta  | 90    | Distinction
Divya Menon  | 45    | Fail
Rohit Sinha  | 78    | Distinction
Meera Nair   | NULL  | Not graded
```

**Key Notes:**
- Conditions are checked **top to bottom**; the first true one wins. Order
  matters — put the strictest first.
- Without `ELSE`, unmatched rows get `NULL`.
- `CASE` works in `SELECT`, `WHERE`, `ORDER BY` and `GROUP BY`.

### NULL handling

| Function | Does |
|---|---|
| `IFNULL(a, b)` | b if a is null (SQLite/MySQL) |
| `COALESCE(a, b, c, …)` | first non-null — **standard, works everywhere** |
| `NULLIF(a, b)` | null if a = b, else a |

```sql
SELECT name, COALESCE(marks, 0) AS marks, COALESCE(course_id, -1) AS course
FROM students
WHERE marks IS NULL OR course_id IS NULL;
```

```text
name        | marks | course
------------+-------+-------
Rohit Sinha | 78    | -1
Meera Nair  | 0     | 4
```

`NULLIF` is the guard against divide-by-zero:
`SELECT total / NULLIF(count, 0)` gives `NULL` instead of an error.

---

## 8. Combining Functions

Functions nest freely:

```sql
SELECT UPPER(SUBSTR(name, 1, 1)) || LOWER(SUBSTR(name, 2)) AS tidy_name
FROM students
LIMIT 3;
```

```text
tidy_name
------------
Rahul verma
Anita sharma
Karan patel
```

Read from the **inside out**: take a substring, change its case, then join.

---

## 9. Common Mistakes

**1. Mixing an aggregate with a plain column** —
`SELECT name, AVG(marks) FROM students;` is meaningless (which name?). You need
`GROUP BY` — that is Day 11.

**2. Expecting `AVG` to count NULLs** — it does not. Use `AVG(IFNULL(col,0))`.

**3. `SUBSTR(name, 0, 3)`** — SQL counts from **1**, not 0.

**4. `7 / 2` giving 3** — integer division. Use `7.0 / 2`.

**5. `WHERE COUNT(*) > 2`** — aggregates are not allowed in `WHERE`. Use
`HAVING` (Day 11).

**6. `CASE` conditions in the wrong order** — `WHEN marks >= 50` before
`WHEN marks >= 75` makes distinctions impossible.

---

## 10. Summary

- **Scalar** functions keep the row count; **aggregate** functions collapse it.
- String: `UPPER`, `LOWER`, `LENGTH`, `SUBSTR` (**1-indexed**), `TRIM`,
  `REPLACE`, `||`.
- Numeric: `ROUND`, `ABS`, `%`, `CAST`. Watch **integer division**.
- Dates are `TEXT`; use `STRFTIME` to extract and `JULIANDAY` to subtract.
- Aggregates **ignore NULL** — except `COUNT(*)`. `AVG` divides by the count of
  *non-null* values.
- `CASE` is if/else, first match wins. `COALESCE` is the portable NULL default.

---

## 11. Practice Questions

1. Show every student's name in capitals with its length.
2. Show the first three letters of each city.
3. Produce `Rahul Verma - Hyderabad` in one column.
4. Show marks rounded to the nearest 10 (`ROUND(marks, -1)`).
5. Show the year and month each student joined.
6. How many days has each student been enrolled, as of `2025-06-01`?
7. Count the students, count those with marks, and count the distinct cities.
8. Total, average, highest and lowest marks in one query.
9. Explain why `AVG(marks)` is 69.44 and not 62.5.
10. Recalculate the average treating missing marks as 0.
11. Label each student `Distinction` / `Pass` / `Fail` / `Not graded`.
12. Use `CASE` to show `Senior` for age above 22, else `Junior`.
13. Replace every missing `course_id` with the text `Unassigned`.
14. What is the difference between `IFNULL` and `COALESCE`?
15. Why does `SELECT 7/2` give 3, and how do you get 3.5?
