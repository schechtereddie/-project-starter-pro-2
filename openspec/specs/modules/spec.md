# Core Modules Specification

**Version**: 1.0.0  
**Last Updated**: 2025-10-30  
**Status**: Draft  

## Purpose

Describe all major functional modules and their responsibilities within Project Starter Pro 2. Each module represents a distinct area of functionality with clear boundaries, interfaces, and data ownership.

---

## Module Overview

Project Starter Pro 2 is organized into five core functional modules that work together to provide a comprehensive project planning, tracking, and analysis platform:

1. **Project Manager** - Project lifecycle and organization
2. **Notes Manager** - Knowledge capture and documentation
3. **Research Hub** - Information gathering and synthesis
4. **Analytics Engine** - Metrics, insights, and reporting
5. **Settings Manager** - Configuration and preferences

---

## 1. Project Manager

### Purpose
Manage the complete lifecycle of projects from creation through completion and archival, including organization of folders, notes, files, and project metadata.

### Responsibilities
- **Project CRUD Operations**: Create, read, update, delete projects
- **Project Organization**: Hierarchical folder structure, file management
- **Metadata Management**: Tags, categories, status tracking, milestones
- **Project Templates**: Apply and manage reusable project structures
- **Project Archival**: Archive completed projects while preserving data
- **Project Search**: Find projects by name, tags, status, or content

### Key Features

#### Project Creation
- Initialize new projects from scratch or templates
- Set project type (software, business, research, personal)
- Configure initial structure and settings
- Auto-generate project ID and timestamps

#### Project Organization
- Hierarchical folder structure within projects
- File attachment and management
- Link related projects and dependencies
- Organize by custom taxonomies

#### Project Lifecycle
- Status tracking: Planning → Active → Paused → Completed → Archived
- Milestone definition and tracking
- Progress monitoring and reporting
- Automatic timestamp updates

### Data Structures

```python
class Project:
    id: str                    # Unique identifier (UUID)
    name: str                  # Project name (1-200 chars)
    description: str           # Detailed description
    type: ProjectType          # software|business|research|personal
    status: ProjectStatus      # PLANNING|ACTIVE|PAUSED|COMPLETED|ARCHIVED
    created_at: datetime       # Creation timestamp
    updated_at: datetime       # Last modification timestamp
    owner: str                 # Project owner/creator
    tags: list[str]           # Categorization tags
    folders: list[Folder]     # Folder structure
    files: list[File]         # Attached files
    milestones: list[Milestone]  # Project milestones
    metadata: dict            # Custom metadata
    settings: ProjectSettings # Project-specific settings
```

### API Interface

```python
class ProjectManager:
    def create_project(
        self,
        name: str,
        description: str = "",
        project_type: str = "software",
        template_id: str | None = None
    ) -> Project:
        """Create a new project."""
        
    def get_project(self, project_id: str) -> Project:
        """Retrieve project by ID."""
        
    def update_project(self, project_id: str, updates: dict) -> Project:
        """Update project fields."""
        
    def delete_project(self, project_id: str, force: bool = False) -> bool:
        """Delete project (soft delete unless force=True)."""
        
    def list_projects(
        self,
        filters: dict | None = None,
        sort_by: str = "updated_at",
        limit: int = 100
    ) -> list[Project]:
        """List projects with filtering."""
        
    def archive_project(self, project_id: str) -> bool:
        """Archive completed project."""
        
    def search_projects(self, query: str) -> list[Project]:
        """Full-text search across projects."""
        
    def create_folder(self, project_id: str, path: str) -> Folder:
        """Create folder within project."""
        
    def attach_file(self, project_id: str, file_path: str) -> File:
        """Attach file to project."""
```

### Storage Location
- **Base Path**: `/data/projects/{project_id}/`
- **Metadata**: `/data/projects/{project_id}/project.json`
- **Folders**: `/data/projects/{project_id}/folders/`
- **Files**: `/data/projects/{project_id}/files/`

---

## 2. Notes Manager

### Purpose
Provide a comprehensive note-taking system with Markdown support, tagging, attachments, and AI-assisted features for summaries and intelligent search.

### Responsibilities
- **Note Creation**: Create and edit Markdown notes
- **Note Organization**: Tag-based and folder-based organization
- **Attachments**: Link files, images, and resources to notes
- **AI Features**: Generate summaries, extract key points, semantic search
- **Version History**: Track note changes over time
- **Note Linking**: Create connections between related notes

### Key Features

#### Markdown Support
- Full Markdown syntax support
- Code blocks with syntax highlighting
- Tables, lists, and formatting
- Frontmatter for metadata (YAML)
- Live preview and editing modes

