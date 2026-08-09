# MySQL - Database and Table Basics

In this section, we will learn how to create a database, select a database, and view the available databases before creating tables.

---

# What is a Database?

A **database** is an organized collection of related data.

Some important points:

* A database can contain one or more tables.
* It helps store, organize, and manage data efficiently.
* Before creating a table, a database must exist.
* In MySQL, each table belongs to a database.

---

# Create a Database

The `CREATE DATABASE` command creates a new database.

### Syntax

```sql
CREATE DATABASE database_name;
```

### Example

```sql
CREATE DATABASE training;
```

### Expected Output

```
Query OK, 1 row affected
```

---

# Create a Database Only If It Does Not Exist

If the database already exists, MySQL normally throws an error.

To avoid this, use the `IF NOT EXISTS` clause.

### Syntax

```sql
CREATE DATABASE IF NOT EXISTS database_name;
```

### Example

```sql
CREATE DATABASE IF NOT EXISTS training;
```

### Expected Output

```
Query OK, 1 row affected
```

or

```
Query OK, 0 rows affected
```

---

# View All Databases

The `SHOW DATABASES` command displays all databases available on the MySQL server.

### Syntax

```sql
SHOW DATABASES;
```

### Example

```sql
SHOW DATABASES;
```

### Sample Output

```
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
| training           |
+--------------------+
```

---

# Select a Database

Before creating tables, MySQL must know which database you want to work with.

The `USE` command selects the database for the current session.

### Syntax

```sql
USE database_name;
```

### Example

```sql
USE training;
```

### Expected Output

```
Database changed
```

---

# Check the Currently Selected Database

Use the following command to verify which database is currently selected.

### Syntax

```sql
SELECT DATABASE();
```

### Example

```sql
SELECT DATABASE();
```

### Sample Output

```
+------------+
| DATABASE() |
+------------+
| training   |
+------------+
```

---

# Delete a Database

The `DROP DATABASE` command permanently deletes a database and everything inside it.

**Note:** This operation cannot be undone.

### Syntax

```sql
DROP DATABASE database_name;
```

### Example

```sql
DROP DATABASE training;
```

---

# Delete a Database Only If It Exists

Using `IF EXISTS` prevents an error if the database is not present.

### Syntax

```sql
DROP DATABASE IF EXISTS database_name;
```

### Example

```sql
DROP DATABASE IF EXISTS training;
```

---

# Common Errors

### Error 1: Database Already Exists

```
ERROR 1007 (HY000): Can't create database 'training'; database exists
```

**Solution**

```sql
CREATE DATABASE IF NOT EXISTS training;
```

---

### Error 2: Unknown Database

```
ERROR 1049 (42000): Unknown database 'training'
```

**Solution**

Check the available databases.

```sql
SHOW DATABASES;
```

Then use an existing database.

```sql
USE training;
```

---

# Commands Covered

| Command                         | Purpose                                        |
| ------------------------------- | ---------------------------------------------- |
| `CREATE DATABASE`               | Creates a new database                         |
| `CREATE DATABASE IF NOT EXISTS` | Creates the database only if it does not exist |
| `SHOW DATABASES`                | Displays all databases                         |
| `USE database_name`             | Selects a database                             |
| `SELECT DATABASE()`             | Displays the current database                  |
| `DROP DATABASE`                 | Deletes a database                             |
| `DROP DATABASE IF EXISTS`       | Deletes the database only if it exists         |


# Tables in MySQL

A **table** is used to store related data in the form of **rows** and **columns**.

Some important points:

* Every table belongs to a database.
* A table consists of columns (fields) and rows (records).
* Each column stores a specific type of data.
* Every table should have a unique name within a database.

---

# Table Structure

A table is made up of columns, where each column has:

* A column name
* A data type
* Optional constraints

Example:

| Column Name | Data Type   | Description            |
| ----------- | ----------- | ---------------------- |
| course_id   | INT         | Unique course ID       |
| course_name | VARCHAR(50) | Name of the course     |
| duration    | INT         | Course duration (days) |
| fee         | INT         | Course fee             |

---

# Common MySQL Data Types

The following are the most commonly used MySQL data types.

| Data Type     | Description                    | Example               |
| ------------- | ------------------------------ | --------------------- |
| INT           | Integer values                 | 100                   |
| BIGINT        | Large integer values           | 9999999999            |
| FLOAT         | Decimal numbers                | 89.75                 |
| DOUBLE        | High precision decimal numbers | 12345.6789            |
| DECIMAL(10,2) | Fixed decimal values           | 1999.99               |
| CHAR(n)       | Fixed-length string            | 'A'                   |
| VARCHAR(n)    | Variable-length string         | 'Python'              |
| TEXT          | Large text                     | Description           |
| DATE          | Date                           | '2026-08-05'          |
| TIME          | Time                           | '14:30:00'            |
| DATETIME      | Date and Time                  | '2026-08-05 14:30:00' |
| BOOLEAN       | TRUE or FALSE                  | TRUE                  |

---

# Constraints in MySQL

Constraints are rules applied to columns to maintain data accuracy and integrity.

