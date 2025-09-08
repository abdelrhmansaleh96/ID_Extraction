import os
import tempfile
import requests
from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from PIL import Image
import cv2
from utils import detect_and_process_id_card

app = FastAPI(title="Egyptian ID OCR Service", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ImageUrlRequest(BaseModel):
    image_url: HttpUrl

class IDCardResponse(BaseModel):
    first_name: str
    second_name: str
    full_name: str
    national_id: str
    address: str
    birth_date: str
    governorate: str
    gender: str

class ErrorResponse(BaseModel):
    error: str
    detail: str

def download_image_from_url(url: str) -> str:
    """Download image from URL and save to temporary file"""
    try:
        response = requests.get(str(url), timeout=30)
        response.raise_for_status()
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file.write(response.content)
            return temp_file.name
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Failed to download image: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image URL: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Egyptian ID OCR Service", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/extract-id-data", response_model=IDCardResponse)
async def extract_id_data(request: ImageUrlRequest):
    """
    Extract data from Egyptian ID card image URL (JSON format)
    """
    temp_file_path = None
    
    try:
        # Download image from URL
        temp_file_path = download_image_from_url(request.image_url)
        
        # Validate image
        try:
            with Image.open(temp_file_path) as img:
                img.verify()
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid image format")
        
        # Process the image
        first_name, second_name, full_name, national_id, address, birth_date, governorate, gender = detect_and_process_id_card(temp_file_path)
        
        return IDCardResponse(
            first_name=first_name,
            second_name=second_name,
            full_name=full_name,
            national_id=national_id,
            address=address,
            birth_date=birth_date,
            governorate=governorate,
            gender=gender
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")
    finally:
        # Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.post("/extract-id-data-form", response_model=IDCardResponse)
async def extract_id_data_form(image_url: str = Form(...)):
    """
    Extract data from Egyptian ID card image URL (Form-data format)
    """
    temp_file_path = None
    
    try:
        # Clean the URL (remove quotes if present)
        clean_url = image_url.strip().strip('"').strip("'")
        
        # Download image from URL
        temp_file_path = download_image_from_url(clean_url)
        
        # Validate image
        try:
            with Image.open(temp_file_path) as img:
                img.verify()
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid image format")
        
        # Process the image
        first_name, second_name, full_name, national_id, address, birth_date, governorate, gender = detect_and_process_id_card(temp_file_path)
        
        return IDCardResponse(
            first_name=first_name,
            second_name=second_name,
            full_name=full_name,
            national_id=national_id,
            address=address,
            birth_date=birth_date,
            governorate=governorate,
            gender=gender
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")
    finally:
        # Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
