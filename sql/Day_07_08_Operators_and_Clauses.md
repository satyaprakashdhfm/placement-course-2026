# Day 7–8 · Operators & Clauses

**Duration:** 2 × 50–60 Minutes

### Learning Outcomes
- Use **comparison** and **logical** operators, and know their precedence.
- Filter with **`IN`**, **`BETWEEN`**, **`LIKE`**, **`EXISTS`**.
- Know what **`ANY`** and **`ALL`** do, and what to write instead in MySQL.
- Understand **three-valued logic** — `TRUE`, `FALSE`, and `NULL`.

---

## 1. Comparison Operators

| Operator | Meaning | Example |
|---|---|---|
| `=` | equal | `marks = 78` |
| `<>` `!=` | not equal | `city <> 'Pune'` |
| `>` `<` | greater / less | `age > 21` |
| `>=` `<=` | greater / less or equal | `marks >= 40` |
| `IS NULL` | has no value | `marks IS NULL` |
| `IS NOT NULL` | has a value | `marks IS NOT NULL` |

**Key Note:** `<>` is the SQL standard, `!=` is accepted almost everywhere.
Pick one and be consistent.

---

## 2. Logical Operators and Precedence

| Operator | True when |
|---|---|
| `AND` | **both** sides are true |
| `OR` | **either** side is true |
| `NOT` | the condition is false |

Precedence: **`NOT` → `AND` → `OR`**. `AND` binds tighter than `OR`, which is
the cause of countless wrong results:

The intent below is *"students from Hyderabad or Kochi who scored above 60"*.

```sql
-- WRONG: reads as  city='Hyderabad'  OR  (city='Kochi' AND marks>60)
SELECT name, city, marks FROM students
WHERE city = 'Hyderabad' OR city = 'Kochi' AND marks > 60;
```

```text
name        | city      | marks
------------+-----------+------
Rahul Verma | Hyderabad | 78
Karan Patel | Hyderabad | 38     <-- WRONG, he scored 38
Priya Nair  | Kochi     | 66
Vikram Rao  | Hyderabad | 81
```

`AND` bound tighter, so the marks test was applied **only to Kochi**. Every
Hyderabad student came through regardless. Brackets fix it:

```sql
SELECT name, city, marks FROM students
WHERE (city = 'Hyderabad' OR city = 'Kochi') AND marks > 60;
```

```text
name        | city      | marks
------------+-----------+------
Rahul Verma | Hyderabad | 78
Priya Nair  | Kochi     | 66
Vikram Rao  | Hyderabad | 81
```

**Key Note:** when you mix `AND` and `OR`, **always use brackets.** Even when
the result is the same, the next person reading it should not have to work out
precedence.

---

## 3. IN — Match Any of a List

```sql
SELECT name, city FROM students WHERE city IN ('Chennai', 'Pune');
```

```text
name         | city
-------------+--------
Anita Sharma | Chennai
Sneha Iyer   | Chennai
Arjun Mehta  | Pune
Rohit Sinha  | Pune
Meera Nair   | Chennai
```

`IN` is shorthand for a chain of `OR`s:

```sql
WHERE city = 'Chennai' OR city = 'Pune'    -- identical meaning
```

`NOT IN` reverses it:

```sql
SELECT name, city FROM students WHERE city NOT IN ('Chennai', 'Pune');
```

```text
name        | city
------------+----------
Rahul Verma | Hyderabad
Karan Patel | Hyderabad
Priya Nair  | Kochi
Vikram Rao  | Hyderabad
Divya Menon | Kochi
```

> ⚠️ **`NOT IN` with a NULL in the list returns nothing at all.**
> `WHERE course_id NOT IN (1, 2, NULL)` gives zero rows, because SQL cannot
> prove `course_id` differs from an unknown value. Use `NOT EXISTS` instead.

---

## 4. BETWEEN — Match a Range

```sql
SELECT name, age FROM students WHERE age BETWEEN 21 AND 22;
```