| Constraint     | Purpose                         | Example          |
| -------------- | ------------------------------- | ---------------- |
| PRIMARY KEY    | Uniquely identifies each record | course_id        |
| NOT NULL       | Prevents NULL values            | course_name      |
| UNIQUE         | Prevents duplicate values       | email            |
| DEFAULT        | Assigns a default value         | fee DEFAULT 5000 |
| CHECK          | Restricts allowed values        | fee > 0          |
| AUTO_INCREMENT | Generates values automatically  | student_id       |
| FOREIGN KEY    | Links two tables                | department_id    |

---

# Sample Table Using Constraints

```sql
CREATE TABLE courses (
    course_id INT PRIMARY KEY,
    course_name VARCHAR(50) NOT NULL,
    duration INT,
    fee INT DEFAULT 5000
);
```

---

# View All Tables

The `SHOW TABLES` command displays all tables present in the selected database.

### Syntax

```sql
SHOW TABLES;
```

### Example

```sql
SHOW TABLES;
```

### Sample Output

```
+------------------+
| Tables_in_training |
+------------------+
| courses          |
| trainers         |
+------------------+
```

---

# Describe a Table

The `DESCRIBE` (or `DESC`) command displays the table structure.

### Syntax

```sql
DESCRIBE table_name;
```

### Example

```sql
DESCRIBE courses;
```

or

```sql
DESC courses;
```

### Sample Output

```
+-------------+-------------+------+-----+---------+-------+
| Field       | Type        | Null | Key | Default | Extra |
+-------------+-------------+------+-----+---------+-------+
| course_id   | int         | NO   | PRI | NULL    |       |
| course_name | varchar(50) | NO   |     | NULL    |       |
| duration    | int         | YES  |     | NULL    |       |
| fee         | int         | YES  |     | 5000    |       |
+-------------+-------------+------+-----+---------+-------+
```

---

# View the CREATE TABLE Statement

This command displays the exact SQL statement used to create the table.

### Syntax

```sql
SHOW CREATE TABLE table_name;
```

### Example

```sql
SHOW CREATE TABLE courses;
```

---

# Common Errors

## Error 1: No Database Selected

```
ERROR 1046 (3D000): No database selected
```

**Solution**

```sql
USE training;
```

---

## Error 2: Table Doesn't Exist

```
ERROR 1146 (42S02): Table 'training.courses' doesn't exist
```

**Solution**

First create the table.

```sql
CREATE TABLE courses (
    course_id INT PRIMARY KEY,
    course_name VARCHAR(50)
);
```

---

# Commands Covered

| Command                         | Purpose                             |
| ------------------------------- | ----------------------------------- |
| `SHOW TABLES;`                  | Displays all tables                 |
| `DESCRIBE table_name;`          | Shows table structure               |
| `DESC table_name;`              | Short form of DESCRIBE              |
| `SHOW CREATE TABLE table_name;` | Displays the CREATE TABLE statement |


# Creating Tables in MySQL

A table is used to store related data in rows and columns. Before creating a table, make sure a database is selected using the `USE` command.

---

# Basic Syntax

```sql
CREATE TABLE table_name (
    column_name datatype constraint,
    column_name datatype constraint,
    ...
);
```

---

# 1. Create a Table

Creates a new table with the specified columns and constraints.

```sql
CREATE TABLE courses (
    course_id INT PRIMARY KEY,
    course_name VARCHAR(50) NOT NULL,
    duration INT,
    fee INT
);
```

### Expected Output

```
Query OK, 0 rows affected
```

---

# 2. Create a Table Only If It Does Not Exist

Use `IF NOT EXISTS` to avoid an error if the table already exists.

```sql
CREATE TABLE IF NOT EXISTS courses (
    course_id INT PRIMARY KEY,
    course_name VARCHAR(50) NOT NULL,
    duration INT,
    fee INT
);
```

### Expected Output

```
Query OK, 0 rows affected
```

or

```
Query OK, 0 rows affected, 1 warning
```

---

# 3. Create a Table from an Existing Table (Structure + Data)

Copies both the table structure and all existing records.

```sql
CREATE TABLE courses_backup AS
SELECT *
FROM courses;
```

### Verify

```sql
SELECT * FROM courses_backup;
```

---

# 4. Create a Table with Structure Only

Copies only the column structure without copying any data.

This is useful when you need another table with the same design but want to insert data later.

```sql
CREATE TABLE courses_empty AS
SELECT *
FROM courses
WHERE 1 = 0;
```

### Verify

```sql
DESC courses_empty;
```

```sql
SELECT * FROM courses_empty;
```

---

# 5. Create a Table with Selected Columns

Copies only specific columns from an existing table.

```sql
CREATE TABLE course_catalog AS
SELECT
    course_id,
    course_name
FROM courses;
```

### Verify

```sql
DESC course_catalog;
```

---

# 6. Create a Table with Selected Rows

Copies only the records that satisfy the given condition.

```sql
CREATE TABLE premium_courses AS
SELECT *
FROM courses
WHERE fee >= 7000;
```

### Verify

```sql
SELECT * FROM premium_courses;
```

