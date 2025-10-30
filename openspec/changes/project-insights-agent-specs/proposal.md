# Proposal: Define Project Insights Agent Specs

**Status**: Draft  
**Created**: 2025-10-30  
**Author**: Augment CLI  
**Type**: AI Agent Specification  

## Overview

Define comprehensive specifications for the Project Insights Agent - an AI agent that analyzes project data to detect bottlenecks, predict risks, and provide actionable recommendations for project success.

## Problem Statement

Project managers and teams often struggle to:

- Identify bottlenecks before they impact delivery
- Predict project risks early
- Understand root causes of delays
- Optimize resource allocation
- Make data-driven decisions
- Maintain project health

## Proposed Solution

Create a Project Insights Agent that:

1. **Analyzes project data** from tasks, research, and analytics
2. **Detects bottlenecks** in workflows and processes
3. **Predicts risks** before they materialize
4. **Identifies root causes** of issues
5. **Provides recommendations** for optimization
6. **Monitors project health** continuously

## Scope

### In Scope
- Bottleneck detection algorithms
- Risk prediction models
- Root cause analysis
- Recommendation engine
- Project health scoring
- Continuous monitoring

### Out of Scope
- Automated remediation (future enhancement)
- Team performance evaluation (separate feature)
- Budget forecasting (Business Planning Agent)
- External project integrations (separate feature)

## Agent Specification

### Purpose
Analyze project data to detect bottlenecks, predict risks, and provide actionable recommendations for project optimization and success.

### Capabilities

#### 1. Bottleneck Detection

**Workflow Bottlenecks**:
- Tasks stuck in specific states
- Dependencies blocking progress
- Resource constraints
- Process inefficiencies

**Detection Algorithm**:
```python
class BottleneckDetector:
    """Detects bottlenecks in project workflows."""
    
    def detect_task_bottlenecks(self, tasks: list[Task]) -> list[Bottleneck]:
        """Identify tasks causing workflow delays."""
        bottlenecks = []
        
        # Find tasks with many dependents
        for task in tasks:
            dependent_count = len(task.dependent_tasks)
            if dependent_count > 3 and task.status != "completed":
                bottlenecks.append(Bottleneck(
                    type="critical_path",
                    task_id=task.id,
                    severity="high",
                    impact=f"{dependent_count} tasks blocked",
                    recommendation="Prioritize this task immediately"
                ))
        
        # Find tasks stuck in review
        stuck_tasks = [t for t in tasks if t.status == "in_review" 
                       and (datetime.now() - t.review_started) > timedelta(days=2)]
        
        if stuck_tasks:
            bottlenecks.append(Bottleneck(
                type="review_delay",
                task_ids=[t.id for t in stuck_tasks],
                severity="medium",
                impact=f"{len(stuck_tasks)} tasks awaiting review",
                recommendation="Expedite code reviews or add reviewers"
            ))
        
        return bottlenecks
```

#### 2. Risk Prediction

**Risk Categories**:
- Schedule risks (delays, missed deadlines)
- Quality risks (technical debt, bugs)
- Resource risks (capacity, availability)
- Dependency risks (external blockers)

**Prediction Model**:
```python
class RiskPredictor:
    """Predicts project risks using ML and heuristics."""
    
    def predict_schedule_risk(self, project: Project) -> Risk:
        """Predict likelihood of schedule delays."""
        
        # Calculate risk factors
        velocity_trend = self.get_velocity_trend(project)
        remaining_work = self.estimate_remaining_work(project)
        time_remaining = (project.deadline - datetime.now()).days
        
        # Risk score calculation
        risk_score = 0.0
        
        if velocity_trend < 0:  # Declining velocity
            risk_score += 0.3
        
        estimated_days = remaining_work / project.avg_velocity
        if estimated_days > time_remaining:
            risk_score += 0.5
        
        blocked_tasks_ratio = len(project.blocked_tasks) / len(project.tasks)
        risk_score += blocked_tasks_ratio * 0.2
        
        return Risk(
            type="schedule_delay",
            probability=min(risk_score, 1.0),
            severity="high" if risk_score > 0.7 else "medium",
            impact=f"Project may miss deadline by {estimated_days - time_remaining:.0f} days",
            mitigation=[
                "Reduce scope",
                "Add resources",
                "Extend deadline"
            ]
        )
```

