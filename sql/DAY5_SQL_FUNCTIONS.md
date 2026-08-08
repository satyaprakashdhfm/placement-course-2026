# SQL Functions in MySQL

In this section, we will learn the built-in functions MySQL provides for working
with text, numbers, dates, and for summarising whole columns.

---

# What is a Function?

A **function** takes one or more values, does something with them, and returns a
result.

Some important points:

* A function never changes the data stored in the table.
* It only changes what appears in the **result**.
* Functions can be used in `SELECT`, `WHERE`, `ORDER BY` and `GROUP BY`.
* Functions can be nested — the result of one can be passed into another.

---

# Two Types of Functions

This is the most important idea in this topic.

| Type          | Works on            | Rows in → Rows out | Examples                       |
| ------------- | ------------------- | ------------------ | ------------------------------ |
| **Scalar**    | One value at a time | 10 → **10**        | `UPPER`, `ROUND`, `LENGTH`     |
| **Aggregate** | A whole column      | 10 → **1**         | `COUNT`, `SUM`, `AVG`, `MAX`   |

A **scalar** function keeps your row count. An **aggregate** function collapses
all rows into a single row.

---

# Table Used in This Section

Run this once before starting.

```sql
CREATE DATABASE IF NOT EXISTS training;
USE training;

DROP TABLE IF EXISTS students;

CREATE TABLE students (
    student_id INT PRIMARY KEY,
    name       VARCHAR(50) NOT NULL,
    city       VARCHAR(50),
    age        INT,
    course     VARCHAR(50),
    marks      INT,
    joined_on  DATE
);

INSERT INTO students VALUES
(101,'Rahul Verma','Hyderabad',21,'Python',78,'2025-01-15'),
(102,'Anita Sharma','Chennai',22,'SQL',95,'2025-01-20'),
(103,'Karan Patel','Hyderabad',20,'Python',38,'2025-02-01'),
(104,'Priya Nair','Kochi',23,'Java',66,'2025-02-10'),
(105,'Vikram Rao','Hyderabad',21,'SQL',81,'2025-03-05'),
(106,'Sneha Iyer','Chennai',22,'Java',54,'2025-03-12'),
(107,'Arjun Mehta','Pune',24,'DSA',90,'2025-04-02'),
(108,'Divya Menon','Kochi',20,'Python',45,'2025-04-18'),
(109,'Rohit Sinha','Pune',23,NULL,78,'2025-05-01'),
(110,'Meera Nair','Chennai',21,'DSA',NULL,'2025-05-20');
```

---

# PART 1 — STRING FUNCTIONS

---

# 1. UPPER, LOWER and LENGTH

| Function      | Purpose                       |
| ------------- | ----------------------------- |
| `UPPER(text)` | Converts to capital letters   |
| `LOWER(text)` | Converts to small letters     |
| `LENGTH(text)`| Counts the characters         |

### Syntax

```sql
SELECT UPPER(column_name) FROM table_name;
```

### Example

```sql
SELECT name, UPPER(name) AS caps, LOWER(name) AS small, LENGTH(name) AS len
FROM students LIMIT 3;
```

### Expected Output

```
+--------------+--------------+--------------+-----+
| name         | caps         | small        | len |
+--------------+--------------+--------------+-----+
| Rahul Verma  | RAHUL VERMA  | rahul verma  |  11 |
| Anita Sharma | ANITA SHARMA | anita sharma |  12 |
| Karan Patel  | KARAN PATEL  | karan patel  |  11 |
+--------------+--------------+--------------+-----+
```

`LENGTH` counts the space too — `Rahul Verma` is 11 characters.

---

# 2. SUBSTRING, LEFT and RIGHT

| Function                    | Purpose                          |
| --------------------------- | -------------------------------- |
| `SUBSTRING(text, start, n)` | `n` characters from position `start` |
| `LEFT(text, n)`             | First `n` characters             |
| `RIGHT(text, n)`            | Last `n` characters              |

### Syntax

```sql
SELECT SUBSTRING(column_name, start_position, number_of_characters)
FROM table_name;
```

### Example

```sql
SELECT name, SUBSTRING(name,1,5) AS first5, LEFT(name,3) AS l3, RIGHT(name,4) AS r4
FROM students LIMIT 3;
```

### Expected Output

