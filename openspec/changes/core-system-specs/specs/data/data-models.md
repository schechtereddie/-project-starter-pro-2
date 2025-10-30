# Data Models Specification

**Version**: 1.0.0  
**Last Updated**: 2025-10-30  
**Status**: Draft  

## Purpose

Define the data structures, schemas, and persistence strategies for Project Starter Pro 2.

## Data Architecture

### Storage Strategy
- **Primary**: File-based (JSON, YAML, Markdown)
- **Cache**: In-memory + file cache
- **Sync**: Optional cloud storage
- **Backup**: Versioned snapshots

### Data Organization
```
/data/
├── projects/           # Project data
│   └── {project_id}/
│       ├── project.json
│       ├── tasks/
│       ├── research/
│       └── analytics/
├── templates/          # Project templates
├── cache/              # Temporary data
└── backups/            # Versioned backups
```

---

## Core Data Models

### 1. Project

**Purpose**: Represents a project with all its metadata and settings.

**Schema**:
```python
{
    "id": "string (UUID)",
    "name": "string",
    "description": "string",
    "status": "enum (PLANNING|ACTIVE|PAUSED|COMPLETED|ARCHIVED)",
    "type": "string (software|business|research|personal)",
    "created_at": "datetime (ISO 8601)",
    "updated_at": "datetime (ISO 8601)",
    "owner": "string",
    "tags": ["string"],
    "metadata": {
        "version": "string",
        "priority": "enum (LOW|MEDIUM|HIGH|CRITICAL)",
        "visibility": "enum (PRIVATE|TEAM|PUBLIC)",
        "custom": {}
    },
    "settings": {
        "auto_sync": "boolean",
        "notifications": "boolean",
        "analytics_enabled": "boolean",
        "integrations": {}
    },
    "milestones": [
        {
            "id": "string",
            "name": "string",
            "target_date": "datetime",
            "status": "enum (PENDING|COMPLETED|MISSED)"
        }
    ],
    "stats": {
        "total_tasks": "integer",
        "completed_tasks": "integer",
        "total_research_items": "integer",
        "last_activity": "datetime"
    }
}
```

**File**: `/data/projects/{project_id}/project.json`

**Validation Rules**:
- `id` must be unique UUID
- `name` required, 1-200 characters
- `status` must be valid enum value
- `created_at` immutable after creation
- `updated_at` auto-updated on changes

---

### 2. Task

**Purpose**: Represents a unit of work within a project.

**Schema**:
```python
{
    "id": "string (UUID)",
    "project_id": "string (UUID)",
    "title": "string",
    "description": "string",
    "status": "enum (NOT_STARTED|IN_PROGRESS|BLOCKED|COMPLETED|CANCELLED)",
    "priority": "enum (LOW|MEDIUM|HIGH|CRITICAL)",
    "type": "string (feature|bug|chore|research|documentation)",
    "assigned_to": "string",
    "created_by": "string",
    "created_at": "datetime",
    "updated_at": "datetime",
    "started_at": "datetime|null",
    "completed_at": "datetime|null",
    "due_date": "datetime|null",
    "estimated_hours": "float|null",
    "actual_hours": "float|null",
    "dependencies": ["string (task IDs)"],
    "blocked_by": ["string (task IDs)"],
    "tags": ["string"],
    "checklist": [
        {
            "id": "string",
            "text": "string",
            "completed": "boolean"
        }
    ],
    "attachments": [
        {
            "id": "string",
            "name": "string",
            "path": "string",
            "type": "string",
            "size": "integer"
        }
    ],
    "comments": [
        {
            "id": "string",
            "author": "string",
            "text": "string",
            "created_at": "datetime"
        }
    ],
    "metadata": {}
}
```

**File**: `/data/projects/{project_id}/tasks/{task_id}.json`

**Validation Rules**:
- `project_id` must reference existing project
- `dependencies` must not create circular references
- `completed_at` required when status is COMPLETED
- `due_date` must be future date when set

---

### 3. Research

**Purpose**: Stores research data, sources, and synthesized findings.

**Schema**:
```python
{
    "id": "string (UUID)",
    "project_id": "string (UUID)",
    "topic": "string",
    "query": "string",
    "status": "enum (PENDING|IN_PROGRESS|COMPLETED|ARCHIVED)",
    "created_at": "datetime",
    "updated_at": "datetime",
    "sources": [
        {
            "id": "string",
            "type": "enum (WEB|DOCUMENT|API|DATABASE|MANUAL)",
            "url": "string|null",
            "title": "string",
            "author": "string|null",
            "published_date": "datetime|null",
            "retrieved_at": "datetime",
            "content": "string",
            "summary": "string",
            "relevance_score": "float (0-1)",
            "metadata": {}
        }
    ],
    "findings": [
        {
            "id": "string",
            "category": "string",
            "text": "string",
            "source_ids": ["string"],
            "confidence": "float (0-1)",
            "tags": ["string"]
        }
    ],
    "synthesis": {
        "summary": "string",
        "key_points": ["string"],
        "recommendations": ["string"],
        "gaps": ["string"],
        "generated_at": "datetime"
    },
    "tags": ["string"],
    "metadata": {}
}
```

**File**: `/data/projects/{project_id}/research/{research_id}.json`

---

### 4. Analytics Report

**Purpose**: Stores analytical insights and metrics.

