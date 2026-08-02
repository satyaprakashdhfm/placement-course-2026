# MySQL vs SQLite vs PostgreSQL — The Differences

**Use this to explain to the team why the same SQL looks slightly different
everywhere.**

We teach **MySQL** because it is the most widely used database in industry.
But every interview and every job will eventually put you in front of
PostgreSQL, SQLite or Oracle. The good news:

> **About 90% of SQL is identical everywhere.** `SELECT`, `WHERE`, `JOIN`,
> `GROUP BY`, `HAVING`, `ORDER BY`, subqueries and window functions are the
> same language. Only the edges differ.

This page is the list of edges. Everything marked ✅ / ❌ below was **tested**,
MySQL on **8.4.11** and SQLite on **3.50.4**.

---

## 1. What They Are

| | **MySQL** | **SQLite** | **PostgreSQL** |
|---|---|---|---|
| Type | Client–**server** | **Serverless** library | Client–**server** |
| The database is | A service + data directory | **One file** | A service + data directory |
| Setup | Install server, set root password | Just a file | Install server, create role |
| Login | user + password + port 3306 | none | user + password + port 5432 |
| Typical use | Web apps, most companies | Phones, browsers, small apps, tests | Analytics, complex data, GIS |
| Reputation | Fast, everywhere, easy | Tiny, zero-config | Strictest, most features |
| Typing | **Strict** | **Flexible** (accepts anything) | **Strictest** |

**A useful line for the team:** *SQLite is a file, MySQL is a service,
PostgreSQL is a service that argues with you when your data is wrong.*

---

## 2. The Differences That Bite

### String concatenation — the most common mistake

| | Syntax |
|---|---|
| **MySQL** | `CONCAT(a, b)` |
| SQLite | `a \|\| b` |
| PostgreSQL | `a \|\| b` |
| Oracle | `a \|\| b` |

⚠️ **MySQL is the odd one out.** In MySQL, `||` means **OR**, not concatenation:

```sql
SELECT 'a' || 'b';        -- MySQL
```
```text
+-------+
| pipes |
+-------+
|     0 |
+-------+
```

It returned **0** — MySQL read it as `'a' OR 'b'`, both non-numeric so both
false. In SQLite and PostgreSQL the same line returns `ab`. Silent wrong answer,
no error. Always use `CONCAT()` in MySQL.

### Division

```sql
SELECT 7/2;
```

| | Result | Integer division |
|---|---|---|
| **MySQL** | `3.5000` | `7 DIV 2` → 3 |
| SQLite | `3` | `/` is already integer |
| PostgreSQL | `3` | `7.0/2` → 3.5 |

⚠️ MySQL is again the odd one — `/` always gives a decimal.

### LIMIT

| | Syntax |
|---|---|
| **MySQL** | `LIMIT 10 OFFSET 5` or `LIMIT 5, 10` |
| SQLite | `LIMIT 10 OFFSET 5` |
| PostgreSQL | `LIMIT 10 OFFSET 5` |
| **Oracle** | `FETCH FIRST 10 ROWS ONLY` |
| **SQL Server** | `SELECT TOP 10` |

### Auto-increment

| | Syntax |
|---|---|
| **MySQL** | `id INT PRIMARY KEY AUTO_INCREMENT` |
| SQLite | `id INTEGER PRIMARY KEY AUTOINCREMENT` |
| PostgreSQL | `id SERIAL PRIMARY KEY` or `GENERATED ALWAYS AS IDENTITY` |

### Case sensitivity

| | Table names | `WHERE name = 'rahul'` |
|---|---|---|
| **MySQL** | Case-**insensitive** on Windows, **sensitive** on Linux ⚠️ | case-**insensitive** |
| SQLite | insensitive | **sensitive** (but `LIKE` is insensitive) |
| PostgreSQL | folds to lowercase | case-**sensitive** |

⚠️ This one causes real production bugs: code written on a Windows laptop
breaks when deployed to a Linux server, because `SELECT * FROM Students` no
longer finds `students`.

---

## 3. Feature Support — Tested

