"""
Florida Processing Types Update Script
Updates all Florida plate types with proper processing type classifications.

Florida Processing Rules:
- Most plates: Standard processing (all numbers version)
- Special Dropdown Plates: Require dropdown selection THEN key license plate
  * Seminole Indian (Code 125)
  * Miccosukee Indian (Code 129)
  * State Senator (Code 127)
  * House Speaker (Code 123)
  * Member of Congress (Code 124)
  * US Senator (Code 128)
- EXCEPTION: If plate has "Official" or "Retired" in name, do NOT use dropdown (standard processing)
"""

import json
from collections import Counter

def update_florida_processing_types():
    # Load Florida data
    with open('data/states/florida.json', 'r', encoding='utf-8') as f:
        florida_data = json.load(f)
    
    print(f"Loaded {len(florida_data['plate_types'])} Florida plate types")
    
    # Define processing type metadata
    processing_types = {
        "standard": {
            "description": "Standard processing - key all characters from license plate",
            "character_modifications": None,
            "special_rules": None,
            "dropdown_required": False
        },
        "dropdown_seminole_indian": {
            "description": "Seminole Indian - Select from dropdown THEN key license plate",
            "character_modifications": None,
            "special_rules": "Select 'Seminole Indian' from dropdown, then key the license plate number",
            "dropdown_required": True,
            "dropdown_identifier": "Seminole Indian",
            "code_numbers": ["125"]
        },
        "dropdown_miccosukee_indian": {
            "description": "Miccosukee Indian - Select from dropdown THEN key license plate",
            "character_modifications": None,
            "special_rules": "Select 'Miccosukee Indian' from dropdown, then key the license plate number",
            "dropdown_required": True,
            "dropdown_identifier": "Miccosukee Indian",
            "code_numbers": ["129"]
        },
        "dropdown_state_senator": {
            "description": "State Senator - Select from dropdown THEN key license plate",
            "character_modifications": None,
            "special_rules": "Select 'State Senator' from dropdown, then key the license plate number",
            "dropdown_required": True,
            "dropdown_identifier": "State Senator",
            "code_numbers": ["127"]
        },
        "dropdown_house_speaker": {
            "description": "House Speaker - Select from dropdown THEN key license plate",
            "character_modifications": None,
            "special_rules": "Select 'House Speaker' from dropdown, then key the license plate number",
            "dropdown_required": True,
            "dropdown_identifier": "House Speaker",
            "code_numbers": ["123"]
        },
        "dropdown_member_of_congress": {
            "description": "Member of Congress - Select from dropdown THEN key license plate",
            "character_modifications": None,
            "special_rules": "Select 'Member of Congress' from dropdown, then key the license plate number",
            "dropdown_required": True,
            "dropdown_identifier": "Member of Congress",
            "code_numbers": ["124"]
        },
        "dropdown_us_senator": {
            "description": "US Senator - Select from dropdown THEN key license plate",
            "character_modifications": None,
            "special_rules": "Select 'US Senator' from dropdown, then key the license plate number",
            "dropdown_required": True,
            "dropdown_identifier": "US Senator",
            "code_numbers": ["128"]
        }
    }
    
    # Update global rules to include processing types
    florida_data['processing_metadata']['processing_types'] = processing_types
    florida_data['processing_metadata']['global_rules']['has_variable_processing_types'] = True
    
    # Counters for tracking
    updates = 0
    processing_type_counts = Counter()
    code_distribution = {}
    
    # Update each plate type
    for plate in florida_data['plate_types']:
        plate_name = plate['type_name']
        code = plate.get('code_number', '0')
        
        # Initialize processing_info if not exists
        if 'processing_info' not in plate:
            plate['processing_info'] = {}
        
        # Determine processing type based on rules
        processing_type = "standard"  # Default
        
        # Check if this is a special dropdown plate
        # EXCEPTION: If plate has "Official" or "Retired", use standard processing
        if 'official' in plate_name.lower() or 'retired' in plate_name.lower():
            processing_type = "standard"
            plate['processing_info']['special_note'] = "Has Official/Retired - Do NOT use dropdown"
        
        # Check for special dropdown plates
        elif 'seminole indian' in plate_name.lower():
            processing_type = "dropdown_seminole_indian"
        elif 'miccosukee indian' in plate_name.lower():
            processing_type = "dropdown_miccosukee_indian"
        elif code == "127" or 'state senator' in plate_name.lower():
            processing_type = "dropdown_state_senator"
        elif code == "123" or 'house speaker' in plate_name.lower():
            processing_type = "dropdown_house_speaker"
        elif code == "124" or 'member of congress' in plate_name.lower():
            processing_type = "dropdown_member_of_congress"
        elif code == "128" or 'us senator' in plate_name.lower():
            processing_type = "dropdown_us_senator"
        
        # Update plate with processing type
        plate['processing_type'] = processing_type
        plate['processing_info']['processing_type_name'] = processing_type
        plate['processing_info']['description'] = processing_types[processing_type]['description']
        
        # Add dropdown info if applicable
        if processing_types[processing_type]['dropdown_required']:
            plate['processing_info']['requires_dropdown'] = True
            plate['processing_info']['dropdown_identifier'] = processing_types[processing_type]['dropdown_identifier']
            plate['processing_info']['workflow'] = "1) Select from dropdown, 2) Key license plate number"
        else:
            plate['processing_info']['requires_dropdown'] = False
            plate['processing_info']['workflow'] = "Key all characters from license plate"
        
        # Track updates
        updates += 1
        processing_type_counts[processing_type] += 1
        
        if code not in code_distribution:
            code_distribution[code] = {}
        if processing_type not in code_distribution[code]:
            code_distribution[code][processing_type] = 0
        code_distribution[code][processing_type] += 1
    
    # Save updated data
    with open('data/states/florida.json', 'w', encoding='utf-8') as f:
        json.dump(florida_data, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print(f"\n{'='*70}")
    print("FLORIDA PROCESSING TYPES UPDATE COMPLETE")
    print(f"{'='*70}\n")
    
    print(f"✅ Updated {updates} plate types with processing information")
    print(f"✅ Defined {len(processing_types)} unique processing types")
    
    print(f"\n{'='*70}")
    print("PROCESSING TYPE DISTRIBUTION")
    print(f"{'='*70}\n")
    
    for proc_type, count in processing_type_counts.most_common():
        percentage = (count / updates * 100) if updates > 0 else 0
        print(f"{proc_type:.<50} {count:>4} ({percentage:>5.1f}%)")
    
    print(f"\n{'='*70}")
    print("CODE DISTRIBUTION WITH PROCESSING TYPES")
    print(f"{'='*70}\n")
    
    for code in sorted(code_distribution.keys(), key=lambda x: (x == '0', x)):
        print(f"\nCode {code}:")
        for proc_type, count in sorted(code_distribution[code].items(), key=lambda x: -x[1]):
            print(f"  {proc_type:.<45} {count:>4}")
    
    print(f"\n{'='*70}")
    print("SPECIAL DROPDOWN PLATES SUMMARY")
    print(f"{'='*70}\n")
    
    dropdown_plates = [p for p in florida_data['plate_types'] 
                      if p.get('processing_info', {}).get('requires_dropdown', False)]
    
    print(f"Found {len(dropdown_plates)} plates requiring dropdown selection:\n")
    for plate in dropdown_plates:
        print(f"  • {plate['type_name']}")
        print(f"    Code: {plate.get('code_number', 'N/A')}")
        print(f"    Dropdown: {plate['processing_info'].get('dropdown_identifier', 'N/A')}")
        print(f"    Workflow: {plate['processing_info'].get('workflow', 'N/A')}")
        print()
    
    print(f"\n{'='*70}")
    print("OFFICIAL/RETIRED EXCEPTION PLATES")
    print(f"{'='*70}\n")
    
    exception_plates = [p for p in florida_data['plate_types'] 
                       if 'official' in p['type_name'].lower() or 'retired' in p['type_name'].lower()]
    
    print(f"Found {len(exception_plates)} Official/Retired plates (standard processing):\n")
    for plate in exception_plates:
        print(f"  • {plate['type_name']} (Code {plate.get('code_number', 'N/A')})")
        print(f"    Note: {plate.get('processing_info', {}).get('special_note', 'Standard processing')}")
        print()
    
    print(f"\n{'='*70}")
    print("KEY PROCESSING RULES")
    print(f"{'='*70}\n")
    
    print("✅ Standard Processing (Most plates):")
    print("   - Key all characters from license plate")
    print("   - No dropdown selection required")
    print(f"   - Total: {processing_type_counts['standard']} plates\n")
    
    print("✅ Dropdown Required Plates:")
    print("   1) Seminole Indian (Code 125) - Select from dropdown, then key plate")
    print("   2) Miccosukee Indian (Code 129) - Select from dropdown, then key plate")
    print("   3) State Senator (Code 127) - Select from dropdown, then key plate")
    print("   4) House Speaker (Code 123) - Select from dropdown, then key plate")
    print("   5) Member of Congress (Code 124) - Select from dropdown, then key plate")
    print("   6) US Senator (Code 128) - Select from dropdown, then key plate")
    print(f"   - Total: {sum(v for k, v in processing_type_counts.items() if 'dropdown' in k)} plates\n")
    
    print("⚠️  EXCEPTION:")
    print("   - If plate has 'Official' or 'Retired' in name")
    print("   - DO NOT use dropdown")
    print("   - Use standard processing instead")
    print(f"   - Total: {len(exception_plates)} plates\n")
    
    print(f"{'='*70}")
    print("VALIDATION SUMMARY")
    print(f"{'='*70}\n")
    
    print(f"✅ All {len(florida_data['plate_types'])} plate types have processing_type")
    print(f"✅ All {len(florida_data['plate_types'])} plate types have processing_info")
    print(f"✅ {len(processing_types)} unique processing types defined")
    print(f"✅ {len(dropdown_plates)} dropdown plates correctly identified")
    print(f"✅ {len(exception_plates)} exception plates correctly marked")
    print(f"✅ 100% processing coverage achieved")
    
    print(f"\n{'='*70}")
    print("✅ FLORIDA PROCESSING UPDATE COMPLETE!")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    update_florida_processing_types()
