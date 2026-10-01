from typing import List, Optional

from pydantic import BaseModel, Field


class AIRecommendationRequest(BaseModel):
    """Payload sent by frontend to the FastAPI proxy."""

    category: str = Field(..., description="Website category", examples=["startup"])
    style: str = Field(..., description="Visual style", examples=["moderne"])
    preferences: Optional[str] = Field(
        default="",
        description="Free-form user preferences",
        examples=["tech, innovant"],
    )


class TemplateRecommendation(BaseModel):
    id: str = Field(..., examples=["startup_tech"])
    reason: str = Field(..., examples=["Good fit for a modern startup website"])


class PaletteRecommendation(BaseModel):
    id: str = Field(..., examples=["tech_gradient"])
    reason: str = Field(..., examples=["Modern tech-oriented color palette"])


class FontRecommendation(BaseModel):
    heading: str = Field(..., examples=["Roboto"])
    body: str = Field(..., examples=["Open Sans"])
    reason: str = Field(..., examples=["Readable pair for most business websites"])


class AIRecommendationResponse(BaseModel):
    """Response returned by the FastAPI proxy (AI or fallback)."""

    success: bool = Field(default=True)
    recommended_templates: List[TemplateRecommendation]
    recommended_palette: PaletteRecommendation
    recommended_fonts: FontRecommendation
    fallback_used: bool = Field(default=False)
    source: str = Field(default="ai", description="ai or fallback")
    upstream_error: Optional[str] = Field(
        default=None,
        description="Filled when fallback is used because upstream failed",
    )
