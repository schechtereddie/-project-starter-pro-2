# Docker Setup Guide

## 🐳 Quick Start

### Prerequisites
- Docker Engine 20.10+
- Docker Compose v2.0+

### Start All Services

```bash
docker compose up --build -d
```

This will start:
- **FastAPI Backend** - http://localhost:8000
- **Celery Worker** - Background task processing
- **PostgreSQL** - Database on port 5432
- **Redis** - Message broker on port 6379

---

## 📋 Service Details

### Backend (FastAPI)
- **Container**: `psp-backend`
- **Port**: 8000
- **Image**: Built from `backend/Dockerfile`
- **Command**: `uvicorn backend.main:app --host 0.0.0.0 --port 8000`

### Celery Worker
- **Container**: `psp-celery`
- **Image**: Built from `backend/Dockerfile.celery`
- **Command**: `celery -A backend.app.workers.celery_app.celery worker --loglevel=info`

### PostgreSQL
- **Container**: `psp-db`
- **Port**: 5432
- **Image**: `postgres:16`
- **Database**: `psp`
- **User**: `psp_user`
- **Password**: `psp_pass`

### Redis
- **Container**: `psp-redis`
- **Port**: 6379
- **Image**: `redis:7`

---

## 🔧 Common Commands

### Start Services
```bash
docker compose up -d
```

### Stop Services
```bash
docker compose down
```

### View Logs
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f celery
docker compose logs -f db
docker compose logs -f redis
```

### Check Status
```bash
docker compose ps
```

### Rebuild After Code Changes
```bash
docker compose up --build -d
```

### Stop and Remove Everything (including volumes)
```bash
docker compose down -v
```

---

## 🗄️ Database Migrations

### Run Migrations Inside Container
```bash
docker compose exec backend alembic upgrade head
```

### Create New Migration
```bash
docker compose exec backend alembic revision --autogenerate -m "description"
```

### Downgrade Migration
```bash
docker compose exec backend alembic downgrade -1
```

---

## 🧪 Testing

### Health Check
```bash
curl http://localhost:8000/api/health
```

### Register User
```bash
curl -X POST "http://localhost:8000/auth/register?username=testuser&password=secret123"
```

### Login
```bash
curl -X POST "http://localhost:8000/auth/login?username=testuser&password=secret123"
```

### API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🔍 Debugging

### Access Container Shell
```bash
# Backend
docker compose exec backend bash

# Database
docker compose exec db psql -U psp_user -d psp
```

### View Container Logs
```bash
docker compose logs -f backend
```

### Restart Single Service
```bash
docker compose restart backend
```

---

## 🌍 Environment Variables

Edit `.env` file to configure:

```env
POSTGRES_URL=postgresql+asyncpg://psp_user:psp_pass@db:5432/psp
REDIS_URL=redis://redis:6379/0
SECRET_KEY=supersecret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## 📊 Volume Management

### List Volumes
```bash
docker volume ls
```

### Inspect Volume
```bash
docker volume inspect project-starter-pro-2_postgres_data
```

### Backup Database
```bash
docker compose exec db pg_dump -U psp_user psp > backup.sql
```

### Restore Database
```bash
docker compose exec -T db psql -U psp_user psp < backup.sql
```

---

## 🚀 Production Deployment

### Build for Production
```bash
docker compose -f docker-compose.prod.yml up --build -d
```

### Environment Variables for Production
Create `.env.production`:
```env
POSTGRES_URL=postgresql+asyncpg://user:pass@prod-db:5432/psp
REDIS_URL=redis://prod-redis:6379/0
SECRET_KEY=<generate-strong-secret>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## 🛠️ Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Database Connection Issues
```bash
# Check if database is ready
docker compose exec db pg_isready -U psp_user
```

### Clear Everything and Start Fresh
```bash
docker compose down -v
docker compose up --build -d
```

### View Resource Usage
```bash
docker stats
```

---

## 📦 Docker Images

### List Images
```bash
docker images
```

### Remove Unused Images
```bash
docker image prune -a
```

### Build Specific Service
```bash
docker compose build backend
```

---

## 🔐 Security Notes

1. **Change default passwords** in production
2. **Use secrets management** for sensitive data
3. **Don't commit `.env`** to version control
4. **Use strong SECRET_KEY** for JWT tokens
5. **Enable SSL/TLS** for production databases

---

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/documentation)
- [Celery Documentation](https://docs.celeryproject.org/)

---

## ✅ Quick Verification Checklist

After running `docker compose up -d`:

- [ ] All 4 containers running: `docker compose ps`
- [ ] Backend accessible: `curl http://localhost:8000/`
- [ ] Health check passing: `curl http://localhost:8000/api/health`
- [ ] Database connected: `docker compose exec db psql -U psp_user -d psp -c "SELECT 1;"`
- [ ] Redis connected: `docker compose exec redis redis-cli ping`
- [ ] Celery worker running: `docker compose logs celery | grep "ready"`
- [ ] API docs accessible: http://localhost:8000/docs

---

**Happy Dockerizing! 🐳**

