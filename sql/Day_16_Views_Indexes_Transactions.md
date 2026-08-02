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
+--------------+-----------+-------+
| name         | city      | marks |
+--------------+-----------+-------+
| Anita Sharma | Chennai   |    95 |
| Arjun Mehta  | Pune      |    90 |
| Vikram Rao   | Hyderabad |    81 |
| Rahul Verma  | Hyderabad |    78 |
| Rohit Sinha  | Pune      |    78 |
+--------------+-----------+-------+
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
+-------------+---------+-------------+-------+
| name        | city    | course_name | fee   |
+-------------+---------+-------------+-------+
| Priya Nair  | Kochi   | Java        | 20000 |
| Sneha Iyer  | Chennai | Java        | 20000 |
| Arjun Mehta | Pune    | DSA         | 25000 |
| Meera Nair  | Chennai | DSA         | 25000 |
+-------------+---------+-------------+-------+
```

**Key Notes:**
- The view is **always current** — change the table and the view reflects it.
- Remove one with `DROP VIEW toppers;`
- A **simple** view in MySQL is **updatable** — an `INSERT` into `toppers`
  really inserts into `students`. Views over joins, `GROUP BY` or `DISTINCT`
  are not. 📌 In SQLite views are **always read-only**.
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

Check that it is being used with `EXPLAIN`:

```sql
EXPLAIN SELECT * FROM students WHERE city = 'Pune';
```

Before the index:

```text
+----+----------+------+---------------+------+------+-------------+
| id | table    | type | possible_keys | key  | rows | Extra       |
+----+----------+------+---------------+------+------+-------------+
|  1 | students | ALL  | NULL          | NULL |   10 | Using where |
+----+----------+------+---------------+------+------+-------------+
```

After `CREATE INDEX idx_city ON students(city);`:

```text
+----+----------+------+---------------+----------+------+-------+
| id | table    | type | possible_keys | key      | rows | Extra |
+----+----------+------+---------------+----------+------+-------+
|  1 | students | ref  | idx_city      | idx_city |    2 | NULL  |
+----+----------+------+---------------+----------+------+-------+
```

Read the **`type`** and **`rows`** columns:

| | Before | After |
|---|---|---|
| `type` | **`ALL`** — full table scan | **`ref`** — index lookup |
| `key` | `NULL` — no index used | `idx_city` |
| `rows` | 10 — read everything | 2 — read only what matches |

**`type: ALL` is the warning sign.** On ten rows it does not matter; on ten
million it is the difference between instant and unusable.

📌 **Dialect corner.** SQLite says `SCAN students` / `SEARCH students USING
INDEX`. PostgreSQL says `Seq Scan` / `Index Scan`, and `EXPLAIN ANALYZE` there
actually runs the query and reports real timings.

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
- Drop with `DROP INDEX idx_city ON students;` — MySQL needs the table name.
  📌 SQLite and PostgreSQL just say `DROP INDEX idx_city;`

---

## 3. Transactions

A **transaction** groups statements so they either **all** succeed or **all**
fail. The classic example is a bank transfer — two updates that must never come
apart:

```sql
START TRANSACTION;
    UPDATE accounts SET balance = balance - 1000 WHERE id = 1;
    UPDATE accounts SET balance = balance + 1000 WHERE id = 2;
COMMIT;
```

If the power fails between the two lines, the money would vanish. Inside a
transaction, nothing is saved until `COMMIT`.

| Command | Does |
|---|---|
| `START TRANSACTION;` | start (also `BEGIN;`) |
| `COMMIT;` | make every change permanent |
| `ROLLBACK;` | undo **everything** since `BEGIN` |
| `SAVEPOINT name;` | set a marker part-way |
| `ROLLBACK TO name;` | undo back to that marker only |
| `RELEASE name;` | discard the marker, keep the work |

### ROLLBACK in action

```sql
START TRANSACTION;
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
START TRANSACTION;
    INSERT INTO students (id, name, city) VALUES (201, 'Test One', 'Delhi');
    SAVEPOINT after_first;
    INSERT INTO students (id, name, city) VALUES (202, 'Test Two', 'Delhi');
    ROLLBACK TO after_first;        -- Test Two is undone, Test One survives
COMMIT;                             -- Test One is saved
```

```text
+----------+-------+
| name     | city  |
+----------+-------+
| Test One | Delhi |
+----------+-------+
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

**Key Note:** MySQL is fully ACID — the guarantees are not a big-database
luxury.

### Workbench and transactions

