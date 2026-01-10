'''
CDES - Cannabis Data Exchange Standard Python SDK

A Python library for working with cannabis data that conforms to the CDES v1.0 specification.

Usage:
    from cdes import Strain, StrainType, TerpeneProfile, ProductCategory
    from cdes import normalize_terpene_name, normalize_strain_type
    from cdes import validate_strain, validate_terpene_profile
'''

__version__ = "1.0.0"

# Core models
from .models import (
    StrainType,
    ConcentrationUnit,
    ProductCategory,
    StockLevel,
    ValidationError,
    ValidationResult,
    Concentration,
    TerpeneEntry,
    TerpeneProfile,
    CannabinoidEntry,
    CannabinoidProfile,
    Strain,
    Batch,
    Product,
    FIXED_TERPENE_FIELDS,
    # Legacy compatibility
    Effect,
    BoilingPoint,
    Terpene,
    TerpeneLibrary,
)

# Normalizers
from .normalizer import (
    normalize_terpene_name,
    normalize_cannabinoid_name,
    normalize_strain_type,
    is_known_terpene,
    is_known_cannabinoid,
    TERPENE_ALIASES,
    CANNABINOID_ALIASES,
)

# Validators
from .validators import (
    validate_strain,
    validate_coa,
    validate_terpene_profile,
    validate_cannabinoid_profile,
)

# Reference data
from .reference import get_terpene_library, get_terpene_by_id

# Telemetry (opt-in tracking)
from .telemetry import (
    track_event,
    disable_telemetry,
    enable_telemetry,
)

__all__ = [
    # Version
    "__version__",
    # Enums
    "StrainType",
    "ConcentrationUnit", 
    "ProductCategory",
    "StockLevel",
    # Models
    "ValidationError",
    "ValidationResult",
    "Concentration",
    "TerpeneEntry",
    "TerpeneProfile",
    "CannabinoidEntry",
    "CannabinoidProfile",
    "Strain",
    "Batch",
    "Product",
    "FIXED_TERPENE_FIELDS",
    # Legacy
    "Effect",
    "BoilingPoint",
    "Terpene",
    "TerpeneLibrary",
    # Normalizers
    "normalize_terpene_name",
    "normalize_cannabinoid_name",
    "normalize_strain_type",
    "is_known_terpene",
    "is_known_cannabinoid",
    "TERPENE_ALIASES",
    "CANNABINOID_ALIASES",
    # Validators
    "validate_strain",
    "validate_coa",
    "validate_terpene_profile",
    "validate_cannabinoid_profile",
    # Reference
    "get_terpene_library",
    "get_terpene_by_id",
    # Telemetry
    "track_event",
    "disable_telemetry",
    "enable_telemetry",
]
