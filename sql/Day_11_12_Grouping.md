# Day 11–12 · Grouping

**Duration:** 2 × 50–60 Minutes

### Learning Outcomes
- Collapse rows into groups with **`GROUP BY`**.
- Filter groups with **`HAVING`**, and know exactly how it differs from `WHERE`.
- Combine aggregates with grouping to answer real questions.
- Understand where `GROUP BY` sits in the **run order**.

---

## 1. The Idea

Day 9 aggregates squashed the **whole table** into one row:

```sql
SELECT AVG(marks) FROM students;      -- one number for everyone
```

`GROUP BY` squashes it into **one row per group** instead:

```text
   10 students                        4 cities
   ┌──────────────┐                 ┌──────────────────┐
   │ Hyderabad 78 │                 │ Hyderabad  65.67 │
   │ Chennai   95 │   GROUP BY      │ Chennai    74.50 │
   │ Hyderabad 38 │  ───────────►   │ Kochi      55.50 │
   │ Kochi     66 │    city         │ Pune       84.00 │
   │ ...          │                 └──────────────────┘
   └──────────────┘
```

---

## 2. GROUP BY

```sql
SELECT city, COUNT(*) AS students, ROUND(AVG(marks), 2) AS avg_marks
FROM students
GROUP BY city
ORDER BY avg_marks DESC;
```

```text
city      | students | avg_marks
----------+----------+----------
Pune      | 2        | 84.0
Chennai   | 3        | 74.5
Hyderabad | 3        | 65.67
Kochi     | 2        | 55.5
```

Read it as: *make one row per city; for each, count the rows and average the
marks.*

Aggregates combine freely, and you can calculate with them:

```sql
SELECT city,
       COUNT(*)               AS n,
       MIN(marks)             AS lowest,
       MAX(marks)             AS highest,
       MAX(marks)-MIN(marks)  AS spread
FROM students
WHERE marks IS NOT NULL
GROUP BY city
ORDER BY spread DESC;
```

```text
+-----------+---+--------+---------+--------+
| city      | n | lowest | highest | spread |
+-----------+---+--------+---------+--------+
| Hyderabad | 3 |     38 |      81 |     43 |
| Chennai   | 2 |     54 |      95 |     41 |
| Kochi     | 2 |     45 |      66 |     21 |
| Pune      | 2 |     78 |      90 |     12 |
+-----------+---+--------+---------+--------+
```

`MAX(marks)-MIN(marks)` is an ordinary expression built from two aggregates —
and because it is computed in `SELECT`, you can sort by its alias in
`ORDER BY`. **Spread** is a genuinely useful teaching number: Hyderabad and
Chennai have the same headline average story but very different consistency.

### The golden rule

> Every column in `SELECT` must either be **in the `GROUP BY`**, or be inside an
> **aggregate function**.

```sql
SELECT city, name, COUNT(*) FROM students GROUP BY city;
```

Hyderabad has three students — *which* name should the one row show? The
question has no answer.

> ⚠️ **MySQL lets this through and picks a name arbitrarily.** MySQL (in strict
> mode), PostgreSQL, Oracle and SQL Server all **reject it as an error**. Never
> write it, even though MySQL allows it.

---

## 3. Grouping by More Than One Column

```sql
SELECT city, age, COUNT(*) AS students
FROM students
GROUP BY city, age
ORDER BY city, age;
```

```text
city      | age | students
----------+-----+---------
Chennai   | 21  | 1
Chennai   | 22  | 2
Hyderabad | 20  | 1
Hyderabad | 21  | 2
Kochi     | 20  | 1
Kochi     | 23  | 1
Pune      | 23  | 1
Pune      | 24  | 1
```

One row per **combination**. More grouping columns means more, smaller groups.

---

## 4. HAVING — Filtering Groups

`WHERE` filters **rows**. `HAVING` filters **groups**, after they are formed.

```sql
SELECT city, COUNT(*) AS students
FROM students
GROUP BY city
HAVING COUNT(*) > 2;
```

```text
city      | students
----------+---------
Chennai   | 3
Hyderabad | 3
```

Only cities with more than two students survive.

### WHERE vs HAVING

| | `WHERE` | `HAVING` |
|---|---|---|
| Filters | individual **rows** | whole **groups** |
| Runs | **before** grouping | **after** grouping |
| Aggregates allowed | ❌ no | ✅ yes |
| Needs `GROUP BY` | no | almost always |

```sql
SELECT COUNT(*) FROM students WHERE COUNT(*) > 2;
```
```text
Error: misuse of aggregate function COUNT()
```

**Both together** — `WHERE` first to drop rows, `HAVING` after to drop groups:

```sql
SELECT city, COUNT(*) AS passed, ROUND(AVG(marks), 2) AS avg_marks
FROM students
WHERE marks >= 50            -- 1. keep only passing students
GROUP BY city                -- 2. group what is left
HAVING COUNT(*) >= 2         -- 3. keep cities with 2+ of them
ORDER BY avg_marks DESC;
```

