'''Reference data access for CDES SDK with color support.

This module provides access to the canonical CDES reference data,
including terpene and cannabinoid definitions with standardized colors.
'''

import json
from pathlib import Path
from typing import Optional, Dict, Any, List
from urllib.request import urlopen
from dataclasses import dataclass

from .models import Terpene, TerpeneLibrary


# GitHub raw URLs for reference data
_GITHUB_RAW_BASE = "https://raw.githubusercontent.com/Acidni-LLC/cdes-reference-data/master"
_TERPENE_LIBRARY_URL = f"{_GITHUB_RAW_BASE}/terpenes/terpene-library.json"
_TERPENE_EXTENDED_URL = f"{_GITHUB_RAW_BASE}/terpenes/terpene-library-extended.json"
_TERPENE_COLORS_URL = f"{_GITHUB_RAW_BASE}/terpenes/terpene-colors.json"
_CANNABINOID_LIBRARY_URL = f"{_GITHUB_RAW_BASE}/cannabinoids/cannabinoid-library.json"

# Cache for reference data
_cached_library: Optional[TerpeneLibrary] = None
_cached_colors: Optional[Dict[str, Any]] = None
_cached_cannabinoids: Optional[Dict[str, Any]] = None


@dataclass
class ColorRef:
    '''Standard color reference with hex and RGB values.'''
    hex: str
    r: int
    g: int
    b: int
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ColorRef':
        rgb = data.get("rgb", {})
        return cls(
            hex=data.get("hex", "#000000"),
            r=rgb.get("r", 0),
            g=rgb.get("g", 0),
            b=rgb.get("b", 0)
        )
    
    def to_tuple(self) -> tuple:
        '''Return RGB as tuple for matplotlib, etc.'''
        return (self.r, self.g, self.b)
    
    def to_normalized(self) -> tuple:
        '''Return RGB as normalized 0-1 tuple.'''
        return (self.r / 255.0, self.g / 255.0, self.b / 255.0)


def _fetch_json(url: str) -> Dict[str, Any]:
    '''Fetch JSON data from URL.'''
    with urlopen(url) as response:
        return json.loads(response.read().decode())


def get_terpene_library(use_cache: bool = True) -> TerpeneLibrary:
    '''
    Get the complete CDES terpene library.

    Args:
        use_cache: If True, return cached data if available

    Returns:
        TerpeneLibrary containing all reference terpenes

    Example:
        >>> library = get_terpene_library()
        >>> len(library.terpenes)
        10
        >>> library.terpenes[0].name
        'Myrcene'
    '''
    global _cached_library

    if use_cache and _cached_library is not None:
        return _cached_library

    # Try to load from local file first (for bundled package)
    local_path = Path(__file__).parent / "data" / "terpene-library.json"
    if local_path.exists():
        with open(local_path) as f:
            data = json.load(f)
    else:
        # Fetch from GitHub
        data = _fetch_json(_TERPENE_LIBRARY_URL)

    _cached_library = TerpeneLibrary.from_dict(data)
    return _cached_library


def get_terpene_colors(use_cache: bool = True) -> Dict[str, ColorRef]:
    '''
    Get all terpene colors from reference data.
    
    Returns:
        Dict mapping terpene ID to ColorRef
        
    Example:
        >>> colors = get_terpene_colors()
        >>> colors["terpene:myrcene"].hex
        '#8B4513'
    '''
    global _cached_colors
    
    if use_cache and _cached_colors is not None:
        return _cached_colors
    
    data = _fetch_json(_TERPENE_COLORS_URL)
    _cached_colors = {
        t["id"]: ColorRef.from_dict(t["color"])
        for t in data.get("terpenes", [])
    }
    return _cached_colors


