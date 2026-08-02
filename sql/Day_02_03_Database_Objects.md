# Day 2–3 · Database Objects

**Duration:** 2 × 50–60 Minutes  ·  **MySQL 8**

### Learning Outcomes
- Create, change and remove tables with **`CREATE`**, **`ALTER`**, **`DROP`**.
- Know the real difference between **`DELETE`**, **`TRUNCATE`** and **`DROP`**.
- Use every **constraint**: `PRIMARY KEY`, `NOT NULL`, `UNIQUE`, `CHECK`,
  `DEFAULT`, `FOREIGN KEY`, `AUTO_INCREMENT`.
- Choose the right **data type**.

---

## 1. What is a Database Object?

Anything the database stores *as a structure*, not as data:

| Object | Purpose | Day |
|---|---|---|
| **Database** | A container of tables | today |
| **Table** | Holds the rows | today |
| **Constraint** | A rule the data must obey | today |
| **View** | A saved query that looks like a table | 16 |
| **Index** | A lookup structure that makes searching fast | 16 |
| **Trigger / Procedure** | Code stored in the database | 17 |

---

## 2. Data Types

| Category | Type | Use for |
|---|---|---|
| **Whole numbers** | `TINYINT`, `INT`, `BIGINT` | ids, counts, ages |
| **Decimals** | `DECIMAL(10,2)`, `FLOAT`, `DOUBLE` | **money → always `DECIMAL`** |
| **Text** | `CHAR(n)`, `VARCHAR(n)`, `TEXT` | names, addresses |
| **Dates** | `DATE`, `DATETIME`, `TIMESTAMP`, `TIME`, `YEAR` | joined_on, created_at |
| **Other** | `BOOLEAN`, `ENUM('a','b')`, `BLOB` | flags, fixed choices, files |

### CHAR vs VARCHAR

| | `CHAR(10)` | `VARCHAR(10)` |
|---|---|---|
| Storage | always 10 characters, padded | only what you use |
| Best for | fixed length — country codes, `Y`/`N` | **almost everything else** |

### DECIMAL vs FLOAT — money

```sql
CREATE TABLE money_demo (a FLOAT, b DECIMAL(10,2));
INSERT INTO money_demo VALUES (0.1 + 0.2, 0.1 + 0.2);
SELECT a, b, a = 0.3 AS float_equals_point3 FROM money_demo;
```

```text
+------+------+---------------------+
| a    | b    | float_equals_point3 |
+------+------+---------------------+
|  0.3 | 0.30 |                   0 |
+------+------+---------------------+
```

⚠️ Look carefully. The `FLOAT` column **displays** `0.3` — but the comparison
`a = 0.3` returned **0**, meaning false. `FLOAT` is **approximate**: the stored
value is `0.30000001…` and MySQL merely rounds it for display. The `DECIMAL`
column is exact.

**Never store money in `FLOAT`.** A total that looks right on screen and fails
every comparison is the worst kind of bug.

### MySQL is strict about types

```sql
CREATE TABLE t (marks INT);
INSERT INTO t VALUES ('abc');
```
```text
ERROR 1366 (HY000): Incorrect integer value: 'abc' for column 'marks' at row 1
```

**Key Note:** SQLite would have **accepted** this. MySQL and PostgreSQL reject
it. This is one reason code written against SQLite breaks when it moves to a
real server.

---

## 3. CREATE

```sql
CREATE DATABASE IF NOT EXISTS training;
USE training;

CREATE TABLE courses (
    course_id   INT PRIMARY KEY,
    course_name VARCHAR(50) NOT NULL,
    duration    INT,
    fee         INT
);
```

### AUTO_INCREMENT — let MySQL number the rows

```sql
CREATE TABLE enquiries (
    id      INT PRIMARY KEY AUTO_INCREMENT,
    name    VARCHAR(50),
    created DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO enquiries (name) VALUES ('Asha'), ('Bala');
SELECT id, name FROM enquiries;
```

```text
+----+------+
| id | name |
+----+------+
|  1 | Asha |
|  2 | Bala |
+----+------+
```

You never supplied an `id` — MySQL did. `DEFAULT CURRENT_TIMESTAMP` does the
same for the time.

---

## 4. ALTER TABLE