```text
city      | passed | avg_marks
----------+--------+----------
Pune      | 2      | 84.0
Hyderabad | 2      | 79.5
Chennai   | 2      | 74.5
```

Notice Hyderabad's average is now **79.5**, not 65.67 — Karan (38) was removed
by `WHERE` before the average was taken. **The order of operations changes the
answer.**

---

## 5. Where Grouping Sits in the Run Order

From Day 1, now with the middle filled in:

| Step | Clause | What happens |
|---|---|---|
| 1 | `FROM` | fetch the table |
| 2 | `WHERE` | drop rows |
| 3 | `GROUP BY` | make groups |
| 4 | `HAVING` | drop groups |
| 5 | `SELECT` | work out the columns |
| 6 | `ORDER BY` | sort |
| 7 | `LIMIT` | cut |

This explains three rules you have already met:

- `WHERE` cannot use aggregates — they do not exist until step 3.
- `HAVING` can — step 4 is after grouping.
- `ORDER BY` can use a `SELECT` alias (step 6 > step 5); `WHERE` cannot (2 < 5).

---

## 6. Grouping with NULL

`GROUP BY` puts **all NULLs into one group** — unlike `=`, which never matches
NULL.

```sql
SELECT course_id, COUNT(*) AS students
FROM students
GROUP BY course_id
ORDER BY course_id;
```

```text
course_id | students
----------+---------
NULL      | 1
1         | 3
2         | 2
3         | 2
4         | 2
```

Rohit Sinha, with no course, forms his own `NULL` group.

---

## 7. Useful Grouping Patterns

**Find duplicates** — the classic interview question:

```sql
SELECT city, COUNT(*) AS how_many
FROM students
GROUP BY city
HAVING COUNT(*) > 1;
```

```text
city      | how_many
----------+---------
Chennai   | 3
Hyderabad | 3
Kochi     | 2
Pune      | 2
```

**Group with a CASE** — count by band instead of by column:

```sql
SELECT CASE WHEN marks >= 75 THEN 'Distinction'
            WHEN marks >= 50 THEN 'Pass'
            WHEN marks IS NULL THEN 'Not graded'
            ELSE 'Fail' END AS band,
       COUNT(*) AS students
FROM students
GROUP BY band
ORDER BY students DESC;
```

```text
band        | students
------------+---------
Distinction | 5
Pass        | 2
Fail        | 2
Not graded  | 1
```

`Pass` and `Fail` are tied on 2. Which appears first is **not guaranteed** —
add `ORDER BY students DESC, band` if you need a fixed order.

**Aggregate of an aggregate** needs a subquery (Day 15):

```sql
SELECT ROUND(AVG(city_avg), 2) AS avg_of_city_averages
FROM (SELECT AVG(marks) AS city_avg FROM students GROUP BY city) AS t;
```

```text
avg_of_city_averages
--------------------
69.92
```

Note this is **not** the same as the overall average (69.44) — averaging
averages weights small cities equally with big ones. A favourite exam trap.

---

## 8. Common Mistakes

**1. A bare column in `SELECT` that is not grouped** — MySQL allows it and
gives an arbitrary value; every other database errors.

**2. Using an aggregate in `WHERE`** — `misuse of aggregate function`. Use
`HAVING`.

**3. Using `HAVING` when `WHERE` would do** — `HAVING city = 'Pune'` works but
is slower: it groups everything first, then throws groups away. Filter rows
early with `WHERE`.

**4. Expecting `COUNT(*)` to skip NULLs** — it counts rows. `COUNT(col)` skips
them.

**5. Forgetting NULL forms its own group.**

**6. Averaging averages** — mathematically different from the overall average.

---

## 9. Summary

- `GROUP BY` turns many rows into **one row per group**.
- Every selected column must be **grouped** or **aggregated**.
- `WHERE` filters rows **before** grouping; `HAVING` filters groups **after**.
  Only `HAVING` may contain aggregates.
- Run order: `FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT`.
- All `NULL`s group together into a single group.
- `GROUP BY … HAVING COUNT(*) > 1` is the standard **find duplicates** pattern.

---

## 10. 🔺 ADVANCED — Teacher Reference

### 10.1 `WITH ROLLUP` — subtotals and a grand total for free

```sql
SELECT city, COUNT(*) AS n, ROUND(AVG(marks),2) AS avg_marks
FROM students WHERE marks IS NOT NULL
GROUP BY city WITH ROLLUP;
```

```text
+-----------+---+-----------+
| city      | n | avg_marks |
+-----------+---+-----------+
| Chennai   | 2 |     74.50 |
| Hyderabad | 3 |     65.67 |
| Kochi     | 2 |     55.50 |
| Pune      | 2 |     84.00 |
| NULL      | 9 |     69.44 |
+-----------+---+-----------+
```

