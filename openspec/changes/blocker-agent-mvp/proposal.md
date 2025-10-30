# Proposal: Implement Blocker Agent MVP

**Status**: Draft  
**Created**: 2025-10-30  
**Author**: Project Starter Pro 2 Team  
**Type**: Implementation  

## Overview

Implement a Minimum Viable Product (MVP) of the Blocker Agent - an AI-powered assistant that identifies, analyzes, and helps resolve project blockers in real-time.

## Problem Statement

Projects frequently encounter blockers that:
- Delay critical tasks and milestones
- Block dependent work streams
- Reduce team productivity
- Increase project risk
- Often go unnoticed until too late

Without automated blocker detection, teams must:
- Manually track and identify blockers
- Spend time in status meetings
- React to problems after they've escalated
- Struggle to prioritize resolution efforts

## Proposed Solution

Build an AI agent that:

1. **Detects Blockers** - Automatically identifies tasks and issues blocking progress
2. **Analyzes Impact** - Assesses severity, dependencies, and downstream effects
3. **Suggests Solutions** - Provides actionable recommendations for resolution
4. **Monitors Progress** - Tracks blocker resolution and alerts on escalations
5. **Learns Patterns** - Identifies recurring blocker types and prevention strategies

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────┐
│                  Blocker Agent Core                      │
│                                                          │
│  ┌────────────────┐  ┌────────────────┐  ┌───────────┐ │
│  │    Detector    │  │    Analyzer    │  │  Resolver │ │
│  │                │  │                │  │           │ │
│  │ • Task scan    │  │ • Impact calc  │  │ • Suggest │ │
│  │ • Dependency   │  │ • Severity     │  │ • Track   │ │
│  │ • Pattern      │  │ • Risk score   │  │ • Alert   │ │
│  └────────┬───────┘  └────────┬───────┘  └─────┬─────┘ │
│           │                   │                 │       │
└───────────┼───────────────────┼─────────────────┼───────┘
            │                   │                 │
            ▼                   ▼                 ▼
┌─────────────────────────────────────────────────────────┐
│                    Data Sources                          │
│  • Project tasks                                         │
│  • Task dependencies                                     │
│  • Team assignments                                      │
│  • Historical blocker data                               │
│  • External integrations (GitHub, Jira, etc.)            │
└─────────────────────────────────────────────────────────┘
```

### Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Framework** | CrewAI | Multi-agent orchestration |
| **LLM** | OpenAI GPT-4 / Claude 3 | Analysis and reasoning |
| **Task Queue** | Celery | Async processing |
| **Database** | PostgreSQL | Blocker storage |
| **Cache** | Redis | Fast lookups |
| **Notifications** | WebSocket + Email | Real-time alerts |

## Scope

### In Scope (MVP)

#### Core Features
- [ ] Automatic blocker detection
- [ ] Severity classification (low, medium, high, critical)
- [ ] Impact analysis (tasks blocked, timeline impact)
- [ ] Basic resolution suggestions
- [ ] Real-time notifications
- [ ] Blocker dashboard view

#### Detection Capabilities
- [ ] Overdue tasks blocking others
- [ ] Tasks with missing dependencies
- [ ] Tasks assigned to unavailable team members
- [ ] Tasks waiting on external inputs
- [ ] Resource conflicts
- [ ] Circular dependencies

#### Analysis Features
- [ ] Dependency chain analysis
- [ ] Timeline impact calculation
- [ ] Risk scoring
- [ ] Priority ranking

### Out of Scope (Future Enhancements)
- Advanced ML-based prediction
- Integration with external tools (GitHub, Jira)
- Automated blocker resolution
- Historical trend analysis
- Custom blocker rules engine
- Multi-project blocker correlation

## Blocker Detection Logic

### Detection Rules

#### 1. Overdue Task Blocker
```python
def detect_overdue_blocker(task: Task) -> Optional[Blocker]:
    """Detect tasks that are overdue and blocking others."""
    if task.status != "completed" and task.due_date < datetime.now():
        dependent_tasks = get_dependent_tasks(task.id)
        if len(dependent_tasks) > 0:
            return Blocker(
                type="overdue_task",
                severity=calculate_severity(len(dependent_tasks)),
                task_id=task.id,
                impact={
                    "blocked_tasks": len(dependent_tasks),
                    "days_overdue": (datetime.now() - task.due_date).days
                }
            )
    return None
```

#### 2. Missing Dependency Blocker
```python
def detect_missing_dependency(task: Task) -> Optional[Blocker]:
    """Detect tasks with unresolved dependencies."""
    if task.status == "in_progress":
        dependencies = get_task_dependencies(task.id)
        incomplete = [d for d in dependencies if d.status != "completed"]
        
        if len(incomplete) > 0:
            return Blocker(
                type="missing_dependency",
                severity="medium",
                task_id=task.id,
                impact={
                    "incomplete_dependencies": len(incomplete),
                    "dependency_ids": [d.id for d in incomplete]
                }
            )
    return None
