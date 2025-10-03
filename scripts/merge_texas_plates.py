"""
Merge parsed Texas plate types into the texas.json file
"""
import json

def merge_texas_plates():
    # Read the existing texas.json
    with open(r'c:\Users\richa\Documents\Code\LicensePlateInformation\data\states\texas.json', 'r', encoding='utf-8') as f:
        texas_data = json.load(f)
    
    # Read the parsed plate types
    with open(r'c:\Users\richa\Documents\Code\LicensePlateInformation\data\pending\texas_plate_types_parsed.json', 'r', encoding='utf-8') as f:
        parsed_plates = json.load(f)
    
    # Get existing plate type names to avoid duplicates
    existing_names = {pt['type_name'].lower() for pt in texas_data['plate_types']}
    
    # Add new plate types that don't already exist
    new_count = 0
    for plate in parsed_plates:
        if plate['type_name'].lower() not in existing_names:
            texas_data['plate_types'].append(plate)
            new_count += 1
    
    # Write back to texas.json
    with open(r'c:\Users\richa\Documents\Code\LicensePlateInformation\data\states\texas.json', 'w', encoding='utf-8') as f:
        json.dump(texas_data, f, indent=2)
    
    print(f"Merged {new_count} new plate types into texas.json")
    print(f"Total plate types in texas.json: {len(texas_data['plate_types'])}")
    
    # Show category breakdown
    categories = {}
    for pt in texas_data['plate_types']:
        cat = pt.get('category', 'unknown')
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\nPlate types by category:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count}")

if __name__ == '__main__':
    merge_texas_plates()
