"""
Documentation Agent - Framework Scraper

Automatically discovers, scrapes, normalizes, indexes, and maintains
local mirrors of AI framework documentation.

Usage:
    from src.agents.documentation_agent import DocumentationAgent
    
    agent = DocumentationAgent()
    agent.discover_frameworks()
    agent.scrape_all()
    agent.search("how to create an agent")
"""

from .agent import DocumentationAgent
from .discovery import FrameworkDiscovery
from .scraper import DocumentationScraper
from .normalizer import DocumentationNormalizer
from .indexer import DocumentationIndexer
from .search import DocumentationSearch

__all__ = [
    "DocumentationAgent",
    "FrameworkDiscovery",
    "DocumentationScraper",
    "DocumentationNormalizer",
    "DocumentationIndexer",
    "DocumentationSearch",
]

__version__ = "1.0.0"

