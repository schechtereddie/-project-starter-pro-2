# Documentation Agent - Framework Scraper

Intelligent documentation scraping, indexing, and search system for AI frameworks.

## Features

- **Automatic Discovery**: Reads framework list and extracts documentation URLs
- **Smart Scraping**: Uses ScrapeGraphAI and Firecrawl for comprehensive documentation fetching
- **Clean Normalization**: Converts all docs to consistent Markdown format
- **Vector Search**: Semantic search across all framework documentation
- **Auto-Updates**: Periodic refresh to keep documentation current

## Installation

```bash
# Install dependencies
pip install scrapegraphai firecrawl-py sentence-transformers chromadb html2text beautifulsoup4 httpx

# Set up API keys
export FIRECRAWL_API_KEY="your-key"
export OPENAI_API_KEY="your-key"
```

## Usage

### Basic Usage

```python
from src.agents.documentation_agent import DocumentationAgent

# Initialize agent
agent = DocumentationAgent()

# Discover frameworks
frameworks = agent.discover_frameworks()
print(f"Found {len(frameworks)} frameworks")

# Scrape a specific framework
agent.scrape_framework("CrewAI")

# Search documentation
results = agent.search("how to create an agent", framework="crewai")
for result in results:
    print(f"{result['title']}: {result['snippet']}")
```

### Advanced Usage

```python
# Scrape all frameworks
agent.scrape_all(priority_only=True)

# Update specific framework
agent.update_framework("LangGraph")

# Search across all frameworks
results = agent.search("state management", top_k=10)

# Get framework metadata
metadata = agent.get_framework_metadata("CrewAI")
```

## Components

### 1. FrameworkDiscovery
Parses `docs/frameworks/AI_FRAMEWORKS_OVERVIEW.md` and extracts framework information.

```python
from src.agents.documentation_agent import FrameworkDiscovery

discovery = FrameworkDiscovery()
frameworks = discovery.discover()
```

### 2. DocumentationScraper
Fetches documentation using ScrapeGraphAI and Firecrawl.

```python
from src.agents.documentation_agent import DocumentationScraper

scraper = DocumentationScraper(config)
result = await scraper.scrape_framework(framework)
```

### 3. DocumentationNormalizer
Converts HTML to clean Markdown.

```python
from src.agents.documentation_agent import DocumentationNormalizer

normalizer = DocumentationNormalizer()
markdown = normalizer.normalize(page)
```

### 4. DocumentationIndexer
Stores documentation and creates vector embeddings.

```python
from src.agents.documentation_agent import DocumentationIndexer

indexer = DocumentationIndexer(config)
metadata = indexer.index_framework("CrewAI", pages)
```

### 5. DocumentationSearch
Enables semantic search across documentation.

```python
from src.agents.documentation_agent import DocumentationSearch

search = DocumentationSearch(indexer)
results = search.search("agent configuration", top_k=5)
```

## Configuration

Create `config/docs_agent.yaml`:

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
  openai_api_key: "${OPENAI_API_KEY}"
  llm_model: "gpt-3.5-turbo"
```

## API Endpoints

```bash
# Search documentation
curl "http://localhost:8000/api/v1/docs/search?q=create+agent&framework=crewai"

# Get framework docs
curl "http://localhost:8000/api/v1/docs/frameworks/crewai"

# Trigger update
curl -X POST "http://localhost:8000/api/v1/docs/frameworks/crewai/update"

# Check update status
curl "http://localhost:8000/api/v1/docs/tasks/{task_id}"
```

## Scheduled Updates

Documentation is automatically updated weekly (configurable):

```python
# Celery beat schedule
celery_app.conf.beat_schedule = {
    'update-docs-weekly': {
        'task': 'docs_agent.update_all_frameworks',
        'schedule': crontab(day_of_week='sunday', hour=2, minute=0),
    },
}
```

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
│   └── ...
└── langchain/
    └── ...
```

## Testing

```bash
# Run tests
pytest tests/agents/test_documentation_agent.py -v

# Test discovery
pytest tests/agents/test_discovery.py -v

# Test scraping
pytest tests/agents/test_scraper.py -v

# Test search
pytest tests/agents/test_search.py -v
```

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Format code
black src/agents/documentation_agent/
ruff src/agents/documentation_agent/

# Type check
mypy src/agents/documentation_agent/
```

## Troubleshooting

### API Key Issues
```bash
# Verify API keys are set
echo $FIRECRAWL_API_KEY
echo $OPENAI_API_KEY
```

### Scraping Failures
- Check rate limits
- Verify URL accessibility
- Review Firecrawl quota

### Search Not Working
- Ensure ChromaDB is initialized
- Check embedding model is downloaded
- Verify documents are indexed

## References

- Specification: `openspec/specs/agents/documentation-agent-framework-scraper.md`
- Proposal: `openspec/changes/documentation-agent-framework-scraper/proposal.md`
- Framework Overview: `docs/frameworks/AI_FRAMEWORKS_OVERVIEW.md`

## License

Part of Project Starter Pro 2

