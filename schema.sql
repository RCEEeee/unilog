-- ============================================================
--  UNIVERSITY DATABASE SCHEMA
--  Based on ER Diagram
-- ============================================================

-- Drop tables in reverse dependency order
DROP TABLE IF EXISTS enrollment;
DROP TABLE IF EXISTS course_lecturer;
DROP TABLE IF EXISTS user_role;
DROP TABLE IF EXISTS role_permission;
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS lecturer;
DROP TABLE IF EXISTS staff;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS course;
DROP TABLE IF EXISTS degree_program;
DROP TABLE IF EXISTS faculty;
DROP TABLE IF EXISTS dept;
DROP TABLE IF EXISTS roles;
DROP TABLE IF EXISTS permissions;

-- ============================================================
-- INDEPENDENT / LOOKUP TABLES
-- ============================================================

CREATE TABLE dept (
    id          INT          AUTO_INCREMENT PRIMARY KEY,
    dept_name   VARCHAR(100) NOT NULL UNIQUE,
    dept_desc   TEXT
);

CREATE TABLE roles (
    id          INT          AUTO_INCREMENT PRIMARY KEY,
    role_name   VARCHAR(100) NOT NULL UNIQUE,
    role_desc   TEXT
);

CREATE TABLE permissions (
    id              INT          AUTO_INCREMENT PRIMARY KEY,
    permission_name VARCHAR(100) NOT NULL UNIQUE,
    permission_desc TEXT
);

CREATE TABLE faculty (
    id           INT          AUTO_INCREMENT PRIMARY KEY,
    faculty_name VARCHAR(100) NOT NULL UNIQUE,
    faculty_desc TEXT
);

-- ============================================================
-- CORE USER TABLE
-- ============================================================

CREATE TABLE user (
    id          INT          AUTO_INCREMENT PRIMARY KEY,
    user_name   VARCHAR(100) NOT NULL UNIQUE,
    full_name   VARCHAR(150) NOT NULL,
    cell        VARCHAR(20),
    email       VARCHAR(150) NOT NULL UNIQUE,
    address     TEXT,
    password    VARCHAR(255) NOT NULL   -- store hashed passwords!
);

-- ============================================================
-- ROLE <-> PERMISSION  (many-to-many junction)
-- ============================================================

CREATE TABLE role_permission (
    role_id       INT NOT NULL,
    permission_id INT NOT NULL,
    PRIMARY KEY (role_id, permission_id),
    FOREIGN KEY (role_id)       REFERENCES roles(id)       ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE
);

-- ============================================================
-- USER <-> ROLE  (many-to-many junction)
-- ============================================================

CREATE TABLE user_role (
    user_id INT NOT NULL,
    role_id INT NOT NULL,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES user(id)  ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
);

-- ============================================================
-- USER SPECIALISATIONS  (IS-A relationships)
-- ============================================================

-- Staff  -- belongs to a department
CREATE TABLE staff (
    id       INT AUTO_INCREMENT PRIMARY KEY,
    user_id  INT NOT NULL UNIQUE,
    dept_id  INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id)  ON DELETE CASCADE,
    FOREIGN KEY (dept_id) REFERENCES dept(id)  ON DELETE RESTRICT
);

-- Degree / Programme (belongs to a faculty)
CREATE TABLE degree_program (
    id         INT          AUTO_INCREMENT PRIMARY KEY,
    faculty_id INT          NOT NULL,
    deg_name   VARCHAR(150) NOT NULL,
    deg_desc   TEXT,
    FOREIGN KEY (faculty_id) REFERENCES faculty(id) ON DELETE RESTRICT
);

-- Student -- enrolled in a programme
CREATE TABLE student (
    id           INT          AUTO_INCREMENT PRIMARY KEY,
    user_id      INT          NOT NULL UNIQUE,
    reg_no       VARCHAR(50)  NOT NULL UNIQUE,
    programme_id INT          NOT NULL,
    FOREIGN KEY (user_id)      REFERENCES user(id)           ON DELETE CASCADE,
    FOREIGN KEY (programme_id) REFERENCES degree_program(id) ON DELETE RESTRICT
);

