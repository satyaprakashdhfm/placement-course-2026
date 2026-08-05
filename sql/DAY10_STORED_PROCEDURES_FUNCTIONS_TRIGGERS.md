# Stored Procedures, Functions and Triggers

In this section, we will learn how to store code **inside** the database —
programs with variables, conditions and loops, and code that runs automatically
when data changes.

---

# Why Put Code in the Database?

Plain SQL is **declarative** — one statement, one result. It has no variables, no
`if`, and no loops. **Stored programs** add them.

| SQL alone                  | SQL + stored programs        |
| -------------------------- | ---------------------------- |
| One statement at a time    | Many statements as one unit  |
| No variables               | Variables                    |
| No branching               | `IF` / `CASE`                |
| No loops                   | `WHILE`, `REPEAT`, `LOOP`    |
| Errors stop you            | Error handlers               |
| Runs from your application | Runs **inside** the database |

| Benefit                | Explanation                                  |
| ---------------------- | -------------------------------------------- |
| **Less network trips** | Send one call instead of 100 statements      |
| **Reuse**              | Every application shares the same logic      |
| **Security**           | Grant access to the procedure, not the tables |
| **Speed**              | Parsed once, stored ready to run             |

> 📌 **Naming.** Oracle calls this **PL/SQL**. MySQL calls it **stored programs**.
> SQL Server calls it **T-SQL**, PostgreSQL calls it **PL/pgSQL**. Same idea,
> different dialect.

---

# Table Used in This Section

Run this once before starting.

```sql
CREATE DATABASE IF NOT EXISTS training;
USE training;

DROP TABLE IF EXISTS students;

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

# 1. DELIMITER — Read This First

A stored program **contains semicolons**. The client would stop at the first one,
so you temporarily change the statement terminator.

### Syntax

```sql
DELIMITER $$

CREATE PROCEDURE demo()
BEGIN
    SELECT 'first';
    SELECT 'second';
END$$

DELIMITER ;
```

**What is happening:**

1. `DELIMITER $$` tells the client "statements now end with `$$`, not `;`".
2. The semicolons inside `BEGIN ... END` are passed through untouched.
3. `END$$` finishes the whole `CREATE PROCEDURE`.
4. `DELIMITER ;` puts it back to normal.

> **Key Note:** Forgetting `DELIMITER` is the **number one error** on this topic.
> The symptom is a syntax error pointing at the **first line inside `BEGIN`**.

📌 Oracle uses a lone `/` on its own line instead. PostgreSQL wraps the body in
`$$ ... $$` quotes.

---

# 2. A Simple Stored Procedure

A **procedure** performs an action. You run it with `CALL`.

### Syntax

```sql
DELIMITER $$
CREATE PROCEDURE procedure_name(IN parameter_name datatype)
BEGIN
    -- statements
END$$
DELIMITER ;
```

### Example

```sql
DELIMITER $$
CREATE PROCEDURE city_report(IN p_city VARCHAR(50))
BEGIN
    SELECT name, marks
    FROM students
    WHERE city = p_city
    ORDER BY marks DESC;
END$$
DELIMITER ;
```

### Run It

```sql
CALL city_report('Hyderabad');
```

### Expected Output

```
+-------------+-------+
| name        | marks |
+-------------+-------+
| Vikram Rao  |    81 |
| Rahul Verma |    78 |
| Karan Patel |    38 |
+-------------+-------+
```

**One definition, a different answer for every argument.** That is the value of a
procedure.

> **Note:** Naming parameters with a `p_` prefix is a common convention. It stops
> you confusing a parameter with a column of the same name.

---

# 3. Parameter Modes

| Mode    | Meaning                          |
| ------- | -------------------------------- |
| `IN`    | Given to the procedure (default) |
| `OUT`   | Sent **back** to the caller      |
| `INOUT` | Both                             |

### Example — OUT Parameter

```sql
DELIMITER $$
CREATE PROCEDURE count_in_city(IN p_city VARCHAR(50), OUT p_total INT)
BEGIN
    SELECT COUNT(*) INTO p_total FROM students WHERE city = p_city;
