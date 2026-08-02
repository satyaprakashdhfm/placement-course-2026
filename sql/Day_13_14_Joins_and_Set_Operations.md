# Day 13–14 · Joins & Set Operations

**Duration:** 2 × 50–60 Minutes

### Learning Outcomes
- Combine tables with **`INNER`**, **`LEFT`**, **`RIGHT`**, **`FULL`** and
  **`SELF`** joins.
- Know exactly which rows each one keeps.
- Combine result **sets** with **`UNION`** and `UNION ALL`.
- Tell a **join** (sideways, more columns) from a **union** (downwards, more rows).

> ⚠️ **MySQL has no `FULL OUTER JOIN`** — see §5 for the standard workaround.
> `RIGHT JOIN` works fine.

---

## 1. Why Join?

Our data is split across two tables on purpose:

```text
   students                          courses
   ┌───────────────────┐             ┌──────────────────────┐
   │ id  name  course_id│────────────►│ course_id  course_name│
   └───────────────────┘             └──────────────────────┘
```

Storing the course *name* against every student would repeat `'Python'` three
times — and renaming the course would mean editing many rows. Splitting the
data avoids that; a **join** puts it back together when you need it.

---

## 2. INNER JOIN — Only Matching Rows

```sql
SELECT s.name, c.course_name
FROM students s
INNER JOIN courses c ON s.course_id = c.course_id
LIMIT 4;
```

```text
name         | course_name
-------------+------------
Rahul Verma  | Python
Anita Sharma | SQL
Karan Patel  | Python
Priya Nair   | Java
```

- `s` and `c` are **table aliases** — without them you would write
  `students.course_id` every time.
- `ON` says how the tables line up. Nearly always foreign key = primary key.
- `INNER` is the default: `JOIN` alone means `INNER JOIN`.

**Only rows that match on both sides survive.** Rohit Sinha (no course) and
Cloud (no students) are both missing from the result.

---

## 3. LEFT JOIN — Keep Everything on the Left

```sql
SELECT s.name, c.course_name
FROM students s
LEFT JOIN courses c ON s.course_id = c.course_id;
```

```text
name         | course_name
-------------+------------
Rahul Verma  | Python
Anita Sharma | SQL
Karan Patel  | Python
Priya Nair   | Java
Vikram Rao   | SQL
Sneha Iyer   | Java
Arjun Mehta  | DSA
Divya Menon  | Python
Rohit Sinha  | NULL
Meera Nair   | DSA
```

All 10 students appear. Rohit has no course, so his `course_name` is `NULL`.

### The "find the orphans" pattern

A `LEFT JOIN` plus `IS NULL` finds rows with **no match** — one of the most
useful patterns in SQL:

```sql
SELECT s.name
FROM students s
LEFT JOIN courses c ON s.course_id = c.course_id
WHERE c.course_name IS NULL;
```

```text
name
-----------
Rohit Sinha
```

---

## 4. RIGHT JOIN — Keep Everything on the Right

```sql
SELECT s.name, c.course_name
FROM students s
RIGHT JOIN courses c ON s.course_id = c.course_id
WHERE s.name IS NULL;
```

```text
name | course_name
-----+------------
NULL | Cloud
```

Cloud has no students, so it survives with a `NULL` name.

**Key Note:** `A RIGHT JOIN B` is identical to `B LEFT JOIN A`. Many teams ban
`RIGHT JOIN` for readability — you can always swap the tables and use `LEFT`.

---

## 5. FULL OUTER JOIN — Which MySQL Does Not Have

A full outer join keeps **both** unmatched sides: the student with no course
**and** the course with no students.

```sql
SELECT s.name, c.course_name
FROM students s
FULL OUTER JOIN courses c ON s.course_id = c.course_id;
```

```text
ERROR 1064 (42000): You have an error in your SQL syntax ... near 'OUTER JOIN courses'
```

