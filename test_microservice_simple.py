import os
import tempfile
import requests
import logging
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, HttpUrl, validator
from datetime import datetime
import uuid

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Egyptian ID OCR Microservice - Test Version",
    description="A microservice for extracting data from Egyptian ID card images (Test Mode)",
    version="2.0.0-test",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class ImageUrlRequest(BaseModel):
    image_url: HttpUrl
    request_id: Optional[str] = None
    
    @validator('request_id', pre=True, always=True)
    def generate_request_id(cls, v):
        return v or str(uuid.uuid4())

class IDCardResponse(BaseModel):
    success: bool = True
    request_id: str
    extracted_data: Dict[str, str]
    processing_time: float
    timestamp: str

class ErrorResponse(BaseModel):
    success: bool = False
    request_id: str
    error: str
    error_code: str
    detail: str
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: str
    uptime: float

# Global variables for health monitoring
start_time = datetime.now()

# Error codes
class ErrorCodes:
    INVALID_URL = "INVALID_URL"
    DOWNLOAD_FAILED = "DOWNLOAD_FAILED"
    INVALID_IMAGE = "INVALID_IMAGE"
    PROCESSING_FAILED = "PROCESSING_FAILED"
    NO_ID_DETECTED = "NO_ID_DETECTED"
    EXTRACTION_FAILED = "EXTRACTION_FAILED"
    INTERNAL_ERROR = "INTERNAL_ERROR"

def validate_image_url(url: str) -> bool:
    """Validate if the URL points to a valid image"""
    try:
        # Check if URL is accessible
        response = requests.head(str(url), timeout=10)
        if response.status_code != 200:
            return False
        
        # Check content type - be more lenient for testing
        content_type = response.headers.get('content-type', '').lower()
        valid_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'image/gif']
        
        # If no content-type header, try to access the URL anyway for testing
        if not content_type:
            return True
            
        return any(valid_type in content_type for valid_type in valid_types)
    except Exception:
        # For testing purposes, allow URLs that might not respond to HEAD requests
        return True

def download_image_from_url(url: str, request_id: str) -> str:
    """Download image from URL and save to temporary file with enhanced error handling"""
    try:
        logger.info(f"[{request_id}] Downloading image from URL: {url}")
        
        # Validate URL first
        if not validate_image_url(url):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid image URL or unsupported image format"
            )
        
        response = requests.get(str(url), timeout=30, stream=True)
        response.raise_for_status()
        
        # Check file size (limit to 10MB)
        content_length = response.headers.get('content-length')
        if content_length and int(content_length) > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="Image file too large. Maximum size is 10MB"
            )
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            for chunk in response.iter_content(chunk_size=8192):
                temp_file.write(chunk)
            temp_file_path = temp_file.name
        
        logger.info(f"[{request_id}] Image downloaded successfully to: {temp_file_path}")
        return temp_file_path
        
    except requests.exceptions.Timeout:
        logger.error(f"[{request_id}] Timeout downloading image from URL: {url}")
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail="Request timeout while downloading image"
        )
    except requests.exceptions.RequestException as e:
        logger.error(f"[{request_id}] Request error downloading image: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to download image: {str(e)}"
        )
    except Exception as e:
        logger.error(f"[{request_id}] Unexpected error downloading image: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing image URL: {str(e)}"
        )

def mock_id_extraction(file_path: str, request_id: str) -> Dict[str, str]:
    """Mock ID card extraction for testing purposes"""
    try:
        logger.info(f"[{request_id}] Mock ID card extraction (TEST MODE)")
        
        # Simulate processing time
        import time
        time.sleep(1)  # Simulate processing
        
        # Return mock data
        extracted_data = {
            "first_name": "أحمد",
            "second_name": "محمد",
            "full_name": "أحمد محمد",
            "national_id": "12345678901234",
            "address": "القاهرة، مصر",
            "birth_date": "1990-01-01",
            "governorate": "Cairo",
            "gender": "Male"
        }
        
        logger.info(f"[{request_id}] Mock ID card extraction completed")
        return extracted_data
        
    except Exception as e:
        logger.error(f"[{request_id}] Mock ID card extraction failed: {str(e)}")
        raise

