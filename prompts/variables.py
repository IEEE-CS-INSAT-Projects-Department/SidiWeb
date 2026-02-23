"""
variables.py

Defines and documents the input variables used by the SidiWeb AI
recommendation system. These variables guide the LLM to generate
controlled, design-system-based recommendations.


"""

DESIGN_PROMPT_VARIABLES = {
    "category": {
        "description": (
            "The category or type of website needed. "
            "This variable is used to filter relevant templates "
            "from the design system based on the project's purpose."
        ),
        "type": "string",
        "allowed_values": [
            "service",        # Services professionnels
            "vitrine",        # Site vitrine basique
            "startup",        # Startup tech/innovante
            "landing",        # Landing page
            "freelance",      # Freelance/consultant
            "evenement",      # Événements
            "entreprise",     # Entreprise établie
            "education",      # Éducation/formation
            "cv",            # CV en ligne
            "association",    # Association/ONG
            "artisan",       # Artisan/métiers manuels
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
            "moderne",       # Moderne/contemporain
            "professionnel", # Professionnel/sérieux
            "simple",        # Simple/épuré
            "classique",     # Classique/traditionnel
            "minimal",       # Minimaliste
            "dynamique",     # Dynamique/énergique
            "corporate",     # Corporate/institutionnel
            "academique",    # Académique/structuré
        ],
        "example": "moderne",
    },

    "preferences": {
        "description": (
            "Optional additional preferences expressed by the user. "
            "These are used to fine-tune recommendations without overriding "
            "the constraints of the design system."
        ),
        "type": "string",
        "example": "simple, coloré, accessible, responsive",
    },
}

# Required variables for a valid recommendation request
REQUIRED_FIELDS = ["category", "style"]

# Example request payloads passed to the LLM
EXAMPLE_REQUESTS = [
    {
        "category": "education",
        "style": "academique",
        "preferences": "simple, professionnel, accessible",
    },
    {
        "category": "startup",
        "style": "moderne",
        "preferences": "dynamique, innovant, tech",
    },
    {
        "category": "freelance",
        "style": "professionnel",
        "preferences": "portfolio, moderne, créatif",
    },
]

# Category to style mappings (reference)
CATEGORY_STYLE_SUGGESTIONS = {
    "service": ["professionnel", "moderne", "simple"],
    "vitrine": ["simple", "minimal", "classique"],
    "startup": ["moderne", "dynamique"],
    "landing": ["moderne", "dynamique"],
    "freelance": ["moderne", "professionnel", "minimal"],
    "evenement": ["moderne", "dynamique"],
    "entreprise": ["corporate", "professionnel", "classique"],
    "education": ["academique", "professionnel", "simple"],
    "cv": ["minimal", "professionnel"],
    "association": ["simple", "classique"],
    "artisan": ["classique", "simple"],
}