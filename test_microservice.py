#!/usr/bin/env python3
"""
Test script for the Egyptian ID OCR Microservice
"""

import requests
import json
import time
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"
TEST_IMAGE_URL = "https://via.placeholder.com/400x300/000000/FFFFFF?text=Test+Image"

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        response.raise_for_status()
        data = response.json()
        print(f"✅ Health check passed: {data['status']}")
        print(f"   Version: {data['version']}")
        print(f"   Uptime: {data['uptime']:.2f}s")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_service_info():
    """Test the service info endpoint"""
    print("\n🔍 Testing service info...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        response.raise_for_status()
        data = response.json()
        print(f"✅ Service info: {data['service']} v{data['version']}")
        return True
    except Exception as e:
        print(f"❌ Service info failed: {e}")
        return False

def test_validate_image():
    """Test the image validation endpoint"""
    print("\n🔍 Testing image validation...")
    try:
        response = requests.get(
            f"{BASE_URL}/validate-image",
            params={"image_url": TEST_IMAGE_URL},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        print(f"✅ Image validation: {data['valid']}")
        return True
    except Exception as e:
        print(f"❌ Image validation failed: {e}")
        return False

def test_extract_id_success():
    """Test successful ID extraction"""
    print("\n🔍 Testing ID extraction with valid image...")
    try:
        payload = {
            "image_url": TEST_IMAGE_URL,
            "request_id": f"test-{int(time.time())}"
        }
        
        response = requests.post(
            f"{BASE_URL}/extract-id",
            json=payload,
            timeout=30
        )
        
        data = response.json()
        
        if data.get("success"):
            print("✅ ID extraction completed successfully")
            print(f"   Request ID: {data['request_id']}")
            print(f"   Processing time: {data['processing_time']:.2f}s")
            print(f"   Extracted data: {json.dumps(data['extracted_data'], indent=2)}")
        else:
            print(f"⚠️  ID extraction failed: {data.get('error', 'Unknown error')}")
            print(f"   Error code: {data.get('error_code', 'N/A')}")
            print(f"   Detail: {data.get('detail', 'N/A')}")
        
        return True
    except Exception as e:
        print(f"❌ ID extraction test failed: {e}")
        return False

def test_extract_id_invalid_url():
    """Test ID extraction with invalid URL"""
    print("\n🔍 Testing ID extraction with invalid URL...")
    try:
        payload = {
            "image_url": "https://invalid-url-that-does-not-exist.com/image.jpg",
            "request_id": f"test-invalid-{int(time.time())}"
        }
        
        response = requests.post(
            f"{BASE_URL}/extract-id",
            json=payload,
            timeout=30
        )
        
        data = response.json()
        
        if not data.get("success"):
            print("✅ Invalid URL handled correctly")
            print(f"   Error: {data.get('error', 'Unknown error')}")
            print(f"   Error code: {data.get('error_code', 'N/A')}")
        else:
            print("❌ Invalid URL should have failed")
        
        return True
    except Exception as e:
        print(f"❌ Invalid URL test failed: {e}")
        return False

def test_extract_id_malformed_request():
    """Test ID extraction with malformed request"""
    print("\n🔍 Testing ID extraction with malformed request...")
    try:
        # Send request without required fields
        payload = {
            "invalid_field": "test"
        }
        
        response = requests.post(
            f"{BASE_URL}/extract-id",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 422:
            print("✅ Malformed request handled correctly (422 Unprocessable Entity)")
        else:
            print(f"⚠️  Unexpected response code: {response.status_code}")
        
        return True
    except Exception as e:
        print(f"❌ Malformed request test failed: {e}")
        return False

def run_performance_test():
    """Run a simple performance test"""
    print("\n🔍 Running performance test...")
    try:
        start_time = time.time()
        successful_requests = 0
        failed_requests = 0
        
        for i in range(5):
            payload = {
                "image_url": TEST_IMAGE_URL,
                "request_id": f"perf-test-{i}-{int(time.time())}"
            }
            
            try:
                response = requests.post(
                    f"{BASE_URL}/extract-id",
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    successful_requests += 1
                else:
                    failed_requests += 1
                    
            except Exception:
                failed_requests += 1
        
        total_time = time.time() - start_time
        avg_time = total_time / 5
        
        print(f"✅ Performance test completed")
        print(f"   Total time: {total_time:.2f}s")
        print(f"   Average time per request: {avg_time:.2f}s")
        print(f"   Successful requests: {successful_requests}")
        print(f"   Failed requests: {failed_requests}")
        
        return True
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Egyptian ID OCR Microservice Tests")
    print("=" * 50)
    
    tests = [
        test_health_check,
        test_service_info,
        test_validate_image,
        test_extract_id_success,
        test_extract_id_invalid_url,
        test_extract_id_malformed_request,
        run_performance_test
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed. Check the output above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
