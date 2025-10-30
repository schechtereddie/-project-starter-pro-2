# API Specification

**Version**: 1.0.0  
**Last Updated**: 2025-10-30  
**Status**: Draft  

## Purpose

Define internal and external service interfaces for Project Starter Pro 2, including REST endpoints, request/response formats, authentication, and error handling.

---

## API Architecture

### API Layers

1. **Internal Python APIs**: Module-to-module communication
2. **CLI Interface**: Command-line tool for user interaction
3. **REST API**: HTTP endpoints for local/remote access (optional)
4. **Integration APIs**: External service connectors

### Design Principles

- **RESTful**: Follow REST conventions for HTTP APIs
- **Consistent**: Uniform naming, structure, and patterns
- **Versioned**: Explicit versioning in all APIs
- **Documented**: Self-documenting with OpenAPI/Swagger
- **Secure**: Authentication and authorization on all endpoints
- **Validated**: Input validation at API boundaries

---

## Internal Endpoints

### Base URL (Local Mode)
```
http://localhost:8080/api/v1
```

### Authentication

**Local Mode**: No authentication required (OS-level security)

**Team Mode**: Token-based authentication
```http
Authorization: Bearer <jwt_token>
```

---

## Project Management API

### List Projects

**Endpoint**: `GET /projects`

**Query Parameters**:
- `status` (optional): Filter by status (PLANNING|ACTIVE|PAUSED|COMPLETED|ARCHIVED)
- `type` (optional): Filter by type (software|business|research|personal)
- `tag` (optional): Filter by tag
- `sort` (optional): Sort field (name|created_at|updated_at), default: updated_at
- `order` (optional): Sort order (asc|desc), default: desc
- `limit` (optional): Max results, default: 100
- `offset` (optional): Pagination offset, default: 0

**Response**: `200 OK`
```json
{
  "status": "success",
  "data": {
    "projects": [
      {
        "id": "proj_abc123",
        "name": "My Project",
        "description": "Project description",
        "type": "software",
        "status": "ACTIVE",
        "created_at": "2025-10-30T10:00:00Z",
        "updated_at": "2025-10-30T12:00:00Z",
        "owner": "user_123",
        "tags": ["web", "frontend"],
        "stats": {
          "total_tasks": 25,
          "completed_tasks": 12
        }
      }
    ],
    "total": 1,
    "limit": 100,
    "offset": 0
  }
}
```

### Create Project

**Endpoint**: `POST /projects`

**Request Body**:
```json
{
  "name": "New Project",
  "description": "Project description",
  "type": "software",
  "template_id": "template_123",
  "tags": ["web", "api"],
  "settings": {
    "auto_sync": true,
    "notifications": true
  }
}
```

**Response**: `201 Created`
```json
{
  "status": "success",
  "data": {
    "project": {
      "id": "proj_xyz789",
      "name": "New Project",
      "description": "Project description",
      "type": "software",
      "status": "PLANNING",
      "created_at": "2025-10-30T13:00:00Z",
      "updated_at": "2025-10-30T13:00:00Z",
      "owner": "user_123",
      "tags": ["web", "api"]
    }
  },
  "message": "Project created successfully"
}
```

### Get Project

**Endpoint**: `GET /projects/{id}`

**Response**: `200 OK`
```json
{
  "status": "success",
  "data": {
    "project": {
      "id": "proj_abc123",
      "name": "My Project",
      "description": "Detailed project information",
      "type": "software",
      "status": "ACTIVE",
      "created_at": "2025-10-30T10:00:00Z",
      "updated_at": "2025-10-30T12:00:00Z",
      "owner": "user_123",
      "tags": ["web", "frontend"],
      "milestones": [
        {
          "id": "milestone_1",
          "name": "MVP Release",
          "target_date": "2025-12-31T00:00:00Z",
          "status": "PENDING"
        }
      ],
      "stats": {
        "total_tasks": 25,
        "completed_tasks": 12,
        "total_notes": 15,
        "total_research_items": 8
      }
    }
  }
}
```

### Update Project

**Endpoint**: `PUT /projects/{id}`

