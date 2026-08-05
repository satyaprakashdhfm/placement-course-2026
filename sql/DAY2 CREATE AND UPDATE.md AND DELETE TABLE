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
