# Egyptian ID OCR - PHP Integration

This directory contains everything you need to integrate the Egyptian ID OCR service with your PHP application using the direct execution method. This integration has been tested and is production-ready.

## Overview

The direct PHP integration method calls the Python OCR service directly from PHP using `exec()` or `shell_exec()`. This approach is simple, doesn't require HTTP requests, and works well for single-server deployments. It provides better performance and reliability compared to HTTP API calls.

## ✅ Tested & Working

This integration has been thoroughly tested and successfully extracts:

- **Names** (First, Second, Full)
- **National ID** with automatic decoding
- **Address** information
- **Birth Date** (decoded from National ID)
- **Governorate** (decoded from National ID)
- **Gender** (decoded from National ID)

## Files Included

- `EgyptianIDOCR.php` - Main PHP integration class (299 lines)
- `database_schema.sql` - Database schema for storing results
- `example_usage.php` - Complete usage examples
- `test_simple.php` - Simple test script (no database required)
- `debug_test.php` - Debug script for troubleshooting
- `config.php` - Configuration file template
- `README.md` - This documentation

## Prerequisites

1. **Python Environment**: Python 3.7+ with required packages installed
2. **PHP**: PHP 7.4+ with PDO extension
3. **Database**: MySQL 5.7+ or MariaDB 10.2+
4. **OCR Service**: The main OCR service files in the parent directory

## Installation

### 1. Install Python Dependencies

```bash
cd /path/to/ID_Extraction
pip install -r requirements.txt
```

### 2. Test the Integration (No Database Required)

```bash
cd php_integration
php test_simple.php
```

### 3. Set Up Database (Optional)

```sql
-- Run the database schema
mysql -u your_username -p your_database < database_schema.sql
```

### 4. Configure PHP Class

```php
// Update these paths in your PHP code
$ocr = new EgyptianIDOCR(
    pythonPath: 'python3',                    // Path to Python executable
    servicePath: '/path/to/ID_Extraction/',   // Path to OCR service directory
    timeout: 60,                              // Timeout in seconds
    dbConnection: $pdo                        // Database connection (optional)
);
```

## Usage

### Basic Usage

```php
<?php
require_once 'EgyptianIDOCR.php';

// Initialize with database connection
$pdo = new PDO("mysql:host=localhost;dbname=your_db", $username, $password);
$ocr = new EgyptianIDOCR('python3', '/path/to/ID_Extraction/', 60, $pdo);

// Extract from image URL
$result = $ocr->extractFromUrl('https://example.com/id-card.jpg');

if ($result) {
    echo "Name: " . $result['full_name'];
    echo "National ID: " . $result['national_id'];
    // ... other fields
}
?>
```

### Available Methods

#### `extractFromUrl($imageUrl, $saveToDatabase = true)`

Extract data from an image URL.

**Parameters:**

- `$imageUrl` (string): URL of the image to process
- `$saveToDatabase` (bool): Whether to save results to database

**Returns:** Array with extracted data or `false` on failure

#### `extractFromFile($imagePath, $saveToDatabase = true)`

Extract data from a local image file.

**Parameters:**

- `$imagePath` (string): Path to the local image file
- `$saveToDatabase` (bool): Whether to save results to database

**Returns:** Array with extracted data or `false` on failure

#### `searchByNationalId($nationalId)`

Search for previous extractions by national ID.

**Parameters:**

- `$nationalId` (string): National ID to search for

**Returns:** Array of matching records or `false` on failure

#### `getHistory($limit = 50)`

Get extraction history from database.

**Parameters:**

- `$limit` (int): Number of records to retrieve

**Returns:** Array of recent extractions or `false` on failure

#### `testConnection()`

Test if the OCR service is working.

**Returns:** `true` if working, `false` otherwise

## Response Format

All extraction methods return an array with the following structure:

