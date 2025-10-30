# Project Starter Pro 2

**AI-Powered Project Management and Research Platform**

A comprehensive project management system with integrated AI agents for research, documentation, analytics, and intelligent project insights.

## 🚀 Features

### Core Capabilities
- **Project Management** - Create, track, and manage projects with tasks, milestones, and dependencies
- **AI Research Agents** - Automated research with multi-agent intelligence crew
- **Documentation Agent** - Automatic framework documentation scraping and indexing
- **Analytics Engine** - Real-time metrics, insights, and performance tracking
- **Blocker Detection** - AI-powered identification and resolution of project blockers
- **Business Planning** - Automated business plan and financial model generation

### Technology Stack

**Backend**:
- FastAPI (Python 3.13.5+) - Modern async web framework
- Celery - Distributed task queue
- PostgreSQL 15+ - Relational database
- Redis 7.2+ - Message broker and caching

**Frontend**:
- React 18 + TypeScript - Component-based UI
- Tailwind CSS - Utility-first styling
- Vite - Fast build tool
- TanStack Query - Server state management
- WebSocket - Real-time updates

**AI Agents**:
- CrewAI - Multi-agent orchestration
- LangGraph - Workflow orchestration
- LangChain - Foundation layer
- OpenAI GPT-4 / Claude 3 - LLM providers
- ChromaDB - Vector database
- sentence-transformers - Embeddings

## 📋 Prerequisites

- Python 3.13.5 or higher
- Node.js 20 LTS or higher
- PostgreSQL 15+
- Redis 7.2+
- Docker (optional, for containerization)

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/schechtereddie/project-starter-pro-2.git
cd project-starter-pro-2
```

### 2. Backend Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp config/.env.sample config/.env
# Edit config/.env with your settings

# Run database migrations
alembic upgrade head
```

### 3. Frontend Setup

```bash
cd src/frontend
pnpm install
```

### 4. Start Services

```bash
# Terminal 1: Start PostgreSQL (if not using Docker)
# See PostgreSQL installation docs

# Terminal 2: Start Redis (if not using Docker)
redis-server

# Terminal 3: Start FastAPI backend
cd src/backend
uvicorn app.main:app --reload --port 8000

# Terminal 4: Start Celery worker
celery -A app.tasks.celery_app worker --loglevel=info

# Terminal 5: Start Celery beat (scheduler)
celery -A app.tasks.celery_app beat --loglevel=info

# Terminal 6: Start frontend
cd src/frontend
pnpm dev
```

## 🔑 API Keys

Set up the following API keys in `config/.env`:

```bash
# Required
OPENAI_API_KEY=your-openai-key
FIRECRAWL_API_KEY=your-firecrawl-key

# Optional
ANTHROPIC_API_KEY=your-claude-key
DEEPSEEK_API_KEY=your-deepseek-key
```

## 📚 Documentation

- **OpenSpec System**: `openspec/` - Specifications and proposals
- **API Documentation**: http://localhost:8000/docs (when running)
- **Agent Documentation**: `docs/agents/`
- **Framework Documentation**: `docs/frameworks/`

## 🤖 AI Agents

### Documentation Agent
Automatically scrapes and indexes AI framework documentation for offline access and semantic search.

```python
from src.agents.documentation_agent import DocumentationAgent

agent = DocumentationAgent()
agent.scrape_framework("CrewAI")
results = agent.search("how to create an agent")
```

### Research Intelligence Crew
Multi-agent research system with specialized agents for general, technical, and business research.

### Analytics Agent
Tracks project metrics, generates insights, and provides performance analytics.

### Blocker Agent
Detects project blockers, analyzes impact, and suggests resolutions.

### Project Insights Agent
Identifies bottlenecks, predicts risks, and provides actionable recommendations.

### Business Planning Agent
Generates business plans, financial models, and market analysis.

## 🧪 Testing

```bash
# Backend tests
pytest tests/ -v --cov=src/backend

# Frontend tests
cd src/frontend
pnpm test

# Run all tests
./scripts/test-all.sh
```

## 📦 Project Structure

```
project-starter-pro-2/
├── src/
│   ├── backend/          # FastAPI backend
│   ├── frontend/         # React frontend
│   └── agents/           # AI agents
├── openspec/             # Specifications
│   ├── specs/           # Applied specs
│   ├── changes/         # Proposals
│   └── archive/         # Archived changes
├── docs/                # Documentation
├── config/              # Configuration
├── scripts/             # Utility scripts
└── tests/               # Tests
```

## 🚢 Deployment

### Docker

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production

See `docs/deployment/` for production deployment guides.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- CrewAI for multi-agent orchestration
- LangChain for AI framework foundation
- FastAPI for the excellent web framework
- React team for the UI library

## 📞 Support

- **Issues**: https://github.com/schechtereddie/project-starter-pro-2/issues
- **Discussions**: https://github.com/schechtereddie/project-starter-pro-2/discussions
- **Email**: schechtereddie@users.gmail.com

## 🗺️ Roadmap

- [x] Core system specifications
- [x] AI frameworks overview
- [x] Documentation Agent specification
- [ ] Core backend implementation
- [ ] Frontend dashboard implementation
- [ ] Documentation Agent implementation
- [ ] Blocker Agent MVP
- [ ] Research Intelligence Crew
- [ ] Analytics Agent
- [ ] Project Insights Agent
- [ ] Business Planning Agent

---

**Built with ❤️ by the Project Starter Pro 2 Team**