| Feature | **MySQL 8** | **SQLite 3.50** | **PostgreSQL** |
|---|---|---|---|
| `SELECT` / `WHERE` / `ORDER BY` / `LIMIT` | ✅ | ✅ | ✅ |
| `IN`, `BETWEEN`, `LIKE`, `EXISTS` | ✅ | ✅ | ✅ |
| `GROUP BY`, `HAVING` | ✅ | ✅ | ✅ |
| `INNER` / `LEFT` / `RIGHT` JOIN | ✅ | ✅ (3.39+) | ✅ |
| **`FULL OUTER JOIN`** | ❌ **not supported** | ✅ (3.39+) | ✅ |
| `UNION`, `UNION ALL` | ✅ | ✅ | ✅ |
| `INTERSECT`, `EXCEPT` | ❌ (8.0.31+ has them) | ✅ | ✅ |
| **`ANY` / `ALL`** | ✅ | ❌ **not supported** | ✅ |
| Window functions | ✅ **8.0+** | ✅ 3.25+ | ✅ |
| CTEs (`WITH`) | ✅ 8.0+ | ✅ | ✅ |
| **`TRUNCATE`** | ✅ | ❌ **not supported** | ✅ |
| `ALTER TABLE … MODIFY COLUMN` | ✅ | ❌ **not supported** | ✅ (`ALTER COLUMN … TYPE`) |
| **Stored procedures / functions** | ✅ | ❌ **none at all** | ✅ (PL/pgSQL) |
| Triggers | ✅ | ✅ | ✅ |
| Views | ✅ (updatable) | ✅ (**read-only**) | ✅ |
| `CHECK` constraints | ✅ **8.0.16+** | ✅ | ✅ |
| Foreign keys | ✅ on by default | ⚠️ **off by default** | ✅ on |
| Strict data types | ✅ rejects wrong types | ❌ accepts anything | ✅ strictest |

### The two big reversals

Coming from SQLite, these flip:

1. **`FULL OUTER JOIN` works in SQLite but NOT in MySQL.** In MySQL you emulate
   it with `LEFT JOIN` + `UNION` + `RIGHT JOIN` — see Day 13–14 §5.
2. **Stored procedures do not exist in SQLite but do in MySQL.** Day 17 is a
   hands-on class here, not theory.

---

## 4. Function Name Translation

Same job, different name. This is the table to keep open in an interview.

| Job | **MySQL** | **SQLite** | **PostgreSQL** |
|---|---|---|---|
| Join strings | `CONCAT(a,b)` | `a \|\| b` | `a \|\| b` or `CONCAT` |
| Substring | `SUBSTRING(s,1,3)` | `SUBSTR(s,1,3)` | `SUBSTRING(s,1,3)` |
| Length | `LENGTH(s)` / `CHAR_LENGTH(s)` | `LENGTH(s)` | `LENGTH(s)` |
| Today | `CURDATE()` | `DATE('now')` | `CURRENT_DATE` |
| Now | `NOW()` | `DATETIME('now')` | `NOW()` |
| Year from a date | `YEAR(d)` | `STRFTIME('%Y', d)` | `EXTRACT(YEAR FROM d)` |
| Days between | `DATEDIFF(a,b)` | `JULIANDAY(a)-JULIANDAY(b)` | `a - b` |
| Format a date | `DATE_FORMAT(d,'%d-%m-%Y')` | `STRFTIME('%d-%m-%Y', d)` | `TO_CHAR(d,'DD-MM-YYYY')` |
| NULL default | `IFNULL(a,b)` | `IFNULL(a,b)` | `COALESCE(a,b)` |
| **Works in all three** | **`COALESCE(a,b)`** | ✅ | ✅ |
| Type change | `CAST(x AS SIGNED)` | `CAST(x AS INTEGER)` | `CAST(x AS INTEGER)` or `x::int` |
| Query plan | `EXPLAIN` | `EXPLAIN QUERY PLAN` | `EXPLAIN ANALYZE` |
| List tables | `SHOW TABLES;` | `.tables` | `\dt` |
| Describe a table | `DESCRIBE students;` | `PRAGMA table_info(students);` | `\d students` |

