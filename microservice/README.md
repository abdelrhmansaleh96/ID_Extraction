# Egyptian ID OCR Microservice

A FastAPI-based microservice for extracting data from Egyptian ID card images.

## Quick Start

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Start the server:

```bash
python start_server.py
```

3. Access the API:

- Server: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## API Endpoints

### POST /extract-id

Extract data from Egyptian ID card image URL

**Request Body:**

```json
{
  "image_url": "https://example.com/id-card.jpg",
  "request_id": "optional-request-id"
}
```

**Response:**

```json
{
  "success": true,
  "request_id": "uuid",
  "extracted_data": {
    "first_name": "Ahmed",
    "second_name": "Mohamed",
    "full_name": "Ahmed Mohamed Ali",
    "national_id": "12345678901234",
    "address": "Cairo, Egypt",
    "birth_date": "01/01/1990",
    "governorate": "Cairo",
    "gender": "Male"
  },
  "processing_time": 2.5,
  "timestamp": "2024-01-01T12:00:00"
}
```

### GET /health

Health check endpoint

### GET /validate-image?image_url=...

Validate if an image URL is accessible

## Testing

Use the provided test scripts or Postman collection for testing the API endpoints.

## Dependencies

- FastAPI for the web framework
- OpenCV for image processing
- PIL/Pillow for image handling
- Pydantic for data validation
- Uvicorn as the ASGI server
