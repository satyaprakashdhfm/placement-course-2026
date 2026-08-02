# Day 17 · Stored Programs (PL/SQL Fundamentals)

**Duration:** 50–60 Minutes  ·  **Fully hands-on in MySQL**

### Learning Outcomes
- Write a **block** with variables, `IF` and loops.
- Create **stored procedures** and **stored functions**, and tell them apart.
- Handle errors with **`DECLARE … HANDLER`**.
- Write **triggers** using `OLD` and `NEW`.

> 📌 **Naming.** Oracle calls this **PL/SQL**. MySQL calls it **stored
> programs**, SQL Server calls it **T-SQL**, PostgreSQL calls it **PL/pgSQL**.
> Same idea, different dialect. **SQLite has none of it** — only triggers.

---

## 1. Why Put Code in the Database?

Plain SQL is **declarative** — one statement, one result. It has no variables,
no `if`, no loops. Stored programs add them:

| SQL alone | SQL + stored programs |
|---|---|
| One statement at a time | Many statements as one program |
| No variables | Variables and constants |
| No branching | `IF` / `CASE` |
| No loops | `LOOP`, `WHILE`, `REPEAT` |
| Errors stop you | Error handlers |
| Runs from your app | Runs **inside** the database |

| Benefit | Explanation |
|---|---|
| **Less network traffic** | Send one call, not 100 statements |
| **Reuse** | Every application shares the same logic |
| **Security** | Grant access to the procedure, not the tables |
| **Speed** | Parsed once, stored ready to run |

---

## 2. DELIMITER — Read This First

A stored program **contains** semicolons. The client would stop at the first
one, so you temporarily change the statement terminator:

```sql
DELIMITER $$

CREATE PROCEDURE demo()
BEGIN
    SELECT 'first';
    SELECT 'second';
END$$

DELIMITER ;
```

**Key Note:** forgetting `DELIMITER` is the #1 error on this topic. The symptom
is a syntax error pointing at the *first* line inside `BEGIN`.

📌 Oracle uses a lone `/` on its own line instead. PostgreSQL wraps the body in
`$$ … $$` quotes.

---

## 3. Variables, IF and Loops

```sql
DELIMITER $$
CREATE PROCEDURE grade_report()
BEGIN
    DECLARE v_count INT DEFAULT 0;
    DECLARE v_avg   DECIMAL(5,2);
    DECLARE v_label VARCHAR(20);

    SELECT COUNT(*), AVG(marks) INTO v_count, v_avg FROM students;

    IF v_avg >= 75 THEN       SET v_label = 'Strong batch';
    ELSEIF v_avg >= 50 THEN   SET v_label = 'Average batch';
    ELSE                      SET v_label = 'Weak batch';
    END IF;

    SELECT v_count AS students, ROUND(v_avg,2) AS avg_marks, v_label AS verdict;
END$$
DELIMITER ;

CALL grade_report();
```

```text
+----------+-----------+---------------+
| students | avg_marks | verdict       |
+----------+-----------+---------------+
|       10 |     69.44 | Average batch |
+----------+-----------+---------------+
```

**Key Notes:**
- All `DECLARE`s must come **first**, before any other statement.
- `SET` assigns. `SELECT … INTO v` puts a query result into a variable.
- `ELSEIF` is one word. Every `IF` ends with `END IF;`.

📌 Oracle uses `:=` to assign and needs a `DECLARE` *section* before `BEGIN`.
MySQL declares **inside** `BEGIN` and uses `SET`.

### The three loops

```sql
WHILE i <= 5 DO          -- test first
    SET i = i + 1;
END WHILE;

REPEAT                   -- test last, always runs once
    SET i = i + 1;
UNTIL i > 5 END REPEAT;

my_loop: LOOP            -- you must leave it yourself
    SET i = i + 1;
    IF i > 5 THEN LEAVE my_loop; END IF;
END LOOP;
```

A working `WHILE`:

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

```text
+-------------+
| loop_output |
+-------------+
| 1,2,3,4,5   |
+-------------+
```

---

## 4. Stored Procedures

A **procedure** performs an action. Call it with `CALL`.

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