---

# 7. Create a Table Using LIKE

The `LIKE` keyword copies the complete table structure.

It copies:

* Column names
* Data types
* Primary Key
* Indexes
* AUTO_INCREMENT

It does **not** copy the data.

```sql
CREATE TABLE courses_clone LIKE courses;
```

### Verify

```sql
DESC courses_clone;
```

---

# 8. Create a Temporary Table

A temporary table exists only during the current database session.

Once the session ends, the table is automatically removed.

```sql
CREATE TEMPORARY TABLE temp_courses (
    course_id INT,
    course_name VARCHAR(50)
);
```

### Verify

```sql
SHOW TABLES;
```

---

# 9. Create a Table with AUTO_INCREMENT

The `AUTO_INCREMENT` attribute automatically generates sequential values.

You do not need to provide the ID while inserting records.

```sql
CREATE TABLE trainers (
    trainer_id INT AUTO_INCREMENT PRIMARY KEY,
    trainer_name VARCHAR(50),
    experience INT
);
```

### Example

```sql
INSERT INTO trainers(trainer_name, experience)
VALUES
('Rahul', 5),
('Anita', 8);
```

### Verify

```sql
SELECT * FROM trainers;
```

---

# Common Errors

## Error 1: Table Already Exists

```
ERROR 1050 (42S01): Table 'courses' already exists
```

### Solution

```sql
CREATE TABLE IF NOT EXISTS courses (
    course_id INT PRIMARY KEY,
    course_name VARCHAR(50)
);
```

---

## Error 2: No Database Selected

```
ERROR 1046 (3D000): No database selected
```

### Solution

```sql
USE training;
```

---

## Error 3: Duplicate Column Name

```
ERROR 1060 (42S21): Duplicate column name 'course_id'
```

### Incorrect

```sql
CREATE TABLE courses (
    course_id INT,
    course_id INT
);
```

### Correct

```sql
CREATE TABLE courses (
    course_id INT,
    course_name VARCHAR(50)
);
```

---

## Error 4: Syntax Error

```
ERROR 1064 (42000): You have an error in your SQL syntax...
```

### Incorrect

```sql
CREATE TABLE courses
course_id INT,
course_name VARCHAR(50);
```

### Correct

```sql
CREATE TABLE courses (
    course_id INT,
    course_name VARCHAR(50)
);
```

---

# Summary

| Method                                       | Description                                 |
| -------------------------------------------- | ------------------------------------------- |
| `CREATE TABLE`                               | Creates a new table                         |
| `CREATE TABLE IF NOT EXISTS`                 | Creates the table only if it does not exist |
| `CREATE TABLE AS SELECT`                     | Copies structure and data                   |
| `CREATE TABLE AS SELECT ... WHERE 1=0`       | Copies only the structure                   |
| `CREATE TABLE AS SELECT column1, column2`    | Copies selected columns                     |
| `CREATE TABLE AS SELECT ... WHERE condition` | Copies selected rows                        |
| `CREATE TABLE LIKE`                          | Copies the complete table structure         |
| `CREATE TEMPORARY TABLE`                     | Creates a temporary table                   |
| `AUTO_INCREMENT`                             | Automatically generates IDs                 |

# Inserting Data into Tables

The `INSERT INTO` statement is used to add new records into a table.

Some important points:

* Data must match the column data types.
* Values are inserted in the same order as the columns unless column names are specified.
* String values should be enclosed in single quotes (`' '`).
* If a column has `AUTO_INCREMENT`, you do not need to provide its value.

---

# Current Table

We will use the following table throughout this section.

```sql
CREATE TABLE courses (
    course_id INT PRIMARY KEY,
    course_name VARCHAR(50) NOT NULL,
    duration INT,
    fee INT
);
```

---

# 1. Insert a Single Record

Use `INSERT INTO` with one set of values.

### Syntax

```sql
INSERT INTO table_name
VALUES (...);
```

### Example

```sql
INSERT INTO courses
VALUES (101, 'Python', 30, 5000);
```

### Expected Output

```
Query OK, 1 row affected
```

---

# Verify the Record

```sql
SELECT * FROM courses;
```

### Sample Output

```
+-----------+-------------+----------+------+
| course_id | course_name | duration | fee  |
+-----------+-------------+----------+------+
| 101       | Python      | 30       | 5000 |
+-----------+-------------+----------+------+
```

---

# 2. Insert Multiple Records

You can insert multiple rows using a single statement.

### Syntax

```sql
INSERT INTO table_name
VALUES
(...),
(...),
(...);
```

### Example

```sql
INSERT INTO courses
VALUES
(102, 'Java', 45, 7000),
(103, 'SQL', 20, 3000),
(104, 'Web Development', 60, 9000);
```

### Verify

```sql
SELECT * FROM courses;
```

---

# 3. Insert Values into Selected Columns

If you do not want to insert values into every column, specify the column names.

### Syntax

```sql
INSERT INTO table_name(column1, column2)
VALUES (...);
```

### Example

```sql
CREATE TABLE trainers (
    trainer_id INT AUTO_INCREMENT PRIMARY KEY,
    trainer_name VARCHAR(50),
    experience INT
);
```