END$$
DELIMITER ;

CALL count_in_city('Chennai', @n);
SELECT @n AS chennai_students;
```

### Expected Output

```
+------------------+
| chennai_students |
+------------------+
|                3 |
+------------------+
```

`@n` is a **session variable** — it lives until you disconnect. The procedure
filled it using `SELECT ... INTO`.

---

# 4. Variables, IF and ELSEIF

### Syntax

```sql
DECLARE variable_name datatype DEFAULT value;
SET variable_name = value;
```

### Example

```sql
DELIMITER $$
CREATE PROCEDURE grade_report()
BEGIN
    DECLARE v_count INT DEFAULT 0;
    DECLARE v_avg   DECIMAL(5,2);
    DECLARE v_label VARCHAR(20);

    SELECT COUNT(*), AVG(marks) INTO v_count, v_avg FROM students;

    IF v_avg >= 75 THEN     SET v_label = 'Strong batch';
    ELSEIF v_avg >= 50 THEN SET v_label = 'Average batch';
    ELSE                    SET v_label = 'Weak batch';
    END IF;

    SELECT v_count AS students, ROUND(v_avg,2) AS avg_marks, v_label AS verdict;
END$$
DELIMITER ;

CALL grade_report();
```

### Expected Output

```
+----------+-----------+---------------+
| students | avg_marks | verdict       |
+----------+-----------+---------------+
|       10 |     69.44 | Average batch |
+----------+-----------+---------------+
```

**Key Notes:**

* All `DECLARE` statements must come **first**, before any other statement.
* `SET` assigns a value. `SELECT ... INTO v` puts a query result into a variable.
* One `SELECT` can fill **two** variables at once, as shown.
* `ELSEIF` is **one word**. Every `IF` ends with `END IF;`.

📌 Oracle uses `:=` to assign and needs a `DECLARE` section **before** `BEGIN`.
MySQL declares **inside** `BEGIN` and uses `SET`.

---

# 5. The Three Loops

```sql
WHILE i <= 5 DO          -- tests first
    SET i = i + 1;
END WHILE;

REPEAT                   -- tests last, so always runs at least once
    SET i = i + 1;
UNTIL i > 5 END REPEAT;

my_loop: LOOP            -- you must leave it yourself
    SET i = i + 1;
    IF i > 5 THEN LEAVE my_loop; END IF;
END LOOP;
```

### A Working WHILE Loop

```sql
DELIMITER $$
CREATE PROCEDURE countdown()
BEGIN
    DECLARE i INT DEFAULT 1;
    DROP TEMPORARY TABLE IF EXISTS nums;
    CREATE TEMPORARY TABLE nums (n INT);
    WHILE i <= 5 DO
        INSERT INTO nums VALUES (i);
        SET i = i + 1;
    END WHILE;
    SELECT GROUP_CONCAT(n) AS loop_output FROM nums;
END$$
DELIMITER ;

CALL countdown();
```

### Expected Output

```
+-------------+
| loop_output |
+-------------+
| 1,2,3,4,5   |
+-------------+
```

> **Note:** A loop needs something that changes, or it runs forever. Here
> `SET i = i + 1;` is what eventually ends it.

---

# 6. Stored Functions

A **function** must **return a value**, and can be used **inside a `SELECT`**.

### Syntax

```sql
DELIMITER $$
CREATE FUNCTION function_name(parameter_name datatype)
RETURNS datatype
DETERMINISTIC
BEGIN
    -- statements
    RETURN value;
END$$
DELIMITER ;
```

### Example

```sql
DELIMITER $$
CREATE FUNCTION get_grade(p_marks INT)
RETURNS VARCHAR(20)
DETERMINISTIC
BEGIN
    DECLARE v_grade VARCHAR(20);
    IF p_marks >= 75 THEN     SET v_grade = 'Distinction';
    ELSEIF p_marks >= 50 THEN SET v_grade = 'Pass';
    ELSE                      SET v_grade = 'Fail';
    END IF;
    RETURN v_grade;
END$$
DELIMITER ;

