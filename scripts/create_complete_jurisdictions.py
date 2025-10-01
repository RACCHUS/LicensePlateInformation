#!/usr/bin/env python3
"""
Complete Missing Jurisdictions for License Plate Recognition System
Creates JSON files for missing US states, territories, Canadian provinces, and government services
"""

import json
import os
from pathlib import Path

# Complete list of all US states
ALL_US_STATES = {
    'alabama': {'name': 'Alabama', 'abbrev': 'AL', 'slogan': 'Heart of Dixie'},
    'alaska': {'name': 'Alaska', 'abbrev': 'AK', 'slogan': 'Last Frontier'},
    'arizona': {'name': 'Arizona', 'abbrev': 'AZ', 'slogan': 'Grand Canyon State'},
    'arkansas': {'name': 'Arkansas', 'abbrev': 'AR', 'slogan': 'Natural State'},
    'california': {'name': 'California', 'abbrev': 'CA', 'slogan': 'Golden State'},
    'colorado': {'name': 'Colorado', 'abbrev': 'CO', 'slogan': 'Centennial State'},
    'connecticut': {'name': 'Connecticut', 'abbrev': 'CT', 'slogan': 'Constitution State'},
    'delaware': {'name': 'Delaware', 'abbrev': 'DE', 'slogan': 'First State'},
    'florida': {'name': 'Florida', 'abbrev': 'FL', 'slogan': 'Sunshine State'},
    'georgia': {'name': 'Georgia', 'abbrev': 'GA', 'slogan': 'Peach State'},
    'hawaii': {'name': 'Hawaii', 'abbrev': 'HI', 'slogan': 'Aloha State'},
    'idaho': {'name': 'Idaho', 'abbrev': 'ID', 'slogan': 'Gem State'},
    'illinois': {'name': 'Illinois', 'abbrev': 'IL', 'slogan': 'Prairie State'},
    'indiana': {'name': 'Indiana', 'abbrev': 'IN', 'slogan': 'Hoosier State'},
    'iowa': {'name': 'Iowa', 'abbrev': 'IA', 'slogan': 'Hawkeye State'},
    'kansas': {'name': 'Kansas', 'abbrev': 'KS', 'slogan': 'Sunflower State'},
    'kentucky': {'name': 'Kentucky', 'abbrev': 'KY', 'slogan': 'Bluegrass State'},
    'louisiana': {'name': 'Louisiana', 'abbrev': 'LA', 'slogan': 'Pelican State'},
    'maine': {'name': 'Maine', 'abbrev': 'ME', 'slogan': 'Pine Tree State'},
    'maryland': {'name': 'Maryland', 'abbrev': 'MD', 'slogan': 'Old Line State'},
    'massachusetts': {'name': 'Massachusetts', 'abbrev': 'MA', 'slogan': 'Bay State'},
    'michigan': {'name': 'Michigan', 'abbrev': 'MI', 'slogan': 'Great Lakes State'},
    'minnesota': {'name': 'Minnesota', 'abbrev': 'MN', 'slogan': 'Land of 10,000 Lakes'},
    'mississippi': {'name': 'Mississippi', 'abbrev': 'MS', 'slogan': 'Magnolia State'},
    'missouri': {'name': 'Missouri', 'abbrev': 'MO', 'slogan': 'Show Me State'},
    'montana': {'name': 'Montana', 'abbrev': 'MT', 'slogan': 'Big Sky Country'},
    'nebraska': {'name': 'Nebraska', 'abbrev': 'NE', 'slogan': 'Cornhusker State'},
    'nevada': {'name': 'Nevada', 'abbrev': 'NV', 'slogan': 'Silver State'},
    'new_hampshire': {'name': 'New Hampshire', 'abbrev': 'NH', 'slogan': 'Live Free or Die'},
    'new_jersey': {'name': 'New Jersey', 'abbrev': 'NJ', 'slogan': 'Garden State'},
    'new_mexico': {'name': 'New Mexico', 'abbrev': 'NM', 'slogan': 'Land of Enchantment'},
    'new_york': {'name': 'New York', 'abbrev': 'NY', 'slogan': 'Empire State'},
    'north_carolina': {'name': 'North Carolina', 'abbrev': 'NC', 'slogan': 'Tar Heel State'},
    'north_dakota': {'name': 'North Dakota', 'abbrev': 'ND', 'slogan': 'Peace Garden State'},
    'ohio': {'name': 'Ohio', 'abbrev': 'OH', 'slogan': 'Buckeye State'},
    'oklahoma': {'name': 'Oklahoma', 'abbrev': 'OK', 'slogan': 'Sooner State'},
    'oregon': {'name': 'Oregon', 'abbrev': 'OR', 'slogan': 'Beaver State'},
    'pennsylvania': {'name': 'Pennsylvania', 'abbrev': 'PA', 'slogan': 'Keystone State'},
    'rhode_island': {'name': 'Rhode Island', 'abbrev': 'RI', 'slogan': 'Ocean State'},
    'south_carolina': {'name': 'South Carolina', 'abbrev': 'SC', 'slogan': 'Palmetto State'},
    'south_dakota': {'name': 'South Dakota', 'abbrev': 'SD', 'slogan': 'Mount Rushmore State'},
    'tennessee': {'name': 'Tennessee', 'abbrev': 'TN', 'slogan': 'Volunteer State'},
    'texas': {'name': 'Texas', 'abbrev': 'TX', 'slogan': 'Lone Star State'},
    'utah': {'name': 'Utah', 'abbrev': 'UT', 'slogan': 'Beehive State'},
    'vermont': {'name': 'Vermont', 'abbrev': 'VT', 'slogan': 'Green Mountain State'},
    'virginia': {'name': 'Virginia', 'abbrev': 'VA', 'slogan': 'Old Dominion'},
    'washington': {'name': 'Washington', 'abbrev': 'WA', 'slogan': 'Evergreen State'},
    'west_virginia': {'name': 'West Virginia', 'abbrev': 'WV', 'slogan': 'Mountain State'},
    'wisconsin': {'name': 'Wisconsin', 'abbrev': 'WI', 'slogan': 'Badger State'},
    'wyoming': {'name': 'Wyoming', 'abbrev': 'WY', 'slogan': 'Equality State'}
}

