#!/bin/bash

# Egyptian ID OCR Microservice Deployment Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="egyptian-id-ocr"
DOCKER_IMAGE="yourusername/egyptian-id-ocr"
VERSION=$(date +%Y%m%d-%H%M%S)

echo -e "${BLUE}🚀 Egyptian ID OCR Microservice Deployment${NC}"
echo "================================================"

# Function to display usage
show_usage() {
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  railway     Deploy to Railway"
    echo "  aws         Deploy to AWS ECS"
    echo "  gcp         Deploy to Google Cloud Run"
    echo "  digitalocean Deploy to DigitalOcean App Platform"
    echo "  dockerhub   Build and push to Docker Hub"
    echo "  local       Run locally with Docker"
    echo "  test        Run tests"
    echo ""
}

# Function to check prerequisites
check_prerequisites() {
    echo -e "${YELLOW}🔍 Checking prerequisites...${NC}"
    
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker is not installed${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Docker is available${NC}"
}

# Function to build Docker image
build_image() {
    echo -e "${YELLOW}🔨 Building Docker image...${NC}"
    docker build -t $DOCKER_IMAGE:$VERSION .
    docker tag $DOCKER_IMAGE:$VERSION $DOCKER_IMAGE:latest
    echo -e "${GREEN}✅ Docker image built successfully${NC}"
}

# Function to deploy to Railway
deploy_railway() {
    echo -e "${YELLOW}🚂 Deploying to Railway...${NC}"
    
    if ! command -v railway &> /dev/null; then
        echo -e "${YELLOW}📥 Installing Railway CLI...${NC}"
        npm install -g @railway/cli
    fi
    
    railway login
    railway init
    railway up
    echo -e "${GREEN}✅ Deployed to Railway${NC}"
}

# Function to deploy to AWS ECS
deploy_aws() {
    echo -e "${YELLOW}☁️  Deploying to AWS ECS...${NC}"
    
    if ! command -v aws &> /dev/null; then
        echo -e "${RED}❌ AWS CLI is not installed${NC}"
        exit 1
    fi
    
    # Build and push to ECR
    aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
    docker tag $DOCKER_IMAGE:latest $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/$PROJECT_NAME:latest
    docker push $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/$PROJECT_NAME:latest
    
    # Update ECS service
    aws ecs update-service --cluster $PROJECT_NAME-cluster --service $PROJECT_NAME-service --force-new-deployment
    
    echo -e "${GREEN}✅ Deployed to AWS ECS${NC}"
}

# Function to deploy to Google Cloud Run
deploy_gcp() {
    echo -e "${YELLOW}🌩️  Deploying to Google Cloud Run...${NC}"
    
    if ! command -v gcloud &> /dev/null; then
        echo -e "${RED}❌ Google Cloud CLI is not installed${NC}"
        exit 1
    fi
    
    # Build and push to Container Registry
    gcloud builds submit --tag gcr.io/$GCP_PROJECT_ID/$PROJECT_NAME:$VERSION .
    
    # Deploy to Cloud Run
    gcloud run deploy $PROJECT_NAME \
        --image gcr.io/$GCP_PROJECT_ID/$PROJECT_NAME:$VERSION \
        --platform managed \
        --region us-central1 \
        --allow-unauthenticated \
        --memory 2Gi \
        --cpu 2 \
        --timeout 300 \
        --max-instances 10
    
    echo -e "${GREEN}✅ Deployed to Google Cloud Run${NC}"
}

# Function to deploy to DigitalOcean
deploy_digitalocean() {
    echo -e "${YELLOW}🌊 Deploying to DigitalOcean App Platform...${NC}"
    
    if ! command -v doctl &> /dev/null; then
        echo -e "${RED}❌ DigitalOcean CLI is not installed${NC}"
        exit 1
    fi
    
    doctl apps create --spec .do/app.yaml
    echo -e "${GREEN}✅ Deployed to DigitalOcean App Platform${NC}"
}

# Function to push to Docker Hub
push_dockerhub() {
    echo -e "${YELLOW}🐳 Pushing to Docker Hub...${NC}"
    
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker is not installed${NC}"
        exit 1
    fi
    
    docker login
    docker push $DOCKER_IMAGE:$VERSION
    docker push $DOCKER_IMAGE:latest
    
    echo -e "${GREEN}✅ Pushed to Docker Hub${NC}"
    echo -e "${BLUE}📦 Image: $DOCKER_IMAGE:latest${NC}"
}

# Function to run locally
run_local() {
    echo -e "${YELLOW}🏠 Running locally with Docker...${NC}"
    docker-compose up --build
}

# Function to run tests
run_tests() {
    echo -e "${YELLOW}🧪 Running tests...${NC}"
    python test_microservice.py
}

# Main script logic
case "${1:-}" in
    "railway")
        check_prerequisites
        deploy_railway
        ;;
    "aws")
        check_prerequisites
        build_image
        deploy_aws
        ;;
    "gcp")
        check_prerequisites
        deploy_gcp
        ;;
    "digitalocean")
        check_prerequisites
        deploy_digitalocean
        ;;
    "dockerhub")
        check_prerequisites
        build_image
        push_dockerhub
        ;;
    "local")
        check_prerequisites
        run_local
        ;;
    "test")
        run_tests
        ;;
    *)
        show_usage
        exit 1
        ;;
esac

echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
