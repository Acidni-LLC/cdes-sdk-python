# CDES AI Software Engineer & Architect Guidelines

---

> ** PROJECT**: Cannabis Data Exchange Standard (CDES)
> ** ORGANIZATION**: Acidni LLC (internal management)
> ** PUBLIC REPOS**: cdes-spec, cdes-reference-data, cdes-sdk-python

---

##  CRITICAL DIRECTIVES  READ FIRST 

### DIRECTIVE 1: NEVER MODIFY CODE OUTSIDE YOUR APP'S HOME REPO

- **EACH CDES PROJECT LIVES IN ITS OWN REPOSITORY**
- **cdes-acidni** = Internal management (private)
- **cdes-spec** = Public schemas and specifications
- **cdes-reference-data** = Public terpene library, cannabinoid registry
- **cdes-sdk-python** = Public Python SDK
- Cross-cutting changes are coordinated from cdes-acidni

### DIRECTIVE 2: SCHEMA VERSIONING

- All schemas use **JSON Schema Draft 2020-12**
- Schemas are versioned: `schemas/v1/`, `schemas/v2/`
- **NEVER make breaking changes** to released schemas
- Breaking changes require new major version

### DIRECTIVE 3: REFERENCE DATA INTEGRITY

- Terpene library entries have **CAS numbers** and **PubChem IDs**
- All reference data is **publicly verifiable**
- Changes require scientific sources

### DIRECTIVE 4: LICENSING

| Repository | License |
|------------|---------|
| cdes-spec | CC BY 4.0 |
| cdes-reference-data | CC0 1.0 (Public Domain) |
| cdes-sdk-* | Apache 2.0 |

---

## Project Context

**CDES** is an open industry standard for cannabis data interoperability. It defines:
- **JSON Schemas** for strains, COAs, terpene profiles, cannabinoid profiles
- **Reference Data** including the official terpene library
- **APIs** for data exchange between systems
- **SDKs** for validation and integration

### Repository Structure

```
Acidni-LLC/
 cdes-acidni/           # Internal management (THIS REPO)
    .github/           # Copilot instructions, tooling
    strategy/          # Strategic planning docs
    governance/        # Charter, policies
    architecture/      # ADRs
    tools/             # Management scripts
 cdes-spec/             # Public specifications
    schemas/v1/        # JSON schemas
    api/v1/            # OpenAPI specs
    vocabulary/        # Controlled vocabularies
 cdes-reference-data/   # Public reference data
    terpenes/          # Terpene library
    cannabinoids/      # Cannabinoid registry
    strains/           # Strain registry
 cdes-sdk-python/       # Python SDK
     cdes/              # Package source
     tests/             # Test suite
```

---

##  CDES SCHEMAS QUICK REFERENCE

### Core Schemas (v1)

| Schema | Purpose | Status |
|--------|---------|--------|
| `strain.json` | Cannabis strain definitions | Stable |
| `coa.json` | Certificate of Analysis | Stable |
| `terpene.json` | Terpene definition | Stable |
| `terpene-profile.json` | Terpene measurements | Stable |
| `cannabinoid-profile.json` | Cannabinoid measurements | Stable |

### Reference Data

| Dataset | Records | Source |
|---------|---------|--------|
| Terpene Library | 24 | CAS, PubChem |
| Cannabinoid Registry | TBD | IUPAC |

---

## Technology Standards

| Component | Technology |
|-----------|------------|
| Schema Language | JSON Schema Draft 2020-12 |
| API Specs | OpenAPI 3.1 |
| Python SDK | Python 3.10+ |
| Documentation | Markdown |

---

## Code Style Guidelines

### JSON Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.cannabis-data-standard.org/v1/strain.json",
  "title": "CDES Strain",
  "description": "Cannabis strain definition",
  "type": "object"
}
```

### Python

```python
from cdes import validate_strain

result = validate_strain(data)
if not result.valid:
    for error in result.errors:
        print(f"{error.path}: {error.message}")
```

---

## Commit Message Format

Use conventional commits:
- `feat(spec): add cannabinoid-profile schema`
- `fix(sdk): handle missing terpene percentages`
- `docs(readme): update quick start guide`
- `data(terpenes): add valencene entry`

---

## Next Steps

1. Complete Python SDK implementation
2. Add cannabinoid library reference data
3. Create TypeScript SDK
4. Launch public documentation website
5. Submit to industry standards bodies