#### AI-Assisted Features
- **Auto-Summaries**: Generate concise summaries of long notes
- **Key Point Extraction**: Identify and highlight important information
- **Semantic Search**: Find notes by meaning, not just keywords
- **Smart Tags**: AI-suggested tags based on content
- **Related Notes**: Automatically suggest related content

#### Organization
- Hierarchical folder structure
- Multi-tag support for flexible categorization
- Favorites and pinned notes
- Custom note templates
- Archive old or completed notes

### Data Structures

```python
class Note:
    id: str                    # Unique identifier
    project_id: str           # Parent project
    title: str                # Note title
    content: str              # Markdown content
    frontmatter: dict         # YAML metadata
    tags: list[str]           # Categorization tags
    folder_path: str          # Folder location
    attachments: list[Attachment]  # Linked files
    links: list[str]          # Links to other notes
    created_at: datetime      # Creation timestamp
    updated_at: datetime      # Last modification
    version: int              # Version number
    is_favorite: bool         # Favorite flag
    is_archived: bool         # Archive flag
    ai_summary: str | None    # AI-generated summary
    ai_tags: list[str]        # AI-suggested tags
```

### API Interface

```python
class NotesManager:
    def create_note(
        self,
        project_id: str,
        title: str,
        content: str = "",
        tags: list[str] | None = None,
        folder_path: str = "/"
    ) -> Note:
        """Create a new note."""
        
    def get_note(self, note_id: str) -> Note:
        """Retrieve note by ID."""
        
    def update_note(self, note_id: str, updates: dict) -> Note:
        """Update note content or metadata."""
        
    def delete_note(self, note_id: str) -> bool:
        """Delete note."""
        
    def list_notes(
        self,
        project_id: str,
        filters: dict | None = None,
        sort_by: str = "updated_at"
    ) -> list[Note]:
        """List notes with filtering."""
        
    def search_notes(
        self,
        query: str,
        project_id: str | None = None,
        semantic: bool = False
    ) -> list[Note]:
        """Search notes (keyword or semantic)."""
        
    def generate_summary(self, note_id: str) -> str:
        """Generate AI summary of note."""
        
    def suggest_tags(self, note_id: str) -> list[str]:
        """Get AI-suggested tags."""
        
    def find_related_notes(self, note_id: str, limit: int = 5) -> list[Note]:
        """Find related notes using AI."""
        
    def attach_file(self, note_id: str, file_path: str) -> Attachment:
        """Attach file to note."""
        
    def link_notes(self, note_id: str, target_note_id: str) -> bool:
        """Create link between notes."""
```

### Storage Location
- **Base Path**: `/data/projects/{project_id}/notes/`
- **Note Files**: `/data/projects/{project_id}/notes/{note_id}.md`
- **Attachments**: `/data/projects/{project_id}/notes/attachments/`
- **Index**: `/data/projects/{project_id}/notes/index.json`

### Frontmatter Format
```yaml
---
title: "Note Title"
tags: [tag1, tag2, tag3]
created: 2025-10-30T10:00:00Z
updated: 2025-10-30T12:00:00Z
favorite: false
archived: false
ai_summary: "Auto-generated summary..."
---

# Note Content

Markdown content goes here...
```

---

## 3. Research Hub

### Purpose
Centralize research activities by importing links, PDFs, snippets, and other sources, with automatic classification, fact extraction, and knowledge synthesis.

### Responsibilities
- **Source Import**: Import web links, PDFs, documents, code snippets
- **Auto-Classification**: Categorize sources by type, topic, relevance
- **Fact Extraction**: Extract key facts, quotes, and data points
- **Source Management**: Organize, tag, and annotate sources
- **Knowledge Synthesis**: Combine multiple sources into coherent insights
- **Citation Management**: Track and format citations

### Key Features

#### Multi-Source Import
- **Web Links**: Fetch and archive web pages
- **PDF Documents**: Extract text and metadata from PDFs
- **Code Snippets**: Import and syntax-highlight code
- **Images**: Store and annotate images
- **Videos**: Link to videos with timestamps
- **Manual Entry**: Add custom research notes

#### Auto-Classification
- Detect source type automatically
- Categorize by topic using AI
- Assign relevance scores
- Extract metadata (author, date, publisher)
- Identify key themes and concepts

#### Fact Extraction
- Extract key facts and statistics
- Identify important quotes
- Highlight actionable insights
- Create structured data from unstructured sources
- Build knowledge graph connections

### Data Structures