MySQL runs with **`autocommit = 1`** by default: every statement is its own
transaction, committed the moment it succeeds. There is no "save" button, and
no undo.

```sql
SELECT @@autocommit;      -- 1 = on
```

`ROLLBACK` therefore only does something once you have **explicitly** started a
transaction with `BEGIN` or `START TRANSACTION`. Outside one, your `DELETE` is
already permanent.

```sql
SET autocommit = 0;       -- now nothing saves until you COMMIT
```

📌 **Dialect corner.** SQLite tools such as DB Browser hold a transaction open
for you and expose it as a **Write Changes** button (`COMMIT`) and **Revert
Changes** (`ROLLBACK`). MySQL and PostgreSQL both autocommit by default — the
safety net is not there, so open transactions yourself before risky work.

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

**3. Assuming you can undo without a transaction** — MySQL autocommits, so a
`DELETE` outside `BEGIN` is already permanent.

**4. Expecting `ROLLBACK` to undo a committed change** — it cannot.

**5. Inserting into a view in MySQL** — views are read-only there.

**6. Indexing a tiny table** — for 10 rows a scan is faster than an index lookup.

---

## 7. Summary

- A **view** is a stored `SELECT` used like a table. It holds no data, is always
  current, and in MySQL is often **updatable**. Use it for simplicity, reuse
  and security. 📌 In SQLite views are strictly read-only.
- An **index** is a sorted structure that turns a `SCAN` into a `SEARCH`.
  Check with `EXPLAIN`. It speeds reads and **slows writes** — index
  what you filter, join or sort on.
- A **transaction** makes several statements all-or-nothing:
  `BEGIN` → work → `COMMIT` (keep) or `ROLLBACK` (undo).
- **`SAVEPOINT`** + `ROLLBACK TO` undoes part of a transaction.
- **ACID** = Atomicity, Consistency, Isolation, Durability.
- MySQL **autocommits**: `ROLLBACK` only helps after an explicit `BEGIN`.

---

## 8. 🔺 ADVANCED — Teacher Reference

### 8.1 Composite indexes and the leftmost-prefix rule

**The most valuable index concept there is.** An index on `(city, marks)` is
sorted by city first, then marks — like a phone book by surname, then first name.

```sql
CREATE INDEX idx_city_marks ON students(city, marks);
```

| Query | Uses the index? |
|---|---|
| `WHERE city = 'Pune'` | ✅ yes |
| `WHERE city = 'Pune' AND marks > 70` | ✅ **fully** |
| `WHERE marks > 70` | ⚠️ only as a scan — the leading column is missing |
| `WHERE marks > 70 AND city = 'Pune'` | ✅ yes — **order in `WHERE` does not matter** |

Proof from `EXPLAIN`:

```sql
EXPLAIN SELECT id FROM students WHERE city='Pune' AND marks>70;
```
```text
| type  | key            | rows | Extra                    |
| range | idx_city_marks |    2 | Using where; Using index |
```

```sql
EXPLAIN SELECT id FROM students WHERE marks>70;      -- skips the leading column
```
```text
| type  | key            | rows | Extra                    |
| index | idx_city_marks |   10 | Using where; Using index |
```

`type: range` reading 2 rows, versus `type: index` scanning all 10. Same index,
very different work.

**Teaching line:** *you can use a prefix of an index, never a suffix.* You may
look up "Sharma, Anita" or "Sharma" in a phone book, but not "Anita".

### 8.2 Covering indexes

Notice `Using index` in both plans above — MySQL answered the query **from the
index alone**, never touching the table. That is a **covering index**, and it is
the single biggest index win.

```sql
EXPLAIN SELECT city, marks FROM students WHERE city='Pune';
```
```text
| type | key            | rows | Extra       |
| ref  | idx_city_marks |    2 | Using index |
```

Both selected columns live in the index, so no row lookup happens. Adding a
frequently-selected column to an index purely to make it covering is a standard
tuning move.

⚠️ `SELECT *` almost never uses a covering index — one more reason to name your
columns.

### 8.3 Reading EXPLAIN properly

The `type` column, best to worst:

| `type` | Meaning |
|---|---|
| `const` / `eq_ref` | one row via a unique key — perfect |
| `ref` | index lookup, several rows — good |
| `range` | index range scan — good |
| `index` | **full index scan** — mediocre |
| `ALL` | **full table scan** — the warning sign |

And the `Extra` column:

