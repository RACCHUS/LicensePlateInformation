#!/usr/bin/env python3
"""
Comprehensive Jurisdiction Coverage Report
Shows complete coverage of all US states, territories, Canadian provinces, and government services
"""

import json
from pathlib import Path

def main():
    base_path = Path(__file__).parent.parent / 'data' / 'states'
    state_files = list(base_path.glob('*.json'))
    
    print("COMPLETE JURISDICTION COVERAGE REPORT")
    print("=" * 45)
    print(f"Total jurisdiction files: {len(state_files)}")
    
    # Load and categorize all jurisdictions
    us_states = []
    us_territories = []
    canadian_provinces = []
    government_services = []
    
    for state_file in sorted(state_files):
        with open(state_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        name = data.get('name', 'Unknown')
        abbrev = data.get('abbreviation', 'XX')
        
        # Categorize by type
        if abbrev in ['AB', 'ON']:
            canadian_provinces.append((name, abbrev))
        elif abbrev in ['US', 'DPL']:
            government_services.append((name, abbrev))
        elif abbrev in ['PR', 'GU', 'VI', 'AS', 'MP', 'DC']:
            us_territories.append((name, abbrev))
        else:
            us_states.append((name, abbrev))
    
    print(f"\n🇺🇸 US STATES ({len(us_states)}/50):")
    print("-" * 25)
    for name, abbrev in sorted(us_states):
        print(f"  • {name} ({abbrev})")
    
    print(f"\n🏝️  US TERRITORIES ({len(us_territories)}):")
    print("-" * 30)
    for name, abbrev in sorted(us_territories):
        print(f"  • {name} ({abbrev})")
    
    print(f"\n🇨🇦 CANADIAN PROVINCES ({len(canadian_provinces)}):")
    print("-" * 35)
    for name, abbrev in sorted(canadian_provinces):
        print(f"  • {name} ({abbrev})")
    
    print(f"\n🏛️  GOVERNMENT SERVICES ({len(government_services)}):")
    print("-" * 35)
    for name, abbrev in sorted(government_services):
        print(f"  • {name} ({abbrev})")
    
    print(f"\n📊 COVERAGE SUMMARY:")
    print("-" * 20)
    print(f"✅ US States: {len(us_states)}/50 ({'COMPLETE' if len(us_states) == 50 else 'INCOMPLETE'})")
    print(f"✅ US Territories: {len(us_territories)}/6 ({'COMPLETE' if len(us_territories) == 6 else 'INCOMPLETE'})")
    print(f"✅ Canadian Provinces: {len(canadian_provinces)}/2 (Major provinces)")
    print(f"✅ Government Services: {len(government_services)}/2 (Federal & Diplomatic)")
    print(f"🎯 TOTAL COVERAGE: {len(state_files)} jurisdictions")
    
    # Check if we have all 50 US states
    if len(us_states) == 50:
        print(f"\n🎉 MILESTONE ACHIEVED: Complete 50-state US coverage!")
        
    comprehensive_states = []
    for state_file in state_files:
        with open(state_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        plate_count = len(data.get('plate_types', []))
        if plate_count > 10:
            comprehensive_states.append((data['name'], plate_count))
    
    if comprehensive_states:
        print(f"\n📋 COMPREHENSIVE IMPLEMENTATIONS:")
        print("-" * 35)
        for name, count in sorted(comprehensive_states, key=lambda x: x[1], reverse=True):
            print(f"  • {name}: {count} plate types")

if __name__ == '__main__':
    main()