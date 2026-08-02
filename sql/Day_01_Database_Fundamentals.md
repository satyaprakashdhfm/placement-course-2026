# Day 1 · Database Fundamentals

**Duration:** 50–60 Minutes  ·  **Tool:** MySQL 8 + MySQL Workbench

### Learning Outcomes
- Understand what a **database** is and why files and Excel are not enough.
- Tell the difference between **DBMS** and **RDBMS**.
- Understand **tables, rows, columns, keys**.
- Know what **SQL** is and its five command families.
- Follow the **SQL execution flow** — what happens when you press Run.
- Know how **MySQL**, **SQLite** and **PostgreSQL** relate to each other.
- Install **MySQL** and run your first query.

---

## 1. Data, Information and Database

| Term | Meaning | Example |
|---|---|---|
| **Data** | Raw facts, no meaning on their own | `101`, `Rahul`, `78` |
| **Information** | Data with meaning | Student 101, Rahul, scored 78 |
| **Database** | An organised collection of data you can store and retrieve | The whole student table |

A **database** stores data in a structured way so it can be found, updated and
protected — reliably, and by many people at once.

---

## 2. Why Not Just Use Files or Excel?

Imagine storing 50,000 student records in `students.txt` or an Excel sheet:

| Problem | What goes wrong |
|---|---|
| **Searching** | You must read the whole file to find one student |
| **Duplication** | The same student typed twice, in two files |
| **No validation** | Nothing stops marks of `500` or a name in the marks column |
| **No relationships** | You cannot easily link a student to their course |
| **Multi-user** | Two people editing at once overwrite each other |
| **Security** | Anyone who opens the file sees everything |
| **Crash safety** | Power cut in the middle of saving = corrupted file |

A **database** solves all of these. That is why every real application uses one.

---

## 3. DBMS and RDBMS

**DBMS** (Database Management System) is the *software* that manages the
database. You never touch the files yourself — you ask the DBMS.

```text
    You  ──SQL──►  DBMS  ──►  Database files on disk
         ◄─result──
```

**RDBMS** (**Relational** DBMS) is a DBMS that stores data in **tables** that
can be **related** to each other. This is the model that won.

| | DBMS | RDBMS |
|---|---|---|
| Stores data as | Files, or a single structure | **Tables** (rows & columns) |
| Relationships | Not supported | Supported, with **keys** |
| Redundancy | High | Low (normalisation) |
| Language | Varies | **SQL** |
| Examples | Older file systems | **MySQL**, PostgreSQL, SQLite, Oracle, SQL Server |

---

## 4. How a Table is Built

A **table** holds one kind of thing. Students in one table, courses in another.

```text
                 columns (fields)
              ┌──────┬─────────────┬───────┐
              │ id   │ name        │ marks │
              ├──────┼─────────────┼───────┤
   rows       │ 101  │ Rahul Verma │  78   │   <- one row = one record
 (records)    │ 102  │ Anita Sharma│  95   │
              │ 103  │ Karan Patel │  38   │
              └──────┴─────────────┴───────┘
```

| Term | Meaning |
|---|---|
| **Table** | A collection of related data (also called a *relation*) |
| **Row** | One record — one student |
| **Column** | One attribute — the name, the marks |
| **Field** | One cell — where a row and column meet |

### Keys

| Key | Meaning |
|---|---|
| **Primary key** | Uniquely identifies each row. Never repeats, never empty |
| **Foreign key** | A column that points to the primary key of another table |
| **Composite key** | A primary key made of two or more columns together |
| **Unique key** | Must be unique, but *can* be empty, and there can be many |

**Key Note:** the primary key is what makes a row findable. Choose something
that never changes — a roll number, not a phone number.

---

## 5. What is SQL?

**SQL** = **S**tructured **Q**uery **L**anguage — the standard language for
talking to a relational database.

It is **declarative**: you say **what** you want, not **how** to get it.

```sql
SELECT name FROM students WHERE marks > 50;
```

You never tell the database how to search. It works that out itself.

**Key Notes:**
- SQL keywords are **not case sensitive** (`SELECT` = `select`), but writing
  keywords in CAPITALS is the normal style.
- Every statement ends with a **semicolon** `;`.
- SQL is a **standard** (ANSI SQL). Every database supports the core of it, and
  then adds its own extras.

---

## 6. The Five Families of SQL Commands

| Family | Full name | Commands | Purpose |
|---|---|---|---|
| **DDL** | Data **Definition** Language | `CREATE`, `ALTER`, `DROP`, `TRUNCATE` | Build and change the *structure* |
| **DML** | Data **Manipulation** Language | `INSERT`, `UPDATE`, `DELETE` | Change the *data* |
| **DQL** | Data **Query** Language | `SELECT` | Read the data |
| **TCL** | **Transaction** Control Language | `COMMIT`, `ROLLBACK`, `SAVEPOINT` | Confirm or undo a batch of changes |
| **DCL** | Data **Control** Language | `GRANT`, `REVOKE` | Permissions |

