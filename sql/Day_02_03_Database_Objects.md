# Day 2–3 · Database Objects

**Duration:** 2 × 50–60 Minutes  ·  **Tool:** DB Browser for SQLite

### Learning Outcomes
- Create, change and remove tables with **`CREATE`**, **`ALTER`**, **`DROP`**.
- Know why **`TRUNCATE`** does not exist in SQLite and what to use instead.
- Use every **constraint**: `PRIMARY KEY`, `NOT NULL`, `UNIQUE`, `CHECK`,
  `DEFAULT`, `FOREIGN KEY`.
- Choose the right **data type**, and understand SQLite's flexible typing.

---

## 1. What is a Database Object?

Anything the database stores *as a structure*, not as data:

| Object | Purpose | Day |
|---|---|---|
| **Table** | Holds the rows | today |
| **Constraint** | A rule the data must obey | today |
| **View** | A saved query that looks like a table | 16 |
| **Index** | A lookup structure that makes searching fast | 16 |
| **Trigger** | Code that runs automatically on a change | 17 |

All of these are built with **DDL** — `CREATE`, `ALTER`, `DROP`.

---

## 2. Data Types

Every column has a type. SQLite has only **five storage classes**:

| SQLite type | Holds | Write it as |
|---|---|---|
| `INTEGER` | Whole numbers | `INTEGER`, `INT` |
| `REAL` | Decimal numbers | `REAL`, `FLOAT`, `DOUBLE` |
| `TEXT` | Strings | `TEXT`, `VARCHAR(50)`, `CHAR(10)` |
| `BLOB` | Raw bytes (images, files) | `BLOB` |
| `NULL` | No value at all | — |

SQLite **accepts** the type names from other databases (`VARCHAR(50)`,
`DATETIME`, `NUMBER`) and maps them onto these five. So you can write
MySQL-style SQL and it still works.

### There is no DATE type

SQLite stores dates as **`TEXT`** in the format `'YYYY-MM-DD'`. That format
sorts correctly as text, which is why it is the one to use. Date functions
come on Day 9.

### ⚠️ SQLite's flexible typing

Other databases **reject** wrong types. SQLite usually does not:

```sql
CREATE TABLE demo (marks INTEGER);
INSERT INTO demo VALUES ('abc');          -- no error in SQLite!
SELECT marks, TYPEOF(marks) FROM demo;
```

```text
marks | TYPEOF(marks)
------+--------------
abc   | text
```

**Key Note:** MySQL and Oracle would refuse this. Never rely on SQLite to catch
type errors — use a `CHECK` constraint (§6) if the value really matters.

---

## 3. CREATE TABLE

```sql
CREATE TABLE courses (
    course_id   INTEGER PRIMARY KEY,
    course_name TEXT    NOT NULL,
    duration    INTEGER,
    fee         INTEGER
);
```

Read it as: *table name, then one line per column: name, type, rules.*

**Safe version** — does nothing if the table is already there:

```sql
CREATE TABLE IF NOT EXISTS courses ( ... );
```

---

## 4. ALTER TABLE

Changes the **structure** of an existing table.

| What you want | SQLite | Works? |
|---|---|---|
| Add a column | `ALTER TABLE students ADD COLUMN email TEXT;` | ✅ |
| Rename a column | `ALTER TABLE students RENAME COLUMN email TO email_id;` | ✅ |
| Remove a column | `ALTER TABLE students DROP COLUMN email_id;` | ✅ (3.35+) |
| Rename the table | `ALTER TABLE students RENAME TO learners;` | ✅ |
| **Change a column's type** | `ALTER TABLE students ALTER COLUMN age TEXT;` | ❌ **not supported** |
| **Add a constraint later** | | ❌ **not supported** |

```sql
ALTER TABLE students ADD COLUMN email TEXT;
```

### Working around the missing ALTER COLUMN

MySQL/Oracle can change a column's type in place. In SQLite you rebuild:

```sql
CREATE TABLE students_new (id INTEGER PRIMARY KEY, name TEXT, age TEXT);
INSERT INTO students_new SELECT id, name, age FROM students;
DROP TABLE students;
ALTER TABLE students_new RENAME TO students;
```

**Key Note:** *create → copy → drop → rename.* Learn this pattern — it is the
standard SQLite answer, and a common interview question.

---

## 5. DROP, DELETE and TRUNCATE

Three ways to remove things — **know the difference, it is asked constantly**:

| Command | Removes | Structure survives? | Family |
|---|---|---|---|
| `DELETE FROM t;` | Rows (can use `WHERE`) | ✅ Yes | DML |
| `TRUNCATE TABLE t;` | **All** rows, fast, no `WHERE` | ✅ Yes | DDL |
| `DROP TABLE t;` | Rows **and** the table itself | ❌ Gone | DDL |

```sql
DELETE FROM students WHERE marks < 40;   -- some rows
DELETE FROM students;                    -- all rows, table stays
DROP TABLE students;                     -- table stops existing
```

### ⚠️ TRUNCATE does not exist in SQLite

```sql
TRUNCATE TABLE students;
```

```text
Error: near "TRUNCATE": syntax error
```

Use `DELETE FROM students;` instead — SQLite optimises a `WHERE`-less delete
internally, so it is just as fast.

**For interviews, know the real difference in MySQL/Oracle:**

