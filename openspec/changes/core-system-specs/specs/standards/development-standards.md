# Development Standards Specification

**Version**: 1.0.0  
**Last Updated**: 2025-10-30  
**Status**: Draft  

## Purpose

Define coding standards, testing requirements, documentation practices, and deployment procedures for Project Starter Pro 2.

---

## 1. Code Standards

### Python Standards

#### Style Guide
- **Base**: PEP 8 compliance
- **Formatter**: `black` (line length: 100)
- **Linter**: `ruff` with strict settings
- **Type Checker**: `mypy` in strict mode

#### Code Structure
```python
"""Module docstring.

Detailed description of module purpose and usage.
"""

from __future__ import annotations

import standard_library
from typing import Any

import third_party
from third_party import SpecificClass

from psp.core import local_module


class ExampleClass:
    """Class docstring with purpose and usage."""
    
    def __init__(self, param: str) -> None:
        """Initialize with parameters.
        
        Args:
            param: Description of parameter
        """
        self._param = param
    
    def public_method(self, input_a: str) -> str:
        """Public method with clear purpose.
        
        Args:
            input_a: Input description
            
        Returns:
            Output description
            
        Raises:
            ValueError: When input is invalid
        """
        if not input_a:
            raise ValueError("input_a cannot be empty")
        return self._private_method(input_a)
    
    def _private_method(self, value: str) -> str:
        """Private helper method."""
        return f"{self._param}: {value}"
```

#### Naming Conventions
- **Modules**: `snake_case.py`
- **Classes**: `PascalCase`
- **Functions/Methods**: `snake_case()`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private**: `_leading_underscore`
- **Protected**: `_single_underscore`

#### Type Hints
- All function signatures must have type hints
- Use `from __future__ import annotations` for forward references
- Prefer built-in types over typing module when possible (Python 3.9+)
- Use `| None` instead of `Optional`
- Use `list[T]`, `dict[K, V]` instead of `List[T]`, `Dict[K, V]`

### Node.js/TypeScript Standards

#### Style Guide
- **Formatter**: `prettier` (default config)
- **Linter**: `eslint` with TypeScript plugin
- **Type Checker**: `tsc` in strict mode

#### Code Structure
```typescript
/**
 * Module description
 */

import { standardLibrary } from 'node:fs';
import thirdParty from 'third-party';
import { localModule } from './local';

/**
 * Interface description
 */
export interface ExampleInterface {
  id: string;
  name: string;
  metadata?: Record<string, unknown>;
}

/**
 * Class description
 */
export class ExampleClass {
  private readonly param: string;

  constructor(param: string) {
    this.param = param;
  }

  /**
   * Public method description
   * @param inputA - Input description
   * @returns Output description
   * @throws {Error} When input is invalid
   */
  public publicMethod(inputA: string): string {
    if (!inputA) {
      throw new Error('inputA cannot be empty');
    }
    return this.privateMethod(inputA);
  }

  private privateMethod(value: string): string {
    return `${this.param}: ${value}`;
  }
}
```

#### Naming Conventions
- **Files**: `kebab-case.ts`
- **Classes/Interfaces**: `PascalCase`
- **Functions/Variables**: `camelCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private**: `#privateField` or `private` keyword

### Shell Script Standards

#### Style Guide
- **Formatter**: `shfmt` (indent: 2 spaces)
- **Linter**: `shellcheck`
- **Shell**: `bash` (not sh, zsh, etc.)

#### Script Template
```bash
#!/usr/bin/env bash
# script_name.sh
# Brief description of script purpose
#
# Usage: ./script_name.sh [OPTIONS] ARGS
# Dependencies: jq, curl
# Environment: FOO, BAR

set -euo pipefail

# Constants
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Functions
function main() {
    local arg="${1:-default}"
    
    echo "Processing: $arg"
    # Implementation
}

function cleanup() {
    echo "Cleaning up..."
    # Cleanup logic
}

# Trap errors
trap cleanup EXIT

# Entry point
main "$@"
```

---

## 2. Testing Standards

### Test Coverage Requirements
- **Minimum**: 80% code coverage
- **Critical Paths**: 100% coverage
- **New Code**: Must include tests
- **Bug Fixes**: Must include regression test

### Python Testing

#### Framework
- **Unit Tests**: `pytest`
- **Coverage**: `pytest-cov`
- **Mocking**: `pytest-mock` or `unittest.mock`

#### Test Structure
```python
"""Test module for example_module."""

import pytest
from psp.core.example_module import ExampleClass


class TestExampleClass:
    """Tests for ExampleClass."""
    
    @pytest.fixture
    def example_instance(self):
        """Fixture providing ExampleClass instance."""
        return ExampleClass("test")
    
    def test_public_method_success(self, example_instance):
        """Test public_method with valid input."""
        result = example_instance.public_method("input")
        assert result == "test: input"
    
    def test_public_method_empty_input(self, example_instance):
        """Test public_method raises error on empty input."""
        with pytest.raises(ValueError, match="cannot be empty"):
            example_instance.public_method("")
    
    @pytest.mark.parametrize("input_val,expected", [
        ("a", "test: a"),
        ("b", "test: b"),
    ])
    def test_public_method_parametrized(
        self, example_instance, input_val, expected
    ):
        """Test public_method with multiple inputs."""
        assert example_instance.public_method(input_val) == expected
```