Remember it as: **DDL builds the box, DML fills the box, DQL reads the box.**

---

## 7. SQL Execution Flow

When you press **Execute**, the database does five things:

```text
   Your SQL
      │
      ▼
  1. PARSER        is the syntax correct? do these tables exist?
      │
      ▼
  2. OPTIMISER     what is the FASTEST way to get this? use an index?
      │
      ▼
  3. EXECUTION     the chosen plan is turned into steps
     PLAN
      │
      ▼
  4. ENGINE        the steps run, rows are read from disk
      │
      ▼
  5. RESULT        rows come back to you
```

**Key Note:** the **optimiser** is why SQL is declarative. Two people can write
the same question differently and the database may run both the same way.

### The order SQL is *actually* run

This surprises everybody. You **write** a query in one order and the database
**runs** it in another:

| Written order | Run order |
|---|---|
| `SELECT` | 5 |
| `FROM` | **1** |
| `WHERE` | 2 |
| `GROUP BY` | 3 |
| `HAVING` | 4 |
| `ORDER BY` | 6 |
| `LIMIT` | 7 |

`FROM` runs **first** — the database must fetch the table before it can filter
it. `SELECT` runs almost **last**. This explains a rule you will meet on Day 4:
you cannot use a `SELECT` alias inside `WHERE`, because `WHERE` ran first.

---

## 8. MySQL, SQLite, PostgreSQL — The Same Language

> **SQL is the language. MySQL is a program that speaks it.**

```text
                    SQL  (the language, a standard)
                     │
      ┌──────────┬───┴────┬───────────┬──────────┐
   MySQL     SQLite   PostgreSQL   Oracle    SQL Server
      └──────────┴────────┴───────────┴──────────┘
              all speak SQL, with small accents
```

Compare it to English: British and American English are the **same language**
with small spelling differences.

| | **MySQL** | **SQLite** | **PostgreSQL** |
|---|---|---|---|
| Type | Client–**server** | **Serverless**, one file | Client–**server** |
| Setup | Install server, set password | Just a file | Install server, create role |
| Port | 3306 | none | 5432 |
| Used for | **Most web applications** | Phones, browsers, tests | Analytics, complex data |
| Typing | strict | flexible | strictest |

**We teach MySQL because it is the one you are most likely to meet at work.**

Around **90% of what you learn transfers directly** — `SELECT`, `WHERE`,
`JOIN`, `GROUP BY`, `HAVING`, subqueries and window functions are identical.
The differences are in the edges: function names, and a few features.

Three you will meet immediately:

| Job | MySQL | SQLite / PostgreSQL |
|---|---|---|
| Join two strings | `CONCAT(a, b)` | `a \|\| b` |
| Today's date | `CURDATE()` | `DATE('now')` / `CURRENT_DATE` |
| Year from a date | `YEAR(d)` | `STRFTIME('%Y',d)` / `EXTRACT(...)` |

📖 **The full comparison is in [DIALECTS.md](DIALECTS.md).** Read it once now,
and again before an interview.

---

## 9. Installing MySQL

**Step 1.** Download the **MySQL Installer for Windows** from:

```text
https://dev.mysql.com/downloads/installer/
```

Choose the larger *(mysql-installer-community)* file so you do not need
internet during setup.

**Step 2.** Run it and choose the **Developer Default** setup type. That
installs:

- **MySQL Server** — the database itself
- **MySQL Workbench** — the graphical tool you will use in class
- MySQL Shell and connectors

**Step 3.** Keep clicking **Next**, and at **Type and Networking** leave the
port as **3306**.

**Step 4.** At **Accounts and Roles**, set a **root password**.

> ⚠️ **Write this password down.** There is no easy recovery, and you will need
> it every time you connect. For class, something simple like `root` is fine —
> never do that on a real server.

**Step 5.** Leave **Configure MySQL Server as a Windows Service** ticked, so
the database starts with your computer.

**Step 6.** Finish, then open **MySQL Workbench**. You will see a connection
tile called **Local instance MySQL80**. Click it and enter your root password.

You are connected.

### If the installer is a problem

Two lighter alternatives, both fine for this course:

| Option | Notes |
|---|---|
| **XAMPP** | Includes MySQL (MariaDB) + phpMyAdmin. Very quick to install |
| **Docker** | `docker run -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root mysql:8` |

---

## 10. The Workbench Window

| Area | What it is for |
|---|---|
| **Navigator (left)** | Your databases, tables, views, procedures |
| **Query tab (middle)** | Where you type SQL |
| **Result grid (bottom)** | The rows that come back |
| **Output panel** | Success / error messages and timings |

To run SQL: type it, then press **Ctrl + Enter** (current statement) or
**Ctrl + Shift + Enter** (the whole tab).

**Key Notes:**
- Unlike a file-based tool, **MySQL saves as you go** — there is no
  "write changes" button. An `INSERT` that succeeds is stored.
