# Revision and Interview Preparation

In this final section, we revise the whole course, work through the query
patterns worth memorising, and go through the questions asked in almost every SQL
interview.

---

# The Whole Course in One Picture

```text
   DDL   CREATE / ALTER / DROP / TRUNCATE     build the structure      Day 2
   DML   INSERT / UPDATE / DELETE             change the data          Day 2
   DQL   SELECT                               read the data            Day 3
   TCL   COMMIT / ROLLBACK / SAVEPOINT        confirm or undo          Day 9
   DCL   GRANT / REVOKE                       permissions
```

```text
   SELECT      columns, aliases, expressions          Day 3     step 5
   FROM        the table, plus JOINs                  Day 7     step 1
   WHERE       filter ROWS      (no aggregates)       Day 3, 4  step 2
   GROUP BY    make groups                            Day 6     step 3
   HAVING      filter GROUPS    (aggregates allowed)  Day 6     step 4
   ORDER BY    sort             (aliases allowed)     Day 3     step 6
   LIMIT       cut                                    Day 3     step 7
```

**The execution order answers half of all SQL questions.** Learn it first.

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

# PART 1 — QUERY PATTERNS TO MEMORISE

These seven patterns cover a very large share of real questions and interview
tasks.

---

# 1. Second Highest Value

### Using a Subquery

```sql
SELECT MAX(marks) AS second_highest FROM students
WHERE marks < (SELECT MAX(marks) FROM students);
```

### Expected Output

```
+----------------+
| second_highest |
+----------------+
|             90 |
+----------------+
```

### Using LIMIT and OFFSET — generalises to Nth

```sql
SELECT DISTINCT marks FROM students WHERE marks IS NOT NULL
ORDER BY marks DESC LIMIT 1 OFFSET 1;
```

> **The follow-up question is always about ties.** `DISTINCT` is what makes the
> second version correct — without it, two students tied for first would make the
> "second" row still show the top mark.

---

# 2. Find Duplicates

### Example

```sql
SELECT city, COUNT(*) AS n FROM students GROUP BY city HAVING COUNT(*) > 1;
```

### Expected Output

```
+-----------+---+
| city      | n |
+-----------+---+
| Hyderabad | 3 |
| Chennai   | 3 |
| Kochi     | 2 |
| Pune      | 2 |
+-----------+---+
```

The same query shape finds duplicate emails, duplicate phone numbers, duplicate
anything:

```sql
SELECT email, COUNT(*) FROM users GROUP BY email HAVING COUNT(*) > 1;
```

---

# 3. Rows With No Match

### Example

Courses nobody has joined.

```sql
SELECT c.course_name FROM courses c
LEFT JOIN students s ON s.course_id = c.course_id
WHERE s.student_id IS NULL;
```

### Expected Output

```
+-------------+
| course_name |
+-------------+
| Cloud       |
+-------------+
```

**`LEFT JOIN` + `IS NULL`** is the answer to "customers with no orders",
"products never sold", "employees with no manager".

> Test `IS NULL` on a column that can never be `NULL` in the other table —
> normally its primary key.

---

# 4. Count Including Empty Groups

### Example

```sql
SELECT c.course_name, COUNT(s.student_id) AS enrolled
FROM courses c
LEFT JOIN students s ON s.course_id = c.course_id
GROUP BY c.course_name
ORDER BY enrolled DESC;
```

### Expected Output

```
+-------------+----------+
| course_name | enrolled |
+-------------+----------+
| Python      |        3 |
| SQL         |        2 |
| Java        |        2 |
| DSA         |        2 |
| Cloud       |        0 |
+-------------+----------+
```

> **Count a column, never `*`.** With `COUNT(*)`, Cloud would show **1** — the
> single `NULL`-filled row the `LEFT JOIN` produced.

---

# 5. Top N Per Group

### Example

The top student in each city.

```sql
SELECT name, city, marks FROM (
    SELECT name, city, marks,
           RANK() OVER (PARTITION BY city ORDER BY marks DESC) AS r
    FROM students WHERE marks IS NOT NULL
) AS t
WHERE r = 1;
```

### Expected Output

```
+--------------+-----------+-------+
| name         | city      | marks |
+--------------+-----------+-------+
| Anita Sharma | Chennai   |    95 |
| Vikram Rao   | Hyderabad |    81 |
| Priya Nair   | Kochi     |    66 |
| Arjun Mehta  | Pune      |    90 |
+--------------+-----------+-------+
```