**Key Note:** when you have a choice, use **`COALESCE`** over `IFNULL` and
**`CAST`** over `::` — they are the SQL standard and work everywhere.

---

## 5. Data Types

| Purpose | **MySQL** | **SQLite** | **PostgreSQL** |
|---|---|---|---|
| Whole number | `INT`, `BIGINT` | `INTEGER` | `INTEGER`, `BIGINT` |
| Decimal | `DECIMAL(10,2)`, `DOUBLE` | `REAL` | `NUMERIC(10,2)` |
| Short text | `VARCHAR(50)` | `TEXT` | `VARCHAR(50)`, `TEXT` |
| Long text | `TEXT` | `TEXT` | `TEXT` |
| Date | **`DATE`** | ❌ **no date type** — `TEXT` `'YYYY-MM-DD'` | `DATE` |
| Date + time | `DATETIME`, `TIMESTAMP` | `TEXT` | `TIMESTAMP` |
| True / false | `BOOLEAN` (really `TINYINT(1)`) | `INTEGER` 0/1 | **real `BOOLEAN`** |
| Auto id | `AUTO_INCREMENT` | `AUTOINCREMENT` | `SERIAL` |

⚠️ **SQLite has only 5 storage classes and no `DATE` type.** It *accepts* the
words `VARCHAR(50)` and `DATETIME` and quietly maps them to `TEXT`. That is why
SQLite code often "works" and then fails when moved to MySQL.

---

## 6. The Same Query, Three Ways

**"Students who joined in 2025, newest first, with a label."**

MySQL:
```sql
SELECT CONCAT(name, ' (', city, ')') AS student,
       YEAR(joined_on) AS yr
FROM students
WHERE YEAR(joined_on) = 2025
ORDER BY joined_on DESC
LIMIT 3;
```

SQLite:
```sql
SELECT name || ' (' || city || ')' AS student,
       STRFTIME('%Y', joined_on) AS yr
FROM students
WHERE STRFTIME('%Y', joined_on) = '2025'
ORDER BY joined_on DESC
LIMIT 3;
```

PostgreSQL:
```sql
SELECT name || ' (' || city || ')' AS student,
       EXTRACT(YEAR FROM joined_on) AS yr
FROM students
WHERE EXTRACT(YEAR FROM joined_on) = 2025
ORDER BY joined_on DESC
LIMIT 3;
```

**The shape never changed.** Only concatenation and the date function did.
That is the lesson to give the team: learn the *shape*, look up the *spelling*.

---

## 7. FULL OUTER JOIN in MySQL

Because MySQL lacks it, this is the workaround worth memorising:

```sql
-- PostgreSQL / SQLite
SELECT s.name, c.course_name
FROM students s FULL OUTER JOIN courses c ON s.course_id = c.course_id;

-- MySQL equivalent
SELECT s.name, c.course_name
FROM students s LEFT JOIN courses c ON s.course_id = c.course_id
UNION
SELECT s.name, c.course_name
FROM students s RIGHT JOIN courses c ON s.course_id = c.course_id;
```

`UNION` (not `UNION ALL`) removes the rows counted twice by both halves.

---

## 8. What to Tell an Interviewer

If you are asked about a database you have not used, this is the answer that
shows competence:

> *"I learned on MySQL. The core SQL — joins, grouping, window functions — is
> the same in PostgreSQL and SQLite. The differences I know to watch for are
> string concatenation (`CONCAT` vs `||`), the date functions, `LIMIT` vs
> `FETCH FIRST`, and that MySQL has no `FULL OUTER JOIN` so you emulate it with
> `LEFT` + `UNION` + `RIGHT`."*

That answer is worth more than claiming to know all three.

---

## 9. One-Line Summary

| | Remember it as |
|---|---|
| **MySQL** | Industry default. `CONCAT`, `AUTO_INCREMENT`, no `FULL OUTER JOIN`, `/` gives decimals |
| **SQLite** | One file, no server. `\|\|`, no `TRUNCATE`, no procedures, no strict types, no `DATE` |
| **PostgreSQL** | The strict one. `\|\|`, `SERIAL`, has everything, real `BOOLEAN` |