# API Endpoints
@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with service information"""
    return {
        "service": "Egyptian ID OCR Microservice - TEST MODE",
        "version": "2.0.0-test",
        "status": "running",
        "docs": "/docs",
        "note": "This is a test version with mock data"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    uptime = (datetime.now() - start_time).total_seconds()
    return HealthResponse(
        status="healthy",
        version="2.0.0-test",
        timestamp=datetime.now().isoformat(),
        uptime=uptime
    )

@app.post("/extract-id", response_model=IDCardResponse)
async def extract_id_data(request: ImageUrlRequest):
    """
    Extract data from Egyptian ID card image URL (TEST MODE - Returns mock data)
    
    - **image_url**: Valid URL pointing to an image file
    - **request_id**: Optional request identifier (auto-generated if not provided)
    
    Returns mock extracted ID card data for testing purposes.
    """
    request_id = request.request_id
    start_time = datetime.now()
    temp_file_path = None
    
    try:
        logger.info(f"[{request_id}] Processing new ID extraction request (TEST MODE)")
        
        # Download image
        temp_file_path = download_image_from_url(request.image_url, request_id)
        
        # Mock ID extraction
        extracted_data = mock_id_extraction(temp_file_path, request_id)
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        logger.info(f"[{request_id}] Request completed successfully in {processing_time:.2f}s")
        
        return IDCardResponse(
            success=True,
            request_id=request_id,
            extracted_data=extracted_data,
            processing_time=processing_time,
            timestamp=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        processing_time = (datetime.now() - start_time).total_seconds()
        logger.error(f"[{request_id}] Unexpected error: {str(e)}")
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse(
                success=False,
                request_id=request_id,
                error="Internal processing error",
                error_code=ErrorCodes.INTERNAL_ERROR,
                detail=f"An unexpected error occurred: {str(e)}",
                timestamp=datetime.now().isoformat()
            ).dict()
        )
    finally:
        # Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
                logger.info(f"[{request_id}] Temporary file cleaned up: {temp_file_path}")
            except Exception as e:
                logger.warning(f"[{request_id}] Failed to clean up temporary file: {str(e)}")

@app.get("/validate-image")
async def validate_image_endpoint(image_url: str):
    """
    Validate if an image URL is accessible and contains a valid image
    
    - **image_url**: URL to validate
    """
    request_id = str(uuid.uuid4())
    
    try:
        logger.info(f"[{request_id}] Validating image URL: {image_url}")
        
        is_valid = validate_image_url(image_url)
        
        return {
            "valid": is_valid,
            "url": image_url,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"[{request_id}] Validation error: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "valid": False,
                "error": str(e),
                "url": image_url,
                "timestamp": datetime.now().isoformat()
            }
        )

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions with proper error response format"""
    request_id = getattr(request.state, 'request_id', str(uuid.uuid4()))
    
    logger.error(f"[{request_id}] HTTP Exception: {exc.status_code} - {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            success=False,
            request_id=request_id,
            error=exc.detail,
            error_code=ErrorCodes.INTERNAL_ERROR,
            detail=exc.detail,
            timestamp=datetime.now().isoformat()
        ).dict()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    request_id = getattr(request.state, 'request_id', str(uuid.uuid4()))
    
    logger.error(f"[{request_id}] General Exception: {str(exc)}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            success=False,
            request_id=request_id,
            error="Internal server error",
            error_code=ErrorCodes.INTERNAL_ERROR,
            detail="An unexpected error occurred",
            timestamp=datetime.now().isoformat()
        ).dict()
    )

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Egyptian ID OCR Microservice - TEST MODE")
    print("📍 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    print("⚠️  NOTE: This is a test version with mock data")
    print("=" * 60)
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level="info",
        access_log=True
    )