```
+--------------+--------+------+------+
| name         | first5 | l3   | r4   |
+--------------+--------+------+------+
| Rahul Verma  | Rahul  | Rah  | erma |
| Anita Sharma | Anita  | Ani  | arma |
| Karan Patel  | Karan  | Kar  | atel |
+--------------+--------+------+------+
```

> **Note:** SQL counts characters starting from **1**, not from 0. So
> `SUBSTRING(name,1,5)` gives the **first** five characters.

---

# 3. CONCAT — Joining Text

### Syntax

```sql
SELECT CONCAT(value1, value2, value3) FROM table_name;
```

### Example

```sql
SELECT CONCAT(name,' - ',city) AS student_city FROM students LIMIT 3;
```

### Expected Output

```
+-------------------------+
| student_city            |
+-------------------------+
| Rahul Verma - Hyderabad |
| Anita Sharma - Chennai  |
| Karan Patel - Hyderabad |
+-------------------------+
```

> **Note:** If any value inside `CONCAT` is `NULL`, the whole result becomes
> `NULL`. Use `CONCAT_WS` or wrap the column in `IFNULL` to avoid this.

---

# 4. REPLACE

### Syntax

```sql
SELECT REPLACE(column_name, old_text, new_text) FROM table_name;
```

### Example

```sql
SELECT name, REPLACE(name,'a','@') AS replaced FROM students LIMIT 3;
```

### Expected Output

```
+--------------+--------------+
| name         | replaced     |
+--------------+--------------+
| Rahul Verma  | R@hul Verm@  |
| Anita Sharma | Anit@ Sh@rm@ |
| Karan Patel  | K@r@n P@tel  |
+--------------+--------------+
```

Every `a` was replaced, not just the first one.

---

# 5. TRIM, LTRIM and RTRIM

These remove unwanted spaces — very common when cleaning imported data.

### Example

```sql
SELECT TRIM('   MySQL   ') AS trimmed,
       LTRIM('   Hi')      AS left_trim,
       RTRIM('Hi   ')      AS right_trim;
```

### Expected Output

```
+---------+-----------+------------+
| trimmed | left_trim | right_trim |
+---------+-----------+------------+
| MySQL   | Hi        | Hi         |
+---------+-----------+------------+
```

| Function | Removes spaces from |
| -------- | ------------------- |
| `TRIM`   | Both sides          |
| `LTRIM`  | Left side only      |
| `RTRIM`  | Right side only     |

---

Yes. If you're building a **SQL learning repo/notebook**, you can keep the same `students` table as your base dataset and then add small sections demonstrating each function.

For example, your repo can have a section like this:

### String Functions — TRIM, LTRIM, RTRIM

```sql
-- Add sample records with leading/trailing spaces
INSERT INTO students
VALUES
(111, '   Surya Reddy', 'Hyderabad', 25, 'SQL', 85, '2025-06-01'),
(112, 'Anita Sharma   ', 'Chennai', 24, 'Python', 90, '2025-06-02'),
(113, '   Rahul Kumar   ', 'Pune', 23, 'Java', 75, '2025-06-03');

-- Remove spaces from the left
SELECT name, LTRIM(name) AS left_trimmed
FROM students
WHERE student_id >= 111;

-- Remove spaces from the right
SELECT name, RTRIM(name) AS right_trimmed
FROM students
WHERE student_id >= 111;

-- Remove spaces from both sides
SELECT name, TRIM(name) AS trimmed_name
FROM students
WHERE student_id >= 111;
```

**Concept:**

* `LTRIM()` → removes spaces from the **left side**.
* `RTRIM()` → removes spaces from the **right side**.
* `TRIM()` → removes spaces from **both sides**.
* These functions modify the **query result only**; they don't change the stored data unless you use them inside an `UPDATE`.

You can follow the same pattern for the other SQL functions you're learning:

```text
students table
     ↓
INSERT sample data if needed
     ↓
SELECT statement demonstrating the function
     ↓
Short explanation of what the function does
     ↓
Expected result / observation
```

That's actually a very good way to structure your SQL repo because students can **run each section independently and immediately see what the function does**.


# 6. INSTR — Finding a Position

`INSTR` returns the position of a character or word, or `0` if not found.

### Example

```sql
SELECT name, INSTR(name,'a') AS pos_of_a FROM students LIMIT 3;
```

### Expected Output

