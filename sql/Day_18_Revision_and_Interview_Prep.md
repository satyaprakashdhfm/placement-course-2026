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
`DELETE` removes rows (can use `WHERE`, can be rolled back). `TRUNCATE` removes
all rows fast, resets auto-increment, cannot be rolled back in most databases.
`DROP` removes the table itself. *In SQLite, `TRUNCATE` does not exist.*

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
performs an action and is called with `EXEC`.

**16. What is a trigger?**
Code that runs automatically on `INSERT` / `UPDATE` / `DELETE`, with access to
`OLD` and `NEW`.

**17. What is normalisation?**
Splitting data to remove repetition. 1NF: atomic values. 2NF: no partial
dependency on part of a composite key. 3NF: no non-key column depending on
another non-key column.

**18. What is a foreign key?**
A column pointing at another table's primary key, giving referential integrity.
*In SQLite it needs `PRAGMA foreign_keys = ON`.*

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
    FROM students WHERE marks IS NOT NULL)
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
16. An index on `marks`; prove it is used with `EXPLAIN QUERY PLAN`.
17. Inside a transaction, delete all Pune students, count, then `ROLLBACK`.
18. A trigger logging every deleted student.

---

## 5. The SQLite Differences — Say These Confidently

If an interviewer asks about a feature you never ran, be straight about it and
show that you know the equivalent. That reads as competence, not a gap.

| Feature | SQLite | Everywhere else |
|---|---|---|
| `TRUNCATE` | ❌ | Use `DELETE FROM t;` |
| `ANY` / `ALL` | ❌ | `> ANY` = `> MIN`, `> ALL` = `> MAX`, `= ANY` = `IN` |
| `ALTER COLUMN` | ❌ | create → copy → drop → rename |
| Stored procedures / functions | ❌ | Oracle PL/SQL, MySQL stored programs |
| Triggers | ✅ | same idea |
| `RIGHT` / `FULL JOIN` | ✅ 3.39+ | same |
| Window functions | ✅ | same |
| Foreign keys | ✅ but **off by default** | on by default |
| Data types | flexible — accepts wrong types | strictly enforced |

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
