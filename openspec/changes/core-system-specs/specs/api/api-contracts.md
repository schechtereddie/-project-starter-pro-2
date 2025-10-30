# API Contracts Specification

**Version**: 1.0.0  
**Last Updated**: 2025-10-30  
**Status**: Draft  

## Purpose

Define the internal and external API contracts for Project Starter Pro 2, ensuring consistent interfaces across modules and external integrations.

## API Architecture

### API Types
1. **Internal APIs**: Python module interfaces
2. **CLI APIs**: Command-line interface
3. **REST APIs**: HTTP endpoints (optional, for team mode)
4. **Integration APIs**: External service connectors

### Design Principles
- **Consistency**: Uniform naming and patterns
- **Versioning**: Explicit version in all APIs
- **Error Handling**: Standardized error responses
- **Documentation**: Self-documenting with type hints
- **Validation**: Input validation at API boundaries

---

## 1. Internal Python APIs

### Project Manager API

```python
class ProjectManager:
    """Manages project lifecycle and metadata."""
    
    def create_project(
        self,
        name: str,
        description: str = "",
        project_type: str = "software",
        template_id: str | None = None,
        settings: dict | None = None
    ) -> Project:
        """
        Create a new project.
        
        Args:
            name: Project name (1-200 chars)
            description: Project description
            project_type: Type of project (software|business|research|personal)
            template_id: Optional template to apply
            settings: Optional project settings
            
        Returns:
            Created Project object
            
        Raises:
            ValidationError: Invalid input parameters
            DuplicateError: Project name already exists
            TemplateNotFoundError: Template ID not found
        """
        
    def get_project(self, project_id: str) -> Project:
        """Get project by ID."""
        
    def update_project(
        self,
        project_id: str,
        updates: dict
    ) -> Project:
        """Update project fields."""
        
    def delete_project(
        self,
        project_id: str,
        force: bool = False
    ) -> bool:
        """Delete project (soft delete unless force=True)."""
        
    def list_projects(
        self,
        filters: dict | None = None,
        sort_by: str = "updated_at",
        order: str = "desc",
        limit: int = 100,
        offset: int = 0
    ) -> list[Project]:
        """List projects with filtering and pagination."""
        
    def archive_project(self, project_id: str) -> bool:
        """Archive a completed project."""
```

### Task Orchestrator API

```python
class TaskOrchestrator:
    """Manages tasks and their execution."""
    
    def create_task(
        self,
        project_id: str,
        title: str,
        description: str = "",
        priority: Priority = Priority.MEDIUM,
        task_type: str = "feature",
        assigned_to: str | None = None,
        due_date: datetime | None = None,
        dependencies: list[str] | None = None,
        tags: list[str] | None = None
    ) -> Task:
        """Create a new task."""
        
    def get_task(self, task_id: str) -> Task:
        """Get task by ID."""
        
    def update_task(self, task_id: str, updates: dict) -> Task:
        """Update task fields."""
        
    def complete_task(
        self,
        task_id: str,
        actual_hours: float | None = None,
        notes: str = ""
    ) -> Task:
        """Mark task as completed."""
        
    def list_tasks(
        self,
        project_id: str,
        filters: dict | None = None,
        sort_by: str = "priority",
        order: str = "desc",
        limit: int = 100,
        offset: int = 0
    ) -> list[Task]:
        """List tasks with filtering and pagination."""
        
    def execute_task(
        self,
        task_id: str,
        context: dict | None = None
    ) -> TaskResult:
        """Execute an automated task."""
        
    def get_task_dependencies(self, task_id: str) -> list[Task]:
        """Get all task dependencies."""
        
    def validate_dependencies(self, task_id: str) -> ValidationResult:
        """Check for circular dependencies."""
```

### Research Engine API

```python
class ResearchEngine:
    """Handles research and information gathering."""
    
    def search(
        self,
        query: str,
        sources: list[str] | None = None,
        max_results: int = 10
    ) -> SearchResults:
        """Search for information."""
        
    def create_research(
        self,
        project_id: str,
        topic: str,
        query: str,
        auto_search: bool = True
    ) -> Research:
        """Create a new research item."""
        
    def add_source(
        self,
        research_id: str,
        source_data: dict
    ) -> Source:
        """Add a source to research."""
        
    def synthesize(
        self,
        research_id: str,
        method: str = "auto"
    ) -> Synthesis:
        """Generate synthesis from research sources."""
        
    def get_research(self, research_id: str) -> Research:
        """Get research by ID."""
        
    def list_research(
        self,
        project_id: str,
        filters: dict | None = None
    ) -> list[Research]:
        """List research items."""
```

### Analytics Engine API

```python
class AnalyticsEngine:
    """Provides analytics and insights."""
    
    def collect_metrics(self, project_id: str) -> Metrics:
        """Collect current project metrics."""
        
    def analyze_progress(
        self,
        project_id: str,
        period: tuple[datetime, datetime] | None = None
    ) -> ProgressAnalysis:
        """Analyze project progress."""
        
    def generate_report(
        self,
        project_id: str,
        report_type: str,
        period: tuple[datetime, datetime] | None = None,
        options: dict | None = None
    ) -> Report:
        """Generate analytics report."""
        
    def predict_completion(
        self,
        project_id: str,
        confidence_level: float = 0.8
    ) -> Prediction:
        """Predict project completion date."""
        
    def identify_bottlenecks(
        self,
        project_id: str
    ) -> list[Bottleneck]:
        """Identify project bottlenecks."""
```

