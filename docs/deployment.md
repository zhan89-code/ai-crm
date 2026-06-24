# AI CRM Deployment Guide

## Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for frontend build)
- Python 3.11+ (for backend)

## Quick Start

### 1. Clone and configure


### 2. Start all services


This starts:
- PostgreSQL (port 5432)
- Redis (port 6379)
- FastAPI backend (port 8000)
- AI Scoring Service (port 8001)

### 3. Run migrations


### 4. Build frontend


### 5. Access
- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- AI Service: http://localhost:8001

## Environment Variables

### Backend (.env)
| Variable | Default | Description |
|---|---|---|
| DATABASE_URL | postgresql+asyncpg://postgres:postgres@db:5432/aicrm | PostgreSQL connection |
| REDIS_URL | redis://redis:6379/0 | Redis connection |
| SECRET_KEY | change-me-in-production | JWT signing key |
| AI_SERVICE_URL | http://ai-service:8001 | AI microservice URL |
| CORS_ORIGINS | http://localhost:3000 | Allowed origins |

### Frontend (.env)
| Variable | Default | Description |
|---|---|---|
| NEXT_PUBLIC_API_URL | http://localhost:8000 | Backend API URL |

## Production Deployment

### Vercel (Frontend)


### Docker (Backend)


## Health Checks
- Backend: GET /health
- AI Service: GET /api/v1/model/status

## Troubleshooting
- Database connection refused: Ensure db container is healthy ()
- Migration failures: Run  then 
- Frontend build errors: Delete  and  again
