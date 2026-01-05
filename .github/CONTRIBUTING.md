# Contributing to CDES Python SDK

Thank you for contributing to the CDES Python SDK!

## Overview

This SDK provides Python tools for working with CDES specifications:

- Schema validation
- Data serialization/deserialization
- Type-safe models

## Development Setup

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
git clone https://github.com/cannabis-data-standard/cdes-sdk-python.git
cd cdes-sdk-python
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest tests/ -v
```

### Running Linting

```bash
ruff check .
mypy cdes
```

## Code Standards

### Style

- Follow PEP 8
- Use type hints for all public functions
- Maximum line length: 88 characters (Black default)

### Documentation

- Docstrings for all public modules, classes, functions
- Use Google-style docstrings

### Example

```python
def validate_strain(data: dict[str, Any]) -> ValidationResult:
    """Validate strain data against CDES schema.
    
    Args:
        data: Dictionary containing strain data to validate.
        
    Returns:
        ValidationResult with valid flag and any errors.
        
    Raises:
        SchemaNotFoundError: If strain schema cannot be loaded.
    """
```

## Pull Request Process

1. Fork and create a feature branch
2. Write tests for new functionality
3. Ensure all tests pass
4. Update documentation
5. Submit PR with clear description

### PR Checklist

- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Type hints added
- [ ] Linting passes
- [ ] All tests pass

## Versioning

We use semantic versioning:

- MAJOR: Breaking API changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

---

**License**: Apache 2.0
