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
| `SUBSTRING(s, start, n)` | part of a string (**starts at 1**) | `SUBSTRING('Rahul',1,3)` → `Rah` |
| `TRIM(s)` | remove outer spaces | `TRIM('  hi  ')` → `hi` |
| `REPLACE(s, a, b)` | swap text | `REPLACE('a-b','-','+')` → `a+b` |
| `INSTR(s, x)` | position of x, else 0 | `INSTR('Rahul','h')` → `3` |
| `CONCAT(a, b, …)` | join strings | `CONCAT('a','b')` → `ab` |

```sql
SELECT UPPER(name) AS caps,
       LENGTH(name) AS len,
       SUBSTRING(name, 1, 5) AS first5
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
`SUBSTRING(name, 1, 5)` is the *first* five characters.

Functions are most useful when they feed something else. Grouping by a computed
initial:

```sql
SELECT UPPER(SUBSTRING(name,1,1)) AS initial, COUNT(*) AS n
FROM students
GROUP BY initial
ORDER BY n DESC, initial;
```

```text
+---------+---+
| initial | n |
+---------+---+
| A       | 2 |
| R       | 2 |
| D       | 1 |
| K       | 1 |
| M       | 1 |
| P       | 1 |
| S       | 1 |
| V       | 1 |
+---------+---+
```

And a text bar chart, which makes results readable without any tooling:

```sql
SELECT name, marks,
       RPAD(REPEAT('#', FLOOR(IFNULL(marks,0)/10)), 10, '.') AS bar
FROM students
ORDER BY marks DESC;
```

```text
+--------------+-------+------------+
| name         | marks | bar        |
+--------------+-------+------------+
| Anita Sharma |    95 | #########. |
| Arjun Mehta  |    90 | #########. |
| Vikram Rao   |    81 | ########.. |
| Rahul Verma  |    78 | #######... |
| Rohit Sinha  |    78 | #######... |
| Priya Nair   |    66 | ######.... |
| Sneha Iyer   |    54 | #####..... |
| Divya Menon  |    45 | ####...... |
| Karan Patel  |    38 | ###....... |
| Meera Nair   |  NULL | .......... |
+--------------+-------+------------+
```

Four functions nested: `REPEAT` builds the bar, `FLOOR(.../10)` scales it,
`IFNULL` keeps the NULL row from vanishing, `RPAD` pads to a fixed width so the
column lines up. Read nested calls **inside out**.

📌 **Dialect corner.** MySQL joins strings with **`CONCAT()`**. SQLite,
PostgreSQL and Oracle use **`||`** — which in MySQL means `OR` and silently
returns `0`. SQLite spells the substring function `SUBSTR`; MySQL and
PostgreSQL accept both `SUBSTR` and `SUBSTRING`.

---

## 3. Numeric Functions

| Function | Does | Example → result |
|---|---|---|
| `ROUND(n, d)` | round to d decimals | `ROUND(68.777, 2)` → `68.78` |
| `ABS(n)` | remove the sign | `ABS(-18)` → `18` |
| `CEIL(n)` / `FLOOR(n)` | up / down to whole | `FLOOR(4.9)` → `4` |
| `n % m` | remainder | `10 % 3` → `1` |
| `CAST(x AS SIGNED)` | change type | `CAST('42' AS SIGNED)` → `42` |

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

> 📌 **Dialect corner — division.** `SELECT 7/2;` gives **`3.5000`** in MySQL:
> `/` always produces a decimal. Use **`7 DIV 2`** for integer division.
> In SQLite and PostgreSQL the same `7/2` gives **`3`**, and you write `7.0/2`
> to get a decimal. **Opposite defaults — check before you trust a total.**

---

## 4. Date Functions

MySQL has real **`DATE`**, `DATETIME` and `TIMESTAMP` types — unlike SQLite,
which stores dates as plain text.

| Function | Does |
|---|---|
| `CURDATE()` | today |
| `NOW()` | today with the time |
| `YEAR(d)`, `MONTH(d)`, `DAY(d)` | pull one piece out |
| `DATE_FORMAT(d, fmt)` | reformat for display |
| `DATEDIFF(a, b)` | days between two dates |
| `DATE_ADD(d, INTERVAL 30 DAY)` | date arithmetic |

| `DATE_FORMAT` code | Gives |
|---|---|
| `%Y` | 4-digit year |
| `%m` | month number |
| `%d` | day |
| `%M` | month name |

```sql
SELECT joined_on,
       YEAR(joined_on)  AS yr,
       MONTH(joined_on) AS mth,
       DATE_FORMAT(joined_on, '%d-%m-%Y') AS pretty