The two-level shape is compulsory — you cannot filter a window function in
`WHERE`.

---

# 6. Groups Above the Overall Average

### Example

```sql
SELECT city, ROUND(AVG(marks),2) AS avg_marks
FROM students
GROUP BY city
HAVING AVG(marks) > (SELECT AVG(marks) FROM students);
```

### Expected Output

```
+---------+-----------+
| city    | avg_marks |
+---------+-----------+
| Chennai |     74.50 |
| Pune    |     84.00 |
+---------+-----------+
```

Note the subquery inside `HAVING` — a group aggregate compared against a
whole-table aggregate.

---

# 7. Pivot — Turning Rows into Columns

### Example

```sql
SELECT city,
       SUM(CASE WHEN marks >= 75 THEN 1 ELSE 0 END) AS distinctions,
       SUM(CASE WHEN marks <  50 THEN 1 ELSE 0 END) AS fails
FROM students
GROUP BY city;
```

### Expected Output

```
+-----------+--------------+-------+
| city      | distinctions | fails |
+-----------+--------------+-------+
| Hyderabad |            2 |     1 |
| Chennai   |            1 |     0 |
| Kochi     |            0 |     1 |
| Pune      |            2 |     0 |
+-----------+--------------+-------+
```

`SUM(CASE WHEN ... THEN 1 ELSE 0 END)` is **conditional aggregation**, and it is
how SQL pivots. One pass over the table, many answers.

---

# PART 2 — THE TWENTY INTERVIEW QUESTIONS

---

**1. What is the difference between `WHERE` and `HAVING`?**
`WHERE` filters rows before grouping and cannot contain aggregates. `HAVING`
filters groups after grouping and can.

**2. `DELETE` vs `TRUNCATE` vs `DROP`?**
`DELETE` removes rows, allows `WHERE`, fires triggers, can be rolled back.
`TRUNCATE` removes all rows quickly, resets `AUTO_INCREMENT`, cannot be rolled
back in MySQL. `DROP` removes the table itself.

**3. `UNION` vs `UNION ALL`?**
`UNION` removes duplicates, which costs a sort. `UNION ALL` keeps everything and
is faster. Use `UNION ALL` unless duplicates must go.

**4. `INNER JOIN` vs `LEFT JOIN`?**
`INNER` keeps only matching rows. `LEFT` keeps every row of the left table,
filling the right side with `NULL`.

**5. Primary key vs unique key?**
Primary: one per table, never `NULL`. Unique: many allowed, `NULL` allowed.

**6. `ROW_NUMBER` vs `RANK` vs `DENSE_RANK`?**
On a tie for 4th place: `ROW_NUMBER` gives 4, 5. `RANK` gives 4, 4 then skips to
**6**. `DENSE_RANK` gives 4, 4 then **5**.

**7. `GROUP BY` vs `PARTITION BY`?**
`GROUP BY` returns one row per group. `PARTITION BY` keeps every row and adds the
calculation beside it.

**8. What does `NULL` mean, and how do you test for it?**
Unknown — not zero, not empty text. Use `IS NULL`, never `= NULL`.

**9. Why does `COUNT(*)` differ from `COUNT(column)`?**
`COUNT(*)` counts rows. `COUNT(column)` skips `NULL`s.

**10. Does `AVG` include `NULL`s?**
No. It divides by the count of non-null values. `AVG(IFNULL(col,0))` counts them
as zero.

**11. `IN` vs `EXISTS`?**
`IN` compares against a list. `EXISTS` checks whether rows exist, is `NULL`-safe,
and is usually better for a large subquery. `NOT IN` breaks when the list
contains a `NULL`.

**12. What is an index, and what is the trade-off?**
A sorted lookup structure. Faster reads, **slower writes**, more disk.

**13. What is a view? Does it make queries faster?**
A stored `SELECT` used like a table. **No** — it re-runs the query every time.
Use it for simplicity, reuse and security.

**14. What is a transaction? Explain ACID.**
A group of statements that all succeed or all fail. **A**tomicity,
**C**onsistency, **I**solation, **D**urability.

**15. Procedure vs function?**
A function must return a value and can be used inside `SELECT`. A procedure
performs an action and is called with `CALL`.

