"""
Script to add design_variants field to Alabama JSON from CSV data.
CSV columns 3-5 contain design variant descriptions.
"""
import json
import csv
import re

def parse_csv_variants():
    """Parse Alabama CSV and extract design variants for each plate type."""
    csv_path = r"c:\Users\richa\Documents\Code\LicensePlateInformation\data\pending\Plate_Type_Matrix_Vs_Jun_25[1] (1)(Alabama).csv"
    
    # Dictionary to store variants by plate type name
    variants_by_type = {}
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
        
        # Skip first 2 header rows, start from row 3 (index 2)
        for row in rows[2:]:
            if len(row) < 6:
                continue
                
            code_number = row[0].strip()
            plate_type = row[1].strip()
            
            # Skip if no plate type
            if not plate_type:
                continue
            
            # Extract variants from columns 3, 4, 5 (indices 2, 3, 4)
            variants = []
            for col_idx in [2, 3, 4]:
                if col_idx < len(row):
                    variant = row[col_idx].strip()
                    if variant:
                        variants.append(variant)
            
            # Store variants if any found
            if variants:
                # Use plate type name as key
                if plate_type not in variants_by_type:
                    variants_by_type[plate_type] = variants
                else:
                    # If duplicate, extend the list
                    for v in variants:
                        if v not in variants_by_type[plate_type]:
                            variants_by_type[plate_type].append(v)
    
    return variants_by_type

def update_alabama_json(variants_by_type):
    """Update Alabama JSON with design_variants."""
    json_path = r"c:\Users\richa\Documents\Code\LicensePlateInformation\data\states\alabama.json"
    
    # Load Alabama JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        alabama_data = json.load(f)
    
    updates_made = 0
    
    # Update each plate type
    for plate_type in alabama_data.get('plate_types', []):
        type_name = plate_type.get('type_name', '')
        
        # Check if we have variants for this type
        if type_name in variants_by_type:
            # Add design_variants to plate_characteristics
            if 'plate_characteristics' not in plate_type:
                plate_type['plate_characteristics'] = {}
            
            plate_type['plate_characteristics']['design_variants'] = variants_by_type[type_name]
            updates_made += 1
            print(f"✓ Updated '{type_name}' with {len(variants_by_type[type_name])} variants")
        else:
            # Add null design_variants if no variants found
            if 'plate_characteristics' not in plate_type:
                plate_type['plate_characteristics'] = {}
            
            if 'design_variants' not in plate_type['plate_characteristics']:
                plate_type['plate_characteristics']['design_variants'] = None
    
    # Save updated JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(alabama_data, f, indent=2)
    
    print(f"\n✅ Updated {updates_made} plate types with design variants")
    print(f"📄 Saved to: {json_path}")

if __name__ == "__main__":
    print("🔍 Parsing Alabama CSV for design variants...")
    variants = parse_csv_variants()
    
    print(f"\n📊 Found variants for {len(variants)} plate types")
    print("\nSample variants:")
    for plate_type, variant_list in list(variants.items())[:5]:
        print(f"  {plate_type}: {variant_list}")
    
    print("\n💾 Updating Alabama JSON...")
    update_alabama_json(variants)
    print("\n✨ Complete!")
