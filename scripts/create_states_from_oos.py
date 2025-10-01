#!/usr/bin/env python3
"""
Create state JSON files based on OOS.txt character usage information
Generates comprehensive state files with O/0 usage patterns
"""

import json
import os
from pathlib import Path

# Complete state information
STATE_INFO = {
    # No O states (already created some)
    'connecticut': {'name': 'Connecticut', 'abbrev': 'CT', 'slogan': 'Constitution State'},
    'hawaii': {'name': 'Hawaii', 'abbrev': 'HI', 'slogan': 'Aloha State'},
    'idaho': {'name': 'Idaho', 'abbrev': 'ID', 'slogan': 'Gem State'},
    'kansas': {'name': 'Kansas', 'abbrev': 'KS', 'slogan': 'Sunflower State'},
    'michigan': {'name': 'Michigan', 'abbrev': 'MI', 'slogan': 'Great Lakes State'},
    'minnesota': {'name': 'Minnesota', 'abbrev': 'MN', 'slogan': 'Land of 10,000 Lakes'},
    'missouri': {'name': 'Missouri', 'abbrev': 'MO', 'slogan': 'Show Me State'},
    'montana': {'name': 'Montana', 'abbrev': 'MT', 'slogan': 'Big Sky Country'},
    'nebraska': {'name': 'Nebraska', 'abbrev': 'NE', 'slogan': 'Cornhusker State'},
    'nevada': {'name': 'Nevada', 'abbrev': 'NV', 'slogan': 'Silver State'},
    'new_jersey': {'name': 'New Jersey', 'abbrev': 'NJ', 'slogan': 'Garden State'},
    'new_mexico': {'name': 'New Mexico', 'abbrev': 'NM', 'slogan': 'Land of Enchantment'},
    'utah': {'name': 'Utah', 'abbrev': 'UT', 'slogan': 'Beehive State'},
    
    # O with letters states
    'alaska': {'name': 'Alaska', 'abbrev': 'AK', 'slogan': 'Last Frontier'},
    'arkansas': {'name': 'Arkansas', 'abbrev': 'AR', 'slogan': 'Natural State'},
    'colorado': {'name': 'Colorado', 'abbrev': 'CO', 'slogan': 'Centennial State'},
    'delaware': {'name': 'Delaware', 'abbrev': 'DE', 'slogan': 'First State'},
    'illinois': {'name': 'Illinois', 'abbrev': 'IL', 'slogan': 'Prairie State'},
    'indiana': {'name': 'Indiana', 'abbrev': 'IN', 'slogan': 'Hoosier State'},
    'iowa': {'name': 'Iowa', 'abbrev': 'IA', 'slogan': 'Hawkeye State'},
    'louisiana': {'name': 'Louisiana', 'abbrev': 'LA', 'slogan': 'Pelican State'},
    'massachusetts': {'name': 'Massachusetts', 'abbrev': 'MA', 'slogan': 'Bay State'},
    'maryland': {'name': 'Maryland', 'abbrev': 'MD', 'slogan': 'Old Line State'},
    'mississippi': {'name': 'Mississippi', 'abbrev': 'MS', 'slogan': 'Magnolia State'},
    'north_dakota': {'name': 'North Dakota', 'abbrev': 'ND', 'slogan': 'Peace Garden State'},
    'ohio': {'name': 'Ohio', 'abbrev': 'OH', 'slogan': 'Buckeye State'},
    'oklahoma': {'name': 'Oklahoma', 'abbrev': 'OK', 'slogan': 'Sooner State'},
    'oregon': {'name': 'Oregon', 'abbrev': 'OR', 'slogan': 'Beaver State'},
    'puerto_rico': {'name': 'Puerto Rico', 'abbrev': 'PR', 'slogan': 'Island of Enchantment'},
    'rhode_island': {'name': 'Rhode Island', 'abbrev': 'RI', 'slogan': 'Ocean State'},
    'virginia': {'name': 'Virginia', 'abbrev': 'VA', 'slogan': 'Old Dominion'},
    'washington': {'name': 'Washington', 'abbrev': 'WA', 'slogan': 'Evergreen State'},
    
    # O only on personalized
    'arizona': {'name': 'Arizona', 'abbrev': 'AZ', 'slogan': 'Grand Canyon State'},
    'kentucky': {'name': 'Kentucky', 'abbrev': 'KY', 'slogan': 'Bluegrass State'},
    'maine': {'name': 'Maine', 'abbrev': 'ME', 'slogan': 'Pine Tree State'},
    'new_hampshire': {'name': 'New Hampshire', 'abbrev': 'NH', 'slogan': 'Live Free or Die'}
}

