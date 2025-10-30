# Proposal: Implement Documentation Agent Framework-Scraper

**Status**: Draft  
**Created**: 2025-10-30  
**Author**: Project Starter Pro 2 Team  
**Type**: Implementation  

## Overview

Implement the Documentation Agent's framework-scraper component - an intelligent system that automatically discovers, scrapes, normalizes, indexes, and maintains local mirrors of AI framework documentation.

## Problem Statement

Developers working with AI frameworks need:
- Quick access to framework documentation
- Offline documentation availability
- Searchable, indexed documentation
- Up-to-date documentation mirrors
- Contextual documentation search across multiple frameworks

Without automated documentation scraping, developers must:
- Manually browse multiple documentation sites
- Rely on internet connectivity
- Search each framework separately
- Miss documentation updates
- Struggle to find relevant information across frameworks

## Proposed Solution

Build an intelligent documentation agent that:

1. **Discovers** - Automatically reads framework lists and extracts documentation URLs
2. **Scrapes** - Uses ScrapeGraphAI and Firecrawl to fetch and parse documentation
3. **Normalizes** - Converts all documentation to clean, consistent Markdown
4. **Indexes** - Stores content locally and creates searchable vector embeddings
5. **Updates** - Periodically refreshes documentation to stay current
6. **Searches** - Enables contextual search across all framework documentation

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────┐
│              Documentation Agent Core                    │
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │Discovery │  │ Scraper  │  │Normalizer│  │ Indexer │ │
│  │          │  │          │  │          │  │         │ │
│  │• Parse   │→ │• Scrape  │→ │• Clean   │→ │• Store  │ │
│  │• Extract │  │• Crawl   │  │• Convert │  │• Embed  │ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │
│                                                          │
└─────────────────────────────────────────────────────────┘
            │                    │                │
            ▼                    ▼                ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────┐
│  Framework List  │  │  Scraping Tools  │  │  Storage │
│                  │  │                  │  │          │
│• AI_FRAMEWORKS_  │  │• ScrapeGraphAI   │  │• /docs/  │
│  OVERVIEW.md     │  │• Firecrawl       │  │• Chroma  │
│• URLs            │  │• BeautifulSoup   │  │• Postgres│
└──────────────────┘  └──────────────────┘  └──────────┘
```

### Technology Stack

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| **Framework** | CrewAI | Latest | Agent orchestration |
| **Scraping** | ScrapeGraphAI | Latest | Structured parsing |
| **Crawling** | Firecrawl | Latest | Recursive crawling |
| **Parsing** | BeautifulSoup4 | 4.12+ | HTML parsing |
| **Markdown** | html2text | 2020+ | HTML to Markdown |
| **Embeddings** | sentence-transformers | 2.2+ | Vector embeddings |
| **Vector Store** | ChromaDB | 0.4+ | Vector database |
| **Database** | PostgreSQL | 15+ | Metadata storage |
| **HTTP Client** | httpx | 0.25+ | Async HTTP requests |
| **Task Queue** | Celery | 5.3+ | Async processing |

## Scope

### In Scope

#### Phase 1: Discovery & Scraping
- [ ] Framework list parser
- [ ] URL extraction and validation
- [ ] ScrapeGraphAI integration
- [ ] Firecrawl integration
- [ ] Rate limiting and retry logic
- [ ] Error handling

#### Phase 2: Normalization & Storage
- [ ] HTML to Markdown conversion
- [ ] Content cleaning and formatting
- [ ] File system storage structure
- [ ] Metadata extraction
- [ ] Version tracking

#### Phase 3: Indexing & Search
- [ ] Vector embedding generation
- [ ] ChromaDB integration
- [ ] PostgreSQL metadata storage
- [ ] Contextual search API
- [ ] Multi-framework search

#### Phase 4: Updates & Maintenance
- [ ] Periodic update scheduler
- [ ] Change detection
- [ ] Incremental updates
- [ ] Version comparison
- [ ] Update notifications

### Out of Scope (Future Enhancements)
- PDF documentation scraping
- Video tutorial indexing
- Code example extraction and testing
- Interactive documentation playground
- Community content aggregation

## Component Details

### 1. Discovery Module

**Purpose**: Parse framework list and extract documentation URLs

**Input**: `docs/frameworks/AI_FRAMEWORKS_OVERVIEW.md`

**Output**: List of framework documentation URLs

**Implementation**:

```python
from typing import List, Dict
import re
from pathlib import Path