```php
[
    'first_name' => 'أحمد',
    'second_name' => 'محمد',
    'full_name' => 'أحمد محمد',
    'national_id' => '12345678901234',
    'address' => 'القاهرة',
    'birth_date' => '1990-01-15',
    'governorate' => 'Cairo',
    'gender' => 'Male',
    'status' => 'success'
]
```

## Database Schema

The integration uses three main tables:

### `extracted_id_data`

Stores the extracted ID card information:

- `id` - Primary key
- `image_url` - Original image URL
- `first_name`, `second_name`, `full_name` - Name fields
- `national_id` - National ID number
- `address` - Address information
- `birth_date` - Birth date
- `governorate` - Governorate
- `gender` - Gender (Male/Female)
- `created_at`, `updated_at` - Timestamps

### `ocr_processing_logs`

Optional table for logging processing activities:

- `id` - Primary key
- `image_url` - Processed image URL
- `status` - Processing status
- `error_message` - Error details if failed
- `processing_time_seconds` - Processing duration
- `created_at` - Timestamp

### `api_usage_stats`

Optional table for API usage tracking:

- `id` - Primary key
- `endpoint` - API endpoint used
- `method` - HTTP method
- `response_time_ms` - Response time
- `status_code` - HTTP status code
- `ip_address` - Client IP
- `user_agent` - Client user agent
- `created_at` - Timestamp

## Error Handling

The class includes comprehensive error handling:

```php
$result = $ocr->extractFromUrl($imageUrl);

if ($result === false) {
    // Check error logs for details
    error_log("OCR extraction failed");
    // Handle error appropriately
}
```

## Security Considerations

1. **Input Validation**: Always validate image URLs before processing
2. **File Permissions**: Ensure proper file permissions for the OCR service directory
3. **Database Security**: Use prepared statements (already implemented)
4. **Error Logging**: Monitor error logs for suspicious activity
5. **Resource Limits**: Set appropriate timeouts and memory limits

## Performance Optimization

1. **Caching**: Consider caching results for duplicate requests
2. **Queue System**: For high volume, use a queue system like Redis
3. **Resource Monitoring**: Monitor CPU and memory usage
4. **Database Indexing**: Ensure proper database indexes are in place

## Troubleshooting

### Quick Test

Run the test script to verify everything is working:

```bash
php test_simple.php
```

Expected output:

```
=== Egyptian ID OCR PHP Integration Test ===

1. Testing Python connection...
✅ Python connection successful!

2. Testing OCR extraction with image URL...
✅ Extraction successful! (took ~6s)

=== EXTRACTED DATA ===
First Name: [extracted or "Not detected"]
Second Name: [extracted name]
Full Name: [extracted full name]
National ID: [14-digit number]
Address: [extracted address]
Birth Date: [YYYY-MM-DD format]
Governorate: [Cairo, Alexandria, etc.]
Gender: [Male/Female]
========================
```

### Common Issues

1. **Python Not Found**

   ```
   Error: Command execution failed
   Solution: Update pythonPath in constructor or install Python
   ```

2. **Permission Denied**

   ```
   Error: Permission denied
   Solution: Check file permissions for OCR service directory
   ```

3. **Database Connection Failed**

   ```
   Error: Database connection failed
   Solution: Verify database credentials and connection
   ```

4. **OCR Service Not Working**

   ```
   Error: Failed to parse output
   Solution: Run debug_test.php to see raw output
   ```

5. **Missing Model Files**
   ```
   Error: No such file or directory: 'detect_id_card.pt'
   Solution: Ensure model files are in the service directory
   ```

### Debug Mode

Enable debug logging by setting error reporting:

```php
error_reporting(E_ALL);
ini_set('display_errors', 1);
```

## Example Integration

See `example_usage.php` for complete working examples including:

- Basic extraction from URL
- Local file processing
- Database search functionality
- History retrieval
- Connection testing

## Support

For issues or questions:

1. Check the error logs
2. Verify all prerequisites are met
3. Test with the provided examples
4. Contact the development team

## License

This integration code is part of the Egyptian ID OCR project and follows the same licensing terms.
