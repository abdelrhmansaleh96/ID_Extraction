# Egyptian ID OCR Service

A FastAPI backend service that extracts data from Egyptian ID card images via URL.

## Features

- **Image URL Processing**: Accepts image URLs instead of file uploads
- **ID Card Detection**: Automatically detects and crops ID cards from images
- **Text Extraction**: Extracts Arabic and English text using EasyOCR
- **National ID Decoding**: Decodes Egyptian national IDs to extract:
  - Birth Date
  - Governorate
  - Gender

## Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Make sure you have the required model files:
   - `detect_id_card.pt`
   - `detect_odjects.pt`
   - `detect_id.pt`

## Running the Service

```bash
python main.py
```

The service will start on `http://localhost:8000`

## API Endpoints

### POST `/extract-id-data`

Extract data from an Egyptian ID card image URL.

**Request Body:**

```json
{
  "image_url": "https://example.com/path/to/id_card.jpg"
}
```

**Response:**

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

### GET `/health`

Health check endpoint.

**Response:**

```json
{
  "status": "healthy"
}
```

## Testing

Use the provided test script:

```bash
python test_service.py
```

Or test with curl:

```bash
curl -X POST "http://localhost:8000/extract-id-data" \
     -H "Content-Type: application/json" \
     -d '{"image_url": "https://example.com/path/to/id_card.jpg"}'
```

## Error Handling

The service handles various error scenarios:

- Invalid image URLs
- Network timeouts
- Invalid image formats
- Processing errors

## CORS

CORS is enabled for all origins. Configure `allow_origins` in production.

## Production Deployment

For production deployment:

1. Configure CORS properly
2. Add authentication if needed
3. Use a production ASGI server like Gunicorn
4. Add logging and monitoring
5. Set up proper error handling and rate limiting
