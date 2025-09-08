<?php

/**
 * Configuration file for Egyptian ID OCR PHP Integration
 * 
 * Update these settings according to your environment
 */

// Database Configuration
define('DB_HOST', 'localhost');
define('DB_NAME', 'your_database_name');
define('DB_USER', 'your_username');
define('DB_PASS', 'your_password');
define('DB_CHARSET', 'utf8mb4');

// OCR Service Configuration
define('PYTHON_PATH', 'python3');  // Path to Python executable
define('SERVICE_PATH', '/path/to/ID_Extraction/');  // Path to OCR service directory
define('OCR_TIMEOUT', 60);  // Timeout in seconds

// Optional: Logging Configuration
define('LOG_LEVEL', 'INFO');  // DEBUG, INFO, WARNING, ERROR
define('LOG_FILE', '/var/log/egyptian_id_ocr.log');

// Optional: Security Configuration
define('ALLOWED_IMAGE_DOMAINS', [
    'example.com',
    'your-cdn.com',
    // Add trusted domains here
]);

define('MAX_IMAGE_SIZE', 10 * 1024 * 1024);  // 10MB in bytes

// Optional: Rate Limiting
define('RATE_LIMIT_REQUESTS', 100);  // Max requests per hour
define('RATE_LIMIT_WINDOW', 3600);   // Time window in seconds

?>