SELECT name, marks, get_grade(marks) AS grade FROM students LIMIT 4;
```

### Expected Output

```
+--------------+-------+-------------+
| name         | marks | grade       |
+--------------+-------+-------------+
| Rahul Verma  |    78 | Distinction |
| Anita Sharma |    95 | Distinction |
| Karan Patel  |    38 | Fail        |
| Priya Nair   |    66 | Pass        |
+--------------+-------+-------------+
```

The function was called **once per row**, exactly like a built-in function.

> **Key Note:** `DETERMINISTIC` promises that the same input always gives the same
> output. Without it — or `READS SQL DATA` if the function queries a table —
> MySQL may refuse to create the function when binary logging is on.

---

# 7. Procedure vs Function

**This is a guaranteed interview question.**

| Point                    | Procedure               | Function                |
| ------------------------ | ----------------------- | ----------------------- |
| Returns a value          | Optional, via `OUT`     | **Compulsory** (`RETURNS`) |
| Called with              | `CALL name(...)`        | Inside an expression    |
| Usable in `SELECT`       | ❌ No                   | ✅ **Yes**              |
| Can return a result set  | ✅ Yes                  | ❌ No                   |
| Purpose                  | **Do** something        | **Calculate** something |

**Simple rule:** if you want a value back to use in a query, write a function.
If you want an action performed, write a procedure.

---

# 8. Error Handling with HANDLER

MySQL declares error handlers **up front**, rather than in a block at the end.

### Syntax

```sql
DECLARE EXIT HANDLER FOR SQLEXCEPTION statement;
```

| Handler          | Meaning                                    |
| ---------------- | ------------------------------------------ |
| `EXIT HANDLER`   | Run it, then **leave** the block           |
| `CONTINUE HANDLER` | Run it, then **carry on**                |
| `FOR SQLEXCEPTION` | Any error                                |
| `FOR NOT FOUND`  | A `SELECT` or cursor found nothing         |
| `FOR SQLSTATE '23000'` | One specific error code              |

### Example

```sql
DELIMITER $$
CREATE PROCEDURE safe_insert(IN p_id INT, IN p_name VARCHAR(50))
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
        SELECT 'Insert failed - id already exists' AS message;

    INSERT INTO students (student_id, name) VALUES (p_id, p_name);
    SELECT 'Inserted' AS message;
END$$
DELIMITER ;

CALL safe_insert(101,'Clash');
```

### Expected Output

```
+-----------------------------------+
| message                           |
+-----------------------------------+
| Insert failed - id already exists |
+-----------------------------------+
```

No error reached the user. The handler caught the duplicate-key failure and
printed a friendly message instead.

---

# 9. Raising Your Own Error with SIGNAL

Handlers **catch** errors. `SIGNAL` **throws** them. This is how a procedure
enforces a business rule.

### Syntax

```sql
SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'your message';
```

### Example

```sql
DELIMITER $$
CREATE PROCEDURE check_marks(IN p_marks INT)
BEGIN
    IF p_marks > 100 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Marks cannot exceed 100';
    END IF;
    SELECT CONCAT('Accepted ', p_marks) AS result;
END$$
DELIMITER ;

CALL check_marks(50);
```

```
+-------------+
| result      |
+-------------+
| Accepted 50 |
+-------------+
```

```sql
CALL check_marks(150);
```

```text
ERROR 1644 (45000): Marks cannot exceed 100
```

> **Note:** `45000` is the SQLSTATE reserved for "unhandled user-defined
> exception". Use it unless you have a specific reason not to.

---

# 10. Listing and Removing Stored Programs

```sql
SHOW PROCEDURE STATUS WHERE Db = 'training';
SHOW FUNCTION STATUS WHERE Db = 'training';
SHOW CREATE PROCEDURE city_report;

