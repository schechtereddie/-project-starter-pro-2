# Development Standards Specification

**Version**: 1.0.0  
**Last Updated**: 2025-10-30  
**Status**: Draft  

## Purpose

Define code quality standards, workflow conventions, documentation requirements, and deployment procedures for Project Starter Pro 2 to ensure consistent, maintainable, and high-quality development.

---

## Code Quality Standards

### Python Standards

#### Style Guide
- **Base Standard**: PEP 8 compliance
- **Formatter**: `black` (line length: 100 characters)
- **Linter**: `flake8` with strict configuration
- **Type Checker**: `mypy` in strict mode
- **Import Sorter**: `isort` for organized imports

#### Configuration Files

**pyproject.toml**:
```toml
[tool.black]
line-length = 100
target-version = ['py313']
include = '\.pyi?$'

[tool.isort]
profile = "black"
line_length = 100

[tool.mypy]
python_version = "3.13"
strict = true
warn_return_any = true
warn_unused_configs = true

[tool.pytest.ini_options]
minversion = "7.0"
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "--cov=src --cov-report=html --cov-report=term-missing"
```

#### Code Structure Example

```python
"""Module for project management functionality.

This module provides the ProjectManager class for handling
project lifecycle operations including creation, updates,
and archival.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field, validator

logger = logging.getLogger(__name__)


class Project(BaseModel):
    """Project data model with validation."""
    
    id: str = Field(default_factory=lambda: f"proj_{uuid4().hex[:12]}")
    name: str = Field(..., min_length=1, max_length=200)
    description: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    @validator('updated_at')
    def updated_after_created(cls, v: datetime, values: dict[str, Any]) -> datetime:
        """Ensure updated_at is not before created_at."""
        if 'created_at' in values and v < values['created_at']:
            raise ValueError('updated_at must be >= created_at')
        return v


class ProjectManager:
    """Manages project lifecycle operations."""
    
    def __init__(self, data_dir: str) -> None:
        """Initialize ProjectManager.
        
        Args:
            data_dir: Base directory for project data storage
        """
        self.data_dir = data_dir
        logger.info(f"ProjectManager initialized with data_dir: {data_dir}")
    
    def create_project(self, name: str, description: str = "") -> Project:
        """Create a new project.
        
        Args:
            name: Project name (1-200 characters)
            description: Optional project description
            
        Returns:
            Created Project instance
            
        Raises:
            ValueError: If name is invalid
            
        Examples:
            >>> pm = ProjectManager("/data")
            >>> project = pm.create_project("My Project")
            >>> project.name
            'My Project'
        """
        project = Project(name=name, description=description)
        self._save_project(project)
        logger.info(f"Created project: {project.id}")
        return project
    
    def _save_project(self, project: Project) -> None:
        """Save project to disk (private method)."""
        # Implementation details...
        pass
```

#### Testing Standards

**Test Structure**:
```python
"""Tests for project_manager module."""

import pytest
from datetime import datetime
from pathlib import Path

from psp.core.project_manager import Project, ProjectManager


class TestProject:
    """Tests for Project model."""
    
    def test_project_creation_with_defaults(self) -> None:
        """Test creating project with default values."""
        project = Project(name="Test Project")
        
        assert project.name == "Test Project"
        assert project.description == ""
        assert project.id.startswith("proj_")
        assert isinstance(project.created_at, datetime)
    
    def test_project_name_validation(self) -> None:
        """Test project name validation rules."""
        with pytest.raises(ValueError, match="min_length"):
            Project(name="")
        
        with pytest.raises(ValueError, match="max_length"):
            Project(name="x" * 201)
    
    @pytest.mark.parametrize("name,expected", [
        ("Simple", "Simple"),
        ("With Spaces", "With Spaces"),
        ("With-Dashes", "With-Dashes"),
    ])
    def test_project_name_formats(self, name: str, expected: str) -> None:
        """Test various valid project name formats."""
        project = Project(name=name)
        assert project.name == expected


class TestProjectManager:
    """Tests for ProjectManager class."""
    
    @pytest.fixture
    def temp_data_dir(self, tmp_path: Path) -> Path:
        """Provide temporary data directory."""
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        return data_dir
    
    @pytest.fixture
    def project_manager(self, temp_data_dir: Path) -> ProjectManager:
        """Provide ProjectManager instance."""
        return ProjectManager(str(temp_data_dir))
    
    def test_create_project_success(self, project_manager: ProjectManager) -> None:
        """Test successful project creation."""
        project = project_manager.create_project("Test Project", "Description")
        
        assert project.name == "Test Project"
        assert project.description == "Description"
        assert project.id is not None
    
    def test_create_project_invalid_name(self, project_manager: ProjectManager) -> None:
        """Test project creation with invalid name."""
        with pytest.raises(ValueError):
            project_manager.create_project("")
```

