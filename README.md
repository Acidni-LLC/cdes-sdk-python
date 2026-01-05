# CDES Python SDK

> **Official Python SDK for the Cannabis Data Exchange Standard**

[![PyPI version](https://badge.fury.io/py/cdes.svg)](https://badge.fury.io/py/cdes)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Installation

```bash
pip install cdes
```

## Usage

```python
from cdes import validate_strain, validate_coa

# Validate a strain
strain_data = {
    "name": "Gelato",
    "type": "hybrid",
    "thcRange": {"min": 20, "max": 25}
}
result = validate_strain(strain_data)
print(f"Valid: {result.valid}")

# Validate a COA
coa_data = {...}
result = validate_coa(coa_data)
```

## License

Apache 2.0
