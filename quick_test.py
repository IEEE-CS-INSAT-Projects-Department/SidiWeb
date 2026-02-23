"""
quick_test.py

Quick test to verify the system works with backend templates.
Run from workspace root: python quick_test.py
"""

import json
import sys
from pathlib import Path

print("=" * 70)
print("  SIDIWEB - QUICK VERIFICATION TEST")
print("=" * 70)
print()

# Change to workspace root
workspace_root = Path(__file__).parent
print(f"📁 Workspace: {workspace_root}")
print()

# ============================================================================
# TEST 1: Check backend templates
# ============================================================================
print("TEST 1: Checking backend templates...")
backend_templates_dir = workspace_root / "data" / "backend_templates"
if backend_templates_dir.exists():
    templates = list(backend_templates_dir.glob("*.json"))
    print(f"✅ Found {len(templates)} backend templates:")
    for t in templates:
        print(f"   - {t.name}")
    print()
else:
    print("❌ Backend templates directory not found!")
    print()

# ============================================================================
# TEST 2: Verify design_system.json
# ============================================================================
print("TEST 2: Verifying design_system.json...")
design_system_path = workspace_root / "data" / "design_system.json"

if design_system_path.exists():
    with open(design_system_path, "r", encoding="utf-8") as f:
        design_system = json.load(f)
    
    print(f"✅ Design system loaded successfully!")
    print(f"   📦 Templates: {len(design_system.get('templates', []))}")
    print(f"   🎨 Color palettes: {len(design_system.get('color_palettes', []))}")
    print(f"   ✍️  Font pairings: {len(design_system.get('font_pairings', []))}")
    print()
    
    # Show template categories
    categories = set(t['category'] for t in design_system['templates'])
    print(f"   📋 Categories available: {', '.join(sorted(categories))}")
    print()
else:
    print("❌ design_system.json not found!")
    print()

# ============================================================================
# TEST 3: Check design notes
# ============================================================================
print("TEST 3: Checking design notes...")
notes_path = workspace_root / "data" / "design_notes" / "analysis.md"
if notes_path.exists():
    print(f"✅ Design notes found ({notes_path.stat().st_size} bytes)")
    print()
else:
    print("⚠️  Design notes not found (optional)")
    print()

# ============================================================================
# TEST 4: Verify prompts configuration
# ============================================================================
print("TEST 4: Checking prompts configuration...")
initial_prompt_path = workspace_root / "prompts" / "initial_prompt.txt"
variables_path = workspace_root / "prompts" / "variables.py"

if initial_prompt_path.exists():
    print("✅ initial_prompt.txt exists")
    with open(initial_prompt_path, "r", encoding="utf-8") as f:
        content = f.read()
        if "category" in content:
            print("   ✓ Uses 'category' (correct)")
        elif "sector" in content:
            print("   ⚠️  Still uses 'sector' (should be 'category')")
else:
    print("❌ initial_prompt.txt not found")

if variables_path.exists():
    print("✅ variables.py exists")
    # Check if it has new categories
    with open(variables_path, "r", encoding="utf-8") as f:
        content = f.read()
        if "startup" in content and "freelance" in content:
            print("   ✓ Contains new backend categories")
        else:
            print("   ⚠️  May need update with new categories")
else:
    print("❌ variables.py not found")
print()

# ============================================================================
# TEST 5: Check source code
# ============================================================================
print("TEST 5: Checking source code structure...")
src_dir = workspace_root / "src"

chains_dir = src_dir / "chains"
models_dir = src_dir / "models"

if chains_dir.exists() and (chains_dir / "recommendation_chain.py").exists():
    print("✅ recommendation_chain.py exists")
else:
    print("❌ recommendation_chain.py not found")

if models_dir.exists() and (models_dir / "output_models.py").exists():
    print("✅ output_models.py exists")
else:
    print("❌ output_models.py not found")

test_files = list(src_dir.glob("*test*.py"))
print(f"✅ Found {len(test_files)} test files")
print()

# ============================================================================
# TEST 6: Validate JSON structure
# ============================================================================
print("TEST 6: Validating JSON structure...")
try:
    # Validate all templates have required fields
    all_valid = True
    required_fields = ['id', 'name', 'category', 'layout', 'colors']
    
    for template in design_system['templates']:
        missing = [f for f in required_fields if f not in template]
        if missing:
            print(f"❌ Template {template.get('id', 'unknown')} missing: {missing}")
            all_valid = False
    
    if all_valid:
        print("✅ All templates have required fields")
    
    # Validate color palettes
    for palette in design_system['color_palettes']:
        if 'colors' not in palette or len(palette['colors']) < 3:
            print(f"⚠️  Palette {palette.get('id', 'unknown')} has insufficient colors")
            all_valid = False
    
    if all_valid:
        print("✅ All color palettes valid")
    
    print()
    
except Exception as e:
    print(f"❌ Validation error: {e}")
    print()

print("All quick tests completed!")