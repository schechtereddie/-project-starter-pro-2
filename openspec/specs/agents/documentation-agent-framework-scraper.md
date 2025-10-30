# Documentation Agent Framework-Scraper Specification

**Version**: 1.0  
**Status**: Approved  
**Applied**: 2025-10-30  

## Overview

The Documentation Agent Framework-Scraper is an intelligent system that automatically discovers, scrapes, normalizes, indexes, and maintains local mirrors of AI framework documentation.

## Core Functions

| Function | Description |
|----------|-------------|
| **Discovery** | Read frameworks list from `docs/frameworks/AI_FRAMEWORKS_OVERVIEW.md` and extract URLs automatically |
| **Scraping** | Use ScrapeGraphAI for structured page parsing and Firecrawl for recursive crawling (limited depth, configurable) |
| **Normalization** | Convert docs to clean Markdown (.md) with minimal HTML |
| **Indexing** | Store parsed content in `/docs/frameworks/<framework-name>/` and register metadata in PostgreSQL or Chroma vector store |
| **Embedding** | Generate vector embeddings using sentence-transformers so any agent can query documentation contextually |
| **Update Loop** | Periodic re-scan (e.g., weekly) to fetch updated docs and refresh vectors |

## Architecture

### Components

1. **FrameworkDiscovery** - Parses overview file and extracts framework URLs
2. **DocumentationScraper** - Fetches documentation using ScrapeGraphAI and Firecrawl
3. **DocumentationNormalizer** - Converts HTML to clean Markdown
4. **DocumentationIndexer** - Stores files and creates vector embeddings
5. **DocumentationSearch** - Enables contextual search across frameworks
6. **UpdateScheduler** - Manages periodic documentation updates

### Technology Stack

- **Framework**: CrewAI
- **Scraping**: ScrapeGraphAI, Firecrawl, BeautifulSoup4
- **Markdown**: html2text
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)
- **Vector Store**: ChromaDB
- **Database**: PostgreSQL
- **Task Queue**: Celery

## Storage Structure

```
docs/frameworks/
├── crewai/
│   ├── index.md
│   ├── getting-started.md
│   ├── core-concepts/
│   │   ├── agents.md
│   │   ├── tasks.md
│   │   └── crews.md
│   └── metadata.json
├── langgraph/
│   ├── index.md
│   ├── tutorials/
│   └── metadata.json
└── langchain/
    ├── index.md
    ├── modules/
    └── metadata.json
```

## API Endpoints

```
GET  /api/v1/docs/search?q={query}&framework={name}&limit={n}
GET  /api/v1/docs/frameworks/{framework_name}
POST /api/v1/docs/frameworks/{framework_name}/update
GET  /api/v1/docs/tasks/{task_id}
```

## Configuration

```yaml
docs_agent:
  overview_file: "docs/frameworks/AI_FRAMEWORKS_OVERVIEW.md"
  firecrawl_api_key: "${FIRECRAWL_API_KEY}"
  max_depth: 3
  max_pages: 100
  rate_limit: 10
  docs_path: "docs/frameworks"
  chroma_path: ".augment/chroma"
  embedding_model: "all-MiniLM-L6-v2"
  chunk_size: 512
  update_schedule: "weekly"
  update_day: "sunday"
  update_hour: 2
  openai_api_key: "${OPENAI_API_KEY}"
  llm_model: "gpt-3.5-turbo"
```

## Agent Registration

```python
from src.agents.documentation_agent import DocumentationAgent

# Register with orchestrator
orchestrator.register_agent("docs", DocumentationAgent())
```

## Implementation Status

- [x] Specification defined
- [ ] Discovery module implemented
- [ ] Scraper implemented
- [ ] Normalizer implemented
- [ ] Indexer implemented
- [ ] Search API implemented
- [ ] Update scheduler implemented
- [ ] Tests written
- [ ] Documentation complete

## References

- Proposal: `openspec/changes/documentation-agent-framework-scraper/proposal.md`
- Tasks: `openspec/changes/documentation-agent-framework-scraper/tasks.md`
- Source: `docs/frameworks/AI_FRAMEWORKS_OVERVIEW.md`