DROP PROCEDURE IF EXISTS city_report;
DROP FUNCTION IF EXISTS get_grade;
```

### Sample Output

```
+----------+---------------+-----------+----------------+
| Db       | Name          | Type      | Definer        |
+----------+---------------+-----------+----------------+
| training | city_report   | PROCEDURE | root@localhost |
| training | count_in_city | PROCEDURE | root@localhost |
| training | countdown     | PROCEDURE | root@localhost |
| training | safe_insert   | PROCEDURE | root@localhost |
+----------+---------------+-----------+----------------+
```

---

# PART 2 — TRIGGERS

---

# 11. What Is a Trigger?

A **trigger** is code that runs **automatically** when data changes. You never
call it — the database does.

### Syntax

```sql
DELIMITER $$
CREATE TRIGGER trigger_name
{BEFORE | AFTER} {INSERT | UPDATE | DELETE} ON table_name
FOR EACH ROW
BEGIN
    -- statements
END$$
DELIMITER ;
```

| Choice   | Meaning                                        |
| -------- | ---------------------------------------------- |
| `BEFORE` | Runs **before** the change — can validate or modify it |
| `AFTER`  | Runs **after** the change — used for logging   |
| `FOR EACH ROW` | Runs once per affected row                |

---

# 12. OLD and NEW

Inside a trigger, two special records are available.

| Event    | `OLD` available     | `NEW` available      |
| -------- | ------------------- | -------------------- |
| `INSERT` | ❌ No               | ✅ The incoming row  |
| `UPDATE` | ✅ Values before    | ✅ Values after      |
| `DELETE` | ✅ The row going    | ❌ No                |

---

# 13. An AFTER DELETE Trigger — Auditing

First create a log table.

```sql
DROP TABLE IF EXISTS audit_log;

CREATE TABLE audit_log (
    log_id    INT AUTO_INCREMENT PRIMARY KEY,
    action    VARCHAR(50),
    student   VARCHAR(50),
    logged_at DATETIME
);
```

### Create the Trigger

```sql
DELIMITER $$
CREATE TRIGGER log_delete
AFTER DELETE ON students
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (action, student, logged_at)
    VALUES ('DELETE', OLD.name, NOW());
END$$
DELIMITER ;
```

### Test It

```sql
DELETE FROM students WHERE student_id = 110;
SELECT action, student FROM audit_log;
```

### Expected Output

```
+--------+------------+
| action | student    |
+--------+------------+
| DELETE | Meera Nair |
+--------+------------+
```

**Nobody wrote to `audit_log`.** The trigger did it automatically. `OLD.name` gave
the name of the row being deleted.

---

# 14. An AFTER UPDATE Trigger

### Create the Trigger

```sql
DELIMITER $$
CREATE TRIGGER log_update
AFTER UPDATE ON students
FOR EACH ROW
BEGIN
    IF OLD.marks <> NEW.marks THEN
        INSERT INTO audit_log (action, student, logged_at)
        VALUES (CONCAT('UPDATE ', OLD.marks, ' -> ', NEW.marks), NEW.name, NOW());
    END IF;
END$$
DELIMITER ;
```

### Test It

```sql
DELETE FROM audit_log;
UPDATE students SET marks = 85 WHERE student_id = 101;
UPDATE students SET city  = 'Mumbai' WHERE student_id = 102;
SELECT action, student FROM audit_log;
```

### Expected Output

```
+-----------------+-------------+
| action          | student     |
+-----------------+-------------+
| UPDATE 78 -> 85 | Rahul Verma |
+-----------------+-------------+
```

Only **one** row was logged. The city update did not create a log entry, because
the `IF OLD.marks <> NEW.marks` test was false.

> ⚠️ **Important MySQL limitation.** A trigger fires on **every** update to the
> table. MySQL has **no** `AFTER UPDATE OF marks` syntax — writing that gives a
> syntax error. You must fire on all updates and filter with an `IF` inside, as
> above.
>
> 📌 PostgreSQL and SQLite **do** support `UPDATE OF column`. This is a real
> dialect difference worth mentioning.

Undo the test changes:

```sql
UPDATE students SET marks = 78 WHERE student_id = 101;
UPDATE students SET city  = 'Chennai' WHERE student_id = 102;
DELETE FROM audit_log;
```

---

# 15. A BEFORE Trigger — Validation

A `BEFORE` trigger can **reject** a change by raising an error.

```sql
DELIMITER $$
CREATE TRIGGER guard_marks
BEFORE INSERT ON students
FOR EACH ROW
BEGIN
    IF NEW.marks > 100 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Marks cannot exceed 100';
    END IF;
