# Proposal: Implement Core Backend (FastAPI + Celery + PostgreSQL)

**Status**: Draft  
**Created**: 2025-10-30  
**Author**: Project Starter Pro 2 Team  
**Type**: Implementation  

## Overview

Implement the core backend infrastructure for Project Starter Pro 2 using FastAPI for the REST API, Celery for asynchronous task processing, and PostgreSQL for data persistence.

## Problem Statement

The project requires a robust, scalable backend that can:
- Handle REST API requests efficiently
- Process long-running AI agent tasks asynchronously
- Store and retrieve project data reliably
- Support real-time updates via WebSocket
- Scale horizontally as usage grows
- Provide observability and monitoring

Without a well-architected backend, the system would suffer from:
- Poor performance under load
- Blocking operations during AI processing
- Data consistency issues
- Difficulty scaling
- Limited monitoring capabilities

## Proposed Solution

Build a production-ready backend using:

1. **FastAPI** - Modern, fast Python web framework
2. **Celery** - Distributed task queue for async processing
3. **PostgreSQL** - Reliable relational database
4. **Redis** - Message broker and caching layer
5. **SQLAlchemy** - ORM for database operations
6. **Alembic** - Database migrations
7. **Pydantic** - Data validation and serialization

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────┐
│                    Client Layer                          │
│              (React Dashboard, CLI)                      │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  FastAPI REST API                        │
│  • Authentication & Authorization                        │
│  • Request validation (Pydantic)                         │
│  • WebSocket endpoints                                   │
│  • API documentation (OpenAPI)                           │
└────────────┬────────────────────────┬───────────────────┘
             │                        │
             ▼                        ▼
┌────────────────────────┐  ┌────────────────────────────┐
│   PostgreSQL Database   │  │    Celery Task Queue       │
│  • Projects             │  │  • AI agent tasks          │
│  • Tasks                │  │  • Research jobs           │
│  • Research             │  │  • Analytics processing    │
│  • Analytics            │  │  • Report generation       │
│  • Users (team mode)    │  │  • Background jobs         │
└────────────────────────┘  └────────────┬───────────────┘
                                         │
                                         ▼
                            ┌────────────────────────────┐
                            │    Redis Message Broker    │
                            │  • Task queue              │
                            │  • Result backend          │
                            │  • Caching layer           │
                            │  • WebSocket pub/sub       │
                            └────────────────────────────┘
```

### Technology Stack

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| **Web Framework** | FastAPI | 0.104+ | REST API, WebSocket |
| **Task Queue** | Celery | 5.3+ | Async task processing |
| **Database** | PostgreSQL | 15+ | Data persistence |
| **Message Broker** | Redis | 7.2+ | Task queue, caching |
| **ORM** | SQLAlchemy | 2.0+ | Database operations |
| **Migrations** | Alembic | 1.12+ | Schema versioning |
| **Validation** | Pydantic | 2.5+ | Data validation |
| **ASGI Server** | Uvicorn | 0.24+ | Production server |

## Scope

### In Scope

#### Phase 1: Foundation
- [ ] FastAPI application setup
- [ ] PostgreSQL database setup
- [ ] SQLAlchemy models and ORM
- [ ] Alembic migrations
- [ ] Basic CRUD endpoints
- [ ] Authentication (JWT)
- [ ] API documentation (OpenAPI/Swagger)

#### Phase 2: Async Processing
- [ ] Celery worker setup
- [ ] Redis configuration
- [ ] Task definitions for AI agents
- [ ] Task status tracking
- [ ] Result storage and retrieval
- [ ] Error handling and retries

#### Phase 3: Real-time Features
- [ ] WebSocket endpoints
- [ ] Real-time task updates
- [ ] Live analytics streaming
- [ ] Notification system

#### Phase 4: Production Readiness
- [ ] Logging and monitoring
- [ ] Health check endpoints
- [ ] Rate limiting
- [ ] CORS configuration
- [ ] Environment configuration
- [ ] Docker containerization

### Out of Scope
- Frontend implementation (separate proposal)
- AI agent implementation (separate proposals)
- Deployment infrastructure (future work)
- Load balancing (future work)

## Database Schema

### Core Tables

#### Projects
```sql
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) NOT NULL,
    type VARCHAR(50),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    archived_at TIMESTAMP,
    metadata JSONB,
    settings JSONB,
    owner_id UUID REFERENCES users(id)
);

CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_projects_owner ON projects(owner_id);
CREATE INDEX idx_projects_created ON projects(created_at DESC);
```

#### Tasks
```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    status VARCHAR(50) NOT NULL,
    priority VARCHAR(20),
    assigned_to UUID REFERENCES users(id),
    due_date TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    metadata JSONB,
    dependencies JSONB
);

CREATE INDEX idx_tasks_project ON tasks(project_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_assigned ON tasks(assigned_to);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
```

#### Research Items
```sql
CREATE TABLE research_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    content TEXT,
    source_url VARCHAR(1000),
    source_type VARCHAR(50),
    credibility_score FLOAT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    metadata JSONB,
    tags TEXT[]
);

CREATE INDEX idx_research_project ON research_items(project_id);
CREATE INDEX idx_research_created ON research_items(created_at DESC);
CREATE INDEX idx_research_tags ON research_items USING GIN(tags);
```

#### Celery Tasks
```sql
CREATE TABLE celery_tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id VARCHAR(255) UNIQUE NOT NULL,
    task_name VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL,
    result JSONB,
    error TEXT,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    metadata JSONB
);

CREATE INDEX idx_celery_task_id ON celery_tasks(task_id);
CREATE INDEX idx_celery_status ON celery_tasks(status);
CREATE INDEX idx_celery_created ON celery_tasks(created_at DESC);
```

#### Users (Team Mode)
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    role VARCHAR(50) NOT NULL DEFAULT 'viewer',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    last_login TIMESTAMP,
    metadata JSONB
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_role ON users(role);
```

## API Endpoints

### Project Management

```python
# Create project
POST /api/v1/projects
Request: {
    "name": "string",
    "description": "string",
    "type": "software|business|research",
    "settings": {}
}
Response: Project

# List projects
GET /api/v1/projects?status=active&limit=20&offset=0
Response: {
    "items": [Project],
    "total": int,
    "limit": int,
    "offset": int
}

# Get project
GET /api/v1/projects/{project_id}
Response: Project

# Update project
PATCH /api/v1/projects/{project_id}
Request: Partial<Project>
Response: Project

# Delete project
DELETE /api/v1/projects/{project_id}
Response: 204 No Content
```

### Task Management

```python
# Create task
POST /api/v1/projects/{project_id}/tasks
Request: {
    "title": "string",
    "description": "string",
    "priority": "low|medium|high",
    "due_date": "datetime"
}
Response: Task

# List tasks
GET /api/v1/projects/{project_id}/tasks?status=active
Response: {
    "items": [Task],
    "total": int
}

# Update task
PATCH /api/v1/tasks/{task_id}
Request: Partial<Task>
Response: Task
```

### Async Task Management

```python
# Start AI agent task
POST /api/v1/agents/research/execute
Request: {
    "project_id": "uuid",
    "topic": "string",
    "depth": "shallow|medium|deep"
}
Response: {
    "task_id": "string",
    "status": "pending",
    "created_at": "datetime"
}

# Get task status
GET /api/v1/tasks/celery/{task_id}
Response: {
    "task_id": "string",
    "status": "pending|running|completed|failed",
    "result": {},
    "error": "string",
    "progress": 0.75
}

# Cancel task
DELETE /api/v1/tasks/celery/{task_id}
Response: 204 No Content
```

### WebSocket Endpoints

```python
# Real-time task updates
WS /api/v1/ws/tasks/{project_id}
Messages: {
    "type": "task_update",
    "task_id": "uuid",
    "status": "string",
    "data": {}
}

# Real-time analytics
WS /api/v1/ws/analytics/{project_id}
Messages: {
    "type": "metric_update",
    "metric": "string",
    "value": number,
    "timestamp": "datetime"
}
```

## Celery Task Definitions

### Research Tasks

