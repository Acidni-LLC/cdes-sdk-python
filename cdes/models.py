"""
CDES Data Models - Cannabis Data Exchange Standard Python SDK

Dataclass models conforming to CDES JSON Schema specifications.
Aligned with CDES v1.0 specification.

Version: 1.0.0
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import date
from enum import Enum


class StrainType(str, Enum):
    """Cannabis strain types (CDES v1.0)."""
    INDICA = "indica"
    SATIVA = "sativa"
    HYBRID = "hybrid"
    CBD = "cbd"
    UNKNOWN = "unknown"


class ConcentrationUnit(str, Enum):
    """Units for concentration measurements (CDES v1.0)."""
    PERCENT = "percent"
    MG_G = "mg_g"
    PPM = "ppm"


class ProductCategory(str, Enum):
    """Cannabis product categories (CDES v1.0)."""
    FLOWER = "flower"
    CONCENTRATE = "concentrate"
    EDIBLE = "edible"
    VAPE = "vape"
    TOPICAL = "topical"
    TINCTURE = "tincture"
    CAPSULE = "capsule"
    PRE_ROLL = "pre_roll"
    RSO = "rso"
    OTHER = "other"


class StockLevel(str, Enum):
    """Inventory stock level indicator (CDES v1.0)."""
    IN_STOCK = "in_stock"
    LOW_STOCK = "low_stock"
    OUT_OF_STOCK = "out_of_stock"


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
    errors: List[ValidationError] = field(default_factory=list)
    
    def __bool__(self) -> bool:
        return self.valid


@dataclass
class Concentration:
    """A concentration measurement with unit (CDES v1.0)."""
    value: float
    unit: ConcentrationUnit = ConcentrationUnit.PERCENT
    
    def to_percent(self) -> float:
        """Convert to percentage."""
        if self.unit == ConcentrationUnit.PERCENT:
            return self.value
        elif self.unit == ConcentrationUnit.MG_G:
            return self.value / 10
        elif self.unit == ConcentrationUnit.PPM:
            return self.value / 10000
        return self.value
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to CDES-compliant dictionary."""
        return {"value": self.value, "unit": self.unit.value}


@dataclass
class TerpeneEntry:
    """A single terpene measurement (CDES v1.0)."""
    name: str
    value: float
    unit: ConcentrationUnit = ConcentrationUnit.PERCENT
    cdes_id: Optional[str] = None
    cas_number: Optional[str] = None
    lod: Optional[float] = None
    loq: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        result = {"name": self.name, "value": self.value, "unit": self.unit.value}
        if self.cdes_id:
            result["cdesId"] = self.cdes_id
        if self.cas_number:
            result["casNumber"] = self.cas_number
        if self.lod is not None:
            result["lod"] = self.lod
        if self.loq is not None:
            result["loq"] = self.loq
        return result


# Fixed terpene field names for TerpeneProfile
FIXED_TERPENE_FIELDS = [
    "myrcene", "limonene", "caryophyllene", "pinene", "linalool",
    "humulene", "terpinolene", "ocimene", "bisabolol"
]


@dataclass
class TerpeneProfile:
    """CDES-compliant terpene profile (CDES v1.0)."""
    myrcene: float = 0.0
    limonene: float = 0.0
    caryophyllene: float = 0.0
    pinene: float = 0.0
    linalool: float = 0.0
    humulene: float = 0.0
    terpinolene: float = 0.0
    ocimene: float = 0.0
    bisabolol: float = 0.0
    terpenes: List[TerpeneEntry] = field(default_factory=list)
    total: Optional[float] = None
    dominant_terpene: Optional[str] = None
    
    def to_vector(self) -> List[float]:
        """Convert to 9-element vector for ML/similarity."""
        return [
            self.myrcene, self.limonene, self.caryophyllene,
            self.pinene, self.linalool, self.humulene,
            self.terpinolene, self.ocimene, self.bisabolol
        ]
    
    def calculate_similarity(self, other: "TerpeneProfile") -> float:
        """Calculate cosine similarity with another profile."""
        import math
        v1, v2 = self.to_vector(), other.to_vector()
        dot = sum(a * b for a, b in zip(v1, v2))
        m1 = math.sqrt(sum(a * a for a in v1))
        m2 = math.sqrt(sum(b * b for b in v2))
        return dot / (m1 * m2) if m1 and m2 else 0.0
    
    def get_total(self) -> float:
        """Calculate total terpene percentage."""
        if self.total is not None:
            return self.total
        return sum(self.to_vector())
    
    def get_dominant(self) -> Optional[str]:
        """Get dominant terpene name."""
        if self.dominant_terpene:
            return self.dominant_terpene
        vals = list(zip(FIXED_TERPENE_FIELDS, self.to_vector()))
        if not vals or max(v for _, v in vals) == 0:
            return None
        return max(vals, key=lambda x: x[1])[0]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "myrcene": self.myrcene, "limonene": self.limonene,
            "caryophyllene": self.caryophyllene, "pinene": self.pinene,
            "linalool": self.linalool, "humulene": self.humulene,
            "terpinolene": self.terpinolene, "ocimene": self.ocimene,
            "bisabolol": self.bisabolol, "total": self.get_total(),
            "dominantTerpene": self.get_dominant(),
            "terpenes": [t.to_dict() for t in self.terpenes]
        }