```sql
INSERT INTO trainers(trainer_name, experience)
VALUES ('Rahul', 5);
```

Since `trainer_id` is `AUTO_INCREMENT`, MySQL generates it automatically.

---

# Verify

```sql
SELECT * FROM trainers;
```

---

# 4. Insert Multiple Records into Selected Columns

```sql
INSERT INTO trainers(trainer_name, experience)
VALUES
('Anita', 8),
('Kiran', 4),
('David', 6);
```

---

# 5. Insert Data from Another Table

Copies records from one table into another.

### Example

```sql
CREATE TABLE courses_backup AS
SELECT *
FROM courses
WHERE 1 = 0;
```

```sql
INSERT INTO courses_backup
SELECT *
FROM courses;
```

---

# Verify

```sql
SELECT * FROM courses_backup;
```

---

# 6. Insert Only Selected Columns from Another Table

```sql
CREATE TABLE course_catalog (
    course_id INT,
    course_name VARCHAR(50)
);
```

```sql
INSERT INTO course_catalog(course_id, course_name)
SELECT
course_id,
course_name
FROM courses;
```

---

# Common Errors

## Error 1: Duplicate Primary Key

```sql
INSERT INTO courses
VALUES (101, 'C Programming', 25, 4000);
```

### Error

```
ERROR 1062 (23000):
Duplicate entry '101' for key 'PRIMARY'
```

### Reason

A Primary Key must always be unique.

---

## Error 2: Column Count Doesn't Match

```sql
INSERT INTO courses
VALUES (105, 'Java');
```

### Error

```
ERROR 1136 (21S01):
Column count doesn't match value count at row 1
```

### Reason

The number of values does not match the number of columns.

---

## Error 3: Cannot Insert NULL

```sql
INSERT INTO courses
VALUES (106, NULL, 20, 3000);
```

### Error

```
ERROR 1048 (23000):
Column 'course_name' cannot be null
```

### Reason

The `course_name` column has the `NOT NULL` constraint.

---

## Error 4: Incorrect Data Type

```sql
INSERT INTO courses
VALUES ('ABC', 'Python', 30, 5000);
```

### Error

```
ERROR 1366 (HY000):
Incorrect integer value: 'ABC'
```

### Reason

`course_id` is of type `INT`.

---

# Commands Covered

| Command                               | Purpose                        |
| ------------------------------------- | ------------------------------ |
| `INSERT INTO ... VALUES`              | Inserts one record             |
| `INSERT INTO ... VALUES (...), (...)` | Inserts multiple records       |
| `INSERT INTO(column1, column2)`       | Inserts selected columns       |
| `INSERT INTO ... SELECT`              | Copies data from another table |

---

# Practice Questions

1. Create a table named `students`.
2. Insert one student record.
3. Insert five student records using a single statement.
4. Create a backup table named `students_backup`.
5. Copy all records into `students_backup`.
6. Create a table containing only `student_id` and `student_name`.
7. Verify all inserted records using `SELECT *`.



# ALTER TABLE in MySQL

The `ALTER TABLE` statement is used to modify the structure of an existing table.

Some important points:

* It does **not** delete the existing data (in most cases).
* You can add, remove, rename, or modify columns.
* You can also rename the table.
* `ALTER TABLE` changes only the table structure.

---

# Current Table

We will use the following table throughout this section.

```sql
CREATE TABLE courses (
    course_id INT PRIMARY KEY,
    course_name VARCHAR(50) NOT NULL,
    duration INT,
    fee INT
);
```

---

# 1. Add a New Column

Use the `ADD COLUMN` clause to add a new column.

### Syntax

```sql
ALTER TABLE table_name
ADD COLUMN column_name datatype;
```

### Example

```sql
ALTER TABLE courses
ADD COLUMN trainer_name VARCHAR(50);
```

### Verify

```sql
DESC courses;
```

---

# 2. Add Multiple Columns

You can add more than one column in a single statement.

```sql
ALTER TABLE courses
ADD COLUMN start_date DATE,
ADD COLUMN mode VARCHAR(20);
```

### Verify

```sql
DESC courses;
```

---

# 3. Modify the Data Type of a Column

Use the `MODIFY COLUMN` clause to change the data type.

### Syntax

```sql
ALTER TABLE table_name
MODIFY COLUMN column_name new_datatype;
```

### Example

Increase the size of the `course_name` column.

```sql
ALTER TABLE courses
MODIFY COLUMN course_name VARCHAR(100);
```

### Verify

```sql
DESC courses;
```

---

# 4. Rename a Column

Use the `RENAME COLUMN` clause to rename an existing column.

### Syntax

```sql
ALTER TABLE table_name
RENAME COLUMN old_name TO new_name;
```

### Example

```sql
ALTER TABLE courses
RENAME COLUMN fee TO course_fee;
```

### Verify

```sql
DESC courses;
```

---

# 5. Rename a Table

The `RENAME TO` clause changes the table name.

### Syntax

```sql
ALTER TABLE table_name
RENAME TO new_table_name;
```

### Example

