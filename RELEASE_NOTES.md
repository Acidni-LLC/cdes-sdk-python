# CDES Python SDK v1.2.0 - Genetics Domain

##  New Features

### Comprehensive Genetics Support
This release adds a complete genetics domain to CDES, enabling seed banks, dispensaries, and researchers to share and compare strain genetics data in a standardized format.

### New Enums
- **BreedingTechnique**: cross, backcross, selfing, landrace, polyhybrid, f1-f5, s1-s2, bx1-bx3, clone, tissue_culture
- **GeneticsStability**: unstable, semi_stable, stable, ibl, landrace, clone_only
- **GeneticsConfidence**: verified, high, medium, low, disputed
- **LineageRelationship**: parent, mother, father, grandparent, ancestor, sibling, child

### New Dataclasses
- **GeneticsProfile**: Main entity with multi-parent support, breeder info, indica/sativa %, breeding technique, stability, full lineage tree, provenance sources, phenotypes, awards
- **LineageNode**: Recursive lineage tree node for complex breeding histories
- **GeneticsSource**: Provenance tracking with source name, type, URL, confidence level, verification
- **PhenotypeVariant**: Phenotype expression tracking with distinguishing traits

### Updated Models
- **Strain**: Now includes \genetics_profile: Optional[GeneticsProfile]\ alongside existing \genetics: str\ for backward compatibility

##  Installation
\\\ash
pip install cdes==1.2.0
\\\

##  Quick Start
\\\python
from cdes import GeneticsProfile, BreedingTechnique, GeneticsStability, GeneticsSource

# Create a genetics profile
gsc = GeneticsProfile(
    parent_1="OG Kush",
    parent_2="Durban Poison",
    breeder="Cookie Fam",
    breeding_technique=BreedingTechnique.F1,
    stability=GeneticsStability.STABLE,
    indica_pct=60,
    sativa_pct=40,
)

# Add provenance
gsc.add_source(GeneticsSource(
    source_name="SeedFinder",
    source_type="database",
    confidence=GeneticsConfidence.HIGH,
))

# Serialize to JSON
data = gsc.to_dict()
\\\

##  Links
- [PyPI Package](https://pypi.org/project/cdes/1.2.0/)
- [Documentation](https://cdes.terprint.com)