```
+--------------+----------+
| name         | pos_of_a |
+--------------+----------+
| Rahul Verma  |        2 |
| Anita Sharma |        1 |
| Karan Patel  |        2 |
+--------------+----------+
```

`Anita` gives 1 because MySQL is not case sensitive here — it matched the
capital `A`.

---

# PART 2 — NUMERIC FUNCTIONS

---

# 7. ROUND, CEIL and FLOOR

| Function          | Purpose                            |
| ----------------- | ---------------------------------- |
| `ROUND(n, d)`     | Rounds to `d` decimal places       |
| `CEIL(n)`         | Rounds **up** to a whole number    |
| `FLOOR(n)`        | Rounds **down** to a whole number  |

### Example

```sql
SELECT marks, ROUND(marks/3,2) AS rounded, CEIL(marks/3) AS up, FLOOR(marks/3) AS down
FROM students WHERE marks IS NOT NULL LIMIT 3;
```

### Expected Output

```
+-------+---------+------+------+
| marks | rounded | up   | down |
+-------+---------+------+------+
|    78 |   26.00 |   26 |   26 |
|    95 |   31.67 |   32 |   31 |
|    38 |   12.67 |   13 |   12 |
+-------+---------+------+------+
```

For 78, all three agree because 78÷3 is exactly 26.

---

# 8. ABS, POWER, SQRT and MOD

### Example

```sql
SELECT ABS(-45) AS absolute, POWER(2,5) AS power,
       SQRT(81) AS square_root, MOD(10,3) AS remainder;
```

### Expected Output

```
+----------+-------+-------------+-----------+
| absolute | power | square_root | remainder |
+----------+-------+-------------+-----------+
|       45 |    32 |           9 |         1 |
+----------+-------+-------------+-----------+
```

| Function       | Meaning                  |
| -------------- | ------------------------ |
| `ABS(n)`       | Removes the minus sign   |
| `POWER(a,b)`   | a raised to the power b  |
| `SQRT(n)`      | Square root              |
| `MOD(a,b)`     | Remainder after division |

---

# 9. Division — An Important Difference

### Example

```sql
SELECT 7/2 AS division, 7 DIV 2 AS integer_division, 7%2 AS remainder;
```

### Expected Output

```
+----------+------------------+-----------+
| division | integer_division | remainder |
+----------+------------------+-----------+
|   3.5000 |                3 |         1 |
+----------+------------------+-----------+
```

| Operator | Result | Meaning                     |
| -------- | ------ | --------------------------- |
| `/`      | 3.5000 | Normal division             |
| `DIV`    | 3      | Whole number division       |
| `%`      | 1      | Remainder                   |

> **Note:** In MySQL, `7/2` gives `3.5000`. In some other databases such as
> PostgreSQL, `7/2` gives `3` because both numbers are integers.

---

# PART 3 — DATE FUNCTIONS

---

# 10. Extracting Parts of a Date

| Function          | Returns             |
| ----------------- | ------------------- |
| `YEAR(date)`      | The year            |
| `MONTH(date)`     | Month number (1–12) |
| `DAY(date)`       | Day of the month    |
| `MONTHNAME(date)` | Month name          |
| `DAYNAME(date)`   | Day name            |

### Example

```sql
SELECT name, joined_on, YEAR(joined_on) AS yr, MONTH(joined_on) AS mth, DAY(joined_on) AS dy
FROM students LIMIT 3;
```

### Expected Output

```
+--------------+------------+------+------+------+
| name         | joined_on  | yr   | mth  | dy   |
+--------------+------------+------+------+------+
| Rahul Verma  | 2025-01-15 | 2025 |    1 |   15 |
| Anita Sharma | 2025-01-20 | 2025 |    1 |   20 |
| Karan Patel  | 2025-02-01 | 2025 |    2 |    1 |
+--------------+------------+------+------+------+
```

### Example — Names Instead of Numbers

```sql
SELECT name, joined_on, MONTHNAME(joined_on) AS month_name, DAYNAME(joined_on) AS day_name
FROM students LIMIT 3;
```

### Expected Output

```
+--------------+------------+------------+-----------+
| name         | joined_on  | month_name | day_name  |
+--------------+------------+------------+-----------+
| Rahul Verma  | 2025-01-15 | January    | Wednesday |
| Anita Sharma | 2025-01-20 | January    | Monday    |
| Karan Patel  | 2025-02-01 | February   | Saturday  |
+--------------+------------+------------+-----------+
```

