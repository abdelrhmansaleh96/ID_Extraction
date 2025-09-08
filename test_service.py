import requests
import json

def test_ocr_service_json(image_url: str):
    """
    Test the OCR service with JSON format
    """
    url = "http://localhost:8000/extract-id-data"
    
    payload = {
        "image_url": image_url
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        data = response.json()
        print("Extracted Data (JSON):")
        print(f"First Name: {data['first_name']}")
        print(f"Second Name: {data['second_name']}")
        print(f"Full Name: {data['full_name']}")
        print(f"National ID: {data['national_id']}")
        print(f"Address: {data['address']}")
        print(f"Birth Date: {data['birth_date']}")
        print(f"Governorate: {data['governorate']}")
        print(f"Gender: {data['gender']}")
        
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return None

def test_ocr_service_form(image_url: str):
    """
    Test the OCR service with form-data format
    """
    url = "http://localhost:8000/extract-id-data-form"
    
    payload = {
        "image_url": image_url
    }
    
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        
        data = response.json()
        print("Extracted Data (Form-data):")
        print(f"First Name: {data['first_name']}")
        print(f"Second Name: {data['second_name']}")
        print(f"Full Name: {data['full_name']}")
        print(f"National ID: {data['national_id']}")
        print(f"Address: {data['address']}")
        print(f"Birth Date: {data['birth_date']}")
        print(f"Governorate: {data['governorate']}")
        print(f"Gender: {data['gender']}")
        
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return None

if __name__ == "__main__":
    # Example usage - replace with your image URL
    test_image_url = "https://mrkoon.s3.eu-north-1.amazonaws.com/images/userPaperFile/68b9b30185af8.jpeg"
    
    print("Testing with JSON format:")
    test_ocr_service_json(test_image_url)
    
    print("\nTesting with Form-data format:")
    test_ocr_service_form(test_image_url)