class FrameworkDiscovery:
    """Discover framework documentation URLs from overview file."""
    
    def __init__(self, overview_path: str = "docs/frameworks/AI_FRAMEWORKS_OVERVIEW.md"):
        self.overview_path = Path(overview_path)
        self.frameworks = []
    
    def discover(self) -> List[Dict[str, str]]:
        """Parse overview file and extract framework URLs."""
        content = self.overview_path.read_text()
        
        # Extract framework sections
        frameworks = []
        
        # Pattern: Framework name followed by URL
        # Example: **CrewAI** - https://docs.crewai.com/
        pattern = r'\*\*([^*]+)\*\*[^\n]*?(https?://[^\s\)]+)'
        
        matches = re.findall(pattern, content)
        
        for name, url in matches:
            frameworks.append({
                "name": name.strip(),
                "url": url.strip(),
                "type": self._detect_framework_type(name),
                "priority": self._calculate_priority(name)
            })
        
        self.frameworks = frameworks
        return frameworks
    
    def _detect_framework_type(self, name: str) -> str:
        """Detect framework category."""
        name_lower = name.lower()
        
        if any(x in name_lower for x in ['crewai', 'autogen', 'langgraph']):
            return 'core'
        elif any(x in name_lower for x in ['mem0', 'browser', 'agentops']):
            return 'tool'
        else:
            return 'additional'
    
    def _calculate_priority(self, name: str) -> int:
        """Calculate scraping priority (1=highest, 3=lowest)."""
        priority_map = {
            'CrewAI': 1,
            'LangGraph': 1,
            'LangChain': 1,
            'AutoGen': 2,
            'LlamaIndex': 2,
            'Mem0': 2,
            'Browser-Use': 2,
        }
        return priority_map.get(name, 3)
```

### 2. Scraper Module

**Purpose**: Fetch and parse documentation pages

**Tools**:
- **ScrapeGraphAI**: Structured content extraction
- **Firecrawl**: Recursive crawling with depth limits

**Implementation**:

```python
from scrapegraphai.graphs import SmartScraperGraph
from firecrawl import FirecrawlApp
import httpx
from typing import Dict, List, Optional

