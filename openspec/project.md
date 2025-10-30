# Project Starter Pro 2 — Project Overview

**Goal**
Deliver a unified workspace for planning, tracking, researching, and building both software and business projects with fully integrated AI automation.

**Vision**
To create an intelligent ecosystem that manages ideas, research, documentation, analytics, and business planning through a coordinated network of AI agents.

---

## Core Objectives
1. Centralize all project data — notes, research, specs, analytics, and business plans — in one structure.
2. Automate documentation, research, and setup using AI agents.
3. Provide business and financial insights alongside technical tools.
4. Offer local-first operation with optional cloud sync.
5. Seamlessly integrate external LLM APIs and data crawlers for live intelligence.

---

## Primary Features
- OpenSpec-driven project lifecycle management.
- Dual-core architecture: Node.js CLI frontend + Python logic engine.
- Integrated suite of specialized AI agents for research, analytics, business planning, and documentation.
- Automatic gathering and organization of framework documentation.
- Financial and market analysis for business ideation.
- Integration of ScrapeGraph and Firecrawl for structured data capture.
- Local + API-based AI inference using OpenAI, Claude, and DeepSeek.
- Preloaded API and tool documentation for immediate use.

---

## AI Agents Overview

### 1. **Research Intelligence Crew**
A coordinated team of AI agents specialized by domain:
- **General Research Agent** – Performs topic-based exploration, fact-checking, and summarization.
- **Technical Research Agent** – Focuses on programming frameworks, libraries, and APIs used in each project.
- **Business Research Agent** – Collects financial, market, and economic data for new ideas.
- **Data Collector Agent** – Utilizes ScrapeGraph and Firecrawl to extract structured knowledge from the web.
All findings are stored in `/data/research/` and indexed for retrieval.

### 2. **Documentation Agent**
**Purpose**: Aggregate and organize all framework, library, and API documentation used in the project.
**Functions**:
- Automatically scrape and format official docs for Python, Node.js, and integrated libraries.
- Maintain local doc mirrors for offline access.
- Store data under `/docs/frameworks/` and `/docs/api/`.
- Support linking documentation snippets to relevant specs or code modules.

### 3. **Analytics Agent**
**Purpose**: Track usage, productivity, and technical performance.
**Functions**:
- Measure task completion, coding velocity, and AI utilization metrics.
- Monitor errors, performance logs, and recommendations.
- Generate periodic analytics summaries to `/data/analytics.json`.

### 4. **Project Insights Agent**
**Purpose**: Combine research, analytics, and development data to generate actionable insights.
**Functions**:
- Detect project bottlenecks, risks, and opportunities.
- Recommend design or business adjustments.
- Write reports into `/data/insights/`.

### 5. **Business Planning Agent**
**Purpose**: Generate structured business plans, models, and projections.
**Functions**:
- Use research data and financial models to create business plans.
- Build forecasts and revenue models based on parameters.
- Output documents under `/data/business/` as markdown or PDF.

---

## API Integrations

### Preloaded API Keys (for system-level use)
| Provider | Purpose | Usage |
|-----------|----------|-------|
| **OpenAI API** | General-purpose reasoning, coding, text generation | Integrated for assistant and business writing |
| **Claude API** | Large-context reasoning and structured generation | For long-form and analytical work |
| **DeepSeek API** | High-speed data analysis and correlation | Used by analytics and research subsystems |

All APIs can be toggled per user or project.
Keys and configs stored securely in `/config/api_keys.yaml`.

---

## Supporting Tools and Frameworks

### ScrapeGraph
Used for structured data extraction from websites, documentation, and reports.
- Integrated for both internal research agents and user-facing scraping tools.
- Graph-based extraction ensures reliable structure and reproducibility.

### Firecrawl
Used for crawling and indexing documentation and public datasets.
- Enables full-site mirroring for offline doc availability.
- Used by the Documentation Agent and Research Intelligence Crew.

---

## Tech Stack
- **Backend**: Python 3.13.5+ (core logic engine)
- **Frontend**: Node.js 20 LTS (CLI and tooling)
- **AI Integration**: Augment CLI for OpenSpec workflow
- **Storage**: Local-first with optional cloud/NAS synchronization
- **APIs**: OpenAI, Claude, DeepSeek
- **Data Tools**: ScrapeGraph, Firecrawl

---

## Directory Structure
```
/data/
├── projects/          # Project data and metadata
├── research/          # AI-gathered research data
├── analytics.json     # Aggregated analytics
├── insights/          # AI-generated project insights
├── business/          # Business plans and projections
├── context/           # Unified context index for agents
/docs/
├── frameworks/        # Framework documentation
└── api/               # API references and schemas
/config/
├── settings.yaml      # System configuration
└── api_keys.yaml      # API credentials and usage settings
/openspec/
├── specs/             # Approved specifications
├── changes/           # Proposed changes (deltas)
└── project.md         # This file
```

---

## OpenSpec Conventions
- Every feature uses the OpenSpec **proposal → apply → archive** cycle.
- Deltas are stored under `openspec/changes/`.
- Approved specs live under `openspec/specs/`.
- All agents follow the OpenSpec lifecycle for coordination.

---

## Agent Coordination Layer
All agents share a unified context index under `/data/context/`
and communicate through the **Augment CLI orchestration layer**.

Agents can:
- Access shared research and documentation
- Coordinate on multi-step workflows
- Generate insights from combined data sources
- Propose and apply changes via OpenSpec

---

## Future Additions
- Plugin API for adding new research domains.
- Optional public dataset sync for business intelligence.
- Team mode with collaborative AI agent sessions.
- Graph-based visualization of data relationships and dependencies.

---

## Success Criteria
- Fully automated research and documentation workflow.
- Actionable analytics and insights produced continuously.
- Business plans and market projections generated with minimal input.
- End-to-end AI collaboration supported locally and via API integrations.
