# Day 17 · PL/SQL Fundamentals

**Duration:** 50–60 Minutes  ·  **Mostly theory — read §1 first**

---

## ⚠️ 1. Read This Before The Class

**SQLite has no procedural language.** Five of today's six topics **cannot be
run** in DB Browser:

| Topic | SQLite | What we do |
|---|---|---|
| Blocks (`DECLARE … BEGIN … END`) | ❌ syntax error | theory + Oracle/MySQL syntax |
| Variables | ❌ | theory |
| Loops (`LOOP`, `FOR`, `WHILE`) | ❌ | theory |
| Stored procedures | ❌ | theory |
| Stored functions | ❌ | theory |
| **Triggers** | ✅ **works** | **hands-on** |

```sql
CREATE PROCEDURE greet() BEGIN SELECT 'hi'; END;
```
```text
Error: near "PROCEDURE": syntax error
```

```sql
DECLARE v_count INT;
```
```text
Error: near "DECLARE": syntax error
```

So today is a **theory class with one practical section**. You must be able to
**read and write** PL/SQL for interviews and for any job using Oracle or MySQL —
you simply cannot execute it here. Everything else in this course you have run
yourself; be honest with yourself that this part is learned from the page.

---

## 2. What is PL/SQL?

**PL/SQL** = **P**rocedural **L**anguage extension to **SQL** (Oracle's name;
MySQL calls its version *stored programs*, SQL Server calls it *T-SQL*).

Plain SQL is **declarative** — one statement, one result. It has no variables,
no `if`, no loops. PL/SQL adds them:

| SQL alone | SQL + PL/SQL |
|---|---|
| One statement at a time | Many statements as one program |
| No variables | Variables and constants |
| No branching | `IF` / `CASE` |
| No loops | `LOOP`, `WHILE`, `FOR` |
| Errors stop you | `EXCEPTION` handling |
| Runs from your app | Runs **inside** the database |

**Why put code in the database?**

| Benefit | Explanation |
|---|---|
| **Less network traffic** | Send one call, not 100 statements |
| **Reuse** | Every application shares the same logic |
| **Security** | Grant access to the procedure, not the tables |
| **Speed** | Compiled once, stored ready to run |

---

## 3. The Block Structure

Every PL/SQL program is a **block** with up to three parts:

```sql
DECLARE                        -- optional: variables
    v_count   NUMBER;
    v_name    VARCHAR2(50);
BEGIN                          -- required: the code
    SELECT COUNT(*) INTO v_count FROM students;
    DBMS_OUTPUT.PUT_LINE('Students: ' || v_count);
EXCEPTION                      -- optional: what to do when it fails
    WHEN NO_DATA_FOUND THEN
        DBMS_OUTPUT.PUT_LINE('Nothing found');
END;
/
```

| Part | Required? | Purpose |
|---|---|---|
| `DECLARE` | optional | declare variables |
| `BEGIN … END` | **required** | the statements |
| `EXCEPTION` | optional | handle errors |

A block with no name like the one above is an **anonymous block** — it runs
once and is not stored.

---

## 4. Variables

```sql
DECLARE
    v_marks     NUMBER := 75;                      -- with a starting value
    v_name      VARCHAR2(50);
    c_pass_mark CONSTANT NUMBER := 40;             -- cannot be changed
    v_city      students.city%TYPE;                -- same type as that column
BEGIN
    v_name := 'Rahul';                             -- := is assignment
    SELECT city INTO v_city FROM students WHERE id = 101;
END;
/
```

**Key Notes:**
- `:=` assigns, `=` compares — the opposite of most languages.
- `%TYPE` copies a column's type. If the column changes later, your code still
  matches.
- `SELECT … INTO v` puts a query result into a variable. It **must** return
  exactly one row, or you get `NO_DATA_FOUND` / `TOO_MANY_ROWS`.

---

## 5. Conditions

```sql
IF v_marks >= 75 THEN
    v_grade := 'Distinction';
ELSIF v_marks >= 50 THEN
    v_grade := 'Pass';
ELSE
    v_grade := 'Fail';
END IF;
```

Note the spellings: **`ELSIF`** (not `elseif` or `elif`), and every `IF` is
closed by **`END IF;`**.

---

## 6. Loops

```sql
-- 1. Basic loop - you must exit yourself
LOOP
    v_i := v_i + 1;
    EXIT WHEN v_i > 5;
END LOOP;

-- 2. WHILE loop - test first
WHILE v_i <= 5 LOOP
    v_i := v_i + 1;
END LOOP;

-- 3. FOR loop - counter is created for you
FOR i IN 1..5 LOOP
    DBMS_OUTPUT.PUT_LINE(i);
END LOOP;

-- 4. Cursor FOR loop - walk through query results
FOR rec IN (SELECT name, marks FROM students) LOOP
    DBMS_OUTPUT.PUT_LINE(rec.name || ' scored ' || rec.marks);
END LOOP;
```

The **cursor FOR loop** is the one that matters — it is how PL/SQL processes a
result set row by row, and the reason procedural SQL exists.

---

## 7. Procedures and Functions

### Procedure — performs an action

```sql
CREATE OR REPLACE PROCEDURE add_student (
    p_id     IN NUMBER,
    p_name   IN VARCHAR2,
    p_marks  IN NUMBER
) AS
BEGIN
    INSERT INTO students (id, name, marks) VALUES (p_id, p_name, p_marks);
    COMMIT;
END;
/

EXEC add_student(201, 'New Student', 65);
```

### Function — calculates and **returns** a value