⚠️ **MySQL has no `FULL OUTER JOIN`.** PostgreSQL and SQLite (3.39+) do. You
emulate it with `LEFT` + `UNION` + `RIGHT` — **memorise this, it is a standard
interview question:**

```sql
SELECT s.name, c.course_name
FROM students s LEFT JOIN courses c ON s.course_id = c.course_id
UNION
SELECT s.name, c.course_name
FROM students s RIGHT JOIN courses c ON s.course_id = c.course_id;
```

```text
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
| NULL         | Cloud       |
| Meera Nair   | DSA         |
+--------------+-------------+
```

Eleven rows: the ten students, plus Cloud. Both orphans are present.

**Key Note:** use `UNION`, **not** `UNION ALL`. The matching rows appear in both
halves, and `UNION` removes the duplicates. `UNION ALL` would list them twice.

### The four joins side by side

```text
   INNER            LEFT             RIGHT            FULL
   ┌───┬───┐        ┌───┬───┐        ┌───┬───┐        ┌───┬───┐
   │   │▓▓▓│        │▓▓▓│▓▓▓│        │   │▓▓▓│        │▓▓▓│▓▓▓│
   │   │▓▓▓│        │▓▓▓│▓▓▓│        │   │▓▓▓│        │▓▓▓│▓▓▓│
   └───┴───┘        └───┴───┘        └───┴───┘        └───┴───┘
   only matches     all left +       all right +      everything
                    matches          matches          (not in MySQL)
```

| Join | Keeps | MySQL |
|---|---|---|
| `INNER` | rows matching in **both** | ✅ |
| `LEFT` | **all** left rows + matches | ✅ |
| `RIGHT` | **all** right rows + matches | ✅ |
| `FULL OUTER` | **all** rows from both | ❌ emulate with `UNION` |
| `CROSS` | every combination (10 × 5 = 50 rows) | ✅ |

---

## 6. SELF JOIN — A Table Joined to Itself

Used when rows point at other rows in the **same** table. Our `employees`
table has a `manager_id` pointing at another `emp_id`:

```sql
SELECT e.emp_name AS employee, m.emp_name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.emp_id;
```

```text
employee | manager
---------+--------
Anil     | NULL
Bhavna   | Anil
Chetan   | Anil
Deepa    | Bhavna
Esha     | Bhavna
```

**Key Notes:**
- Aliases are **compulsory** here — `e` and `m` are the same table twice, and
  without different names SQL cannot tell them apart.
- `LEFT JOIN` keeps Anil, the boss, who has no manager. An `INNER JOIN` would
  drop him.

---

## 7. Joining with GROUP BY

Joins and grouping combine constantly:

```sql
SELECT c.course_name, COUNT(s.id) AS enrolled
FROM courses c
LEFT JOIN students s ON s.course_id = c.course_id
GROUP BY c.course_name
ORDER BY enrolled DESC;
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

> ⚠️ **Use `COUNT(s.id)`, not `COUNT(*)`.** `COUNT(*)` counts the *row*, and the
> `LEFT JOIN` produces one row for Cloud with all-NULL student columns — so
> `COUNT(*)` would report **1** for Cloud instead of 0. `COUNT(s.id)` skips
> NULLs and correctly gives 0. This is a favourite interview trap.

Joining three tables works the same way — chain the joins:

```sql
SELECT s.name, c.course_name, c.fee
FROM students s
JOIN courses c ON s.course_id = c.course_id
WHERE c.fee > 15000
ORDER BY c.fee DESC;
```

```text
name        | course_name | fee
------------+-------------+------
Arjun Mehta | DSA         | 25000
Meera Nair  | DSA         | 25000
Priya Nair  | Java        | 20000
Sneha Iyer  | Java        | 20000
```

---

## 8. UNION — Stacking Results

A join adds **columns** (sideways). A union adds **rows** (downwards).

```text
   JOIN                          UNION
   ┌────┬────┐                   ┌────┐
   │ A  │ B  │                   │ A  │
   └────┴────┘                   ├────┤
   wider                         │ B  │
                                 └────┘
                                 taller
