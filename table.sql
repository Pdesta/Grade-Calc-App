-- Subjects table
CREATE TABLE subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    target FLOAT DEFAULT 50
);

-- Tests table
CREATE TABLE tests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subject_id INT,
    weight FLOAT NOT NULL,
    score FLOAT, -- NULL means not entered
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
);