**Request Body**:
```json
{
  "name": "Updated Project Name",
  "description": "Updated description",
  "status": "ACTIVE",
  "tags": ["web", "frontend", "react"]
}
```

**Response**: `200 OK`
```json
{
  "status": "success",
  "data": {
    "project": {
      "id": "proj_abc123",
      "name": "Updated Project Name",
      "updated_at": "2025-10-30T14:00:00Z"
    }
  },
  "message": "Project updated successfully"
}
```

### Delete Project

**Endpoint**: `DELETE /projects/{id}`

**Query Parameters**:
- `force` (optional): Permanent delete if true, default: false (soft delete)

**Response**: `204 No Content`

### Archive Project

**Endpoint**: `POST /projects/{id}/archive`

**Response**: `200 OK`
```json
{
  "status": "success",
  "data": {
    "project": {
      "id": "proj_abc123",
      "status": "ARCHIVED",
      "archived_at": "2025-10-30T15:00:00Z"
    }
  },
  "message": "Project archived successfully"
}
```

---

## Notes Management API

### List Notes

**Endpoint**: `GET /projects/{project_id}/notes`

**Query Parameters**:
- `tag` (optional): Filter by tag
- `folder` (optional): Filter by folder path
- `favorite` (optional): Filter favorites (true|false)
- `archived` (optional): Include archived (true|false), default: false
- `sort` (optional): Sort field (title|created_at|updated_at)
- `limit` (optional): Max results, default: 100
- `offset` (optional): Pagination offset

**Response**: `200 OK`
```json
{
  "status": "success",
  "data": {
    "notes": [
      {
        "id": "note_xyz789",
        "project_id": "proj_abc123",
        "title": "Implementation Notes",
        "folder_path": "/docs",
        "tags": ["architecture", "backend"],
        "created_at": "2025-10-30T10:00:00Z",
        "updated_at": "2025-10-30T11:30:00Z",
        "is_favorite": true,
        "ai_summary": "Notes on API architecture..."
      }
    ],
    "total": 1
  }
}
```

### Create Note

**Endpoint**: `POST /projects/{project_id}/notes`

**Request Body**:
```json
{
  "title": "New Note",
  "content": "# Note Content\n\nMarkdown content here...",
  "tags": ["important", "todo"],
  "folder_path": "/docs"
}
```

**Response**: `201 Created`

### Get Note

**Endpoint**: `GET /notes/{id}`

**Response**: `200 OK`
```json
{
  "status": "success",
  "data": {
    "note": {
      "id": "note_xyz789",
      "project_id": "proj_abc123",
      "title": "Implementation Notes",
      "content": "# Implementation Notes\n\n...",
      "tags": ["architecture", "backend"],
      "folder_path": "/docs",
      "attachments": [
        {
          "id": "att_1",
          "name": "diagram.png",
          "path": "attachments/diagram.png",
          "type": "image/png",
          "size": 45678
        }
      ],
      "links": ["note_abc456"],
      "created_at": "2025-10-30T10:00:00Z",
      "updated_at": "2025-10-30T11:30:00Z",
      "ai_summary": "Notes on API architecture design decisions..."
    }
  }
}
```

### Update Note

**Endpoint**: `PUT /notes/{id}`

**Request Body**:
```json
{
  "title": "Updated Title",
  "content": "Updated content...",
  "tags": ["architecture", "backend", "api"]
}
```

**Response**: `200 OK`

### Delete Note

**Endpoint**: `DELETE /notes/{id}`

**Response**: `204 No Content`

### Generate Note Summary

**Endpoint**: `POST /notes/{id}/summary`

**Response**: `200 OK`
```json
{
  "status": "success",
  "data": {
    "summary": "AI-generated summary of the note content...",
    "key_points": [
      "Point 1",
      "Point 2",
      "Point 3"
    ]
  }
}
```

### Search Notes

**Endpoint**: `GET /notes/search`

**Query Parameters**:
- `q` (required): Search query
- `project_id` (optional): Limit to specific project
- `semantic` (optional): Use semantic search (true|false), default: false
- `limit` (optional): Max results, default: 20

