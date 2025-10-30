# Data Specification

**Version**: 1.0.0  
**Last Updated**: 2025-10-30  
**Status**: Draft  

## Purpose

Define the persistent and temporary data storage structure for Project Starter Pro 2, including storage design, synchronization strategy, backup procedures, and detailed data schemas.

---

## Storage Design

### Local-First Architecture

Project Starter Pro 2 follows a **local-first** data storage approach:
- All data stored locally in human-readable formats
- No external dependencies required for core functionality
- Optional cloud/NAS sync for backup and multi-device access
- Fast access and offline capability

### Storage Formats

| Data Type | Format | Location | Purpose |
|-----------|--------|----------|---------|
| Project Metadata | JSON | `/data/projects/{id}/project.json` | Structured project data |
| Notes | Markdown | `/data/projects/{id}/notes/*.md` | Human-readable notes |
| Configuration | YAML | `/config/*.yaml` | System and user settings |
| Analytics | JSON | `/data/projects/{id}/analytics/*.json` | Metrics and reports |
| Cache | JSON | `/data/cache/` | Temporary computed data |
| Logs | Text | `/.augment/run.log` | System logs |

### Directory Structure

```
/
├── data/
│   ├── projects/
│   │   └── {project-id}/
│   │       ├── project.json           # Project metadata
│   │       ├── notes/
│   │       │   ├── {note-id}.md       # Individual notes
│   │       │   ├── attachments/       # Note attachments
│   │       │   └── index.json         # Notes index
│   │       ├── research/
│   │       │   ├── {item-id}.json     # Research items
│   │       │   └── files/             # Downloaded sources
│   │       ├── analytics/
│   │       │   ├── reports/           # Generated reports
│   │       │   └── history.json       # Historical metrics
│   │       ├── tasks/
│   │       │   └── {task-id}.json     # Task data
│   │       └── files/                 # Project files
│   ├── templates/
│   │   └── {template-id}.yaml         # Project templates
│   ├── cache/
│   │   ├── research/                  # Cached web content
│   │   ├── analytics/                 # Computed metrics
│   │   └── search/                    # Search indexes
│   └── backups/
│       └── {timestamp}/               # Versioned backups
├── config/
│   ├── settings.yaml                  # System settings
│   ├── user-preferences.yaml          # User preferences
│   ├── theme.yaml                     # Theme configuration
│   ├── integrations/
│   │   └── {service}.json             # Integration configs (encrypted)
│   └── .env.sample                    # Environment template
└── .augment/
    ├── state.json                     # Agent state
    ├── run.log                        # Execution logs
    ├── versions.txt                   # Tool versions
    └── tmp/                           # Temporary files
```

---

## Data Schemas

### 1. Project Data (`project.json`)

```json
{
  "id": "proj_abc123",
  "name": "My Project",
  "description": "Project description",
  "type": "software",
  "status": "ACTIVE",
  "created_at": "2025-10-30T10:00:00Z",
  "updated_at": "2025-10-30T12:00:00Z",
  "owner": "user_123",
  "tags": ["web", "frontend", "react"],
  "metadata": {
    "version": "1.0.0",
    "priority": "HIGH",
    "visibility": "PRIVATE",
    "custom": {}
  },
  "settings": {
    "auto_sync": true,
    "notifications": true,
    "analytics_enabled": true,
    "integrations": {
      "github": {
        "enabled": true,
        "repo": "owner/repo"
      }
    }
  },
  "milestones": [
    {
      "id": "milestone_1",
      "name": "MVP Release",
      "target_date": "2025-12-31T00:00:00Z",
      "status": "PENDING",
      "progress": 0.45
    }
  ],
  "stats": {
    "total_tasks": 25,
    "completed_tasks": 12,
    "total_notes": 15,
    "total_research_items": 8,
    "last_activity": "2025-10-30T12:00:00Z"
  },
  "folders": [
    {
      "path": "/docs",
      "description": "Documentation"
    },
    {
      "path": "/src",
      "description": "Source code"
    }
  ]
}
```

### 2. Note Data (`{note-id}.md`)