---

# 11. DATE_FORMAT — Changing How a Date Looks

### Syntax

```sql
SELECT DATE_FORMAT(column_name, 'format') FROM table_name;
```

### Example

```sql
SELECT name, DATE_FORMAT(joined_on,'%d-%m-%Y') AS formatted FROM students LIMIT 3;
```

### Expected Output

```
+--------------+------------+
| name         | formatted  |
+--------------+------------+
| Rahul Verma  | 15-01-2025 |
| Anita Sharma | 20-01-2025 |
| Karan Patel  | 01-02-2025 |
+--------------+------------+
```

| Code | Meaning        |
| ---- | -------------- |
| `%Y` | 4-digit year   |
| `%y` | 2-digit year   |
| `%m` | Month number   |
| `%M` | Month name     |
| `%d` | Day number     |
| `%W` | Day name       |

> **Note:** `DATE_FORMAT` returns **text**, not a date. Never sort or compare on
> its result — `'15-01-2025'` sorts before `'20-12-2024'` as text.

---
. Text → DATE using STR_TO_DATE()

If a date is stored as text, and we want to perform date operations on it, we can convert it into an actual DATE using STR_TO_DATE().

SELECT
    STR_TO_DATE('15-01-2025', '%d-%m-%Y') AS converted_date;

Yes. If you mean **“I want the SQL statements and the expected output to appear in a code-style block so I can copy them directly into my notebook”**, then yes — use triple backticks:

```sql
SELECT *
FROM students;
```

And for output, you can use a normal table or a text block:

```text
student_id | name         | joined_on
-----------|--------------|-----------
101        | Rahul Verma  | 2025-01-15
102        | Anita Sharma | 2025-01-20
```

For your date example, I would structure it like this:

### 1. Original DATE

```sql
SELECT joined_on
FROM students
WHERE student_id = 101;
```

**Output:**

```text
joined_on
----------
2025-01-15
```

**Datatype:**

```text
DATE
```

### 2. Convert DATE → formatted text

```sql
SELECT
    joined_on,
    DATE_FORMAT(joined_on, '%d-%m-%Y') AS formatted_date
FROM students
WHERE student_id = 101;
```

**Output:**

```text
joined_on   | formatted_date
------------|---------------
2025-01-15  | 15-01-2025
```

Here:

```text
joined_on       → DATE
formatted_date  → formatted string
```

### 3. Actually create a table to see the datatype

```sql
DROP TABLE IF EXISTS formatted_dates;

CREATE TABLE formatted_dates AS
SELECT
    student_id,
    joined_on,
    DATE_FORMAT(joined_on, '%d-%m-%Y') AS formatted_date
FROM students;
```

Then:

```sql
DESC formatted_dates;
```

**Expected output:**

```text
Field            Type
---------------  -------------
student_id       int
joined_on        date
formatted_date   varchar(...)
```

### 4. Convert the text back to DATE

```sql
DROP TABLE IF EXISTS converted_dates;

CREATE TABLE converted_dates AS
SELECT
    student_id,
    formatted_date,
    STR_TO_DATE(formatted_date, '%d-%m-%Y') AS converted_date
FROM formatted_dates;
```

Then:

```sql
DESC converted_dates;
```

**Expected output:**

```text
Field            Type
---------------  -------------
student_id       int
formatted_date   varchar(...)
converted_date   date
```

And finally:

```sql
SELECT *
FROM converted_dates;
```

**Output:**

```text
student_id | formatted_date | converted_date
-----------|----------------|---------------
101        | 15-01-2025     | 2025-01-15
102        | 20-01-2025     | 2025-01-20
103        | 01-02-2025     | 2025-02-01
```

So your teaching flow becomes very clear:

```text
DATE
  ↓
DATE_FORMAT()
  ↓
VARCHAR / TEXT
  ↓
STR_TO_DATE()
  ↓
DATE
```

And yes, **triple backticks with `sql`** are the right format when you want the SQL to be copy-pasteable.


# 12. DATEDIFF — Days Between Two Dates

### Syntax

```sql
SELECT DATEDIFF(later_date, earlier_date);
```

### Example

```sql
SELECT name, DATEDIFF('2025-06-01', joined_on) AS days_since FROM students LIMIT 3;
```