**Response**: `200 OK`
```json
{
  "status": "success",
  "data": {
    "results": [
      {
        "note_id": "note_xyz789",
        "title": "Implementation Notes",
        "relevance_score": 0.95,
        "snippet": "...matching content snippet..."
      }
    ],
    "total": 1
  }
}
```

---

## Research Management API

### Import Research Source

**Endpoint**: `POST /projects/{project_id}/research`

**Request Body**:
```json
{
  "url": "https://example.com/article",
  "source_type": "WEB",
  "auto_process": true
}
```

**Response**: `201 Created`
```json
{
  "status": "success",
  "data": {
    "research_item": {
      "id": "research_123",
      "project_id": "proj_abc123",
      "title": "Article Title",
      "source_type": "WEB",
      "url": "https://example.com/article",
      "relevance_score": 0.85,
      "created_at": "2025-10-30T12:00:00Z"
    }
  },
  "message": "Research source imported successfully"
}
```

### List Research Items

**Endpoint**: `GET /projects/{project_id}/research`

**Query Parameters**:
- `source_type` (optional): Filter by type (WEB|PDF|SNIPPET|IMAGE|VIDEO|MANUAL)
- `tag` (optional): Filter by tag
- `min_relevance` (optional): Minimum relevance score (0.0-1.0)
- `sort` (optional): Sort field
- `limit` (optional): Max results

**Response**: `200 OK`

### Get Research Item

**Endpoint**: `GET /research/{id}`

**Response**: `200 OK`
```json
{
  "status": "success",
  "data": {
    "research_item": {
      "id": "research_123",
      "project_id": "proj_abc123",
      "title": "React Best Practices 2025",
      "source_type": "WEB",
      "url": "https://example.com/react-best-practices",
      "summary": "AI-generated summary...",
      "tags": ["react", "javascript"],
      "topics": ["hooks", "performance"],
      "relevance_score": 0.92,
      "facts": [
        {
          "id": "fact_1",
          "text": "React 18 introduces automatic batching",
          "confidence": 0.95
        }
      ],
      "quotes": [
        {
          "id": "quote_1",
          "text": "Always use functional components",
          "author": "Dan Abramov"
        }
      ]
    }
  }
}
```

### Synthesize Research

**Endpoint**: `POST /projects/{project_id}/research/synthesize`

**Request Body**:
```json
{
  "topic": "React Performance Optimization",
  "source_ids": ["research_123", "research_456"]
}
```

**Response**: `200 OK`
```json
{
  "status": "success",
  "data": {
    "synthesis": {
      "topic": "React Performance Optimization",
      "summary": "Combined insights from multiple sources...",
      "key_points": [
        "Use React.memo for expensive components",
        "Implement code splitting",
        "Optimize re-renders"
      ],
      "recommendations": [
        "Start with profiling",
        "Focus on bottlenecks"
      ],
      "sources_used": ["research_123", "research_456"]
    }
  }
}
```

---

## Analytics API

### Get Metrics

**Endpoint**: `GET /projects/{project_id}/metrics`

**Response**: `200 OK`
```json
{
  "status": "success",
  "data": {
    "metrics": {
      "task_completion_rate": 0.48,
      "velocity": 12.5,
      "cycle_time_avg": 3.2,
      "lead_time_avg": 5.8,
      "throughput": 8,
      "work_in_progress": 5,
      "blocked_tasks": 1
    },
    "timestamp": "2025-10-30T12:00:00Z"
  }
}
```

### Generate Report

**Endpoint**: `POST /projects/{project_id}/analytics/reports`

**Request Body**:
```json
{
  "report_type": "VELOCITY",
  "period": {
    "start_date": "2025-10-01T00:00:00Z",
    "end_date": "2025-10-30T23:59:59Z"
  }
}
```

**Response**: `201 Created`
```json
{
  "status": "success",
  "data": {
    "report": {
      "id": "report_123",
      "project_id": "proj_abc123",
      "report_type": "VELOCITY",
      "generated_at": "2025-10-30T12:00:00Z",
      "metrics": {
        "average_velocity": 12.3,
        "velocity_trend": "UP"
      },
      "insights": [
        {
          "type": "OBSERVATION",
          "text": "Velocity increased 15% this month"
        }
      ]
    }
  }
}
```

