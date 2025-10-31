# Project Starter Pro 2 - Backend

FastAPI backend with PostgreSQL, Redis, and Celery.

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Start PostgreSQL

```bash
# Using Docker
docker run -d \
  --name psp-postgres \
  -e POSTGRES_USER=psp_user \
  -e POSTGRES_PASSWORD=psp_pass \
  -e POSTGRES_DB=psp \
  -p 5432:5432 \
  postgres:15
```

### 3. Start Redis

```bash
# Using Docker
docker run -d \
  --name psp-redis \
  -p 6379:6379 \
  redis:7
```

### 4. Run Database Migrations

```bash
# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### 5. Start FastAPI Server

```bash
# From project root
uvicorn backend.main:app --reload --port 8000
```

### 6. Start Celery Worker (Optional)

```bash
# From project root
celery -A backend.app.workers.celery_app worker --loglevel=info
```

## API Endpoints

### Health Check
- `GET /` - Root endpoint
- `GET /api/health` - Health check

### Projects
- `POST /api/projects` - Create project
- `GET /api/projects` - List projects
- `GET /api/projects/{id}` - Get project
- `PUT /api/projects/{id}` - Update project
- `DELETE /api/projects/{id}` - Delete project

## API Documentation

Once the server is running:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend/
├── main.py                      # FastAPI application
├── requirements.txt             # Dependencies
├── alembic.ini                  # Alembic config
├── alembic/                     # Database migrations
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
└── app/
    ├── core/
    │   └── config.py           # Settings
    ├── db/
    │   ├── base.py             # Base model
    │   └── session.py          # Database session
    ├── models/
    │   └── project.py          # SQLAlchemy models
    ├── schemas/
    │   └── project.py          # Pydantic schemas
    ├── crud/
    │   └── project.py          # CRUD operations
    ├── api/
    │   └── routes.py           # API routes
    └── workers/
        └── celery_app.py       # Celery tasks
```

## Testing

```bash
# Test API
curl http://localhost:8000/

# Create a project
curl -X POST http://localhost:8000/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Project", "description": "A test project"}'

# List projects
curl http://localhost:8000/api/projects

# Test Celery
python -c "from backend.app.workers.celery_app import test_task; print(test_task.delay().get())"
```

## Configuration

Edit `backend/app/core/config.py` or set environment variables:

- `POSTGRES_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `CELERY_BROKER_URL` - Celery broker URL
- `CELERY_RESULT_BACKEND` - Celery result backend URL

## Development

```bash
# Format code
black backend/

# Lint code
ruff backend/

# Run tests
pytest backend/tests/
```