| `Extra` | Means |
|---|---|
| `Using index` | ✅ covering index, no table access |
| `Using where` | rows filtered after reading |
| `Using temporary` | ⚠️ a temp table was built (often `GROUP BY`) |
| `Using filesort` | ⚠️ a sort no index could satisfy |
| `Using join buffer` | ⚠️ joining without an index — add one |

`EXPLAIN ANALYZE` (8.0.18+) actually **runs** the query and prints real timings
beside the estimates — the fastest way to spot a bad row estimate.

### 8.4 Cardinality — when an index is useless

```sql
SHOW INDEX FROM students;
```

The `Cardinality` column is the number of distinct values. An index only helps
when it is **selective** — roughly, when it narrows the search to under a third
of the table.

| Column | Cardinality | Worth indexing? |
|---|---|---|
| `id` (primary key) | 10 of 10 | ✅ perfect |
| `city` | 4 of 10 | ✅ reasonable |
| A yes/no flag | 2 of millions | ❌ a scan is cheaper |

**Other reasons an index is ignored:**

- a function on the column — `WHERE YEAR(joined_on)=2025` cannot use an index on
  `joined_on`; rewrite as a range `WHERE joined_on >= '2025-01-01' AND ... < '2026-01-01'`
- a leading wildcard — `LIKE '%nair'` cannot use one, `LIKE 'nair%'` can
- a type mismatch between the column and the literal

### 8.5 Isolation levels — the "I" in ACID

```sql
SELECT @@transaction_isolation;
```
```text
+-------------------+
| isolation_level   |
+-------------------+
| REPEATABLE-READ   |
+-------------------+
```

| Level | Dirty read | Non-repeatable read | Phantom read |
|---|---|---|---|
| `READ UNCOMMITTED` | possible | possible | possible |
| `READ COMMITTED` | ❌ | possible | possible |
| **`REPEATABLE READ`** (MySQL default) | ❌ | ❌ | ❌ in InnoDB |
| `SERIALIZABLE` | ❌ | ❌ | ❌ |

| Anomaly | Meaning |
|---|---|
| **Dirty read** | you see another transaction's uncommitted change |
| **Non-repeatable read** | you read the same row twice and get different values |
| **Phantom read** | you run the same query twice and get different **rows** |

📌 **MySQL defaults to `REPEATABLE READ`; PostgreSQL and Oracle default to
`READ COMMITTED`.** That genuinely changes application behaviour, and it is a
favourite senior-interview question.

InnoDB also prevents phantoms at `REPEATABLE READ` using **gap locks** — stricter
than the SQL standard requires, and a common source of surprise deadlocks on
write-heavy tables.

### 8.6 Deadlocks

Two transactions each holding what the other needs. InnoDB detects it, kills the
cheaper one, and that session sees:

```text
ERROR 1213 (40001): Deadlock found when trying to get lock; try restarting transaction
```

```sql
SHOW ENGINE INNODB STATUS;      -- read the LATEST DETECTED DEADLOCK section
```

**Avoiding them:** touch rows in a **consistent order** everywhere, keep
transactions short, and index the columns you filter on — an unindexed `UPDATE`
locks far more rows than you expect.

**Handling them:** retry the transaction. Deadlocks are normal under load, not a
bug to be eliminated entirely.

### 8.7 Materialised views — the thing MySQL lacks

A view re-runs its query every time. When that is expensive, other databases
offer a **materialised view** that stores the result. MySQL has none, so you
build one by hand:

```sql
CREATE TABLE mv_city_stats AS
SELECT city, COUNT(*) AS n, AVG(marks) AS avg_marks
FROM students GROUP BY city;
-- refresh on a schedule with an EVENT (Day 17) or from a trigger
```

📌 PostgreSQL and Oracle have real `CREATE MATERIALIZED VIEW ... REFRESH`.

---

## 8. Practice Questions

1. Create a view `passed_students` showing everyone with marks of 50 or more.
2. Query your view, sorted by marks.
3. Create a view joining students to their course name and fee.
4. Drop a view. Does the underlying data change?
5. Why does a view not make a slow query faster?
6. Create an index on `students(marks)`.
7. Run `EXPLAIN` for `WHERE marks > 80` before and after. What
   changes?
8. Give two reasons **not** to add an index.
9. Which two constraints create an index automatically?
10. Start a transaction, delete all Kochi students, check the count, then
    `ROLLBACK` and check again.
11. Use a `SAVEPOINT` to insert two rows and keep only the first.
12. Explain each letter of ACID in one sentence.
13. What does `SELECT @@autocommit;` return, and why does it matter?
14. Can you `ROLLBACK` after a `COMMIT`? Why not?
