#!/usr/bin/env python3
"""
Single image extraction script for PHP integration
This script processes a single image and returns JSON output
"""

import sys
import json
import os
import tempfile
import requests
import logging
import warnings
from utils import detect_and_process_id_card

# Suppress all logging and warnings
logging.disable(logging.CRITICAL)
warnings.filterwarnings("ignore")

# Redirect stderr to devnull to suppress warnings
sys.stderr = open(os.devnull, 'w')

# Suppress ultralytics warnings
os.environ['ULTRALYTICS_OFFLINE'] = '1'

def download_image_from_url(url):
    """Download image from URL and save to temporary file"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file.write(response.content)
            return temp_file.name
    except Exception as e:
        raise Exception(f"Failed to download image: {str(e)}")

def main():
    if len(sys.argv) != 2:
        print(json.dumps({"error": "Usage: python extract_single.py <image_url>"}))
        sys.exit(1)
    
    image_url = sys.argv[1]
    temp_file_path = None
    
    try:
        # Handle URL vs local file
        if image_url.startswith(('http://', 'https://')):
            # Download image from URL
            temp_file_path = download_image_from_url(image_url)
            image_path = temp_file_path
        elif image_url.startswith('file://'):
            # Handle file:// URLs
            image_path = image_url[7:]  # Remove 'file://' prefix
        else:
            # Assume it's a local file path
            image_path = image_url
        
        # Process the image
        first_name, second_name, full_name, national_id, address, birth_date, governorate, gender = detect_and_process_id_card(image_path)
        
        # Create result dictionary
        result = {
            "first_name": first_name,
            "second_name": second_name,
            "full_name": full_name,
            "national_id": national_id,
            "address": address,
            "birth_date": birth_date,
            "governorate": governorate,
            "gender": gender,
            "status": "success"
        }
        
        # Output only JSON (no other output)
        print(json.dumps(result, ensure_ascii=False))
        
    except Exception as e:
        error_result = {
            "error": str(e),
            "status": "error"
        }
        print(json.dumps(error_result, ensure_ascii=False))
        sys.exit(1)
    finally:
        # Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)

if __name__ == "__main__":
    main()
