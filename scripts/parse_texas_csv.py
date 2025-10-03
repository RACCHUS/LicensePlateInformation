"""
Parse Texas CSV plate type matrix and generate JSON entries
"""
import csv
import json
import sys

def parse_texas_csv(csv_file):
    """Parse the Texas CSV and extract plate type information"""
    plate_types = []
    
    with open(csv_file, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f)
        
        # Skip header rows
        next(reader)  # Skip first row
        next(reader)  # Skip second row
        next(reader)  # Skip third row (column headers)
        
        for row in reader:
            # Check if plate type column (index 1) has data instead of code number
            if len(row) < 12 or not row[1].strip():
                continue
            
            # Extract data from row - code_number may be empty
            code_number = row[0].strip()
            plate_type = row[1].strip()
            image1 = row[2].strip() if len(row) > 2 else ""
            image2 = row[3].strip() if len(row) > 3 else ""
            image3 = row[4].strip() if len(row) > 4 else ""
            # Column 5 is "Currently being processed"
            currently_processed = row[5].strip() if len(row) > 5 else "N"
            add_prefix = row[6].strip() if len(row) > 6 else "N"
            add_suffix = row[7].strip() if len(row) > 7 else "N"
            omit_add_chars = row[8].strip() if len(row) > 8 else "N"
            verify_state_abbrev = row[9].strip() if len(row) > 9 else "Y"
            visual_identifier = row[10].strip() if len(row) > 10 else ""
            vehicle_type_id = row[11].strip() if len(row) > 11 else "N"
            all_numeric = row[12].strip() if len(row) > 12 else "N"
            
            if not plate_type or currently_processed.upper() != 'Y':
                continue
            
            # Build plate type entry
            plate_entry = {
                "type_name": plate_type,
                "code_number": code_number if code_number else "0",
                "category": determine_category(plate_type),
                "description": f"TX {plate_type} plate",
                "background_color": "#FFFFFF",
                "text_color": "#000000",
                "has_stickers": True,
                "sticker_description": "Month/Year validation stickers",
                "processing_metadata": {
                    "currently_processed": True,
                    "requires_prefix": add_prefix.upper() == 'Y',
                    "requires_suffix": add_suffix.upper() == 'Y',
                    "character_modifications": omit_add_chars if omit_add_chars and omit_add_chars != 'N' else None,
                    "verify_state_abbreviation": verify_state_abbrev.upper() == 'Y',
                    "visual_identifier": visual_identifier if visual_identifier else None,
                    "vehicle_type_identification": vehicle_type_id if vehicle_type_id and vehicle_type_id != 'N' else None,
                    "all_numeric_plate": all_numeric.upper() == 'Y',
                },
                "plate_characteristics": {
                    "variations": []
                }
            }
            
            # Add variations
            if image1:
                plate_entry["plate_characteristics"]["variations"].append(image1)
            if image2:
                plate_entry["plate_characteristics"]["variations"].append(image2)
            if image3:
                plate_entry["plate_characteristics"]["variations"].append(image3)
            
            plate_types.append(plate_entry)
    
    return plate_types

def determine_category(plate_type):
    """Determine the category based on plate type name"""
    plate_lower = plate_type.lower()
    
    if 'motorcycle' in plate_lower or 'mc' in plate_lower:
        return 'motorcycle'
    elif 'trailer' in plate_lower:
        return 'trailer'
    elif 'truck' in plate_lower or 'commercial' in plate_lower:
        return 'commercial'
    elif 'dealer' in plate_lower or 'manufacturer' in plate_lower:
        return 'dealer'
    elif 'temporary' in plate_lower or 'permit' in plate_lower:
        return 'temporary'
    elif 'disabled' in plate_lower or 'veteran' in plate_lower or 'military' in plate_lower:
        return 'military'
    elif 'university' in plate_lower or 'college' in plate_lower or 'collegiate' in plate_lower:
        return 'collegiate'
    elif 'antique' in plate_lower or 'classic' in plate_lower:
        return 'antique'
    elif 'passenger' in plate_lower or 'default' in plate_lower:
        return 'passenger'
    else:
        return 'specialty'

def main():
    csv_file = r'c:\Users\richa\Documents\Code\LicensePlateInformation\data\pending\Plate_Type_Matrix_Vs_Jun_25[1] (1)(Texas).csv'
    output_file = r'c:\Users\richa\Documents\Code\LicensePlateInformation\data\pending\texas_plate_types_parsed.json'
    
    print(f"Parsing {csv_file}...")
    plate_types = parse_texas_csv(csv_file)
    
    print(f"Found {len(plate_types)} plate types")
    
    # Write to JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(plate_types, f, indent=2)
    
    print(f"Wrote parsed data to {output_file}")
    
    # Print summary
    categories = {}
    for pt in plate_types:
        cat = pt['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\nPlate types by category:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count}")

if __name__ == '__main__':
    main()