### Get Predictions

**Endpoint**: `GET /projects/{project_id}/predictions`

**Response**: `200 OK`
```json
{
  "status": "success",
  "data": {
    "predictions": {
      "estimated_completion_date": "2025-12-15T00:00:00Z",
      "confidence": 0.82,
      "assumptions": [
        "Current velocity maintained",
        "No major blockers"
      ]
    }
  }
}
```

### Get Bottlenecks

**Endpoint**: `GET /projects/{project_id}/bottlenecks`

**Response**: `200 OK`
```json
{
  "status": "success",
  "data": {
    "bottlenecks": [
      {
        "type": "BLOCKED_TASKS",
        "severity": "HIGH",
        "description": "3 tasks blocked by external dependency",
        "affected_tasks": ["task_1", "task_2", "task_3"],
        "recommendation": "Follow up with external team"
      }
    ]
  }
}
```

---

## Configuration API

### Get Settings

**Endpoint**: `GET /config`

**Response**: `200 OK`
```json
{
  "status": "success",
  "data": {
    "settings": {
      "system": {
        "version": "1.0.0",
        "log_level": "INFO"
      },
      "features": {
        "analytics": true,
        "research": true
      },
      "user_preferences": {
        "theme_mode": "dark",
        "language": "en"
      }
    }
  }
}
```

### Update Settings

**Endpoint**: `PUT /config`

**Request Body**:
```json
{
  "user_preferences": {
    "theme_mode": "light",
    "notifications_enabled": true
  }
}
```

**Response**: `200 OK`

---

## External Sync API

### Upload Project Data

**Endpoint**: `POST /sync/upload`

**Request Body**:
```json
{
  "project_id": "proj_abc123",
  "target": "cloud",
  "force": false
}
```

**Response**: `200 OK`
```json
{
  "status": "success",
  "data": {
    "sync_result": {
      "project_id": "proj_abc123",
      "files_uploaded": 25,
      "bytes_uploaded": 1048576,
      "duration_ms": 1234,
      "conflicts": []
    }
  },
  "message": "Project data uploaded successfully"
}
```

### Download Project Data

**Endpoint**: `POST /sync/download`

**Request Body**:
```json
{
  "project_id": "proj_abc123",
  "source": "cloud"
}
```

**Response**: `200 OK`

---

## System Status API

### Health Check

**Endpoint**: `GET /status`

**Response**: `200 OK`
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "uptime_seconds": 86400,
  "services": {
    "database": "healthy",
    "cache": "healthy",
    "sync": "healthy"
  }
}
```

### Version Info

**Endpoint**: `GET /version`

**Response**: `200 OK`
```json
{
  "version": "1.0.0",
  "build": "20251030",
  "python_version": "3.13.5",
  "node_version": "20.10.0"
}
```

---

## Error Responses

### Error Format

All errors follow this structure:

```json
{
  "status": "error",
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field": "field_name",
      "constraint": "validation_rule",
      "value": "invalid_value"
    }
  }
}
```

### HTTP Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful GET/PUT |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid input |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Resource conflict |
| 422 | Unprocessable Entity | Validation error |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |

### Error Codes

- `VALIDATION_ERROR`: Input validation failed
- `NOT_FOUND`: Resource not found
- `DUPLICATE`: Resource already exists
- `PERMISSION_DENIED`: Insufficient permissions
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `INTERNAL_ERROR`: Server error

---

## Authentication & Authorization

### Token-Based Auth (Team Mode)

**Login**:
```http
POST /auth/login
Content-Type: application/json

{
  "username": "user@example.com",
  "password": "password123"
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_at": "2025-10-31T12:00:00Z",
    "user": {
      "id": "user_123",
      "name": "John Doe"
    }
  }
}
```

**Using Token**:
```http
GET /projects
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## Rate Limiting

### Limits

- **Anonymous**: 100 requests/hour
- **Authenticated**: 1000 requests/hour
- **Premium**: 10000 requests/hour

### Headers

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1635724800
```

---

## References

- OpenAPI Spec: https://swagger.io/specification/
- REST API Design: https://restfulapi.net/
- JWT: https://jwt.io/

