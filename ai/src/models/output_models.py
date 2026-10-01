"""
output_models.py

Defines Pydantic models for structured output from the recommendation chain.
These models ensure the LLM response follows the expected format.
"""

from typing import List, Dict
from pydantic import BaseModel, Field


class TemplateRecommendation(BaseModel):
    """Single template recommendation with reasoning."""
    id: str = Field(description="Template ID from the design system")
    reason: str = Field(description="Explanation why this template fits the user needs")


class PaletteRecommendation(BaseModel):
    """Color palette recommendation with reasoning."""
    id: str = Field(description="Color palette ID from the design system")
    reason: str = Field(description="Why this color palette is appropriate")


class FontRecommendation(BaseModel):
    """Font pairing recommendation with reasoning."""
    heading: str = Field(description="Font name for headings")
    body: str = Field(description="Font name for body text")
    reason: str = Field(description="Why this font pairing works well")


class RecommendationOutput(BaseModel):
    """
    Complete recommendation output as specified in the project requirements.
    
    This matches the schema from the PDF:
    - templates: List[str] for IDs
    - colors: List[str] for HEX codes
    - fonts: Dict[str, str] for heading/body
    """
    templates: List[str] = Field(
        description="List of recommended template IDs",
        min_items=2,
        max_items=3
    )
    colors: List[str] = Field(
        description="List of HEX color codes (e.g., #FFFFFF)",
        min_items=3,
        max_items=6
    )
    fonts: Dict[str, str] = Field(
        description="Font pairing with 'heading' and 'body' keys"
    )


class DetailedRecommendationOutput(BaseModel):
    """
    Extended recommendation output with reasoning for each choice.
    This is the format used internally by the prompt template.
    """
    recommended_templates: List[TemplateRecommendation] = Field(
        description="2-3 recommended templates with explanations"
    )
    recommended_palette: PaletteRecommendation = Field(
        description="Selected color palette with reasoning"
    )
    recommended_fonts: FontRecommendation = Field(
        description="Selected font pairing with reasoning"
    )