**16. What is a trigger?**
Code that runs automatically on `INSERT`, `UPDATE` or `DELETE`, with access to
`OLD` and `NEW`.

**17. What is normalisation?**
Splitting data to remove repetition. **1NF**: atomic values, no repeating groups.
**2NF**: no partial dependency on part of a composite key. **3NF**: no non-key
column depending on another non-key column.

**18. What is a foreign key?**
A column pointing at another table's primary key, giving referential integrity.
Supports `ON DELETE CASCADE` and `ON DELETE SET NULL`.

**19. What is the execution order of a `SELECT`?**
`FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT`.

**20. Why can you not use a `SELECT` alias in `WHERE`?**
`WHERE` (step 2) runs before `SELECT` (step 5), so the alias does not exist yet.
`ORDER BY` (step 6) can use it.

---

# PART 3 — THE MISTAKES THAT DO NOT GIVE AN ERROR

These are worth more class time than the loud errors, because nothing tells you
you are wrong.

| Mistake                          | What happens                          | Correct way              |
| -------------------------------- | ------------------------------------- | ------------------------ |
| `WHERE marks = NULL`             | Returns nothing                       | `IS NULL`                |
| `NOT IN (1, 2, NULL)`            | Returns nothing                       | `NOT EXISTS`             |
| `BETWEEN 22 AND 21`              | Returns nothing                       | Smaller value first      |
| `WHERE name = 'R%'`              | Returns nothing                       | `LIKE 'R%'`              |
| `JOIN` with no `ON`              | Silent **cross join**, row explosion  | Always write `ON`        |
| `COUNT(*)` with a `LEFT JOIN`    | Empty groups count as 1               | `COUNT(right.column)`    |
| `WHERE` on the right table of a `LEFT JOIN` | Becomes an `INNER JOIN`    | Put the condition in `ON` |
| `AND` / `OR` without brackets    | Wrong rows returned                   | Use brackets             |
| `ROLLBACK` with no transaction   | Nothing is undone                     | `START TRANSACTION` first |
| `ROLLBACK` after `COMMIT`        | Nothing is undone                     | Cannot be undone         |
| `SUBSTRING(name, 0, 3)`          | Empty text                            | Count from **1**         |
| `CONCAT` with a `NULL`           | Whole result is `NULL`                | Wrap in `IFNULL`         |

---

# PART 4 — MYTHS TO CORRECT

| Claim                                    | Truth                                     |
| ---------------------------------------- | ----------------------------------------- |
| "`COUNT(1)` is faster than `COUNT(*)`"   | Identical. Both are optimised the same way |
| "A view makes queries faster"            | No — it re-runs the query                 |
| "More indexes are always better"         | Every index slows down writes             |
| "`DISTINCT` fixes duplicate rows"        | It hides a broken join — fix the join     |
| "`NULL` equals `NULL`"                   | It is unknown. Use `IS NULL` or `<=>`     |
| "`TRUNCATE` can be rolled back"          | Not in MySQL. It can in PostgreSQL        |
| "`WHERE` and `HAVING` are the same"      | Only when there is no `GROUP BY`          |
| "`SELECT *` is fine"                     | More I/O, and it breaks when columns change |

---

# PART 5 — DIALECT DIFFERENCES

If an interviewer asks about a database you have not used, knowing the difference
reads as competence, not as a gap.

| Feature                | **MySQL** (ours)    | SQLite         | PostgreSQL        |
| ---------------------- | ------------------- | -------------- | ----------------- |
| Join strings           | `CONCAT(a,b)`       | `a \|\| b`     | `a \|\| b`        |
| `7/2`                  | `3.5000`            | `3`            | `3`               |
| `TRUNCATE`             | ✅                  | ❌             | ✅ (rollback-able) |
| `ANY` / `ALL`          | ✅                  | ❌             | ✅                |
| `FULL OUTER JOIN`      | ❌ emulate with `UNION` | ✅          | ✅                |
| Stored procedures      | ✅                  | ❌             | ✅                |
| `UPDATE OF column` trigger | ❌              | ✅             | ✅                |
| Auto number            | `AUTO_INCREMENT`    | `AUTOINCREMENT`| `SERIAL`          |
| Default isolation      | `REPEATABLE READ`   | —              | `READ COMMITTED`  |
| Type checking          | Strict              | Flexible       | Strictest         |
| `LIMIT`                | `LIMIT n`           | `LIMIT n`      | `LIMIT n`         |
| Oracle equivalent      | —                   | —              | `FETCH FIRST n ROWS ONLY` |