# US Territories
US_TERRITORIES = {
    'puerto_rico': {'name': 'Puerto Rico', 'abbrev': 'PR', 'slogan': 'Island of Enchantment'},
    'guam': {'name': 'Guam', 'abbrev': 'GU', 'slogan': 'Where America\'s Day Begins'},
    'us_virgin_islands': {'name': 'US Virgin Islands', 'abbrev': 'VI', 'slogan': 'American Paradise'},
    'american_samoa': {'name': 'American Samoa', 'abbrev': 'AS', 'slogan': 'Heart of Polynesia'},
    'northern_mariana_islands': {'name': 'Northern Mariana Islands', 'abbrev': 'MP', 'slogan': 'Western Pacific Territory'},
    'washington_dc': {'name': 'Washington DC', 'abbrev': 'DC', 'slogan': 'Nation\'s Capital'}
}

# Canadian Provinces
CANADIAN_PROVINCES = {
    'alberta': {'name': 'Alberta', 'abbrev': 'AB', 'slogan': 'Wild Rose Country'},
    'ontario': {'name': 'Ontario', 'abbrev': 'ON', 'slogan': 'Yours to Discover'}
}

# Government Services
GOVERNMENT_SERVICES = {
    'us_government': {'name': 'US Government', 'abbrev': 'US', 'slogan': 'Federal Plates'},
    'diplomatic': {'name': 'Diplomatic Corps', 'abbrev': 'DPL', 'slogan': 'International Diplomatic'}
}

