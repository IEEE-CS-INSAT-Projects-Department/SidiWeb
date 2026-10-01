"""
test_quality_mini.py

MINI quality test suite with only 5 scenarios.
Use this when you have quota limits or want quick testing.
"""

import sys
from pathlib import Path
from dotenv import load_dotenv
import time

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.chains.recommendation_chain import create_recommendation_chain
from src.utils.validators import validate_recommendation, calculate_conformity_rate


# 5 diverse test scenarios
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
    }
]


def print_header():
    """Print test suite header."""
    print("=" * 80)
    print("  SIDIWEB AI - MINI QUALITY TEST (5 scenarios)")
    print("  Quick testing with quota-friendly delays")
    print("=" * 80)
    print()


def print_scenario_header(scenario_num: int, scenario_name: str):
    """Print individual scenario header."""
    print("\n" + "=" * 80)
    print(f"  TEST {scenario_num}/5: {scenario_name}")
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
        
        # Check if fallback was used
        if result.get("_fallback_used"):
            print(f"\n⚠️  FALLBACK: {result.get('_fallback_reason', 'Unknown')}")
        
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
    print("  MINI TEST REPORT")
    print("=" * 80)
    
    print(f"\n📊 RESULTS:")
    print(f"  • Total tests: {stats['total_tests']}")
    print(f"  • Passed: {stats['passed']} ✅")
    print(f"  • Failed: {stats['failed']} ❌")
    print(f"  • Conformity rate: {stats['conformity_rate']:.1f}%")
    
    # Color code the conformity rate
    if stats['conformity_rate'] == 100:
        print("\n🎉 PERFECT! All tests passed!")
    elif stats['conformity_rate'] >= 80:
        print("\n✅ GOOD! Most tests passed.")
    else:
        print("\n⚠️  NEEDS IMPROVEMENT. Check errors below.")
    
    if stats['common_errors']:
        print("\n📋 ERRORS FOUND:")
        for error in stats['common_errors']:
            print(f"   • {error}")
    
    print("\n" + "=" * 80)


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
    
    # Run all tests with delays
    all_validations = []
    
    for i, scenario in enumerate(TEST_SCENARIOS, 1):
        validation = run_test_scenario(chain, scenario, i)
        all_validations.append(validation)
        
        # Wait 10 seconds between tests to avoid quota issues
        if i < len(TEST_SCENARIOS):
            print(f"\n⏸️  Waiting 10 seconds before next test (quota-friendly)...")
            time.sleep(10)
    
    # Print final report
    print_final_report(all_validations)


if __name__ == "__main__":
    main()