FROM students
LIMIT 3;
```

```text
+------------+------+------+------------+
| joined_on  | yr   | mth  | pretty     |
+------------+------+------+------------+
| 2025-01-15 | 2025 |    1 | 15-01-2025 |
| 2025-01-20 | 2025 |    1 | 20-01-2025 |
| 2025-02-01 | 2025 |    2 | 01-02-2025 |
+------------+------+------+------------+
```

Days between two dates is a single function:

```sql
SELECT name, DATEDIFF('2025-06-01', joined_on) AS days_enrolled
FROM students
LIMIT 3;
```

```text
+--------------+---------------+
| name         | days_enrolled |
+--------------+---------------+
| Rahul Verma  |           137 |
| Anita Sharma |           132 |
| Karan Patel  |           120 |
+--------------+---------------+
```

Dates combine with the other functions in the obvious way:

```sql
SELECT CONCAT(name,' (',city,')')               AS who,
       DATEDIFF('2025-06-01', joined_on)        AS days_enrolled,
       DATE_ADD(joined_on, INTERVAL 6 MONTH)    AS review_due
FROM students
ORDER BY joined_on
LIMIT 3;
```

```text
+-------------------------+---------------+------------+
| who                     | days_enrolled | review_due |
+-------------------------+---------------+------------+
| Rahul Verma (Hyderabad) |           137 | 2025-07-15 |
| Anita Sharma (Chennai)  |           132 | 2025-07-20 |
| Karan Patel (Hyderabad) |           120 | 2025-08-01 |
+-------------------------+---------------+------------+
```

`DATE_ADD` understands `INTERVAL n DAY | WEEK | MONTH | QUARTER | YEAR`, and it
handles month lengths properly — adding 1 month to 31 January gives 28 February,
not an invalid date.

> ⚠️ Use a **fixed date** like `'2025-06-01'` in notes and tests. Writing
> `CURDATE()` means the output changes every day and nobody can tell whether the
> query broke or the calendar moved.

📌 **Dialect corner — dates are where the three differ most.**

| Job | **MySQL** | **SQLite** | **PostgreSQL** |
|---|---|---|---|
| Today | `CURDATE()` | `DATE('now')` | `CURRENT_DATE` |
| Year | `YEAR(d)` | `STRFTIME('%Y', d)` | `EXTRACT(YEAR FROM d)` |
| Days between | `DATEDIFF(a,b)` | `JULIANDAY(a)-JULIANDAY(b)` | `a - b` |
| Format | `DATE_FORMAT(d,'%d-%m-%Y')` | `STRFTIME('%d-%m-%Y',d)` | `TO_CHAR(d,'DD-MM-YYYY')` |
| Add 30 days | `DATE_ADD(d, INTERVAL 30 DAY)` | `DATE(d,'+30 days')` | `d + INTERVAL '30 days'` |

SQLite has **no date type at all** — it keeps text in `'YYYY-MM-DD'` form,
which sorts correctly but accepts nonsense like `'2025-99-99'`. MySQL rejects
that.

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

The same aggregates per group, with a spread measure:

```sql
SELECT city, COUNT(*) AS n, SUM(marks) AS total,
       ROUND(AVG(marks),1) AS avg, ROUND(STDDEV(marks),2) AS std