def create_jurisdiction_json(key, data, jurisdiction_type, o_usage_pattern="unknown"):
    """Create JSON for any jurisdiction based on type"""
    
    base_template = {
        "name": data['name'],
        "abbreviation": data['abbrev'],
        "slogan": data['slogan'],
        "primary_colors": ["#FFFFFF", "#000000"],
        "processing_metadata": {
            "description": f"Official {data['name']} processing rules and validation requirements",
            "global_rules": {
                "font_changes": "Information needed - research historical changes",
                "code_system": "Information needed - research plate type code system"
            }
        },
        "plate_types": []
    }
    
    # Set O/0 usage based on pattern
    if o_usage_pattern == "no_o":
        base_template.update({
            "uses_zero_for_o": True,
            "allows_letter_o": False,
            "zero_is_slashed": False
        })
        base_template["processing_metadata"]["global_rules"]["character_restrictions"] = "Does not use letter 'O' - only number zero '0'"
        base_template["notes"] = f"{data['name']} uses only number zero '0', no letter 'O' on plates. Requires verification with official documentation."
    elif o_usage_pattern == "o_with_letters":
        base_template.update({
            "uses_zero_for_o": False,
            "allows_letter_o": True,
            "zero_is_slashed": False
        })
        base_template["processing_metadata"]["global_rules"]["character_restrictions"] = "Uses both O and 0 - O with letters, 0 with numbers"
        base_template["notes"] = f"{data['name']} uses letter 'O' with letters and number '0' with numbers. Requires verification with official documentation."
    else:
        base_template.update({
            "uses_zero_for_o": False,
            "allows_letter_o": True,
            "zero_is_slashed": False
        })
        base_template["processing_metadata"]["global_rules"]["character_restrictions"] = "Unknown O/0 usage pattern - requires research"
        base_template["notes"] = f"{data['name']} O/0 character usage pattern unknown. Requires research with official documentation."
    
    # Add jurisdiction-specific notes
    if jurisdiction_type == "canadian":
        base_template["notes"] += f" Canadian province - may have different format standards than US states."
        base_template["processing_metadata"]["global_rules"]["international"] = "Canadian province with different standards"
    elif jurisdiction_type == "territory":
        base_template["notes"] += f" US Territory - follows federal standards with local variations."
        base_template["processing_metadata"]["global_rules"]["territory_status"] = "US Territory with federal oversight"
    elif jurisdiction_type == "government":
        base_template["notes"] += f" Government service plates - special federal formatting and security features."
        base_template["processing_metadata"]["global_rules"]["security_level"] = "Federal government plates with enhanced security"
    
    # Add basic passenger plate
    passenger_plate = {
        "type_name": "Standard Issue" if jurisdiction_type == "government" else "Passenger Default",
        "pattern": "ABC123" if jurisdiction_type != "government" else "G123456",
        "character_count": 6,
        "description": f"{data['name']} standard {'government' if jurisdiction_type == 'government' else 'passenger'} plate",
        "background_color": "#FFFFFF",
        "text_color": "#000000",
        "has_stickers": True,
        "sticker_description": "Validation stickers" if jurisdiction_type != "canadian" else "Registration validation",
        "category": "government" if jurisdiction_type == "government" else "passenger",
        "code_number": "0",
        "processing_metadata": {
            "currently_processed": True,
            "requires_prefix": False,
            "requires_suffix": False,
            "character_modifications": None,
            "verify_state_abbreviation": True,
            "visual_identifier": None,
            "vehicle_type_identification": None,
            "all_numeric_plate": False,
            "dot_processing_type": "never_standard" if jurisdiction_type == "government" else "always_standard",
            "dot_dropdown_identifier": "GOVERNMENT_PLATES" if jurisdiction_type == "government" else None,
            "dot_conditional_rules": None,
            "date_ranges": {"period_1": None, "period_2": None},
            "plate_images_available": None
        },
        "visual_identifier": "",
        "processing_rules": "Special government handling" if jurisdiction_type == "government" else "",
        "requires_prefix": False
    }
    
    base_template["plate_types"].append(passenger_plate)
    
    return base_template

