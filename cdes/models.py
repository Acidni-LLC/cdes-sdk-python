"""
CDES Data Models - Cannabis Data Exchange Standard Python SDK

Dataclass models conforming to CDES JSON Schema specifications.
Aligned with CDES v1.2 specification.

Version: 1.2.0

Changelog v1.2.0:
- Added comprehensive Genetics domain (GeneticsProfile, LineageNode, GeneticsSource)
- Added BreedingTechnique, GeneticsStability enums
- Added PhenotypeVariant for phenotype tracking
- Updated Strain to support structured genetics_profile
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from enum import Enum


# =============================================================================
# ENUMERATIONS
# =============================================================================

class StrainType(str, Enum):
    """Cannabis strain types (CDES v1.0)."""
    INDICA = "indica"
    SATIVA = "sativa"
    HYBRID = "hybrid"
    HYBRID_INDICA = "hybrid_indica"
    HYBRID_SATIVA = "hybrid_sativa"
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


class BreedingTechnique(str, Enum):
    """Cannabis breeding technique used to create a strain (CDES v1.2)."""
    CROSS = "cross"                    # Standard cross (A  B)
    BACKCROSS = "backcross"            # Cross with parent to reinforce traits (BX)
    SELFING = "selfing"                # Self-pollination (S1, S2, etc.)
    LANDRACE = "landrace"              # Original wild strain
    POLYHYBRID = "polyhybrid"          # Complex multi-generation hybrid
    F1 = "f1"                          # First filial generation
    F2 = "f2"                          # Second filial generation
    F3 = "f3"                          # Third filial generation
    F4 = "f4"                          # Fourth filial generation
    F5_PLUS = "f5_plus"                # Fifth generation or beyond
    S1 = "s1"                          # First selfed generation
    S2 = "s2"                          # Second selfed generation
    BX1 = "bx1"                        # First backcross
    BX2 = "bx2"                        # Second backcross
    BX3 = "bx3"                        # Third backcross
    CLONE = "clone"                    # Vegetative propagation
    TISSUE_CULTURE = "tissue_culture"  # Laboratory propagation
    UNKNOWN = "unknown"


class GeneticsStability(str, Enum):
    """Stability level of strain genetics (CDES v1.2)."""
    UNSTABLE = "unstable"          # High phenotype variation
    SEMI_STABLE = "semi_stable"    # Some variation
    STABLE = "stable"              # Consistent expression
    IBL = "ibl"                    # Inbred line, highly stabilized
    LANDRACE = "landrace"          # Natural landrace
    CLONE_ONLY = "clone_only"      # Only available as clone
    UNKNOWN = "unknown"


class GeneticsConfidence(str, Enum):
    """Confidence level for genetics data (CDES v1.2)."""
    VERIFIED = "verified"          # Verified by breeder/lab
    HIGH = "high"                  # High confidence from reliable source
    MEDIUM = "medium"              # Moderate confidence
    LOW = "low"                    # Unconfirmed/community reported
    DISPUTED = "disputed"          # Multiple conflicting claims
    UNKNOWN = "unknown"


class LineageRelationship(str, Enum):
    """Relationship type in lineage (CDES v1.2)."""
    PARENT = "parent"              # Direct parent (mother or father)
    MOTHER = "mother"              # Specifically female parent
    FATHER = "father"              # Specifically male/pollen donor
    GRANDPARENT = "grandparent"    # Second generation ancestor
    GREAT_GRANDPARENT = "great_grandparent"
    ANCESTOR = "ancestor"          # Distant ancestor
    SIBLING = "sibling"            # Same parents
    CHILD = "child"                # Direct offspring
    UNKNOWN = "unknown"


# =============================================================================
# VALIDATION MODELS
# =============================================================================

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


# =============================================================================
# CONCENTRATION MODELS
# =============================================================================

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


# =============================================================================
# TERPENE MODELS
# =============================================================================

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


# =============================================================================
# CANNABINOID MODELS
# =============================================================================

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


# =============================================================================
# GENETICS MODELS (CDES v1.2)
# =============================================================================

@dataclass
class GeneticsSource:
    """
    Provenance tracking for genetics data (CDES v1.2).
    
    Enables tracking where genetics information came from and how reliable it is.
    Supports multiple sources with different confidence levels for the same strain.
    """
    source_name: str                                    # e.g., "SeedFinder", "Leafly", "Breeder Direct"
    source_type: str = "database"                       # database, breeder, lab, community, registry
    source_url: Optional[str] = None                    # URL to the source
    source_id: Optional[str] = None                     # ID in the source system
    confidence: GeneticsConfidence = GeneticsConfidence.MEDIUM
    retrieved_at: Optional[datetime] = None
    verified_by: Optional[str] = None                   # Who verified this data
    verification_date: Optional[date] = None
    notes: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "sourceName": self.source_name,
            "sourceType": self.source_type,
            "confidence": self.confidence.value,
        }
        if self.source_url:
            result["sourceUrl"] = self.source_url
        if self.source_id:
            result["sourceId"] = self.source_id
        if self.retrieved_at:
            result["retrievedAt"] = self.retrieved_at.isoformat()
        if self.verified_by:
            result["verifiedBy"] = self.verified_by
        if self.verification_date:
            result["verificationDate"] = self.verification_date.isoformat()
        if self.notes:
            result["notes"] = self.notes
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GeneticsSource":
        return cls(
            source_name=data["sourceName"],
            source_type=data.get("sourceType", "database"),
            source_url=data.get("sourceUrl"),
            source_id=data.get("sourceId"),
            confidence=GeneticsConfidence(data.get("confidence", "medium")),
            retrieved_at=datetime.fromisoformat(data["retrievedAt"]) if data.get("retrievedAt") else None,
            verified_by=data.get("verifiedBy"),
            verification_date=date.fromisoformat(data["verificationDate"]) if data.get("verificationDate") else None,
            notes=data.get("notes"),
        )


@dataclass
class LineageNode:
    """
    A node in the strain lineage tree (CDES v1.2).
    
    Represents a single ancestor in the lineage with relationship details.
    Supports recursive lineage trees for complex breeding histories.
    """
    strain_name: str
    strain_id: Optional[str] = None                     # CDES strain ID if known
    relationship: LineageRelationship = LineageRelationship.PARENT
    generation: int = 1                                 # 1 = parent, 2 = grandparent, etc.
    contribution_pct: Optional[float] = None            # Genetic contribution percentage
    strain_type: Optional[StrainType] = None
    breeder: Optional[str] = None
    is_verified: bool = False
    children: List["LineageNode"] = field(default_factory=list)  # Sub-lineage
    source: Optional[GeneticsSource] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "strainName": self.strain_name,
            "relationship": self.relationship.value,
            "generation": self.generation,
            "isVerified": self.is_verified,
        }
        if self.strain_id:
            result["strainId"] = self.strain_id
        if self.contribution_pct is not None:
            result["contributionPct"] = self.contribution_pct
        if self.strain_type:
            result["strainType"] = self.strain_type.value
        if self.breeder:
            result["breeder"] = self.breeder
        if self.children:
            result["children"] = [c.to_dict() for c in self.children]
        if self.source:
            result["source"] = self.source.to_dict()
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LineageNode":
        return cls(
            strain_name=data["strainName"],
            strain_id=data.get("strainId"),
            relationship=LineageRelationship(data.get("relationship", "parent")),
            generation=data.get("generation", 1),
            contribution_pct=data.get("contributionPct"),
            strain_type=StrainType(data["strainType"]) if data.get("strainType") else None,
            breeder=data.get("breeder"),
            is_verified=data.get("isVerified", False),
            children=[cls.from_dict(c) for c in data.get("children", [])],
            source=GeneticsSource.from_dict(data["source"]) if data.get("source") else None,
        )


@dataclass
class PhenotypeVariant:
    """
    A phenotype expression variant of a strain (CDES v1.2).
    
    Different phenotypes (phenos) of the same strain can have different
    characteristics. This tracks specific phenotype variants.
    """
    phenotype_name: str                                 # e.g., "GDP #4", "Blue Dream Cut"
    phenotype_number: Optional[int] = None              # e.g., 4 for "#4"
    discovered_by: Optional[str] = None                 # Who discovered/selected this pheno
    discovery_year: Optional[int] = None
    
    # Characteristics that differ from parent strain
    strain_type_override: Optional[StrainType] = None   # May lean more indica/sativa
    indica_pct: Optional[int] = None
    sativa_pct: Optional[int] = None
    
    # Distinguishing features
    distinguishing_traits: List[str] = field(default_factory=list)
    typical_thc_min: Optional[float] = None
    typical_thc_max: Optional[float] = None
    typical_cbd_min: Optional[float] = None
    typical_cbd_max: Optional[float] = None
    typical_terpene_profile: Optional[TerpeneProfile] = None
    
    # Cultivation info
    flowering_days_min: Optional[int] = None
    flowering_days_max: Optional[int] = None
    yield_indoor_g_m2: Optional[float] = None
    yield_outdoor_g_plant: Optional[float] = None
    
    notes: Optional[str] = None
    is_clone_only: bool = False

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "phenotypeName": self.phenotype_name,
            "isCloneOnly": self.is_clone_only,
        }
        if self.phenotype_number is not None:
            result["phenotypeNumber"] = self.phenotype_number
        if self.discovered_by:
            result["discoveredBy"] = self.discovered_by
        if self.discovery_year:
            result["discoveryYear"] = self.discovery_year
        if self.strain_type_override:
            result["strainTypeOverride"] = self.strain_type_override.value
        if self.indica_pct is not None:
            result["indicaPct"] = self.indica_pct
        if self.sativa_pct is not None:
            result["sativaPct"] = self.sativa_pct
        if self.distinguishing_traits:
            result["distinguishingTraits"] = self.distinguishing_traits
        if self.typical_thc_min is not None:
            result["typicalThcMin"] = self.typical_thc_min
        if self.typical_thc_max is not None:
            result["typicalThcMax"] = self.typical_thc_max
        if self.typical_terpene_profile:
            result["typicalTerpeneProfile"] = self.typical_terpene_profile.to_dict()
        if self.flowering_days_min is not None:
            result["floweringDaysMin"] = self.flowering_days_min
        if self.flowering_days_max is not None:
            result["floweringDaysMax"] = self.flowering_days_max
        if self.notes:
            result["notes"] = self.notes
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PhenotypeVariant":
        return cls(
            phenotype_name=data["phenotypeName"],
            phenotype_number=data.get("phenotypeNumber"),
            discovered_by=data.get("discoveredBy"),
            discovery_year=data.get("discoveryYear"),
            strain_type_override=StrainType(data["strainTypeOverride"]) if data.get("strainTypeOverride") else None,
            indica_pct=data.get("indicaPct"),
            sativa_pct=data.get("sativaPct"),
            distinguishing_traits=data.get("distinguishingTraits", []),
            typical_thc_min=data.get("typicalThcMin"),
            typical_thc_max=data.get("typicalThcMax"),
            typical_cbd_min=data.get("typicalCbdMin"),
            typical_cbd_max=data.get("typicalCbdMax"),
            typical_terpene_profile=TerpeneProfile(**data["typicalTerpeneProfile"]) if data.get("typicalTerpeneProfile") else None,
            flowering_days_min=data.get("floweringDaysMin"),
            flowering_days_max=data.get("floweringDaysMax"),
            yield_indoor_g_m2=data.get("yieldIndoorGM2"),
            yield_outdoor_g_plant=data.get("yieldOutdoorGPlant"),
            notes=data.get("notes"),
            is_clone_only=data.get("isCloneOnly", False),
        )


@dataclass
class GeneticsProfile:
    """
    Comprehensive cannabis genetics profile (CDES v1.2).
    
    A first-class CDES entity that captures complete genetics information
    for a strain. Designed to be interoperable across seed banks, dispensaries,
    growers, and researchers.
    
    Features:
    - Multi-parent lineage support (not just 2 parents)
    - Full lineage tree with unlimited depth
    - Multiple data sources with provenance tracking
    - Phenotype variant support
    - Breeding technique and generation tracking
    - Genetic stability classification
    - Awards and recognition tracking
    - Extensible metadata
    
    Example:
        profile = GeneticsProfile(
            parent_1="OG Kush",
            parent_2="Durban Poison",
            breeder="DNA Genetics",
            breeding_technique=BreedingTechnique.F1,
            stability=GeneticsStability.STABLE,
            indica_pct=60,
            sativa_pct=40,
        )
    """
    # Primary parents (simple case)
    parent_1: Optional[str] = None
    parent_2: Optional[str] = None
    
    # Breeder / Origin
    breeder: Optional[str] = None
    breeder_url: Optional[str] = None
    original_breeder: Optional[str] = None              # If different from current
    origin_year: Optional[int] = None
    origin_location: Optional[str] = None               # Geographic origin for landraces
    
    # Classification
    indica_pct: Optional[int] = None                    # 0-100
    sativa_pct: Optional[int] = None                    # 0-100
    ruderalis_pct: Optional[int] = None                 # 0-100 (for autoflower genetics)
    
    # Breeding details
    breeding_technique: BreedingTechnique = BreedingTechnique.UNKNOWN
    generation: Optional[str] = None                    # e.g., "F1", "S1", "BX2"
    stability: GeneticsStability = GeneticsStability.UNKNOWN
    is_feminized: Optional[bool] = None
    is_autoflower: Optional[bool] = None
    is_clone_only: bool = False
    
    # Full lineage tree (for complex genetics)
    lineage: List[LineageNode] = field(default_factory=list)
    lineage_text: Optional[str] = None                  # Human-readable, e.g., "OG Kush  Durban Poison"
    
    # Additional parents (for polyhybrids)
    additional_parents: List[str] = field(default_factory=list)
    
    # Phenotype variants
    phenotypes: List[PhenotypeVariant] = field(default_factory=list)
    selected_phenotype: Optional[str] = None            # Currently selected pheno name
    
    # Data provenance
    sources: List[GeneticsSource] = field(default_factory=list)
    primary_source: Optional[str] = None                # Primary source name
    confidence: GeneticsConfidence = GeneticsConfidence.UNKNOWN
    last_verified: Optional[date] = None
    
    # Recognition
    awards: List[str] = field(default_factory=list)     # e.g., ["Cannabis Cup 2015"]
    cup_wins: List[Dict[str, Any]] = field(default_factory=list)  # Detailed cup info
    
    # Genetic markers (for advanced use)
    genetic_markers: Dict[str, Any] = field(default_factory=dict)
    chemotype: Optional[str] = None                     # e.g., "Type I", "Type II", "Type III"
    
    # Extensible metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)

    def get_parent_string(self) -> Optional[str]:
        """Get simple parent string like 'OG Kush  Durban Poison'."""
        if self.lineage_text:
            return self.lineage_text
        parents = []
        if self.parent_1:
            parents.append(self.parent_1)
        if self.parent_2:
            parents.append(self.parent_2)
        parents.extend(self.additional_parents)
        if not parents:
            return None
        return "  ".join(parents)

    def get_all_parents(self) -> List[str]:
        """Get list of all parent strain names."""
        parents = []
        if self.parent_1:
            parents.append(self.parent_1)
        if self.parent_2:
            parents.append(self.parent_2)
        parents.extend(self.additional_parents)
        return parents

    def get_lineage_depth(self) -> int:
        """Get the maximum depth of the lineage tree."""
        if not self.lineage:
            return 1 if self.parent_1 or self.parent_2 else 0
        
        def _depth(node: LineageNode) -> int:
            if not node.children:
                return 1
            return 1 + max(_depth(c) for c in node.children)
        
        return max(_depth(n) for n in self.lineage)

    def add_source(self, source: GeneticsSource) -> None:
        """Add a data source with de-duplication."""
        existing = [s for s in self.sources if s.source_name == source.source_name]
        if not existing:
            self.sources.append(source)
        else:
            # Update existing if newer
            idx = self.sources.index(existing[0])
            if source.retrieved_at and (not existing[0].retrieved_at or 
                                        source.retrieved_at > existing[0].retrieved_at):
                self.sources[idx] = source

    def to_dict(self) -> Dict[str, Any]:
        """Convert to CDES-compliant dictionary."""
        result: Dict[str, Any] = {
            "$schema": "https://cdes.terprint.com/v1.2/genetics-profile.schema.json",
            "cdesVersion": "1.2.0",
        }
        
        # Parents
        if self.parent_1:
            result["parent1"] = self.parent_1
        if self.parent_2:
            result["parent2"] = self.parent_2
        if self.additional_parents:
            result["additionalParents"] = self.additional_parents
        if self.lineage_text:
            result["lineageText"] = self.lineage_text
        
        # Breeder
        if self.breeder:
            result["breeder"] = self.breeder
        if self.breeder_url:
            result["breederUrl"] = self.breeder_url
        if self.original_breeder:
            result["originalBreeder"] = self.original_breeder
        if self.origin_year:
            result["originYear"] = self.origin_year
        if self.origin_location:
            result["originLocation"] = self.origin_location
        
        # Classification
        if self.indica_pct is not None:
            result["indicaPct"] = self.indica_pct
        if self.sativa_pct is not None:
            result["sativaPct"] = self.sativa_pct
        if self.ruderalis_pct is not None:
            result["ruderalisPct"] = self.ruderalis_pct
        
        # Breeding details
        if self.breeding_technique != BreedingTechnique.UNKNOWN:
            result["breedingTechnique"] = self.breeding_technique.value
        if self.generation:
            result["generation"] = self.generation
        if self.stability != GeneticsStability.UNKNOWN:
            result["stability"] = self.stability.value
        if self.is_feminized is not None:
            result["isFeminized"] = self.is_feminized
        if self.is_autoflower is not None:
            result["isAutoflower"] = self.is_autoflower
        if self.is_clone_only:
            result["isCloneOnly"] = self.is_clone_only
        
        # Lineage tree
        if self.lineage:
            result["lineage"] = [n.to_dict() for n in self.lineage]
        
        # Phenotypes
        if self.phenotypes:
            result["phenotypes"] = [p.to_dict() for p in self.phenotypes]
        if self.selected_phenotype:
            result["selectedPhenotype"] = self.selected_phenotype
        
        # Provenance
        if self.sources:
            result["sources"] = [s.to_dict() for s in self.sources]
        if self.primary_source:
            result["primarySource"] = self.primary_source
        if self.confidence != GeneticsConfidence.UNKNOWN:
            result["confidence"] = self.confidence.value
        if self.last_verified:
            result["lastVerified"] = self.last_verified.isoformat()
        
        # Awards
        if self.awards:
            result["awards"] = self.awards
        if self.cup_wins:
            result["cupWins"] = self.cup_wins
        
        # Markers
        if self.genetic_markers:
            result["geneticMarkers"] = self.genetic_markers
        if self.chemotype:
            result["chemotype"] = self.chemotype
        
        # Metadata
        if self.metadata:
            result["metadata"] = self.metadata
        if self.tags:
            result["tags"] = self.tags
        
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GeneticsProfile":
        """Create GeneticsProfile from dictionary."""
        return cls(
            parent_1=data.get("parent1"),
            parent_2=data.get("parent2"),
            breeder=data.get("breeder"),
            breeder_url=data.get("breederUrl"),
            original_breeder=data.get("originalBreeder"),
            origin_year=data.get("originYear"),
            origin_location=data.get("originLocation"),
            indica_pct=data.get("indicaPct"),
            sativa_pct=data.get("sativaPct"),
            ruderalis_pct=data.get("ruderalisPct"),
            breeding_technique=BreedingTechnique(data["breedingTechnique"]) if data.get("breedingTechnique") else BreedingTechnique.UNKNOWN,
            generation=data.get("generation"),
            stability=GeneticsStability(data["stability"]) if data.get("stability") else GeneticsStability.UNKNOWN,
            is_feminized=data.get("isFeminized"),
            is_autoflower=data.get("isAutoflower"),
            is_clone_only=data.get("isCloneOnly", False),
            lineage=[LineageNode.from_dict(n) for n in data.get("lineage", [])],
            lineage_text=data.get("lineageText"),
            additional_parents=data.get("additionalParents", []),
            phenotypes=[PhenotypeVariant.from_dict(p) for p in data.get("phenotypes", [])],
            selected_phenotype=data.get("selectedPhenotype"),
            sources=[GeneticsSource.from_dict(s) for s in data.get("sources", [])],
            primary_source=data.get("primarySource"),
            confidence=GeneticsConfidence(data["confidence"]) if data.get("confidence") else GeneticsConfidence.UNKNOWN,
            last_verified=date.fromisoformat(data["lastVerified"]) if data.get("lastVerified") else None,
            awards=data.get("awards", []),
            cup_wins=data.get("cupWins", []),
            genetic_markers=data.get("geneticMarkers", {}),
            chemotype=data.get("chemotype"),
            metadata=data.get("metadata", {}),
            tags=data.get("tags", []),
        )

    @classmethod
    def from_simple(cls, genetics_string: str) -> "GeneticsProfile":
        """
        Create GeneticsProfile from a simple genetics string.
        
        Parses strings like:
        - "OG Kush x Durban Poison"
        - "GSC  Gelato"
        - "(GSC x OG Kush) x Gelato"
        """
        if not genetics_string:
            return cls()
        
        # Normalize separators
        text = genetics_string.strip()
        
        # Simple case: A x B or A  B
        for sep in ["  ", " x ", " X ", "  "]:
            if sep in text:
                parts = [p.strip() for p in text.split(sep)]
                if len(parts) == 2:
                    return cls(
                        parent_1=parts[0],
                        parent_2=parts[1],
                        lineage_text=text.replace(" x ", "  ").replace(" X ", "  "),
                    )
                elif len(parts) > 2:
                    return cls(
                        parent_1=parts[0],
                        parent_2=parts[1],
                        additional_parents=parts[2:],
                        lineage_text=text.replace(" x ", "  ").replace(" X ", "  "),
                        breeding_technique=BreedingTechnique.POLYHYBRID,
                    )
        
        # Couldn't parse, store as lineage text
        return cls(lineage_text=text)


# =============================================================================
# STRAIN MODEL (Updated for v1.2)
# =============================================================================

@dataclass
class Strain:
    """A cannabis strain (CDES v1.2)."""
    name: str
    type: StrainType = StrainType.UNKNOWN
    id: Optional[str] = None
    display_name: Optional[str] = None
    
    # Genetics - now supports both simple string and full profile
    genetics: Optional[str] = None                      # Simple string for backward compat
    genetics_profile: Optional[GeneticsProfile] = None  # Full genetics profile
    breeder: Optional[str] = None
    
    # Characteristics
    description: Optional[str] = None
    effects: List[str] = field(default_factory=list)
    flavors: List[str] = field(default_factory=list)
    aromas: List[str] = field(default_factory=list)
    aliases: List[str] = field(default_factory=list)
    
    # Typical ranges
    typical_thc_min: Optional[float] = None
    typical_thc_max: Optional[float] = None
    typical_cbd_min: Optional[float] = None
    typical_cbd_max: Optional[float] = None
    typical_terpene_profile: Optional[TerpeneProfile] = None

    def get_genetics_string(self) -> Optional[str]:
        """Get genetics as a simple string."""
        if self.genetics:
            return self.genetics
        if self.genetics_profile:
            return self.genetics_profile.get_parent_string()
        return None

    def get_parents(self) -> List[str]:
        """Get list of parent strain names."""
        if self.genetics_profile:
            return self.genetics_profile.get_all_parents()
        if self.genetics:
            # Parse simple string
            for sep in ["  ", " x ", " X "]:
                if sep in self.genetics:
                    return [p.strip() for p in self.genetics.split(sep)]
        return []

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "$schema": "https://cdes.terprint.com/v1.2/strain.schema.json",
            "cdesVersion": "1.2.0",
            "name": self.name,
            "type": self.type.value,
        }
        if self.id:
            result["id"] = self.id
        if self.display_name:
            result["displayName"] = self.display_name
        if self.genetics:
            result["genetics"] = self.genetics
        if self.genetics_profile:
            result["geneticsProfile"] = self.genetics_profile.to_dict()
        if self.breeder:
            result["breeder"] = self.breeder
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
        if self.typical_thc_min is not None:
            result["typicalThcMin"] = self.typical_thc_min
        if self.typical_thc_max is not None:
            result["typicalThcMax"] = self.typical_thc_max
        if self.typical_cbd_min is not None:
            result["typicalCbdMin"] = self.typical_cbd_min
        if self.typical_cbd_max is not None:
            result["typicalCbdMax"] = self.typical_cbd_max
        if self.typical_terpene_profile:
            result["typicalTerpeneProfile"] = self.typical_terpene_profile.to_dict()
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Strain":
        return cls(
            name=data["name"],
            type=StrainType(data.get("type", "unknown")),
            id=data.get("id"),
            display_name=data.get("displayName"),
            genetics=data.get("genetics"),
            genetics_profile=GeneticsProfile.from_dict(data["geneticsProfile"]) if data.get("geneticsProfile") else None,
            breeder=data.get("breeder"),
            description=data.get("description"),
            effects=data.get("effects", []),
            flavors=data.get("flavors", []),
            aromas=data.get("aromas", []),
            aliases=data.get("aliases", []),
            typical_thc_min=data.get("typicalThcMin"),
            typical_thc_max=data.get("typicalThcMax"),
            typical_cbd_min=data.get("typicalCbdMin"),
            typical_cbd_max=data.get("typicalCbdMax"),
            typical_terpene_profile=TerpeneProfile(**data["typicalTerpeneProfile"]) if data.get("typicalTerpeneProfile") else None,
        )


# =============================================================================
# BATCH AND PRODUCT MODELS
# =============================================================================

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


# =============================================================================
# LEGACY COMPATIBILITY EXPORTS
# =============================================================================

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


# =============================================================================
# GENETICS UTILITY FUNCTIONS (CDES v1.2.1)
# =============================================================================

import re

def parse_strain_name(name: str) -> Dict[str, Any]:
    """
    Parse a strain name to extract phenotype number and base name.
    
    Examples:
        "Tropical Teeth #2" -> {"base_name": "Tropical Teeth", "pheno_number": 2}
        "Oz Kush F2 #15" -> {"base_name": "Oz Kush F2", "pheno_number": 15}
        "Orange Sherbert 52" -> {"base_name": "Orange Sherbert", "pheno_number": 52}
        "Blue Dream" -> {"base_name": "Blue Dream", "pheno_number": None}
    
    Args:
        name: Full strain name potentially containing phenotype marker
        
    Returns:
        Dictionary with base_name and pheno_number (None if no number found)
    """
    if not name:
        return {"base_name": "", "pheno_number": None}
    
    name = name.strip()
    
    # Pattern 1: "#N" format (most common) - e.g., "Wino #4", "Tropical Teeth #2"
    match = re.match(r'^(.+?)\s*#(\d+)$', name)
    if match:
        return {"base_name": match.group(1).strip(), "pheno_number": int(match.group(2))}
    
    # Pattern 2: Trailing number with no # - e.g., "Orange Sherbert 52"
    # Only match if the number is at the end and preceded by a space
    match = re.match(r'^(.+?)\s+(\d+)$', name)
    if match:
        base = match.group(1).strip()
        num = int(match.group(2))
        # Don't match if it looks like a generation marker (F1, F2, S1, BX1, etc.)
        if not re.search(r'[FSBX]\s*$', base, re.IGNORECASE):
            return {"base_name": base, "pheno_number": num}
    
    return {"base_name": name, "pheno_number": None}


def parse_genetics_line(line: str) -> Dict[str, Any]:
    """
    Parse a genetics line in format "Strain Name    Parent1 x Parent2 x Parent3".
    
    Examples:
        "Triangle Kush    Hindu Kush x Lemon Thai x Chemdawg"
        "Tropical Teeth #2    Ice Cream Cake x Grape Teeth"
        "Yuzu Sour    Orange Sherbert 52 x Oz Kush F2 #15 x Gastro Pop"
    
    Args:
        line: A line containing strain name and genetics separated by whitespace
        
    Returns:
        Dictionary with strain info and genetics profile data
    """
    if not line or not line.strip():
        return {}
    
    # Split on multiple spaces (tab or 2+ spaces)
    parts = re.split(r'\s{2,}|\t', line.strip(), maxsplit=1)
    
    if len(parts) < 2:
        return {"strain_name": line.strip(), "genetics": None}
    
    strain_full_name = parts[0].strip()
    genetics_str = parts[1].strip()
    
    # Parse the strain name for phenotype info
    strain_info = parse_strain_name(strain_full_name)
    
    # Parse genetics (supports x, , or X as separator)
    parents = []
    for sep in ['  ', ' x ', ' X ']:
        if sep in genetics_str:
            parents = [p.strip() for p in genetics_str.split(sep)]
            break
    
    if not parents:
        parents = [genetics_str]
    
    return {
        "strain_name": strain_full_name,
        "base_name": strain_info["base_name"],
        "pheno_number": strain_info["pheno_number"],
        "genetics_string": genetics_str,
        "parents": parents,
        "parent_count": len(parents),
    }


def create_strain_with_genetics(
    name: str,
    genetics_string: str,
    strain_type: StrainType = StrainType.UNKNOWN,
    breeder: Optional[str] = None,
) -> "Strain":
    """
    Create a Strain with full GeneticsProfile from name and genetics string.
    
    Handles complex parent strings and extracts phenotype info from name.
    
    Examples:
        create_strain_with_genetics("Wino #4", "Cherry Punch x Grape Teeth")
        create_strain_with_genetics("Yuzu Sour", "Orange Sherbert 52 x Oz Kush F2 #15 x Gastro Pop")
    
    Args:
        name: Strain name (may include phenotype number)
        genetics_string: Parent string like "Parent1 x Parent2 x Parent3"
        strain_type: Optional strain type classification
        breeder: Optional breeder name
        
    Returns:
        Strain instance with populated genetics_profile
    """
    # Parse name for phenotype
    name_info = parse_strain_name(name)
    
    # Create genetics profile from parent string
    profile = GeneticsProfile.from_simple(genetics_string)
    
    if breeder:
        profile.breeder = breeder
    
    # Create phenotype variant if pheno number found
    if name_info["pheno_number"] is not None:
        from datetime import date
        pheno = PhenotypeVariant(
            phenotype_name=name,
            phenotype_number=name_info["pheno_number"],
        )
        profile.phenotypes.append(pheno)
        profile.selected_phenotype = name
    
    return Strain(
        name=name,
        display_name=name,
        type=strain_type,
        breeder=breeder,
        genetics=genetics_string,  # Keep simple string for backward compat
        genetics_profile=profile,
    )


def bulk_parse_genetics(lines: List[str]) -> List[Dict[str, Any]]:
    """
    Parse multiple genetics lines (e.g., from a spreadsheet or text file).
    
    Args:
        lines: List of lines in format "Strain    Parent1 x Parent2 x ..."
        
    Returns:
        List of parsed genetics dictionaries
    """
    results = []
    for line in lines:
        if line.strip():
            parsed = parse_genetics_line(line)
            if parsed:
                results.append(parsed)
    return results


# =============================================================================
# GENETICS UTILITY FUNCTIONS (CDES v1.2.1)
# =============================================================================

import re

def parse_strain_name(name: str) -> Dict[str, Any]:
    """
    Parse a strain name to extract phenotype number and base name.
    
    Examples:
        "Tropical Teeth #2" -> {"base_name": "Tropical Teeth", "pheno_number": 2}
        "Oz Kush F2 #15" -> {"base_name": "Oz Kush F2", "pheno_number": 15}
        "Orange Sherbert 52" -> {"base_name": "Orange Sherbert", "pheno_number": 52}
        "Blue Dream" -> {"base_name": "Blue Dream", "pheno_number": None}
    
    Args:
        name: Full strain name potentially containing phenotype marker
        
    Returns:
        Dictionary with base_name and pheno_number (None if no number found)
    """
    if not name:
        return {"base_name": "", "pheno_number": None}
    
    name = name.strip()
    
    # Pattern 1: "#N" format (most common) - e.g., "Wino #4", "Tropical Teeth #2"
    match = re.match(r'^(.+?)\s*#(\d+)$', name)
    if match:
        return {"base_name": match.group(1).strip(), "pheno_number": int(match.group(2))}
    
    # Pattern 2: Trailing number with no # - e.g., "Orange Sherbert 52"
    # Only match if the number is at the end and preceded by a space
    match = re.match(r'^(.+?)\s+(\d+)$', name)
    if match:
        base = match.group(1).strip()
        num = int(match.group(2))
        # Don't match if it looks like a generation marker (F1, F2, S1, BX1, etc.)
        if not re.search(r'[FSBX]\s*$', base, re.IGNORECASE):
            return {"base_name": base, "pheno_number": num}
    
    return {"base_name": name, "pheno_number": None}


def parse_genetics_line(line: str) -> Dict[str, Any]:
    """
    Parse a genetics line in format "Strain Name    Parent1 x Parent2 x Parent3".
    
    Examples:
        "Triangle Kush    Hindu Kush x Lemon Thai x Chemdawg"
        "Tropical Teeth #2    Ice Cream Cake x Grape Teeth"
        "Yuzu Sour    Orange Sherbert 52 x Oz Kush F2 #15 x Gastro Pop"
    
    Args:
        line: A line containing strain name and genetics separated by whitespace
        
    Returns:
        Dictionary with strain info and genetics profile data
    """
    if not line or not line.strip():
        return {}
    
    # Split on multiple spaces (tab or 2+ spaces)
    parts = re.split(r'\s{2,}|\t', line.strip(), maxsplit=1)
    
    if len(parts) < 2:
        return {"strain_name": line.strip(), "genetics": None}
    
    strain_full_name = parts[0].strip()
    genetics_str = parts[1].strip()
    
    # Parse the strain name for phenotype info
    strain_info = parse_strain_name(strain_full_name)
    
    # Parse genetics (supports x, , or X as separator)
    parents = []
    for sep in ['  ', ' x ', ' X ']:
        if sep in genetics_str:
            parents = [p.strip() for p in genetics_str.split(sep)]
            break
    
    if not parents:
        parents = [genetics_str]
    
    return {
        "strain_name": strain_full_name,
        "base_name": strain_info["base_name"],
        "pheno_number": strain_info["pheno_number"],
        "genetics_string": genetics_str,
        "parents": parents,
        "parent_count": len(parents),
    }


def create_strain_with_genetics(
    name: str,
    genetics_string: str,
    strain_type: StrainType = StrainType.UNKNOWN,
    breeder: Optional[str] = None,
) -> "Strain":
    """
    Create a Strain with full GeneticsProfile from name and genetics string.
    
    Handles complex parent strings and extracts phenotype info from name.
    
    Examples:
        create_strain_with_genetics("Wino #4", "Cherry Punch x Grape Teeth")
        create_strain_with_genetics("Yuzu Sour", "Orange Sherbert 52 x Oz Kush F2 #15 x Gastro Pop")
    
    Args:
        name: Strain name (may include phenotype number)
        genetics_string: Parent string like "Parent1 x Parent2 x Parent3"
        strain_type: Optional strain type classification
        breeder: Optional breeder name
        
    Returns:
        Strain instance with populated genetics_profile
    """
    # Parse name for phenotype
    name_info = parse_strain_name(name)
    
    # Create genetics profile from parent string
    profile = GeneticsProfile.from_simple(genetics_string)
    
    if breeder:
        profile.breeder = breeder
    
    # Create phenotype variant if pheno number found
    if name_info["pheno_number"] is not None:
        from datetime import date
        pheno = PhenotypeVariant(
            phenotype_name=name,
            phenotype_number=name_info["pheno_number"],
        )
        profile.phenotypes.append(pheno)
        profile.selected_phenotype = name
    
    return Strain(
        name=name,
        display_name=name,
        type=strain_type,
        breeder=breeder,
        genetics=genetics_string,  # Keep simple string for backward compat
        genetics_profile=profile,
    )


def bulk_parse_genetics(lines: List[str]) -> List[Dict[str, Any]]:
    """
    Parse multiple genetics lines (e.g., from a spreadsheet or text file).
    
    Args:
        lines: List of lines in format "Strain    Parent1 x Parent2 x ..."
        
    Returns:
        List of parsed genetics dictionaries
    """
    results = []
    for line in lines:
        if line.strip():
            parsed = parse_genetics_line(line)
            if parsed:
                results.append(parsed)
    return results