def create_state_json(state_key, state_data, usage_type, special_notes=""):
    """Create JSON for a state based on its O/0 usage type"""
    
    base_template = {
        "name": state_data['name'],
        "abbreviation": state_data['abbrev'],
        "slogan": state_data['slogan'],
        "primary_colors": ["#FFFFFF", "#000000"],
        "processing_metadata": {
            "description": f"Official {state_data['name']} DMV processing rules and validation requirements",
            "global_rules": {
                "font_changes": "Information needed - check historical changes",
                "code_system": "Information needed - research plate type code system"
            }
        },
        "plate_types": []
    }
    
    # Configure based on usage type
    if usage_type == "no_o":
        base_template.update({
            "uses_zero_for_o": True,
            "allows_letter_o": False,
            "zero_is_slashed": False,
            "notes": f"{state_data['name']} does not use the letter 'O' on standard plates. Only the number zero '0' is used to avoid confusion. Source: OOS.txt compilation - requires verification with official DMV documentation."
        })
        base_template["processing_metadata"]["global_rules"]["character_restrictions"] = "Does not use letter 'O' on standard plates - only number zero '0'"
        
    elif usage_type == "o_with_letters":
        base_template.update({
            "uses_zero_for_o": False,
            "allows_letter_o": True,
            "zero_is_slashed": False,
            "notes": f"{state_data['name']} uses letter 'O' with letters/personalized plates and number '0' with numbers. Standard format varies. Source: OOS.txt compilation - requires verification with official DMV documentation."
        })
        base_template["processing_metadata"]["global_rules"]["character_restrictions"] = "Uses both O and 0 - O with letters, 0 with numbers"
        
    elif usage_type == "o_only_personalized":
        base_template.update({
            "uses_zero_for_o": True,
            "allows_letter_o": False,
            "zero_is_slashed": False,
            "notes": f"{state_data['name']} uses letter 'O' only on personalized/vanity plates. Standard plates use only number zero '0'. Source: OOS.txt compilation - requires verification with official DMV documentation."
        })
        base_template["processing_metadata"]["global_rules"]["character_restrictions"] = "O only on personalized plates; standard uses 0"
    
    if special_notes:
        base_template["notes"] = f"{base_template['notes']} Special note: {special_notes}"
    
    # Add standard passenger plate
    passenger_plate = {
        "type_name": "Passenger Default",
        "pattern": "ABC123",
        "character_count": 6,
        "description": f"{state_data['name']} standard passenger plate",
        "background_color": "#FFFFFF",
        "text_color": "#000000",
        "has_stickers": True,
        "sticker_description": "Month/Year validation stickers",
        "category": "passenger",
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
            "dot_processing_type": "always_standard",
            "dot_dropdown_identifier": None,
            "dot_conditional_rules": None,
            "date_ranges": {"period_1": None, "period_2": None},
            "plate_images_available": None
        },
        "visual_identifier": "",
        "processing_rules": "",
        "requires_prefix": False
    }
    
    base_template["plate_types"].append(passenger_plate)
    
    # Add personalized plate for states that allow O on personalized
    if usage_type in ["o_with_letters", "o_only_personalized"]:
        personalized_plate = {
            "type_name": "Personalized/Vanity",
            "pattern": "CUSTOM",
            "character_count": 8,
            "description": f"{state_data['name']} personalized/vanity plate",
            "background_color": "#FFFFFF",
            "text_color": "#000000",
            "has_stickers": True,
            "sticker_description": "Month/Year validation stickers",
            "category": "specialty",
            "code_number": "1",
            "processing_metadata": {
                "currently_processed": True,
                "requires_prefix": False,
                "requires_suffix": False,
                "character_modifications": "Allows letter O on personalized plates",
                "verify_state_abbreviation": True,
                "visual_identifier": None,
                "vehicle_type_identification": None,
                "all_numeric_plate": False,
                "dot_processing_type": "conditional",
                "dot_dropdown_identifier": "PERSONALIZED_PLATES",
                "dot_conditional_rules": {
                    "plate_type": {
                        "action": "allow_letter_o",
                        "description": "Letter O allowed on personalized plates"
                    }
                },
                "date_ranges": {"period_1": None, "period_2": None},
                "plate_images_available": None
            },
            "visual_identifier": "",
            "processing_rules": "Allows letter O",
            "requires_prefix": False
        }
        base_template["plate_types"].append(personalized_plate)
    
    return base_template