```python
@celery_app.task(bind=True, name="agents.research.general")
def research_general_task(self, project_id: str, topic: str, depth: str):
    """Execute general research task."""
    try:
        # Update task status
        self.update_state(state="RUNNING", meta={"progress": 0.1})
        
        # Execute research
        agent = GeneralResearchAgent()
        result = agent.research(topic=topic, depth=depth)
        
        # Store results
        store_research_results(project_id, result)
        
        # Update progress
        self.update_state(state="RUNNING", meta={"progress": 1.0})
        
        return {
            "status": "completed",
            "items_found": len(result.items),
            "quality_score": result.quality_score
        }
    except Exception as e:
        self.update_state(state="FAILURE", meta={"error": str(e)})
        raise
```

### Analytics Tasks

```python
@celery_app.task(name="analytics.generate_report")
def generate_analytics_report(project_id: str, period: str):
    """Generate analytics report."""
    # Collect metrics
    metrics = collect_project_metrics(project_id, period)
    
    # Analyze trends
    trends = analyze_trends(metrics)
    
    # Generate insights
    insights = generate_insights(metrics, trends)
    
    # Store report
    report = store_analytics_report(project_id, {
        "metrics": metrics,
        "trends": trends,
        "insights": insights
    })
    
    return report.id
```

## Configuration

### Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/psp2
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10

# Redis
REDIS_URL=redis://localhost:6379/0
REDIS_CACHE_TTL=3600

# Celery
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2
CELERY_TASK_TRACK_STARTED=true
CELERY_TASK_TIME_LIMIT=3600

# API
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4
API_RELOAD=false

# Security
SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION=3600

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
CORS_CREDENTIALS=true

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

## Project Structure

```
src/backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app
│   ├── config.py               # Configuration
│   ├── database.py             # Database connection
│   ├── dependencies.py         # FastAPI dependencies
│   │
│   ├── models/                 # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── project.py
│   │   ├── task.py
│   │   ├── research.py
│   │   └── user.py
│   │
│   ├── schemas/                # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── project.py
│   │   ├── task.py
│   │   └── user.py
│   │
│   ├── api/                    # API routes
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── projects.py
│   │   │   ├── tasks.py
│   │   │   ├── research.py
│   │   │   ├── analytics.py
│   │   │   └── auth.py
│   │   └── websocket.py
│   │
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   ├── project_service.py
│   │   ├── task_service.py
│   │   └── auth_service.py
│   │
│   ├── tasks/                  # Celery tasks
│   │   ├── __init__.py
│   │   ├── celery_app.py
│   │   ├── research_tasks.py
│   │   └── analytics_tasks.py
│   │
│   └── utils/                  # Utilities
│       ├── __init__.py
│       ├── security.py
│       └── logging.py
│
├── alembic/                    # Database migrations
│   ├── versions/
│   └── env.py
│
├── tests/                      # Tests
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api/
│   ├── test_services/
│   └── test_tasks/
│
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Success Criteria

- [ ] FastAPI application running and serving requests
- [ ] PostgreSQL database configured with all tables
- [ ] Celery workers processing tasks successfully
- [ ] WebSocket connections working
- [ ] All CRUD endpoints functional
- [ ] Authentication and authorization working
- [ ] API documentation auto-generated
- [ ] Health check endpoints responding
- [ ] Logging and monitoring configured
- [ ] Tests passing (>80% coverage)
- [ ] Docker containers building successfully

## Dependencies

- Core system specifications (approved)
- Python 3.13.5+
- PostgreSQL 15+
- Redis 7.2+
- Docker (for containerization)

## Risks & Mitigation

**Risk**: Database performance under load  
**Mitigation**: Proper indexing, connection pooling, query optimization

**Risk**: Celery task failures  
**Mitigation**: Retry logic, error handling, dead letter queues

**Risk**: WebSocket connection stability  
**Mitigation**: Reconnection logic, heartbeat mechanism

## Timeline

- **Week 1**: FastAPI setup, database models, basic CRUD
- **Week 2**: Celery integration, task definitions
- **Week 3**: WebSocket implementation, real-time features
- **Week 4**: Testing, documentation, Docker setup

## Next Steps

1. Create detailed implementation tasks
2. Set up development environment
3. Initialize FastAPI project
4. Configure PostgreSQL and Redis
5. Implement core endpoints
6. Set up Celery workers
7. Add WebSocket support
8. Write tests
9. Create Docker configuration
10. Review and validate

