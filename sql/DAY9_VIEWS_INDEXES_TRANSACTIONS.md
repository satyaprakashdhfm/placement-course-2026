# Views, Indexes and Transactions

In this section, we will learn how to save a query as a view, how to make
searching faster with an index, and how to group changes into a transaction that
can be undone.

---

# What Are These Three?

| Object          | What it is                      | Used for                       |
| --------------- | ------------------------------- | ------------------------------ |
| **View**        | A saved `SELECT` statement      | Simplicity, reuse, security    |
| **Index**       | A sorted lookup structure       | **Speed**                      |
| **Transaction** | A group of statements           | Safety — all succeed or all fail |

They are unrelated jobs, so keep them separate in your mind. A view does not make
anything faster. An index does not change results. A transaction protects data.

---

# Table Used in This Section

Run this once before starting.

```sql
CREATE DATABASE IF NOT EXISTS training;
USE training;

DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS courses;

CREATE TABLE courses (
    course_id   INT PRIMARY KEY,
    course_name VARCHAR(50),
    duration    INT,
    fee         INT
);

INSERT INTO courses VALUES
(1,'Python',45,15000),
(2,'SQL',30,10000),
(3,'Java',60,20000),
(4,'DSA',90,25000),
(5,'Cloud',30,18000);

CREATE TABLE students (
    student_id INT PRIMARY KEY,
    name       VARCHAR(50),
    city       VARCHAR(50),
    course_id  INT,
    marks      INT,
    joined_on  DATE
);

INSERT INTO students VALUES
(101,'Rahul Verma','Hyderabad',1,78,'2025-01-15'),
(102,'Anita Sharma','Chennai',2,95,'2025-01-20'),
(103,'Karan Patel','Hyderabad',1,38,'2025-02-01'),
(104,'Priya Nair','Kochi',3,66,'2025-02-10'),
(105,'Vikram Rao','Hyderabad',2,81,'2025-03-05'),
(106,'Sneha Iyer','Chennai',3,54,'2025-03-12'),
(107,'Arjun Mehta','Pune',4,90,'2025-04-02'),
(108,'Divya Menon','Kochi',1,45,'2025-04-18'),
(109,'Rohit Sinha','Pune',NULL,78,'2025-05-01'),
(110,'Meera Nair','Chennai',4,NULL,'2025-05-20');
```

---

# PART 1 — VIEWS

---

# 1. Creating a View

A **view** is a stored `SELECT`. It holds **no data** of its own — it runs its
query every time you use it.

### Syntax

```sql
CREATE VIEW view_name AS
SELECT columns FROM table_name WHERE condition;
```

### Example

```sql
CREATE OR REPLACE VIEW toppers AS
SELECT name, city, marks FROM students WHERE marks >= 75;
```

### Expected Output

```
Query OK, 0 rows affected
```

Nothing was copied. Only the **query** was saved.

---

# 2. Using a View

A view is queried exactly like a table.

### Example

```sql
SELECT * FROM toppers ORDER BY marks DESC;
```

### Expected Output

```
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

You can add `WHERE`, `ORDER BY`, `GROUP BY` — anything you would use on a table.

> **Note:** `CREATE OR REPLACE VIEW` redefines an existing view. Tables do not
> support `OR REPLACE`, but views do.

---

# 3. Why Use Views?

| Reason          | Explanation                                              |
| --------------- | -------------------------------------------------------- |
| **Simplicity**  | Hide a complicated join behind one name                  |
| **Reuse**       | Write the logic once; everybody uses the same definition |
| **Security**    | Give access to the view, not the table — hide salary columns |
| **Consistency** | One official definition of "topper" for the whole team   |

---

# 4. A View Over a Join

This is the most common real use — the complexity is written **once**.

### Example

```sql
CREATE OR REPLACE VIEW student_courses AS
SELECT s.name, s.city, c.course_name, c.fee
FROM students s
LEFT JOIN courses c ON s.course_id = c.course_id;

SELECT * FROM student_courses WHERE fee > 15000;
```

### Expected Output

```
+-------------+---------+-------------+-------+
| name        | city    | course_name | fee   |
+-------------+---------+-------------+-------+
| Priya Nair  | Kochi   | Java        | 20000 |
| Sneha Iyer  | Chennai | Java        | 20000 |
| Arjun Mehta | Pune    | DSA         | 25000 |
| Meera Nair  | Chennai | DSA         | 25000 |
+-------------+---------+-------------+-------+
```

Anyone can now query student–course information without knowing how the join
works.

---

# 5. A View With Aggregates

### Example

```sql
CREATE OR REPLACE VIEW course_summary AS
SELECT c.course_id, c.course_name,
       COUNT(s.student_id)   AS enrolled,
       ROUND(AVG(s.marks),1) AS avg_marks