```text
name         | age
-------------+----
Rahul Verma  | 21
Anita Sharma | 22
Vikram Rao   | 21
Sneha Iyer   | 22
Meera Nair   | 21
```

`BETWEEN` is **inclusive** on both ends — the same as `age >= 21 AND age <= 22`.

**Key Notes:**
- The small value comes **first**. `BETWEEN 22 AND 21` returns nothing.
- It works on text and dates too:
  `WHERE joined_on BETWEEN '2025-01-01' AND '2025-03-31'`.

---

## 5. LIKE — Pattern Matching

| Wildcard | Means |
|---|---|
| `%` | any number of characters (including none) |
| `_` | exactly one character |

```sql
SELECT name FROM students WHERE name LIKE '%a Nair';
```

```text
name
----------
Priya Nair
Meera Nair
```

| Pattern | Finds |
|---|---|
| `'R%'` | starts with R |
| `'%a'` | ends with a |
| `'%Nair%'` | contains Nair anywhere |
| `'_a%'` | second letter is a |

```sql
SELECT name FROM students WHERE name LIKE 'R%';
```

```text
name
-----------
Rahul Verma
Rohit Sinha
```

📌 **Dialect corner.** In MySQL, `LIKE` is **case-insensitive** — `'r%'` finds
Rahul too. SQLite is also insensitive for `LIKE`. PostgreSQL is case-**sensitive**
(`ILIKE` is its insensitive version). Use `LOWER()` when it must be portable.

---

## 6. EXISTS — Does a Related Row Exist?

`EXISTS` takes a subquery and returns true if it produces **at least one row**.

```sql
SELECT course_name
FROM courses c
WHERE EXISTS (SELECT 1 FROM students s WHERE s.course_id = c.course_id);
```

```text
course_name
-----------
Python
SQL
Java
DSA
```

Cloud is missing — nobody has enrolled. `NOT EXISTS` finds exactly that:

```sql
SELECT course_name
FROM courses c
WHERE NOT EXISTS (SELECT 1 FROM students s WHERE s.course_id = c.course_id);
```

```text
course_name
-----------
Cloud
```

**Key Notes:**
- `SELECT 1` is a convention — `EXISTS` only cares *whether* rows come back,
  never what is in them.
- `EXISTS` stops at the first match, so it is often faster than `IN` on large
  tables.
- **`NOT EXISTS` is NULL-safe**, unlike `NOT IN`. When in doubt, use it.

---

## 7. IN vs EXISTS

| | `IN` | `EXISTS` |
|---|---|---|
| Compares | a value against a list | whether rows exist |
| Subquery returns | one column | anything (`SELECT 1`) |
| NULL behaviour | `NOT IN` breaks | safe |
| Usually faster when | the list is small | the subquery is large |

---

## 8. ANY and ALL

These compare a value against **every** result of a subquery.

| Form | True when |
|---|---|
| `x > ANY (subquery)` | x is greater than **at least one** value |
| `x > ALL (subquery)` | x is greater than **every** value |

### They work in MySQL

```sql
SELECT name, marks FROM students
WHERE marks > ANY (SELECT marks FROM students WHERE city = 'Kochi');
```

```text
+--------------+-------+
| name         | marks |
+--------------+-------+
| Rahul Verma  |    78 |
| Anita Sharma |    95 |
| Priya Nair   |    66 |
| Vikram Rao   |    81 |
| Sneha Iyer   |    54 |
| Arjun Mehta  |    90 |
| Rohit Sinha  |    78 |
+--------------+-------+
```

📌 **Dialect corner.** PostgreSQL supports `ANY`/`ALL` too, but **SQLite does
not** — there you must rewrite them. The rewrites are worth knowing anyway,
because they say plainly what the operators mean:

| Instead of | Write |
|---|---|
| `= ANY (sub)` | `IN (sub)` |
| `<> ALL (sub)` | `NOT IN (sub)` |
| `> ANY (sub)` | `> (SELECT MIN(...) FROM ...)` |
| `> ALL (sub)` | `> (SELECT MAX(...) FROM ...)` |