@dataclass
class CannabinoidEntry:
    """A single cannabinoid measurement (CDES v1.0)."""
    name: str
    value: float
    unit: ConcentrationUnit = ConcentrationUnit.PERCENT
    cdes_id: Optional[str] = None
    lod: Optional[float] = None
    loq: Optional[float] = None
    is_below_loq: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        result = {"name": self.name, "value": self.value, "unit": self.unit.value}
        if self.cdes_id:
            result["cdesId"] = self.cdes_id
        if self.lod is not None:
            result["lod"] = self.lod
        if self.loq is not None:
            result["loq"] = self.loq
        if self.is_below_loq:
            result["isBelowLoq"] = self.is_below_loq
        return result


@dataclass
class CannabinoidProfile:
    """CDES-compliant cannabinoid profile (CDES v1.0)."""
    thc: float = 0.0
    thca: float = 0.0
    cbd: float = 0.0
    cbda: float = 0.0
    cbg: float = 0.0
    cbn: float = 0.0
    cbc: float = 0.0
    thcv: float = 0.0
    cannabinoids: List[CannabinoidEntry] = field(default_factory=list)
    total: Optional[float] = None
    
    def get_total(self) -> float:
        if self.total is not None:
            return self.total
        return self.thc + self.thca + self.cbd + self.cbda + self.cbg + self.cbn + self.cbc + self.thcv
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "thc": self.thc, "thca": self.thca, "cbd": self.cbd, "cbda": self.cbda,
            "cbg": self.cbg, "cbn": self.cbn, "cbc": self.cbc, "thcv": self.thcv,
            "total": self.get_total(),
            "cannabinoids": [c.to_dict() for c in self.cannabinoids]
        }


@dataclass
class Strain:
    """A cannabis strain (CDES v1.0)."""
    name: str
    type: StrainType = StrainType.UNKNOWN
    id: Optional[str] = None
    display_name: Optional[str] = None
    genetics: Optional[str] = None
    breeder: Optional[str] = None
    description: Optional[str] = None
    effects: List[str] = field(default_factory=list)
    flavors: List[str] = field(default_factory=list)
    aromas: List[str] = field(default_factory=list)
    aliases: List[str] = field(default_factory=list)
    typical_thc_min: Optional[float] = None
    typical_thc_max: Optional[float] = None
    typical_cbd_min: Optional[float] = None
    typical_cbd_max: Optional[float] = None
    typical_terpene_profile: Optional[TerpeneProfile] = None
    
    def to_dict(self) -> Dict[str, Any]:
        result = {"name": self.name, "type": self.type.value}
        if self.id:
            result["id"] = self.id
        if self.display_name:
            result["displayName"] = self.display_name
        if self.genetics:
            result["genetics"] = self.genetics
        if self.description:
            result["description"] = self.description
        if self.effects:
            result["effects"] = self.effects
        if self.flavors:
            result["flavors"] = self.flavors
        if self.aromas:
            result["aromas"] = self.aromas
        if self.aliases:
            result["aliases"] = self.aliases
        if self.typical_terpene_profile:
            result["typicalTerpeneProfile"] = self.typical_terpene_profile.to_dict()
        return result