class DocumentationScraper:
    """Scrape framework documentation using multiple tools."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.firecrawl = FirecrawlApp(api_key=config.get('firecrawl_api_key'))
        self.max_depth = config.get('max_depth', 3)
        self.max_pages = config.get('max_pages', 100)
    
    async def scrape_framework(self, framework: Dict) -> Dict:
        """Scrape entire framework documentation."""
        
        base_url = framework['url']
        
        # Use Firecrawl for recursive crawling
        crawl_result = await self._crawl_with_firecrawl(
            base_url,
            max_depth=self.max_depth,
            max_pages=self.max_pages
        )
        
        # Parse each page with ScrapeGraphAI
        parsed_pages = []
        for page in crawl_result['pages']:
            parsed = await self._parse_with_scrapegraph(page)
            if parsed:
                parsed_pages.append(parsed)
        
        return {
            'framework': framework['name'],
            'base_url': base_url,
            'pages': parsed_pages,
            'total_pages': len(parsed_pages),
            'scraped_at': datetime.now().isoformat()
        }
    
    async def _crawl_with_firecrawl(
        self, 
        url: str, 
        max_depth: int,
        max_pages: int
    ) -> Dict:
        """Crawl documentation site with Firecrawl."""
        
        crawl_params = {
            'url': url,
            'crawlerOptions': {
                'maxDepth': max_depth,
                'limit': max_pages,
                'excludes': [
                    '**/api-reference/**',  # Skip API reference (too large)
                    '**/changelog/**',       # Skip changelog
                    '**/blog/**'            # Skip blog
                ],
                'includes': [
                    '**/docs/**',
                    '**/guide/**',
                    '**/tutorial/**'
                ]
            },
            'pageOptions': {
                'onlyMainContent': True,
                'includeHtml': True
            }
        }
        
        result = self.firecrawl.crawl_url(**crawl_params)
        return result
    
    async def _parse_with_scrapegraph(self, page: Dict) -> Optional[Dict]:
        """Parse page content with ScrapeGraphAI."""
        
        graph_config = {
            "llm": {
                "model": "gpt-3.5-turbo",
                "api_key": self.config.get('openai_api_key')
            },
            "verbose": False
        }
        
        # Define extraction schema
        prompt = """
        Extract the following from this documentation page:
        - Title
        - Main content (clean text)
        - Code examples
        - Section headings
        - Navigation links
        """
        
        scraper = SmartScraperGraph(
            prompt=prompt,
            source=page['html'],
            config=graph_config
        )
        
        result = scraper.run()
        
        if result:
            return {
                'url': page['url'],
                'title': result.get('title', ''),
                'content': result.get('main_content', ''),
                'code_examples': result.get('code_examples', []),
                'headings': result.get('section_headings', []),
                'links': result.get('navigation_links', [])
            }
        
        return None
```

### 3. Normalizer Module

**Purpose**: Convert HTML to clean, consistent Markdown

**Implementation**:

```python
import html2text
from bs4 import BeautifulSoup
import re
from typing import Dict

class DocumentationNormalizer:
    """Normalize documentation to clean Markdown."""
    
    def __init__(self):
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = False
        self.html_converter.ignore_images = False
        self.html_converter.body_width = 0  # No line wrapping
    
    def normalize(self, page: Dict) -> str:
        """Convert page to clean Markdown."""
        
        # Extract main content
        content = page.get('content', '')
        
        # Clean HTML
        soup = BeautifulSoup(content, 'html.parser')
        
        # Remove unwanted elements
        for element in soup.find_all(['script', 'style', 'nav', 'footer', 'header']):
            element.decompose()
        
        # Convert to Markdown
        markdown = self.html_converter.handle(str(soup))
        
        # Clean up Markdown
        markdown = self._clean_markdown(markdown)
        
        # Add metadata header
        header = self._create_header(page)
        
        return f"{header}\n\n{markdown}"
    
    def _clean_markdown(self, markdown: str) -> str:
        """Clean up Markdown formatting."""
        
        # Remove excessive blank lines
        markdown = re.sub(r'\n{3,}', '\n\n', markdown)
        
        # Fix code block formatting
        markdown = re.sub(r'```(\w+)\n\n', r'```\1\n', markdown)
        
        # Remove HTML comments
        markdown = re.sub(r'<!--.*?-->', '', markdown, flags=re.DOTALL)
        
        # Normalize heading spacing
        markdown = re.sub(r'(#{1,6})\s+', r'\1 ', markdown)
        
        return markdown.strip()
    
    def _create_header(self, page: Dict) -> str:
        """Create YAML frontmatter header."""
        
        title = page.get('title', 'Untitled')
        url = page.get('url', '')
        
        header = f"""---
