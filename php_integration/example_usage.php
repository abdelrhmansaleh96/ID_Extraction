<?php

require_once 'EgyptianIDOCR.php';

// Database configuration
$host = 'localhost';
$dbname = 'your_database_name';
$username = 'your_username';
$password = 'your_password';

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8mb4", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die("Database connection failed: " . $e->getMessage());
}

// Initialize the OCR service
$ocr = new EgyptianIDOCR(
    pythonPath: 'python3',                    // Path to Python executable
    servicePath: '/path/to/ID_Extraction/',   // Path to OCR service directory
    timeout: 60,                              // Timeout in seconds
    dbConnection: $pdo                        // Database connection
);

// Example 1: Extract from image URL
echo "=== Example 1: Extract from Image URL ===\n";

$imageUrl = 'https://mrkoon.s3.eu-north-1.amazonaws.com/images/userPaperFile/68b9b30185af8.jpeg';

$result = $ocr->extractFromUrl($imageUrl, true); // true = save to database

if ($result) {
    echo "Extraction successful!\n";
    echo "First Name: " . $result['first_name'] . "\n";
    echo "Second Name: " . $result['second_name'] . "\n";
    echo "Full Name: " . $result['full_name'] . "\n";
    echo "National ID: " . $result['national_id'] . "\n";
    echo "Address: " . $result['address'] . "\n";
    echo "Birth Date: " . $result['birth_date'] . "\n";
    echo "Governorate: " . $result['governorate'] . "\n";
    echo "Gender: " . $result['gender'] . "\n";
} else {
    echo "Extraction failed!\n";
}

echo "\n";

// Example 2: Extract from local file
echo "=== Example 2: Extract from Local File ===\n";

$localImagePath = '/path/to/local/id_card.jpg';

$result = $ocr->extractFromFile($localImagePath, true);

if ($result) {
    echo "Extraction successful!\n";
    echo "Full Name: " . $result['full_name'] . "\n";
    echo "National ID: " . $result['national_id'] . "\n";
} else {
    echo "Extraction failed!\n";
}

echo "\n";

// Example 3: Search by National ID
echo "=== Example 3: Search by National ID ===\n";

$searchResults = $ocr->searchByNationalId('28906130102292');

if ($searchResults) {
    echo "Found " . count($searchResults) . " records:\n";
    foreach ($searchResults as $record) {
        echo "- " . $record['full_name'] . " (ID: " . $record['national_id'] . ") - " . $record['created_at'] . "\n";
    }
} else {
    echo "No records found.\n";
}

echo "\n";

// Example 4: Get extraction history
echo "=== Example 4: Get Extraction History ===\n";

$history = $ocr->getHistory(10);

if ($history) {
    echo "Recent extractions:\n";
    foreach ($history as $record) {
        echo "- " . $record['full_name'] . " - " . $record['created_at'] . "\n";
    }
} else {
    echo "No history found.\n";
}

echo "\n";

// Example 5: Test connection
echo "=== Example 5: Test Connection ===\n";

if ($ocr->testConnection()) {
    echo "OCR service is working properly.\n";
} else {
    echo "OCR service is not working.\n";
}

?>