```sql
ALTER TABLE courses
RENAME TO course_details;
```

### Verify

```sql
SHOW TABLES;
```

---

# 6. Drop a Column

Use the `DROP COLUMN` clause to remove an existing column.

### Syntax

```sql
ALTER TABLE table_name
DROP COLUMN column_name;
```

### Example

```sql
ALTER TABLE course_details
DROP COLUMN trainer_name;
```

### Verify

```sql
DESC course_details;
```

---

# 7. Change the Position of a Column

Use the `FIRST` keyword to move a column to the beginning.

```sql
ALTER TABLE course_details
MODIFY COLUMN course_fee INT FIRST;
```

### Verify

```sql
DESC course_details;
```

---

# 8. Place a Column After Another Column

Use the `AFTER` keyword to place a column in a specific position.

```sql
ALTER TABLE course_details
MODIFY COLUMN course_fee INT
AFTER duration;
```

### Verify

```sql
DESC course_details;
```

---

# 9. Add a Default Value

```sql
ALTER TABLE course_details
ALTER COLUMN mode
SET DEFAULT 'Offline';
```

> **Note:** The syntax for setting a default value can vary slightly between MySQL versions. Another common approach is:

```sql
ALTER TABLE course_details
MODIFY COLUMN mode VARCHAR(20) DEFAULT 'Offline';
```

---

# 10. Remove a Default Value

```sql
ALTER TABLE course_details
ALTER COLUMN mode
DROP DEFAULT;
```

> **Note:** Older MySQL versions may require `MODIFY COLUMN` instead.

---

# Common Errors

## Error 1: Unknown Column

```sql
ALTER TABLE courses
DROP COLUMN salary;
```

### Error

```text
ERROR 1091 (42000):
Can't DROP 'salary'; check that column/key exists
```

### Solution

Check the table structure first.

```sql
DESC courses;
```

---

## Error 2: Table Doesn't Exist

```sql
ALTER TABLE students
ADD COLUMN email VARCHAR(100);
```

### Error

```text
ERROR 1146 (42S02):
Table 'training.students' doesn't exist
```

### Solution

```sql
SHOW TABLES;
```

---

## Error 3: Duplicate Column Name

```sql
ALTER TABLE courses
ADD COLUMN duration INT;
```

### Error

```text
ERROR 1060 (42S21):
Duplicate column name 'duration'
```

---

# Summary

| Command                          | Purpose                                        |
| -------------------------------- | ---------------------------------------------- |
| `ADD COLUMN`                     | Adds a new column                              |
| `ADD COLUMN ..., ADD COLUMN ...` | Adds multiple columns                          |
| `MODIFY COLUMN`                  | Changes the datatype or definition of a column |
| `RENAME COLUMN`                  | Renames a column                               |
| `RENAME TO`                      | Renames the table                              |
| `DROP COLUMN`                    | Deletes a column                               |
| `FIRST`                          | Moves a column to the first position           |
| `AFTER`                          | Places a column after another column           |

---

# Practice Questions

1. Add a column named `category` to the `courses` table.
2. Add two new columns: `rating` and `language`.
3. Change the size of `course_name` from `VARCHAR(50)` to `VARCHAR(150)`.
4. Rename the column `fee` to `course_fee`.
5. Rename the table `courses` to `course_details`.
6. Delete the `category` column.
7. Move `course_fee` to the first position.
8. Display the final table structure using `DESC`.


# UPDATE in MySQL

The `UPDATE` statement is used to **modify existing data in one or more rows of a table**.

Unlike `ALTER TABLE`, which changes the **structure of a table**, `UPDATE` changes the **data stored in the table**.

### Important Points

* `UPDATE` modifies existing records.
* It can update one column or multiple columns.
* The `WHERE` clause determines which rows will be updated.
* If `WHERE` is omitted, **all rows will be updated**.
* You can use calculations, functions, `CASE`, and conditions inside an `UPDATE`.
* `NULL` values should be checked using `IS NULL` or `IS NOT NULL`.
* Always verify the `WHERE` condition before executing an important `UPDATE`.

---

# Current Table

We will use the following table throughout this section.

```sql
CREATE TABLE students (
    student_id INT PRIMARY KEY,
    name       VARCHAR(50) NOT NULL,
    city       VARCHAR(50),
    age        INT,
    course     VARCHAR(50),
    marks      INT,
    joined_on  DATE
);
```

Example data:

```sql
INSERT INTO students VALUES
(101, 'Rahul Verma', 'Hyderabad', 21, 'Python', 78, '2025-01-15'),
(102, 'Anita Sharma', 'Chennai', 22, 'SQL', 95, '2025-01-20'),
(103, 'Karan Patel', 'Hyderabad', 20, 'Python', 38, '2025-02-01'),
(104, 'Priya Nair', 'Kochi', 23, 'Java', 66, '2025-02-10'),
(105, 'Vikram Rao', 'Hyderabad', 21, 'SQL', 81, '2025-03-05');
```

---

# 1. Update a Single Column

Use `SET` to specify the new value.

### Syntax

```sql
UPDATE table_name
SET column_name = new_value
WHERE condition;
```