CALL city_report('Hyderabad');
```

```text
+-------------+-------+
| name        | marks |
+-------------+-------+
| Vikram Rao  |    81 |
| Rahul Verma |    78 |
| Karan Patel |    38 |
+-------------+-------+
```

### Parameter modes

| Mode | Meaning |
|---|---|
| `IN` | given to the procedure (default) |
| `OUT` | sent back to the caller |
| `INOUT` | both |

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

```text
+------------------+
| chennai_students |
+------------------+
|                3 |
+------------------+
```

`@n` is a **session variable** — it lives until you disconnect.

---

## 5. Stored Functions

A **function** must return a value, and can be used **inside a `SELECT`**.

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

```text
+--------------+-------+-------------+
| name         | marks | grade       |
+--------------+-------+-------------+
| Rahul Verma  |    78 | Distinction |
| Anita Sharma |    95 | Distinction |
| Karan Patel  |    38 | Fail        |
| Priya Nair   |    66 | Pass        |
+--------------+-------+-------------+
```

**Key Note:** `DETERMINISTIC` promises the same input always gives the same
output. Without it (or `READS SQL DATA`) MySQL may refuse to create the function
when binary logging is on.

### Procedure vs Function — a guaranteed interview question

| | Procedure | Function |
|---|---|---|
| Returns a value | optional, via `OUT` | **compulsory** (`RETURNS`) |
| Called with | `CALL name(...)` | inside an expression |
| Usable in `SELECT` | ❌ no | ✅ **yes** |
| Can return a result set | ✅ yes | ❌ no |
| Purpose | **do** something | **calculate** something |

---

## 6. Error Handling

MySQL uses **handlers** declared up front, rather than a block at the end:

```sql
DELIMITER $$
CREATE PROCEDURE safe_insert(IN p_id INT, IN p_name VARCHAR(50))
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
        SELECT 'Insert failed - id already exists' AS message;

    INSERT INTO students (id, name) VALUES (p_id, p_name);
    SELECT 'Inserted' AS message;
END$$
DELIMITER ;

CALL safe_insert(101, 'Clash');
```

```text
+-----------------------------------+
| message                           |
+-----------------------------------+
| Insert failed - id already exists |
+-----------------------------------+
```

No error reached the user — the handler caught it.

| Handler | Meaning |
|---|---|
| `EXIT HANDLER` | run it, then leave the block |
| `CONTINUE HANDLER` | run it, then carry on |
| `FOR SQLEXCEPTION` | any error |
| `FOR NOT FOUND` | a `SELECT INTO` found nothing |
| `FOR SQLSTATE '23000'` | one specific error (here, duplicate key) |

📌 Oracle writes this as an `EXCEPTION WHEN … THEN` block at the **end**, with
named exceptions like `NO_DATA_FOUND` and `DUP_VAL_ON_INDEX`. Same purpose,
different shape.

---

## 7. Triggers

A **trigger** fires **automatically** when data changes. This is the one part
of today that also exists in SQLite.

```sql
CREATE TABLE audit_log (
    action    VARCHAR(60),
    student   VARCHAR(50),
    logged_at DATETIME
);

DELIMITER $$
CREATE TRIGGER log_marks_change
AFTER UPDATE ON students
FOR EACH ROW
BEGIN
    INSERT INTO audit_log
    VALUES (CONCAT('UPDATE ', OLD.marks, ' -> ', NEW.marks), NEW.name, NOW());
END$$
DELIMITER ;

UPDATE students SET marks = 85 WHERE id = 101;
SELECT action, student FROM audit_log;
```

```text
+-----------------+-------------+
| action          | student     |
+-----------------+-------------+
| UPDATE 78 -> 85 | Rahul Verma |
+-----------------+-------------+
```

Nobody wrote to `audit_log` — the trigger did.

### OLD and NEW

| Event | `OLD` | `NEW` |
|---|---|---|
| `INSERT` | ❌ | ✅ the incoming row |
| `UPDATE` | ✅ before | ✅ after |
| `DELETE` | ✅ the row going | ❌ |

### Timing

`BEFORE` or `AFTER`, on `INSERT`, `UPDATE` or `DELETE` — six combinations.
Use `BEFORE` to **change or reject** the incoming value, `AFTER` to **record**
what happened.

```sql
DELIMITER $$
CREATE TRIGGER tidy_name
BEFORE INSERT ON students
FOR EACH ROW
BEGIN
    SET NEW.name = TRIM(NEW.name);
