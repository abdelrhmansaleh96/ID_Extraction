#!/usr/bin/env python3
"""
Process users.json file and extract national ID numbers from images
Adds 'national_id_number' field to each user object
"""

import json
import sys
import os
import tempfile
import requests
import logging
import warnings
from utils import detect_and_process_id_card
from pdf2image import convert_from_path, convert_from_bytes

# Suppress all logging and warnings
logging.disable(logging.CRITICAL)
warnings.filterwarnings("ignore")

# Redirect stderr to devnull to suppress warnings
sys.stderr = open(os.devnull, 'w')

# Suppress ultralytics warnings
os.environ['ULTRALYTICS_OFFLINE'] = '1'

def download_file_from_url(url):
    """Download file from URL and save to temporary file"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Determine file extension from URL or content type
        if url.lower().endswith('.pdf'):
            suffix = ".pdf"
        elif url.lower().endswith(('.jpg', '.jpeg')):
            suffix = ".jpg"
        elif url.lower().endswith('.png'):
            suffix = ".png"
        else:
            suffix = ".tmp"
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file.write(response.content)
            return temp_file.name
    except Exception as e:
        raise Exception(f"Failed to download file: {str(e)}")

def convert_pdf_to_image(pdf_path):
    """Convert PDF to images and return all pages as image paths"""
    try:
        # Convert PDF to images (all pages)
        images = convert_from_path(pdf_path, dpi=300)
        
        if not images:
            raise Exception("No pages found in PDF")
        
        # Save all pages as temporary images
        image_paths = []
        for i, image in enumerate(images):
            with tempfile.NamedTemporaryFile(delete=False, suffix=f"_page_{i+1}.jpg") as temp_file:
                image.save(temp_file.name, 'JPEG', quality=95)
                image_paths.append(temp_file.name)
        
        return image_paths
    except Exception as e:
        raise Exception(f"Failed to convert PDF to image: {str(e)}")

def extract_national_id(file_url):
    """Extract national ID from image URL or PDF"""
    temp_file_path = None
    pdf_temp_paths = []
    
    try:
        # Handle URL vs local file
        if file_url.startswith(('http://', 'https://')):
            # Download file from URL
            temp_file_path = download_file_from_url(file_url)
            file_path = temp_file_path
        elif file_url.startswith('file://'):
            # Handle file:// URLs
            file_path = file_url[7:]  # Remove 'file://' prefix
        else:
            # Assume it's a local file path
            file_path = file_url
        
        # Check if it's a PDF file
        if file_path.lower().endswith('.pdf'):
            # Convert PDF to images (all pages)
            pdf_temp_paths = convert_pdf_to_image(file_path)
            
            # Try to extract ID from each page
            for i, image_path in enumerate(pdf_temp_paths):
                try:
                    print(f"    Trying page {i+1}/{len(pdf_temp_paths)}...")
                    first_name, second_name, full_name, national_id, address, birth_date, governorate, gender = detect_and_process_id_card(image_path)
                    
                    if national_id:
                        print(f"    ✅ Found ID on page {i+1}: {national_id}")
                        return national_id
                except Exception as e:
                    print(f"    ❌ Page {i+1} failed: {str(e)}")
                    continue
            
            # If no ID found on any page
            return ""
        else:
            # It's already an image
            first_name, second_name, full_name, national_id, address, birth_date, governorate, gender = detect_and_process_id_card(file_path)
            return national_id if national_id else ""
        
    except Exception as e:
        print(f"Error processing {file_url}: {str(e)}")
        return ""
    finally:
        # Clean up temporary files
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        for pdf_temp_path in pdf_temp_paths:
            if os.path.exists(pdf_temp_path):
                os.remove(pdf_temp_path)

def process_users(input_file, output_file=None):
    """Process users.json and add national_id_number field"""
    
    if output_file is None:
        output_file = input_file  # Overwrite original file
    
    # Read the users.json file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            users = json.load(f)
    except Exception as e:
        print(f"Error reading {input_file}: {str(e)}")
        return
    
    print(f"Processing {len(users)} users...")
    
    # Process each user
    for i, user in enumerate(users):
        print(f"Processing user {i+1}/{len(users)} (ID: {user['user_id']})")
        
        # Extract national ID
        national_id = extract_national_id(user['file'])
        
        # Add national_id_number field
        user['national_id_number'] = national_id
        
        if national_id:
            print(f"  ✅ Extracted ID: {national_id}")
        else:
            print(f"  ❌ Failed to extract ID")
    
    # Save the updated data
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
        print(f"\n✅ Successfully saved updated data to {output_file}")
    except Exception as e:
        print(f"Error saving {output_file}: {str(e)}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python process_users.py <input_file> [output_file]")
        print("Example: python process_users.py users.json")
        print("Example: python process_users.py users.json users_processed.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(input_file):
        print(f"Error: File {input_file} not found")
        sys.exit(1)
    
    process_users(input_file, output_file)

if __name__ == "__main__":
    main()