### Example

Change Rahul's marks from 78 to 85:

```sql
UPDATE students
SET marks = 85
WHERE student_id = 101;
```

### Verify

```sql
SELECT *
FROM students
WHERE student_id = 101;
```

### Concept

```text
UPDATE → Which table?
SET    → What should change?
WHERE  → Which rows should change?
```

---

# 2. Update Multiple Columns

You can update multiple columns in a single statement.

### Example

Update Rahul's city and marks:

```sql
UPDATE students
SET
    city = 'Bangalore',
    marks = 90
WHERE student_id = 101;
```

### Verify

```sql
SELECT *
FROM students
WHERE student_id = 101;
```

---

# 3. Update Multiple Rows

The `WHERE` condition can match multiple rows.

### Example

Change all Python students to Data Science:

```sql
UPDATE students
SET course = 'Data Science'
WHERE course = 'Python';
```

Every row where `course = 'Python'` will be updated.

### Verify

```sql
SELECT *
FROM students
WHERE course = 'Data Science';
```

---

# 4. Update All Rows

If you do not specify a `WHERE` clause, **all rows in the table will be updated**.

### Example

Increase everyone's marks by 5:

```sql
UPDATE students
SET marks = marks + 5;
```

This updates every row.

### Important Warning

This statement:

```sql
UPDATE students
SET city = 'Hyderabad';
```

will change the city of **every student** to Hyderabad.

If you only want to update one student:

```sql
UPDATE students
SET city = 'Hyderabad'
WHERE student_id = 101;
```

> **Always be careful when using `UPDATE` without `WHERE`.**

---

# 5. Update Using an Expression

The new value does not have to be a fixed value.

You can use the existing value in a calculation.

### Example

Increase marks by 10 for SQL students:

```sql
UPDATE students
SET marks = marks + 10
WHERE course = 'SQL';
```

If a student currently has:

```text
marks = 81
```

After the update:

```text
marks = 91
```

The calculation is performed separately for each matching row.

---

# 6. Update Using Multiple Conditions

You can use `AND`, `OR`, `IN`, and other conditions.

### Example: AND

Increase marks by 5 for SQL students who scored below 80:

```sql
UPDATE students
SET marks = marks + 5
WHERE course = 'SQL'
  AND marks < 80;
```

### Example: IN

Update the course for students from Hyderabad or Chennai:

```sql
UPDATE students
SET course = 'SQL'
WHERE city IN ('Hyderabad', 'Chennai');
```

### Example: OR

```sql
UPDATE students
SET course = 'SQL'
WHERE city = 'Hyderabad'
   OR city = 'Chennai';
```

---

# 7. Update NULL Values

To find `NULL` values, use `IS NULL`.

Do **not** use:

```sql
UPDATE students
SET marks = 0
WHERE marks = NULL;
```

Use:

```sql
UPDATE students
SET marks = 0
WHERE marks IS NULL;
```

### Why?

`NULL` represents an unknown or missing value and cannot be compared using `=`.

### Verify

```sql
SELECT *
FROM students
WHERE marks IS NULL;
```

---

# 8. Update Only Non-NULL Values

Use `IS NOT NULL` when you want to update rows that already have a value.

### Example

Increase marks by 5 only where marks are available:

```sql
UPDATE students
SET marks = marks + 5
WHERE marks IS NOT NULL;
```

---

# 9. Update Using SQL Functions

You can use SQL functions inside an `UPDATE`.

### Example: UPPER()

Convert city names to uppercase:

```sql
UPDATE students
SET city = UPPER(city);
```

### Example: TRIM()

Remove leading and trailing spaces from names:

```sql
UPDATE students
SET name = TRIM(name);
```

### Example: COALESCE()

Replace NULL course values with `Not Assigned`:

```sql
UPDATE students
SET course = COALESCE(course, 'Not Assigned')
WHERE course IS NULL;
```

---

# 10. Update Using CASE

`CASE` allows different rows to receive different values based on conditions.

### Example

Suppose we want to create different performance categories.

```sql
UPDATE students
SET course =
    CASE
        WHEN marks >= 90 THEN 'Advanced'
        WHEN marks >= 60 THEN 'Intermediate'
        ELSE 'Beginner'
    END;
```

The logic is:

```text
marks >= 90  → Advanced
marks >= 60  → Intermediate
marks < 60   → Beginner
```

> **Note:** In a real database, it would be better to store this in a separate column such as `performance_level` rather than replacing the `course` column. This example is only for demonstrating `CASE` with `UPDATE`.

---

# 11. Update a Date Column

You can directly assign a date value.

```sql
UPDATE students
SET joined_on = '2025-06-01'
WHERE student_id = 101;
```

You can also perform date calculations.

### Add 7 days

```sql
UPDATE students
SET joined_on = joined_on + INTERVAL 7 DAY
WHERE student_id = 101;
```

### Subtract 30 days

```sql
UPDATE students
SET joined_on = joined_on - INTERVAL 30 DAY
WHERE student_id = 101;
```

---

# 12. Update Using Another Column

You can use the value of one column to calculate another column.

### Example