FROM courses c
LEFT JOIN students s ON s.course_id = c.course_id
GROUP BY c.course_id, c.course_name;

SELECT * FROM course_summary WHERE enrolled > 0 ORDER BY avg_marks DESC;
```

### Expected Output

```
+-----------+-------------+----------+-----------+
| course_id | course_name | enrolled | avg_marks |
+-----------+-------------+----------+-----------+
|         4 | DSA         |        2 |      90.0 |
|         2 | SQL         |        2 |      88.0 |
|         3 | Java        |        2 |      60.0 |
|         1 | Python      |        3 |      53.7 |
+-----------+-------------+----------+-----------+
```

Notice `WHERE enrolled > 0`. You are filtering on a column the **view
calculated**, which you could not do in the original query without `HAVING`.
That is a real reason to build a view.

---

# 6. Listing and Removing Views

### List all views

```sql
SHOW FULL TABLES WHERE Table_type = 'VIEW';
```

### Expected Output

```
+--------------------+------------+
| Tables_in_training | Table_type |
+--------------------+------------+
| course_summary     | VIEW       |
| student_courses    | VIEW       |
| toppers            | VIEW       |
+--------------------+------------+
```

### See a view's definition

```sql
SHOW CREATE VIEW toppers;
```

### Remove a view

```sql
DROP VIEW IF EXISTS toppers;
```

> **Note:** Dropping a view does **not** affect the underlying table. Only the
> saved query is deleted.

---

# 7. Important Facts About Views

* A view is **always current**. Change the table and the view reflects it
  immediately.
* A view does **not** make a query faster — it runs the same query each time.
* A **simple** view in MySQL is **updatable** — an `INSERT` into it really
  inserts into the table.
* A view over a join, `GROUP BY` or `DISTINCT` is **not** updatable.

---

# PART 2 — INDEXES

---

# 8. What Is an Index?

Without an index, finding `city = 'Pune'` means reading **every row**. This is
called a **full table scan**.

An index is a sorted structure, like the index at the back of a textbook.

```text
   No index                     With an index on city
   read row 1  x                Chennai   -> rows 2, 6, 10
   read row 2  x                Hyderabad -> rows 1, 3, 5
   read row 3  x                Kochi     -> rows 4, 8
   ... all 10 rows              Pune      -> rows 7, 9    <- jump straight there