#### Test Commands
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html --cov-report=term

# Run specific test file
pytest tests/unit/test_example.py

# Run with markers
pytest -m "not slow"
```

### Node.js/TypeScript Testing

#### Framework
- **Unit Tests**: `vitest`
- **Coverage**: Built-in vitest coverage
- **Mocking**: `vitest` mocking utilities

#### Test Structure
```typescript
import { describe, it, expect, beforeEach } from 'vitest';
import { ExampleClass } from './example';

describe('ExampleClass', () => {
  let instance: ExampleClass;

  beforeEach(() => {
    instance = new ExampleClass('test');
  });

  it('should process valid input', () => {
    const result = instance.publicMethod('input');
    expect(result).toBe('test: input');
  });

  it('should throw error on empty input', () => {
    expect(() => instance.publicMethod('')).toThrow('cannot be empty');
  });

  it.each([
    ['a', 'test: a'],
    ['b', 'test: b'],
  ])('should handle input %s', (input, expected) => {
    expect(instance.publicMethod(input)).toBe(expected);
  });
});
```

### Integration Testing
- Test module interactions
- Use test databases/fixtures
- Mock external services
- Test error scenarios

### Test Organization
```
tests/
├── unit/              # Unit tests
│   ├── core/
│   ├── cli/
│   └── integrations/
├── integration/       # Integration tests
│   ├── api/
│   └── workflows/
├── fixtures/          # Test data
│   ├── projects/
│   └── tasks/
└── conftest.py        # Pytest configuration
```

---

## 3. Documentation Standards

### Code Documentation

#### Python Docstrings
- **Style**: Google style
- **Required**: All public modules, classes, functions
- **Optional**: Private methods (when complex)

```python
def function_name(param1: str, param2: int = 0) -> bool:
    """Brief one-line summary.
    
    Detailed description of function behavior, edge cases,
    and important notes.
    
    Args:
        param1: Description of param1
        param2: Description of param2 (default: 0)
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param1 is empty
        TypeError: When param2 is not an integer
        
    Examples:
        >>> function_name("test", 5)
        True
        >>> function_name("")
        ValueError: param1 cannot be empty
    """
```

#### TypeScript Documentation
- **Style**: TSDoc
- **Required**: All exported items

```typescript
/**
 * Brief one-line summary
 *
 * Detailed description of function behavior
 *
 * @param param1 - Description of param1
 * @param param2 - Description of param2
 * @returns Description of return value
 * @throws {Error} When param1 is empty
 *
 * @example
 * ```typescript
 * functionName("test", 5);
 * // Returns: true
 * ```
 */
export function functionName(param1: string, param2: number = 0): boolean {
  // Implementation
}
```

### Project Documentation

#### Required Documents
- `README.md`: Project overview, setup, usage
- `CONTRIBUTING.md`: Contribution guidelines
- `CHANGELOG.md`: Version history
- `docs/api/`: API reference
- `docs/guides/`: User guides
- `docs/architecture/`: Technical documentation

#### README Template
```markdown
# Project Name

Brief description

## Features

- Feature 1
- Feature 2

## Installation

\`\`\`bash
# Installation steps
\`\`\`

## Usage

\`\`\`bash
# Usage examples
\`\`\`

## Documentation

- [API Reference](docs/api/)
- [User Guide](docs/guides/)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT
```

---

## 4. Version Control Standards

### Git Workflow
- **Branching**: Feature branches from `main`
- **Branch Naming**: `feat/feature-name`, `fix/bug-name`, `chore/task-name`
- **Commits**: Conventional Commits format
- **Pull Requests**: Required for all changes

### Commit Message Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Example**:
```
feat(project-manager): add project archival functionality

Implement archive_project method to move completed projects
to archived state while preserving all data.

Closes #123
```

### Pre-commit Hooks
```bash
# Format code
black .
prettier -w .

# Lint code
ruff .
eslint .

# Run tests
pytest
vitest run
```

---

## 5. Deployment Standards

### Environment Management
- **Development**: Local development environment
- **Staging**: Pre-production testing
- **Production**: Live deployment

### Configuration
- Use environment variables for secrets
- Separate config files per environment
- Never commit secrets to version control

### Deployment Checklist
- [ ] All tests passing
- [ ] Code reviewed and approved
- [ ] Documentation updated
- [ ] Version bumped
- [ ] Changelog updated
- [ ] Backup created
- [ ] Deployment script tested
- [ ] Rollback plan ready

### Versioning
- **Semantic Versioning**: MAJOR.MINOR.PATCH
- **Version Bumps**: Automated via scripts
- **Tags**: Git tags for releases

---

## 6. Code Review Standards

### Review Checklist
- [ ] Code follows style guidelines
- [ ] Tests included and passing
- [ ] Documentation updated
- [ ] No security vulnerabilities
- [ ] Performance considerations addressed
- [ ] Error handling appropriate
- [ ] Backward compatibility maintained

### Review Process
1. Author creates PR with description
2. Automated checks run (CI)
3. Reviewer(s) assigned
4. Review feedback addressed
5. Approval required before merge
6. Squash and merge to main

---

## References

- PEP 8: https://peps.python.org/pep-0008/
- Black: https://black.readthedocs.io/
- Pytest: https://docs.pytest.org/
- Vitest: https://vitest.dev/
- Conventional Commits: https://www.conventionalcommits.org/

