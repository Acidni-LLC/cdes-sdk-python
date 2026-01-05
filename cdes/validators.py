"""Validation functions for CDES data types."""

from typing import Any
from .models import ValidationResult, ValidationError


def validate_strain(data: dict[str, Any]) -> ValidationResult:
    """
    Validate a strain record against the CDES strain schema.
    
    Args:
        data: A dictionary containing strain data
        
    Returns:
        ValidationResult with valid=True if data conforms to schema
        
    Example:
        >>> result = validate_strain({
        ...     "id": "blue-dream",
        ...     "name": "Blue Dream",
        ...     "type": "hybrid"
        ... })
        >>> result.valid
        True
    """
    errors = []
    
    # Required fields
    required = ["id", "name", "type"]
    for field_name in required:
        if field_name not in data:
            errors.append(ValidationError(
                path=f"$.{field_name}",
                message=f"Required field '{field_name}' is missing"
            ))
    
    # Validate type enum
    if "type" in data:
        valid_types = ["indica", "sativa", "hybrid"]
        if data["type"] not in valid_types:
            errors.append(ValidationError(
                path="$.type",
                message=f"Type must be one of: {', '.join(valid_types)}",
                value=data["type"]
            ))
    
    # Validate id format (lowercase, hyphenated)
    if "id" in data:
        id_val = data["id"]
        if not isinstance(id_val, str) or not id_val.replace("-", "").isalnum():
            errors.append(ValidationError(
                path="$.id",
                message="ID must be lowercase alphanumeric with hyphens",
                value=id_val
            ))
    
    return ValidationResult(valid=len(errors) == 0, errors=errors)


def validate_coa(data: dict[str, Any]) -> ValidationResult:
    """
    Validate a Certificate of Analysis (COA) record.
    
    Args:
        data: A dictionary containing COA data
        
    Returns:
        ValidationResult with valid=True if data conforms to schema
    """
    errors = []
    
    # Required fields
    required = ["batchId", "lab", "testDate"]
    for field_name in required:
        if field_name not in data:
            errors.append(ValidationError(
                path=f"$.{field_name}",
                message=f"Required field '{field_name}' is missing"
            ))
    
    # Validate lab structure
    if "lab" in data:
        lab = data["lab"]
        if not isinstance(lab, dict):
            errors.append(ValidationError(
                path="$.lab",
                message="Lab must be an object"
            ))
        else:
            if "name" not in lab:
                errors.append(ValidationError(
                    path="$.lab.name",
                    message="Lab name is required"
                ))
    
    return ValidationResult(valid=len(errors) == 0, errors=errors)


def validate_terpene_profile(data: dict[str, Any]) -> ValidationResult:
    """
    Validate a terpene profile record.
    
    Args:
        data: A dictionary containing terpene profile data
        
    Returns:
        ValidationResult with valid=True if data conforms to schema
    """
    errors = []
    
    if "terpenes" not in data:
        errors.append(ValidationError(
            path="$.terpenes",
            message="Terpenes array is required"
        ))
    elif not isinstance(data["terpenes"], list):
        errors.append(ValidationError(
            path="$.terpenes",
            message="Terpenes must be an array"
        ))
    else:
        for i, terp in enumerate(data["terpenes"]):
            if "id" not in terp:
                errors.append(ValidationError(
                    path=f"$.terpenes[{i}].id",
                    message="Terpene ID is required"
                ))
            if "percentage" not in terp:
                errors.append(ValidationError(
                    path=f"$.terpenes[{i}].percentage",
                    message="Terpene percentage is required"
                ))
            elif not isinstance(terp["percentage"], (int, float)):
                errors.append(ValidationError(
                    path=f"$.terpenes[{i}].percentage",
                    message="Percentage must be a number"
                ))
            elif terp["percentage"] < 0 or terp["percentage"] > 100:
                errors.append(ValidationError(
                    path=f"$.terpenes[{i}].percentage",
                    message="Percentage must be between 0 and 100"
                ))
    
    return ValidationResult(valid=len(errors) == 0, errors=errors)


def validate_cannabinoid_profile(data: dict[str, Any]) -> ValidationResult:
    """
    Validate a cannabinoid profile record.
    
    Args:
        data: A dictionary containing cannabinoid profile data
        
    Returns:
        ValidationResult with valid=True if data conforms to schema
    """
    errors = []
    
    if "cannabinoids" not in data:
        errors.append(ValidationError(
            path="$.cannabinoids",
            message="Cannabinoids array is required"
        ))
    elif not isinstance(data["cannabinoids"], list):
        errors.append(ValidationError(
            path="$.cannabinoids",
            message="Cannabinoids must be an array"
        ))
    else:
        for i, cann in enumerate(data["cannabinoids"]):
            if "id" not in cann:
                errors.append(ValidationError(
                    path=f"$.cannabinoids[{i}].id",
                    message="Cannabinoid ID is required"
                ))
            if "percentage" not in cann:
                errors.append(ValidationError(
                    path=f"$.cannabinoids[{i}].percentage",
                    message="Cannabinoid percentage is required"
                ))
    
    return ValidationResult(valid=len(errors) == 0, errors=errors)
