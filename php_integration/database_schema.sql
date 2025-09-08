-- Egyptian ID OCR Database Schema
-- This schema stores extracted ID card data

CREATE TABLE IF NOT EXISTS extracted_id_data (
    id INT PRIMARY KEY AUTO_INCREMENT,
    image_url VARCHAR(500) NOT NULL,
    first_name VARCHAR(100) DEFAULT '',
    second_name VARCHAR(100) DEFAULT '',
    full_name VARCHAR(200) DEFAULT '',
    national_id VARCHAR(20) DEFAULT '',
    address TEXT DEFAULT '',
    birth_date DATE NULL,
    governorate VARCHAR(100) DEFAULT '',
    gender ENUM('Male', 'Female', '') DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes for better performance
    INDEX idx_national_id (national_id),
    INDEX idx_created_at (created_at),
    INDEX idx_full_name (full_name),
    INDEX idx_gender (gender)
);

-- Optional: Create a table for processing logs
CREATE TABLE IF NOT EXISTS ocr_processing_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    image_url VARCHAR(500) NOT NULL,
    status ENUM('success', 'error', 'processing') DEFAULT 'processing',
    error_message TEXT NULL,
    processing_time_seconds DECIMAL(10,3) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
);

-- Optional: Create a table for API usage tracking
CREATE TABLE IF NOT EXISTS api_usage_stats (
    id INT PRIMARY KEY AUTO_INCREMENT,
    endpoint VARCHAR(100) NOT NULL,
    method VARCHAR(10) NOT NULL,
    response_time_ms INT NOT NULL,
    status_code INT NOT NULL,
    ip_address VARCHAR(45) NOT NULL,
    user_agent TEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_endpoint (endpoint),
    INDEX idx_status_code (status_code),
    INDEX idx_created_at (created_at)
);
