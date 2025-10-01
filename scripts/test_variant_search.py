"""Test searching design_variants through search engine"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.gui.utils.json_search_engine import JSONSearchEngine

# Create search engine
engine = JSONSearchEngine()

print("Testing design_variants search functionality...")
print("=" * 60)

# Test 1: Search for "Sweet Home" variant
print("\nTest 1: Searching for 'sweet' (should find 'Sweet Home' variants)")
print("-" * 60)
results = engine.search("sweet", category="all", state_filter="AL")
print(f"Found {len(results)} results:")
for i, result in enumerate(results[:10], 1):
    print(f"{i}. {result['plate_type']} ({result['state']})")
    print(f"   Field: {result['field']}")
    print(f"   Value: {result['value']}")

# Test 2: Search for "Mobile Bay" variant
print("\n\nTest 2: Searching for 'mobile' (should find 'Mobile Bay' variants)")
print("-" * 60)
results = engine.search("mobile", category="all", state_filter="AL")
print(f"Found {len(results)} results:")
for i, result in enumerate(results[:10], 1):
    print(f"{i}. {result['plate_type']} ({result['state']})")
    print(f"   Field: {result['field']}")
    print(f"   Value: {result['value']}")

# Test 3: Search for date-based variant
print("\n\nTest 3: Searching for 'Since 2022' (date-based variants)")
print("-" * 60)
results = engine.search("since 2022", category="all", state_filter="AL")
print(f"Found {len(results)} results:")
for i, result in enumerate(results[:10], 1):
    print(f"{i}. {result['plate_type']} ({result['state']})")
    print(f"   Field: {result['field']}")
    print(f"   Value: {result['value']}")

# Test 4: Search for "Stars Fell On" variant
print("\n\nTest 4: Searching for 'stars fell' (should find 'Stars Fell On' variants)")
print("-" * 60)
results = engine.search("stars fell", category="all", state_filter="AL")
print(f"Found {len(results)} results:")
for i, result in enumerate(results[:10], 1):
    print(f"{i}. {result['plate_type']} ({result['state']})")
    print(f"   Field: {result['field']}")
    print(f"   Value: {result['value']}")

print("\n" + "=" * 60)
print("Testing complete!")
print("=" * 60)