**Frontmatter + Content**:
```markdown
---
id: note_xyz789
project_id: proj_abc123
title: "Implementation Notes"
tags: [architecture, backend, api]
folder_path: /docs/architecture
created_at: 2025-10-30T10:00:00Z
updated_at: 2025-10-30T11:30:00Z
version: 3
is_favorite: true
is_archived: false
attachments:
  - id: att_1
    name: diagram.png
    path: attachments/diagram.png
    type: image/png
    size: 45678
links:
  - note_abc456
  - note_def789
ai_summary: "Notes on API architecture design decisions..."
ai_tags: [rest, microservices, scalability]
---

# Implementation Notes

## Overview

Detailed notes about the implementation...

## Key Decisions

1. Use REST API architecture
2. Implement microservices pattern
3. ...

## Code Examples

\`\`\`python
def example():
    pass
\`\`\`
```

### 3. Research Item (`{item-id}.json`)

```json
{
  "id": "research_123",
  "project_id": "proj_abc123",
  "title": "React Best Practices 2025",
  "source_type": "WEB",
  "url": "https://example.com/react-best-practices",
  "content": "Full extracted content...",
  "summary": "AI-generated summary of the article...",
  "tags": ["react", "javascript", "frontend"],
  "topics": ["hooks", "performance", "testing"],
  "relevance_score": 0.92,
  "facts": [
    {
      "id": "fact_1",
      "text": "React 18 introduces automatic batching",
      "confidence": 0.95,
      "source_location": "paragraph 3",
      "verified": true
    }
  ],
  "quotes": [
    {
      "id": "quote_1",
      "text": "Always use functional components with hooks",
      "author": "Dan Abramov",
      "context": "Discussion on modern React patterns",
      "page": null
    }
  ],
  "metadata": {
    "author": "John Doe",
    "published_date": "2025-10-15T00:00:00Z",
    "publisher": "Example Blog",
    "word_count": 2500
  },
  "created_at": "2025-10-30T10:00:00Z",
  "updated_at": "2025-10-30T10:05:00Z",
  "annotations": [
    {
      "id": "ann_1",
      "text": "Important for our project",
      "location": "section 2",
      "created_at": "2025-10-30T10:10:00Z"
    }
  ]
}
```

### 4. Analytics Data (`analytics/history.json`)

```json
{
  "project_id": "proj_abc123",
  "snapshots": [
    {
      "timestamp": "2025-10-30T00:00:00Z",
      "metrics": {
        "task_completion_rate": 0.48,
        "velocity": 12.5,
        "cycle_time_avg": 3.2,
        "lead_time_avg": 5.8,
        "throughput": 8,
        "work_in_progress": 5,
        "blocked_tasks": 1
      }
    },
    {
      "timestamp": "2025-10-29T00:00:00Z",
      "metrics": {
        "task_completion_rate": 0.44,
        "velocity": 11.0,
        "cycle_time_avg": 3.5,
        "lead_time_avg": 6.1,
        "throughput": 7,
        "work_in_progress": 6,
        "blocked_tasks": 2
      }
    }
  ],
  "reports": [
    {
      "id": "report_1",
      "type": "VELOCITY",
      "generated_at": "2025-10-30T12:00:00Z",
      "file": "reports/velocity_2025-10-30.json"
    }
  ]
}
```

### 5. Configuration (`config/settings.yaml`)

```yaml
system:
  version: "1.0.0"
  data_dir: "/data"
  log_level: "INFO"
  log_file: "/.augment/run.log"
  max_cache_size_mb: 1024
  auto_cleanup: true
  backup_enabled: true
  backup_frequency: "daily"
  backup_retention_days: 30

features:
  analytics: true
  research: true
  integrations: true
  cloud_sync: false
  ai_assistance: true

defaults:
  project_type: "software"
  task_priority: "MEDIUM"
  notification_enabled: true
  auto_save_interval_seconds: 30

performance:
  max_concurrent_tasks: 10
  cache_ttl_seconds: 3600
  request_timeout_seconds: 30
  search_index_update_interval: 300

security:
  encryption_enabled: true
  credential_storage: "ENV"
  session_timeout_minutes: 1440
  max_login_attempts: 5
```

