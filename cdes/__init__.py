"""
CDES - Cannabis Data Exchange Standard Python SDK

A Python library for validating and working with cannabis data
that conforms to the CDES specification.
"""

from .validators import (
    validate_strain,
    validate_coa,
    validate_terpene_profile,
    validate_cannabinoid_profile,
)
from .reference import get_terpene_library, get_terpene_by_id
from .models import ValidationResult, Terpene, TerpeneLibrary

__version__ = "0.1.0"
__all__ = [
    "validate_strain",
    "validate_coa", 
    "validate_terpene_profile",
    "validate_cannabinoid_profile",
    "get_terpene_library",
    "get_terpene_by_id",
    "ValidationResult",
    "Terpene",
    "TerpeneLibrary",
]
