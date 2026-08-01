# Day 16 · Views, Indexes & Transactions

**Duration:** 50–60 Minutes

### Learning Outcomes
- Save a query as a **view** and use it like a table.
- Speed up searching with an **index**, and know when *not* to add one.
- Group changes into a **transaction** with `COMMIT`, `ROLLBACK` and
  `SAVEPOINT`.
- Understand **ACID**.

---

## 1. Views — A Saved Query

A **view** is a stored `SELECT` that behaves like a table. It holds **no data**
of its own — it runs its query every time you use it.

```sql
CREATE VIEW toppers AS
SELECT name, city, marks
FROM students
WHERE marks >= 75;
```

Now query it like any table:

```sql
SELECT * FROM toppers ORDER BY marks DESC;
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

### Why views?

| Reason | Explanation |
|---|---|
| **Simplicity** | Hide a 5-table join behind one name |
| **Reuse** | Write the logic once, everyone uses the same definition |
| **Security** | Give access to the view, not the table — hide salary columns |
| **Consistency** | One official definition of "topper" for the whole company |

A view over a join is the common case:

```sql
CREATE VIEW student_courses AS
SELECT s.name, s.city, c.course_name, c.fee
FROM students s
LEFT JOIN courses c ON s.course_id = c.course_id;

SELECT * FROM student_courses WHERE fee > 15000;
```

```text
name        | city  | course_name | fee
------------+-------+-------------+------
Priya Nair  | Kochi | Java        | 20000
Sneha Iyer  | Chennai | Java      | 20000
Arjun Mehta | Pune  | DSA         | 25000
Meera Nair  | Chennai | DSA       | 25000
```

**Key Notes:**
- The view is **always current** — change the table and the view reflects it.
- Remove one with `DROP VIEW toppers;`
- Views in SQLite are **read-only**. You cannot `INSERT` into one. (MySQL and
  Oracle allow updates on simple views.)
- A view does **not** make anything faster — it runs the same query each time.
  For speed you need an index.

---

## 2. Indexes — Making Searches Fast

Without an index, finding `city = 'Pune'` means reading **every row** — a
**full table scan**. An index is a sorted lookup structure, like the index at
the back of a textbook.

```text
   No index                    With an index on city
   read row 1  ✗               Chennai  -> rows 2, 6, 10
   read row 2  ✗               Hyderabad-> rows 1, 3, 5
   read row 3  ✗               Kochi    -> rows 4, 8
   ... all 10                  Pune     -> rows 7, 9     <- jump straight there
```

```sql
CREATE INDEX idx_city ON students(city);
```

Check that it is being used with `EXPLAIN QUERY PLAN`:

```sql
EXPLAIN QUERY PLAN SELECT * FROM students WHERE city = 'Pune';
```

```text
SEARCH students USING INDEX idx_city (city=?)
```

Without the index the same command reports:

```text
SCAN students
```

**`SEARCH … USING INDEX`** = good. **`SCAN`** = reading everything.

### The cost of an index

An index is not free:

| | Effect |
|---|---|
| `SELECT` | ✅ Much faster |
| `INSERT`, `UPDATE`, `DELETE` | ❌ Slower — the index must be updated too |
| Disk space | ❌ More |

**Index columns you search, join or sort on. Do not index everything.**

| Good candidate | Bad candidate |
|---|---|
| A column in many `WHERE` clauses | A column you never filter on |
| A foreign key used in joins | A tiny table (10 rows — a scan is fine) |
| A column you `ORDER BY` a lot | A column with 2 values (e.g. yes/no) |

**Key Notes:**
- A `PRIMARY KEY` is indexed **automatically**. So is `UNIQUE`.
- Multi-column: `CREATE INDEX idx ON students(city, marks);` — helps queries
  filtering on `city`, or on `city` **and** `marks`, but not `marks` alone.
- Drop with `DROP INDEX idx_city;`

---

## 3. Transactions

A **transaction** groups statements so they either **all** succeed or **all**
fail. The classic example is a bank transfer — two updates that must never come
apart:

```sql
BEGIN TRANSACTION;
    UPDATE accounts SET balance = balance - 1000 WHERE id = 1;
    UPDATE accounts SET balance = balance + 1000 WHERE id = 2;
