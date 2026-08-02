# SQL Course — Syllabus (Day 1–18)

Taught in **MySQL 8** with **MySQL Workbench** — the database used by most of
the industry.

📖 **[DIALECTS.md](DIALECTS.md)** compares MySQL with **SQLite** and
**PostgreSQL** side by side. Every day also ends with a 📌 *Dialect corner*
noting what changes elsewhere, so the team can move between engines.

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