Add the student's age to their marks:

```sql
UPDATE students
SET marks = marks + age
WHERE marks IS NOT NULL;
```

For example:

```text
marks = 78
age   = 21

New marks = 78 + 21 = 99
```

---

# 13. Update Using Another Table

MySQL allows you to update a table using data from another table with `JOIN`.

Suppose we have:

```sql
CREATE TABLE courses (
    course_id INT PRIMARY KEY,
    course_name VARCHAR(50)
);
```

And `students` contains:

```text
student_id
course_id
course
```

We can update the student's course name using the `courses` table:

```sql
UPDATE students s
JOIN courses c
    ON s.course_id = c.course_id
SET s.course = c.course_name;
```

This is useful when the value that needs to be updated comes from another related table.

---

# 14. Update a Limited Number of Rows

MySQL allows `LIMIT` with `UPDATE`.

### Example

Update only one matching row:

```sql
UPDATE students
SET marks = marks + 5
WHERE course = 'SQL'
LIMIT 1;
```

This updates only one matching row.

> **Note:** If multiple rows satisfy the condition, do not assume which particular row will be selected unless you use an appropriate ordering strategy.

---

# 15. Verify Before Updating

A good practice is to first run a `SELECT` using the same `WHERE` condition.

Suppose you want to run:

```sql
UPDATE students
SET marks = marks + 5
WHERE course = 'SQL';
```

Before executing it, first check:

```sql
SELECT *
FROM students
WHERE course = 'SQL';
```

This lets you see which rows will be affected.

Then execute the `UPDATE`.

### Recommended workflow

```text
1. SELECT → Check the rows
2. UPDATE → Modify the rows
3. SELECT → Verify the result
```

---

# 16. UPDATE vs ALTER TABLE

This is an important distinction.

### ALTER TABLE

Changes the **structure/schema** of the table.

```sql
ALTER TABLE students
ADD COLUMN email VARCHAR(100);
```

This adds a new column.

### UPDATE

Changes the **data stored in existing rows**.

```sql
UPDATE students
SET email = 'student@example.com'
WHERE student_id = 101;
```

This changes the value in an existing row.

### Easy way to remember

```text
ALTER TABLE → Changes table structure
UPDATE      → Changes existing data
```

---

# 17. UPDATE vs INSERT

Another important distinction:

### INSERT

Adds a **new row**.

```sql
INSERT INTO students
(student_id, name, city, age, course, marks, joined_on)
VALUES
(106, 'Sneha Iyer', 'Chennai', 22, 'Java', 54, '2025-03-12');
```

### UPDATE

Changes an **existing row**.

```sql
UPDATE students
SET marks = 60
WHERE student_id = 106;
```

### Easy way to remember

```text
INSERT → Add new rows
UPDATE → Change existing rows
```

---

# 18. UPDATE and Primary Keys

You can update a primary key, but you should generally avoid doing so unless there is a valid reason.

For example:

```sql
UPDATE students
SET student_id = 200
WHERE student_id = 101;
```

If `200` is not already being used and no foreign-key relationships prevent the change, MySQL may allow it.

However, changing primary keys can affect related tables and is generally not recommended for routine data updates.

---

# 19. UPDATE and UNIQUE Columns

If a column has a `UNIQUE` constraint, the new value must also remain unique.

Suppose:

```text
email
-------------------
surya@example.com
rahul@example.com
```

If `email` is unique:

```sql
UPDATE students
SET email = 'rahul@example.com'
WHERE student_id = 101;
```

MySQL will reject the update because that email already exists.

This demonstrates that **constraints are checked during UPDATE as well as INSERT**.

---

# 20. Quick Cheat Sheet

| Requirement                | Example                         |
| -------------------------- | ------------------------------- |
| Update one column          | `SET marks = 90`                |
| Update multiple columns    | `SET city = 'Pune', marks = 90` |
| Update specific rows       | Use `WHERE`                     |
| Update all rows            | Omit `WHERE`                    |
| Increase a number          | `marks = marks + 5`             |
| Update NULL values         | `WHERE marks IS NULL`           |
| Update non-NULL values     | `WHERE marks IS NOT NULL`       |
| Use multiple conditions    | `AND`, `OR`, `IN`               |
| Conditional update         | `CASE`                          |
| Update text                | `UPPER()`, `LOWER()`, `TRIM()`  |
| Update dates               | `INTERVAL`, date functions      |
| Update using another table | `UPDATE ... JOIN`               |
| Limit affected rows        | `LIMIT`                         |
| Check before updating      | Run matching `SELECT` first     |

---

# Key Concept

The basic structure to remember is:

```sql
UPDATE table_name
SET
    column1 = new_value,
    column2 = new_value
WHERE condition;
```

Think of it as:

```text
UPDATE → Which table?
SET    → What should change?
WHERE  → Which rows should change?
```

### Most Important Rule

> **If you omit the `WHERE` clause, the `UPDATE` statement will affect every row in the table. Always check the `WHERE` condition carefully before executing an UPDATE.**




# Deleting Data and Dropping Tables

MySQL provides different commands to remove data or database objects. Choosing the correct command is important because each command behaves differently.

