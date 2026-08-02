# Day 4–6 · SELECT Queries

**Duration:** 3 × 50–60 Minutes  ·  **Setup:** run `setup_training_db.sql` first

### Learning Outcomes
- Read data with **`SELECT`** and filter it with **`WHERE`**.
- Sort with **`ORDER BY`**, remove repeats with **`DISTINCT`**, cut the list
  with **`LIMIT`** / **`OFFSET`**.
- Rename output columns with **aliases**, and calculate new ones with
  **expressions**.
- Handle **`NULL`** correctly — the trap in every SQL exam.

All output below is real, from the training database.

---

## 1. The Shape of a SELECT

```sql
SELECT   column_list      -- 5. what to show
FROM     table            -- 1. where from
WHERE    condition        -- 2. which rows
GROUP BY column           -- 3. (Day 11)
HAVING   condition        -- 4. (Day 11)
ORDER BY column           -- 6. what order
LIMIT    n;               -- 7. how many
```

The numbers are the **run order** from Day 1 — `FROM` first, `SELECT` almost
last. Everything else you learn today fits into this one skeleton.

---

## 2. SELECT Everything

```sql
SELECT * FROM students;
```

```text
id  | name         | city      | age | course_id | marks | joined_on
----+--------------+-----------+-----+-----------+-------+-----------
101 | Rahul Verma  | Hyderabad | 21  | 1         | 78    | 2025-01-15
102 | Anita Sharma | Chennai   | 22  | 2         | 95    | 2025-01-20
103 | Karan Patel  | Hyderabad | 20  | 1         | 38    | 2025-02-01
104 | Priya Nair   | Kochi     | 23  | 3         | 66    | 2025-02-10
105 | Vikram Rao   | Hyderabad | 21  | 2         | 81    | 2025-03-05
106 | Sneha Iyer   | Chennai   | 22  | 3         | 54    | 2025-03-12
107 | Arjun Mehta  | Pune      | 24  | 4         | 90    | 2025-04-02
108 | Divya Menon  | Kochi     | 20  | 1         | 45    | 2025-04-18
109 | Rohit Sinha  | Pune      | 23  | NULL      | 78    | 2025-05-01
110 | Meera Nair   | Chennai   | 21  | 4         | NULL  | 2025-05-20
```

`*` means *every column*. Convenient when exploring — **avoid it in real code**,
because you get columns you do not need and your query silently changes when
someone adds a column.

## 3. SELECT Specific Columns

```sql
SELECT name, city FROM students LIMIT 3;
```

```text
name         | city
-------------+----------
Rahul Verma  | Hyderabad
Anita Sharma | Chennai
Karan Patel  | Hyderabad
```

The order you list the columns is the order you get them.

---

## 4. WHERE — Filtering Rows

```sql
SELECT name, city, marks
FROM students
WHERE marks > 70
ORDER BY marks DESC;
```

```text
name         | city      | marks
-------------+-----------+------
Anita Sharma | Chennai   | 95
Arjun Mehta  | Pune      | 90
Vikram Rao   | Hyderabad | 81
Rahul Verma  | Hyderabad | 78
Rohit Sinha  | Pune      | 78
```

| Operator | Meaning |
|---|---|
| `=` | equal (**one** `=`, not `==`) |
| `<>` or `!=` | not equal |
| `>` `<` `>=` `<=` | comparisons |
| `AND` `OR` `NOT` | combine conditions |

```sql
SELECT name, city, age
FROM students
WHERE city = 'Hyderabad' AND age < 21;
```

```text
name        | city      | age
------------+-----------+----
Karan Patel | Hyderabad | 20
```

**Key Notes:**
- Text goes in **single quotes**: `'Hyderabad'`. Double quotes mean a column name.
- Text comparison is **case-INsensitive** in MySQL by default: `'hyderabad'`
  finds Hyderabad. 📌 SQLite and PostgreSQL are case-**sensitive** for `=`, so
  the same query finds nothing there. Use `LOWER()` when it must be portable.
- `AND` is evaluated before `OR`. Use brackets when you mix them:
  `WHERE (city='Pune' OR city='Kochi') AND marks > 60`

---

## 5. ORDER BY — Sorting

```sql
SELECT name, marks FROM students ORDER BY marks DESC LIMIT 4;
```

```text
name         | marks
-------------+------
Anita Sharma | 95
Arjun Mehta  | 90
Vikram Rao   | 81
Rahul Verma  | 78
```

| Form | Meaning |
|---|---|
| `ORDER BY marks` | ascending (default, same as `ASC`) |
| `ORDER BY marks DESC` | descending |
| `ORDER BY city, marks DESC` | by city, then by marks inside each city |
| `ORDER BY 2` | by the **2nd** column in the SELECT list |

**Key Note:** without `ORDER BY`, the order of rows is **not guaranteed**. It may
look sorted today and change tomorrow. If order matters, say so.

---

## 6. DISTINCT — Remove Duplicates

```sql
SELECT DISTINCT city FROM students;
```

```text
city
---------
Hyderabad
Chennai
Kochi
Pune
```

Ten students, four cities. `DISTINCT` applies to **all** the selected columns
together, not just the first:

```sql
SELECT DISTINCT city, age FROM students;
```

gives every unique *pair* of city and age.

---

## 7. LIMIT and OFFSET

```sql
SELECT name, marks FROM students ORDER BY marks DESC LIMIT 3;
```

```text
name         | marks
-------------+------
Anita Sharma | 95
Arjun Mehta  | 90
Vikram Rao   | 81
```

