
CREATE DATABASE attendance_db;
USE attendance_db;

-- Admin Table
CREATE TABLE admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL
);

INSERT INTO admin (username, password)
VALUES ('admin', 'admin123');

-- Students Table
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    roll_no VARCHAR(20) UNIQUE NOT NULL,
    department VARCHAR(50) NOT NULL
);

INSERT INTO students (name, roll_no, department) VALUES
('Arun Kumar', 'CSE001', 'CSE'),
('Priya S', 'CSE002', 'CSE'),
('Rahul M', 'ECE001', 'ECE');

-- Attendance Table
CREATE TABLE attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    attendance_date DATE,
    status ENUM('Present', 'Absent') NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id)
);
