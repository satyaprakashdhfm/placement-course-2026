# SQL Course — Syllabus

Taught in **MySQL 8** with **MySQL Workbench**.

There are **two sets of notes in this folder**, kept deliberately:

| Set | Files | Purpose |
|---|---|---|
| **Teaching notes** | `DAY2_...`, `DAY3_...`, `DAY4_...` | What you teach *from*, live. One operation per numbered section, Syntax → Example → Expected Output, self-contained and runnable top to bottom |
| **Reference notes** | `Day_01_...` to `Day_18_...` | Deeper background, dialect comparisons, and the 🔺 ADVANCED teacher sections. Read before class, not during |

## Teaching notes (class order)

| # | File | Topics |
|---|---|---|
| 1 | [DAY2_CREATE_UPATE_DELETE.md](DAY2_CREATE_UPATE_DELETE.md) | Databases, tables, data types, constraints, `CREATE`, `INSERT`, `ALTER`, `DELETE`, `TRUNCATE`, `DROP` |
| 2 | [DAY3_SELECT_RETRIEVING_DATA.md](DAY3_SELECT_RETRIEVING_DATA.md) | `SELECT`, `DISTINCT`, `WHERE`, `ORDER BY`, `LIMIT`, `OFFSET`, aliases, `NULL`, `IFNULL` |
| 3 | [DAY4_OPERATORS_AND_CLAUSES.md](DAY4_OPERATORS_AND_CLAUSES.md) | `IN`, `BETWEEN`, `LIKE`, `AND`/`OR`/`NOT`, precedence, `EXISTS` |
| — | *still to write* | Functions · Grouping · Joins · Subqueries & Window · Views/Indexes/Transactions · Stored Programs · Revision |

Every SQL block in the teaching notes is executed against MySQL before it is
committed, and the `Expected Output` blocks are the real output. The examples in
`Common Errors` are real failures, with the real message.

---

## Days

| Day | Topic | Contents |
|---|---|---|
| **1** | [Database Fundamentals](Day_01_Database_Fundamentals.md) | DBMS, RDBMS, SQL, execution flow, **install MySQL** |
| **2–3** | [Database Objects](Day_02_03_Database_Objects.md) | `CREATE`, `ALTER`, `DROP`, `TRUNCATE`, constraints, `AUTO_INCREMENT` |
| **4–6** | [SELECT Queries](Day_04_06_SELECT_Queries.md) | `SELECT`, `WHERE`, `ORDER BY`, `DISTINCT`, `LIMIT`, aliases, `NULL` |
| **7–8** | [Operators & Clauses](Day_07_08_Operators_and_Clauses.md) | `IN`, `BETWEEN`, `LIKE`, `EXISTS`, `ANY`, `ALL`, 3-valued logic |
| **9–10** | [SQL Functions](Day_09_10_SQL_Functions.md) | String, numeric, date, aggregate, `CASE` |
| **11–12** | [Grouping](Day_11_12_Grouping.md) | `GROUP BY`, `HAVING`, run order |
| **13–14** | [Joins & Set Operations](Day_13_14_Joins_and_Set_Operations.md) | `INNER`, `LEFT`, `RIGHT`, `SELF`, `UNION`, emulating `FULL OUTER` |
| **15** | [Subqueries & Window Functions](Day_15_Subqueries_and_Window_Functions.md) | Subqueries, `ROW_NUMBER`, `RANK`, `DENSE_RANK` |
| **16** | [Views, Indexes & Transactions](Day_16_Views_Indexes_Transactions.md) | Views, indexes, `EXPLAIN`, `COMMIT`/`ROLLBACK`, ACID |
| **17** | [Stored Programs (PL/SQL)](Day_17_PL_SQL_Fundamentals.md) | Procedures, functions, loops, handlers, triggers |
| **18** | [Revision & Interview Prep](Day_18_Revision_and_Interview_Prep.md) | 20 interview questions, query patterns, checklist |

---

## 🔺 Advanced sections — teacher reference

**Every day file ends with a `🔺 ADVANCED — Teacher Reference` section
before the practice questions.** These are *your* notes, not the student
handout: deeper mechanics, real-world gotchas, and the follow-up questions a
sharp student or an interviewer will ask.

| Day | Advanced topics |
|---|---|
| 1 | Normalisation by the anomaly each form prevents, connection/buffer-pool architecture, storage engines, `information_schema` |
| 2–3 | Generated columns, `ENUM`/`SET`, surrogate vs natural keys and InnoDB clustering, online `ALTER` algorithms |
| 4–6 | `<=>` null-safe equality, custom sort orders and the `FIELD()` trap, `REGEXP`, deep-pagination and keyset paging, collations |
| 7–8 | Row constructors, *why* `NOT IN` + NULL returns nothing, full precedence table, `BETWEEN` on datetimes, `IN`/`EXISTS`/`JOIN` compared |
| 9–10 | JSON columns and `->>`, `GROUP_CONCAT`/`SUBSTRING_INDEX`, date bucketing, numeric precision traps, functions that kill indexes |
| 11–12 | `WITH ROLLUP`, `GROUP_CONCAT`, conditional aggregation (pivot), `ONLY_FULL_GROUP_BY`/`ANY_VALUE`, grouping performance |
| 13–14 | Semi/anti-join patterns, reading `EXPLAIN FORMAT=TREE`, join algorithms, `ON` vs `WHERE` on outer joins, set operators |
| 15 | CTEs, **recursive CTEs**, `LAG`/`LEAD`/`NTILE`/`PERCENT_RANK`, frame clauses, running totals, median |
| 16 | **Leftmost-prefix rule**, covering indexes, reading `EXPLAIN`, cardinality, isolation levels, deadlocks, materialised views |
| 17 | `SIGNAL`, cursors, dynamic SQL and injection, events/scheduler, transactions in procedures, when *not* to use them |
| 18 | Hard interview questions with answers, optimisation checklist, anti-patterns, design questions, myths |

Everything in them was executed against MySQL 8.4.11 — the outputs are real.

---

## Version requirements

| Feature | Needs |
|---|---|
| Window functions, CTEs | **MySQL 8.0+** |
| `CHECK` constraints enforced | **MySQL 8.0.16+** |
| `INTERSECT` / `EXCEPT` | MySQL 8.0.31+ |
| **`FULL OUTER JOIN`** | ❌ **not in any MySQL version** — see Day 13–14 §5 |

Everything in these files was written against **MySQL 8.4**. On MySQL 5.7,
Days 15 and 17 will need workarounds.

---

## Sample data

All days from 2 onwards use [`setup_training_db.sql`](setup_training_db.sql) —
10 students, 5 courses, 5 employees. It deliberately includes a student with no
course, a course with no students, a missing mark and a tied mark, so
`LEFT JOIN`, `NULL` handling and `RANK` vs `DENSE_RANK` all have something real
to show.

**Every query output in these files was run against MySQL 8.4.11 and pasted in
as-is.**

## Setup (one time)

1. Download the MySQL Installer from <https://dev.mysql.com/downloads/installer/>
2. Choose **Developer Default**, keep port **3306**, set a **root password**
3. Open **MySQL Workbench** and connect to *Local instance*
4. Open `setup_training_db.sql` and run it (⚡ button)
5. `USE training;` and start querying

Full walkthrough in [Day 1](Day_01_Database_Fundamentals.md#9-installing-mysql).

**Quick alternative with Docker:**

```bash
docker run -d --name mysqlcourse -e MYSQL_ROOT_PASSWORD=root -p 3306:3306 mysql:8
```