### Expected Output

```
+--------------+------------+
| name         | days_since |
+--------------+------------+
| Rahul Verma  |        137 |
| Anita Sharma |        132 |
| Karan Patel  |        120 |
+--------------+------------+
```

> **Note:** In notes and tests, use a **fixed date** like `'2025-06-01'`. If you
> use `CURDATE()`, the answer changes every day and students cannot tell whether
> the query is wrong or the date moved.

---
Current date
SELECT CURDATE();

Example output:

2026-08-08

CURRENT_DATE() can also be used:

SELECT CURRENT_DATE();
Current date and time
SELECT NOW();

Example:

2026-08-08 22:47:00

So:

CURDATE() → Current date only
NOW()     → Current date + current time
Yesterday


# 13. DATE_ADD and DATE_SUB

### Syntax

```sql
SELECT DATE_ADD(column_name, INTERVAL number unit) FROM table_name;
```

### Example

```sql
SELECT name,
       DATE_ADD(joined_on, INTERVAL 30 DAY)  AS after_30,
       DATE_SUB(joined_on, INTERVAL 1 MONTH) AS before_1m
FROM students LIMIT 3;
```

### Expected Output

```
+--------------+------------+------------+
| name         | after_30   | before_1m  |
+--------------+------------+------------+
| Rahul Verma  | 2025-02-14 | 2024-12-15 |
| Anita Sharma | 2025-02-19 | 2024-12-20 |
| Karan Patel  | 2025-03-03 | 2025-01-01 |
+--------------+------------+------------+
```

Units available: `DAY`, `WEEK`, `MONTH`, `QUARTER`, `YEAR`, `HOUR`, `MINUTE`.

Notice that subtracting one month from `2025-01-15` correctly gives
`2024-12-15` — MySQL handles the year change and different month lengths for you.

### Other Useful Date Functions

| Function     | Returns                    |
| ------------ | -------------------------- |
| `CURDATE()`  | Today's date               |
| `NOW()`      | Today's date and time      |
| `LAST_DAY(d)`| Last date of that month    |

---
Use DATE_SUB():

SELECT DATE_SUB(CURDATE(), INTERVAL 1 DAY);

Or more simply:

SELECT CURDATE() - INTERVAL 1 DAY;
Tomorrow
SELECT CURDATE() + INTERVAL 1 DAY;
Find students who joined in the last 30 days
SELECT *
FROM students
WHERE joined_on >= CURDATE() - INTERVAL 30 DAY;
Find the difference between two dates

Use DATEDIFF():

SELECT DATEDIFF('2025-03-05', '2025-01-15');

This returns the number of days between the two dates.

# PART 4 — AGGREGATE FUNCTIONS

---

# 14. The Five Aggregate Functions

| Function     | Returns                       | Ignores `NULL`? |
| ------------ | ----------------------------- | --------------- |
| `COUNT(*)`   | Number of **rows**            | ❌ No           |
| `COUNT(col)` | Number of **non-null values** | ✅ Yes          |
| `SUM(col)`   | Total                         | ✅ Yes          |
| `AVG(col)`   | Average                       | ✅ Yes          |
| `MIN(col)`   | Smallest value                | ✅ Yes          |
| `MAX(col)`   | Largest value                 | ✅ Yes          |

### Example

```sql
SELECT COUNT(*)            AS total_rows,
       COUNT(marks)        AS with_marks,
       SUM(marks)          AS total,
       ROUND(AVG(marks),2) AS average,
       MIN(marks)          AS lowest,
       MAX(marks)          AS highest
FROM students;
```

### Expected Output

```
+------------+------------+-------+---------+--------+---------+
| total_rows | with_marks | total | average | lowest | highest |
+------------+------------+-------+---------+--------+---------+
|         10 |          9 |   625 |   69.44 |     38 |      95 |
+------------+------------+-------+---------+--------+---------+
```

Ten rows collapsed into **one row**. That is what an aggregate does.

---

# 15. Why COUNT(*) and COUNT(marks) Differ

Look carefully at the previous output:

* `COUNT(*)` = **10** — it counts every **row**.
* `COUNT(marks)` = **9** — it skips the row where marks are `NULL`.

This also explains the average:

```text
AVG(marks) = 625 / 9  = 69.44        <- divides by 9, not 10
```