| | `DELETE` | `TRUNCATE` |
|---|---|---|
| `WHERE` allowed | ✅ | ❌ |
| Speed | Slower (row by row, logged) | Faster (deallocates pages) |
| Can be rolled back | ✅ | ❌ in MySQL/Oracle |
| Resets AUTO_INCREMENT | ❌ | ✅ |
| Fires triggers | ✅ | ❌ |

---

## 6. Constraints

A **constraint** is a rule the database enforces. Bad data is rejected before
it is ever stored — the database protects itself, no matter which program
writes to it.

| Constraint | Meaning |
|---|---|
| `PRIMARY KEY` | Unique **and** not null. One per table |
| `NOT NULL` | Must have a value |
| `UNIQUE` | No duplicates, but `NULL` allowed |
| `CHECK` | Your own condition must be true |
| `DEFAULT` | Value used when none is given |
| `FOREIGN KEY` | Must match a row in another table |

```sql
CREATE TABLE enrolments (
    id        INTEGER PRIMARY KEY,
    email     TEXT    UNIQUE,
    name      TEXT    NOT NULL,
    marks     INTEGER CHECK (marks BETWEEN 0 AND 100),
    status    TEXT    DEFAULT 'active',
    course_id INTEGER REFERENCES courses(course_id)
);
```

### What each one does when broken

Every message below is the **real** SQLite error:

```sql
INSERT INTO students (id, name) VALUES (200, NULL);
```
```text
NOT NULL constraint failed: students.name
```

```sql
INSERT INTO students (id, name) VALUES (101, 'Duplicate');
```
```text
UNIQUE constraint failed: students.id
```

```sql
INSERT INTO enrolments (id, marks) VALUES (1, 150);
```
```text
CHECK constraint failed: marks BETWEEN 0 AND 100
```

```sql
INSERT INTO students (id, name, course_id) VALUES (201, 'X', 99);
```
```text
FOREIGN KEY constraint failed
```

---

## 7. Primary Key vs Unique vs Foreign Key

| | `PRIMARY KEY` | `UNIQUE` | `FOREIGN KEY` |
|---|---|---|---|
| Duplicates | ❌ | ❌ | ✅ allowed |
| `NULL` allowed | ❌ | ✅ | ✅ |
| How many per table | **1** | many | many |
| Purpose | Identify the row | Stop repeats | Link to another table |

```text
      courses                       students
   ┌────────────┐                ┌─────────────┐
   │ course_id  │◄───────────────│ course_id   │   FOREIGN KEY
   │ (PRIMARY)  │                │ (FOREIGN)   │
   └────────────┘                └─────────────┘
```

A foreign key gives **referential integrity**: you cannot enrol a student in
course 99 if course 99 does not exist.

> ⚠️ **SQLite turns foreign keys OFF by default.** They are only checked if you
> switch them on:
> ```sql
> PRAGMA foreign_keys = ON;
> ```
> In DB Browser: **Edit Pragmas** tab → tick **Foreign Keys** → Save.
> Do this now, or your `FOREIGN KEY` rules will silently do nothing.

---

## 8. Composite Keys

When one column is not enough to identify a row, use two:

```sql
CREATE TABLE attendance (
    student_id INTEGER,
    class_date TEXT,
    present    INTEGER,
    PRIMARY KEY (student_id, class_date)
);
```

One student can appear many times, one date can appear many times, but the
**pair** appears only once.

---

## 9. Common Mistakes

**1. Expecting `TRUNCATE` to work** — it does not exist in SQLite. Use `DELETE FROM`.

**2. Forgetting `PRAGMA foreign_keys = ON`** — your foreign keys are decoration
until you enable them.

**3. `DROP` instead of `DELETE`** — `DROP` destroys the table. There is no undo
once changes are written.

**4. Two `PRIMARY KEY` columns written separately** — that is an error. For two
columns use one composite `PRIMARY KEY (a, b)`.

**5. Trusting SQLite's types** — `'abc'` fits happily in an `INTEGER` column.

**6. `NOT NULL` with no `DEFAULT`** — every future `INSERT` must supply it.

---

## 10. Summary

- **DDL** builds structure: `CREATE`, `ALTER`, `DROP`.
- SQLite has **5 storage classes** and accepts other databases' type names.
  Dates are `TEXT` in `'YYYY-MM-DD'`.
- `ALTER` in SQLite can add, drop and rename columns — but **not change a type**.
  Work around it with **create → copy → drop → rename**.
- `DELETE` removes rows · `TRUNCATE` removes all rows (**not in SQLite**) ·
  `DROP` removes the table.
- **Constraints** make the database reject bad data: `PRIMARY KEY`, `NOT NULL`,
  `UNIQUE`, `CHECK`, `DEFAULT`, `FOREIGN KEY`.
- Foreign keys need **`PRAGMA foreign_keys = ON`** in SQLite.

---

## 11. Practice Questions

1. Create a `teachers` table with `teacher_id`, `name` (required), `email`
   (unique) and `salary` with a `CHECK` that it is above 0.
2. Add a `phone` column to `teachers`, then rename it to `mobile`.
3. What is the difference between `DELETE`, `TRUNCATE` and `DROP`?
4. Why does `TRUNCATE` fail in SQLite, and what do you use instead?
5. Write the four statements that change a column's type in SQLite.
6. Give one difference between a primary key and a unique key.
7. Create a table where the primary key is two columns together.
8. Turn foreign keys on, then try to insert a student with `course_id = 99`.
   What is the exact error?
9. Insert `'hello'` into an `INTEGER` column. Why does SQLite allow it?
10. Which constraint would stop two students sharing an e-mail address?
