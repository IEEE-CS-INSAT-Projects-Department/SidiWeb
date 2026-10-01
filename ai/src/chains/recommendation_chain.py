"""
recommendation_chain.py

Implements the core LangChain recommendation chain for SidiWeb.
Uses ChatPromptTemplate, OpenAI GPT-3.5-turbo, and JsonOutputParser
to generate structured design recommendations.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any

#from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI  # Pour Gemini (pip install langchain-google-genai)
# from langchain_anthropic import ChatAnthropic  # Pour Claude
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnablePassthrough

from ..models.output_models import DetailedRecommendationOutput


class RecommendationChain:
    """
    Main recommendation chain for SidiWeb AI.
    
    This chain takes user inputs (category, style, preferences) and generates
    design recommendations based on a provided design system.
    """
    
    def __init__(self, design_system_path: str = None, model_name: str = "gpt-3.5-turbo"):
        """
        Initialize the recommendation chain.
        
        Args:
            design_system_path: Path to the design_system.json file
            model_name: OpenAI model to use (default: gpt-3.5-turbo)
        """
        self.model_name = model_name
        self.design_system = self._load_design_system(design_system_path)
        self.llm = self._initialize_llm()
        self.prompt_template = self._create_prompt_template()
        self.parser = JsonOutputParser(pydantic_object=DetailedRecommendationOutput)
        self.chain = self._build_chain()
    
    def _load_design_system(self, path: str = None) -> Dict[str, Any]:
        """Load the design system from JSON file."""
        if path is None:
            # Default path
            path = Path(__file__).parent.parent.parent / "data" / "design_system.json"
        
        if not Path(path).exists():
            raise FileNotFoundError(
                f"Design system file not found: {path}\n"
                "Please create the design_system.json file with templates, "
                "color palettes, and fonts."
            )
        
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def _initialize_llm(self):
        """Initialize the LLM (OpenAI, Gemini, or Claude)."""
        
        # # Option 1: OpenAI (DEFAULT)
        # api_key = os.getenv("OPENAI_API_KEY")
        # if api_key and api_key != "sk_your_api_key_here":
        #     return ChatOpenAI(
        #         model=self.model_name,
        #         temperature=0.7,
        #         openai_api_key=api_key
        #     )
        
        # Option 2: Google Gemini
        # Pour activer : pip install langchain-google-genai google-generativeai
        # Puis décommentez ces lignes et ajoutez GOOGLE_API_KEY dans .env
        gemini_key = os.getenv("GOOGLE_API_KEY")
        if gemini_key:
            from langchain_google_genai import ChatGoogleGenerativeAI
            return ChatGoogleGenerativeAI(
                model="gemini-flash-lite-latest",
                temperature=0.7,
                google_api_key=gemini_key
            )
        
        # Option 3: Anthropic Claude
        # Pour activer : pip install langchain-anthropic anthropic
        # Puis décommentez ces lignes et ajoutez ANTHROPIC_API_KEY dans .env
        # claude_key = os.getenv("ANTHROPIC_API_KEY")
        # if claude_key:
        #     from langchain_anthropic import ChatAnthropic
        #     return ChatAnthropic(
        #         model="claude-3-sonnet-20240229",
        #         temperature=0.7,
        #         anthropic_api_key=claude_key
        #     )
        
        raise ValueError(
            "No valid API key found in .env file.\n"
            "Please set one of: GOOGLE_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY"
        )
    
    def _create_prompt_template(self) -> ChatPromptTemplate:
        """Create the ChatPromptTemplate from the initial prompt."""
        # Load the base prompt from prompts/initial_prompt.txt
        prompt_path = Path(__file__).parent.parent.parent / "prompts" / "initial_prompt.txt"
        
        with open(prompt_path, "r", encoding="utf-8") as f:
            base_prompt = f.read()
        
        # Create the template with format instructions
        template = base_prompt + "\n\nUSER INPUTS:\n- category: {category}\n- style: {style}\n- preferences: {preferences}\n\n{format_instructions}"
        
        return ChatPromptTemplate.from_template(template)
    
    def _build_chain(self):
        """Build the complete LangChain chain."""
        # Chain: input -> prompt -> LLM -> parser -> output
        chain = (
            {
                "category": RunnablePassthrough(),
                "style": RunnablePassthrough(),
                "preferences": RunnablePassthrough(),
                "design_system": lambda _: json.dumps(self.design_system, indent=2),
                "format_instructions": lambda _: self.parser.get_format_instructions()
            }
            | self.prompt_template
            | self.llm
            | self.parser
        )
        
        return chain
    
    def _fallback_rule_based(self, category: str, style: str, preferences: str = "") -> Dict[str, Any]:
        """
        Rule-based fallback when LLM fails.
        Uses simple business rules to match category to templates.
        
        Args:
            category: Website category
            style: Visual style
            preferences: User preferences
            
        Returns:
            Basic recommendation dict
        """
        # Category-to-template mapping
        category_mapping = {
            "education": ["education_formation", "site_vitrine"],
            "startup": ["startup_tech", "landing_page"],
            "freelance": ["portfolio_creatif", "site_vitrine"],
            "entreprise": ["agence_corporate", "service_professionnel"],
            "association": ["association_solidarite", "site_vitrine"],
            "service": ["service_professionnel", "site_vitrine"],
            "ecommerce": ["ecommerce_boutique", "landing_page"],
            "blog": ["blog_magazine", "site_vitrine"],
            "restaurant": ["restaurant_gastronomie", "site_vitrine"],
            "vitrine": ["site_vitrine", "landing_page"],
            "landing": ["landing_page", "site_vitrine"]
        }
        
        # Style-to-palette mapping
        style_mapping = {
            "moderne": "minimal_modern",
            "professionnel": "ocean_pro",
            "créatif": "creative_bold",
            "corporate": "elegant_classic",
            "minimaliste": "minimal_modern",
            "tech": "tech_gradient",
            "naturel": "earthy_natural",
            "élégant": "elegant_classic",
            "simple": "minimal_modern",
            "dynamique": "vibrant_energy",
            "zen": "soft_pastel",
            "traditionnel": "elegant_classic"
        }
        
        # Get templates for category (or default)
        templates = category_mapping.get(category.lower(), ["site_vitrine", "landing_page"])
        
        # Get palette for style (or default)
        palette_id = style_mapping.get(style.lower(), "ocean_pro")
        
        # Default font pairing - VALID from design_system.json
        font_heading = "Roboto"
        font_body = "Open Sans"
        
        return {
            "recommended_templates": [
                {
                    "id": templates[0],
                    "reason": f"Fallback recommendation: Best match for {category} category"
                },
                {
                    "id": templates[1] if len(templates) > 1 else templates[0],
                    "reason": f"Fallback recommendation: Alternative option for {category}"
                }
            ],
            "recommended_palette": {
                "id": palette_id,
                "reason": f"Fallback recommendation: Matches {style} style"
            },
            "recommended_fonts": {
                "heading": font_heading,
                "body": font_body,
                "reason": "Fallback recommendation: Universal readable font pairing"
            },
            "_fallback_used": True,
            "_fallback_reason": "Rule-based fallback due to LLM error"
        }
    
    def _fallback_default(self) -> Dict[str, Any]:
        """
        Default fallback when everything fails.
        Returns a safe, generic recommendation.
        
        Returns:
            Generic recommendation dict
        """
        return {
            "recommended_templates": [
                {
                    "id": "site_vitrine",
                    "reason": "Default fallback: Universal template suitable for most use cases"
                },
                {
                    "id": "landing_page",
                    "reason": "Default fallback: Simple landing page alternative"
                }
            ],
            "recommended_palette": {
                "id": "ocean_pro",
                "reason": "Default fallback: Professional neutral palette"
            },
            "recommended_fonts": {
                "heading": "Roboto",
                "body": "Open Sans",
                "reason": "Default fallback: Universal readable fonts (fonts_pro_clean)"
            },
            "_fallback_used": True,
            "_fallback_reason": "Default fallback - system timeout or critical error"
        }
    
    def invoke(self, category: str, style: str, preferences: str = "") -> Dict[str, Any]:
        """
        Generate recommendations based on user inputs.
        Includes fallback system for error handling.
        
        Args:
            category: Website category (e.g., "education", "startup", "freelance")
            style: Desired visual style (e.g., "moderne", "minimal", "classique")
            preferences: Optional additional preferences
        
        Returns:
            Dict containing recommended_templates, recommended_palette, recommended_fonts
        """
        inputs = {
            "category": category,
            "style": style,
            "preferences": preferences or "No specific preferences"
        }
        
        try:
            # Try primary LLM chain
            result = self.chain.invoke(inputs)
            return result
            
        except Exception as e:
            error_msg = str(e).lower()
            
            # If it's a parsing error (invalid JSON from LLM), use rule-based fallback
            if "parse" in error_msg or "json" in error_msg or "validation" in error_msg:
                print("⚠️  LLM output parsing failed. Using rule-based fallback...")
                return self._fallback_rule_based(category, style, preferences)
            
            # If it's a timeout or connection error, use default fallback
            elif "timeout" in error_msg or "connection" in error_msg or "quota" in error_msg:
                print("⚠️  LLM connection failed. Using default fallback...")
                return self._fallback_default()
            
            # For any other error, use rule-based fallback
            else:
                print(f"⚠️  LLM error: {e}. Using rule-based fallback...")
                return self._fallback_rule_based(category, style, preferences)
    
    async def ainvoke(self, category: str, style: str, preferences: str = "") -> Dict[str, Any]:
        """
        Generate recommendations based on user inputs (async version).
        Includes fallback system for error handling.
        
        Args:
            category: Website category
            style: Desired visual style
            preferences: Optional additional preferences
        
        Returns:
            Dict containing recommendations
        """
        inputs = {
            "category": category,
            "style": style,
            "preferences": preferences or "No specific preferences"
        }
        
        try:
            # Try primary LLM chain
            result = await self.chain.ainvoke(inputs)
            return result
            
        except Exception as e:
            error_msg = str(e).lower()
            
            # If it's a parsing error, use rule-based fallback
            if "parse" in error_msg or "json" in error_msg or "validation" in error_msg:
                print("⚠️  LLM output parsing failed. Using rule-based fallback...")
                return self._fallback_rule_based(category, style, preferences)
            
            # If it's a timeout or connection error, use default fallback
            elif "timeout" in error_msg or "connection" in error_msg or "quota" in error_msg:
                print("⚠️  LLM connection failed. Using default fallback...")
                return self._fallback_default()
            
            # For any other error, use rule-based fallback
            else:
                print(f"⚠️  LLM error: {e}. Using rule-based fallback...")
                return self._fallback_rule_based(category, style, preferences)


def create_recommendation_chain(
    design_system_path: str = None,
    model_name: str = "gpt-3.5-turbo"
) -> RecommendationChain:
    """
    Factory function to create a recommendation chain.
    
    Args:
        design_system_path: Path to design_system.json
        model_name: OpenAI model name
    
    Returns:
        Initialized RecommendationChain instance
    """
    return RecommendationChain(
        design_system_path=design_system_path,
        model_name=model_name
    )
