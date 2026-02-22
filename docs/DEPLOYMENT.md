# Deployment Guide

## Overview

This guide covers deploying PromptLab to various environments, from development to production. Choose the deployment strategy that best fits your needs.

---

## Table of Contents

1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment](#cloud-deployment)
4. [Environment Configuration](#environment-configuration)
5. [Database Migration](#database-migration)
6. [Monitoring and Logging](#monitoring-and-logging)
7. [Troubleshooting](#troubleshooting)

---

## Local Development

### Prerequisites

- Python 3.10+
- pip
- Virtual environment tool

### Setup

```bash
# Clone repository
git clone <your-repo-url>
cd promptlab

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Run the application
python main.py
```

### Configuration

Development uses default settings:
- Host: `0.0.0.0`
- Port: `8000`
- Reload: `True` (auto-reload on code changes)
- Storage: In-memory (data lost on restart)

### Access

- **API:** http://localhost:8000
- **Docs:** http://localhost:8000/docs
- **Health:** http://localhost:8000/health

---

## Docker Deployment

### Create Dockerfile

**backend/Dockerfile**:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Create docker-compose.yml

**Root directory**:

```yaml
version: '3.8'

services:
  api:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - ENV=production
      - LOG_LEVEL=info
    restart: unless-stopped
```

### Build and Run

```bash
# Build image
docker build -t promptlab-api ./backend

# Run container
docker run -p 8000:8000 promptlab-api

# Or use docker-compose
docker-compose up -d
```

### Docker Commands

```bash
# View logs
docker logs <container-id>

# Stop container
docker stop <container-id>

# Remove container
docker rm <container-id>

# View running containers
docker ps
```

---

## Cloud Deployment

### Heroku

**1. Create Procfile**:

```
web: uvicorn app.api:app --host 0.0.0.0 --port $PORT
```

**2. Create runtime.txt**:

```
python-3.10.12
```

**3. Deploy**:

```bash
# Login to Heroku
heroku login

# Create app
heroku create promptlab-api

# Deploy
git push heroku main

# Open app
heroku open
```

### AWS EC2

**1. Launch EC2 instance** (Ubuntu 22.04)

**2. SSH into instance**:

```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

**3. Install dependencies**:

```bash
# Update system
sudo apt update
sudo apt upgrade -y

# Install Python
sudo apt install python3.10 python3-pip -y

# Install nginx
sudo apt install nginx -y
```

**4. Deploy application**:

```bash
# Clone repository
git clone <your-repo-url>
cd promptlab/backend

# Install dependencies
pip install -r requirements.txt

# Run with supervisor or systemd
```

**5. Configure Nginx**:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Google Cloud Run

**1. Create Dockerfile** (see Docker section)

**2. Build and push**:

```bash
# Configure gcloud
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Build and push to Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/promptlab-api

# Deploy to Cloud Run
gcloud run deploy promptlab-api \
  --image gcr.io/YOUR_PROJECT_ID/promptlab-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Azure App Service

**1. Install Azure CLI**

**2. Deploy**:

```bash
# Login
az login

# Create resource group
az group create --name promptlab-rg --location eastus

# Create App Service plan
az appservice plan create \
  --name promptlab-plan \
  --resource-group promptlab-rg \
  --sku B1 \
  --is-linux

# Create web app
az webapp create \
  --resource-group promptlab-rg \
  --plan promptlab-plan \
  --name promptlab-api \
  --runtime "PYTHON|3.10"

# Deploy code
az webapp up --name promptlab-api
```

---

## Environment Configuration

### Environment Variables

**Create .env file** (not committed to git):

```bash
# Application
ENV=production
DEBUG=False
LOG_LEVEL=info

# API
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4

# Database (future)
DATABASE_URL=postgresql://user:pass@host:5432/promptlab

# Security (future)
SECRET_KEY=your-secret-key
JWT_SECRET=your-jwt-secret

# CORS
ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
```

### Load Environment Variables

**backend/config.py**:

```python
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    env: str = "development"
    debug: bool = True
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    log_level: str = "info"
    
    class Config:
        env_file = ".env"

settings = Settings()
```

**Use in application**:

```python
from config import settings

if __name__ == "__main__":
    uvicorn.run(
        app, 
        host=settings.api_host,
        port=settings.api_port,
        log_level=settings.log_level
    )
```

---

## Database Migration

### Current State

- In-memory storage (development only)
- Data lost on restart
- Not suitable for production

### Migration to PostgreSQL

**1. Install dependencies**:

```bash
pip install sqlalchemy psycopg2-binary alembic
```

**2. Create database models** (SQLAlchemy):

```python
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PromptDB(Base):
    __tablename__ = "prompts"
    
    id = Column(String, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    description = Column(String(500))
    collection_id = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))
```

**3. Set up Alembic** (migrations):

```bash
alembic init migrations
```

**4. Create migration**:

```bash
alembic revision --autogenerate -m "Initial schema"
```

**5. Run migration**:

```bash
alembic upgrade head
```

**6. Update storage layer** to use database instead of in-memory dictionaries.

---

## Monitoring and Logging

### Logging Configuration

**backend/logging_config.py**:

```python
import logging
import sys

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('app.log')
        ]
    )

# Use in application
logger = logging.getLogger(__name__)
logger.info("Application started")
```

### Health Check Endpoint

Already implemented at `/health`:

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

### Application Monitoring

**Recommended Tools:**

1. **Sentry** - Error tracking
   ```bash
   pip install sentry-sdk
   ```

2. **Prometheus** - Metrics
   ```bash
   pip install prometheus-fastapi-instrumentator
   ```

3. **Datadog** - Full observability

4. **New Relic** - APM

### Example: Sentry Integration

```python
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0,
)
```

---

## Production Checklist

Before deploying to production:

### Security
- [ ] Disable debug mode
- [ ] Change default secret keys
- [ ] Restrict CORS origins
- [ ] Add authentication
- [ ] Use HTTPS/TLS
- [ ] Sanitize inputs
- [ ] Add rate limiting

### Performance
- [ ] Use production database (PostgreSQL)
- [ ] Enable connection pooling
- [ ] Configure caching
- [ ] Optimize queries
- [ ] Use CDN for static files
- [ ] Enable gzip compression

### Reliability
- [ ] Set up auto-restart (systemd/supervisor)
- [ ] Configure health checks
- [ ] Set up backups
- [ ] Add error tracking (Sentry)
- [ ] Configure logging
- [ ] Monitor resource usage

### Deployment
- [ ] Use environment variables
- [ ] Set up CI/CD pipeline
- [ ] Configure auto-scaling
- [ ] Set up load balancing
- [ ] Test disaster recovery

---

## Troubleshooting

### Application won't start

**Check Python version:**
```bash
python --version  # Should be 3.10+
```

**Check dependencies:**
```bash
pip install -r requirements.txt
```

**Check port availability:**
```bash
# Windows
netstat -ano | findstr :8000

# Linux/macOS
lsof -i :8000
```

### Docker issues

**Container exits immediately:**
```bash
# Check logs
docker logs <container-id>

# Run interactively
docker run -it promptlab-api /bin/bash
```

**Can't connect to API:**
```bash
# Check if container is running
docker ps

# Check port mapping
docker port <container-id>
```

### Database connection issues

**Can't connect to database:**
- Check DATABASE_URL is correct
- Verify database is running
- Check firewall rules
- Verify credentials

### Performance issues

**Slow response times:**
- Check database query performance
- Add database indexes
- Enable caching
- Monitor resource usage

**High memory usage:**
- Check for memory leaks
- Optimize data structures
- Add pagination
- Use connection pooling

---

## Backup and Recovery

### Backup Strategy

**Database backups:**
```bash
# PostgreSQL
pg_dump promptlab > backup_$(date +%Y%m%d).sql

# Automated daily backups
0 2 * * * pg_dump promptlab > /backups/backup_$(date +\%Y\%m\%d).sql
```

**Application backups:**
- Code: Stored in Git
- Configuration: Stored in version control
- Data: Regular database backups

### Recovery Process

**Restore from backup:**
```bash
# PostgreSQL
psql promptlab < backup_20260222.sql
```

**Rollback deployment:**
```bash
# Heroku
heroku releases:rollback

# Git
git revert <commit-hash>
git push
```

---

## Scaling Strategies

### Vertical Scaling
- Increase server resources (CPU, RAM)
- Upgrade to larger instance type
- Simple but has limits

### Horizontal Scaling
- Multiple API instances
- Load balancer
- Shared database
- Stateless design (no session storage)

### Database Scaling
- Read replicas
- Connection pooling
- Caching (Redis)
- Database partitioning

---

## Support

For deployment issues:

1. Check this guide
2. Review logs
3. Check documentation
4. Contact team

---

## Additional Resources

- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Docker Documentation](https://docs.docker.com/)
- [Heroku Python](https://devcenter.heroku.com/categories/python-support)
- [AWS EC2](https://docs.aws.amazon.com/ec2/)
- [Google Cloud Run](https://cloud.google.com/run/docs)