**Running Tests**:
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_project_manager.py

# Run specific test
pytest tests/unit/test_project_manager.py::TestProject::test_project_creation_with_defaults

# Run with markers
pytest -m "not slow"

# Run in parallel
pytest -n auto
```

---

### Node.js/TypeScript Standards

#### Style Guide
- **Formatter**: `prettier` with default configuration
- **Linter**: `eslint` with TypeScript plugin
- **Type Checker**: `tsc` in strict mode

#### Configuration Files

**package.json**:
```json
{
  "scripts": {
    "lint": "eslint . --ext .ts,.tsx",
    "format": "prettier --write .",
    "type-check": "tsc --noEmit",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage"
  },
  "devDependencies": {
    "@typescript-eslint/eslint-plugin": "^6.0.0",
    "@typescript-eslint/parser": "^6.0.0",
    "eslint": "^8.0.0",
    "prettier": "^3.0.0",
    "typescript": "^5.0.0",
    "jest": "^29.0.0"
  }
}
```

**.eslintrc.json**:
```json
{
  "parser": "@typescript-eslint/parser",
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:@typescript-eslint/recommended-requiring-type-checking",
    "prettier"
  ],
  "parserOptions": {
    "ecmaVersion": 2022,
    "sourceType": "module",
    "project": "./tsconfig.json"
  },
  "rules": {
    "@typescript-eslint/explicit-function-return-type": "error",
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/no-unused-vars": "error"
  }
}
```

**tsconfig.json**:
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

#### Code Structure Example

```typescript
/**
 * Project management CLI commands
 */

import { Command } from 'commander';
import { ProjectManager } from './project-manager';

interface CreateProjectOptions {
  type?: string;
  template?: string;
  description?: string;
}

/**
 * Create a new project
 * @param name - Project name
 * @param options - Creation options
 * @returns Promise resolving to project ID
 */
export async function createProject(
  name: string,
  options: CreateProjectOptions
): Promise<string> {
  const manager = new ProjectManager();
  
  const project = await manager.create({
    name,
    type: options.type ?? 'software',
    template: options.template,
    description: options.description ?? '',
  });
  
  console.log(`Created project: ${project.id}`);
  return project.id;
}

/**
 * Register project commands
 * @param program - Commander program instance
 */
export function registerProjectCommands(program: Command): void {
  const projectCmd = program
    .command('project')
    .description('Manage projects');
  
  projectCmd
    .command('create <name>')
    .description('Create a new project')
    .option('-t, --type <type>', 'Project type')
    .option('--template <id>', 'Template ID')
    .option('-d, --description <desc>', 'Project description')
    .action(async (name: string, options: CreateProjectOptions) => {
      await createProject(name, options);
    });
}
```

#### Testing Example

```typescript
import { describe, it, expect, beforeEach, jest } from '@jest/globals';
import { ProjectManager } from './project-manager';

