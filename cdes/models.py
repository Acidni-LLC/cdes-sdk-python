"""Data models for CDES SDK."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ValidationError:
    """A single validation error."""
    path: str
    message: str
    value: Any = None


@dataclass
class ValidationResult:
    """Result of a validation operation."""
    valid: bool
    errors: list[ValidationError] = field(default_factory=list)
    
    def __bool__(self) -> bool:
        return self.valid


@dataclass
class Effect:
    """A terpene effect with evidence level."""
    effect: str
    strength: str  # "strong", "moderate", "weak"
    evidence: str  # "high", "moderate", "emerging"


@dataclass
class BoilingPoint:
    """Boiling point in multiple units."""
    celsius: float
    fahrenheit: float


@dataclass
class Terpene:
    """A cannabis terpene with all properties."""
    id: str
    name: str
    casNumber: str
    pubchemId: int
    molecularFormula: str
    category: str  # "monoterpene" or "sesquiterpene"
    aroma: list[str]
    effects: list[Effect]
    boilingPoint: BoilingPoint | None = None
    notes: str | None = None
    
    @classmethod
    def from_dict(cls, data: dict) -> "Terpene":
        """Create a Terpene from a dictionary."""
        effects = [Effect(**e) for e in data.get("effects", [])]
        bp = data.get("boilingPoint")
        boiling_point = BoilingPoint(**bp) if bp else None
        
        return cls(
            id=data["id"],
            name=data["name"],
            casNumber=data["casNumber"],
            pubchemId=data["pubchemId"],
            molecularFormula=data["molecularFormula"],
            category=data["category"],
            aroma=data.get("aroma", []),
            effects=effects,
            boilingPoint=boiling_point,
            notes=data.get("notes"),
        )


@dataclass
class TerpeneLibrary:
    """The complete CDES terpene library."""
    version: str
    lastUpdated: str
    license: str
    terpenes: list[Terpene]
    
    @classmethod
    def from_dict(cls, data: dict) -> "TerpeneLibrary":
        """Create a TerpeneLibrary from a dictionary."""
        terpenes = [Terpene.from_dict(t) for t in data.get("terpenes", [])]
        return cls(
            version=data["version"],
            lastUpdated=data["lastUpdated"],
            license=data["license"],
            terpenes=terpenes,
        )
    
    def get_by_id(self, terpene_id: str) -> Terpene | None:
        """Get a terpene by its ID."""
        for t in self.terpenes:
            if t.id == terpene_id:
                return t
        return None
    
    def get_by_cas(self, cas_number: str) -> Terpene | None:
        """Get a terpene by its CAS number."""
        for t in self.terpenes:
            if t.casNumber == cas_number:
                return t
        return None