title: {title}
source: {url}
scraped_at: {datetime.now().isoformat()}
---"""
        
        return header
```

### 4. Indexer Module

**Purpose**: Store documentation and create vector embeddings

**Storage Structure**:
```
docs/frameworks/
├── crewai/
│   ├── index.md                    # Overview
│   ├── getting-started.md
│   ├── core-concepts/
│   │   ├── agents.md
│   │   ├── tasks.md
│   │   └── crews.md
│   └── metadata.json               # Framework metadata
├── langgraph/
│   ├── index.md
│   ├── tutorials/
│   └── metadata.json
└── langchain/
    ├── index.md
    ├── modules/
    └── metadata.json
```

**Implementation**:

```python
from sentence_transformers import SentenceTransformer
import chromadb
from pathlib import Path
import json
from typing import List, Dict

class DocumentationIndexer:
    """Index documentation with vector embeddings."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.docs_path = Path(config.get('docs_path', 'docs/frameworks'))
        
        # Initialize embedding model
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize ChromaDB
        self.chroma_client = chromadb.PersistentClient(
            path=config.get('chroma_path', '.augment/chroma')
        )
        self.collection = self.chroma_client.get_or_create_collection(
            name="framework_docs",
            metadata={"description": "AI framework documentation"}
        )
    
    def index_framework(self, framework_name: str, pages: List[Dict]):
        """Index all pages for a framework."""
        
        framework_path = self.docs_path / framework_name.lower().replace(' ', '-')
        framework_path.mkdir(parents=True, exist_ok=True)
        
        # Store metadata
        metadata = {
            'name': framework_name,
            'total_pages': len(pages),
            'indexed_at': datetime.now().isoformat(),
            'pages': []
        }
        
        # Process each page
        for page in pages:
            # Save Markdown file
            file_path = self._save_page(framework_path, page)
            
            # Create embeddings
            self._embed_page(framework_name, page, file_path)
            
            # Add to metadata
            metadata['pages'].append({
                'title': page.get('title', ''),
                'url': page.get('url', ''),
                'file': str(file_path.relative_to(self.docs_path))
            })
        
        # Save metadata
        metadata_path = framework_path / 'metadata.json'
        metadata_path.write_text(json.dumps(metadata, indent=2))
        
        return metadata
    
    def _save_page(self, framework_path: Path, page: Dict) -> Path:
        """Save page as Markdown file."""
        
        # Generate filename from URL
        url = page.get('url', '')
        filename = self._url_to_filename(url)
        
        file_path = framework_path / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write Markdown content
        content = page.get('markdown', '')
        file_path.write_text(content)
        
        return file_path
    
    def _embed_page(self, framework_name: str, page: Dict, file_path: Path):
        """Create and store vector embeddings."""
        
        content = page.get('markdown', '')
        
        # Split into chunks (for long documents)
        chunks = self._chunk_content(content, max_length=512)
        
        # Generate embeddings
        embeddings = self.embedder.encode(chunks)
        
        # Store in ChromaDB
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            self.collection.add(
                ids=[f"{framework_name}_{file_path.stem}_{i}"],
                embeddings=[embedding.tolist()],
                documents=[chunk],
                metadatas=[{
                    'framework': framework_name,
                    'title': page.get('title', ''),
                    'url': page.get('url', ''),
                    'file': str(file_path),
                    'chunk_index': i
                }]
            )
    
    def _chunk_content(self, content: str, max_length: int = 512) -> List[str]:
        """Split content into chunks for embedding."""
        
        # Split by paragraphs
        paragraphs = content.split('\n\n')
        
        chunks = []
        current_chunk = []
        current_length = 0
        
        for para in paragraphs:
            para_length = len(para.split())
            
            if current_length + para_length > max_length and current_chunk:
                chunks.append('\n\n'.join(current_chunk))
                current_chunk = [para]
                current_length = para_length
            else:
                current_chunk.append(para)
                current_length += para_length
        
        if current_chunk:
            chunks.append('\n\n'.join(current_chunk))
        
        return chunks
    
    def _url_to_filename(self, url: str) -> str:
        """Convert URL to filesystem-safe filename."""
        
        # Extract path from URL
        from urllib.parse import urlparse
        parsed = urlparse(url)
        path = parsed.path.strip('/')
        
        # Convert to filename
        if not path or path == '':
            return 'index.md'
        
        # Replace slashes with directory structure
        filename = path.replace('/', '/') + '.md'
        
        return filename
```

### 5. Search Module

**Purpose**: Enable contextual search across all documentation

**Implementation**:

```python
class DocumentationSearch:
    """Search framework documentation contextually."""
    
    def __init__(self, indexer: DocumentationIndexer):
        self.indexer = indexer
        self.collection = indexer.collection
        self.embedder = indexer.embedder
    
    def search(
        self, 
        query: str, 
        framework: Optional[str] = None,
        top_k: int = 5
    ) -> List[Dict]:
        """Search documentation with semantic similarity."""
        
        # Generate query embedding
        query_embedding = self.embedder.encode([query])[0]
        
        # Build filter
        where_filter = None
        if framework:
            where_filter = {"framework": framework}
        
        # Search ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k,
            where=where_filter
        )
        
        # Format results
        search_results = []
        for i in range(len(results['ids'][0])):
            search_results.append({
                'id': results['ids'][0][i],
                'content': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i] if 'distances' in results else None
            })
        
        return search_results
```

### 6. Update Scheduler

**Purpose**: Periodically refresh documentation

**Implementation**:

```python
from celery import Celery
from celery.schedules import crontab