```sql
CREATE OR REPLACE FUNCTION get_grade (p_marks IN NUMBER)
RETURN VARCHAR2 AS
    v_grade VARCHAR2(20);
BEGIN
    IF    p_marks >= 75 THEN v_grade := 'Distinction';
    ELSIF p_marks >= 50 THEN v_grade := 'Pass';
    ELSE                     v_grade := 'Fail';
    END IF;
    RETURN v_grade;
END;
/

SELECT name, marks, get_grade(marks) FROM students;
```

### The difference — a guaranteed interview question

| | Procedure | Function |
|---|---|---|
| Returns a value | optional (via `OUT`) | **compulsory** (`RETURN`) |
| Called with | `EXEC name(...)` | inside an expression |
| Usable in `SELECT` | ❌ no | ✅ **yes** |
| Purpose | **do** something | **calculate** something |

**Parameter modes:** `IN` (given to it, default), `OUT` (sent back),
`IN OUT` (both).

---

## 8. Triggers — The Part You Can Actually Run

A **trigger** is code that fires **automatically** when data changes. SQLite
supports these, so this section is hands-on.

```sql
CREATE TABLE audit_log (
    action     TEXT,
    student    TEXT,
    logged_at  TEXT
);

CREATE TRIGGER log_deleted_student
AFTER DELETE ON students
BEGIN
    INSERT INTO audit_log VALUES ('DELETE', OLD.name, DATETIME('now'));
END;
```

Now delete somebody and check the log:

```sql
DELETE FROM students WHERE id = 110;
SELECT action, student FROM audit_log;
```

```text
action | student
-------+------------
DELETE | Meera Nair
```

Nobody wrote to `audit_log` — the trigger did.

### OLD and NEW

| Event | `OLD` available | `NEW` available |
|---|---|---|
| `INSERT` | ❌ | ✅ the incoming row |
| `UPDATE` | ✅ before | ✅ after |
| `DELETE` | ✅ the row going | ❌ |

```sql
CREATE TRIGGER log_marks_change
AFTER UPDATE OF marks ON students
BEGIN
    INSERT INTO audit_log
    VALUES ('UPDATE ' || OLD.marks || ' -> ' || NEW.marks, NEW.name, DATETIME('now'));
END;
```

```sql
UPDATE students SET marks = 85 WHERE id = 101;
SELECT action, student FROM audit_log;
```

```text
action            | student
------------------+------------
UPDATE 78 -> 85   | Rahul Verma
```

### Uses for triggers

| Use | Example |
|---|---|
| **Auditing** | Record who changed what, and when |
| **Validation** | Reject an impossible value |
| **Derived data** | Keep a running total up to date |
| **History** | Copy the old row into an archive table |

> ⚠️ **Use triggers sparingly.** They run invisibly. A slow or buggy trigger is
> very hard to debug, because nothing in your code mentions it.

**Key Note:** SQLite supports `BEFORE` / `AFTER` / `INSTEAD OF` triggers on
`INSERT`, `UPDATE`, `DELETE` — but **not** Oracle's `FOR EACH STATEMENT`
(SQLite is always `FOR EACH ROW`).

---

## 9. Exception Handling

```sql
BEGIN
    SELECT name INTO v_name FROM students WHERE id = 999;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        DBMS_OUTPUT.PUT_LINE('No such student');
    WHEN TOO_MANY_ROWS THEN
        DBMS_OUTPUT.PUT_LINE('More than one match');
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error: ' || SQLERRM);
END;
/
```

| Exception | Raised when |
|---|---|
| `NO_DATA_FOUND` | `SELECT INTO` found nothing |
| `TOO_MANY_ROWS` | `SELECT INTO` found more than one row |
| `ZERO_DIVIDE` | division by zero |
| `DUP_VAL_ON_INDEX` | duplicate on a unique column |
| `OTHERS` | anything else — always put it **last** |

If this looks like Python's `try` / `except`, that is because it is the same
idea with different words.

---

## 10. Summary

- **PL/SQL adds procedural features to SQL**: variables, `IF`, loops,
  exceptions — and runs **inside** the database.
- Structure: `DECLARE` (optional) → `BEGIN … END` (required) → `EXCEPTION`
  (optional).
- `:=` assigns, `=` compares. `%TYPE` borrows a column's type.
- Four loops; the **cursor FOR loop** walks a result set.
- **Procedure** = does something, called with `EXEC`.
  **Function** = returns something, usable inside `SELECT`.
- **Triggers** run automatically on `INSERT` / `UPDATE` / `DELETE`, using
  `OLD` and `NEW`. **These do work in SQLite.**
- Exceptions are SQL's `try` / `except`; `WHEN OTHERS` goes last.
- ⚠️ Everything except triggers is **theory only** in this course.

---

## 11. Practice Questions

**Written (no computer):**

1. What does PL/SQL add that plain SQL does not have?
2. Name the three parts of a block and say which is compulsory.
3. What is the difference between `:=` and `=`?
4. What does `students.city%TYPE` mean and why use it?
5. Write a block that stores the student count in a variable and prints it.
6. Write an `IF / ELSIF / ELSE` that grades a mark.
7. Write a `FOR` loop printing 1 to 10.
8. Write a cursor `FOR` loop printing every student's name.
9. Give three differences between a procedure and a function.
10. Which one can be used inside a `SELECT`, and why can the other not be?
11. What are the three parameter modes?
12. When is `NO_DATA_FOUND` raised?
13. Why must `WHEN OTHERS` be last?

**Hands-on in DB Browser:**

14. Create an `audit_log` table and a trigger recording every deleted student.
15. Delete a student and check the log.
16. Write a trigger recording the old and new marks on every `UPDATE`.
17. Which of `OLD` and `NEW` exists for `INSERT`, `UPDATE` and `DELETE`?
18. Give one good reason and one danger of using triggers.
