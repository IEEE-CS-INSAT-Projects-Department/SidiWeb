"""
variables.py

Defines and documents the input variables used by the SidiWeb AI
recommendation system. These variables guide the LLM to generate
controlled, design-system-based recommendations.
"""

DESIGN_PROMPT_VARIABLES = {
    "sector": {
        "description": (
            "The business or project domain of the website. "
            "This variable is used to filter relevant templates, "
            "color palettes, and font pairings from the design system."
        ),
        "type": "string",
        "allowed_values": [
            "education",
            "business",
            "portfolio",
            "ecommerce",
            "saas",
            "healthcare",
            "travel",
        ],
        "example": "education",
    },

    "style": {
        "description": (
            "The desired visual and aesthetic direction of the website. "
            "This influences layout structure, typography, and color usage."
        ),
        "type": "string",
        "allowed_values": [
            "modern",
            "minimal",
            "classic",
            "corporate",
            "creative",
        ],
        "example": "modern",
    },

    "preferences": {
        "description": (
            "Optional additional preferences expressed by the user. "
            "These are used to fine-tune recommendations without overriding "
            "the constraints of the design system."
        ),
        "type": "string",
        "example": "simple, professional, mobile-first",
    },
}

# Required variables for a valid recommendation request
REQUIRED_FIELDS = ["sector", "style"]

# Example request payload passed to the LLM
EXAMPLE_REQUEST = {
    "sector": "education",
    "style": "modern",
    "preferences": "simple, professional, accessibility-friendly",
}