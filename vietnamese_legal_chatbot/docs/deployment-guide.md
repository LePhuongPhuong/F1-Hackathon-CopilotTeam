# 🚀 Deployment Guide - Vietnamese Legal AI Chatbot

## Overview

This guide provides comprehensive instructions for deploying the Vietnamese Legal AI Chatbot in various environments, from local development to production deployment.

## Prerequisites

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **CPU** | 2 cores | 4+ cores |
| **RAM** | 4GB | 8GB+ |
| **Storage** | 10GB | 50GB+ SSD |
| **Python** | 3.8+ | 3.11+ |
| **Network** | 100Mbps | 1Gbps |

### Software Dependencies

- Python 3.8+ with pip
- Git for version control
- Docker (optional, recommended)
- Node.js 16+ (for admin tools)

## Environment Setup

### 1. Local Development

#### Clone Repository
```bash
git clone https://github.com/LePhuongPhuong/F1-Hackathon-CopilotTeam.git
cd F1-Hackathon-CopilotTeam/vietnamese_legal_chatbot
```

#### Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

#### Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Environment Configuration
```bash
# Copy template
cp .env.template .env

# Edit configuration
nano .env  # or use your preferred editor
```

#### Required Environment Variables
```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002

# Pinecone Configuration
PINECONE_API_KEY=your-pinecone-api-key-here
PINECONE_ENVIRONMENT=your-pinecone-environment
PINECONE_INDEX_NAME=vietnamese-legal-docs

# Application Configuration
APP_NAME=Vietnamese Legal AI Chatbot
APP_VERSION=2.0.0
DEBUG_MODE=true
LOG_LEVEL=INFO

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
FRONTEND_PORT=8501

# Security
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=["http://localhost:8501"]

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=3600
```

#### Start Services
```bash
# Option 1: Use development runner
python run_development.py

# Option 2: Start services manually
# Terminal 1 - Backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2 - Frontend
streamlit run app/streamlit_app.py --server.port 8501
```

### 2. Docker Deployment

#### Build Docker Images
```bash
# Backend
docker build -t vietnamese-legal-api:latest -f docker/Dockerfile.backend .

# Frontend
docker build -t vietnamese-legal-frontend:latest -f docker/Dockerfile.frontend .
```

#### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: docker/Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - PINECONE_API_KEY=${PINECONE_API_KEY}
      - PINECONE_ENVIRONMENT=${PINECONE_ENVIRONMENT}
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build:
      context: .
      dockerfile: docker/Dockerfile.frontend
    ports:
      - "8501:8501"
    environment:
      - BACKEND_URL=http://backend:8000
    depends_on:
      - backend
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - backend
      - frontend
    restart: unless-stopped

volumes:
  logs:
```

#### Start with Docker Compose
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 3. Cloud Deployment

#### AWS Deployment

##### EC2 Instance Setup
```bash
# Launch EC2 instance (Ubuntu 22.04 LTS)
# Instance type: t3.medium or larger
# Security groups: Allow ports 22, 80, 443, 8000, 8501

# Connect to instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
sudo systemctl enable docker
sudo systemctl start docker

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

##### Deploy Application
```bash
# Clone repository
git clone https://github.com/LePhuongPhuong/F1-Hackathon-CopilotTeam.git
cd F1-Hackathon-CopilotTeam/vietnamese_legal_chatbot

# Configure environment
cp .env.template .env
nano .env  # Add your API keys

# Start services
docker-compose -f docker-compose.prod.yml up -d
```

##### Load Balancer Setup (ALB)
```bash
# Create Application Load Balancer
# Target groups for backend (8000) and frontend (8501)
# Health checks on /health and /_stcore/health
# SSL certificate from ACM
```

#### Google Cloud Platform

##### Compute Engine Setup
```bash
# Create VM instance
gcloud compute instances create vietnamese-legal-chatbot \
    --zone=asia-southeast1-a \
    --machine-type=e2-medium \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=50GB \
    --tags=http-server,https-server

# SSH into instance
gcloud compute ssh vietnamese-legal-chatbot --zone=asia-southeast1-a
```

