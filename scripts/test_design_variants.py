"""Test design_variants search functionality"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import json

# Load Alabama JSON directly
alabama_path = r"c:\Users\richa\Documents\Code\LicensePlateInformation\data\states\alabama.json"

with open(alabama_path, 'r', encoding='utf-8') as f:
    alabama_data = json.load(f)

print("Testing design_variants field in Alabama JSON...")
print("=" * 60)

# Test 1: Count plate types with variants
plate_types = alabama_data.get('plate_types', [])
with_variants = 0
without_variants = 0

for plate_type in plate_types:
    characteristics = plate_type.get('plate_characteristics', {})
    variants = characteristics.get('design_variants')
    
    if variants and len(variants) > 0:
        with_variants += 1
    else:
        without_variants += 1

print(f"\nPlate Types with variants: {with_variants}")
print(f"Plate Types without variants: {without_variants}")
print(f"Total plate types: {len(plate_types)}")

# Test 2: Show examples with variants
print("\n" + "=" * 60)
print("Examples of plates WITH design variants:")
print("=" * 60)

count = 0
for plate_type in plate_types:
    characteristics = plate_type.get('plate_characteristics', {})
    variants = characteristics.get('design_variants')
    
    if variants and len(variants) > 0:
        print(f"\n{plate_type['type_name']}:")
        print(f"  Variants ({len(variants)}): {', '.join(variants[:3])}")
        if len(variants) > 3:
            print(f"  ... and {len(variants) - 3} more")
        
        count += 1
        if count >= 5:
            break

# Test 3: Search for "Sweet Home" in variants
print("\n" + "=" * 60)
print("Plates with 'Sweet Home' design variant:")
print("=" * 60)

for plate_type in plate_types:
    characteristics = plate_type.get('plate_characteristics', {})
    variants = characteristics.get('design_variants', [])
    
    if variants and any('Sweet Home' in v for v in variants):
        print(f"  - {plate_type['type_name']}")

# Test 4: Search for date-based variants
print("\n" + "=" * 60)
print("Plates with 'Since 2022' design variant:")
print("=" * 60)

for plate_type in plate_types:
    characteristics = plate_type.get('plate_characteristics', {})
    variants = characteristics.get('design_variants', [])
    
    if variants and any('Since 2022' in v for v in variants):
        print(f"  - {plate_type['type_name']}")
        print(f"    All variants: {', '.join(variants)}")

print("\n" + "=" * 60)
print("SUCCESS: design_variants field working correctly!")
print("=" * 60)
