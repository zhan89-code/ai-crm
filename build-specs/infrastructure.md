# Infrastructure & Deployment

## Docker Compose Stack

version: "3.8"

services:
  db:
    image: pgvector/pgvector:pg15
    environment:
      POSTGRES_DB: ai_crm
      POSTGRES_USER: crm_user
      POSTGRES_PASSWORD: 
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./db/init:/docker-entrypoint-initdb.d
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U crm_user -d ai_crm"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    command: redis-server --requirepass 
    volumes:
      - redisdata:/data

  api:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql+asyncpg://crm_user:@db:5432/ai_crm
      REDIS_URL: redis://:@redis:6379/0
      JWT_SECRET: 
      ENCRYPTION_KEY: 
      SALESFORCE_CLIENT_ID: 
      SALESFORCE_CLIENT_SECRET: 
      HUBSPOT_CLIENT_ID: 
      HUBSPOT_CLIENT_SECRET: 
      AWS_ACCESS_KEY_ID: 
      AWS_SECRET_ACCESS_KEY: 
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    restart: unless-stopped

  ai-service:
    build:
      context: ./ai-service
      dockerfile: Dockerfile
    ports:
      - "8001:8001"
    environment:
      DATABASE_URL: postgresql+asyncpg://crm_user:@db:5432/ai_crm
      REDIS_URL: redis://:@redis:6379/0
      MODEL_BUCKET: s3://ai-crm/models
    depends_on:
      - db
      - redis
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: "2.0"

  celery-worker:
    build:
      context: ./backend
      dockerfile: Dockerfile
    command: celery -A tasks worker --loglevel=info --concurrency=4
    environment:
      DATABASE_URL: postgresql+asyncpg://crm_user:@db:5432/ai_crm
      REDIS_URL: redis://:@redis:6379/0
      ENCRYPTION_KEY: 
      SMTP_HOST: 
      SMTP_PORT: 
      SMTP_USER: 
      SMTP_PASSWORD: 
      FROM_EMAIL: 
    depends_on:
      - db
      - redis
    restart: unless-stopped

  celery-beat:
    build:
      context: ./backend
      dockerfile: Dockerfile
    command: celery -A tasks beat --loglevel=info
    environment:
      REDIS_URL: redis://:@redis:6379/0
    depends_on:
      - redis
    restart: unless-stopped

  web:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      NEXT_PUBLIC_API_URL: http://api:8000
      NEXT_PUBLIC_AI_URL: http://ai-service:8001
    depends_on:
      - api
      - ai-service
    restart: unless-stopped

  minio:
    image: minio/minio
    ports:
      - "9000:9000"
      - "9001:9001"
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: 
      MINIO_ROOT_PASSWORD: 
    volumes:
      - miniodata:/data

volumes:
  pgdata:
  redisdata:
  miniodata:

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| DB_PASSWORD | Yes | PostgreSQL password |
| REDIS_PASSWORD | Yes | Redis password |
| JWT_SECRET | Yes | JWT signing secret (32+ chars) |
| ENCRYPTION_KEY | Yes | Fernet key for token encryption |
| SMTP_HOST | Yes | Email server host |
| SMTP_PORT | Yes | Email server port |
| SMTP_USER | Yes | Email auth user |
| SMTP_PASSWORD | Yes | Email auth password |
| FROM_EMAIL | Yes | Sender email address |
| AWS_ACCESS_KEY_ID | No | For S3 model storage |
| AWS_SECRET_ACCESS_KEY | No | For S3 model storage |
| SF_CLIENT_ID | No | Salesforce OAuth |
| SF_CLIENT_SECRET | No | Salesforce OAuth |
| HS_CLIENT_ID | No | HubSpot OAuth |
| HS_CLIENT_SECRET | No | HubSpot OAuth |
| MINIO_ROOT_USER | No | Local S3 access |
| MINIO_ROOT_PASSWORD | No | Local S3 secret |

## Production Deployment (DigitalOcean)

### Recommended Specs
- App Platform: 2 GB RAM, 2 CPUs (backend + frontend)
- Managed PostgreSQL: 2 GB RAM, 1 CPU, 25GB storage
- Managed Redis: 512MB
- Spaces (S3): 5GB for model artifacts

### Alternative: AWS ECS
- ECS Fargate: 2 vCPU, 4GB RAM (backend service)
- ECS Fargate: 2 vCPU, 4GB RAM (AI service)
- RDS PostgreSQL: db.t3.micro, 20GB
- ElastiCache Redis: cache.t3.micro
- S3 bucket for models

### Health Checks
- GET /health on api (200 on healthy DB connection)
- GET /health on ai-service
- GET / on web (returns 200)

### Monitoring
- Structured JSON logging to stdout
- Health endpoint returns DB connection status + last AI model retrain timestamp
- Celery Flower dashboard for task monitoring (port 5555)

## CI/CD Pipeline
1. Push to main branch
2. Run tests (pytest backend, jest frontend)
3. Build Docker images
4. Push to container registry
5. Deploy to DigitalOcean/AWS
6. Run Alembic migrations
7. Verify health endpoints