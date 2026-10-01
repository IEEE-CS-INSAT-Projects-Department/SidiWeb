"""
validators.py

Validation utilities for checking recommendation quality.
Validates template IDs, color formats, palette IDs, and font IDs.
"""

import re
import json
from pathlib import Path
from typing import Dict, Any, List, Tuple


# Valid IDs from design_system.json
VALID_TEMPLATE_IDS = [
    "service_professionnel",
    "site_vitrine", 
    "startup_tech",
    "landing_page",
    "portfolio_creatif",
    "blog_magazine",
    "ecommerce_boutique",
    "education_formation",
    "restaurant_gastronomie",
    "agence_corporate",
    "association_solidarite"
]

VALID_PALETTE_IDS = [
    "ocean_pro",
    "forest_fresh",
    "sunset_warm",
    "ocean_deep",
    "creative_bold",
    "minimal_modern",
    "earthy_natural",
    "tech_gradient",
    "elegant_classic",
    "vibrant_energy",
    "soft_pastel"
]

VALID_FONT_IDS = [
    "pro_modern",
    "startup_tech",
    "simple_clean",
    "creative_bold",
    "corporate_classic",
    "blog_friendly",
    "elegant_serif",
    "modern_minimal"
]

# HEX color pattern
HEX_COLOR_PATTERN = re.compile(r'^#[0-9A-Fa-f]{6}$')


def validate_template_ids(template_recommendations: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
    """
    Validate that all recommended template IDs exist in the design system.
    
    Args:
        template_recommendations: List of template recommendation dicts with 'id' field
        
    Returns:
        Tuple of (all_valid: bool, invalid_ids: List[str])
    """
    invalid_ids = []
    
    for template in template_recommendations:
        template_id = template.get("id")
        if template_id not in VALID_TEMPLATE_IDS:
            invalid_ids.append(template_id)
    
    return len(invalid_ids) == 0, invalid_ids


def validate_hex_colors(colors: List[str]) -> Tuple[bool, List[str]]:
    """
    Validate that all colors are in valid HEX format (#RRGGBB).
    
    Args:
        colors: List of color strings to validate
        
    Returns:
        Tuple of (all_valid: bool, invalid_colors: List[str])
    """
    invalid_colors = []
    
    for color in colors:
        if not HEX_COLOR_PATTERN.match(color):
            invalid_colors.append(color)
    
    return len(invalid_colors) == 0, invalid_colors


def validate_palette_id(palette_id: str) -> bool:
    """
    Validate that a palette ID exists in the design system.
    
    Args:
        palette_id: The palette ID to validate
        
    Returns:
        True if valid, False otherwise
    """
    return palette_id in VALID_PALETTE_IDS


def validate_font_pairing(heading_font: str, body_font: str) -> Tuple[bool, str]:
    """
    Validate that the font pairing exists in the design system.
    
    Args:
        heading_font: The heading font name
        body_font: The body font name
        
    Returns:
        Tuple of (is_valid: bool, message: str)
    """
    # Load design system to check fonts
    design_system_path = Path(__file__).parent.parent.parent / "data" / "design_system.json"
    
    try:
        with open(design_system_path, "r", encoding="utf-8") as f:
            design_system = json.load(f)
        
        # Check if this combination exists in font_pairings
        for font_pairing in design_system.get("font_pairings", []):
            if (font_pairing.get("heading") == heading_font and 
                font_pairing.get("body") == body_font):
                return True, "Valid font pairing"
        
        return False, f"Font pairing {heading_font}/{body_font} not found in design system"
    
    except Exception as e:
        return False, f"Error validating fonts: {str(e)}"


def validate_recommendation(recommendation: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate a complete recommendation output.
    
    Args:
        recommendation: The full recommendation dict
        
    Returns:
        Dict with validation results:
        {
            "is_valid": bool,
            "errors": List[str],
            "warnings": List[str]
        }
    """
    errors = []
    warnings = []
    
    # Validate templates
    templates = recommendation.get("recommended_templates", [])
    if not templates:
        errors.append("No templates recommended")
    elif len(templates) < 2:
        warnings.append(f"Only {len(templates)} template(s) recommended (expected 2-3)")
    elif len(templates) > 3:
        warnings.append(f"{len(templates)} templates recommended (expected 2-3)")
    
    templates_valid, invalid_template_ids = validate_template_ids(templates)
    if not templates_valid:
        errors.append(f"Invalid template IDs: {', '.join(invalid_template_ids)}")
    
    # Check for reason field in templates
    for template in templates:
        if "reason" not in template:
            warnings.append(f"Template {template.get('id')} missing 'reason' field")
    
    # Validate palette
    palette = recommendation.get("recommended_palette", {})
    if not palette:
        errors.append("No color palette recommended")
    else:
        palette_id = palette.get("id")
        if not validate_palette_id(palette_id):
            errors.append(f"Invalid palette ID: {palette_id}")
        if "reason" not in palette:
            warnings.append("Palette missing 'reason' field")
    
    # Validate fonts
    fonts = recommendation.get("recommended_fonts", {})
    if not fonts:
        errors.append("No fonts recommended")
    else:
        heading = fonts.get("heading")
        body = fonts.get("body")
        
        if not heading or not body:
            errors.append("Font pairing incomplete (missing heading or body)")
        else:
            font_valid, font_message = validate_font_pairing(heading, body)
            if not font_valid:
                errors.append(font_message)
        
        if "reason" not in fonts:
            warnings.append("Fonts missing 'reason' field")
    
    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }


def calculate_conformity_rate(test_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate the conformity rate across multiple test results.
    
    Args:
        test_results: List of validation results from validate_recommendation()
        
    Returns:
        Dict with conformity statistics:
        {
            "total_tests": int,
            "passed": int,
            "failed": int,
            "conformity_rate": float (percentage),
            "common_errors": List[str]
        }
    """
    total = len(test_results)
    passed = sum(1 for result in test_results if result["is_valid"])
    failed = total - passed
    
    # Count common errors
    error_counts = {}
    for result in test_results:
        for error in result.get("errors", []):
            error_counts[error] = error_counts.get(error, 0) + 1
    
    # Sort by frequency
    common_errors = sorted(error_counts.items(), key=lambda x: x[1], reverse=True)
    common_errors = [f"{error} ({count}x)" for error, count in common_errors[:5]]
    
    return {
        "total_tests": total,
        "passed": passed,
        "failed": failed,
        "conformity_rate": (passed / total * 100) if total > 0 else 0,
        "common_errors": common_errors
    }