#### 3. Root Cause Analysis

**Analysis Methods**:
- 5 Whys technique
- Fishbone diagram analysis
- Correlation analysis
- Pattern matching

**Implementation**:
```python
class RootCauseAnalyzer:
    """Analyzes root causes of project issues."""
    
    def analyze_velocity_drop(self, project: Project) -> RootCause:
        """Determine why velocity decreased."""
        
        # Gather evidence
        recent_metrics = self.get_recent_metrics(project, days=14)
        
        factors = []
        
        # Check for increased complexity
        if recent_metrics.avg_task_complexity > project.historical_avg_complexity:
            factors.append({
                "factor": "increased_complexity",
                "confidence": 0.8,
                "evidence": "Average task complexity up 30%"
            })
        
        # Check for team changes
        if recent_metrics.team_size < project.avg_team_size:
            factors.append({
                "factor": "reduced_capacity",
                "confidence": 0.9,
                "evidence": "Team size decreased from 5 to 3"
            })
        
        # Check for blockers
        if recent_metrics.blocked_tasks_ratio > 0.2:
            factors.append({
                "factor": "external_blockers",
                "confidence": 0.7,
                "evidence": "20% of tasks blocked by dependencies"
            })
        
        # Determine primary root cause
        primary_cause = max(factors, key=lambda x: x["confidence"])
        
        return RootCause(
            issue="velocity_drop",
            primary_cause=primary_cause["factor"],
            contributing_factors=[f["factor"] for f in factors if f != primary_cause],
            confidence=primary_cause["confidence"],
            evidence=primary_cause["evidence"],
            recommendations=self.get_recommendations(primary_cause["factor"])
        )
```

#### 4. Recommendation Engine

**Recommendation Types**:
- Process improvements
- Resource reallocation
- Scope adjustments
- Risk mitigation actions
- Quality improvements

**Engine**:
```python
class RecommendationEngine:
    """Generates actionable recommendations."""
    
    def generate_recommendations(
        self, 
        bottlenecks: list[Bottleneck],
        risks: list[Risk],
        root_causes: list[RootCause]
    ) -> list[Recommendation]:
        """Generate prioritized recommendations."""
        
        recommendations = []
        
        # Address high-severity bottlenecks
        for bottleneck in bottlenecks:
            if bottleneck.severity == "high":
                recommendations.append(Recommendation(
                    type="immediate_action",
                    priority="high",
                    title=f"Resolve {bottleneck.type}",
                    description=bottleneck.recommendation,
                    expected_impact="Unblock workflow, improve velocity",
                    effort="medium",
                    confidence=0.9
                ))
        
        # Mitigate high-probability risks
        for risk in risks:
            if risk.probability > 0.7:
                for mitigation in risk.mitigation:
                    recommendations.append(Recommendation(
                        type="risk_mitigation",
                        priority="high",
                        title=f"Mitigate {risk.type}",
                        description=mitigation,
                        expected_impact=f"Reduce risk probability to <50%",
                        effort="high",
                        confidence=0.8
                    ))
        
        # Address root causes
        for root_cause in root_causes:
            recommendations.extend(
                self.get_root_cause_recommendations(root_cause)
            )
        
        # Prioritize and return
        return sorted(recommendations, key=lambda r: r.priority, reverse=True)
```

#### 5. Project Health Scoring

**Health Dimensions**:
- Schedule health (on track vs. delayed)
- Quality health (technical debt, bugs)
- Team health (velocity, morale)
- Risk health (risk exposure)

