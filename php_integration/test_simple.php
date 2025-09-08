<?php

/**
 * Simple test script for Egyptian ID OCR PHP Integration
 * This test doesn't require a database connection
 */

require_once 'EgyptianIDOCR.php';

echo "=== Egyptian ID OCR PHP Integration Test ===\n\n";

// Test 1: Test Python connection
echo "1. Testing Python connection...\n";
$ocr = new EgyptianIDOCR('python3', __DIR__ . '/../', 60, null);
if ($ocr->testConnection()) {
    echo "✅ Python connection successful!\n\n";
} else {
    echo "❌ Python connection failed!\n";
    echo "Make sure Python 3 is installed and accessible.\n\n";
    exit(1);
}

// Test 2: Test with the working image URL
echo "2. Testing OCR extraction with image URL...\n";
$imageUrl = 'https://mrkoon.s3.eu-north-1.amazonaws.com/images/userPaperFile/68b9b30185af8.jpeg';

echo "Processing image: $imageUrl\n";
$startTime = microtime(true);

$result = $ocr->extractFromUrl($imageUrl, false); // false = don't save to database

$endTime = microtime(true);
$processingTime = round($endTime - $startTime, 2);

if ($result) {
    echo "✅ Extraction successful! (took {$processingTime}s)\n\n";
    echo "=== EXTRACTED DATA ===\n";
    echo "First Name: " . ($result['first_name'] ?: 'Not detected') . "\n";
    echo "Second Name: " . ($result['second_name'] ?: 'Not detected') . "\n";
    echo "Full Name: " . ($result['full_name'] ?: 'Not detected') . "\n";
    echo "National ID: " . ($result['national_id'] ?: 'Not detected') . "\n";
    echo "Address: " . ($result['address'] ?: 'Not detected') . "\n";
    echo "Birth Date: " . (isset($result['birth_date']) ? $result['birth_date'] : 'Not detected') . "\n";
    echo "Governorate: " . (isset($result['governorate']) ? $result['governorate'] : 'Not detected') . "\n";
    echo "Gender: " . (isset($result['gender']) ? $result['gender'] : 'Not detected') . "\n";
    echo "========================\n\n";
} else {
    echo "❌ Extraction failed!\n";
    echo "Check the error logs for more details.\n\n";
}

// Test 3: Test with a different image (if you have one)
echo "3. Testing with a different image...\n";
echo "You can add another image URL here to test with different images.\n";
echo "Example:\n";
echo "\$result = \$ocr->extractFromUrl('https://example.com/another-id.jpg', false);\n\n";

// Test 4: Show system information
echo "4. System Information:\n";
echo "PHP Version: " . PHP_VERSION . "\n";
echo "Python Path: python3\n";
echo "Service Path: " . __DIR__ . "/../\n";
echo "Current Directory: " . getcwd() . "\n\n";

echo "=== Test Complete ===\n";
echo "If all tests passed, your PHP integration is working correctly!\n";
echo "You can now integrate this into your main PHP application.\n";

?>