---

# Difference Between DELETE, TRUNCATE and DROP

| Command    | Removes Data | Removes Structure | Can Use WHERE | Can Be Rolled Back* |
| ---------- | ------------ | ----------------- | ------------- | ------------------- |
| DELETE     | ✅ Yes        | ❌ No              | ✅ Yes         | ✅ Yes               |
| TRUNCATE   | ✅ Yes        | ❌ No              | ❌ No          | ❌ No                |
| DROP TABLE | ✅ Yes        | ✅ Yes             | ❌ No          | ❌ No                |

> **Note:** Rollback depends on the storage engine and transaction settings.

---

# Current Table

```sql
CREATE TABLE courses (
    course_id INT PRIMARY KEY,
    course_name VARCHAR(50),
    duration INT,
    fee INT
);
```

```sql
INSERT INTO courses
VALUES
(101, 'Python', 30, 5000),
(102, 'Java', 45, 7000),
(103, 'SQL', 20, 3000),
(104, 'Web Development', 60, 9000);
```

---

# 1. Delete a Specific Record

Use the `WHERE` clause to delete only the required record.

### Syntax

```sql
DELETE FROM table_name
WHERE condition;
```

### Example

```sql
DELETE FROM courses
WHERE course_id = 103;
```

### Verify

```sql
SELECT * FROM courses;
```

---

# 2. Delete Multiple Records

Deletes all records that satisfy the given condition.

```sql
DELETE FROM courses
WHERE fee < 6000;
```

### Verify

```sql
SELECT * FROM courses;
```

---

# 3. Delete All Records

Removes all rows from the table but keeps the table structure.

```sql
DELETE FROM courses;
```

### Verify

```sql
SELECT * FROM courses;
```

Expected Output

```text
Empty set
```

---

# 4. TRUNCATE TABLE

`TRUNCATE` removes all rows from a table.

Unlike `DELETE`, it is faster because it removes all records at once.

The table structure remains unchanged.

### Syntax

```sql
TRUNCATE TABLE table_name;
```

### Example

```sql
TRUNCATE TABLE courses;
```

### Verify

```sql
SELECT * FROM courses;
```

---

# 5. Drop a Table

`DROP TABLE` permanently removes the table and all its data.

### Syntax

```sql
DROP TABLE table_name;
```

### Example

```sql
DROP TABLE courses;
```

### Verify

```sql
SHOW TABLES;
```

---

# 6. Drop a Table Only If It Exists

Avoids an error if the table is not available.

```sql
DROP TABLE IF EXISTS courses;
```

---

# 7. Drop Multiple Tables

```sql
DROP TABLE trainers, course_catalog;
```

---

# 8. Drop an Entire Database

Deletes the database and every table inside it.

### Syntax

```sql
DROP DATABASE database_name;
```

### Example

```sql
DROP DATABASE training;
```

---

# 9. Drop a Database Only If It Exists

```sql
DROP DATABASE IF EXISTS training;
```

---




# Common Errors

## Error 1: Unknown Table

```sql
DROP TABLE students;
```

### Error

```text
ERROR 1051 (42S02):
Unknown table 'students'
```

### Solution

```sql
SHOW TABLES;
```

or

```sql
DROP TABLE IF EXISTS students;
```

---

## Error 2: Unknown Database

```sql
DROP DATABASE college;
```

### Error

```text
ERROR 1008 (HY000):
Can't drop database 'college'; database doesn't exist
```

### Solution

```sql
SHOW DATABASES;
```

or

```sql
DROP DATABASE IF EXISTS college;
```

---

# Summary

| Command                              | Purpose                                |
| ------------------------------------ | -------------------------------------- |
| `DELETE FROM table WHERE condition;` | Deletes selected rows                  |
| `DELETE FROM table;`                 | Deletes all rows                       |
| `TRUNCATE TABLE table;`              | Removes all rows quickly               |
| `DROP TABLE table;`                  | Deletes the table permanently          |
| `DROP TABLE IF EXISTS table;`        | Deletes the table only if it exists    |
| `DROP DATABASE database;`            | Deletes the database permanently       |
| `DROP DATABASE IF EXISTS database;`  | Deletes the database only if it exists |

---

# Practice Questions

1. Delete the course with `course_id = 102`.
2. Delete all courses where the fee is less than `6000`.
3. Remove all records from the `courses` table using `DELETE`.
4. Insert the records again and remove all rows using `TRUNCATE`.
5. Verify that the table structure still exists.
6. Delete the `courses` table.
7. Display all remaining tables.
8. Delete the `training` database.
9. Display all available databases.

---

# Class Summary

In this notebook, you learned:

* Creating a database
* Viewing and selecting a database
* Understanding tables, datatypes, and constraints
* Creating tables in different ways
* Inserting records
* Modifying tables using `ALTER TABLE`
* Deleting records using `DELETE`
* Removing all records using `TRUNCATE`
* Deleting tables using `DROP TABLE`
* Deleting databases using `DROP DATABASE`

You are now ready to learn the next topic: **Retrieving Data using the `SELECT` statement**.


