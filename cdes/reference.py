"""Reference data access for CDES SDK."""

import json
from pathlib import Path
from typing import Optional
from urllib.request import urlopen

from .models import Terpene, TerpeneLibrary


_TERPENE_LIBRARY_URL = "https://raw.githubusercontent.com/Acidni-LLC/cdes-reference-data/main/terpenes/terpene-library.json"
_cached_library: Optional[TerpeneLibrary] = None


def get_terpene_library(use_cache: bool = True) -> TerpeneLibrary:
    """
    Get the complete CDES terpene library.
    
    Args:
        use_cache: If True, return cached data if available
        
    Returns:
        TerpeneLibrary containing all reference terpenes
        
    Example:
        >>> library = get_terpene_library()
        >>> len(library.terpenes)
        24
        >>> library.terpenes[0].name
        'Myrcene'
    """
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
        with urlopen(_TERPENE_LIBRARY_URL) as response:
            data = json.loads(response.read().decode())
    
    _cached_library = TerpeneLibrary.from_dict(data)
    return _cached_library


def get_terpene_by_id(terpene_id: str) -> Optional[Terpene]:
    """
    Get a specific terpene by its CDES ID.
    
    Args:
        terpene_id: The terpene ID (e.g., "terp-myrcene")
        
    Returns:
        Terpene object if found, None otherwise
        
    Example:
        >>> myrcene = get_terpene_by_id("terp-myrcene")
        >>> myrcene.casNumber
        '123-35-3'
    """
    library = get_terpene_library()
    return library.get_by_id(terpene_id)


def get_terpene_by_cas(cas_number: str) -> Optional[Terpene]:
    """
    Get a specific terpene by its CAS registry number.
    
    Args:
        cas_number: The CAS number (e.g., "123-35-3")
        
    Returns:
        Terpene object if found, None otherwise
        
    Example:
        >>> terpene = get_terpene_by_cas("123-35-3")
        >>> terpene.name
        'Myrcene'
    """
    library = get_terpene_library()
    return library.get_by_cas(cas_number)
