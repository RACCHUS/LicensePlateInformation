"""Simple category filter test"""
import sys
sys.path.insert(0, '.')
from src.gui.utils.json_search_engine import JSONSearchEngine

engine = JSONSearchEngine()

# Test 1: Search "stars" in colors category - should NOT return slogan
print("=" * 70)
print("TEST 1: Search 'stars' in COLORS category")
print("=" * 70)
results = engine.search('stars', category='colors')
print(f"Total results: {len(results)}")
slogan_results = [r for r in results if r['field'] == 'slogan']
print(f"Slogan results: {len(slogan_results)}")
if slogan_results:
    print("❌ FAIL: Found slogan results in colors category!")
    for r in slogan_results:
        print(f"   {r['state']}: {r['value']}")
else:
    print("✅ PASS: No slogan results in colors category")

# Test 2: Search "fell" in slogans category - SHOULD return slogan
print("\n" + "=" * 70)
print("TEST 2: Search 'fell' in SLOGANS category")
print("=" * 70)
results = engine.search('fell', category='slogans')
print(f"Total results: {len(results)}")
if results:
    print("Results:")
    for r in results[:3]:
        print(f"   {r['state']}: {r['field']} = {r['value'][:50]}")
    slogan_results = [r for r in results if r['field'] == 'slogan']
    if slogan_results:
        print(f"✅ PASS: Found {len(slogan_results)} slogan result(s)")
    else:
        print("⚠️  WARNING: No slogan results found")
else:
    print("❌ FAIL: Should have found results")

# Test 3: Search "fell" in all category - should return more results
print("\n" + "=" * 70)
print("TEST 3: Search 'fell' in ALL category")
print("=" * 70)
results = engine.search('fell', category='all')
print(f"Total results: {len(results)}")
slogan_results = [r for r in results if r['field'] == 'slogan']
print(f"Slogan results: {len(slogan_results)}")
if slogan_results:
    print("✅ PASS: Found slogan results in all category")