---

# PART 6 — QUERY OPTIMISATION CHECKLIST

Work down this list in order.

1. **Run `EXPLAIN` first.** Never optimise on a guess. Read `type` and `rows`.
2. **`type: ALL` on a large table** — the filter or join column needs an index.
3. **Index every foreign key.** MySQL does not do it for you.
4. **Remove functions from indexed columns** — `WHERE YEAR(d) = 2025` becomes a
   date range.
5. **Select fewer columns.** `SELECT *` costs more I/O.
6. **Filter early with `WHERE`,** not late with `HAVING`.
7. **Avoid deep `OFFSET`** — page 5000 reads and discards everything before it.
8. **Check for a missing `ON`** if a result has more rows than either table.

---

# Practice Set — Do These Without Notes

1. Every student with their course name and fee.
2. Courses with no students.
3. Students with no course.
4. The top scorer in each city.
5. The 2nd, 3rd and 4th highest marks.
6. Cities whose average is above the overall average.
7. Each course's student count, including the empty course.
8. Every student beside their city's average marks.
9. Students who joined in the first quarter of 2025.
10. Count students in each grade band using `CASE`.
11. Each city's distinctions and fails as two columns.
12. The course with the most students, in one query.
13. Students who scored more than every Kochi student.
14. Find every city that appears more than once.
15. A view of passing students, then query it.
16. An index on `marks`; prove it is used with `EXPLAIN`.
17. Inside a transaction, delete all Pune students, count, then `ROLLBACK`.
18. A trigger that logs every deleted student.
19. A function returning `Pass` or `Fail` for a given mark.
20. A procedure that reports the student count for a given city.

---

# Final Checklist

Before an interview, make sure you can do each of these **from memory**:

- [ ] Write a `SELECT` with `WHERE`, `GROUP BY`, `HAVING` and `ORDER BY`, and say
      the order they run in.
- [ ] Explain `WHERE` vs `HAVING` with an example.
- [ ] Draw the four joins and say which rows each keeps.
- [ ] Write `LEFT JOIN ... WHERE ... IS NULL` to find unmatched rows.
- [ ] Explain `RANK` vs `DENSE_RANK` using a tie.
- [ ] Write a top-N-per-group query.
- [ ] Find the second highest value two different ways.
- [ ] Find duplicates with `GROUP BY ... HAVING`.
- [ ] Explain `NULL`, `IS NULL`, and why `AVG` skips it.
- [ ] Explain what an index does and its trade-off.
- [ ] Explain a transaction and ACID.
- [ ] Explain the difference between a procedure and a function.
- [ ] Name three mistakes that produce no error message.

---

# Course Summary

Across this course you learned:

| Day | Topic                                                        |
| --- | ------------------------------------------------------------ |
| 2   | Databases, tables, data types, constraints, `CREATE`, `INSERT`, `ALTER`, `DELETE`, `TRUNCATE`, `DROP` |
| 3   | `SELECT`, `DISTINCT`, `WHERE`, `ORDER BY`, `LIMIT`, aliases, `NULL` |
| 4   | `IN`, `BETWEEN`, `LIKE`, `AND`/`OR`/`NOT`, precedence, `EXISTS` |
| 5   | String, numeric, date, aggregate and conditional functions   |
| 6   | `GROUP BY`, `HAVING`, execution order, duplicates, `WITH ROLLUP` |
| 7   | `INNER`, `LEFT`, `RIGHT`, `CROSS` and `SELF` joins, `UNION`  |
| 8   | Subqueries, derived tables, window functions, `RANK` family  |
| 9   | Views, indexes, `EXPLAIN`, transactions, `SAVEPOINT`, ACID   |
| 10  | Stored procedures, functions, handlers, `SIGNAL`, triggers   |
| 11  | Revision, query patterns, interview questions                |

You can now read, write and reason about SQL well enough to work with a real
database and to answer the questions asked in interviews.

The next things worth learning, in order:

* **Normalisation in depth** — 1NF to 3NF on messy real tables.
* **Query optimisation** — reading `EXPLAIN ANALYZE`, composite indexes.
* **Connecting SQL to a program** — using MySQL from Python.