def main():
    base_path = Path(__file__).parent.parent / 'data' / 'states'
    
    # Check which files already exist
    existing_files = {f.stem for f in base_path.glob('*.json')}
    
    print("CREATING STATE JSON FILES FROM OOS.txt INFORMATION")
    print("=" * 55)
    
    created_count = 0
    skipped_count = 0
    
    # No O states
    no_o_states = ['connecticut', 'hawaii', 'idaho', 'kansas', 'michigan', 'minnesota', 
                   'missouri', 'montana', 'nebraska', 'nevada', 'new_jersey', 'new_mexico', 'utah']
    
    for state_key in no_o_states:
        if state_key in existing_files:
            print(f"SKIP: {STATE_INFO[state_key]['name']} (already exists)")
            skipped_count += 1
            continue
            
        json_content = create_state_json(state_key, STATE_INFO[state_key], "no_o")
        
        file_path = base_path / f"{state_key}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(json_content, f, indent=2)
        
        print(f"CREATED: {STATE_INFO[state_key]['name']} ({STATE_INFO[state_key]['abbrev']}) - No O")
        created_count += 1
    
    # O with letters states
    o_with_letters_states = ['alaska', 'arkansas', 'colorado', 'delaware', 'illinois', 'indiana', 
                           'iowa', 'louisiana', 'massachusetts', 'maryland', 'mississippi', 
                           'north_dakota', 'ohio', 'oklahoma', 'oregon', 'puerto_rico', 
                           'rhode_island', 'virginia', 'washington']
    
    for state_key in o_with_letters_states:
        if state_key in existing_files:
            print(f"SKIP: {STATE_INFO[state_key]['name']} (already exists)")
            skipped_count += 1
            continue
            
        json_content = create_state_json(state_key, STATE_INFO[state_key], "o_with_letters")
        
        file_path = base_path / f"{state_key}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(json_content, f, indent=2)
        
        print(f"CREATED: {STATE_INFO[state_key]['name']} ({STATE_INFO[state_key]['abbrev']}) - O with letters")
        created_count += 1
    
    # O only on personalized states
    o_only_personalized_states = ['arizona', 'kentucky', 'maine', 'new_hampshire']
    
    for state_key in o_only_personalized_states:
        if state_key in existing_files:
            print(f"SKIP: {STATE_INFO[state_key]['name']} (already exists)")
            skipped_count += 1
            continue
            
        json_content = create_state_json(state_key, STATE_INFO[state_key], "o_only_personalized")
        
        file_path = base_path / f"{state_key}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(json_content, f, indent=2)
        
        print(f"CREATED: {STATE_INFO[state_key]['name']} ({STATE_INFO[state_key]['abbrev']}) - O only personalized")
        created_count += 1
    
    print(f"\nSUMMARY:")
    print(f"Created: {created_count} new state files")
    print(f"Skipped: {skipped_count} existing files")
    print(f"Total states with O/0 information: {created_count + skipped_count}")
    print(f"\nAll files include:")
    print(f"- Proper O/0 usage flags based on OOS.txt")
    print(f"- Basic passenger plate template")
    print(f"- Personalized plate info where applicable")
    print(f"- Comprehensive DOT processing metadata")
    print(f"- Source attribution and verification notes")

if __name__ == '__main__':
    main()