describe('ProjectManager', () => {
  let manager: ProjectManager;
  
  beforeEach(() => {
    manager = new ProjectManager('/tmp/test-data');
  });
  
  describe('create', () => {
    it('should create project with valid name', async () => {
      const project = await manager.create({
        name: 'Test Project',
        type: 'software',
      });
      
      expect(project.name).toBe('Test Project');
      expect(project.type).toBe('software');
      expect(project.id).toMatch(/^proj_[a-z0-9]+$/);
    });
    
    it('should throw error for empty name', async () => {
      await expect(
        manager.create({ name: '', type: 'software' })
      ).rejects.toThrow('Name cannot be empty');
    });
  });
});
```

---

## Git Workflow

### Branch Strategy

**Branch Types**:
- `main` - Production-ready code
- `develop` - Integration branch (optional)
- `feature/<description>` - New features
- `fix/<description>` - Bug fixes
- `chore/<description>` - Maintenance tasks
- `docs/<description>` - Documentation updates

**Branch Naming**:
```bash
# Good examples
feature/add-project-templates
fix/project-deletion-bug
chore/update-dependencies
docs/api-documentation

# Bad examples
feature/new-stuff
fix/bug
my-branch
```

### Commit Message Format

**Conventional Commits**:
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements

**Examples**:
```bash
# Feature
feat(project-manager): add project archival functionality

Implement archive_project method to move completed projects
to archived state while preserving all data and history.

Closes #123

# Bug fix
fix(notes): resolve markdown rendering issue with code blocks

Code blocks with triple backticks were not rendering correctly
due to incorrect escaping in the parser.

Fixes #456

# Documentation
docs(api): update REST API endpoint documentation

Add examples for all project management endpoints and
clarify authentication requirements.

# Chore
chore(deps): update pytest to 7.4.0

Update pytest and related testing dependencies to latest
stable versions.
```

### Pull Request Process

1. **Create Feature Branch**:
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make Changes and Commit**:
   ```bash
   git add .
   git commit -m "feat(module): add new feature"
   ```

3. **Push to Remote**:
   ```bash
   git push origin feature/my-feature
   ```

4. **Create Pull Request**:
   - Clear title and description
   - Link related issues
   - Add screenshots/examples if applicable
   - Request reviewers

5. **Code Review**:
   - At least one approval required
   - All CI checks must pass
   - Address review feedback

6. **Merge**:
   - Squash and merge (preferred)
   - Delete branch after merge

### Pre-commit Hooks

**`.pre-commit-config.yaml`**:
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.10.0
    hooks:
      - id: black
        language_version: python3.13
  
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
  
  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
  
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.0.3
    hooks:
      - id: prettier
        types_or: [javascript, typescript, json, yaml, markdown]
  
  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.52.0
    hooks:
      - id: eslint
        files: \.[jt]sx?$
        types: [file]
```

**Install hooks**:
```bash
pip install pre-commit
pre-commit install
```

---

## Documentation Standards

### Code Documentation

**Required Documentation**:
- All public modules, classes, and functions
- Complex algorithms or business logic
- API endpoints and contracts
- Configuration options

**Python Docstrings** (Google Style):
```python
def process_data(input_data: list[dict], validate: bool = True) -> dict:
    """Process input data and return aggregated results.
    
    This function takes a list of data dictionaries, optionally validates
    them, and returns aggregated statistics.
    
    Args:
        input_data: List of dictionaries containing data to process
        validate: Whether to validate input data (default: True)
        
    Returns:
        Dictionary containing aggregated results with keys:
        - 'total': Total number of items processed
        - 'valid': Number of valid items
        - 'errors': List of validation errors
        
    Raises:
        ValueError: If input_data is empty
        ValidationError: If validation fails and validate=True
        
    Examples:
        >>> data = [{'value': 1}, {'value': 2}]
        >>> result = process_data(data)
        >>> result['total']
        2
        
    Note:
        This function modifies the input data in-place if validation
        is enabled.
    """
```

**TypeScript Documentation** (TSDoc):
```typescript
/**
 * Process input data and return aggregated results
 *
 * This function takes an array of data objects, optionally validates
 * them, and returns aggregated statistics.
 *
 * @param inputData - Array of objects containing data to process
 * @param validate - Whether to validate input data
 * @returns Object containing aggregated results
 * @throws {ValueError} If inputData is empty
 * @throws {ValidationError} If validation fails
 *
 * @example
 * ```typescript
 * const data = [{ value: 1 }, { value: 2 }];
 * const result = processData(data);
 * console.log(result.total); // 2
 * ```
 */
export function processData(
  inputData: DataObject[],
  validate: boolean = true
): AggregatedResult {
  // Implementation
}
```

