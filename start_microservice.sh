#!/bin/bash

# Egyptian ID OCR Microservice Startup Script

set -e

echo "🚀 Starting Egyptian ID OCR Microservice..."

# Check if Docker is available
if command -v docker &> /dev/null; then
    echo "📦 Docker detected. Starting with Docker Compose..."
    
    # Check if docker-compose is available
    if command -v docker-compose &> /dev/null; then
        docker-compose up --build
    elif command -v docker &> /dev/null && docker compose version &> /dev/null; then
        docker compose up --build
    else
        echo "❌ Docker Compose not found. Building and running with Docker..."
        docker build -t egyptian-id-ocr .
        docker run -p 8000:8000 egyptian-id-ocr
    fi
else
    echo "🐍 Docker not found. Starting with Python..."
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        echo "📦 Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    echo "🔧 Activating virtual environment..."
    source venv/bin/activate
    
    # Install dependencies
    echo "📥 Installing dependencies..."
    pip install -r requirements-microservice.txt
    
    # Start the service
    echo "🎯 Starting microservice..."
    python microservice.py
fi
