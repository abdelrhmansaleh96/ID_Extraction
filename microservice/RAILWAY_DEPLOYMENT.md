# Railway Deployment Guide

This guide will help you deploy the Egyptian ID OCR Microservice to Railway.

## Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **Railway CLI**: Install the Railway CLI
   ```bash
   npm install -g @railway/cli
   ```
3. **Git Repository**: Your code should be in a Git repository

## Deployment Steps

### Method 1: Using Railway CLI (Recommended)

1. **Login to Railway**:

   ```bash
   railway login
   ```

2. **Initialize Railway project**:

   ```bash
   cd microservice
   railway init
   ```

3. **Deploy to Railway**:
   ```bash
   railway up
   ```

### Method 2: Using Railway Dashboard

1. **Connect GitHub Repository**:

   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Set the root directory to `microservice`

2. **Configure Deployment**:
   - Railway will automatically detect the `railway.json` configuration
   - The service will use the Dockerfile for building
   - Port 8000 will be exposed automatically

## Configuration

The microservice is configured with:

- **Port**: 8000 (automatically exposed by Railway)
- **Health Check**: `/health` endpoint
- **Start Command**: `python3 microservice.py`
- **Restart Policy**: On failure with 10 retries

## Environment Variables

Railway will automatically set:

- `PORT`: The port Railway assigns (usually 8000)
- `RAILWAY_PUBLIC_DOMAIN`: Your service's public URL

## Monitoring

1. **Health Check**: Visit `https://your-app.railway.app/health`
2. **API Documentation**: Visit `https://your-app.railway.app/docs`
3. **Logs**: View logs in the Railway dashboard

## Testing Your Deployment

Once deployed, test your microservice:

```bash
# Health check
curl https://your-app.railway.app/health

# Test ID extraction
curl -X POST "https://your-app.railway.app/extract-id" \
  -H "Content-Type: application/json" \
  -d '{"image_url": "https://example.com/id-card.jpg"}'
```

## Troubleshooting

### Common Issues

1. **Build Failures**:

   - Check that all dependencies are in `requirements.txt`
   - Ensure model files (`.pt`) are included
   - Verify Dockerfile syntax

2. **Runtime Errors**:

   - Check logs in Railway dashboard
   - Ensure all required files are copied to the container
   - Verify Python version compatibility

3. **Memory Issues**:
   - Railway provides limited memory
   - Consider optimizing image processing
   - Monitor memory usage in logs

### Debug Commands

```bash
# View logs
railway logs

# Connect to running container
railway shell

# Check service status
railway status
```

## Scaling

Railway automatically handles:

- Load balancing
- Health checks
- Automatic restarts
- SSL certificates

## Cost Optimization

- Railway charges based on usage
- Monitor your service usage in the dashboard
- Consider pausing the service when not in use

## Security

- Railway provides HTTPS by default
- Environment variables are encrypted
- No need to configure SSL certificates

## Updates

To update your deployment:

1. **Push changes to Git**:

   ```bash
   git add .
   git commit -m "Update microservice"
   git push
   ```

2. **Railway will automatically redeploy**:
   - New builds are triggered on Git pushes
   - Zero-downtime deployments
   - Automatic rollback on failure

## Support

- Railway Documentation: [docs.railway.app](https://docs.railway.app)
- Railway Discord: [discord.gg/railway](https://discord.gg/railway)
- Railway Status: [status.railway.app](https://status.railway.app)
