"""
Live Search Testing Script - Test the enhanced search functionality
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from gui.utils.json_search_engine import JSONSearchEngine


def test_search():
    """Test various search scenarios"""
    
    # Initialize search engine
    engine = JSONSearchEngine(data_directory="data/states")
    
    print("=" * 80)
    print("SEARCH ENHANCEMENT TEST")
    print("=" * 80)
    
    # Test 1: All states available
    print("\n[TEST 1] All Available States:")
    all_states = engine.get_all_state_codes()
    print(f"Total jurisdictions: {len(all_states)}")
    print(f"States: {', '.join(sorted(all_states)[:10])}... (showing first 10)")
    
    # Test 2: Search for O vs 0 rules
    print("\n[TEST 2] Search for 'O vs 0' rules:")
    results = engine.search(query="zero for o", category="handling_rules", state_filter=None)
    print(f"Found {len(results)} results")
    for result in results[:5]:  # Show first 5
        print(f"  {result['state']}: {result['field']} = {result['value'][:60]}...")
    
    # Test 3: Search for stacked characters
    print("\n[TEST 3] Search for 'X2' in stacked characters:")
    results = engine.search(query="X2", category="handling_rules", state_filter=None)
    print(f"Found {len(results)} results")
    for result in results[:5]:
        print(f"  {result['state']}: {result['field']} = {result['value'][:80]}...")
    
    # Test 4: Search in specific state (Alabama)
    print("\n[TEST 4] Search 'stacked' in Alabama only:")
    results = engine.search(query="stacked", category="handling_rules", state_filter="AL")
    print(f"Found {len(results)} results")
    for result in results:
        print(f"  {result['field']} = {result['value'][:80]}...")
    
    # Test 5: Search restrictions
    print("\n[TEST 5] Search 'does not allow' in restrictions:")
    results = engine.search(query="does not allow", category="restrictions", state_filter=None)
    print(f"Found {len(results)} results")
    for result in results[:5]:
        print(f"  {result['state']}: {result['field']} = {result['value'][:60]}...")
    
    # Test 6: Search processing rules
    print("\n[TEST 6] Search 'vertical' in processing:")
    results = engine.search(query="vertical", category="processing", state_filter=None)
    print(f"Found {len(results)} results")
    for result in results[:5]:
        print(f"  {result['state']}: {result['field']} = {result['value'][:60]}...")
    
    # Test 7: Search all fields
    print("\n[TEST 7] Search 'Heart' in all fields:")
    results = engine.search(query="Heart", category="all", state_filter=None)
    print(f"Found {len(results)} results")
    for result in results[:3]:
        print(f"  {result['state']}: {result['field']} = {result['value'][:60]}...")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    test_search()
