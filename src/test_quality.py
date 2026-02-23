"""
test_quality.py

Quality test suite with 20 diverse user scenarios.
Tests recommendation quality and calculates conformity rate.

Run this to ensure >90% success rate on recommendations.
"""

import sys
from pathlib import Path
from dotenv import load_dotenv
import time

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.chains.recommendation_chain import create_recommendation_chain
from src.utils.validators import validate_recommendation, calculate_conformity_rate


# 20 diverse test scenarios covering different categories and styles
TEST_SCENARIOS = [
    {
        "name": "École primaire - Simple et coloré",
        "category": "education",
        "style": "simple",
        "preferences": "coloré, enfantin, accessible"
    },
    {
        "name": "Startup FinTech - Moderne et tech",
        "category": "startup",
        "style": "moderne",
        "preferences": "professionnel, tech, innovant"
    },
    {
        "name": "Photographe freelance - Portfolio créatif",
        "category": "freelance",
        "style": "créatif",
        "preferences": "visuel, artistique, portfolio"
    },
    {
        "name": "Cabinet d'avocats - Corporate classique",
        "category": "entreprise",
        "style": "corporate",
        "preferences": "sérieux, confiance, traditionnel"
    },
    {
        "name": "ONG humanitaire - Solidaire et accessible",
        "category": "association",
        "style": "simple",
        "preferences": "chaleureux, solidaire, accessible"
    },
    {
        "name": "Boutique de vêtements en ligne",
        "category": "ecommerce",
        "style": "moderne",
        "preferences": "visuel, mode, catalogue"
    },
    {
        "name": "Blog lifestyle et voyages",
        "category": "blog",
        "style": "créatif",
        "preferences": "personnel, storytelling, images"
    },
    {
        "name": "Designer graphique - Portfolio minimaliste",
        "category": "freelance",
        "style": "minimaliste",
        "preferences": "épuré, élégant, portfolio"
    },
    {
        "name": "Restaurant gastronomique haut de gamme",
        "category": "restaurant",
        "style": "élégant",
        "preferences": "luxe, gastronomie, réservation"
    },
    {
        "name": "Clinique dentaire - Professionnel et rassurant",
        "category": "service",
        "style": "professionnel",
        "preferences": "santé, confiance, moderne"
    },
    {
        "name": "Agence immobilière - Classique et corporate",
        "category": "entreprise",
        "style": "corporate",
        "preferences": "sérieux, catalogue, recherche"
    },
    {
        "name": "Agence de communication créative",
        "category": "entreprise",
        "style": "créatif",
        "preferences": "innovant, original, portfolio"
    },
    {
        "name": "Association sportive locale",
        "category": "association",
        "style": "dynamique",
        "preferences": "sportif, communauté, événements"
    },
    {
        "name": "Plateforme de formation en ligne",
        "category": "education",
        "style": "professionnel",
        "preferences": "cours, e-learning, structuré"
    },
    {
        "name": "Organisateur d'événements - Moderne",
        "category": "service",
        "style": "moderne",
        "preferences": "événementiel, dynamique, visuel"
    },
    {
        "name": "Boutique de produits bio artisanaux",
        "category": "ecommerce",
        "style": "naturel",
        "preferences": "bio, authentique, terroir"
    },
    {
        "name": "Studio de yoga et bien-être",
        "category": "service",
        "style": "zen",
        "preferences": "calme, bien-être, réservation"
    },
    {
        "name": "Développeur web freelance - Tech",
        "category": "freelance",
        "style": "tech",
        "preferences": "portfolio, projets, tech"
    },
    {
        "name": "Cabinet de consulting en management",
        "category": "entreprise",
        "style": "professionnel",
        "preferences": "expertise, corporate, services"
    },
    {
        "name": "Artisan menuisier - Authentique",
        "category": "service",
        "style": "traditionnel",
        "preferences": "artisanat, savoir-faire, authentique"
    }
]


def print_header():
    """Print test suite header."""
    print("=" * 80)
    print("  SIDIWEB AI - QUALITY TEST SUITE")
    print("  Testing 20 diverse scenarios with validation")
    print("=" * 80)
    print()


