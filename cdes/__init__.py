"""
CDES Python SDK - Cannabis Data Exchange Standard

A Python implementation of the Cannabis Data Exchange Standard (CDES)
for standardized cannabis data representation.

Version: 1.2.0

Changelog:
- v1.2.0: Added comprehensive genetics domain (GeneticsProfile, LineageNode, etc.)
- v1.1.0: Initial public release with core models
"""

__version__ = "1.2.0"

# Core Enums
from .models import (
    StrainType,
    ConcentrationUnit,
    ProductCategory,
    StockLevel,
)

# Genetics Enums (CDES v1.2)
from .models import (
    BreedingTechnique,
    GeneticsStability,
    GeneticsConfidence,
    LineageRelationship,
)

# Validation
from .models import (
    ValidationError,
    ValidationResult,
)

# Concentration
from .models import Concentration

# Terpene Models
from .models import (
    TerpeneEntry,
    TerpeneProfile,
    FIXED_TERPENE_FIELDS,
)

# Cannabinoid Models
from .models import (
    CannabinoidEntry,
    CannabinoidProfile,
)

# Genetics Models (CDES v1.2)
from .models import (
    GeneticsSource,
    LineageNode,
    PhenotypeVariant,
    GeneticsProfile,
)

# Core Entity Models
from .models import (
    Strain,
    Batch,
    Product,
)

# Legacy/Library
from .models import (
    Effect,
    BoilingPoint,
    Terpene,
    TerpeneLibrary,
)

__all__ = [
    # Version
    "__version__",
    
    # Core Enums
    "StrainType",
    "ConcentrationUnit",
    "ProductCategory",
    "StockLevel",
    
    # Genetics Enums
    "BreedingTechnique",
    "GeneticsStability",
    "GeneticsConfidence",
    "LineageRelationship",
    
    # Validation
    "ValidationError",
    "ValidationResult",
    
    # Concentration
    "Concentration",
    
    # Terpene Models
    "TerpeneEntry",
    "TerpeneProfile",
    "FIXED_TERPENE_FIELDS",
    
    # Cannabinoid Models
    "CannabinoidEntry",
    "CannabinoidProfile",
    
    # Genetics Models
    "GeneticsSource",
    "LineageNode",
    "PhenotypeVariant",
    "GeneticsProfile",
    
    # Core Entities
    "Strain",
    "Batch",
    "Product",
    
    # Legacy/Library
    "Effect",
    "BoilingPoint",
    "Terpene",
    "TerpeneLibrary",
]
