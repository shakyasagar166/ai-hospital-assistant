-- AI Hospital Assistant - Database DDL Schema
-- MySQL 8.0 Compatible

CREATE DATABASE IF NOT EXISTS hospital_ai CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE hospital_ai;

-- 1. Users Table (Patients, Doctors, Staff)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'patient', -- patient, doctor, staff, admin
    blood_group VARCHAR(10) DEFAULT 'O+',
    emergency_contact VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Medical Departments Table
CREATE TABLE IF NOT EXISTS departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE,
    description TEXT NOT NULL,
    floor_location VARCHAR(100) NOT NULL,
    head_doctor VARCHAR(255),
    contact_ext VARCHAR(50) DEFAULT '101',
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_dept_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Specialist Doctors Table
CREATE TABLE IF NOT EXISTS doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    department_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    specialization VARCHAR(255) NOT NULL,
    qualification VARCHAR(255) NOT NULL,
    experience_years INT NOT NULL,
    consultation_fee_inr DECIMAL(10, 2) NOT NULL,
    rating DECIMAL(3, 2) DEFAULT 4.80,
    available_days_json JSON,
    available_hours VARCHAR(100) DEFAULT '09:00 AM - 05:00 PM',
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE,
    INDEX idx_doctor_dept (department_id),
    INDEX idx_doctor_spec (specialization)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. Appointments Table
CREATE TABLE IF NOT EXISTS appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    appointment_date VARCHAR(50) NOT NULL,
    time_slot VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'confirmed', -- confirmed, pending, completed, cancelled
    symptoms_summary TEXT,
    triage_level VARCHAR(50) DEFAULT 'Low', -- Low, Medium, Urgent, Emergency
    confirmation_code VARCHAR(64) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE,
    INDEX idx_appt_patient (patient_id),
    INDEX idx_appt_doctor (doctor_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. Diagnostic Lab Tests Table
CREATE TABLE IF NOT EXISTS lab_tests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    department_id INT,
    name VARCHAR(255) NOT NULL,
    sample_type VARCHAR(100) NOT NULL, -- Blood, Urine, Imaging, Swab
    fasting_required BOOLEAN DEFAULT FALSE,
    turnaround_hours INT DEFAULT 24,
    price_inr DECIMAL(10, 2) NOT NULL,
    description TEXT,
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL,
    INDEX idx_lab_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6. Conversations & Messages
CREATE TABLE IF NOT EXISTS conversations (
    id VARCHAR(64) PRIMARY KEY,
    user_id INT,
    title VARCHAR(255) DEFAULT 'New Clinical Inquiry',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_conv_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    conversation_id VARCHAR(64) NOT NULL,
    sender VARCHAR(20) NOT NULL, -- user, assistant
    content TEXT NOT NULL,
    agent_steps_json JSON,
    triage_payload_json JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
    INDEX idx_msg_conv (conversation_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
