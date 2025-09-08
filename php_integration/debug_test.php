<?php

require_once 'EgyptianIDOCR.php';

echo "=== Debug Test ===\n";

$ocr = new EgyptianIDOCR('python3', __DIR__ . '/../', 60, null);

$imageUrl = 'https://mrkoon.s3.eu-north-1.amazonaws.com/images/userPaperFile/68b9b30185af8.jpeg';

echo "Testing with image: $imageUrl\n\n";

$result = $ocr->extractFromUrl($imageUrl, false);

echo "Raw result:\n";
var_dump($result);

echo "\nJSON encoded result:\n";
echo json_encode($result, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);

?>
