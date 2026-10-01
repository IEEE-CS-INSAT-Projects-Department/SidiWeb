"""Chains package for SidiWeb AI."""

from .recommendation_chain import RecommendationChain, create_recommendation_chain

__all__ = ["RecommendationChain", "create_recommendation_chain"]
# makes the chain importable as a python module 