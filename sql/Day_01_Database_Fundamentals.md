# Day 1 · Database Fundamentals

**Duration:** 50–60 Minutes  ·  **Tool:** DB Browser for SQLite

### Learning Outcomes
- Understand what a **database** is and why files and Excel are not enough.
- Tell the difference between **DBMS** and **RDBMS**.
- Understand **tables, rows, columns, keys**.
- Know what **SQL** is and its five command families.
- Follow the **SQL execution flow** — what happens when you press Run.
- Know the difference between **SQL** and **SQLite**, and why learning SQLite
  teaches you SQL everywhere.
- Install **DB Browser for SQLite** and create your first database.

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
| Examples | Older file systems | **SQLite**, MySQL, PostgreSQL, Oracle, SQL Server |

**Key Note:** every database you will use in this course is an **RDBMS**.

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
| **Primary key** | Uniquely identifies each row. Never repeats, never empty. `id` |
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
- SQL is a **standard** (ANSI SQL). Every database supports the core of it,
  and then adds its own extras.

---

## 6. The Five Families of SQL Commands

| Family | Full name | Commands | Purpose |
|---|---|---|---|
| **DDL** | Data **Definition** Language | `CREATE`, `ALTER`, `DROP` | Build and change the *structure* |
| **DML** | Data **Manipulation** Language | `INSERT`, `UPDATE`, `DELETE` | Change the *data* |
| **DQL** | Data **Query** Language | `SELECT` | Read the data |
| **TCL** | **Transaction** Control Language | `COMMIT`, `ROLLBACK`, `SAVEPOINT` | Confirm or undo a batch of changes |
| **DCL** | Data **Control** Language | `GRANT`, `REVOKE` | Permissions (not in SQLite — see §9) |

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
it. `SELECT` runs almost **last**. This explains a rule you will meet on Day 11:
you cannot use a `SELECT` alias inside `WHERE`, because `WHERE` ran first.

---

## 8. SQL vs SQLite — What is the Difference?

This confuses everyone at the start, so be clear:

> **SQL is the language. SQLite is a program that speaks it.**

```text
                    SQL  (the language, a standard)
                     │
      ┌──────────┬───┴────┬───────────┬──────────┐
   SQLite     MySQL   PostgreSQL   Oracle    SQL Server
      └──────────┴────────┴───────────┴──────────┘
              all speak SQL, with small accents
```

Compare it to English: British and American English are the **same language**
with small spelling differences. SQLite and Oracle are the same for the
**things you are learning**.

| | SQLite | MySQL / Oracle / SQL Server |
|---|---|---|
| Type | **Serverless** — a library inside your app | Client–**server** |
| The database is | **One single file** (`training.db`) | A service with data directories |
| Setup | Download and open | Install server, create user, start service |
| Login | None | Username, password, port |
| Size it suits | Small to medium, phones, apps, learning | Large multi-user systems |
| The SQL you write | **Almost identical** | **Almost identical** |

### Does learning SQLite teach me real SQL?

**Yes.** Around **95% of what you learn transfers directly.** Everything in this
syllabus — `SELECT`, `WHERE`, `ORDER BY`, `JOIN`, `GROUP BY`, `HAVING`,
subqueries, window functions, views, indexes, transactions — is **the same SQL**
in every database. Learn it here, use it anywhere.

### The honest list of what differs

These were tested on **SQLite 3.50.4**, the version DB Browser ships today:

| Topic | SQLite | Note |
|---|---|---|
| `SELECT`, `WHERE`, `ORDER BY`, `LIMIT` | ✅ Same | |
| `IN`, `BETWEEN`, `LIKE`, `EXISTS` | ✅ Same | |
| `GROUP BY`, `HAVING`, aggregates | ✅ Same | |
| `INNER` / `LEFT` / `RIGHT` / `FULL` / `SELF` join | ✅ Same | `RIGHT`/`FULL` need SQLite **3.39+** — update DB Browser if they fail |
| `UNION`, subqueries | ✅ Same | |
| Window functions (`ROW_NUMBER`, `RANK`, `DENSE_RANK`) | ✅ Same | |
| Views, Indexes | ✅ Same | |
| Transactions (`COMMIT`, `ROLLBACK`, `SAVEPOINT`) | ✅ Same | |
| Triggers | ✅ Same | |
| **`TRUNCATE TABLE`** | ❌ **Missing** | Use `DELETE FROM table;` — same result |
| **`ANY` / `ALL`** | ❌ **Missing** | Use `IN` or `MAX()`/`MIN()` instead |
| **`ALTER TABLE ... ALTER COLUMN`** | ❌ **Missing** | Can `ADD`/`DROP`/`RENAME` a column only |
| **Stored procedures, `DECLARE`, loops (PL/SQL)** | ❌ **Missing** | SQLite has no procedural language at all |
| Data types | ⚠️ Flexible | SQLite will accept text in an `INTEGER` column |
| `GRANT` / `REVOKE` (DCL) | ❌ Missing | There are no users to grant to — file permissions instead |