FROM students
WHERE marks IS NOT NULL
GROUP BY city
ORDER BY avg DESC;
```

```text
+-----------+---+-------+------+------+
| city      | n | total | avg  | std  |
+-----------+---+-------+------+------+
| Pune      | 2 |   168 | 84.0 |    6 |
| Chennai   | 2 |   149 | 74.5 | 20.5 |
| Hyderabad | 3 |   197 | 65.7 | 19.6 |
| Kochi     | 2 |   111 | 55.5 | 10.5 |
+-----------+---+-------+------+------+
```

`STDDEV` shows how *spread out* a group is. Chennai and Pune have similar
averages but very different consistency — the average alone hides that, which is
a point worth making whenever you teach `AVG`.

Other aggregates worth knowing: `VARIANCE`, `BIT_OR`, and `COUNT(DISTINCT col)`.

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

`CASE` has a shorter cousin for two-way choices:

```sql
SELECT name, marks,
       IF(marks >= 50, 'Pass', 'Fail')  AS quick,
       IFNULL(marks, 'not graded')      AS shown
FROM students
LIMIT 4;
```

```text
+--------------+-------+-------+-------+
| name         | marks | quick | shown |
+--------------+-------+-------+-------+
| Rahul Verma  |    78 | Pass  | 78    |
| Anita Sharma |    95 | Pass  | 95    |
| Karan Patel  |    38 | Fail  | 38    |
| Priya Nair   |    66 | Pass  | 66    |
+--------------+-------+-------+-------+
```

`IF(condition, then, else)` is fine for two outcomes. Use `CASE` for three or
more — and remember `IF()` is **MySQL-only**; `CASE` is standard SQL and works
everywhere.

### NULL handling

| Function | Does |
|---|---|
| `IFNULL(a, b)` | b if a is null (MySQL and SQLite; **not** PostgreSQL) |
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
SELECT UPPER(SUBSTRING(name, 1, 1)) || LOWER(SUBSTRING(name, 2)) AS tidy_name
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

**3. `SUBSTRING(name, 0, 3)`** — SQL counts from **1**, not 0.

**4. Assuming `/` truncates** — in MySQL `7/2` is `3.5000`. Use `DIV` for whole numbers.

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
- MySQL has a real `DATE` type: `YEAR()`, `DATEDIFF()`, `DATE_FORMAT()`.
- Aggregates **ignore NULL** — except `COUNT(*)`. `AVG` divides by the count of
  *non-null* values.
- `CASE` is if/else, first match wins. `COALESCE` is the portable NULL default.

---

## 11. 🔺 ADVANCED — Teacher Reference

### 11.1 JSON — MySQL as a document store

MySQL 8 has a real `JSON` type with indexing and full query support.

```sql
CREATE TABLE profiles (
    id   INT PRIMARY KEY,
    data JSON
);
INSERT INTO profiles VALUES
 (1, '{"skills":["Python","SQL"],"exp":2,"contact":{"city":"Pune"}}'),
 (2, '{"skills":["Java"],"exp":5,"contact":{"city":"Kochi"}}');

SELECT id,
       data->>'$.exp'            AS experience,
       data->>'$.contact.city'   AS city,
       JSON_LENGTH(data->'$.skills') AS skill_count
FROM profiles;
```

```text
+----+------------+-------+-------------+
| id | experience | city  | skill_count |
+----+------------+-------+-------------+
|  1 | 2          | Pune  |           2 |
|  2 | 5          | Kochi |           1 |
+----+------------+-------+-------------+
```

| Operator / function | Does |
|---|---|
| `->` | extract, **keeps** JSON quotes |
| `->>` | extract and **unquote** — usually what you want |
| `JSON_EXTRACT`, `JSON_UNQUOTE` | the long forms of the above |
| `JSON_CONTAINS`, `JSON_LENGTH`, `JSON_KEYS` | inspect |
| `JSON_TABLE(...)` | turn a JSON array into **rows** |

**When to use it:** genuinely variable attributes. **When not to:** as an excuse
to avoid designing a schema. You lose constraints, foreign keys and easy joins.

📌 PostgreSQL's `JSONB` is more mature and indexes better. SQLite has JSON1.

### 11.2 String aggregation and splitting

```sql
SELECT GROUP_CONCAT(DISTINCT city ORDER BY city SEPARATOR ' | ') AS all_cities
FROM students;
```

```text
+---------------------------------------+
| all_cities                            |
+---------------------------------------+
| Chennai | Hyderabad | Kochi | Pune    |
+---------------------------------------+
```

⚠️ Truncates silently at `group_concat_max_len` (default 1024).

MySQL has no `SPLIT` function. `SUBSTRING_INDEX` is the workaround:

```sql
SELECT SUBSTRING_INDEX('Rahul Verma', ' ', 1)  AS first_name,
       SUBSTRING_INDEX('Rahul Verma', ' ', -1) AS last_name;