-- Lecturer -- belongs to a faculty
CREATE TABLE lecturer (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    user_id    INT NOT NULL UNIQUE,
    faculty_id INT NOT NULL,
    FOREIGN KEY (user_id)    REFERENCES user(id)    ON DELETE CASCADE,
    FOREIGN KEY (faculty_id) REFERENCES faculty(id) ON DELETE RESTRICT
);

-- ============================================================
-- COURSE
-- ============================================================

CREATE TABLE course (
    id          INT          AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(150) NOT NULL,
    course_desc TEXT,
    faculty_id  INT          NOT NULL,   -- "belongs to" faculty
    FOREIGN KEY (faculty_id) REFERENCES faculty(id) ON DELETE RESTRICT
);

-- ============================================================
-- JUNCTION TABLES
-- ============================================================

-- Student  "is enrolled to"  Course
CREATE TABLE enrollment (
    student_id INT NOT NULL,
    course_id  INT NOT NULL,
    enrolled_at DATE DEFAULT (CURRENT_DATE),
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES student(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id)  REFERENCES course(id)  ON DELETE CASCADE
);

-- Lecturer  "teaches"  Course
CREATE TABLE course_lecturer (
    lecturer_id INT NOT NULL,
    course_id   INT NOT NULL,
    PRIMARY KEY (lecturer_id, course_id),
    FOREIGN KEY (lecturer_id) REFERENCES lecturer(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id)   REFERENCES course(id)   ON DELETE CASCADE
);

-- ============================================================
-- SAMPLE SEED DATA
-- ============================================================

-- Departments
INSERT INTO dept (dept_name, dept_desc) VALUES
('Computer Science', 'CS department'),
('Mathematics',      'Maths department');

-- Faculties
INSERT INTO faculty (faculty_name, faculty_desc) VALUES
('Faculty of Engineering',   'Engineering & Technology'),
('Faculty of Natural Science','Science programs');

-- Roles & Permissions
INSERT INTO roles (role_name, role_desc) VALUES
('Admin',    'Full system access'),
('Student',  'Student portal access'),
('Lecturer', 'Lecturer portal access');

INSERT INTO permissions (permission_name, permission_desc) VALUES
('manage_users',   'Create/edit/delete users'),
('view_courses',   'View all courses'),
('grade_students', 'Enter grades');

INSERT INTO role_permission (role_id, permission_id) VALUES
(1,1),(1,2),(1,3),
(2,2),
(3,2),(3,3);

-- Degree programs
INSERT INTO degree_program (faculty_id, deg_name, deg_desc) VALUES
(1, 'BSc Computer Science', '3-year CS degree'),
(1, 'BSc Software Engineering', '3-year SE degree');

-- Users
INSERT INTO user (user_name, full_name, cell, email, address, password) VALUES
('admin1',   'Admin',    '0700000001', 'rasper@uni.edu',   '1 Main St', 'hashed_pw'),
('student1', 'Bob Student',    '0700000002', 'bob@uni.edu',     '2 Oak Ave', 'hashed_pw'),
('lect1',    'Carol Lecturer', '0700000003', 'carol@uni.edu',   '3 Pine Rd', 'hashed_pw'),
('staff1',   'Dave Staff',     '0700000004', 'dave@uni.edu',    '4 Elm St',  'hashed_pw');

-- Assign roles
INSERT INTO user_role VALUES (1,1),(2,2),(3,3),(4,1);

-- Specialisations
INSERT INTO staff   (user_id, dept_id)                VALUES (4, 1);
INSERT INTO student (user_id, reg_no, programme_id)   VALUES (2, 'S2024001', 1);
INSERT INTO lecturer(user_id, faculty_id)             VALUES (3, 1);

-- Courses
INSERT INTO course (course_name, course_desc, faculty_id) VALUES
('Introduction to Programming', 'Basics of coding', 1),
('Data Structures',             'Arrays, trees, graphs', 1),
('Calculus I',                  'Differentiation & integration', 2);

-- Assignments
INSERT INTO course_lecturer VALUES (1,1),(1,2);
INSERT INTO enrollment      VALUES (1,1,'2024-09-01'),(1,2,'2024-09-01');

UPDATE user
SET password = 'wandinoda'
WHERE email = 'rasper@uni.edu';