| What you want | MySQL |
|---|---|
| Add a column | `ALTER TABLE students ADD COLUMN email VARCHAR(80);` |
| **Change a type** | `ALTER TABLE students MODIFY COLUMN email VARCHAR(120);` |
| **Rename + retype** | `ALTER TABLE students CHANGE COLUMN email email_id VARCHAR(120);` |
| Rename only | `ALTER TABLE students RENAME COLUMN email_id TO mail;` |
| Remove a column | `ALTER TABLE students DROP COLUMN mail;` |
| Rename the table | `ALTER TABLE students RENAME TO learners;` |
| Add a constraint | `ALTER TABLE students ADD CONSTRAINT chk CHECK (age > 0);` |

**Key Note:** `MODIFY` changes the type only; `CHANGE` changes name **and**
type, so `CHANGE` always needs the type repeated.

📌 **Dialect corner.** SQLite **cannot** change a column's type at all — you
rebuild the table (create → copy → drop → rename). PostgreSQL says
`ALTER TABLE … ALTER COLUMN email TYPE VARCHAR(120)`. Three spellings, one idea.

---

## 5. DROP, DELETE and TRUNCATE

**Know this table — it is asked in almost every interview:**

| | `DELETE` | `TRUNCATE` | `DROP` |
|---|---|---|---|
| Removes | rows | **all** rows | rows **and the table** |
| `WHERE` allowed | ✅ | ❌ | ❌ |
| Family | DML | DDL | DDL |
| Speed | slower (row by row, logged) | **fast** (recreates the table) | fast |
| Resets `AUTO_INCREMENT` | ❌ | ✅ | n/a |
| Fires triggers | ✅ | ❌ | ❌ |
| Can be rolled back | ✅ | ❌ | ❌ |
| Table still exists | ✅ | ✅ | ❌ |

```sql
DELETE FROM students WHERE marks < 40;   -- some rows
TRUNCATE TABLE students;                 -- all rows, instantly
DROP TABLE students;                     -- table stops existing
```

### AUTO_INCREMENT proves the difference

```sql
INSERT INTO enquiries (name) VALUES ('Chandra');
DELETE FROM enquiries;
INSERT INTO enquiries (name) VALUES ('After DELETE');
SELECT id, name FROM enquiries;
```
```text
+----+--------------+
| id | name         |
+----+--------------+
|  4 | After DELETE |
+----+--------------+
```

```sql
TRUNCATE TABLE enquiries;
INSERT INTO enquiries (name) VALUES ('After TRUNCATE');
SELECT id, name FROM enquiries;
```
```text
+----+----------------+
| id | name           |
+----+----------------+
|  1 | After TRUNCATE |
+----+----------------+
```

After `DELETE` the counter carried on at **4**. After `TRUNCATE` it restarted at
**1**. That is the clearest demonstration of the difference.

📌 **Dialect corner.** SQLite has **no `TRUNCATE` at all** — you write
`DELETE FROM t;`. PostgreSQL has `TRUNCATE`, and unlike MySQL it **can** be
rolled back inside a transaction.

---

## 6. Constraints

A **constraint** is a rule the database enforces, so bad data is rejected no
matter which program writes it.

| Constraint | Meaning |
|---|---|
| `PRIMARY KEY` | Unique **and** not null. One per table |
| `NOT NULL` | Must have a value |
| `UNIQUE` | No duplicates, but `NULL` allowed |
| `CHECK` | Your own condition must be true |
| `DEFAULT` | Value used when none is given |
| `FOREIGN KEY` | Must match a row in another table |
| `AUTO_INCREMENT` | MySQL supplies the next number |

```sql
CREATE TABLE enrolments (
    id        INT PRIMARY KEY AUTO_INCREMENT,
    email     VARCHAR(80) UNIQUE,
    name      VARCHAR(50) NOT NULL,
    marks     INT CHECK (marks BETWEEN 0 AND 100),
    status    VARCHAR(10) DEFAULT 'active',
    course_id INT,
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);
```

### The real error messages

```sql
INSERT INTO students (id, name) VALUES (200, NULL);
```
```text
ERROR 1048 (23000): Column 'name' cannot be null
```

```sql
INSERT INTO students (id, name) VALUES (101, 'Duplicate');
```
```text
ERROR 1062 (23000): Duplicate entry '101' for key 'students.PRIMARY'
```

```sql
INSERT INTO enrolments (name, marks) VALUES ('X', 150);
```
```text
ERROR 3819 (HY000): Check constraint 'enrolments_chk_1' is violated.
```

