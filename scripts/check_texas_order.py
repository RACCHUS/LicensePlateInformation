"""
Check the order and completeness of Texas plate types
"""
import json

def check_texas_order():
    with open(r'c:\Users\richa\Documents\Code\LicensePlateInformation\data\states\texas.json', 'r', encoding='utf-8') as f:
        texas_data = json.load(f)
    
    plate_types = texas_data['plate_types']
    
    print(f"Total plate types in texas.json: {len(plate_types)}")
    print("\n" + "="*80)
    
    # Check for important special plates mentioned in CSV
    important_plates = [
        "Disabled Veteran",
        "Purple Heart",
        "Antique",
        "Temporary",
        "144/72 Hour Permit",
        "Air Medal",
        "Bronze Star",
        "Silver Star"
    ]
    
    print("\nImportant plate types verification:")
    print("-" * 80)
    for important in important_plates:
        matches = [pt for pt in plate_types if important.lower() in pt['type_name'].lower()]
        if matches:
            print(f"✓ {important}: Found {len(matches)} variant(s)")
            for match in matches[:3]:  # Show first 3
                char_mods = match.get('processing_metadata', {}).get('character_modifications')
                if char_mods:
                    print(f"    - {match['type_name']}: {char_mods}")
                else:
                    print(f"    - {match['type_name']}")
        else:
            print(f"✗ {important}: NOT FOUND")
    
    print("\n" + "="*80)
    print("\nCategory breakdown:")
    print("-" * 80)
    categories = {}
    for pt in plate_types:
        cat = pt.get('category', 'unknown')
        categories[cat] = categories.get(cat, 0) + 1
    
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat:20s}: {count:4d}")
    
    print("\n" + "="*80)
    print("\nPlates with special character modifications:")
    print("-" * 80)
    special_processing = []
    for pt in plate_types:
        char_mods = pt.get('processing_metadata', {}).get('character_modifications')
        if char_mods and char_mods != 'N' and char_mods is not None:
            special_processing.append((pt['type_name'], char_mods))
    
    for name, mods in special_processing[:20]:  # Show first 20
        print(f"  {name:40s}: {mods}")
    
    if len(special_processing) > 20:
        print(f"  ... and {len(special_processing) - 20} more")
    
    print("\n" + "="*80)
    print("\nPlates with visual identifiers:")
    print("-" * 80)
    visual_ids = []
    for pt in plate_types:
        visual_id = pt.get('processing_metadata', {}).get('visual_identifier')
        if visual_id and visual_id not in ['N', None, '']:
            visual_ids.append((pt['type_name'], visual_id))
    
    print(f"Found {len(visual_ids)} plates with visual identifiers")
    for name, vid in visual_ids[:10]:  # Show first 10
        print(f"  {name:40s}: {vid[:60]}...")
    
    if len(visual_ids) > 10:
        print(f"  ... and {len(visual_ids) - 10} more")
    
    print("\n" + "="*80)
    print("\nCollegiate/University plates:")
    print("-" * 80)
    collegiate = [pt for pt in plate_types if pt.get('category') == 'collegiate']
    print(f"Found {len(collegiate)} collegiate plates")
    for pt in collegiate[:15]:
        print(f"  - {pt['type_name']}")
    if len(collegiate) > 15:
        print(f"  ... and {len(collegiate) - 15} more")

if __name__ == '__main__':
    check_texas_order()