- The one exception is when you open a **transaction** yourself — see Day 16.
- ⚠️ Workbench has a **safe update mode** on by default: it refuses `UPDATE` or
  `DELETE` without a `WHERE` on a key column. If you hit *"Error 1175"*, that is
  why. Turn it off with:
  ```sql
  SET SQL_SAFE_UPDATES = 0;
  ```

---

## 11. Databases Inside the Server

Unlike a single file, one MySQL server holds **many databases**. So you must
say which one you mean:

```sql
CREATE DATABASE training;
USE training;
SHOW DATABASES;
SHOW TABLES;
```

`USE training;` sets the current database for the rest of your session. Forget
it and you get *"No database selected"*.

---

## 12. Your First SQL

Run these one at a time in Workbench.

**Create a table (DDL):**

```sql
CREATE DATABASE IF NOT EXISTS training;
USE training;

CREATE TABLE students (
    id     INT PRIMARY KEY,
    name   VARCHAR(50) NOT NULL,
    marks  INT
);
```

**Put data in (DML):**

```sql
INSERT INTO students (id, name, marks) VALUES
    (101, 'Rahul Verma',  78),
    (102, 'Anita Sharma', 95),
    (103, 'Karan Patel',  38);
```

**Read it back (DQL):**

```sql
SELECT * FROM students;
```

```text
+-----+--------------+-------+
| id  | name         | marks |
+-----+--------------+-------+
| 101 | Rahul Verma  |    78 |
| 102 | Anita Sharma |    95 |
| 103 | Karan Patel  |    38 |
+-----+--------------+-------+
```

**Ask a real question:**

```sql
SELECT name, marks
FROM students
WHERE marks > 50
ORDER BY marks DESC;
```

```text
+--------------+-------+
| name         | marks |
+--------------+-------+
| Anita Sharma |    95 |
| Rahul Verma  |    78 |
+--------------+-------+
```

**See what a table looks like:**

```sql
DESCRIBE students;
```

```text
+-------+-------------+------+-----+---------+-------+
| Field | Type        | Null | Key | Default | Extra |
+-------+-------------+------+-----+---------+-------+
| id    | int         | NO   | PRI | NULL    |       |
| name  | varchar(50) | NO   |     | NULL    |       |
| marks | int         | YES  |     | NULL    |       |
+-------+-------------+------+-----+---------+-------+
```

---

## 13. Common Mistakes

**1. Forgetting `USE training;`** — *"No database selected"*.

**2. Forgetting the semicolon** — Workbench waits for you to finish the
statement.

**3. Using `||` to join strings** — in MySQL that means **OR** and quietly
returns `0`. Use `CONCAT(a, b)`.

**4. Using double quotes for text** — SQL text uses **single quotes**:
`'Rahul'`. (MySQL tolerates `"Rahul"`, but PostgreSQL will not — build the
right habit.)

**5. `=` vs `==`** — SQL comparison is a **single** `=`.

**6. Error 1175 on `UPDATE`/`DELETE`** — Workbench safe update mode. Add a
`WHERE`, or `SET SQL_SAFE_UPDATES = 0;`.

**7. Losing the root password** — there is no easy way back.

---

## 14. Summary

- A **database** solves searching, duplication, validation, relationships,
  multi-user access and crash safety — things files and Excel cannot.
- A **DBMS** manages the database; an **RDBMS** stores it as **related tables**.
- Data lives in **tables** of **rows** and **columns**, identified by a
  **primary key** and linked with a **foreign key**.
- **SQL** is the declarative standard language, in five families:
  **DDL, DML, DQL, TCL, DCL**.
- A query is **parsed → optimised → planned → executed**, and it runs
  **`FROM` first, `SELECT` almost last**.
- **SQL is the language; MySQL is one engine.** ~90% transfers to PostgreSQL,
  SQLite and Oracle — see [DIALECTS.md](DIALECTS.md).
- MySQL is a **server**: many databases inside it, so always `USE` one.

---

## 15. Practice Questions

1. Give three problems with storing 50,000 records in Excel that a database solves.
2. What is the difference between a DBMS and an RDBMS?
3. What is the difference between a primary key and a unique key?
4. Which family does each belong to — `CREATE`, `INSERT`, `SELECT`, `ROLLBACK`?
5. Why can a `SELECT` alias not be used inside `WHERE`? (Think about run order.)
6. In one sentence each: what is SQL, and what is MySQL?
7. Name two differences between MySQL and SQLite.
8. Why does `SELECT 'a' || 'b';` return `0` in MySQL?
9. Install MySQL and connect with Workbench.
10. Create a database `training` and select it.
11. Create a `courses` table with `course_id`, `course_name` and `duration`.
12. Insert three courses, then select those longer than 30 days.
13. Run `DESCRIBE courses;` and explain each column of the output.
14. Insert a student with a duplicate `id` and read the error carefully.