```

---

# 9. Before the Index — EXPLAIN

`EXPLAIN` shows **how** MySQL will run a query, without running it.

### Example

```sql
EXPLAIN SELECT * FROM students WHERE city = 'Pune';
```

### Expected Output

```
+----+----------+------+---------------+------+------+----------+-------------+
| id | table    | type | possible_keys | key  | rows | filtered | Extra       |
+----+----------+------+---------------+------+------+----------+-------------+
|  1 | students | ALL  | NULL          | NULL |   10 |    10.00 | Using where |
+----+----------+------+---------------+------+------+----------+-------------+
```

Read two columns:

* **`type: ALL`** — a full table scan. This is the warning sign.
* **`rows: 10`** — MySQL expects to read all ten rows to find two.

---

# 10. Creating an Index

### Syntax

```sql
CREATE INDEX index_name ON table_name(column_name);
```

### Example

```sql
CREATE INDEX idx_city ON students(city);
```

### Now run EXPLAIN again

```sql
EXPLAIN SELECT * FROM students WHERE city = 'Pune';
```

### Expected Output

```
+----+----------+------+---------------+----------+------+----------+-------+
| id | table    | type | possible_keys | key      | rows | filtered | Extra |
+----+----------+------+---------------+----------+------+----------+-------+
|  1 | students | ref  | idx_city      | idx_city |    2 |   100.00 | NULL  |
+----+----------+------+---------------+----------+------+----------+-------+
```

### The Comparison

| Column | Before        | After            |
| ------ | ------------- | ---------------- |
| `type` | **`ALL`** — full scan | **`ref`** — index lookup |
| `key`  | `NULL` — no index used | `idx_city`      |
| `rows` | 10 — read everything | **2** — read only the matches |

On ten rows this makes no difference you can feel. On ten million rows it is the
difference between instant and unusable.

---

# 11. Reading the type Column

Best to worst:

| `type`    | Meaning                             |
| --------- | ----------------------------------- |
| `const`   | One row via a unique key — perfect  |
| `eq_ref`  | One row per join match — excellent  |
| `ref`     | Index lookup, several rows — good   |
| `range`   | Index range scan — good             |
| `index`   | Full **index** scan — mediocre      |
| `ALL`     | Full **table** scan — the warning sign |

---

# 12. Viewing and Removing Indexes

### List the indexes on a table

```sql
SHOW INDEX FROM students;
```

### Expected Output

```
+----------+------------+----------+--------------+-------------+-------------+
| Table    | Non_unique | Key_name | Seq_in_index | Column_name | Cardinality |
+----------+------------+----------+--------------+-------------+-------------+
| students |          0 | PRIMARY  |            1 | student_id  |          10 |
| students |          1 | idx_city |            1 | city        |           4 |
+----------+------------+----------+--------------+-------------+-------------+
```

Two useful things here:

* `PRIMARY` exists even though you never created it — a **primary key is indexed
  automatically**.
* **`Cardinality`** is the number of distinct values. `student_id` has 10 (every
  value unique), `city` has 4.

### Remove an index

```sql
DROP INDEX idx_city ON students;
```

---

# 13. The Cost of an Index

An index is **not free**.

| Operation                     | Effect                                  |
| ----------------------------- | --------------------------------------- |
| `SELECT`                      | ✅ Much faster                          |
| `INSERT`, `UPDATE`, `DELETE`  | ❌ Slower — the index must be updated too |
| Disk space                    | ❌ More                                 |

### What to index

| Good candidate                       | Bad candidate                        |
| ------------------------------------ | ------------------------------------ |
| A column used in many `WHERE` clauses | A column you never filter on         |
| A **foreign key** used in joins       | A very small table                   |
| A column you often `ORDER BY`         | A column with only 2 values (yes/no) |

> **Most valuable habit:** index every **foreign key**. MySQL indexes primary keys
> for you but **not** the columns that point at them.

---

# 14. When an Index Is Ignored

Even when an index exists, MySQL cannot use it if you hide the column inside a
function.

```sql
WHERE YEAR(joined_on) = 2025                                     -- cannot use an index
WHERE joined_on >= '2025-01-01' AND joined_on < '2026-01-01'     -- can use an index
```

Also:

* `LIKE 'Pune%'` — can use an index.
* `LIKE '%Pune'` — **cannot**, because the start is unknown.

---

# PART 3 — TRANSACTIONS

---

# 15. What Is a Transaction?

A **transaction** groups several statements so that they **all** succeed or
**all** fail.

The classic example is a bank transfer — two updates that must never come apart:

```sql
START TRANSACTION;
    UPDATE accounts SET balance = balance - 1000 WHERE id = 1;
    UPDATE accounts SET balance = balance + 1000 WHERE id = 2;
COMMIT;
```

If the server crashed between the two lines without a transaction, the money
would simply vanish.

| Command                   | Purpose                                |
| ------------------------- | -------------------------------------- |
| `START TRANSACTION;`      | Begin. (`BEGIN;` also works)           |
| `COMMIT;`                 | Make every change permanent            |
| `ROLLBACK;`               | Undo **everything** since the start    |
| `SAVEPOINT name;`         | Place a marker part-way through        |
| `ROLLBACK TO SAVEPOINT name;` | Undo back to that marker only      |

---

# 16. ROLLBACK in Action

### Example

```sql
SELECT COUNT(*) AS before_delete FROM students;
```

```
+---------------+
| before_delete |
+---------------+
|            10 |
+---------------+
```

```sql
START TRANSACTION;
DELETE FROM students WHERE city = 'Pune';
SELECT COUNT(*) AS after_delete FROM students;
```

```
+--------------+
| after_delete |
+--------------+
|            8 |
+--------------+
```

The delete **has** happened — two rows are gone as far as this session is
concerned.

```sql
ROLLBACK;
SELECT COUNT(*) AS after_rollback FROM students;
```

```
+----------------+
| after_rollback |
+----------------+
|             10 |
+----------------+
```

All ten rows are back.

> **Note:** `ROLLBACK` only works **before** `COMMIT`. Once you commit, the change
> is permanent — that is what "commit" means.

---

# 17. SAVEPOINT — Undoing Part of a Transaction

### Example

```sql
START TRANSACTION;