---

## 2. CLI API

### Command Structure
```
psp <command> [subcommand] [options] [arguments]
```

### Core Commands

#### Project Commands
```bash
# Create project
psp project create <name> [--type TYPE] [--template TEMPLATE]

# List projects
psp project list [--status STATUS] [--tag TAG] [--limit N]

# Show project details
psp project show <project-id>

# Update project
psp project update <project-id> [--name NAME] [--status STATUS]

# Delete project
psp project delete <project-id> [--force]

# Archive project
psp project archive <project-id>
```

#### Task Commands
```bash
# Create task
psp task create <project-id> <title> [--priority PRIORITY] [--due DATE]

# List tasks
psp task list <project-id> [--status STATUS] [--assigned-to USER]

# Show task details
psp task show <task-id>

# Update task
psp task update <task-id> [--status STATUS] [--priority PRIORITY]

# Complete task
psp task complete <task-id> [--hours HOURS]

# Execute automated task
psp task execute <task-id>
```

#### Research Commands
```bash
# Create research
psp research create <project-id> <topic> [--query QUERY]

# Search
psp research search <query> [--sources SOURCES]

# Add source
psp research add-source <research-id> <url>

# Synthesize findings
psp research synthesize <research-id>

# Show research
psp research show <research-id>
```

#### Analytics Commands
```bash
# Generate report
psp analytics report <project-id> [--type TYPE] [--period PERIOD]

# Show metrics
psp analytics metrics <project-id>

# Predict completion
psp analytics predict <project-id>

# Identify bottlenecks
psp analytics bottlenecks <project-id>
```

### CLI Response Format

**Success Response**:
```json
{
    "status": "success",
    "data": { ... },
    "message": "Operation completed successfully"
}
```

**Error Response**:
```json
{
    "status": "error",
    "error": {
        "code": "ERROR_CODE",
        "message": "Human-readable error message",
        "details": { ... }
    }
}
```

---

## 3. REST API (Optional - Team Mode)

### Base URL
```
http://localhost:8080/api/v1
```

### Authentication
```
Authorization: Bearer <token>
```

### Endpoints

#### Projects
```
GET    /projects                    # List projects
POST   /projects                    # Create project
GET    /projects/{id}               # Get project
PUT    /projects/{id}               # Update project
DELETE /projects/{id}               # Delete project
POST   /projects/{id}/archive       # Archive project
```

#### Tasks
```
GET    /projects/{id}/tasks         # List tasks
POST   /projects/{id}/tasks         # Create task
GET    /tasks/{id}                  # Get task
PUT    /tasks/{id}                  # Update task
DELETE /tasks/{id}                  # Delete task
POST   /tasks/{id}/complete         # Complete task
POST   /tasks/{id}/execute          # Execute task
```

#### Research
```
GET    /projects/{id}/research      # List research
POST   /projects/{id}/research      # Create research
GET    /research/{id}               # Get research
PUT    /research/{id}               # Update research
POST   /research/{id}/sources       # Add source
POST   /research/{id}/synthesize    # Generate synthesis
```

#### Analytics
```
GET    /projects/{id}/metrics       # Get metrics
POST   /projects/{id}/reports       # Generate report
GET    /projects/{id}/predictions   # Get predictions
GET    /projects/{id}/bottlenecks   # Get bottlenecks
```

### HTTP Status Codes
- `200 OK`: Successful GET/PUT
- `201 Created`: Successful POST
- `204 No Content`: Successful DELETE
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource conflict
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

---

## 4. Integration APIs

### GitHub Integration
```python
class GitHubIntegration:
    def sync_issues(self, project_id: str) -> SyncResult
    def create_issue(self, task: Task) -> GitHubIssue
    def update_issue(self, issue_id: str, updates: dict) -> GitHubIssue
    def sync_pull_requests(self, project_id: str) -> SyncResult
```

### Jira Integration
```python
class JiraIntegration:
    def sync_tickets(self, project_id: str) -> SyncResult
    def create_ticket(self, task: Task) -> JiraTicket
    def update_ticket(self, ticket_id: str, updates: dict) -> JiraTicket
```

---

## Error Handling

### Error Types
```python
class PSPError(Exception):
    """Base exception for all PSP errors."""
    code: str
    message: str
    details: dict

class ValidationError(PSPError):
    """Input validation failed."""

class NotFoundError(PSPError):
    """Resource not found."""

class DuplicateError(PSPError):
    """Resource already exists."""

class PermissionError(PSPError):
    """Insufficient permissions."""

class IntegrationError(PSPError):
    """External integration failed."""
```

### Error Response Format
```python
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid project name",
        "details": {
            "field": "name",
            "constraint": "length",
            "expected": "1-200 characters",
            "actual": "0 characters"
        }
    }
}
```

---

## Versioning Strategy

### API Versioning
- Major version in URL/module path: `/api/v1/`, `psp.v1`
- Minor/patch versions backward compatible
- Deprecation warnings for 2 versions before removal

### Version Header (REST API)
```
X-API-Version: 1.0.0
```

---

## Rate Limiting (REST API)

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1635724800
```

---

## References

- REST API Design: https://restfulapi.net/
- Python Type Hints: https://docs.python.org/3/library/typing.html
- CLI Design: https://clig.dev/