def print_scenario_header(scenario_num: int, scenario_name: str):
    """Print individual scenario header."""
    print("\n" + "=" * 80)
    print(f"  TEST {scenario_num}/20: {scenario_name}")
    print("=" * 80)


def print_validation_results(validation: dict):
    """Print validation results with colors."""
    if validation["is_valid"]:
        print("✅ VALIDATION: PASSED")
    else:
        print("❌ VALIDATION: FAILED")
        print("\n📋 Errors:")
        for error in validation["errors"]:
            print(f"   • {error}")
    
    if validation["warnings"]:
        print("\n⚠️  Warnings:")
        for warning in validation["warnings"]:
            print(f"   • {warning}")


def run_test_scenario(chain, scenario: dict, scenario_num: int) -> dict:
    """Run a single test scenario and return validation result."""
    print_scenario_header(scenario_num, scenario["name"])
    
    print(f"\n📥 INPUT:")
    print(f"  • Category: {scenario['category']}")
    print(f"  • Style: {scenario['style']}")
    print(f"  • Preferences: {scenario['preferences']}")
    
    try:
        print("\n⏳ Invoking chain...")
        start_time = time.time()
        
        result = chain.invoke(
            category=scenario["category"],
            style=scenario["style"],
            preferences=scenario["preferences"]
        )
        
        elapsed = time.time() - start_time
        print(f"⏱️  Completed in {elapsed:.2f}s")
        
        print("\n📤 OUTPUT:")
        print(f"  • Templates: {[t['id'] for t in result.get('recommended_templates', [])]}")
        print(f"  • Palette: {result.get('recommended_palette', {}).get('id', 'N/A')}")
        fonts = result.get('recommended_fonts', {})
        print(f"  • Fonts: {fonts.get('heading', 'N/A')} / {fonts.get('body', 'N/A')}")
        
        # Validate the result
        validation = validate_recommendation(result)
        print_validation_results(validation)
        
        return validation
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        return {
            "is_valid": False,
            "errors": [f"Chain invocation failed: {str(e)}"],
            "warnings": []
        }


def print_final_report(all_validations: list):
    """Print final conformity report."""
    stats = calculate_conformity_rate(all_validations)
    
    print("\n" + "=" * 80)
    print("  FINAL QUALITY REPORT")
    print("=" * 80)
    
    print(f"\n📊 RESULTS:")
    print(f"  • Total tests: {stats['total_tests']}")
    print(f"  • Passed: {stats['passed']} ✅")
    print(f"  • Failed: {stats['failed']} ❌")
    print(f"  • Conformity rate: {stats['conformity_rate']:.1f}%")
    
    # Color code the conformity rate
    if stats['conformity_rate'] >= 90:
        print("\n🎉 EXCELLENT! Conformity rate ≥ 90% - Quality target achieved!")
    elif stats['conformity_rate'] >= 75:
        print("\n⚠️  GOOD but needs improvement. Target: ≥ 90%")
    else:
        print("\n❌ INSUFFICIENT. Significant prompt improvements needed. Target: ≥ 90%")
    
    if stats['common_errors']:
        print("\n📋 MOST COMMON ERRORS:")
        for error in stats['common_errors']:
            print(f"   • {error}")
    
    print("\n" + "=" * 80)
    print("💡 TIP: If conformity < 90%, review the prompt and add more constraints.")
    print("=" * 80)


def main():
    """Main test execution."""
    print_header()
    
    # Load environment
    load_dotenv()
    
    # Create chain
    print("🔧 Initializing recommendation chain...")
    try:
        chain = create_recommendation_chain()
        print("✅ Chain created successfully!\n")
    except Exception as e:
        print(f"❌ Failed to create chain: {e}")
        return
    
    # Run all tests
    all_validations = []
    
    for i, scenario in enumerate(TEST_SCENARIOS, 1):
        validation = run_test_scenario(chain, scenario, i)
        all_validations.append(validation)
        
        # Longer delay to avoid rate limiting (5 seconds between tests)
        if i < len(TEST_SCENARIOS):
            print(f"\n⏸️  Waiting 5 seconds to avoid rate limits...")
            time.sleep(5)
    
    # Print final report
    print_final_report(all_validations)


if __name__ == "__main__":
    main()