```

#### 3. Resource Conflict Blocker
```python
def detect_resource_conflict(task: Task) -> Optional[Blocker]:
    """Detect tasks assigned to overloaded team members."""
    if task.assigned_to:
        assignee_tasks = get_active_tasks_for_user(task.assigned_to)
        
        if len(assignee_tasks) > TASK_THRESHOLD:
            return Blocker(
                type="resource_conflict",
                severity="low",
                task_id=task.id,
                impact={
                    "assignee_load": len(assignee_tasks),
                    "threshold": TASK_THRESHOLD
                }
            )
    return None
```

#### 4. Circular Dependency Blocker
```python
def detect_circular_dependency(task: Task) -> Optional[Blocker]:
    """Detect circular dependency chains."""
    visited = set()
    
    def has_cycle(current_id: str, path: set) -> bool:
        if current_id in path:
            return True
        if current_id in visited:
            return False
            
        visited.add(current_id)
        path.add(current_id)
        
        dependencies = get_task_dependencies(current_id)
        for dep in dependencies:
            if has_cycle(dep.id, path.copy()):
                return True
        
        return False
    
    if has_cycle(task.id, set()):
        return Blocker(
            type="circular_dependency",
            severity="critical",
            task_id=task.id,
            impact={"cycle_detected": True}
        )
    return None
```

## Impact Analysis

### Severity Calculation

```python
def calculate_blocker_severity(blocker: Blocker) -> str:
    """Calculate blocker severity based on multiple factors."""
    score = 0
    
    # Factor 1: Number of blocked tasks
    blocked_count = blocker.impact.get("blocked_tasks", 0)
    if blocked_count > 10:
        score += 40
    elif blocked_count > 5:
        score += 30
    elif blocked_count > 2:
        score += 20
    else:
        score += 10
    
    # Factor 2: Days overdue
    days_overdue = blocker.impact.get("days_overdue", 0)
    if days_overdue > 7:
        score += 30
    elif days_overdue > 3:
        score += 20
    elif days_overdue > 1:
        score += 10
    
    # Factor 3: Critical path impact
    if blocker.impact.get("on_critical_path", False):
        score += 30
    
    # Classify severity
    if score >= 80:
        return "critical"
    elif score >= 60:
        return "high"
    elif score >= 40:
        return "medium"
    else:
        return "low"
```

### Timeline Impact

```python
def calculate_timeline_impact(blocker: Blocker) -> dict:
    """Calculate impact on project timeline."""
    task = get_task(blocker.task_id)
    dependent_tasks = get_dependent_tasks(blocker.task_id)
    
    # Calculate delay propagation
    total_delay_days = 0
    affected_milestones = []
    
    for dep_task in dependent_tasks:
        # Estimate delay for each dependent task
        delay = estimate_task_delay(task, dep_task)
        total_delay_days += delay
        
        # Check if delay affects milestones
        milestones = get_affected_milestones(dep_task)
        affected_milestones.extend(milestones)
    
    return {
        "total_delay_days": total_delay_days,
        "affected_tasks": len(dependent_tasks),
        "affected_milestones": list(set(affected_milestones)),
        "estimated_completion_delay": calculate_completion_delay(task)
    }
```

## Resolution Suggestions

### AI-Powered Recommendations

```python
async def generate_resolution_suggestions(blocker: Blocker) -> list[Suggestion]:
    """Use AI to generate resolution suggestions."""
    
    # Prepare context
    task = get_task(blocker.task_id)
    dependencies = get_task_dependencies(blocker.task_id)
    team = get_project_team(task.project_id)
    
    context = {
        "blocker_type": blocker.type,
        "task": task.to_dict(),
        "dependencies": [d.to_dict() for d in dependencies],
        "team_availability": [m.to_dict() for m in team]
    }
    
    # Call LLM for suggestions
    prompt = f"""
    Analyze this project blocker and provide 3-5 actionable resolution suggestions.
    
    Blocker Type: {blocker.type}
    Severity: {blocker.severity}
    Task: {task.title}
    Status: {task.status}
    
    Context:
    {json.dumps(context, indent=2)}
    
    Provide suggestions in this format:
    1. [Action] - [Expected outcome] - [Estimated time]
    """
    
    response = await llm.generate(prompt)
    suggestions = parse_suggestions(response)
    
    return suggestions
```

### Suggestion Types

1. **Reassignment**
   - Suggest reassigning to available team member
   - Include workload comparison
   - Estimate impact on timeline

2. **Dependency Resolution**
   - Identify which dependencies to prioritize
   - Suggest parallel work opportunities
   - Recommend dependency removal if possible

3. **Scope Adjustment**
   - Suggest breaking down large tasks
   - Recommend deferring non-critical work
   - Identify MVP scope options

4. **Resource Addition**
   - Suggest adding team members
   - Recommend external help
   - Identify skill gaps

## Data Models

### Blocker Model

```python
from sqlalchemy import Column, String, DateTime, JSON, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Blocker(Base):
    __tablename__ = "blockers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), nullable=False)
    task_id = Column(UUID(as_uuid=True), nullable=False)
    
    type = Column(String(50), nullable=False)  # overdue_task, missing_dependency, etc.
    severity = Column(String(20), nullable=False)  # low, medium, high, critical
    status = Column(String(20), nullable=False, default="active")  # active, resolved, ignored
    
    impact = Column(JSON, nullable=False)  # Impact metrics
    suggestions = Column(JSON)  # Resolution suggestions
    
    detected_at = Column(DateTime, nullable=False)
    resolved_at = Column(DateTime)
    
    metadata = Column(JSON)