def main():
    base_path = Path(__file__).parent.parent / 'data' / 'states'
    
    # Check which files already exist
    existing_files = {f.stem for f in base_path.glob('*.json')}
    
    print("CREATING MISSING JURISDICTIONS FOR COMPLETE COVERAGE")
    print("=" * 55)
    
    created_count = 0
    skipped_count = 0
    
    print("\nCHECKING US STATES (50 total):")
    print("-" * 35)
    missing_states = []
    for state_key, state_data in ALL_US_STATES.items():
        if state_key not in existing_files:
            missing_states.append((state_key, state_data))
            print(f"MISSING: {state_data['name']} ({state_data['abbrev']})")
        else:
            print(f"EXISTS:  {state_data['name']} ({state_data['abbrev']})")
            skipped_count += 1
    
    print(f"\nMissing US States: {len(missing_states)}")
    
    # Create missing US states
    for state_key, state_data in missing_states:
        # Use default O/0 pattern for new states
        json_content = create_jurisdiction_json(state_key, state_data, "state", "o_with_letters")
        
        file_path = base_path / f"{state_key}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(json_content, f, indent=2)
        
        print(f"CREATED: {state_data['name']} ({state_data['abbrev']})")
        created_count += 1
    
    print("\nCHECKING US TERRITORIES:")
    print("-" * 25)
    for territory_key, territory_data in US_TERRITORIES.items():
        if territory_key not in existing_files:
            json_content = create_jurisdiction_json(territory_key, territory_data, "territory", "o_with_letters")
            
            file_path = base_path / f"{territory_key}.json"
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(json_content, f, indent=2)
            
            print(f"CREATED: {territory_data['name']} ({territory_data['abbrev']})")
            created_count += 1
        else:
            print(f"EXISTS:  {territory_data['name']} ({territory_data['abbrev']})")
            skipped_count += 1
    
    print("\nCREATING CANADIAN PROVINCES:")
    print("-" * 30)
    for province_key, province_data in CANADIAN_PROVINCES.items():
        if province_key not in existing_files:
            json_content = create_jurisdiction_json(province_key, province_data, "canadian", "o_with_letters")
            
            file_path = base_path / f"{province_key}.json"
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(json_content, f, indent=2)
            
            print(f"CREATED: {province_data['name']} ({province_data['abbrev']})")
            created_count += 1
        else:
            print(f"EXISTS:  {province_data['name']} ({province_data['abbrev']})")
            skipped_count += 1
    
    print("\nCREATING GOVERNMENT SERVICES:")
    print("-" * 30)
    for gov_key, gov_data in GOVERNMENT_SERVICES.items():
        if gov_key not in existing_files:
            json_content = create_jurisdiction_json(gov_key, gov_data, "government", "unknown")
            
            file_path = base_path / f"{gov_key}.json"
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(json_content, f, indent=2)
            
            print(f"CREATED: {gov_data['name']} ({gov_data['abbrev']})")
            created_count += 1
        else:
            print(f"EXISTS:  {gov_data['name']} ({gov_data['abbrev']})")
            skipped_count += 1
    
    print(f"\nFINAL SUMMARY:")
    print("-" * 15)
    print(f"New files created: {created_count}")
    print(f"Existing files: {skipped_count}")
    print(f"Total jurisdictions: {created_count + skipped_count}")
    print(f"\nComplete coverage now includes:")
    print(f"✅ All 50 US States")
    print(f"✅ All US Territories (PR, GU, VI, AS, MP, DC)")
    print(f"✅ Major Canadian Provinces (AB, ON)")
    print(f"✅ Government Services (Federal, Diplomatic)")

if __name__ == '__main__':
    main()