# Day 18 · Revision & Interview Prep

**Duration:** 50–60 Minutes

### Learning Outcomes
- Revise the whole course in one page.
- Answer the questions that come up in **every** SQL interview.
- Solve **real-world query patterns** from memory.

---

## 1. The Whole Course on One Page

```text
   DDL   CREATE / ALTER / DROP              build the structure     (Day 2-3)
   DML   INSERT / UPDATE / DELETE           change the data
   DQL   SELECT                             read the data           (Day 4-6)
   TCL   COMMIT / ROLLBACK / SAVEPOINT      confirm or undo         (Day 16)
```

```text
   SELECT      columns, aliases, expressions          Day 4-6    step 5
   FROM        the table, plus JOINs                  Day 13-14  step 1
   WHERE       filter ROWS      (no aggregates)       Day 4-8    step 2
   GROUP BY    make groups                            Day 11-12  step 3
   HAVING      filter GROUPS    (aggregates allowed)  Day 11-12  step 4
   ORDER BY    sort             (aliases allowed)     Day 4-6    step 6
   LIMIT       cut                                    Day 4-6    step 7
```

**The run order is the answer to half of all SQL questions.**

---

## 2. The Twenty Questions You Will Be Asked

**1. `WHERE` vs `HAVING`?**
`WHERE` filters rows before grouping and cannot contain aggregates. `HAVING`
filters groups after grouping and can.

**2. `DELETE` vs `TRUNCATE` vs `DROP`?**
`DELETE` removes rows (can use `WHERE`, can be rolled back, fires triggers).
`TRUNCATE` removes all rows fast, resets `AUTO_INCREMENT`, cannot be rolled
back in MySQL. `DROP` removes the table itself.

**3. `UNION` vs `UNION ALL`?**
`UNION` removes duplicates, which costs a sort. `UNION ALL` keeps everything and
is faster. Use `UNION ALL` unless duplicates must go.

**4. `INNER` vs `LEFT JOIN`?**
`INNER` keeps only matching rows. `LEFT` keeps every row of the left table,
filling the right with `NULL`.

**5. Primary key vs unique key?**
Primary: one per table, never `NULL`. Unique: many allowed, `NULL` allowed.

**6. `RANK` vs `DENSE_RANK` vs `ROW_NUMBER`?**
On a tie: `ROW_NUMBER` gives 4, 5. `RANK` gives 4, 4 then skips to **6**.
`DENSE_RANK` gives 4, 4 then **5**.

**7. `GROUP BY` vs `PARTITION BY`?**
`GROUP BY` returns one row per group. `PARTITION BY` keeps every row and adds
the calculation beside it.

**8. What does `NULL` mean, and how do you test for it?**
Unknown — not zero and not empty. Use `IS NULL`, never `= NULL`.

**9. Why does `COUNT(*)` differ from `COUNT(column)`?**
`COUNT(*)` counts rows; `COUNT(column)` skips `NULL`s.

**10. Does `AVG` include `NULL`s?**
No. `AVG` divides by the count of non-null values. Use `AVG(IFNULL(col,0))` to
count them as zero.

**11. `IN` vs `EXISTS`?**
`IN` compares against a list. `EXISTS` checks whether rows exist, is `NULL`-safe
and often faster on large subqueries. `NOT IN` breaks when the list has a `NULL`.

**12. What is an index and what is the trade-off?**
A sorted lookup structure. Faster reads, **slower writes**, more disk.

**13. What is a view? Does it make things faster?**
A stored query used like a table. **No** — it re-runs each time. Use it for
simplicity, reuse and security.

**14. What is a transaction? Explain ACID.**
A group of statements that all succeed or all fail.
**A**tomicity, **C**onsistency, **I**solation, **D**urability.

**15. Procedure vs function?**
A function must return a value and can be used inside `SELECT`. A procedure
performs an action and is called with `CALL` (MySQL) or `EXEC` (SQL Server).

**16. What is a trigger?**
Code that runs automatically on `INSERT` / `UPDATE` / `DELETE`, with access to
`OLD` and `NEW`.

**17. What is normalisation?**
Splitting data to remove repetition. 1NF: atomic values. 2NF: no partial
dependency on part of a composite key. 3NF: no non-key column depending on
another non-key column.

**18. What is a foreign key?**
A column pointing at another table's primary key, giving referential integrity.
Supports `ON DELETE CASCADE` / `SET NULL`.

**19. Order of execution of a SELECT?**
`FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT`.

**20. Why can you not use a `SELECT` alias in `WHERE`?**
`WHERE` (step 2) runs before `SELECT` (step 5), so the alias does not exist yet.
`ORDER BY` (step 6) can use it.

---

## 3. Query Patterns to Memorise

**Second highest value**

```sql
SELECT MAX(marks) FROM students WHERE marks < (SELECT MAX(marks) FROM students);
```
```text
90
```

Or, and this generalises to *n*th:

```sql
SELECT DISTINCT marks FROM students WHERE marks IS NOT NULL
ORDER BY marks DESC LIMIT 1 OFFSET 1;
```

**Find duplicates**

