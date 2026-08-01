# SQL Course — Syllabus (Day 1–18)

Taught entirely in **DB Browser for SQLite**. No server, no login, no port —
one file, `training.db`, and all class time spent on SQL.

## Days

| Day | Topic | Contents | Notes |
|---|---|---|---|
| **1** | [Database Fundamentals](Day_01_Database_Fundamentals.md) | DBMS, RDBMS, SQL, database design, SQL execution flow, **install DB Browser** | ✅ written |
| **2–3** | [Database Objects](Day_02_03_Database_Objects.md) | `CREATE`, `ALTER`, `DROP`, constraints, data types | ✅ written |
| **4–6** | [SELECT Queries](Day_04_06_SELECT_Queries.md) | `SELECT`, `WHERE`, `ORDER BY`, `DISTINCT`, `LIMIT`, aliases, `NULL` | ✅ written |
| **7–8** | [Operators & Clauses](Day_07_08_Operators_and_Clauses.md) | Comparison, logical, `IN`, `BETWEEN`, `LIKE`, `EXISTS` | ✅ written |
| **9–10** | [SQL Functions](Day_09_10_SQL_Functions.md) | String, numeric, date, aggregate, `CASE` | ✅ written |
| **11–12** | [Grouping](Day_11_12_Grouping.md) | `GROUP BY`, `HAVING`, aggregations | ✅ written |
| **13–14** | [Joins & Set Operations](Day_13_14_Joins_and_Set_Operations.md) | `INNER`, `LEFT`, `RIGHT`, `FULL`, `SELF`, `UNION` | ✅ written |
| **15** | [Subqueries & Window Functions](Day_15_Subqueries_and_Window_Functions.md) | Subqueries, `ROW_NUMBER`, `RANK`, `DENSE_RANK` | ✅ written |
| **16** | [Views, Indexes & Transactions](Day_16_Views_Indexes_Transactions.md) | Views, indexes, `COMMIT`, `ROLLBACK`, `SAVEPOINT`, ACID | ✅ written |
| **17** | [PL/SQL Fundamentals](Day_17_PL_SQL_Fundamentals.md) | Blocks, variables, loops, procedures, functions, triggers | ⚠️ theory + triggers |
| **18** | [Revision & Interview Prep](Day_18_Revision_and_Interview_Prep.md) | 20 interview questions, query patterns, checklist | ✅ written |

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

## Sample data

All days from 2 onwards use [`setup_training_db.sql`](setup_training_db.sql) —
10 students, 5 courses, 5 employees. It deliberately includes a student with no
course, a course with no students, a missing mark and a tied mark, so `LEFT JOIN`,
`NULL` handling and `RANK` vs `DENSE_RANK` all have something real to show.

**Every query output in these files was run against SQLite 3.50.4 and pasted in
as-is.**

## Setup (one time)

1. Download from <https://sqlitebrowser.org/dl/>
2. Install: Next → Next → Install → Finish
3. Open it, click **New Database**, save as `training.db`
4. Go to the **Execute SQL** tab, paste `setup_training_db.sql`, run it
5. Click **Write Changes**

Full walkthrough in [Day 1](Day_01_Database_Fundamentals.md#10-installation--step-by-step).