`OFFSET` skips rows first — this is how web pages do "page 2":

```sql
SELECT name, marks FROM students ORDER BY marks DESC LIMIT 3 OFFSET 3;
```

```text
name        | marks
------------+------
Rahul Verma | 78
Rohit Sinha | 78
Priya Nair  | 66
```

📌 **Dialect corner.** `LIMIT` works in MySQL, SQLite and PostgreSQL. Oracle
uses `FETCH FIRST n ROWS ONLY`; SQL Server uses `SELECT TOP n`. MySQL also
accepts the older `LIMIT 3, 3` (offset first) — avoid it, it reads backwards.

---

## 8. Aliases — Renaming the Output

```sql
SELECT name AS student_name, marks AS score
FROM students
LIMIT 3;
```

```text
student_name | score
-------------+------
Rahul Verma  | 78
Anita Sharma | 95
Karan Patel  | 38
```

- `AS` is optional (`name student_name` works) but keep it — it reads better.
- Use double quotes for an alias with spaces: `AS "Student Name"`.
- Table aliases save typing, and are essential in joins (Day 13):
  `FROM students s` then `s.name`.

> ⚠️ **You cannot use an alias in `WHERE`.** `WHERE score > 50` fails, because
> `WHERE` runs *before* `SELECT` (Day 1 §7). You **can** use it in `ORDER BY`,
> which runs after.

---

## 9. Expressions — Calculated Columns

You can calculate new columns that exist only in the result:

```sql
SELECT name, marks, marks + 5 AS bonus_marks
FROM students
LIMIT 3;
```

```text
name         | marks | bonus_marks
-------------+-------+------------
Rahul Verma  | 78    | 83
Anita Sharma | 95    | 100
Karan Patel  | 38    | 43
```

Arithmetic: `+` `-` `*` `/` `%`. Text is joined with **`CONCAT()`**:

```sql
SELECT CONCAT(name, ' from ', city) AS description
FROM students
LIMIT 3;
```

```text
+----------------------------+
| description                |
+----------------------------+
| Rahul Verma from Hyderabad |
| Anita Sharma from Chennai  |
| Karan Patel from Hyderabad |
+----------------------------+
```

> ⚠️ **Do not use `||` in MySQL.** In SQLite and PostgreSQL `||` joins strings,
> but in MySQL it means **OR** — `SELECT 'a' || 'b';` returns `0`, with no
> error. This is the single most common mistake when moving between them.

**Key Note:** the table is **not** changed. `marks + 5` only affects what is
displayed. To change stored data you need `UPDATE`.

---

## 10. NULL — The Big Trap

`NULL` means **unknown**, not zero and not empty text. Meera Nair has no marks.

Any comparison with `NULL` gives **not true**:

```sql
SELECT name FROM students WHERE marks = NULL;    -- returns NOTHING
```

You must use `IS NULL` / `IS NOT NULL`:

```sql
SELECT name FROM students WHERE marks IS NULL;
```

```text
name
----------
Meera Nair
```

```sql
SELECT COUNT(*) AS all_rows, COUNT(marks) AS rows_with_marks FROM students;
```

```text
all_rows | rows_with_marks
---------+----------------
10       | 9
```

`COUNT(*)` counts rows; `COUNT(column)` **skips NULLs**. Remember this for Day 11.

To substitute a value, use `IFNULL` (MySQL) / `COALESCE` (everywhere):

```sql
SELECT name, IFNULL(marks, 0) AS marks FROM students WHERE id = 110;
```

```text
name       | marks
-----------+------
Meera Nair | 0
```

---

## 11. Common Mistakes

**1. `WHERE marks = NULL`** — always empty. Use `IS NULL`.

**2. Using an alias in `WHERE`** — it does not exist yet. Repeat the expression
or use a subquery.

**3. Double quotes around text** — MySQL tolerates `"Pune"`, but in PostgreSQL
and standard SQL double quotes mean a *column name*. Always use single quotes.

**4. `==` instead of `=`** — MySQL tolerates `==`, other databases reject it.
Write `=`.

**5. Expecting rows in order without `ORDER BY`.**

**6. `SELECT *` in production code** — breaks quietly when columns change.

---

## 12. Summary

- `SELECT` chooses columns, `WHERE` chooses rows.
- `ORDER BY` sorts (`ASC` default, `DESC` reverse); without it order is undefined.
- `DISTINCT` removes duplicate **rows**, across all selected columns.
- `LIMIT n OFFSET m` returns a page of results.
- **Aliases** rename output — usable in `ORDER BY`, **not** in `WHERE`.
- **Expressions** create calculated columns; `||` joins text.
- `NULL` is unknown: compare with `IS NULL`, count with care, replace with
  `IFNULL` / `COALESCE`.

---

## 13. Practice Questions

1. List every student's name and city.
2. Show only students from Chennai.
3. Show students aged 21 or 22, youngest first.
4. List the distinct cities, alphabetically.
5. Show the top 5 students by marks.
6. Show students ranked 4th to 6th by marks (use `LIMIT` and `OFFSET`).
7. Show `name` and `marks` with headings `Student` and `Score`.
8. Add a column showing each student's marks out of 200 (`marks * 2`).
9. Produce one column reading `Rahul Verma (Hyderabad)` for every student.
10. Find the students with no marks recorded.
11. Find students with no course allotted.
12. Show all students, printing `0` where marks are missing.
13. Students from Pune **or** Kochi who scored above 60.
14. Why does `WHERE marks = NULL` return nothing?
15. Why does `SELECT name AS n FROM students WHERE n = 'Rahul Verma'` fail?
