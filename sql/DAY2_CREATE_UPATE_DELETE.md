# CREATE TABLE in MySQL

In this notebook, we will learn different ways of creating tables in MySQL.

---

## Step 1: Create a Database

```sql
CREATE DATABASE IF NOT EXISTS training;
```

---

## Step 2: Select the Database

```sql
USE training;
```

---

## 1. Create a Table

Creates a new table named `courses`.

```sql
CREATE TABLE courses (
    course_id   INT PRIMARY KEY,
    course_name VARCHAR(50) NOT NULL,
    duration    INT,
    fee         INT
);
```

---

## 2. Create a Table Only If It Does Not Exist

Prevents an error if the table already exists.

```sql
CREATE TABLE IF NOT EXISTS courses (
    course_id   INT PRIMARY KEY,
    course_name VARCHAR(50) NOT NULL,
    duration    INT,
    fee         INT
);
```

---

## 3. Insert Sample Records

Insert some data into the `courses` table.

```sql
INSERT INTO courses VALUES
(101, 'Python', 30, 5000),
(102, 'Java', 45, 7000),
(103, 'SQL', 20, 3000),
(104, 'Web Development', 60, 9000);
```

---

## 4. Create a Table from an Existing Table (Structure + Data)

Copies both the table structure and all the data.

```sql
CREATE TABLE courses_backup AS
SELECT *
FROM courses;
```

---

## 5. Create a Table with Structure Only

Copies only the table structure without any records.

```sql
CREATE TABLE courses_empty AS
SELECT *
FROM courses
WHERE 1 = 0;
```

---

## 6. Create a Table with Selected Columns

Copies only specific columns from an existing table.

```sql
CREATE TABLE course_catalog AS
SELECT
    course_id,
    course_name
FROM courses;
```

---

## 7. Create a Table with Selected Rows

Copies only the records that satisfy a condition.

```sql
CREATE TABLE premium_courses AS
SELECT *
FROM courses
WHERE fee >= 7000;
```

---

## 8. Create a Table Using LIKE

Copies the complete table structure, including indexes and constraints, but not the data.

```sql
CREATE TABLE courses_clone LIKE courses;
```

---

## 9. Create a Temporary Table

Temporary tables exist only for the current database session.

```sql
CREATE TEMPORARY TABLE temp_courses (
    course_id   INT,
    course_name VARCHAR(50)
);
```

---

## 10. Create a Table with AUTO_INCREMENT

Automatically generates a unique ID for each new record.

```sql
CREATE TABLE trainers (
    trainer_id   INT AUTO_INCREMENT PRIMARY KEY,
    trainer_name VARCHAR(50),
    experience   INT
);
```

---

## Summary

| Method | Description |
|---------|-------------|
| `CREATE TABLE` | Creates a new table |
| `CREATE TABLE IF NOT EXISTS` | Creates the table only if it doesn't exist |
| `CREATE TABLE AS SELECT` | Copies structure and data |
| `CREATE TABLE AS SELECT ... WHERE 1=0` | Copies only the structure |
| `CREATE TABLE AS SELECT column1, column2` | Copies selected columns |
| `CREATE TABLE AS SELECT ... WHERE condition` | Copies selected rows |
| `CREATE TABLE LIKE` | Copies complete table structure |
| `CREATE TEMPORARY TABLE` | Creates a temporary table |
| `AUTO_INCREMENT` | Generates automatic IDs |


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

