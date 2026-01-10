'''CDES Name Normalizer - Converts raw names to CDES standard identifiers.'''

from typing import Tuple, Optional
from functools import lru_cache
from .models import StrainType

TERPENE_ALIASES = {
    "beta-myrcene": "terpene:myrcene", "b-myrcene": "terpene:myrcene", "myrcene": "terpene:myrcene",
    "alpha-pinene": "terpene:alpha-pinene", "a-pinene": "terpene:alpha-pinene", "pinene": "terpene:alpha-pinene",
    "beta-pinene": "terpene:beta-pinene", "b-pinene": "terpene:beta-pinene",
    "beta-caryophyllene": "terpene:beta-caryophyllene", "caryophyllene": "terpene:beta-caryophyllene",
    "d-limonene": "terpene:limonene", "limonene": "terpene:limonene",
    "alpha-humulene": "terpene:humulene", "humulene": "terpene:humulene",
    "linalool": "terpene:linalool", "terpinolene": "terpene:terpinolene",
    "ocimene": "terpene:ocimene", "bisabolol": "terpene:bisabolol",
    "alpha-bisabolol": "terpene:bisabolol", "geraniol": "terpene:geraniol",
    "eucalyptol": "terpene:eucalyptol", "1,8-cineole": "terpene:eucalyptol",
    "nerolidol": "terpene:nerolidol", "valencene": "terpene:valencene",
    "camphene": "terpene:camphene", "carene": "terpene:carene",
}

CANNABINOID_ALIASES = {
    "thc": "cannabinoid:thc", "delta-9-thc": "cannabinoid:thc", "d9-thc": "cannabinoid:thc",
    "thca": "cannabinoid:thca", "thc-a": "cannabinoid:thca",
    "cbd": "cannabinoid:cbd", "cbda": "cannabinoid:cbda", "cbd-a": "cannabinoid:cbda",
    "cbg": "cannabinoid:cbg", "cbga": "cannabinoid:cbga",
    "cbn": "cannabinoid:cbn", "cbc": "cannabinoid:cbc",
    "thcv": "cannabinoid:thcv", "cbdv": "cannabinoid:cbdv",
    "delta-8-thc": "cannabinoid:delta8-thc", "d8-thc": "cannabinoid:delta8-thc",
}

STRAIN_TYPE_ALIASES = {
    "indica": StrainType.INDICA, "ind": StrainType.INDICA, "i": StrainType.INDICA,
    "sativa": StrainType.SATIVA, "sat": StrainType.SATIVA, "s": StrainType.SATIVA,
    "hybrid": StrainType.HYBRID, "hyb": StrainType.HYBRID, "h": StrainType.HYBRID,
    "indica dominant": StrainType.HYBRID, "sativa dominant": StrainType.HYBRID,
    "balanced": StrainType.HYBRID, "50/50": StrainType.HYBRID,
    "cbd": StrainType.CBD, "cbd-dominant": StrainType.CBD, "high cbd": StrainType.CBD,
    "hemp": StrainType.CBD, "unknown": StrainType.UNKNOWN, "n/a": StrainType.UNKNOWN,
    "": StrainType.UNKNOWN, "none": StrainType.UNKNOWN,
}

@lru_cache(maxsize=1000)
def normalize_terpene_name(raw_name: str) -> Tuple[str, str]:
    '''Normalize terpene name to CDES ID and canonical name.'''
    if not raw_name:
        return ("terpene:unknown", "Unknown")
    clean = raw_name.strip().lower().replace("_", "-")
    clean = clean.replace("\u03b2", "beta").replace("\u03b1", "alpha")
    if clean in TERPENE_ALIASES:
        cdes_id = TERPENE_ALIASES[clean]
        canonical = cdes_id.split(":")[1].replace("-", " ").title()
        return (cdes_id, canonical)
    return (f"terpene:unknown:{clean}", raw_name.title())

@lru_cache(maxsize=500)
def normalize_cannabinoid_name(raw_name: str) -> Tuple[str, str]:
    '''Normalize cannabinoid name to CDES ID and canonical name.'''
    if not raw_name:
        return ("cannabinoid:unknown", "Unknown")
    clean = raw_name.strip().lower().replace("_", "-")
    if clean in CANNABINOID_ALIASES:
        cdes_id = CANNABINOID_ALIASES[clean]
        canonical = cdes_id.split(":")[1].upper()
        return (cdes_id, canonical)
    return (f"cannabinoid:unknown:{clean}", raw_name.upper())

def normalize_strain_type(raw_type: str) -> StrainType:
    '''Normalize strain type string to StrainType enum.'''
    if not raw_type:
        return StrainType.UNKNOWN
    clean = raw_type.strip().lower()
    return STRAIN_TYPE_ALIASES.get(clean, StrainType.UNKNOWN)

def is_known_terpene(cdes_id: str) -> bool:
    '''Check if a CDES ID is a known terpene.'''
    return cdes_id in set(TERPENE_ALIASES.values())

def is_known_cannabinoid(cdes_id: str) -> bool:
    '''Check if a CDES ID is a known cannabinoid.'''
    return cdes_id in set(CANNABINOID_ALIASES.values())