##### Cloud Run Deployment
```yaml
# cloudbuild.yaml
steps:
  # Build backend
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/vietnamese-legal-api', '-f', 'docker/Dockerfile.backend', '.']
  
  # Build frontend
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/vietnamese-legal-frontend', '-f', 'docker/Dockerfile.frontend', '.']
  
  # Push images
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/vietnamese-legal-api']
  
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/vietnamese-legal-frontend']
  
  # Deploy to Cloud Run
  - name: 'gcr.io/cloud-builders/gcloud'
    args: ['run', 'deploy', 'vietnamese-legal-api', 
           '--image', 'gcr.io/$PROJECT_ID/vietnamese-legal-api',
           '--platform', 'managed',
           '--region', 'asia-southeast1',
           '--allow-unauthenticated']
```

#### Azure Deployment

##### Container Instances
```bash
# Create resource group
az group create --name vietnamese-legal-rg --location southeastasia

# Create container instances
az container create \
    --resource-group vietnamese-legal-rg \
    --name vietnamese-legal-backend \
    --image vietnamese-legal-api:latest \
    --ports 8000 \
    --environment-variables OPENAI_API_KEY=$OPENAI_API_KEY

az container create \
    --resource-group vietnamese-legal-rg \
    --name vietnamese-legal-frontend \
    --image vietnamese-legal-frontend:latest \
    --ports 8501
```

### 4. Production Deployment

#### Kubernetes Deployment

##### Namespace and ConfigMap
```yaml
# namespace.yml
apiVersion: v1
kind: Namespace
metadata:
  name: vietnamese-legal

---
# configmap.yml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: vietnamese-legal
data:
  APP_NAME: "Vietnamese Legal AI Chatbot"
  APP_VERSION: "2.0.0"
  DEBUG_MODE: "false"
  LOG_LEVEL: "INFO"
```

##### Secrets
```yaml
# secrets.yml
apiVersion: v1
kind: Secret
metadata:
  name: api-secrets
  namespace: vietnamese-legal
type: Opaque
data:
  OPENAI_API_KEY: <base64-encoded-key>
  PINECONE_API_KEY: <base64-encoded-key>
  SECRET_KEY: <base64-encoded-secret>
```

##### Backend Deployment
```yaml
# backend-deployment.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vietnamese-legal-backend
  namespace: vietnamese-legal
spec:
  replicas: 3
  selector:
    matchLabels:
      app: vietnamese-legal-backend
  template:
    metadata:
      labels:
        app: vietnamese-legal-backend
    spec:
      containers:
      - name: backend
        image: vietnamese-legal-api:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: app-config
        - secretRef:
            name: api-secrets
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: vietnamese-legal-backend-service
  namespace: vietnamese-legal
spec:
  selector:
    app: vietnamese-legal-backend
  ports:
  - port: 8000
    targetPort: 8000
  type: ClusterIP
```

##### Frontend Deployment
```yaml
# frontend-deployment.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vietnamese-legal-frontend
  namespace: vietnamese-legal
spec:
  replicas: 2
  selector:
    matchLabels:
      app: vietnamese-legal-frontend
  template:
    metadata:
      labels:
        app: vietnamese-legal-frontend
    spec:
      containers:
      - name: frontend
        image: vietnamese-legal-frontend:latest
        ports:
        - containerPort: 8501
        env:
        - name: BACKEND_URL
          value: "http://vietnamese-legal-backend-service:8000"
        resources:
          requests:
            memory: "256Mi"
            cpu: "125m"
          limits:
            memory: "512Mi"
            cpu: "250m"

---
apiVersion: v1
kind: Service
metadata:
  name: vietnamese-legal-frontend-service
  namespace: vietnamese-legal
spec:
  selector:
    app: vietnamese-legal-frontend
  ports:
  - port: 8501
    targetPort: 8501
  type: ClusterIP
```

##### Ingress
```yaml
# ingress.yml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: vietnamese-legal-ingress
  namespace: vietnamese-legal
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  tls:
  - hosts:
    - legal-ai.gov.vn
    - api.legal-ai.gov.vn
    secretName: vietnamese-legal-tls
  rules:
  - host: legal-ai.gov.vn
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: vietnamese-legal-frontend-service
            port:
              number: 8501
  - host: api.legal-ai.gov.vn
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: vietnamese-legal-backend-service
            port:
              number: 8000
```

## SSL/TLS Configuration