END$$
DELIMITER ;
```

### Test It

```sql
INSERT INTO students VALUES (301,'Bad Marks','Delhi',1,150,'2025-06-01');
```

### Error

```text
ERROR 1644 (45000): Marks cannot exceed 100
```

The row was never inserted.

> **Note:** A `CHECK` constraint (Day 2) does this job better and more cheaply.
> Use a trigger only when the rule needs **other tables**, or has to write an
> audit row — things a constraint cannot do.

---

# 16. Listing and Removing Triggers

```sql
SHOW TRIGGERS;
DROP TRIGGER IF EXISTS log_delete;
```

### Sample Output

```
+-------------+--------+----------+--------+
| Trigger     | Event  | Table    | Timing |
+-------------+--------+----------+--------+
| guard_marks | INSERT | students | BEFORE |
| log_delete  | DELETE | students | AFTER  |
| log_update  | UPDATE | students | AFTER  |
+-------------+--------+----------+--------+
```

---

# 17. Uses and Dangers of Triggers

| Use              | Example                                    |
| ---------------- | ------------------------------------------ |
| **Auditing**     | Record who changed what, and when          |
| **Validation**   | Reject an impossible value                 |
| **Derived data** | Keep a running total up to date            |
| **History**      | Copy the old row into an archive table     |

> ⚠️ **Use triggers sparingly.** They run **invisibly**. Nothing in your
> application code mentions them, so a slow or buggy trigger is very hard to
> track down. If a colleague asks "why did this row change?", a trigger is the
> last place anyone looks.

---

# Common Errors

## Error 1: Forgetting DELIMITER

```sql
CREATE PROCEDURE demo2()
BEGIN
    SELECT 'first';
    SELECT 'second';
END;
```

### Error

```text
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that
corresponds to your MySQL server version for the right syntax to use near '' at
line 3
```

### Reason

The client stopped at the **first** semicolon, inside `BEGIN`, so MySQL received
an incomplete `CREATE PROCEDURE`.

### Solution

Wrap it with `DELIMITER $$ ... END$$ DELIMITER ;`

---

## Error 2: DECLARE Not at the Top

```sql
DELIMITER $$
CREATE PROCEDURE bad_order()
BEGIN
    SELECT 'hello';
    DECLARE v INT;
