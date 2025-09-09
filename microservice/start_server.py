#!/usr/bin/env python3
"""
Startup script for Egyptian ID OCR Microservice
"""
import uvicorn
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("Starting Egyptian ID OCR Microservice...")
    print("Server will be available at: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("Health Check: http://localhost:8000/health")
    print("\nPress Ctrl+C to stop the server\n")
    
    uvicorn.run(
        "microservice:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        access_log=True,
        reload=False
    )
