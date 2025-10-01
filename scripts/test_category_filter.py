"""
Test category filter to ensure categories don't return unrelated fields.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.gui.utils.json_search_engine import JSONSearchEngine

def test_colors_category_excludes_slogan():
    """Test that searching 'colors' category doesn't return slogan results"""
    engine = JSONSearchEngine()
    
    # Search for a word that appears in Alabama's slogan but not colors
    # Alabama slogan: "Stars Fell on Alabama"
    results = engine.search('stars', category='colors')
    
    print(f"\n=== Testing 'stars' in COLORS category ===")
    print(f"Total results: {len(results)}")
    
    # Check if any results are from slogan field (they shouldn't be)
    slogan_results = [r for r in results if r.get('match_field') == 'slogan']
    
    if slogan_results:
        print(f"❌ FAIL: Found {len(slogan_results)} slogan result(s) in COLORS category:")
        for r in slogan_results:
            print(f"   State: {r['state_code']}, Field: {r['match_field']}, Value: {r['match_value']}")
    else:
        print("✅ PASS: No slogan results found in COLORS category")
    
    # Now test in 'all' category - should find slogan
    results_all = engine.search('stars', category='all')
    slogan_results_all = [r for r in results_all if r.get('match_field') == 'slogan']
    
    print(f"\n=== Testing 'stars' in ALL category ===")
    print(f"Total results: {len(results_all)}")
    print(f"Slogan results: {len(slogan_results_all)}")
    
    if slogan_results_all:
        print("✅ PASS: Found slogan results in ALL category as expected")
        for r in slogan_results_all[:3]:
            print(f"   State: {r['state_code']}, Field: {r['match_field']}, Value: {r['match_value'][:50]}")
    else:
        print("❌ FAIL: Should have found slogan results in ALL category")

def test_slogans_category_only():
    """Test that searching 'slogans' category only returns slogan results"""
    engine = JSONSearchEngine()
    
    results = engine.search('stars', category='slogans')
    
    print(f"\n=== Testing 'stars' in SLOGANS category ===")
    print(f"Total results: {len(results)}")
    
    if results:
        print("Results found:")
        for r in results[:5]:
            print(f"   State: {r['state_code']}, Field: {r['match_field']}, Value: {r['match_value'][:50]}")
        
        # Check if all results are slogan-related
        non_slogan = [r for r in results if r.get('match_field') not in ['slogan', 'motto', 'tagline']]
        if non_slogan:
            print(f"❌ WARNING: Found {len(non_slogan)} non-slogan results in SLOGANS category")
        else:
            print("✅ PASS: All results are slogan-related")
    else:
        print("No results found (may need to check data)")

def test_fonts_category_excludes_colors():
    """Test that searching 'fonts' category doesn't return color results"""
    engine = JSONSearchEngine()
    
    # Search for a color name
    results = engine.search('white', category='fonts')
    
    print(f"\n=== Testing 'white' in FONTS category ===")
    print(f"Total results: {len(results)}")
    
    # Check if any results are from color fields
    color_results = [r for r in results if 'color' in r.get('match_field', '').lower()]
    
    if color_results:
        print(f"❌ FAIL: Found {len(color_results)} color result(s) in FONTS category:")
        for r in color_results[:3]:
            print(f"   State: {r['state_code']}, Field: {r['match_field']}, Value: {r['match_value'][:50]}")
    else:
        print("✅ PASS: No color results found in FONTS category")
    
    # Compare with 'all' category
    results_all = engine.search('white', category='all')
    color_results_all = [r for r in results_all if 'color' in r.get('match_field', '').lower()]
    
    print(f"\n=== Testing 'white' in ALL category ===")
    print(f"Total results: {len(results_all)}")
    print(f"Color results: {len(color_results_all)}")
    
    if color_results_all:
        print("✅ PASS: Found color results in ALL category as expected")

if __name__ == "__main__":
    print("=" * 80)
    print("CATEGORY FILTER VERIFICATION TEST")
    print("=" * 80)
    
    test_colors_category_excludes_slogan()
    test_slogans_category_only()
    test_fonts_category_excludes_colors()
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)