INSERT INTO students VALUES (201,'Test One','Delhi',1,60,'2025-06-01');

SAVEPOINT after_first;

INSERT INTO students VALUES (202,'Test Two','Delhi',1,70,'2025-06-02');

SELECT COUNT(*) AS both_inserted FROM students WHERE city='Delhi';
```

```
+---------------+
| both_inserted |
+---------------+
|             2 |
+---------------+
```

Now undo only the second insert:

```sql
ROLLBACK TO SAVEPOINT after_first;
SELECT name FROM students WHERE city='Delhi';
```

```
+----------+
| name     |
+----------+
| Test One |
+----------+
```

```sql
COMMIT;
```

`Test Two` was removed; `Test One` survived and is now permanent. A savepoint
lets a long process undo one step without throwing away everything.

Clean up:

```sql
DELETE FROM students WHERE city='Delhi';
COMMIT;
```

---

# 18. AUTOCOMMIT

By default MySQL commits **every statement immediately**.

```sql
SELECT @@autocommit AS autocommit_setting;
```

```
+--------------------+
| autocommit_setting |
+--------------------+
|                  1 |
+--------------------+
```

`1` means on. So a plain `DELETE` is committed the moment it runs, and cannot be
rolled back.

`START TRANSACTION` temporarily suspends autocommit until you `COMMIT` or
`ROLLBACK`.

> **This is why students think `ROLLBACK` does not work.** They run `DELETE`, then
> `ROLLBACK`, and nothing happens — because there was no open transaction. You
> must run `START TRANSACTION` **first**.

---

# 19. ACID — The Four Guarantees

| Letter | Name            | Meaning                                             |
| ------ | --------------- | --------------------------------------------------- |
| **A**  | Atomicity       | All or nothing — half a transfer can never happen   |
| **C**  | Consistency     | Rules and constraints are never left broken         |
| **I**  | Isolation       | Concurrent users do not see each other's half-done work |
| **D**  | Durability      | Once committed, a power cut cannot lose it          |

### Checking the isolation level

```sql
SELECT @@transaction_isolation AS isolation_level;
```

```
+-----------------+
| isolation_level |
+-----------------+
| REPEATABLE-READ |
+-----------------+
```

> **Note:** MySQL's default is `REPEATABLE READ`. PostgreSQL and Oracle default
> to `READ COMMITTED`. This is a common interview question.

---

# 20. Views vs Indexes — Do Not Confuse Them

| Point           | View                     | Index                        |
| --------------- | ------------------------ | ---------------------------- |
| It is           | A saved **query**        | A lookup **structure**       |
| Stores data     | ❌ No                    | ✅ Yes (a sorted copy of the key) |
| Purpose         | Simplicity, security     | **Speed**                    |
| Affects writes  | No                       | Yes — slows them             |
| You query it    | ✅ By name               | ❌ Never — MySQL uses it automatically |

---

# Common Errors

## Error 1: Inserting into a View Over a Join

```sql
INSERT INTO student_courses (name, city) VALUES ('Test','Delhi');
```

### Error

```text
ERROR 1471 (HY000): The target table student_courses of the INSERT is not
insertable-into
```

### Reason

`student_courses` is built from a **join**, so MySQL cannot work out which
underlying table a new row belongs to. Views over joins, `GROUP BY` or `DISTINCT`
are read-only.

### Solution

Insert into the real table instead.

```sql
INSERT INTO students (student_id, name, city) VALUES (201,'Test','Delhi');
```

---

## Error 2: Duplicate Index Name

```sql
CREATE INDEX idx_city ON students(city);
CREATE INDEX idx_city ON students(marks);
```

### Error

```text
ERROR 1061 (42000): Duplicate key name 'idx_city'
```

### Solution

Give each index a distinct, descriptive name such as `idx_marks`.

---

## Error 3: ROLLBACK After COMMIT

```sql
START TRANSACTION;
DELETE FROM students WHERE city='Pune';
COMMIT;
ROLLBACK;
```

### Result

No error, and **nothing is undone**. The rows are gone permanently.

### Reason

`COMMIT` ended the transaction. The `ROLLBACK` applies to a new, empty one.

---

## Error 4: Forgetting START TRANSACTION

```sql
DELETE FROM students WHERE city='Pune';
ROLLBACK;
```

### Result

No error, and **nothing is undone** — because autocommit already committed the
delete.

### Solution

```sql
START TRANSACTION;
DELETE FROM students WHERE city='Pune';
ROLLBACK;
```

---

## Error 5: DDL Cannot Be Rolled Back

```sql
START TRANSACTION;
DROP TABLE courses;
ROLLBACK;
```

### Result

The table is **gone**. `ROLLBACK` cannot bring it back.

### Reason

DDL statements such as `CREATE`, `ALTER`, `DROP` and `TRUNCATE` cause an
**implicit commit**. Never mix them into a transaction you might need to undo.

---

# Commands Covered

| Command                          | Purpose                              |
| -------------------------------- | ------------------------------------ |
| `CREATE VIEW ... AS SELECT ...`  | Saves a query as a view              |
| `CREATE OR REPLACE VIEW`         | Redefines an existing view           |
| `SHOW FULL TABLES WHERE ...VIEW` | Lists all views                      |
| `SHOW CREATE VIEW name`          | Shows a view's definition            |
| `DROP VIEW IF EXISTS name`       | Removes a view                       |
| `EXPLAIN SELECT ...`             | Shows how MySQL will run a query     |
| `CREATE INDEX name ON t(col)`    | Creates an index                     |
| `SHOW INDEX FROM t`              | Lists the indexes on a table         |
| `DROP INDEX name ON t`           | Removes an index                     |
| `START TRANSACTION`              | Begins a transaction                 |
| `COMMIT`                         | Makes changes permanent              |
| `ROLLBACK`                       | Undoes everything since the start    |
| `SAVEPOINT name`                 | Places a marker                      |
| `ROLLBACK TO SAVEPOINT name`     | Undoes back to the marker            |

---

# Summary

* A **view** is a stored `SELECT`, always current, and holds no data. Use it for
  simplicity, reuse and security — **not** for speed.
* An **index** turns a full table scan (`type: ALL`) into a lookup (`type: ref`).
  Check with `EXPLAIN`. It speeds reads and **slows writes**.
* Index what you **filter, join or sort** on — especially foreign keys. Do not
  index everything.
* A function around a column stops the index being used.
* A **transaction** makes several statements all-or-nothing:
  `START TRANSACTION` → work → `COMMIT` or `ROLLBACK`.
* **`SAVEPOINT`** lets you undo part of a transaction.
* Autocommit is **on** by default, which is why `ROLLBACK` seems not to work
  unless you started a transaction.
* DDL cannot be rolled back.
* **ACID** = Atomicity, Consistency, Isolation, Durability.

---

# Practice Questions

1. Create a view `passed_students` showing everyone with marks of 50 or more.
2. Query your view, sorted by marks descending.
3. Create a view joining students to their course name and fee.
4. List all the views in the database.
5. Drop a view. Does the table data change?
6. Why does a view not make a slow query faster?
7. Run `EXPLAIN` on `WHERE marks > 80` and note the `type` and `rows`.
8. Create an index on `marks`, run `EXPLAIN` again, and compare.
9. Which column in `SHOW INDEX` tells you how many distinct values there are?
10. Which index exists without you creating it, and why?
11. Give two reasons **not** to add an index.
12. Why can `WHERE YEAR(joined_on) = 2025` not use an index?
13. Start a transaction, delete all Kochi students, check the count, then
    `ROLLBACK` and check again.
14. Use a `SAVEPOINT` to insert two rows and keep only the first.
15. Run a `DELETE` without `START TRANSACTION`, then `ROLLBACK`. Explain what
    happens.
16. Explain each letter of ACID in one sentence.

---

# Class Summary

In this notebook, you learned:

* Creating, using, listing and dropping **views**
* Views over joins and over aggregates, and filtering on a calculated column
* Why a view does not improve performance
* What an **index** is, and how it turns a scan into a lookup
* Using `EXPLAIN` to prove an index is being used
* Reading the `type` and `rows` columns of `EXPLAIN`
* The cost of an index on writes, and what is worth indexing
* When MySQL ignores an index
* **Transactions** with `START TRANSACTION`, `COMMIT` and `ROLLBACK`
* Partial undo using `SAVEPOINT`
* Why autocommit makes `ROLLBACK` appear to do nothing
* That DDL cannot be rolled back
* The four **ACID** guarantees

You are now ready to learn the next topic: **Stored Procedures, Functions and
Triggers**.