```sql
SELECT city, COUNT(*) AS n FROM students GROUP BY city HAVING COUNT(*) > 1;
```

**Rows with no match (orphans)**

```sql
SELECT c.course_name FROM courses c
LEFT JOIN students s ON s.course_id = c.course_id
WHERE s.id IS NULL;
```
```text
Cloud
```

**Top N per group**

```sql
SELECT name, city, marks FROM (
    SELECT name, city, marks,
           RANK() OVER (PARTITION BY city ORDER BY marks DESC) AS r
    FROM students WHERE marks IS NOT NULL) AS ranked
WHERE r = 1;
```

**Above the average**

```sql
SELECT name, marks FROM students WHERE marks > (SELECT AVG(marks) FROM students);
```

**Count including empty groups** — count a column, never `*`

```sql
SELECT c.course_name, COUNT(s.id) AS enrolled
FROM courses c LEFT JOIN students s ON s.course_id = c.course_id
GROUP BY c.course_name;
```

**Pivot with CASE** — turn rows into columns

```sql
SELECT city,
       SUM(CASE WHEN marks >= 75 THEN 1 ELSE 0 END) AS distinctions,
       SUM(CASE WHEN marks <  50 THEN 1 ELSE 0 END) AS fails
FROM students
GROUP BY city;
```
```text
city      | distinctions | fails
----------+--------------+------
Chennai   | 1            | 0
Hyderabad | 2            | 1
Kochi     | 0            | 1
Pune      | 2            | 0
```

---

## 4. Real-World Exercises

Do these without looking anything up.

1. Every student with their course name and fee.
2. Courses with no students.
3. Students with no course.
4. The top scorer in each city.
5. The 2nd, 3rd and 4th highest marks.
6. Cities where the average is above the overall average.
7. Each course's student count, including the empty one.
8. Every student beside their city's average and the difference.
9. Students who joined in the first quarter of 2025.
10. Count students per grade band with `CASE`.
11. Each employee with their manager's name, keeping the boss.
12. The course with the most students (one query).
13. Students scoring more than **every** Kochi student.
14. Each city's distinctions and fails as two columns.
15. A view of passing students, then query it.
16. An index on `marks`; prove it is used with `EXPLAIN` (look at `type`).
17. Inside a transaction, delete all Pune students, count, then `ROLLBACK`.
18. A trigger logging every deleted student.

---

## 5. Know Your Dialects — Say These Confidently

If an interviewer asks about a database you have not used, showing you know the
differences reads as competence, not a gap.

| Feature | **MySQL** (ours) | SQLite | PostgreSQL |
|---|---|---|---|
| Join strings | `CONCAT(a,b)` | `a \|\| b` | `a \|\| b` |
| `7/2` | `3.5000` | `3` | `3` |
| `TRUNCATE` | ✅ | ❌ | ✅ (rollback-able) |
| `ANY` / `ALL` | ✅ | ❌ | ✅ |
| **`FULL OUTER JOIN`** | ❌ **emulate with UNION** | ✅ | ✅ |
| Stored procedures | ✅ | ❌ none | ✅ PL/pgSQL |
| Window functions | ✅ 8.0+ | ✅ | ✅ |
| Auto id | `AUTO_INCREMENT` | `AUTOINCREMENT` | `SERIAL` |
| Year from date | `YEAR(d)` | `STRFTIME('%Y',d)` | `EXTRACT(YEAR FROM d)` |
| Query plan | `EXPLAIN` | `EXPLAIN QUERY PLAN` | `EXPLAIN ANALYZE` |
| `=` on text | case-**insensitive** | case-sensitive | case-sensitive |
| Wrong data types | rejected | **accepted** | rejected |

**The line to use in an interview:**

> *"I learned on MySQL. The core SQL is the same everywhere — joins, grouping,
> window functions. The differences I watch for are `CONCAT` vs `||`, the date
> functions, and that MySQL has no `FULL OUTER JOIN`, so you emulate it with
> `LEFT` + `UNION` + `RIGHT`."*

Full detail in [DIALECTS.md](DIALECTS.md).

---

## 6. 🔺 ADVANCED — Teacher Reference

### 6.1 The hard interview questions

**Q. Find the Nth highest salary/mark.**

```sql
SELECT DISTINCT marks FROM students WHERE marks IS NOT NULL
ORDER BY marks DESC LIMIT 1 OFFSET 1;          -- N-1 as the offset
```
Better, because it handles ties explicitly and states intent:
```sql
SELECT marks FROM (
    SELECT marks, DENSE_RANK() OVER (ORDER BY marks DESC) AS r
    FROM students WHERE marks IS NOT NULL) t
WHERE r = 2;
```
The follow-up is always *"what if two people tie for first?"* — `DENSE_RANK`
treats them as one place, `ROW_NUMBER` does not. Say which you mean.

**Q. Delete duplicate rows, keeping one.**

```sql
DELETE s1 FROM students s1
JOIN students s2
  ON s1.name = s2.name AND s1.id > s2.id;       -- keeps the lowest id
```
The self-join with `>` is the trick: every duplicate except the smallest matches.

**Q. Gaps and islands — find consecutive runs.**