```sql
INSERT INTO students (id, name, course_id) VALUES (201, 'X', 99);
```
```text
ERROR 1452 (23000): Cannot add or update a child row: a foreign key constraint fails
```

📌 **Dialect corner.** `CHECK` is only **enforced** in MySQL **8.0.16+**. Older
MySQL *parsed and silently ignored* it — a nasty trap on legacy servers. SQLite
and PostgreSQL have always enforced it.

📌 **Dialect corner.** MySQL and PostgreSQL enforce foreign keys by default.
**SQLite does not** — it needs `PRAGMA foreign_keys = ON`.

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

### ON DELETE / ON UPDATE

What should happen to the students when a course is deleted?

```sql
FOREIGN KEY (course_id) REFERENCES courses(course_id)
    ON DELETE SET NULL
    ON UPDATE CASCADE
```

| Option | Effect |
|---|---|
| `RESTRICT` / `NO ACTION` | Block the delete (**default**) |
| `CASCADE` | Delete the students too |
| `SET NULL` | Keep the students, empty their `course_id` |

---

## 8. Composite Keys

```sql
CREATE TABLE attendance (
    student_id INT,
    class_date DATE,
    present    BOOLEAN,
    PRIMARY KEY (student_id, class_date)
);
```

One student can appear many times, one date can appear many times, but the
**pair** appears only once.

---

## 9. Inspecting What You Built

| Command | Shows |
|---|---|
| `SHOW DATABASES;` | every database |
| `SHOW TABLES;` | tables in the current database |
| `DESCRIBE students;` | columns, types, keys |
| `SHOW CREATE TABLE students;` | the exact `CREATE` statement |
| `SHOW INDEX FROM students;` | its indexes |

📌 **Dialect corner.** SQLite: `.tables` and `PRAGMA table_info(t)`.
PostgreSQL: `\dt` and `\d students`.

---

## 10. Common Mistakes

**1. `FLOAT` for money** — `0.1 + 0.2 != 0.3`. Use `DECIMAL`.

**2. Expecting `TRUNCATE` to be undoable** — it cannot be rolled back in MySQL.

**3. `DROP` when you meant `DELETE`** — the table is gone.

**4. Assuming `CHECK` works on old MySQL** — silently ignored before 8.0.16.

**5. Forgetting `VARCHAR` needs a length** — `VARCHAR` alone is an error.

**6. Two `PRIMARY KEY` columns declared separately** — use one composite
`PRIMARY KEY (a, b)`.

---

## 11. Summary

- **DDL** builds structure: `CREATE`, `ALTER`, `DROP`, `TRUNCATE`.
- Types: `INT`, `DECIMAL` (**money**), `VARCHAR`, `DATE`/`DATETIME`, `BOOLEAN`.
  MySQL **rejects** wrong types; SQLite does not.
- `ALTER … MODIFY` changes a type, `CHANGE` renames and retypes.
- `DELETE` (rows, undoable) · `TRUNCATE` (all rows, fast, resets
  `AUTO_INCREMENT`) · `DROP` (the table itself).
- **Constraints** reject bad data: `PRIMARY KEY`, `NOT NULL`, `UNIQUE`,
  `CHECK`, `DEFAULT`, `FOREIGN KEY`.
- Foreign keys support `ON DELETE CASCADE` / `SET NULL`.

---

## 12. Practice Questions

1. Create a `teachers` table with `teacher_id` auto-incrementing, `name`
   required, `email` unique, and `salary` with a `CHECK` above 0.
2. Insert two teachers without giving an id. What ids do they get?
3. Add a `phone` column, change it to `VARCHAR(15)`, then rename it to `mobile`.
4. What is the difference between `MODIFY` and `CHANGE`?
5. Give four differences between `DELETE` and `TRUNCATE`.
6. Show with `AUTO_INCREMENT` that `TRUNCATE` resets the counter.
7. Why must money never be stored in a `FLOAT`?
8. Create a table where the primary key is two columns.
9. Try to insert `'abc'` into an `INT`. What is the error? What would SQLite do?
10. Add a foreign key with `ON DELETE SET NULL` and test it.
11. Which constraint stops two students sharing an e-mail?
12. Run `SHOW CREATE TABLE students;` and read it line by line.
13. Name the SQLite and PostgreSQL equivalents of `DESCRIBE`.