The final `NULL` row is the **grand total**. With two grouping columns you get a
subtotal per first column as well — this is how reporting tools build totals
rows without a second query.

⚠️ The total row is marked by `NULL` in the grouped column, which is ambiguous
if the column itself has NULLs. Distinguish them with `GROUPING()`:
`SELECT IF(GROUPING(city), 'ALL CITIES', city) AS city ...`

📌 PostgreSQL and Oracle write it as `GROUP BY ROLLUP(city)`. SQLite has neither.

### 10.2 `GROUP_CONCAT` — flatten a group into one string

```sql
SELECT city, GROUP_CONCAT(name ORDER BY marks DESC SEPARATOR ', ') AS students_by_rank
FROM students WHERE marks IS NOT NULL GROUP BY city;
```

```text
+-----------+--------------------------------------+
| city      | students_by_rank                     |
+-----------+--------------------------------------+
| Chennai   | Anita Sharma, Sneha Iyer             |
| Hyderabad | Vikram Rao, Rahul Verma, Karan Patel |
| Kochi     | Priya Nair, Divya Menon              |
| Pune      | Arjun Mehta, Rohit Sinha             |
+-----------+--------------------------------------+
```

Enormously useful for reports and for debugging "which rows are in this group?".

⚠️ **Silently truncates at `group_concat_max_len` (default 1024 bytes).** No
error, just a short string. Raise it with `SET SESSION group_concat_max_len = 100000;`

📌 PostgreSQL calls this `STRING_AGG(name, ', ')`; Oracle `LISTAGG`;
SQLite `GROUP_CONCAT` but **without** `ORDER BY` support.

### 10.3 Conditional aggregation — the pivot pattern

`SUM()` over a boolean is the cleanest way to count subsets in one pass:

```sql
SELECT
  COUNT(*)                                        AS total,
  SUM(marks >= 75)                                AS distinctions,
  SUM(marks <  40)                                AS fails,
  ROUND(100.0 * SUM(marks >= 75)/COUNT(*),1)      AS pct_distinction
FROM students WHERE marks IS NOT NULL;
```

```text
+-------+--------------+-------+-----------------+
| total | distinctions | fails | pct_distinction |
+-------+--------------+-------+-----------------+
|     9 |            5 |     1 |            55.6 |
+-------+--------------+-------+-----------------+
```

In MySQL a boolean **is** 1 or 0, so `SUM(marks >= 75)` counts the matches.
`SUM(CASE WHEN ... THEN 1 ELSE 0 END)` is the portable spelling — teach that one
for interviews, this one for real work.

**One pass, many answers.** Compare with running three separate `COUNT` queries.

### 10.4 `ONLY_FULL_GROUP_BY` and `ANY_VALUE()`

MySQL 5.7+ rejects selecting a column that is neither grouped nor aggregated.
When you genuinely do not care which value you get, say so explicitly:

```sql
SELECT city, ANY_VALUE(name) AS a_student, COUNT(*) AS n
FROM students GROUP BY city ORDER BY city;
```

```text
+-----------+--------------+---+
| city      | a_student    | n |
+-----------+--------------+---+
| Chennai   | Anita Sharma | 3 |
| Hyderabad | Rahul Verma  | 3 |
| Kochi     | Priya Nair   | 2 |
| Pune      | Arjun Mehta  | 2 |
+-----------+--------------+---+
```

`ANY_VALUE()` documents the intent. Turning the mode off
(`SET sql_mode=''`) hides real bugs — do not teach that as the fix.

### 10.5 Performance notes worth saying out loud

| Point | Why |
|---|---|
| `WHERE` before `HAVING` | filtering rows early means fewer rows to group |
| An index on the `GROUP BY` column | lets MySQL group by reading in order, avoiding a temp table |
| `Using temporary; Using filesort` in `EXPLAIN` | the warning sign for grouping |
| `COUNT(*)` vs `COUNT(1)` | **identical** — the "COUNT(1) is faster" claim is a myth |
| `COUNT(DISTINCT x)` | far more expensive than `COUNT(x)`; it must deduplicate |

---

## 10. Practice Questions

1. Count the students in each city.
2. Average marks per city, best first.
3. Highest and lowest marks in each city.
4. Number of students per `course_id`.
5. Cities with more than two students.
6. Cities whose average marks are above 70.
7. Count students per age.
8. Among students who passed (50+), the average per city, for cities with at
   least two such students.
9. Explain why Hyderabad's average changes when you add `WHERE marks >= 50`.
10. Why does `WHERE COUNT(*) > 2` fail but `HAVING COUNT(*) > 2` work?
11. Find every city that appears more than once.
12. Count students in each grade band using `CASE`.
13. Which group does Rohit Sinha (no course) fall into, and why?
14. Compute the average of the per-city averages. Why is it not 69.44?