END$$
DELIMITER ;
```

| Use | Example |
|---|---|
| **Auditing** | Record who changed what, and when |
| **Validation** | Reject an impossible value |
| **Derived data** | Keep a running total up to date |
| **Cleaning** | Trim spaces before storing |

> ⚠️ **Use triggers sparingly.** They run invisibly. A slow or buggy trigger is
> very hard to debug, because nothing in your code mentions it.

📌 MySQL is always `FOR EACH ROW`. Oracle also has statement-level triggers.
SQLite supports triggers but has no procedures or functions at all.

---

## 8. Managing Stored Programs

| Command | Does |
|---|---|
| `SHOW PROCEDURE STATUS WHERE Db='training';` | list procedures |
| `SHOW FUNCTION STATUS WHERE Db='training';` | list functions |
| `SHOW TRIGGERS;` | list triggers |
| `SHOW CREATE PROCEDURE city_report;` | see the source |
| `DROP PROCEDURE IF EXISTS city_report;` | remove it |
| `DROP TRIGGER IF EXISTS log_marks_change;` | remove it |

**Key Note:** MySQL has no `CREATE OR REPLACE PROCEDURE`. You must `DROP` first
— which is why every example above should really start with
`DROP PROCEDURE IF EXISTS …`.

---

## 9. Common Mistakes

**1. Forgetting `DELIMITER`** — syntax error at the first inner `;`.

**2. `DECLARE` after another statement** — all declarations come first.

**3. Expecting `CREATE OR REPLACE`** — not supported for procedures in MySQL.

**4. Missing `DETERMINISTIC` on a function** — creation may be refused.

**5. Calling a procedure inside `SELECT`** — only functions can do that.

**6. Heavy logic in a trigger** — every row change pays the cost, invisibly.

**7. Assuming this is portable** — stored program syntax is the **least**
portable part of SQL. The concepts move; the code does not.

---

## 10. Summary

- Stored programs add variables, `IF`, loops and error handling, and run
  **inside** the database.
- **`DELIMITER $$`** is required so the client does not stop at the first `;`.
- `DECLARE` first, `SET` to assign, `SELECT … INTO` to capture a result.
- Loops: `WHILE`, `REPEAT`, `LOOP` + `LEAVE`.
- **Procedure** = does something, `CALL` it, can have `OUT` parameters.
  **Function** = returns one value, usable **inside `SELECT`**.
- Errors are caught with `DECLARE EXIT HANDLER FOR SQLEXCEPTION`.
- **Triggers** fire on `INSERT`/`UPDATE`/`DELETE` with `OLD` and `NEW`;
  `BEFORE` to change, `AFTER` to record.
- 📌 Oracle = PL/SQL, MySQL = stored programs, PostgreSQL = PL/pgSQL,
  **SQLite = triggers only**.

---

## 11. 🔺 ADVANCED — Teacher Reference

### 11.1 `SIGNAL` — raising your own errors

Handlers *catch* errors; `SIGNAL` *throws* them. This is how a procedure
enforces a business rule and makes the caller deal with it.

```sql
DELIMITER $$
CREATE PROCEDURE risky(IN p_marks INT)
BEGIN
    IF p_marks > 100 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Marks cannot exceed 100';
    END IF;
    SELECT CONCAT('accepted ', p_marks) AS result;
END$$
DELIMITER ;

CALL risky(50);
```
```text
+-------------+
| result      |
+-------------+
| accepted 50 |
+-------------+
```

```sql
CALL risky(150);
```
```text
ERROR 1644 (45000): Marks cannot exceed 100
```

`45000` is the SQLSTATE reserved for "unhandled user-defined exception" — use it
unless you have a reason not to. `RESIGNAL` re-throws inside a handler after
logging.

### 11.2 Cursors — row-by-row processing

When you truly must walk a result set one row at a time:

```sql
DELIMITER $$
CREATE PROCEDURE grade_everyone()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE v_id INT;
    DECLARE v_marks INT;
    DECLARE cur CURSOR FOR SELECT id, marks FROM students WHERE marks IS NOT NULL;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    OPEN cur;
    read_loop: LOOP
        FETCH cur INTO v_id, v_marks;
        IF done THEN LEAVE read_loop; END IF;
        -- per-row work here
    END LOOP;
    CLOSE cur;