```python
class ResearchItem:
    id: str                    # Unique identifier
    project_id: str           # Parent project
    title: str                # Source title
    source_type: SourceType   # WEB|PDF|SNIPPET|IMAGE|VIDEO|MANUAL
    url: str | None           # Source URL
    content: str              # Extracted content
    summary: str              # AI-generated summary
    tags: list[str]           # Classification tags
    topics: list[str]         # Identified topics
    relevance_score: float    # 0.0 - 1.0
    facts: list[Fact]         # Extracted facts
    quotes: list[Quote]       # Important quotes
    metadata: SourceMetadata  # Author, date, etc.
    created_at: datetime      # Import timestamp
    updated_at: datetime      # Last modification
    annotations: list[Annotation]  # User annotations

class Fact:
    id: str
    text: str                 # Fact statement
    confidence: float         # Confidence score
    source_location: str      # Where in source
    verified: bool            # User verification
    
class Quote:
    id: str
    text: str                 # Quote text
    author: str | None        # Quote author
    context: str              # Surrounding context
    page: int | None          # Page number (for PDFs)
```

### API Interface

```python
class ResearchHub:
    def import_source(
        self,
        project_id: str,
        source_url: str | None = None,
        source_type: str | None = None,
        content: str | None = None,
        auto_process: bool = True
    ) -> ResearchItem:
        """Import a research source."""
        
    def get_research_item(self, item_id: str) -> ResearchItem:
        """Retrieve research item by ID."""
        
    def list_research(
        self,
        project_id: str,
        filters: dict | None = None
    ) -> list[ResearchItem]:
        """List research items."""
        
    def classify_source(self, item_id: str) -> dict:
        """Auto-classify source and extract metadata."""
        
    def extract_facts(self, item_id: str) -> list[Fact]:
        """Extract key facts from source."""
        
    def extract_quotes(self, item_id: str) -> list[Quote]:
        """Extract important quotes."""
        
    def synthesize_research(
        self,
        project_id: str,
        topic: str,
        source_ids: list[str] | None = None
    ) -> Synthesis:
        """Synthesize multiple sources into insights."""
        
    def add_annotation(
        self,
        item_id: str,
        text: str,
        location: str
    ) -> Annotation:
        """Add user annotation to source."""
        
    def search_research(
        self,
        query: str,
        project_id: str | None = None
    ) -> list[ResearchItem]:
        """Search across research sources."""
```

### Storage Location
- **Base Path**: `/data/projects/{project_id}/research/`
- **Items**: `/data/projects/{project_id}/research/{item_id}.json`
- **Cached Content**: `/data/cache/research/{item_id}/`
- **Attachments**: `/data/projects/{project_id}/research/files/`

---

## 4. Analytics Engine

### Purpose
Track productivity metrics, project velocity, and trends to provide actionable insights through charts, reports, and AI-powered analysis.

### Responsibilities
- **Metrics Collection**: Gather data on tasks, time, progress
- **Trend Analysis**: Identify patterns and changes over time
- **Velocity Tracking**: Measure project and team velocity
- **Report Generation**: Create visual and textual reports
- **AI Insights**: Generate intelligent recommendations
- **Forecasting**: Predict completion dates and resource needs

### Key Features

#### Productivity Metrics
- Task completion rates
- Time tracking and estimates vs. actuals
- Work-in-progress limits
- Cycle time and lead time
- Throughput measurements
- Blocked task analysis

#### Project Velocity
- Sprint/iteration velocity
- Burndown and burnup charts
- Cumulative flow diagrams
- Velocity trends over time
- Capacity planning

#### AI-Powered Insights
- Bottleneck identification
- Risk detection and alerts
- Optimization recommendations
- Pattern recognition
- Anomaly detection
- Predictive analytics

### Data Structures

```python
class AnalyticsReport:
    id: str
    project_id: str
    report_type: ReportType   # PRODUCTIVITY|VELOCITY|TRENDS|CUSTOM
    period_start: datetime
    period_end: datetime
    generated_at: datetime
    metrics: MetricsSnapshot
    trends: list[Trend]
    insights: list[Insight]
    charts: list[Chart]
    predictions: Predictions

class MetricsSnapshot:
    task_completion_rate: float
    average_cycle_time: float
    average_lead_time: float
    throughput: int
    work_in_progress: int
    blocked_tasks: int
    velocity: float
    custom_metrics: dict

class Insight:
    type: InsightType         # OBSERVATION|WARNING|RECOMMENDATION
    priority: Priority        # LOW|MEDIUM|HIGH|CRITICAL
    title: str
    description: str
    data: dict
    action_items: list[str]
```

### API Interface

