# Egyptian ID OCR Service

A comprehensive OCR solution for Egyptian ID cards with both FastAPI microservice and direct PHP integration options. This service processes ID cards to extract key information including names, addresses, and national IDs, then decodes the national ID to provide additional details like birth date, governorate, and gender.

## Key Features

🔹 **Dual Integration Methods** – FastAPI microservice + Direct PHP integration  
🔹 **Image URL Processing** – Accepts image URLs instead of file uploads  
🔹 **AI-Powered ID Detection** – Automatically detects and crops Egyptian ID cards from images  
🔹 **Advanced OCR** – Extracts Arabic and English text using EasyOCR  
🔹 **Field Extraction & Data Processing** – Captures essential details, including:

- Full Name
- Address
- National ID Number
- Birth Date
- Governorate
- Gender

🔹 **RESTful API** – Clean HTTP endpoints for easy integration with any backend  
🔹 **Multiple Input Formats** – Supports both JSON and form-data requests
🔹 **Database Integration** – Built-in database storage and search capabilities

## Quick Start

### Option 1: FastAPI Microservice

1. **Clone the repository:**

   ```bash
   git clone https://github.com/abdelrhmansaleh96/ID_Extraction.git
   cd ID_Extraction
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the service:**

   ```bash
   python main.py
   ```

4. **Test the API:**
   ```bash
   curl -X POST "http://localhost:8000/extract-id-data-form" \
        -F "image_url=https://example.com/id-card.jpg"
   ```

### Option 2: Direct PHP Integration

1. **Set up Python environment:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Configure PHP integration:**

   ```php
   require_once 'php_integration/EgyptianIDOCR.php';
   $ocr = new EgyptianIDOCR('python3', '/path/to/ID_Extraction/', 60, $pdo);
   ```

3. **Extract data:**
   ```php
   $result = $ocr->extractFromUrl('https://example.com/id-card.jpg');
   ```

## API Endpoints

### Extract ID Data (JSON)

```bash
POST /extract-id-data
Content-Type: application/json

{
  "image_url": "https://example.com/id-card.jpg"
}
```

### Extract ID Data (Form-data)

```bash
POST /extract-id-data-form
Content-Type: multipart/form-data

image_url=https://example.com/id-card.jpg
```

### Health Check

```bash
GET /health
```

## Response Format

```json
{
  "first_name": "أحمد",
  "second_name": "محمد",
  "full_name": "أحمد محمد",
  "national_id": "12345678901234",
  "address": "القاهرة",
  "birth_date": "1990-01-15",
  "governorate": "Cairo",
  "gender": "Male"
}
```

## Integration Examples

### PHP Integration (Direct Method - Recommended)

```php
<?php
require_once 'php_integration/EgyptianIDOCR.php';

// Initialize with database connection
$pdo = new PDO("mysql:host=localhost;dbname=your_db", $username, $password);
$ocr = new EgyptianIDOCR('python3', '/path/to/ID_Extraction/', 60, $pdo);

// Extract from image URL
$result = $ocr->extractFromUrl('https://example.com/id-card.jpg');

if ($result) {
    echo "Name: " . $result['full_name'];
    echo "National ID: " . $result['national_id'];
    // Automatically saved to database!
}
?>
```

### PHP Integration (HTTP API Method)

```php
function extractIDData($imageUrl) {
    $url = 'https://your-ocr-service.com/extract-id-data-form';
    $data = ['image_url' => $imageUrl];

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

    $response = curl_exec($ch);
    curl_close($ch);

    return json_decode($response, true);
}
```

### Python Integration

```python
import requests

def extract_id_data(image_url):
    url = "http://localhost:8000/extract-id-data-form"
    data = {"image_url": image_url}

    response = requests.post(url, data=data)
    return response.json()
```

## Docker Deployment

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "main.py"]
```

## Project Structure

```
ID_Extraction/
├── main.py                    # FastAPI microservice
├── extract_single.py          # Python script for PHP integration
├── utils.py                   # Core OCR logic
├── requirements.txt           # Python dependencies
├── php_integration/           # PHP integration package
│   ├── EgyptianIDOCR.php     # Main PHP class
│   ├── database_schema.sql   # Database schema
│   ├── example_usage.php     # Usage examples
│   ├── test_simple.php       # Test script
│   └── README.md             # PHP integration docs
├── detect_id_card.pt          # ID card detection model
├── detect_odjects.pt          # Field detection model
└── detect_id.pt              # National ID detection model
```

## Why Choose This Service?

✅ **High Accuracy** – Advanced deep learning models ensure precise ID recognition  
✅ **Fast & Automated** – AI speeds up document processing with minimal human effort  
✅ **Dual Integration** – Both HTTP API and direct PHP integration options  
✅ **Database Ready** – Built-in database storage and search capabilities  
✅ **Production Ready** – Built with FastAPI for high performance and reliability  
✅ **Easy Setup** – Simple installation and configuration process

## Model Files Required

Make sure these model files are in the project directory:

- `detect_id_card.pt` – ID card detection model
- `detect_odjects.pt` – Field detection model
- `detect_id.pt` – National ID detection model

## Acknowledgments

This project utilizes:

- [YOLO](https://github.com/ultralytics/yolov5) for object detection
- [EasyOCR](https://github.com/JaidedAI/EasyOCR) for text recognition
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework

## Contact & Support

For questions or feedback, feel free to open an issue or reach out to [abdelrhmansaleh96](https://github.com/abdelrhmansaleh96).

## هI HOPE YOU ENJOY THE EXPERIENCE 💖
