#!/usr/bin/env python3
"""
Simple test script to verify the microservice is working
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_service():
    print("🧪 Testing Egyptian ID OCR Microservice")
    print("=" * 50)
    
    # Test 1: Health check
    print("1. Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Health: {data['status']} (uptime: {data['uptime']:.1f}s)")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
    
    # Test 2: Service info
    print("\n2. Testing service info...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Service: {data['service']} v{data['version']}")
        else:
            print(f"   ❌ Service info failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Service info error: {e}")
    
    # Test 3: Image validation
    print("\n3. Testing image validation...")
    test_urls = [
        "https://picsum.photos/400/300",
        "https://via.placeholder.com/400x300",
        "https://httpbin.org/image/jpeg"
    ]
    
    for url in test_urls:
        try:
            response = requests.get(f"{BASE_URL}/validate-image", params={"image_url": url}, timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"   {'✅' if data['valid'] else '❌'} {url}: {data['valid']}")
            else:
                print(f"   ❌ {url}: HTTP {response.status_code}")
        except Exception as e:
            print(f"   ❌ {url}: {e}")
    
    # Test 4: ID extraction with mock data
    print("\n4. Testing ID extraction...")
    try:
        payload = {
            "image_url": "https://picsum.photos/400/300",
            "request_id": f"test-{int(time.time())}"
        }
        
        response = requests.post(
            f"{BASE_URL}/extract-id",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print("   ✅ ID extraction successful!")
                print(f"   📋 Request ID: {data['request_id']}")
                print(f"   ⏱️  Processing time: {data['processing_time']:.2f}s")
                print(f"   📄 Extracted data:")
                for key, value in data['extracted_data'].items():
                    print(f"      {key}: {value}")
            else:
                print(f"   ❌ ID extraction failed: {data.get('error', 'Unknown error')}")
        else:
            print(f"   ❌ ID extraction HTTP error: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"   ❌ ID extraction error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Testing completed!")

if __name__ == "__main__":
    test_service()
