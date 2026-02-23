"""
Pydantic schemas for API request/response validation.
"""
from pydantic import BaseModel, Field
from typing import Optional, List


class RecommendationRequest(BaseModel):
    """Request schema for recommendation endpoint."""
    
    category: str = Field(
        ...,
        description="Website category",
        example="startup"
    )
    style: str = Field(
        ...,
        description="Visual style preference",
        example="moderne"
    )
    preferences: Optional[str] = Field(
        default="",
        description="Additional user preferences",
        example="tech, innovant, coloré"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "category": "startup",
                "style": "moderne",
                "preferences": "tech, innovant"
            }
        }


class TemplateRecommendation(BaseModel):
    """Single template recommendation."""
    
    id: str = Field(..., example="startup_tech")
    reason: str = Field(..., example="Perfect template for tech startups")


class PaletteRecommendation(BaseModel):
    """Color palette recommendation."""
    
    id: str = Field(..., example="tech_gradient")
    reason: str = Field(..., example="Modern gradient colors for tech companies")


class FontRecommendation(BaseModel):
    """Font pairing recommendation."""
    
    heading: str = Field(..., example="Space Grotesk")
    body: str = Field(..., example="Work Sans")
    reason: str = Field(..., example="Modern and highly readable combination")


class RecommendationResponse(BaseModel):
    """Success response with recommendations."""
    
    success: bool = Field(default=True, example=True)
    recommended_templates: List[TemplateRecommendation]
    recommended_palette: PaletteRecommendation
    recommended_fonts: FontRecommendation
    fallback_used: bool = Field(default=False)
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "recommended_templates": [
                    {
                        "id": "startup_tech",
                        "reason": "Perfect template for tech startups"
                    },
                    {
                        "id": "landing_page",
                        "reason": "High conversion landing page"
                    }
                ],
                "recommended_palette": {
                    "id": "tech_gradient",
                    "reason": "Modern gradient colors"
                },
                "recommended_fonts": {
                    "heading": "Space Grotesk",
                    "body": "Work Sans",
                    "reason": "Modern and readable"
                },
                "fallback_used": False
            }
        }


class ErrorResponse(BaseModel):
    """Error response schema."""
    
    success: bool = Field(default=False)
    error: str
    detail: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "error": "Invalid request format",
                "detail": "category field is required"
            }
        }
