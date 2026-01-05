# CDES Python SDK

Official Python SDK for the [Cannabis Data Exchange Standard (CDES)](https://cdes.acidni.net).

## Installation

```bash
pip install cdes
```

## Quick Start

### Validate Cannabis Data

```python
from cdes import validate_strain, validate_terpene_profile

# Validate a strain record
result = validate_strain({
    "id": "blue-dream",
    "name": "Blue Dream",
    "type": "hybrid"
})

if result.valid:
    print(" Strain data is valid!")
else:
    for error in result.errors:
        print(f" {error.path}: {error.message}")
```

### Access Reference Data

```python
from cdes import get_terpene_library, get_terpene_by_id

# Get the complete terpene library
library = get_terpene_library()
print(f"Library version: {library.version}")
print(f"Total terpenes: {len(library.terpenes)}")

# Look up a specific terpene
myrcene = get_terpene_by_id("terp-myrcene")
print(f"{myrcene.name}: CAS {myrcene.casNumber}")
print(f"Aromas: {', '.join(myrcene.aroma)}")
```

## Features

- **Schema Validation** - Validate strains, COAs, terpene profiles, and cannabinoid profiles
- **Reference Data** - Access the official CDES terpene library with CAS numbers and effects
- **Type Safety** - Full type hints and dataclass models
- **Zero Dependencies** - Pure Python, no external packages required

## API Reference

### Validators

| Function | Description |
|----------|-------------|
| `validate_strain(data)` | Validate a strain record |
| `validate_coa(data)` | Validate a Certificate of Analysis |
| `validate_terpene_profile(data)` | Validate a terpene profile |
| `validate_cannabinoid_profile(data)` | Validate a cannabinoid profile |

### Reference Data

| Function | Description |
|----------|-------------|
| `get_terpene_library()` | Get the complete terpene library |
| `get_terpene_by_id(id)` | Look up a terpene by CDES ID |

### Models

| Class | Description |
|-------|-------------|
| `ValidationResult` | Result of a validation operation |
| `ValidationError` | A single validation error |
| `Terpene` | A cannabis terpene |
| `TerpeneLibrary` | The complete terpene reference |

## Development

```bash
# Clone the repository
git clone https://github.com/Acidni-LLC/cdes-sdk-python.git
cd cdes-sdk-python

# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black cdes tests
```

## Related Projects

- [cdes-spec](https://github.com/Acidni-LLC/cdes-spec) - JSON Schema specifications
- [cdes-reference-data](https://github.com/Acidni-LLC/cdes-reference-data) - Reference datasets
- [cdes-website](https://github.com/Acidni-LLC/cdes-website) - Documentation website

## License

MIT License - see [LICENSE](LICENSE) for details.

## Maintained By

[Acidni LLC](https://acidni.com) - Cannabis Data Analytics & AI Solutions