If a missing mark should be treated as zero, you must say so:

```sql
SELECT ROUND(AVG(IFNULL(marks,0)),2) AS average_with_zeros FROM students;
```

```
+--------------------+
| average_with_zeros |
+--------------------+
|              62.50 |
+--------------------+
```

**Two different answers, both correct.** Which one is right depends on the
question being asked. This is a very common interview question.

---

# PART 5 — CONDITIONAL FUNCTIONS

---

# 16. CASE — The SQL if / else

### Syntax

```sql
SELECT CASE WHEN condition1 THEN result1
            WHEN condition2 THEN result2
            ELSE result3
       END AS alias_name
FROM table_name;
```

### Example

```sql
SELECT name, marks,
       CASE WHEN marks >= 75   THEN 'Distinction'
            WHEN marks >= 50   THEN 'Pass'
            WHEN marks IS NULL THEN 'Not graded'
            ELSE 'Fail'
       END AS result
FROM students;
```

### Expected Output

```
+--------------+-------+-------------+
| name         | marks | result      |
+--------------+-------+-------------+
| Rahul Verma  |    78 | Distinction |
| Anita Sharma |    95 | Distinction |
| Karan Patel  |    38 | Fail        |
| Priya Nair   |    66 | Pass        |
| Vikram Rao   |    81 | Distinction |
| Sneha Iyer   |    54 | Pass        |
| Arjun Mehta  |    90 | Distinction |
| Divya Menon  |    45 | Fail        |
| Rohit Sinha  |    78 | Distinction |
| Meera Nair   |  NULL | Not graded  |
+--------------+-------+-------------+
```

**Key Notes:**

* Conditions are checked **top to bottom**. The **first** true one wins.
* Put the strictest condition first. If `marks >= 50` came before
  `marks >= 75`, nobody would ever get a Distinction.
* Without `ELSE`, unmatched rows get `NULL`.

---

# 17. IF — For Two Outcomes Only

### Syntax

```sql
SELECT IF(condition, value_if_true, value_if_false) FROM table_name;
```

### Example

```sql
SELECT name, IF(marks >= 50,'Pass','Fail') AS status FROM students LIMIT 4;
```

### Expected Output

```
+--------------+--------+
| name         | status |
+--------------+--------+
| Rahul Verma  | Pass   |
| Anita Sharma | Pass   |
| Karan Patel  | Fail   |
| Priya Nair   | Pass   |
+--------------+--------+
```

> **Note:** `IF()` is MySQL only. `CASE` is standard SQL and works in every
> database. Use `IF` for two outcomes, `CASE` for three or more.

---

# 18. IFNULL and COALESCE

| Function                | Purpose                              |
| ----------------------- | ------------------------------------ |
| `IFNULL(a, b)`          | Returns `b` if `a` is `NULL`         |
| `COALESCE(a, b, c, …)`  | Returns the first value that is not `NULL` |

### Example

```sql
SELECT name, IFNULL(marks,0) AS marks, COALESCE(course,'Not assigned') AS course
FROM students WHERE marks IS NULL OR course IS NULL;
```

### Expected Output

```
+-------------+-------+--------------+
| name        | marks | course       |
+-------------+-------+--------------+
| Rohit Sinha |    78 | Not assigned |
| Meera Nair  |     0 | DSA          |
+-------------+-------+--------------+
```

> **Note:** `COALESCE` is standard SQL and accepts many values. `IFNULL` accepts
> exactly two and is MySQL only. Prefer `COALESCE`.

---

# Common Errors

## Error 1: Mixing an Aggregate with a Normal Column

```sql
SELECT name, AVG(marks) FROM students;
```

### Error

```text
ERROR 1140 (42000): In aggregated query without GROUP BY, expression #1 of
SELECT list contains nonaggregated column 'training.students.name'; this is
incompatible with sql_mode=only_full_group_by
```

### Reason

`AVG(marks)` returns **one** value, but `name` has ten. MySQL cannot decide
which name to show.

### Solution

Use `GROUP BY`, which is the next topic.

---

## Error 2: Using an Aggregate in WHERE

```sql
SELECT city FROM students WHERE COUNT(*) > 2;
```

### Error

```text
ERROR 1111 (HY000): Invalid use of group function
```

### Reason

`WHERE` runs **before** the rows are grouped, so aggregates do not exist yet.

