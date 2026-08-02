-- ============================================================
--  Training database used from Day 2 onwards   (MySQL 8)
--  In MySQL Workbench: open this file and click the lightning bolt.
--  At the command line:  mysql -u root -p < setup_training_db.sql
-- ============================================================

DROP DATABASE IF EXISTS training;
CREATE DATABASE training;
USE training;

-- ---------------------------------------------- courses
CREATE TABLE courses (
    course_id   INT PRIMARY KEY,
    course_name VARCHAR(50) NOT NULL,
    duration    INT,                     -- in days
    fee         INT
);

INSERT INTO courses VALUES
    (1, 'Python', 45, 15000),
    (2, 'SQL',    30, 10000),
    (3, 'Java',   60, 20000),
    (4, 'DSA',    90, 25000),
    (5, 'Cloud',  30, 18000);            -- nobody has joined this one yet

-- ---------------------------------------------- students
CREATE TABLE students (
    id        INT PRIMARY KEY,
    name      VARCHAR(50) NOT NULL,
    city      VARCHAR(50),
    age       INT,
    course_id INT,
    marks     INT,
    joined_on DATE,
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

INSERT INTO students VALUES
    (101, 'Rahul Verma',  'Hyderabad', 21, 1,    78,   '2025-01-15'),
    (102, 'Anita Sharma', 'Chennai',   22, 2,    95,   '2025-01-20'),
    (103, 'Karan Patel',  'Hyderabad', 20, 1,    38,   '2025-02-01'),
    (104, 'Priya Nair',   'Kochi',     23, 3,    66,   '2025-02-10'),
    (105, 'Vikram Rao',   'Hyderabad', 21, 2,    81,   '2025-03-05'),
    (106, 'Sneha Iyer',   'Chennai',   22, 3,    54,   '2025-03-12'),
    (107, 'Arjun Mehta',  'Pune',      24, 4,    90,   '2025-04-02'),
    (108, 'Divya Menon',  'Kochi',     20, 1,    45,   '2025-04-18'),
    (109, 'Rohit Sinha',  'Pune',      23, NULL, 78,   '2025-05-01'),  -- no course; ties with 101
    (110, 'Meera Nair',   'Chennai',   21, 4,    NULL, '2025-05-20');  -- no marks yet

-- ---------------------------------------------- employees (for SELF JOIN)
CREATE TABLE employees (
    emp_id     INT PRIMARY KEY,
    emp_name   VARCHAR(50),
    manager_id INT,
    salary     INT
);

INSERT INTO employees VALUES
    (1, 'Anil',   NULL, 90000),
    (2, 'Bhavna', 1,    70000),
    (3, 'Chetan', 1,    65000),
    (4, 'Deepa',  2,    50000),
    (5, 'Esha',   2,    52000);
