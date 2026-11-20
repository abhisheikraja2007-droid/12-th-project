-- Database setup script for Criminal Management System

CREATE DATABASE IF NOT EXISTS management;
USE management;

-- Table for User Authentication
CREATE TABLE IF NOT EXISTS login (
    userid VARCHAR(50) NOT NULL PRIMARY KEY,
    password VARCHAR(50) NOT NULL
);

-- Insert default administrative user (default in app: user 'root'/'admin' or custom)
INSERT INTO login (userid, password) VALUES 
('admin', 'admin'),
('user', '123')
ON DUPLICATE KEY UPDATE userid=userid;

-- Table for Criminal Records
CREATE TABLE IF NOT EXISTS criminal (
    Case_id VARCHAR(50) NOT NULL PRIMARY KEY,
    Criminal_no VARCHAR(50) NOT NULL,
    Criminal_name VARCHAR(100) NOT NULL,
    Nick_name VARCHAR(50),
    arrest_date VARCHAR(50),
    dateOfcrime VARCHAR(50),
    address VARCHAR(255),
    age VARCHAR(10),
    occupation VARCHAR(100),
    BirthMark VARCHAR(100),
    crimeType VARCHAR(100),
    fatherName VARCHAR(100),
    gender VARCHAR(20),
    wanted VARCHAR(20)
);