**Key Note:** you will be told each time we reach one of these, and shown the
equivalent used in MySQL and Oracle, so an interview never catches you out.

---

## 9. Why DB Browser for SQLite?

For learning, the tool must not get in the way. With DB Browser there is:

- ✅ **No MySQL Server** to install
- ✅ **No Oracle** installation (which is several GB)
- ✅ **No usernames or passwords**
- ✅ **No port 3306** or connection strings
- ✅ **No service** to start and stop
- ✅ **No admin rights** needed on the lab computers

Everything is stored in **one file** that you can copy to a pen drive, e-mail to
yourself, or submit as homework. If you break it, delete it and make a new one.

That means **100% of the class time goes on SQL**, not on setup problems.

---

## 10. Installation — Step by Step

**Step 1.** Download DB Browser for SQLite from:

```text
https://sqlitebrowser.org/dl/
```

Pick the **standard installer for Windows** (64-bit for most machines).

**Step 2.** Run the installer: **Next → Next → Install → Finish**.

**Step 3.** Open the application from the Start menu
(*DB Browser for SQLite*).

**Step 4.** Click **New Database**.

**Step 5.** Save it as:

```text
training.db
```

Put it somewhere you will find again, for example `Documents\SQL_Course\`.

**Step 6.** A *Create Table* window pops up — click **Cancel** for now. We will
create tables with SQL instead of clicking.

You are ready to write SQL. That is the whole setup.

---

## 11. The DB Browser Window

Four tabs matter:

| Tab | What it is for |
|---|---|
| **Database Structure** | The list of your tables, columns and indexes |
| **Browse Data** | A spreadsheet-like view of the rows in one table |
| **Edit Pragmas** | Engine settings — ignore for now |
| **Execute SQL** | **Where you will live.** Type SQL, press ▶ to run |

To run a query: go to **Execute SQL**, type it, then press
**Ctrl + Return** (or the ▶ button).

> ⚠️ **The most common beginner mistake.** After changing data, click
> **Write Changes** (Ctrl+S) in the toolbar. Until you do, your changes are
> only held in memory — close the program and they are gone.
> **Revert Changes** throws them away on purpose.

---

## 12. Your First SQL

Open **Execute SQL** and run these one at a time.

**Create a table (DDL):**

```sql
CREATE TABLE students (
    id     INTEGER PRIMARY KEY,
    name   TEXT    NOT NULL,
    marks  INTEGER
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

Expected result:

```text
id   | name          | marks
-----+---------------+------
101  | Rahul Verma   | 78
102  | Anita Sharma  | 95
103  | Karan Patel   | 38
```

**Ask a real question:**

```sql
SELECT name, marks
FROM students
WHERE marks > 50
ORDER BY marks DESC;
```

```text
name          | marks
--------------+------
Anita Sharma  | 95
Rahul Verma   | 78
```

Now click **Write Changes**. Your database is saved.

---

## 13. Common Mistakes

**1. Forgetting the semicolon** — DB Browser is forgiving with one statement,
but running several at once needs `;` between them.

**2. Forgetting Write Changes** — your work looks fine, then vanishes when you
close the program.

**3. Using double quotes for text** — SQL text uses **single quotes**:
`'Rahul'`. Double quotes mean a column *name*.

**4. `=` vs `==`** — SQL comparison is a **single** `=`, not `==` like Python.

**5. Expecting SQLite to reject wrong types** — it will happily store `'abc'`
in an `INTEGER` column. Other databases refuse. Do not rely on it.

---

## 14. Summary

- A **database** solves searching, duplication, validation, relationships,
  multi-user access and crash safety — things files and Excel cannot.
- A **DBMS** manages the database; an **RDBMS** stores it as **related tables**.
- Data lives in **tables** made of **rows** and **columns**, identified by a
  **primary key** and linked with a **foreign key**.
- **SQL** is the declarative standard language, in five families:
  **DDL, DML, DQL, TCL, DCL**.
- A query is **parsed → optimised → planned → executed**, and it runs
  **`FROM` first, `SELECT` almost last**.
- **SQL is the language; SQLite is one engine that speaks it.** ~95% of what you
  learn here works unchanged in MySQL, PostgreSQL and Oracle.
- **DB Browser for SQLite** needs no server, no login and no port — one file,
  and all the time goes on SQL.

---

## 15. Practice Questions

1. Give three problems with storing 50,000 records in Excel that a database solves.
2. What is the difference between a DBMS and an RDBMS?
3. What is the difference between a primary key and a unique key?
4. Which family does each belong to — `CREATE`, `INSERT`, `SELECT`, `ROLLBACK`?
5. Why can a `SELECT` alias not be used inside `WHERE`? (Think about run order.)
6. In one sentence each: what is SQL, and what is SQLite?
7. Name two things this syllabus covers that SQLite does **not** support.
8. Install DB Browser and create `training.db`.
9. Create a `courses` table with `course_id`, `course_name` and `duration`.
10. Insert three courses, then select only those longer than 30 days.
11. Write a query listing students with marks between 40 and 90, best first.
12. Break something on purpose: insert a student with a duplicate `id` and read
    the error message carefully.