**Scoring**:
```python
class ProjectHealthScorer:
    """Calculates overall project health score."""
    
    def calculate_health_score(self, project: Project) -> HealthScore:
        """Calculate multi-dimensional health score."""
        
        # Schedule health (0-100)
        schedule_health = self.calculate_schedule_health(project)
        
        # Quality health (0-100)
        quality_health = self.calculate_quality_health(project)
        
        # Team health (0-100)
        team_health = self.calculate_team_health(project)
        
        # Risk health (0-100)
        risk_health = 100 - (sum(r.probability for r in project.risks) * 20)
        
        # Overall health (weighted average)
        overall = (
            schedule_health * 0.3 +
            quality_health * 0.25 +
            team_health * 0.25 +
            risk_health * 0.2
        )
        
        return HealthScore(
            overall=overall,
            schedule=schedule_health,
            quality=quality_health,
            team=team_health,
            risk=risk_health,
            status=self.get_health_status(overall),
            timestamp=datetime.now()
        )
    
    def get_health_status(self, score: float) -> str:
        """Convert score to status."""
        if score >= 80:
            return "healthy"
        elif score >= 60:
            return "at_risk"
        else:
            return "critical"
```

### Output Formats

#### Insight Report
```json
{
  "report_id": "string",
  "project_id": "string",
  "generated_at": "datetime",
  "health_score": {
    "overall": 75.5,
    "schedule": 80,
    "quality": 70,
    "team": 75,
    "risk": 78,
    "status": "healthy"
  },
  "bottlenecks": [
    {
      "type": "critical_path",
      "severity": "high",
      "description": "Task #123 blocking 5 dependent tasks",
      "recommendation": "Prioritize immediately"
    }
  ],
  "risks": [
    {
      "type": "schedule_delay",
      "probability": 0.65,
      "severity": "medium",
      "impact": "May miss deadline by 3 days",
      "mitigation": ["Reduce scope", "Add resources"]
    }
  ],
  "recommendations": [
    {
      "priority": "high",
      "title": "Resolve critical path bottleneck",
      "description": "Focus team on Task #123",
      "expected_impact": "Unblock 5 tasks, improve velocity 20%",
      "effort": "medium"
    }
  ]
}
```

## Storage Strategy

```
/data/insights/
├── reports/
│   ├── daily/
│   ├── weekly/
│   └── on-demand/
├── bottlenecks/
├── risks/
└── recommendations/
```

## Workflows

### 1. Daily Insights Generation
```
1. Collect project data (tasks, metrics, analytics)
2. Run bottleneck detection
3. Run risk prediction
4. Calculate health score
5. Generate recommendations
6. Create insight report
7. Notify stakeholders
```

### 2. Continuous Monitoring
```
1. Monitor key project indicators
2. Check for threshold violations
3. Detect critical issues
4. Generate alerts
5. Update health score
```

## API Integration

### Claude API
**Purpose**: Deep analysis and recommendation generation

**Usage**:
```python
from anthropic import Anthropic

client = Anthropic(api_key=config.claude_api_key)

# Analyze complex project situation
response = client.messages.create(
    model="claude-3-opus-20240229",
    messages=[{
        "role": "user",
        "content": f"""Analyze this project situation and provide recommendations:
        
        Project Data:
        {json.dumps(project_data, indent=2)}
        
        Bottlenecks:
        {json.dumps(bottlenecks, indent=2)}
        
        Provide: 1) Root cause analysis, 2) Top 3 recommendations, 3) Expected impact
        """
    }]
)

insights = parse_claude_response(response.content)
```

## Configuration

```yaml
project_insights_agent:
  enabled: true
  
  monitoring:
    continuous: true
    check_interval: 3600  # 1 hour
    
  detection:
    bottleneck_threshold: 2  # days stuck
    risk_threshold: 0.5      # probability
    
  reporting:
    daily_insights: true
    weekly_summary: true
    alert_on_critical: true
    
  health_scoring:
    weights:
      schedule: 0.3
      quality: 0.25
      team: 0.25
      risk: 0.2
```

## Success Criteria

- [ ] Agent architecture defined
- [ ] Bottleneck detection algorithms specified
- [ ] Risk prediction models documented
- [ ] Root cause analysis methods defined
- [ ] Recommendation engine designed
- [ ] Health scoring system established
- [ ] Ready for implementation

## Dependencies

- Core system specifications
- Analytics Agent (for metrics)
- Claude API integration

## Timeline

- Specification: 1-2 hours
- Implementation: Separate proposal

## Next Steps

1. Create detailed specifications
2. Define algorithms and models
3. Document workflows
4. Review and validate
5. Apply with `/openspec-apply`