@celery_app.task(name="docs_agent.update_framework")
def update_framework_task(framework_name: str):
    """Update documentation for a single framework."""
    
    # Initialize components
    discovery = FrameworkDiscovery()
    scraper = DocumentationScraper(config)
    normalizer = DocumentationNormalizer()
    indexer = DocumentationIndexer(config)
    
    # Find framework
    frameworks = discovery.discover()
    framework = next((f for f in frameworks if f['name'] == framework_name), None)
    
    if not framework:
        return {"error": f"Framework {framework_name} not found"}
    
    # Scrape documentation
    scraped_data = await scraper.scrape_framework(framework)
    
    # Normalize pages
    for page in scraped_data['pages']:
        page['markdown'] = normalizer.normalize(page)
    
    # Index documentation
    metadata = indexer.index_framework(framework_name, scraped_data['pages'])
    
    return {
        "framework": framework_name,
        "pages_updated": metadata['total_pages'],
        "updated_at": metadata['indexed_at']
    }

@celery_app.task(name="docs_agent.update_all_frameworks")
def update_all_frameworks_task():
    """Update all framework documentation."""
    
    discovery = FrameworkDiscovery()
    frameworks = discovery.discover()
    
    results = []
    for framework in sorted(frameworks, key=lambda x: x['priority']):
        result = update_framework_task.delay(framework['name'])
        results.append(result)
    
    return {"frameworks_queued": len(results)}

# Schedule periodic updates
celery_app.conf.beat_schedule = {
    'update-docs-weekly': {
        'task': 'docs_agent.update_all_frameworks',
        'schedule': crontab(day_of_week='sunday', hour=2, minute=0),
    },
}
```

## API Endpoints

```python
# Search documentation
GET /api/v1/docs/search?q=how+to+create+agent&framework=crewai&limit=5
Response: {
    "query": "how to create agent",
    "results": [
        {
            "framework": "crewai",
            "title": "Creating Agents",
            "url": "https://docs.crewai.com/core-concepts/agents",
            "file": "crewai/core-concepts/agents.md",
            "snippet": "...",
            "relevance": 0.92
        }
    ],
    "total": 5
}

# Get framework documentation
GET /api/v1/docs/frameworks/{framework_name}
Response: {
    "name": "CrewAI",
    "total_pages": 45,
    "indexed_at": "2025-10-30T...",
    "pages": [...]
}

# Trigger documentation update
POST /api/v1/docs/frameworks/{framework_name}/update
Response: {
    "task_id": "uuid",
    "status": "queued"
}

# Get update status
GET /api/v1/docs/tasks/{task_id}
Response: {
    "task_id": "uuid",
    "status": "completed",
    "result": {...}
}
```

## Configuration

```python
# config/docs_agent.yaml
docs_agent:
  # Discovery
  overview_file: "docs/frameworks/AI_FRAMEWORKS_OVERVIEW.md"
  
  # Scraping
  firecrawl_api_key: "${FIRECRAWL_API_KEY}"
  max_depth: 3
  max_pages: 100
  rate_limit: 10  # requests per second
  
  # Storage
  docs_path: "docs/frameworks"
  chroma_path: ".augment/chroma"
  
  # Embeddings
  embedding_model: "all-MiniLM-L6-v2"
  chunk_size: 512
  
  # Updates
  update_schedule: "weekly"  # daily, weekly, monthly
  update_day: "sunday"
  update_hour: 2
  
  # LLM (for ScrapeGraphAI)
  openai_api_key: "${OPENAI_API_KEY}"
  llm_model: "gpt-3.5-turbo"
```

## Success Criteria

- [ ] Framework discovery working from overview file
- [ ] ScrapeGraphAI integration functional
- [ ] Firecrawl integration functional
- [ ] HTML to Markdown conversion clean
- [ ] Documentation stored in correct structure
- [ ] Vector embeddings generated successfully
- [ ] ChromaDB search working
- [ ] Contextual search returning relevant results
- [ ] Periodic updates scheduled and running
- [ ] API endpoints functional
- [ ] Tests passing (>80% coverage)

## Dependencies

- Core backend (FastAPI + Celery + PostgreSQL)
- AI Frameworks Overview document
- ScrapeGraphAI API access
- Firecrawl API access
- OpenAI API access (for ScrapeGraphAI)

## Timeline

- **Week 1**: Discovery, scraping, and normalization
- **Week 2**: Indexing and vector embeddings
- **Week 3**: Search API and update scheduler
- **Week 4**: Testing, optimization, documentation

## Next Steps

1. Set up ScrapeGraphAI and Firecrawl API keys
2. Implement discovery module
3. Build scraper with both tools
4. Create normalizer
5. Implement indexer with ChromaDB
6. Build search API
7. Add update scheduler
8. Test with real frameworks
9. Optimize and refine