END$$
DELIMITER ;
```

### Error

```text
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that
corresponds to your MySQL server version for the right syntax to use near
'DECLARE v INT;
END' at line 4
```

### Solution

Move every `DECLARE` to the top of the block, before any other statement.

---

## Error 3: Procedure Already Exists

```sql
CREATE PROCEDURE city_report(IN p_city VARCHAR(50)) ...
```

### Error

```text
ERROR 1304 (42000): PROCEDURE city_report already exists
```

### Reason

There is no `CREATE OR REPLACE PROCEDURE` in MySQL.

### Solution

```sql
DROP PROCEDURE IF EXISTS city_report;
```

then create it again. Put the `DROP` at the top of your script so it can be
re-run.

---

## Error 4: Using a Function to Change Data

A function cannot perform an `INSERT`, `UPDATE` or `DELETE` on the table it is
called from, and cannot return a result set. If you need that, write a
**procedure**.

---

## Error 5: AFTER UPDATE OF column

```sql
CREATE TRIGGER log_update AFTER UPDATE OF marks ON students FOR EACH ROW ...
```

### Error

```text
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that
corresponds to your MySQL server version for the right syntax to use near
'OF marks ON students FOR EACH ROW ...'
```

### Reason

MySQL has no column-specific update trigger.

### Solution

Fire on all updates and test inside — see section 14.

---

# Commands Covered

| Command                                    | Purpose                        |
| ------------------------------------------ | ------------------------------ |
| `DELIMITER $$` … `DELIMITER ;`             | Lets a body contain semicolons |
| `CREATE PROCEDURE name(IN/OUT/INOUT ...)`  | Creates a procedure            |
| `CALL name(...)`                           | Runs a procedure               |
| `DECLARE v datatype DEFAULT x`             | Declares a variable            |
| `SET v = value`                            | Assigns a variable             |
| `SELECT ... INTO v1, v2`                   | Puts query results in variables |
| `IF / ELSEIF / ELSE / END IF`              | Branching                      |
| `WHILE / REPEAT / LOOP`                    | Looping                        |
| `CREATE FUNCTION ... RETURNS ... RETURN`   | Creates a function             |
| `DECLARE ... HANDLER FOR SQLEXCEPTION`     | Catches errors                 |
| `SIGNAL SQLSTATE '45000'`                  | Raises your own error          |
| `CREATE TRIGGER ... BEFORE/AFTER ... FOR EACH ROW` | Creates a trigger      |
| `OLD.column` / `NEW.column`                | Values before / after          |
| `SHOW PROCEDURE STATUS` / `SHOW TRIGGERS`  | Lists them                     |
| `DROP PROCEDURE / FUNCTION / TRIGGER`      | Removes them                   |

---

# Summary

* **Stored programs** add variables, branching, loops and error handling to SQL,
  and run inside the database.
* **`DELIMITER`** is required because a program body contains semicolons.
* A **procedure** does something and is called with `CALL`. A **function**
  returns a value and can be used inside `SELECT`.
* All `DECLARE` statements must come **first** in a block.
* `SET` assigns; `SELECT ... INTO` fills variables from a query.
* **Handlers** catch errors; **`SIGNAL`** raises them.
* A **trigger** runs automatically on `INSERT`, `UPDATE` or `DELETE`, using
  `OLD` and `NEW`.
* MySQL has **no** `UPDATE OF column` — filter with an `IF` inside instead.
* Triggers are invisible. Use them for auditing, not for business logic.

---

# Practice Questions

1. Write a procedure that lists all students of a given course id.
2. Write a procedure with an `OUT` parameter returning the highest marks.
3. Write a procedure that prints `Strong`, `Average` or `Weak` based on the class
   average.
4. Write a `WHILE` loop procedure that lists the numbers 1 to 10.
5. Rewrite question 4 using `REPEAT`.
6. Write a function `is_pass(marks)` returning `Yes` or `No`.
7. Use that function inside a `SELECT` on the students table.
8. Give three differences between a procedure and a function.
9. Why can a procedure not be used inside a `SELECT`?
10. Write a procedure that catches a duplicate-key error and prints a message.
11. Write a procedure that rejects an age below 18 using `SIGNAL`.
12. Create an `audit_log` table and a trigger recording every deleted student.
13. Delete a student and check the log.
14. Write a trigger that logs the old and new marks whenever marks change.
15. Why does that trigger need an `IF` instead of `AFTER UPDATE OF marks`?
16. Which of `OLD` and `NEW` exists for `INSERT`, `UPDATE` and `DELETE`?
17. List all procedures, functions and triggers in the database.
18. Give one good use and one danger of triggers.

---

# Class Summary

In this notebook, you learned:

* Why code is sometimes stored inside the database
* Using `DELIMITER` so a program body can contain semicolons
* Writing **stored procedures** with `IN`, `OUT` and `INOUT` parameters
* Declaring variables, and filling them with `SET` and `SELECT ... INTO`
* Branching with `IF / ELSEIF / ELSE`
* The three loops: `WHILE`, `REPEAT` and `LOOP`
* Writing **stored functions** and using them inside a `SELECT`
* The difference between a procedure and a function
* Catching errors with `DECLARE ... HANDLER`
* Raising your own errors with `SIGNAL`
* Writing **triggers** for `INSERT`, `UPDATE` and `DELETE`
* Using `OLD` and `NEW`, and which one exists for each event
* Why MySQL needs an `IF` instead of `AFTER UPDATE OF column`
* Listing and dropping stored programs and triggers

You are now ready to learn the next topic: **Revision and Interview Preparation**.