**Schema**:
```python
{
    "id": "string (UUID)",
    "project_id": "string (UUID)",
    "report_type": "enum (PROGRESS|VELOCITY|RESOURCE|CUSTOM)",
    "period": {
        "start_date": "datetime",
        "end_date": "datetime"
    },
    "generated_at": "datetime",
    "metrics": {
        "task_completion_rate": "float",
        "velocity": "float",
        "cycle_time_avg": "float",
        "lead_time_avg": "float",
        "throughput": "integer",
        "work_in_progress": "integer",
        "blocked_tasks": "integer"
    },
    "trends": [
        {
            "metric": "string",
            "direction": "enum (UP|DOWN|STABLE)",
            "change_percentage": "float",
            "significance": "enum (LOW|MEDIUM|HIGH)"
        }
    ],
    "insights": [
        {
            "type": "enum (OBSERVATION|WARNING|RECOMMENDATION)",
            "text": "string",
            "priority": "enum (LOW|MEDIUM|HIGH)",
            "data": {}
        }
    ],
    "predictions": {
        "estimated_completion_date": "datetime|null",
        "confidence": "float (0-1)",
        "assumptions": ["string"]
    },
    "visualizations": [
        {
            "type": "string (chart type)",
            "data": {},
            "config": {}
        }
    ]
}
```

**File**: `/data/projects/{project_id}/analytics/{report_id}.json`

---

### 5. Template

**Purpose**: Defines reusable project structures.

**Schema**:
```yaml
id: string (UUID)
name: string
description: string
category: string
version: string (semver)
created_at: datetime
updated_at: datetime
author: string
tags: [string]

variables:
  - name: string
    type: enum (string|number|boolean|choice)
    description: string
    default: any
    required: boolean
    options: [any]  # for choice type

structure:
  directories:
    - path: string
      description: string
  files:
    - path: string
      template: string  # Template content with {{variables}}
      description: string

tasks:
  - title: string
    description: string
    type: string
    priority: enum

integrations:
  - service: string
    config: {}

metadata: {}
```

**File**: `/data/templates/{template_id}.yaml`

---

### 6. Integration Configuration

**Purpose**: Stores external service integration settings.

**Schema**:
```python
{
    "id": "string (UUID)",
    "service": "string (github|gitlab|jira|slack|etc)",
    "name": "string",
    "enabled": "boolean",
    "config": {
        "api_url": "string",
        "api_version": "string",
        "timeout": "integer",
        "retry_attempts": "integer",
        "custom": {}
    },
    "credentials": {
        "type": "enum (API_KEY|OAUTH|TOKEN|BASIC)",
        "encrypted_data": "string",  # Encrypted credentials
        "expires_at": "datetime|null"
    },
    "sync_settings": {
        "enabled": "boolean",
        "direction": "enum (PULL|PUSH|BIDIRECTIONAL)",
        "frequency": "string (cron expression)",
        "last_sync": "datetime|null",
        "next_sync": "datetime|null"
    },
    "mappings": {
        "field_mappings": {},
        "status_mappings": {},
        "custom_mappings": {}
    },
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

**File**: `/config/integrations/{integration_id}.json`

---

### 7. System Configuration

**Purpose**: Global system settings.

**Schema**:
```yaml
system:
  version: string
  data_dir: string
  log_level: enum (DEBUG|INFO|WARN|ERROR)
  log_file: string
  max_cache_size_mb: integer
  auto_cleanup: boolean
  backup_enabled: boolean
  backup_frequency: string

features:
  analytics: boolean
  research: boolean
  integrations: boolean
  cloud_sync: boolean
  ai_assistance: boolean

defaults:
  project_type: string
  task_priority: enum
  notification_enabled: boolean

performance:
  max_concurrent_tasks: integer
  cache_ttl_seconds: integer
  request_timeout_seconds: integer

security:
  encryption_enabled: boolean
  credential_storage: enum (ENV|FILE|KEYRING)
  session_timeout_minutes: integer
```

**File**: `/config/settings.yaml`

---

## Data Relationships

```
Project (1) ──→ (N) Tasks
Project (1) ──→ (N) Research Items
Project (1) ──→ (N) Analytics Reports
Project (1) ──→ (1) Template (optional)

Task (N) ──→ (N) Task Dependencies
Task (1) ──→ (N) Comments
Task (1) ──→ (N) Attachments

Research (1) ──→ (N) Sources
Research (1) ──→ (N) Findings

Integration (N) ──→ (N) Projects
```

## Data Validation

### Validation Strategy
- Schema validation on create/update
- Type checking for all fields
- Referential integrity checks
- Business rule validation
- Custom validators per model

### Validation Tools
- Python: `pydantic` for schema validation
- JSON Schema for file validation
- Custom validators for business logic

---

## Data Migration

### Versioning
- Each model has a `schema_version` field
- Migration scripts in `/scripts/migrations/`
- Backward compatibility for 2 major versions

### Migration Process
1. Detect schema version mismatch
2. Run appropriate migration script
3. Validate migrated data
4. Update schema version
5. Create backup before migration

---

## Performance Considerations

### Indexing
- In-memory indexes for frequently accessed data
- File-based indexes for large datasets
- Lazy loading for heavy objects

### Caching
- LRU cache for recent projects/tasks
- TTL-based cache invalidation
- Cache warming on startup

### Optimization
- Pagination for large lists
- Incremental loading
- Compression for archived data

---

## Backup & Recovery

### Backup Strategy
- Automatic daily backups
- Versioned snapshots
- Incremental backups for large projects

### Recovery
- Point-in-time recovery
- Selective restore (project/task level)
- Validation after restore

**Backup Location**: `/data/backups/{timestamp}/`

---

## References

- JSON Schema: https://json-schema.org/
- Pydantic: https://docs.pydantic.dev/
- YAML Spec: https://yaml.org/spec/