def get_terpene_color(name_or_id: str) -> Optional[ColorRef]:
    '''
    Get color for a specific terpene by name or ID.
    
    Args:
        name_or_id: Terpene name (e.g., "Myrcene") or ID (e.g., "terpene:myrcene")
        
    Returns:
        ColorRef if found, None otherwise
        
    Example:
        >>> color = get_terpene_color("myrcene")
        >>> color.hex
        '#8B4513'
        >>> color.to_tuple()
        (139, 69, 19)
    '''
    colors = get_terpene_colors()
    
    # Normalize search term
    normalized = name_or_id.lower().replace(" ", "-").replace("_", "-")
    
    # Try direct ID match
    if f"terpene:{normalized}" in colors:
        return colors[f"terpene:{normalized}"]
    
    # Try ID without prefix
    if name_or_id in colors:
        return colors[name_or_id]
    
    # Search by name (case-insensitive)
    for terp_id, color in colors.items():
        if terp_id.split(":")[-1].lower() == normalized:
            return color
    
    return None


def get_cannabinoid_library(use_cache: bool = True) -> Dict[str, Any]:
    '''
    Get all cannabinoids from reference data.
    
    Returns:
        Dict with cannabinoid data including colors
        
    Example:
        >>> cannabinoids = get_cannabinoid_library()
        >>> cannabinoids["cannabinoids"][0]["name"]
        'THC'
    '''
    global _cached_cannabinoids
    
    if use_cache and _cached_cannabinoids is not None:
        return _cached_cannabinoids
    
    _cached_cannabinoids = _fetch_json(_CANNABINOID_LIBRARY_URL)
    return _cached_cannabinoids


def get_cannabinoid_colors(use_cache: bool = True) -> Dict[str, ColorRef]:
    '''
    Get all cannabinoid colors from reference data.
    
    Returns:
        Dict mapping cannabinoid ID to ColorRef
        
    Example:
        >>> colors = get_cannabinoid_colors()
        >>> colors["cannabinoid:thc"].hex
        '#E63946'
    '''
    data = get_cannabinoid_library(use_cache)
    return {
        c["id"]: ColorRef.from_dict(c["color"])
        for c in data.get("cannabinoids", [])
    }


def get_cannabinoid_color(name_or_id: str) -> Optional[ColorRef]:
    '''
    Get color for a specific cannabinoid by name or ID.
    
    Args:
        name_or_id: Cannabinoid name (e.g., "THC", "CBD") or ID
        
    Returns:
        ColorRef if found, None otherwise
        
    Example:
        >>> color = get_cannabinoid_color("THC")
        >>> color.hex
        '#E63946'
        >>> color = get_cannabinoid_color("CBD")
        >>> color.hex
        '#2A9D8F'
    '''
    data = get_cannabinoid_library()
    normalized = name_or_id.lower().replace(" ", "").replace("-", "")
    
    for cannabinoid in data.get("cannabinoids", []):
        if cannabinoid["id"].lower() == name_or_id.lower():
            return ColorRef.from_dict(cannabinoid["color"])
        if cannabinoid["name"].lower() == normalized:
            return ColorRef.from_dict(cannabinoid["color"])
        if normalized in [alt.lower().replace("-", "").replace(" ", "") 
                         for alt in cannabinoid.get("alternateName", [])]:
            return ColorRef.from_dict(cannabinoid["color"])
    
    return None


def get_terpene_by_id(terpene_id: str) -> Optional[Terpene]:
    '''
    Get a specific terpene by its CDES ID.

    Args:
        terpene_id: The terpene ID (e.g., "terpene:myrcene")

    Returns:
        Terpene object if found, None otherwise
    '''
    library = get_terpene_library()
    return library.get_by_id(terpene_id)


def get_terpene_by_cas(cas_number: str) -> Optional[Terpene]:
    '''
    Get a specific terpene by its CAS registry number.

    Args:
        cas_number: The CAS number (e.g., "123-35-3")

    Returns:
        Terpene object if found, None otherwise
    '''
    library = get_terpene_library()
    return library.get_by_cas(cas_number)


def clear_cache() -> None:
    '''Clear all cached reference data.'''
    global _cached_library, _cached_colors, _cached_cannabinoids
    _cached_library = None
    _cached_colors = None
    _cached_cannabinoids = None