```sql
-- "> ANY" is the same as beating the WEAKEST Kochi student
SELECT name, marks FROM students
WHERE marks > (SELECT MIN(marks) FROM students WHERE city = 'Kochi');
```

```text
name         | marks
-------------+------
Rahul Verma  | 78
Anita Sharma | 95
Priya Nair   | 66
Vikram Rao   | 81
Sneha Iyer   | 54
Arjun Mehta  | 90
Rohit Sinha  | 78
```

```sql
-- "> ALL" -> beat the BEST Kochi student
SELECT name, marks FROM students
WHERE marks > (SELECT MAX(marks) FROM students WHERE city = 'Kochi');
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

**Key Note for interviews:** `> ANY` means *greater than the minimum*;
`> ALL` means *greater than the maximum*. That one sentence answers most
questions on this topic.

---

## 9. Three-Valued Logic

SQL conditions are not just true/false. They can be **`NULL`** (unknown).

| `A` | `B` | `A AND B` | `A OR B` |
|---|---|---|---|
| TRUE | NULL | NULL | TRUE |
| FALSE | NULL | FALSE | NULL |
| NULL | NULL | NULL | NULL |

A `WHERE` clause keeps a row **only when the result is TRUE.** `NULL` is not
true, so the row is dropped. This is why:

```sql
SELECT name FROM students WHERE marks <> 78;
```

```text
name
------------
Anita Sharma
Karan Patel
Priya Nair
Vikram Rao
Sneha Iyer
Arjun Mehta
Divya Menon
```

Meera Nair (`marks IS NULL`) is **not** listed, even though unknown marks are
arguably "not 78". To include her you must say so:

```sql
SELECT name FROM students WHERE marks <> 78 OR marks IS NULL;
```

---

## 10. Common Mistakes

**1. Mixing `AND` / `OR` without brackets** — the classic wrong-result bug.

**2. `NOT IN` with NULLs** — silently returns nothing. Use `NOT EXISTS`.

**3. `BETWEEN` with the bigger number first** — always empty.

**4. Using `ANY` / `ALL` and then moving to SQLite** — they do not exist there.
Know the `MIN`/`MAX`/`IN` rewrites.

**5. Forgetting NULL rows vanish** from `<>` comparisons.

**6. `LIKE 'R%'` vs `LIKE '%R%'`** — the first is "starts with", the second is
"contains".

---

## 11. Summary

- Comparison: `=` `<>` `>` `<` `>=` `<=`, plus `IS NULL` for unknowns.
- Precedence is **`NOT` → `AND` → `OR`**; bracket every mixed condition.
- `IN` = a shorter chain of `OR`s. `BETWEEN` = inclusive range.
  `LIKE` = pattern with `%` (many) and `_` (one).
- `EXISTS` tests whether related rows exist and is **NULL-safe**;
  `NOT IN` is not.
- `ANY` / `ALL` work in MySQL and PostgreSQL, **not in SQLite**. `> ANY` is
  `> MIN`, `> ALL` is `> MAX`, `= ANY` is `IN`.
- SQL logic has **three** values; a `WHERE` keeps only rows that are TRUE.

---

## 12. Practice Questions

1. Students who are **not** from Hyderabad.
2. Students aged between 20 and 22 inclusive.
3. Students whose name starts with `A`.
4. Students whose name contains `Nair`.
5. Students whose name has exactly 11 characters (use `_`).
6. Students in Pune or Kochi **with** marks above 60 — bracketed correctly.
7. Rewrite question 6 using `IN`.
8. Courses that no student has joined, using `NOT EXISTS`.
9. Courses that at least one student has joined, using `EXISTS`.
10. Students who scored more than **every** Kochi student.
11. Students who scored more than **any one** Kochi student.
12. Why does `WHERE marks <> 78` leave out the student with no marks?
13. Why is `NOT EXISTS` safer than `NOT IN`?
14. Rewrite an `ANY` and an `ALL` query without using those keywords.
