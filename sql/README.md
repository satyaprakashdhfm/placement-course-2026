# SQL Course — Syllabus (Day 1–18)

Taught entirely in **DB Browser for SQLite**. No server, no login, no port —
one file, `training.db`, and all class time spent on SQL.

## Days

| Day | Topic | Contents | Notes |
|---|---|---|---|
| **1** | [Database Fundamentals](Day_01_Database_Fundamentals.md) | DBMS, RDBMS, SQL, database design, SQL execution flow, **install DB Browser** | ✅ written |
| 2–3 | Database Objects | `CREATE`, `ALTER`, `DROP`, `TRUNCATE`, constraints, data types | ⚠️ see gaps |
| 4–6 | SELECT Queries | `SELECT`, `WHERE`, `ORDER BY`, `DISTINCT`, `LIMIT`, aliases, expressions | |
| 7–8 | Operators & Clauses | Comparison, logical, `IN`, `BETWEEN`, `LIKE`, `EXISTS`, `ANY`, `ALL` | ⚠️ see gaps |
| 9–10 | SQL Functions | String, numeric, date, aggregate, conditional | |
| 11–12 | Grouping | `GROUP BY`, `HAVING`, aggregations | |
| 13–14 | Joins & Set Operations | `INNER`, `LEFT`, `RIGHT`, `FULL`, `SELF` joins, `UNION` | |
| 15 | Subqueries & Window Functions | Subqueries, `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()` | |
| 16 | Views, Indexes & Transactions | Views, indexes, `COMMIT`, `ROLLBACK`, `SAVEPOINT` | |
| 17 | PL/SQL Fundamentals | Blocks, variables, loops, procedures, functions, triggers | ❌ **see gaps** |
| 18 | Revision & Interview Prep | Revision, real-world queries, complex interview questions | |

---

## What SQLite cannot do

Tested on **SQLite 3.50.4** (the version DB Browser ships today). Four syllabus
items do not exist in SQLite and need a decision before those classes:

| Day | Syllabus item | Status | Suggested handling |
|---|---|---|---|
| 2–3 | **`TRUNCATE`** | ❌ Not supported | Teach `DELETE FROM table;` and explain how `TRUNCATE` differs elsewhere |
| 2–3 | **`ALTER TABLE ... ALTER COLUMN`** | ❌ Not supported | SQLite can `ADD` / `DROP` / `RENAME` a column only. Show the create-copy-rename workaround |
| 7–8 | **`ANY` / `ALL`** | ❌ Not supported | Teach `IN`, and `MAX()`/`MIN()` as the equivalent |
| 17 | **PL/SQL** — blocks, variables, loops, procedures, functions | ❌ Not supported | SQLite has **no procedural language**. Only **triggers** from that day work |

**Day 17 is the real problem.** Five of its six topics cannot be demonstrated in
SQLite at all. Options:

1. **Teach it as theory + syntax** — show Oracle/MySQL syntax on slides, run
   only the triggers part. No install needed.
2. **Install MySQL for that one day** — real practice, but brings back the
   server, login and port setup this course avoids.
3. **Replace it** with more Day 18 interview practice, and move triggers into
   Day 16 next to views and indexes.

Everything else in the syllabus — including `RIGHT`/`FULL` joins and all the
window functions — was tested and works.

> ⚠️ `RIGHT JOIN` and `FULL OUTER JOIN` need **SQLite 3.39+** (2022). They work
> in current DB Browser, but a student on an old install will get a syntax
> error on Day 13. Tell everyone to download a fresh copy.

---

## Setup (one time)

1. Download from <https://sqlitebrowser.org/dl/>
2. Install: Next → Next → Install → Finish
3. Open it, click **New Database**, save as `training.db`
4. Go to the **Execute SQL** tab and start typing

Full walkthrough in [Day 1](Day_01_Database_Fundamentals.md#10-installation--step-by-step).