```

```text
+------------+-----------+
| first_name | last_name |
+------------+-----------+
| Rahul      | Verma     |
+------------+-----------+
```

Positive n takes from the left, negative from the right. Nesting two of them
extracts a middle field — the standard MySQL "split a string" idiom.

### 11.3 Date bucketing — the shape of every analytics query

```sql
SELECT DATE_FORMAT(joined_on, '%Y-%m') AS month,
       COUNT(*)                        AS joined,
       ROUND(AVG(marks),2)             AS avg_marks
FROM students
GROUP BY month
ORDER BY month;
```

```text
+---------+--------+-----------+
| month   | joined | avg_marks |
+---------+--------+-----------+
| 2025-01 |      2 |     86.50 |
| 2025-02 |      2 |     52.00 |
| 2025-03 |      2 |     67.50 |
| 2025-04 |      2 |     67.50 |
| 2025-05 |      2 |     78.00 |
+---------+--------+-----------+
```

`'%Y-%m'` sorts correctly as text, which is why it beats `MONTH()` for grouping
across years.

Other buckets: `YEARWEEK(d)`, `QUARTER(d)`,
`DATE_SUB(d, INTERVAL WEEKDAY(d) DAY)` for week-start.

⚠️ **Grouping by a function on a column cannot use an index.** For big tables,
store a generated column (Day 2–3 §12.1) and index that.

### 11.4 Numeric precision traps

| Trap | Detail |
|---|---|
| `FLOAT` comparison | `0.1+0.2 <> 0.3`. Use `DECIMAL` for money |
| `ROUND` on `.5` | MySQL rounds half **away from zero** for exact types |
| Integer division | `7/2` = `3.5000`, `7 DIV 2` = `3` |
| `NULL` in arithmetic | anything `+ NULL` is `NULL` — wrap with `COALESCE` |
| `AVG` of integers | returns a decimal, not an integer |

The `NULL` one causes the most silent damage:

```sql
SELECT marks + 5 FROM students WHERE id = 110;   -- NULL, not 5
```

### 11.5 A function on a column kills the index — say this every time

```sql
WHERE YEAR(joined_on) = 2025                                    -- ❌ scans
WHERE joined_on >= '2025-01-01' AND joined_on < '2026-01-01'    -- ✅ index range

WHERE LOWER(city) = 'pune'      -- ❌ scans (and unnecessary in MySQL — it is
                                --    already case-insensitive)
WHERE city = 'pune'             -- ✅
```

This one rewrite is the most common real-world query fix there is.

---

## 11. Practice Questions

1. Show every student's name in capitals with its length.
2. Show the first three letters of each city.
3. Produce `Rahul Verma - Hyderabad` in one column.
4. Show marks rounded to the nearest 10 (`ROUND(marks, -1)`).
5. Show the year and month each student joined, and the date as `dd-mm-yyyy`.
6. How many days has each student been enrolled, as of `2025-06-01`?
7. Count the students, count those with marks, and count the distinct cities.
8. Total, average, highest and lowest marks in one query.
9. Explain why `AVG(marks)` is 69.44 and not 62.5.
10. Recalculate the average treating missing marks as 0.
11. Label each student `Distinction` / `Pass` / `Fail` / `Not graded`.
12. Use `CASE` to show `Senior` for age above 22, else `Junior`.
13. Replace every missing `course_id` with the text `Unassigned`.
14. What is the difference between `IFNULL` and `COALESCE`?
15. What does `SELECT 7/2` give in MySQL, and what does it give in SQLite?