COMMIT;
```

If the power fails between the two lines, the money would vanish. Inside a
transaction, nothing is saved until `COMMIT`.

| Command | Does |
|---|---|
| `BEGIN TRANSACTION;` | start (also `BEGIN;`) |
| `COMMIT;` | make every change permanent |
| `ROLLBACK;` | undo **everything** since `BEGIN` |
| `SAVEPOINT name;` | set a marker part-way |
| `ROLLBACK TO name;` | undo back to that marker only |
| `RELEASE name;` | discard the marker, keep the work |

### ROLLBACK in action

```sql
BEGIN TRANSACTION;
DELETE FROM students WHERE city = 'Pune';
SELECT COUNT(*) FROM students;      -- 8, the delete has happened...
ROLLBACK;
SELECT COUNT(*) FROM students;      -- 10, ...and is now undone
```

```text
count_after_delete | count_after_rollback
-------------------+---------------------
8                  | 10
```

**Key Note:** `ROLLBACK` only works **before** `COMMIT`. After a commit, the
change is permanent — that is what "commit" means.

### SAVEPOINT — partial undo

```sql
BEGIN TRANSACTION;
    INSERT INTO students (id, name, city) VALUES (201, 'Test One', 'Delhi');
    SAVEPOINT after_first;
    INSERT INTO students (id, name, city) VALUES (202, 'Test Two', 'Delhi');
    ROLLBACK TO after_first;        -- Test Two is undone, Test One survives
COMMIT;                             -- Test One is saved
```

```text
name     | city
---------+------
Test One | Delhi
```

Only `Test Two` was removed. Savepoints let a long process undo one step
without throwing away everything.

---

## 4. ACID

The four guarantees a transaction gives you:

| Letter | Means | In practice |
|---|---|---|
| **A** — Atomicity | All or nothing | Half a transfer can never happen |
| **C** — Consistency | Rules always hold | Constraints are never left broken |
| **I** — Isolation | Concurrent work does not interfere | Two users do not see each other's half-done work |
| **D** — Durability | Committed means saved | A power cut after `COMMIT` loses nothing |

**Key Note:** SQLite is fully ACID — the guarantees are not a big-database
luxury.

### DB Browser and transactions

DB Browser wraps your work in a transaction automatically. That is exactly what
the toolbar buttons are:

| Button | SQL equivalent |
|---|---|
| **Write Changes** | `COMMIT` |
| **Revert Changes** | `ROLLBACK` |

So the rule from Day 1 — *always click Write Changes* — was really "always
commit your transaction".

---

## 5. Views vs Indexes — Do Not Confuse Them

| | View | Index |
|---|---|---|
| Is | a saved **query** | a lookup **structure** |
| Stores data | ❌ no | ✅ yes (a sorted copy of the key) |
| Purpose | simplicity, reuse, security | **speed** |
| Affects writes | no | yes, slows them |
| You query it | ✅ directly by name | ❌ never — the optimiser uses it |

---

## 6. Common Mistakes

**1. Thinking a view makes queries faster** — it does not. It re-runs the query.

**2. Indexing every column** — writes slow down and space is wasted for no gain.

**3. Forgetting to `COMMIT`** — in DB Browser, forgetting **Write Changes**.
Your work is lost when the program closes.

**4. Expecting `ROLLBACK` to undo a committed change** — it cannot.

**5. Inserting into a view in SQLite** — views are read-only there.

**6. Indexing a tiny table** — for 10 rows a scan is faster than an index lookup.

---

## 7. Summary

- A **view** is a stored `SELECT` used like a table. It holds no data, is always
  current, and is read-only in SQLite. Use it for simplicity, reuse and security.
- An **index** is a sorted structure that turns a `SCAN` into a `SEARCH`.
  Check with `EXPLAIN QUERY PLAN`. It speeds reads and **slows writes** — index
  what you filter, join or sort on.
- A **transaction** makes several statements all-or-nothing:
  `BEGIN` → work → `COMMIT` (keep) or `ROLLBACK` (undo).
- **`SAVEPOINT`** + `ROLLBACK TO` undoes part of a transaction.
- **ACID** = Atomicity, Consistency, Isolation, Durability.
- In DB Browser, **Write Changes = COMMIT** and **Revert Changes = ROLLBACK**.

---

## 8. Practice Questions

1. Create a view `passed_students` showing everyone with marks of 50 or more.
2. Query your view, sorted by marks.
3. Create a view joining students to their course name and fee.
4. Drop a view. Does the underlying data change?
5. Why does a view not make a slow query faster?
6. Create an index on `students(marks)`.
7. Run `EXPLAIN QUERY PLAN` for `WHERE marks > 80` before and after. What
   changes?
8. Give two reasons **not** to add an index.
9. Which two constraints create an index automatically?
10. Start a transaction, delete all Kochi students, check the count, then
    `ROLLBACK` and check again.
11. Use a `SAVEPOINT` to insert two rows and keep only the first.
12. Explain each letter of ACID in one sentence.
13. Which DB Browser buttons are `COMMIT` and `ROLLBACK`?
14. Can you `ROLLBACK` after a `COMMIT`? Why not?
