"""Models package for SidiWeb AI."""

from .output_models import (
    RecommendationOutput,
    DetailedRecommendationOutput,
    TemplateRecommendation,
    PaletteRecommendation,
    FontRecommendation,
)

__all__ = [
    "RecommendationOutput",
    "DetailedRecommendationOutput",
    "TemplateRecommendation",
    "PaletteRecommendation",
    "FontRecommendation",
]
# This makes the models importable as a python module