```

### BlockerSuggestion Model

```python
class BlockerSuggestion(Base):
    __tablename__ = "blocker_suggestions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    blocker_id = Column(UUID(as_uuid=True), nullable=False)
    
    action = Column(String(500), nullable=False)
    expected_outcome = Column(String(500))
    estimated_time = Column(String(100))
    confidence_score = Column(Float)
    
    status = Column(String(20), default="pending")  # pending, accepted, rejected, completed
    
    created_at = Column(DateTime, nullable=False)
    applied_at = Column(DateTime)
```

## API Endpoints

### Blocker Management

```python
# Get blockers for project
GET /api/v1/projects/{project_id}/blockers
Query params: ?severity=high&status=active
Response: {
    "items": [Blocker],
    "total": int,
    "by_severity": {
        "critical": int,
        "high": int,
        "medium": int,
        "low": int
    }
}

# Get blocker details
GET /api/v1/blockers/{blocker_id}
Response: Blocker

# Update blocker status
PATCH /api/v1/blockers/{blocker_id}
Request: {
    "status": "resolved",
    "resolution_notes": "string"
}
Response: Blocker

# Get resolution suggestions
GET /api/v1/blockers/{blocker_id}/suggestions
Response: [BlockerSuggestion]

# Apply suggestion
POST /api/v1/blockers/{blocker_id}/suggestions/{suggestion_id}/apply
Response: {
    "success": boolean,
    "message": string
}
```

## Celery Tasks

### Blocker Detection Task

```python
@celery_app.task(name="blocker_agent.detect_blockers")
def detect_blockers_task(project_id: str):
    """Scan project for blockers."""
    
    # Get all active tasks
    tasks = get_project_tasks(project_id, status=["in_progress", "blocked"])
    
    blockers_found = []
    
    for task in tasks:
        # Run detection rules
        blocker = (
            detect_overdue_blocker(task) or
            detect_missing_dependency(task) or
            detect_resource_conflict(task) or
            detect_circular_dependency(task)
        )
        
        if blocker:
            # Save blocker
            db_blocker = save_blocker(blocker)
            
            # Generate suggestions
            suggestions = generate_resolution_suggestions(blocker)
            save_suggestions(db_blocker.id, suggestions)
            
            # Send notification
            send_blocker_notification(db_blocker)
            
            blockers_found.append(db_blocker)
    
    return {
        "project_id": project_id,
        "blockers_found": len(blockers_found),
        "by_severity": count_by_severity(blockers_found)
    }
```

## Dashboard Integration

### Blocker Dashboard Component

```typescript
interface BlockerDashboardProps {
  projectId: string;
}

export function BlockerDashboard({ projectId }: BlockerDashboardProps) {
  const { data: blockers } = useBlockers(projectId);
  
  const criticalBlockers = blockers?.filter(b => b.severity === 'critical') || [];
  const highBlockers = blockers?.filter(b => b.severity === 'high') || [];
  
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-4 gap-4">
        <MetricCard
          title="Critical Blockers"
          value={criticalBlockers.length}
          variant="destructive"
        />
        <MetricCard
          title="High Priority"
          value={highBlockers.length}
          variant="warning"
        />
        <MetricCard
          title="Total Active"
          value={blockers?.length || 0}
        />
        <MetricCard
          title="Avg Resolution Time"
          value="2.3 days"
        />
      </div>
      
      <BlockerList blockers={blockers} />
    </div>
  );
}
```

## Success Criteria

- [ ] Blocker detection running automatically
- [ ] All 4 detection rules implemented
- [ ] Severity calculation accurate
- [ ] AI suggestions generated successfully
- [ ] Real-time notifications working
- [ ] Dashboard displaying blockers
- [ ] API endpoints functional
- [ ] Tests passing (>80% coverage)
- [ ] Documentation complete

## Dependencies

- Core backend (FastAPI + Celery + PostgreSQL)
- CrewAI framework
- OpenAI or Claude API access
- Frontend dashboard (for UI)

## Timeline

- **Week 1**: Detection logic, data models, API endpoints
- **Week 2**: AI suggestion generation, Celery tasks
- **Week 3**: Dashboard integration, notifications
- **Week 4**: Testing, refinement, documentation

## Next Steps

1. Create detailed implementation tasks
2. Set up blocker detection rules
3. Implement severity calculation
4. Integrate AI for suggestions
5. Build dashboard components
6. Add real-time notifications
7. Test with real project data
8. Refine and optimize