### 6. User Preferences (`config/user-preferences.yaml`)

```yaml
user:
  id: "user_123"
  name: "John Doe"
  email: "john@example.com"

preferences:
  default_project_type: "software"
  notifications_enabled: true
  language: "en"
  timezone: "America/New_York"
  date_format: "YYYY-MM-DD"
  time_format: "24h"
  auto_save: true
  keyboard_shortcuts:
    new_project: "Ctrl+N"
    new_note: "Ctrl+Shift+N"
    search: "Ctrl+F"

ui:
  theme_mode: "dark"
  color_scheme: "default"
  font_family: "Inter"
  font_size: 14
  sidebar_width: 250
  show_line_numbers: true
  word_wrap: true

recent:
  projects:
    - "proj_abc123"
    - "proj_def456"
  notes:
    - "note_xyz789"
  searches:
    - "react hooks"
    - "api design"
```

---

## Synchronization

### Sync Strategy

#### Local-First Approach
1. All operations work locally first
2. Sync happens in background (if enabled)
3. Conflicts resolved automatically or flagged for manual resolution
4. No data loss - all versions preserved

#### Sync Targets
- **NAS**: Network-attached storage (SMB/NFS)
- **Cloud**: Dropbox, Google Drive, OneDrive, S3
- **Git**: Version control for text-based data
- **Custom**: WebDAV or custom sync endpoint

### Sync Configuration

```yaml
sync:
  enabled: true
  target: "cloud"  # nas|cloud|git|custom
  frequency: "auto"  # auto|manual|scheduled
  schedule: "*/15 * * * *"  # Every 15 minutes (cron)
  
  cloud:
    provider: "dropbox"  # dropbox|gdrive|onedrive|s3
    path: "/ProjectStarterPro2"
    credentials_env: "CLOUD_SYNC_TOKEN"
  
  nas:
    protocol: "smb"  # smb|nfs
    host: "192.168.1.100"
    share: "projects"
    path: "/psp2"
    credentials_env: "NAS_CREDENTIALS"
  
  git:
    remote: "origin"
    branch: "main"
    auto_commit: true
    commit_message_template: "Auto-sync: {timestamp}"
  
  conflict_resolution:
    strategy: "timestamp"  # timestamp|manual|keep_both
    notify_on_conflict: true
```

### Conflict Resolution

#### Timestamp Strategy (Default)
- Most recent modification wins
- Older version saved as `{filename}.conflict.{timestamp}`
- User notified of conflict

#### Manual Strategy
- Both versions preserved
- User prompted to resolve
- Merge tool provided for text files

#### Keep Both Strategy
- Both versions kept with suffixes
- User decides which to keep later

### Sync Process

1. **Detect Changes**: Monitor file system for modifications
2. **Queue Changes**: Add to sync queue with metadata
3. **Upload**: Push changes to remote target
4. **Download**: Pull remote changes
5. **Merge**: Resolve conflicts if any
6. **Verify**: Confirm sync success
7. **Notify**: Alert user of sync status

---

## Backup & Recovery

### Auto-Backup

#### Backup Schedule
- **Frequency**: Daily (configurable)
- **Retention**: 30 days (configurable)
- **Trigger Events**:
  - Daily scheduled backup
  - Before major operations (archive, delete)
  - On-demand user request
  - Before system updates

#### Backup Structure

```
/data/backups/
├── 2025-10-30_120000/
│   ├── metadata.json          # Backup metadata
│   ├── projects/              # Full project data
│   ├── config/                # Configuration files
│   └── manifest.json          # File listing with checksums
├── 2025-10-29_120000/
└── 2025-10-28_120000/
```

#### Backup Metadata

```json
{
  "backup_id": "backup_20251030_120000",
  "created_at": "2025-10-30T12:00:00Z",
  "type": "scheduled",
  "size_bytes": 125829120,
  "file_count": 1247,
  "projects_included": ["proj_abc123", "proj_def456"],
  "compression": "gzip",
  "encryption": true,
  "checksum": "sha256:abc123...",
  "version": "1.0.0"
}
```

### Recovery