### Project Documentation

**Required Files**:
- `README.md` - Project overview and quick start
- `CONTRIBUTING.md` - Contribution guidelines
- `CHANGELOG.md` - Version history
- `docs/` - Detailed documentation

**README.md Template**:
```markdown
# Project Starter Pro 2

Unified workspace for planning, tracking, and analyzing software or business projects.

## Features

- 📊 Project management with templates
- 📝 Markdown notes with AI assistance
- 🔍 Research hub with auto-classification
- 📈 Analytics and insights
- ⚙️ Flexible configuration

## Quick Start

\`\`\`bash
# Install dependencies
pip install -r requirements.txt
npm install

# Run setup
./scripts/setup.sh

# Start application
psp project create "My First Project"
\`\`\`

## Documentation

- [User Guide](docs/user-guide.md)
- [API Reference](docs/api/)
- [Development Guide](docs/development.md)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT License - see [LICENSE](LICENSE)
```

---

## Deployment Standards

### Environment Management

**Environments**:
- `development` - Local development
- `staging` - Pre-production testing
- `production` - Live deployment

**Configuration**:
```bash
# .env.development
LOG_LEVEL=DEBUG
AUTO_SYNC=false
ANALYTICS_ENABLED=true

# .env.production
LOG_LEVEL=INFO
AUTO_SYNC=true
ANALYTICS_ENABLED=true
```

### Deployment Checklist

**Pre-Deployment**:
- [ ] All tests passing
- [ ] Code reviewed and approved
- [ ] Documentation updated
- [ ] Version bumped (semantic versioning)
- [ ] CHANGELOG.md updated
- [ ] Database migrations tested
- [ ] Backup created
- [ ] Rollback plan documented

**Deployment**:
- [ ] Deploy to staging first
- [ ] Run smoke tests
- [ ] Monitor logs and metrics
- [ ] Deploy to production
- [ ] Verify deployment
- [ ] Tag release in Git

**Post-Deployment**:
- [ ] Monitor for errors
- [ ] Check performance metrics
- [ ] Verify all features working
- [ ] Update status page
- [ ] Notify stakeholders

### Versioning

**Semantic Versioning** (MAJOR.MINOR.PATCH):
- `MAJOR`: Breaking changes
- `MINOR`: New features (backward compatible)
- `PATCH`: Bug fixes

**Version Bump Script**:
```bash
#!/usr/bin/env bash
# scripts/bump-version.sh

set -euo pipefail

VERSION_TYPE="${1:-patch}"  # major|minor|patch

# Update version in files
poetry version "$VERSION_TYPE"
npm version "$VERSION_TYPE" --no-git-tag-version

# Get new version
NEW_VERSION=$(poetry version -s)

# Update CHANGELOG
echo "## [$NEW_VERSION] - $(date +%Y-%m-%d)" >> CHANGELOG.md

# Commit and tag
git add pyproject.toml package.json CHANGELOG.md
git commit -m "chore: bump version to $NEW_VERSION"
git tag "v$NEW_VERSION"

echo "Version bumped to $NEW_VERSION"
```

---

## Continuous Integration

### CI Pipeline

**GitHub Actions** (`.github/workflows/ci.yml`):
```yaml
name: CI

on: [push, pull_request]

jobs:
  test-python:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.13'
      - run: pip install -r requirements.txt
      - run: black --check .
      - run: flake8 .
      - run: mypy .
      - run: pytest --cov=src --cov-report=xml
      - uses: codecov/codecov-action@v3
  
  test-node:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '20'
      - run: npm ci
      - run: npm run lint
      - run: npm run type-check
      - run: npm test -- --coverage
```

---

## References

- PEP 8: https://peps.python.org/pep-0008/
- Black: https://black.readthedocs.io/
- Conventional Commits: https://www.conventionalcommits.org/
- Semantic Versioning: https://semver.org/

