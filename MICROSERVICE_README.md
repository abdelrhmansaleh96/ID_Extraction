# Egyptian ID OCR Microservice

A robust FastAPI microservice for extracting data from Egyptian ID card images via URL.

## Features

- **URL-based image processing**: Upload images via URL instead of file upload
- **Comprehensive error handling**: Detailed error responses with error codes
- **Image validation**: Validates image format, size, and content
- **Request tracking**: Unique request IDs for monitoring and debugging
- **Health monitoring**: Built-in health checks and uptime tracking
- **Docker support**: Easy deployment with Docker and Docker Compose
- **Auto-generated docs**: Interactive API documentation at `/docs`

## Quick Start

### Using Docker (Recommended)

1. **Build and run with Docker Compose:**

```bash
docker-compose up --build
```

2. **Or build and run with Docker:**

```bash
docker build -t egyptian-id-ocr .
docker run -p 8000:8000 egyptian-id-ocr
```

### Local Development

1. **Install dependencies:**

```bash
pip install -r requirements.txt
```

2. **Run the service:**

```bash
python microservice.py
```

The service will be available at `http://localhost:8000`

## API Endpoints

### 1. Extract ID Data

**POST** `/extract-id`

Extract data from Egyptian ID card image URL.

**Request Body:**

```json
{
  "image_url": "https://example.com/id-card.jpg",
  "request_id": "optional-unique-id"
}
```

**Success Response:**

```json
{
  "success": true,
  "request_id": "uuid-here",
  "extracted_data": {
    "first_name": "أحمد",
    "second_name": "محمد",
    "full_name": "أحمد محمد",
    "national_id": "12345678901234",
    "address": "القاهرة",
    "birth_date": "1990-01-01",
    "governorate": "Cairo",
    "gender": "Male"
  },
  "processing_time": 2.45,
  "timestamp": "2024-01-01T12:00:00Z"
}
```

**Error Response:**

```json
{
  "success": false,
  "request_id": "uuid-here",
  "error": "Invalid image URL or unsupported image format",
  "error_code": "INVALID_URL",
  "detail": "Failed to download image: Connection timeout",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### 2. Validate Image URL

**GET** `/validate-image?image_url=https://example.com/image.jpg`

Validate if an image URL is accessible and contains a valid image.

**Response:**

```json
{
  "valid": true,
  "url": "https://example.com/image.jpg",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### 3. Health Check

**GET** `/health`

Check service health and uptime.

**Response:**

```json
{
  "status": "healthy",
  "version": "2.0.0",
  "timestamp": "2024-01-01T12:00:00Z",
  "uptime": 3600.5
}
```

### 4. Service Info

**GET** `/`

Get basic service information.

**Response:**

```json
{
  "service": "Egyptian ID OCR Microservice",
  "version": "2.0.0",
  "status": "running",
  "docs": "/docs"
}
```

## Error Codes

| Code                | Description                            |
| ------------------- | -------------------------------------- |
| `INVALID_URL`       | Invalid or inaccessible image URL      |
| `DOWNLOAD_FAILED`   | Failed to download image from URL      |
| `INVALID_IMAGE`     | Invalid image format or corrupted file |
| `PROCESSING_FAILED` | Error during ID card processing        |
| `NO_ID_DETECTED`    | No ID card detected in image           |
| `EXTRACTION_FAILED` | Failed to extract data from ID card    |
| `INTERNAL_ERROR`    | Unexpected internal error              |

## Configuration

### Environment Variables

- `PYTHONPATH`: Python path (default: `/app`)
- `PYTHONUNBUFFERED`: Python output buffering (default: `1`)

### Resource Limits (Docker)

- **Memory**: 2GB limit, 1GB reserved
- **CPU**: 1.0 limit, 0.5 reserved

## Usage Examples

### cURL

```bash
# Extract ID data
curl -X POST "http://localhost:8000/extract-id" \
  -H "Content-Type: application/json" \
  -d '{"image_url": "https://example.com/id-card.jpg"}'

# Validate image URL
curl "http://localhost:8000/validate-image?image_url=https://example.com/image.jpg"

# Health check
curl "http://localhost:8000/health"
```

### Python

```python
import requests

# Extract ID data
response = requests.post(
    "http://localhost:8000/extract-id",
    json={"image_url": "https://example.com/id-card.jpg"}
)
data = response.json()

if data["success"]:
    print(f"Name: {data['extracted_data']['full_name']}")
    print(f"National ID: {data['extracted_data']['national_id']}")
else:
    print(f"Error: {data['error']} - {data['detail']}")
```

### JavaScript/Node.js

```javascript
const response = await fetch("http://localhost:8000/extract-id", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    image_url: "https://example.com/id-card.jpg",
  }),
});

const data = await response.json();

if (data.success) {
  console.log(`Name: ${data.extracted_data.full_name}`);
  console.log(`National ID: ${data.extracted_data.national_id}`);
} else {
  console.error(`Error: ${data.error} - ${data.detail}`);
}
```

## Monitoring and Logging

The service includes comprehensive logging with:

- Request/response tracking
- Error logging with stack traces
- Processing time measurement
- Image validation details

Logs are written to stdout in JSON format for easy parsing by log aggregation systems.

## Production Deployment

### Docker Swarm

```bash
docker stack deploy -c docker-compose.yml egyptian-id-ocr
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: egyptian-id-ocr
spec:
  replicas: 3
  selector:
    matchLabels:
      app: egyptian-id-ocr
  template:
    metadata:
      labels:
        app: egyptian-id-ocr
    spec:
      containers:
        - name: egyptian-id-ocr
          image: egyptian-id-ocr:latest
          ports:
            - containerPort: 8000
          resources:
            requests:
              memory: "1Gi"
              cpu: "500m"
            limits:
              memory: "2Gi"
              cpu: "1000m"
```

### Load Balancer Configuration

```nginx
upstream egyptian_id_ocr {
    server egyptian-id-ocr-1:8000;
    server egyptian-id-ocr-2:8000;
    server egyptian-id-ocr-3:8000;
}

server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://egyptian_id_ocr;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Troubleshooting

### Common Issues

1. **Image download fails**: Check URL accessibility and image format
2. **Processing timeout**: Large images may take longer to process
3. **Memory issues**: Ensure sufficient memory allocation
4. **Model loading errors**: Verify model files are present

### Debug Mode

Set log level to DEBUG for detailed processing information:

```bash
export LOG_LEVEL=DEBUG
python microservice.py
```

## API Documentation

Interactive API documentation is available at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## License

This project is licensed under the MIT License.