#### Point-in-Time Recovery
```bash
# Restore entire system to specific backup
psp backup restore --backup-id backup_20251030_120000

# Restore specific project
psp backup restore --backup-id backup_20251030_120000 --project proj_abc123

# Restore specific files
psp backup restore --backup-id backup_20251030_120000 --files "projects/proj_abc123/notes/*"
```

#### Recovery Process
1. Select backup to restore from
2. Choose scope (full/project/files)
3. Verify backup integrity (checksum)
4. Create safety backup of current state
5. Restore selected data
6. Validate restored data
7. Notify user of completion

---

## Cache Management

### Cache Strategy

#### What Gets Cached
- **Research Content**: Downloaded web pages, PDFs
- **Analytics**: Computed metrics and reports
- **Search Indexes**: Full-text search indexes
- **AI Results**: Summaries, tags, insights
- **Thumbnails**: Image previews

#### Cache Location
```
/data/cache/
├── research/
│   └── {url-hash}/
│       ├── content.html
│       └── metadata.json
├── analytics/
│   └── {project-id}/
│       └── {metric-name}.json
├── search/
│   └── {project-id}/
│       └── index.json
└── ai/
    └── {content-hash}/
        └── result.json
```

#### Cache Invalidation
- **TTL-Based**: Expire after configured time (default: 1 hour)
- **Event-Based**: Invalidate on data changes
- **Size-Based**: LRU eviction when cache exceeds limit
- **Manual**: User can clear cache

#### Cache Configuration

```yaml
cache:
  enabled: true
  max_size_mb: 1024
  ttl_seconds: 3600
  eviction_policy: "lru"  # lru|fifo|lfu
  
  research:
    enabled: true
    max_size_mb: 512
    ttl_seconds: 86400  # 24 hours
  
  analytics:
    enabled: true
    max_size_mb: 256
    ttl_seconds: 3600  # 1 hour
  
  search:
    enabled: true
    max_size_mb: 128
    rebuild_on_startup: false
  
  ai:
    enabled: true
    max_size_mb: 128
    ttl_seconds: 604800  # 7 days
```

---

## Data Validation

### Validation Rules

#### On Write
- Schema validation (JSON Schema)
- Type checking
- Required field validation
- Format validation (dates, UUIDs, etc.)
- Range validation (min/max values)
- Referential integrity

#### On Read
- Checksum verification
- Schema version compatibility
- Data migration if needed
- Corruption detection

### Validation Example

```python
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import List, Optional

class Project(BaseModel):
    id: str = Field(..., regex=r'^proj_[a-z0-9]+$')
    name: str = Field(..., min_length=1, max_length=200)
    description: str = ""
    type: str = Field(..., regex=r'^(software|business|research|personal)$')
    status: str = Field(..., regex=r'^(PLANNING|ACTIVE|PAUSED|COMPLETED|ARCHIVED)$')
    created_at: datetime
    updated_at: datetime
    owner: str
    tags: List[str] = []
    
    @validator('updated_at')
    def updated_after_created(cls, v, values):
        if 'created_at' in values and v < values['created_at']:
            raise ValueError('updated_at must be >= created_at')
        return v
```

---

## Data Migration

### Version Migration

When schema versions change:
1. Detect version mismatch
2. Run migration script
3. Validate migrated data
4. Update schema version
5. Create backup before migration

### Migration Scripts

```python
# migrations/001_add_milestones.py
def migrate(project_data: dict) -> dict:
    """Add milestones field to project schema."""
    if 'milestones' not in project_data:
        project_data['milestones'] = []
    return project_data
```

---

## Performance Considerations

### Optimization Strategies
- **Lazy Loading**: Load data on-demand
- **Pagination**: Limit large result sets
- **Indexing**: Maintain indexes for fast lookups
- **Compression**: Compress archived data
- **Batch Operations**: Group multiple writes

### File Size Limits
- **Project JSON**: 10 MB max
- **Note Markdown**: 5 MB max
- **Research Item**: 50 MB max
- **Analytics Report**: 10 MB max

---

## References

- System Architecture: `../architecture/system-architecture.md`
- Core Modules: `../modules/spec.md`
- API Contracts: `../api/spec.md`