```

```sql
SELECT name AS person, city AS place FROM students WHERE city = 'Pune'
UNION
SELECT emp_name, 'Office' FROM employees WHERE salary > 65000;
```

```text
person      | place
------------+-------
Anil        | Office
Arjun Mehta | Pune
Bhavna      | Office
Rohit Sinha | Pune
```

**Rules for `UNION`:**
1. Both queries need the **same number of columns**.
2. Columns must be in the **same order** with compatible types.
3. Column names come from the **first** query.
4. `ORDER BY` goes at the very **end**, once.

### UNION vs UNION ALL

| | `UNION` | `UNION ALL` |
|---|---|---|
| Duplicates | **removed** | **kept** |
| Speed | slower (must sort/compare) | faster |

```sql
SELECT city FROM students WHERE city='Pune'
UNION ALL
SELECT city FROM students WHERE city='Pune';
```

```text
city
----
Pune
Pune
Pune
Pune
```

With `UNION` instead, that returns one row. **Use `UNION ALL` unless you
actually need duplicates removed** — it avoids needless work.

---

## 9. Common Mistakes

**1. Forgetting `ON`** — `FROM a JOIN b` with no condition gives a **cross
join**: every row paired with every row. 10 students × 5 courses = 50 rows.

**2. `COUNT(*)` with a `LEFT JOIN`** — counts non-matching rows as 1 instead of
0. Count a column from the right-hand table.

**3. Filtering the outer table in `WHERE`** — this:
```sql
FROM courses c LEFT JOIN students s ON ... WHERE s.marks > 50
```
silently turns your `LEFT JOIN` into an `INNER JOIN`, because `NULL > 50` is not
true. Put the condition in the `ON` clause instead:
```sql
LEFT JOIN students s ON s.course_id = c.course_id AND s.marks > 50
```

**4. No aliases in a self join** — SQL cannot tell the two copies apart.

**5. Different column counts in a `UNION`.**

**6. `UNION` where `UNION ALL` was meant** — losing legitimate duplicate rows.

---

## 10. Summary

- A **join** widens the result; a **union** lengthens it.
- `INNER` keeps matches only · `LEFT` keeps all of the left · `RIGHT` keeps all
  of the right · `CROSS` pairs everything.
- **MySQL has no `FULL OUTER JOIN`**: use `LEFT` `UNION` `RIGHT`.
- `A RIGHT JOIN B` = `B LEFT JOIN A`. Prefer `LEFT` for readability.
- **`LEFT JOIN … WHERE right IS NULL`** finds unmatched rows.
- A **self join** needs two aliases for the same table.
- With `LEFT JOIN` + `GROUP BY`, count a **column**, not `*`.
- `UNION` removes duplicates, `UNION ALL` keeps them and is faster.

---

## 11. Practice Questions

1. List every student with their course name.
2. List every student *including* those with no course.
3. Find students who have no course.
4. Find courses nobody has joined (two ways: `RIGHT JOIN`, and `LEFT JOIN` from
   `courses`).
4b. Write a full outer join of students and courses without `FULL OUTER JOIN`.
5. Show students on courses costing more than ₹15,000.
6. Count the students on each course, including empty courses.
7. Why must that count use `COUNT(s.id)` and not `COUNT(*)`?
8. Show each employee with their manager's name.
9. Which employee has no manager, and which join keeps them?
10. Average marks per course name, best first.
11. Show every student–course pair that could exist (`CROSS JOIN`). How many rows?
12. Stack the student names and employee names into one list.
13. What is the difference between `UNION` and `UNION ALL`?
14. Rewrite `students RIGHT JOIN courses` as a `LEFT JOIN`.
15. Explain why moving a condition from `WHERE` to `ON` changes a `LEFT JOIN`.