END$$
DELIMITER ;
```

**The shape:** `DECLARE cursor` → `DECLARE CONTINUE HANDLER FOR NOT FOUND` →
`OPEN` → `LOOP`/`FETCH`/`LEAVE` → `CLOSE`. The handler is what tells you the
rows ran out; forgetting it gives an infinite loop.

> ⚠️ **Teach cursors, then teach not to use them.** A cursor processes N rows in
> N round trips; a single `UPDATE ... JOIN` does the same work in one pass,
> often hundreds of times faster. Cursors are for when each row needs genuinely
> different, non-set-based work.

### 11.3 Dynamic SQL — `PREPARE` / `EXECUTE`

For when the table or column name is not known until run time.

```sql
DELIMITER $$
CREATE PROCEDURE find_by(IN col VARCHAR(20), IN val VARCHAR(50))
BEGIN
    SET @s = CONCAT('SELECT name, ', col, ' FROM students WHERE ', col, ' = ? LIMIT 3');
    PREPARE stmt FROM @s;
    SET @v = val;
    EXECUTE stmt USING @v;
    DEALLOCATE PREPARE stmt;
END$$
DELIMITER ;

CALL find_by('city', 'Pune');
```
```text
+-------------+------+
| name        | city |
+-------------+------+
| Rohit Sinha | Pune |
| Arjun Mehta | Pune |
+-------------+------+
```

⚠️ **SQL injection lives here.** The *value* is passed safely with `?` and
`USING`. The *column name* cannot be — it is concatenated straight into the
string. Whitelist identifiers against `information_schema.columns`; never accept
them from a user.

### 11.4 Events — MySQL's built-in scheduler

Cron, inside the database. Ideal for refreshing the hand-rolled materialised
view from Day 16 §8.7.

```sql
SET GLOBAL event_scheduler = ON;

CREATE EVENT refresh_city_stats
ON SCHEDULE EVERY 1 HOUR
DO
    REPLACE INTO mv_city_stats
    SELECT city, COUNT(*), AVG(marks) FROM students GROUP BY city;
```

```sql
SHOW EVENTS;
SHOW VARIABLES LIKE 'event_scheduler';
```

⚠️ The scheduler is **off by default**, and events do not run on a replica.
Check `event_scheduler` first when "my event never fired".

### 11.5 Transactions inside stored programs

A procedure can manage its own transaction:

```sql
DELIMITER $$
CREATE PROCEDURE transfer(IN p_from INT, IN p_to INT, IN p_amt DECIMAL(10,2))
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;
        UPDATE accounts SET balance = balance - p_amt WHERE id = p_from;
        UPDATE accounts SET balance = balance + p_amt WHERE id = p_to;
    COMMIT;
END$$
DELIMITER ;
```

**The pattern to memorise:** an `EXIT HANDLER` that does `ROLLBACK` then
`RESIGNAL` — undo the work, but still tell the caller it failed. Swallowing the
error is how data silently goes missing.

⚠️ **DDL causes an implicit commit.** A `CREATE TABLE` or `ALTER` inside a
transaction commits everything before it, so you cannot roll it back. Never mix
DDL into a transactional procedure.

### 11.6 When *not* to put logic in the database

Say this out loud, because the day is otherwise one-sided:

| Against | Why |
|---|---|
| Hard to version-control | procedure bodies live in the DB, not naturally in git |
| Hard to test | no unit-test framework worth the name |
| Hard to debug | no breakpoints, no stack traces |
| **Least portable SQL there is** | rewriting for another engine means rewriting all of it |
| Scales badly | database CPU is the most expensive CPU you own |

**Modern practice:** keep *data integrity* in the database (constraints, a few
triggers) and *business logic* in the application. Stored procedures remain
common in banking, ERP and legacy systems — which is exactly why you must be
able to read them.

---

## 11. Practice Questions

1. Why must you change the `DELIMITER`?
2. Write a procedure that prints how many students are in a given city.
3. Add an `OUT` parameter returning that count instead of selecting it.
4. Write a function `is_pass(marks)` returning `'Yes'` or `'No'`, and use it in
   a `SELECT`.
5. Give three differences between a procedure and a function.
6. Why can a procedure not be used inside a `SELECT`?
7. Write a `WHILE` loop that inserts the numbers 1 to 10 into a temp table.
8. Rewrite it as a `REPEAT` loop.
9. Write a procedure that inserts a student and handles a duplicate id
   gracefully.
10. Create an audit trigger recording every deleted student.
11. Create a `BEFORE INSERT` trigger that upper-cases the city.
12. Which of `OLD` and `NEW` exists for `INSERT`, `UPDATE` and `DELETE`?
13. When would you use `BEFORE` rather than `AFTER`?
14. List your procedures, then drop one.
15. Name the equivalent of stored procedures in Oracle, PostgreSQL and SQLite.
