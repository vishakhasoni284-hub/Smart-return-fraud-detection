

CREATE DATABASE fraud_detection;
USE fraud_detection;
CREATE TABLE admin_settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    platform_id VARCHAR(50) NOT NULL UNIQUE,
    risk_tolerance ENUM('Low', 'Medium', 'High') DEFAULT 'Medium',
    fraud_threshold FLOAT DEFAULT 0.6,
    auto_approve BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE return_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,

    user_id VARCHAR(50),

    account_age INT,
    total_orders INT,
    total_returns INT,

    product_price FLOAT,
    days_after_delivery INT,
    product_condition ENUM('Sealed', 'Opened', 'Damaged'),
    product_category VARCHAR(50),

    high_value BOOLEAN,
    pickup_changed BOOLEAN,
    repeated_reason BOOLEAN,

    fraud_score FLOAT,
    risk_level ENUM('LOW', 'MEDIUM', 'HIGH'),
    decision ENUM('APPROVE', 'MANUAL_REVIEW', 'REJECT'),

    explanation TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) UNIQUE,
    email VARCHAR(100),
    role ENUM('Admin', 'Fraud Analyst'),
    status ENUM('Active', 'Inactive') DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO admin_settings 
(company_name, platform_id, risk_tolerance, fraud_threshold, auto_approve)
VALUES
('DemoMart', 'DM-ECOM-01', 'Medium', 0.6, FALSE);

