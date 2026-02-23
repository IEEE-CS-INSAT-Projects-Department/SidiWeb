"""
manual_test.py

Interactive test script for beginners.
Run this to test the chain with your own inputs!
NOW WITH VALIDATION - Shows if your recommendation is valid!
"""

import sys
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path so we can import src package
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.chains.recommendation_chain import create_recommendation_chain
from src.utils.validators import validate_recommendation


def main():
    print("=" * 70)
    print("  SIDIWEB AI - MANUAL TEST WITH VALIDATION")
    print("=" * 70)
    print()
    print("💡 This test will:")
    print("   1. Generate recommendations based on your inputs")
    print("   2. Validate the output (check IDs, colors, format)")
    print("   3. Show if the recommendation meets quality standards")
    print()
    
    # Load API key
    load_dotenv()
    
    # Create the chain
    print("🔧 Creating recommendation chain...")
    try:
        chain = create_recommendation_chain()
        print("✅ Chain ready!\n")
    except Exception as e:
        print(f"❌ Error creating chain: {e}")
        return
    
    # Get user inputs
    print("Please provide the following information:")
    print()
    
    category = input("1. Category (service/vitrine/startup/landing/freelance/evenement/entreprise/education/cv/association/artisan): ").strip()
    style = input("2. Style (moderne/professionnel/simple/classique/minimal/dynamique/corporate/academique): ").strip()
    preferences = input("3. Preferences (optional, e.g., 'simple, dynamique, coloré'): ").strip()
    
    print()
    print("=" * 70)
    print("  PROCESSING YOUR REQUEST...")
    print("=" * 70)
    print()
    
    # Run the chain
    try:
        result = chain.invoke(
            category=category,
            style=style,
            preferences=preferences
        )
        
        print("✅ RECOMMENDATION SUCCESSFUL!\n")
        
        # Display results
        print("📋 RECOMMENDED TEMPLATES:")
        for i, template in enumerate(result.get("recommended_templates", []), 1):
            print(f"  {i}. {template.get('id', 'N/A')}")
            print(f"     Reason: {template.get('reason', 'N/A')}")
            print()
        
        palette = result.get("recommended_palette", {})
        print("🎨 RECOMMENDED COLOR PALETTE:")
        print(f"  • ID: {palette.get('id', 'N/A')}")
        print(f"    Reason: {palette.get('reason', 'N/A')}")
        print()
        
        fonts = result.get("recommended_fonts", {})
        print("✍️  RECOMMENDED FONTS:")
        print(f"  • Heading: {fonts.get('heading', 'N/A')}")
        print(f"  • Body: {fonts.get('body', 'N/A')}")
        print(f"    Reason: {fonts.get('reason', 'N/A')}")
        print()
        
        # Check if fallback was used
        if result.get("_fallback_used"):
            print("⚠️  FALLBACK USED:")
            print(f"    {result.get('_fallback_reason', 'Unknown reason')}")
            print()
        
        # VALIDATE THE RECOMMENDATION
        print("=" * 70)
        print("  VALIDATION RESULTS")
        print("=" * 70)
        print()
        
        validation = validate_recommendation(result)
        
        if validation["is_valid"]:
            print("✅ VALIDATION: PASSED")
            print("   All template IDs, palette ID, and fonts are valid!")
            print("   This recommendation meets quality standards.")
        else:
            print("❌ VALIDATION: FAILED")
            print("\n📋 Errors found:")
            for error in validation["errors"]:
                print(f"   • {error}")
        
        if validation["warnings"]:
            print("\n⚠️  Warnings:")
            for warning in validation["warnings"]:
                print(f"   • {warning}")
        
        print()
        print("=" * 70)
        if validation["is_valid"]:
            print("  ✅ TEST COMPLETE - RECOMMENDATION IS VALID!")
        else:
            print("  ❌ TEST COMPLETE - RECOMMENDATION HAS ERRORS")
        print("=" * 70)
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