@dataclass
class Batch:
    """A cannabis batch with lab results (CDES v1.0)."""
    id: str
    batch_number: str
    strain_name: Optional[str] = None
    strain_id: Optional[str] = None
    harvest_date: Optional[date] = None
    package_date: Optional[date] = None
    thc_percentage: Optional[float] = None
    cbd_percentage: Optional[float] = None
    total_cannabinoids: Optional[float] = None
    total_terpenes: Optional[float] = None
    terpene_profile: Optional[TerpeneProfile] = None
    cannabinoid_profile: Optional[CannabinoidProfile] = None
    producer: Optional[str] = None
    license_number: Optional[str] = None
    lab_name: Optional[str] = None
    analysis_date: Optional[date] = None
    coa_url: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        result = {"id": self.id, "batchNumber": self.batch_number}
        if self.strain_name:
            result["strainName"] = self.strain_name
        if self.thc_percentage is not None:
            result["thcPercentage"] = self.thc_percentage
        if self.cbd_percentage is not None:
            result["cbdPercentage"] = self.cbd_percentage
        if self.terpene_profile:
            result["terpeneProfile"] = self.terpene_profile.to_dict()
        if self.cannabinoid_profile:
            result["cannabinoidProfile"] = self.cannabinoid_profile.to_dict()
        if self.harvest_date:
            result["harvestDate"] = self.harvest_date.isoformat()
        if self.lab_name:
            result["labName"] = self.lab_name
        if self.analysis_date:
            result["analysisDate"] = self.analysis_date.isoformat()
        return result


@dataclass
class Product:
    """A cannabis product (CDES v1.0)."""
    id: str
    name: str
    category: ProductCategory
    sku: Optional[str] = None
    brand: Optional[str] = None
    subcategory: Optional[str] = None
    strain_name: Optional[str] = None
    strain_id: Optional[str] = None
    batch_number: Optional[str] = None
    batch_id: Optional[str] = None
    thc_percentage: Optional[float] = None
    cbd_percentage: Optional[float] = None
    thc_mg: Optional[float] = None
    cbd_mg: Optional[float] = None
    weight_grams: Optional[float] = None
    servings: Optional[int] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    terpene_profile: Optional[TerpeneProfile] = None
    
    def to_dict(self) -> Dict[str, Any]:
        result = {"id": self.id, "name": self.name, "category": self.category.value}
        if self.sku:
            result["sku"] = self.sku
        if self.brand:
            result["brand"] = self.brand
        if self.strain_name:
            result["strainName"] = self.strain_name
        if self.thc_percentage is not None:
            result["thcPercentage"] = self.thc_percentage
        if self.cbd_percentage is not None:
            result["cbdPercentage"] = self.cbd_percentage
        if self.weight_grams is not None:
            result["weightGrams"] = self.weight_grams
        if self.terpene_profile:
            result["terpeneProfile"] = self.terpene_profile.to_dict()
        return result


# Legacy compatibility exports
@dataclass
class Effect:
    """A terpene effect with evidence level."""
    effect: str
    strength: str
    evidence: str


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
    category: str
    aroma: List[str]
    effects: List[Effect]
    boilingPoint: Optional[BoilingPoint] = None
    notes: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Terpene":
        effects = [Effect(**e) for e in data.get("effects", [])]
        bp = data.get("boilingPoint")
        boiling_point = BoilingPoint(**bp) if bp else None
        return cls(
            id=data["id"], name=data["name"], casNumber=data["casNumber"],
            pubchemId=data["pubchemId"], molecularFormula=data["molecularFormula"],
            category=data["category"], aroma=data.get("aroma", []),
            effects=effects, boilingPoint=boiling_point, notes=data.get("notes"),
        )


@dataclass
class TerpeneLibrary:
    """The complete CDES terpene library."""
    version: str
    lastUpdated: str
    license: str
    terpenes: List[Terpene]

    @classmethod
    def from_dict(cls, data: dict) -> "TerpeneLibrary":
        terpenes = [Terpene.from_dict(t) for t in data.get("terpenes", [])]
        return cls(
            version=data["version"], lastUpdated=data["lastUpdated"],
            license=data["license"], terpenes=terpenes,
        )

    def get_by_id(self, terpene_id: str) -> Optional[Terpene]:
        for t in self.terpenes:
            if t.id == terpene_id:
                return t
        return None