### Solution

Use `HAVING` instead — also the next topic.

---

## Error 3: Starting SUBSTRING at 0

```sql
SELECT SUBSTRING('Rahul',0,3) AS wrong, SUBSTRING('Rahul',1,3) AS right_way;
```

### Result

```
+-------+-----------+
| wrong | right_way |
+-------+-----------+
|       | Rah       |
+-------+-----------+
```

There is **no error** — you simply get an empty text. SQL counts from **1**.

---

## Error 4: CONCAT with a NULL

```sql
SELECT CONCAT(name,' - ',course) AS info FROM students WHERE student_id = 109;
```

### Result

```
+------+
| info |
+------+
| NULL |
+------+
```

### Reason

`Rohit Sinha` has no course. One `NULL` makes the whole `CONCAT` become `NULL`.

### Solution

```sql
SELECT CONCAT(name,' - ',IFNULL(course,'None')) AS info
FROM students WHERE student_id = 109;
```

---

# Commands Covered

| Category        | Functions                                                     |
| --------------- | ------------------------------------------------------------- |
| **String**      | `UPPER`, `LOWER`, `LENGTH`, `SUBSTRING`, `LEFT`, `RIGHT`, `CONCAT`, `REPLACE`, `TRIM`, `LTRIM`, `RTRIM`, `INSTR` |
| **Numeric**     | `ROUND`, `CEIL`, `FLOOR`, `ABS`, `POWER`, `SQRT`, `MOD`, `DIV` |
| **Date**        | `YEAR`, `MONTH`, `DAY`, `MONTHNAME`, `DAYNAME`, `DATE_FORMAT`, `DATEDIFF`, `DATE_ADD`, `DATE_SUB`, `CURDATE`, `NOW`, `LAST_DAY` |
| **Aggregate**   | `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`                            |
| **Conditional** | `CASE`, `IF`, `IFNULL`, `COALESCE`                             |

---

# Summary

* **Scalar** functions keep the number of rows. **Aggregate** functions reduce
  all rows to one.
* Text positions start at **1**, not 0.
* `COUNT(*)` counts rows; every other aggregate **ignores `NULL`**.
* `AVG` divides by the count of **non-null** values, not the row count.
* `CASE` checks conditions top to bottom — the first true one wins.
* One `NULL` inside `CONCAT` makes the whole result `NULL`.
* Aggregates cannot be used in `WHERE`, and cannot be mixed with plain columns
  without `GROUP BY`.

---

# Practice Questions

1. Display every student's name in capital letters with its length.
2. Display the first 4 characters of each city.
3. Join the name and course into one column reading `Rahul Verma (Python)`.
4. Replace every space in the name with an underscore.
5. Display each student's marks divided by 7, rounded to 2 decimals.
6. Display the remainder when marks are divided by 10.
7. Display the year and month name each student joined.
8. Display `joined_on` in `dd/mm/yyyy` format.
9. How many days had passed between each student's joining date and `2025-06-01`?
10. Show the date 45 days after each student joined.
11. Show the total, average, highest and lowest marks in one query.
12. Count the rows, and count the students who have marks. Explain the difference.
13. Recalculate the average treating missing marks as 0.
14. Label each student `Distinction`, `Pass`, `Fail` or `Not graded` using `CASE`.
15. Use `IF` to show `Senior` for age above 22, otherwise `Junior`.
16. Display `Not assigned` wherever a course is missing.

---

# Class Summary

In this notebook, you learned:

* The difference between **scalar** and **aggregate** functions
* String functions: `UPPER`, `LOWER`, `LENGTH`, `SUBSTRING`, `CONCAT`, `REPLACE`, `TRIM`, `INSTR`
* Numeric functions: `ROUND`, `CEIL`, `FLOOR`, `ABS`, `POWER`, `SQRT`, `MOD`
* The three kinds of division: `/`, `DIV` and `%`
* Date functions: `YEAR`, `MONTHNAME`, `DATE_FORMAT`, `DATEDIFF`, `DATE_ADD`, `DATE_SUB`
* Aggregate functions: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`
* Why `COUNT(*)` and `COUNT(column)` give different answers
* Conditional logic using `CASE`, `IF`, `IFNULL` and `COALESCE`

You are now ready to learn the next topic: **Grouping Data using `GROUP BY` and
`HAVING`**.