### Let's Encrypt with Certbot
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d legal-ai.gov.vn -d api.legal-ai.gov.vn

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Nginx Configuration
```nginx
# /etc/nginx/sites-available/vietnamese-legal-chatbot
server {
    listen 80;
    server_name legal-ai.gov.vn;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name legal-ai.gov.vn;
    
    ssl_certificate /etc/letsencrypt/live/legal-ai.gov.vn/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/legal-ai.gov.vn/privkey.pem;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

server {
    listen 443 ssl http2;
    server_name api.legal-ai.gov.vn;
    
    ssl_certificate /etc/letsencrypt/live/legal-ai.gov.vn/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/legal-ai.gov.vn/privkey.pem;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Monitoring and Logging

### Prometheus Monitoring
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'vietnamese-legal-backend'
    static_configs:
    - targets: ['localhost:8000']
    metrics_path: '/metrics'
    
  - job_name: 'vietnamese-legal-frontend'
    static_configs:
    - targets: ['localhost:8501']
```

### Grafana Dashboards
```json
{
  "dashboard": {
    "title": "Vietnamese Legal AI Chatbot",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))"
          }
        ]
      }
    ]
  }
}
```

### Logging Configuration
```yaml
# logging.yml
version: 1
formatters:
  standard:
    format: '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
handlers:
  file:
    class: logging.FileHandler
    filename: /app/logs/app.log
    formatter: standard
  console:
    class: logging.StreamHandler
    formatter: standard
loggers:
  app:
    level: INFO
    handlers: [file, console]
root:
  level: INFO
  handlers: [file, console]
```

## Backup and Recovery

### Database Backup
```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"

# Backup Pinecone index metadata
python scripts/backup_pinecone.py --output "$BACKUP_DIR/pinecone_$DATE.json"

# Backup configuration
tar -czf "$BACKUP_DIR/config_$DATE.tar.gz" .env nginx/ docker/

# Backup logs
tar -czf "$BACKUP_DIR/logs_$DATE.tar.gz" logs/

# Cleanup old backups (keep 30 days)
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
find $BACKUP_DIR -name "*.json" -mtime +30 -delete
```

### Disaster Recovery
```bash
#!/bin/bash
# restore.sh
BACKUP_DATE=$1

if [ -z "$BACKUP_DATE" ]; then
    echo "Usage: $0 <backup_date>"
    exit 1
fi

# Restore configuration
tar -xzf "/backups/config_$BACKUP_DATE.tar.gz"

# Restore Pinecone data
python scripts/restore_pinecone.py --input "/backups/pinecone_$BACKUP_DATE.json"

# Restart services
docker-compose restart
```

## Performance Optimization

### Application Tuning
```python
# app/utils/performance.py
import asyncio
from functools import lru_cache

# Cache frequently accessed data
@lru_cache(maxsize=1000)
def get_legal_domain_info(domain_id):
    # Cached domain information
    pass

# Connection pooling
async def setup_connection_pools():
    # Database connection pools
    # HTTP client pools
    pass
```

### Nginx Optimization
```nginx
# nginx.conf
worker_processes auto;
worker_connections 1024;

http {
    # Compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript;
    
    # Caching
    proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=10g
                     inactive=60m use_temp_path=off;
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    
    server {
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_cache my_cache;
            proxy_cache_valid 200 5m;
        }
    }
}
```

## Security Best Practices

### Application Security
- Environment variable encryption
- API key rotation
- Input validation and sanitization
- SQL injection prevention
- XSS protection

### Infrastructure Security
- Firewall configuration
- VPC/Network security
- Container security scanning
- Regular security updates
- Access logging and monitoring

### Compliance
- Vietnamese data protection laws
- Government security standards
- Audit trail maintenance
- Privacy policy implementation

## Troubleshooting

### Common Issues

#### Service Won't Start
```bash
# Check logs
docker-compose logs backend
docker-compose logs frontend

# Check port availability
netstat -tulpn | grep :8000
netstat -tulpn | grep :8501

# Check environment variables
env | grep OPENAI
env | grep PINECONE
```

#### High Memory Usage
```bash
# Monitor resource usage
docker stats

# Check application metrics
curl http://localhost:8000/metrics

# Restart services if needed
docker-compose restart
```

#### API Errors
```bash
# Test API endpoints
curl -X GET http://localhost:8000/health
curl -X POST http://localhost:8000/api/legal-query \
     -H "Content-Type: application/json" \
     -d '{"query": "test"}'

# Check API logs
tail -f logs/api.log
```

---

For additional deployment support, contact: **devops@legal-ai.gov.vn**