```sql
SELECT MIN(id) AS run_start, MAX(id) AS run_end, COUNT(*) AS len
FROM (SELECT id, id - ROW_NUMBER() OVER (ORDER BY id) AS grp FROM students) t
GROUP BY grp;
```
```text
+-----------+---------+-----+
| run_start | run_end | len |
+-----------+---------+-----+
|       101 |     110 |  10 |
+-----------+---------+-----+
```

One run of 10 — because our ids 101–110 happen to have no gaps. Delete a row and
re-run it and you get two runs; that is the point of the query.

`id - ROW_NUMBER()` is **constant within a consecutive run** and changes at every
gap. That one line is the whole technique — used for streaks, attendance runs
and session detection.

**Q. Running total without window functions (MySQL 5.7).**

```sql
SET @total := 0;
SELECT name, marks, (@total := @total + marks) AS running
FROM students WHERE marks IS NOT NULL ORDER BY joined_on;
```
Worth knowing for legacy systems. ⚠️ Deprecated in MySQL 8, and the evaluation
order is not guaranteed — use window functions where you can.

**Q. Pivot rows into columns.** Conditional aggregation — Day 11–12 §10.3.
SQL cannot pivot on values unknown at write time; that needs dynamic SQL
(Day 17 §11.3) or the reporting layer.

### 6.2 Query optimisation checklist

Work down this list, in order:

1. **`EXPLAIN` first.** Never optimise on a guess. Look at `type` and `rows`.
2. **`type: ALL` on a big table** → the join or filter column needs an index.
3. **Index every foreign key.** MySQL does not do it for you.
4. **Un-wrap functions on columns** — `WHERE YEAR(d)=2025` → a date range.
5. **Composite index order** — equality columns first, then the range column.
6. **Select fewer columns** — `SELECT *` blocks covering indexes.
7. **`Using temporary; Using filesort`** → try to make an index satisfy the
   `GROUP BY`/`ORDER BY`.
8. **Beware `OR`** across different columns — often two `UNION ALL` branches
   each using its own index are faster.
9. **Paginate by keyset**, not `OFFSET` (Day 4–6 §13.4).
10. **`ANALYZE TABLE`** if the optimiser's row estimates look wrong.

### 6.3 Anti-patterns to name

| Anti-pattern | Why it hurts |
|---|---|
| `SELECT *` everywhere | more I/O, breaks covering indexes, breaks silently when columns change |
| Functions on indexed columns in `WHERE` | forces a full scan |
| `OFFSET` deep pagination | reads and discards everything before the page |
| Storing money in `FLOAT` | comparisons fail |
| Storing dates as text | no validation, no date arithmetic |
| `NOT IN` with a nullable subquery | silently returns nothing |
| Indexing every column | writes slow, disk grows, optimiser gets confused |
| Cursors for set-based work | N round trips instead of one statement |
| No foreign keys "for performance" | orphan rows, corrupted reports later |
| `sql_mode = ''` to silence errors | hides real bugs |

### 6.4 Design questions they ask seniors

**"How would you design a schema for X?"** — say this sequence out loud:
entities → relationships → keys → normalise to 3NF → then denormalise only where
a measured read problem exists.

**"How do you handle a table that has grown to 500 million rows?"** — index
review, archiving old data, partitioning by range, read replicas, then sharding.
In that order — reach for the cheap fix first.

**"Where would you cache?"** — the database buffer pool first (free), then an
application cache, then Redis. Name the invalidation strategy or the answer is
incomplete.

### 6.5 Things people get wrong under pressure

| Claim | Truth |
|---|---|
| "`COUNT(1)` is faster than `COUNT(*)`" | Identical. Both are optimised the same |
| "`TRUNCATE` can be rolled back" | Not in MySQL. It can in PostgreSQL |
| "A view makes queries faster" | No. It re-runs the query |
| "More indexes are always better" | Every index slows writes |
| "`DISTINCT` fixes duplicate rows" | It hides a broken join — fix the join |
| "`NULL` equals `NULL`" | It is UNKNOWN. Use `IS NULL` or `<=>` |
| "`WHERE` and `HAVING` are interchangeable" | Only when there is no `GROUP BY` |

---

## 6. Final Checklist

Before an interview, make sure you can do each of these **from memory**:

- [ ] Write a `SELECT` with `WHERE`, `GROUP BY`, `HAVING` and `ORDER BY`, and
      say the order they run in.
- [ ] Explain `WHERE` vs `HAVING` with an example.
- [ ] Draw the four joins and say which rows each keeps.
- [ ] Write a `LEFT JOIN … IS NULL` to find orphans.
- [ ] Explain `RANK` vs `DENSE_RANK` using a tie.
- [ ] Write a top-N-per-group query.
- [ ] Find the second highest value two different ways.
- [ ] Find duplicates with `GROUP BY … HAVING`.
- [ ] Explain `NULL`, `IS NULL`, and why `AVG` skips it.
- [ ] Explain indexes and their trade-off.
- [ ] Explain a transaction and ACID.
- [ ] Say what SQLite cannot do, and the equivalent elsewhere.
