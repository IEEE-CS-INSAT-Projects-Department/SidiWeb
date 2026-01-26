"""
Prompt Variables Configuration
This file defines the variables that will be passed to the LLM for design generation.
"""

DESIGN_PROMPT_VARIABLES = {
    "sector": {
        "description": "Client's business sector",
        "type": "string",
        "examples": ["SaaS RH", "E-commerce", "FinTech", "Healthcare", "Travel", "Education"],
    },
    "style": {
        "description": "Desired artistic direction",
        "type": "string",
        "examples": ["minimal", "brutalist", "corporate", "playful", "luxury", "modern", "retro"],
    },
    "preferences": {
        "description": "Specific constraints or wishes",
        "type": "string",
        "examples": [
            "accent on onboarding",
            "dark mode priority",
            "mobile-first approach",
            "high contrast for accessibility",
            "emphasis on brand storytelling"
        ],
    },
}

# Example usage:
EXAMPLE_REQUEST = {
    "sector": "SaaS RH",
    "style": "minimal",
    "preferences": "accent on onboarding flow and user retention",
}

REQUIRED_FIELDS = ["sector", "style", "preferences"]