```python
class AnalyticsEngine:
    def collect_metrics(self, project_id: str) -> MetricsSnapshot:
        """Collect current metrics snapshot."""
        
    def generate_report(
        self,
        project_id: str,
        report_type: str,
        period: tuple[datetime, datetime] | None = None
    ) -> AnalyticsReport:
        """Generate analytics report."""
        
    def get_trends(
        self,
        project_id: str,
        metric: str,
        period: tuple[datetime, datetime]
    ) -> list[Trend]:
        """Analyze trends for specific metric."""
        
    def get_insights(self, project_id: str) -> list[Insight]:
        """Get AI-generated insights."""
        
    def predict_completion(self, project_id: str) -> Prediction:
        """Predict project completion date."""
        
    def identify_bottlenecks(self, project_id: str) -> list[Bottleneck]:
        """Identify current bottlenecks."""
        
    def track_velocity(
        self,
        project_id: str,
        window_days: int = 30
    ) -> VelocityData:
        """Track project velocity."""
```

### Storage Location
- **Reports**: `/data/projects/{project_id}/analytics/reports/`
- **Metrics Cache**: `/data/cache/analytics/{project_id}/`
- **Historical Data**: `/data/projects/{project_id}/analytics/history.json`

---

## 5. Settings Manager

### Purpose
Centralize storage and management of user preferences, theme customization, integration configurations, and system settings.

### Responsibilities
- **User Preferences**: Store and retrieve user settings
- **Theme Management**: Customize UI appearance
- **Integration Config**: Manage external service connections
- **System Settings**: Configure system-wide options
- **Settings Validation**: Ensure valid configuration
- **Settings Migration**: Handle version upgrades

### Key Features

#### User Preferences
- Default project type and template
- Notification preferences
- Language and locale
- Date/time formats
- Keyboard shortcuts
- Auto-save settings

#### Theme Customization
- Color schemes (light/dark/custom)
- Font family and size
- Layout preferences
- Icon sets
- Custom CSS

#### Integration Management
- API key storage (encrypted)
- OAuth token management
- Sync settings
- Webhook configurations
- Service enable/disable

### Data Structures

```python
class Settings:
    user_preferences: UserPreferences
    theme: ThemeSettings
    integrations: dict[str, IntegrationConfig]
    system: SystemSettings
    version: str

class UserPreferences:
    default_project_type: str
    notifications_enabled: bool
    language: str
    timezone: str
    date_format: str
    auto_save: bool
    keyboard_shortcuts: dict

class ThemeSettings:
    mode: str                 # light|dark|auto
    color_scheme: str
    font_family: str
    font_size: int
    custom_css: str | None

class IntegrationConfig:
    service: str
    enabled: bool
    credentials: dict         # Encrypted
    settings: dict
```

### API Interface

```python
class SettingsManager:
    def get_settings(self) -> Settings:
        """Get all settings."""
        
    def update_settings(self, updates: dict) -> Settings:
        """Update settings."""
        
    def get_preference(self, key: str, default: any = None) -> any:
        """Get specific preference."""
        
    def set_preference(self, key: str, value: any) -> bool:
        """Set specific preference."""
        
    def get_theme(self) -> ThemeSettings:
        """Get theme settings."""
        
    def update_theme(self, theme_updates: dict) -> ThemeSettings:
        """Update theme settings."""
        
    def get_integration(self, service: str) -> IntegrationConfig:
        """Get integration configuration."""
        
    def update_integration(
        self,
        service: str,
        config: dict
    ) -> IntegrationConfig:
        """Update integration configuration."""
        
    def validate_settings(self, settings: dict) -> ValidationResult:
        """Validate settings structure."""
        
    def reset_to_defaults(self) -> Settings:
        """Reset all settings to defaults."""
```

### Storage Location
- **Settings File**: `/config/settings.yaml`
- **User Preferences**: `/config/user-preferences.yaml`
- **Integrations**: `/config/integrations/` (encrypted)
- **Theme**: `/config/theme.yaml`

---

## Module Dependencies

```
Settings Manager (foundation)
    ↓
Project Manager ←→ Notes Manager
    ↓                    ↓
Research Hub ←→ Analytics Engine
```

All modules depend on Settings Manager for configuration.
Project Manager coordinates with other modules for project-scoped operations.

---

## Testing Requirements

Each module must have:
- Unit tests with >80% coverage
- Integration tests with dependent modules
- API contract tests
- Performance benchmarks
- Error handling tests

---

## References

- System Architecture: `../architecture/system-architecture.md`
- Data Models: `../data/spec.md`
- API Contracts: `../api/spec.md`

