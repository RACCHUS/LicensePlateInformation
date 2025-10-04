"""
Universal State CSV Parser
Parses any state's DMV plate type matrix CSV and generates JSON entries
"""
import csv
import json
import sys
import os
import re
from pathlib import Path

def extract_character_rules(first_row):
    """Extract character handling rules from the first row of the CSV"""
    rules = {
        "uses_zero_for_o": False,
        "letter_restrictions": [],
        "font_changes": None,
        "code_system": None,
        "special_notes": []
    }
    
    # The passenger plate default info is typically in columns 5+ of first row
    info_text = ' '.join([col for col in first_row[5:] if col.strip()])
    
    if not info_text:
        return rules
    
    info_lower = info_text.lower()
    
    # Check for O vs 0 usage
    if 'does not use' in info_lower and ('letter o' in info_lower or 'letter "o"' in info_lower):
        rules["uses_zero_for_o"] = True
        rules["special_notes"].append("State does not use letter 'O', only number '0'")
    elif 'uses both' in info_lower and ('letter o' in info_lower or 'letter "o"' in info_lower):
        rules["uses_zero_for_o"] = False
        rules["special_notes"].append("State uses both letter 'O' and number '0'")
    
    # Extract letter restrictions (I, O, Q patterns)
    if 'not used' in info_lower or 'omit' in info_lower:
        # Look for patterns like "I, O, & Q are not used"
        letter_pattern = re.findall(r'letters?\s+([IOQ\s,&]+)\s+(?:are\s+)?not\s+used', info_text, re.IGNORECASE)
        if letter_pattern:
            letters = re.findall(r'[IOQ]', letter_pattern[0], re.IGNORECASE)
            rules["letter_restrictions"] = list(set([l.upper() for l in letters]))
            rules["special_notes"].append(f"Letters {', '.join(rules['letter_restrictions'])} are not used in certain positions")
    
    # Font changes
    if 'font change' in info_lower or 'font varies' in info_lower:
        rules["font_changes"] = info_text[:200]  # Truncate for brevity
    
    # Code system
    if 'code' in info_lower and 'system' in info_lower:
        rules["code_system"] = info_text[:200]
    
    # Add full text as a note if significant
    if len(info_text) > 20:
        rules["special_notes"].append(f"Full rules: {info_text[:300]}")
    
    return rules

def extract_stacked_character_rules(plate_types):
    """Analyze all plate types and extract stacked character omit/include patterns"""
    omit_patterns = []
    include_patterns = []
    position_notes = []
    prefix_rules = {}
    
    for plate in plate_types:
        char_mods = plate.get("processing_metadata", {}).get("character_modifications")
        if char_mods and char_mods not in ['N', 'No', 'None', None]:
            char_mods_lower = char_mods.lower()
            
            # Extract OMIT patterns
            if 'omit' in char_mods_lower:
                # Find quoted strings or uppercase words after "omit"
                quoted = re.findall(r'omit\s+["\']?([A-Z]{2,})["\']?', char_mods, re.IGNORECASE)
                for match in quoted:
                    if match.upper() not in omit_patterns:
                        omit_patterns.append(match.upper())
                
                # Also look for specific patterns like "OMIT DV", "OMIT City"
                words = re.findall(r'omit\s+(?:the\s+)?(?:letters?\s+)?([A-Z]+(?:\s+[A-Z]+)?)', char_mods, re.IGNORECASE)
                for word in words:
                    word_clean = word.strip().upper()
                    if word_clean and word_clean not in omit_patterns and len(word_clean) <= 15:
                        omit_patterns.append(word_clean)
            
            # Extract INCLUDE patterns (less common)
            if 'include' in char_mods_lower or 'add' in char_mods_lower:
                quoted = re.findall(r'(?:include|add)\s+["\']?([A-Z]{1,})["\']?', char_mods, re.IGNORECASE)
                for match in quoted:
                    if match.upper() not in include_patterns:
                        include_patterns.append(match.upper())
            
            # Position information
            if 'stacked' in char_mods_lower or 'vertical' in char_mods_lower:
                if char_mods not in position_notes:
                    position_notes.append(char_mods[:100])
            
            # Prefix rules (for things like DLR, DST, MFG)
            if plate.get("processing_metadata", {}).get("requires_prefix"):
                plate_name = plate.get("type_name", "")
                if any(keyword in plate_name.lower() for keyword in ['dealer', 'distributor', 'manufacturer']):
                    # Try to extract the prefix pattern
                    prefix_match = re.search(r'(?:starts with|prefix)\s+(?:vertical\s+)?([A-Z]{2,})', char_mods, re.IGNORECASE)
                    if prefix_match:
                        prefix_rules[plate_name] = prefix_match.group(1).upper()
    
    return {
        "omit": list(set(omit_patterns)),
        "include": list(set(include_patterns)),
        "position": "; ".join(position_notes[:3]) if position_notes else "Varies by plate type",
        "prefix_rules": prefix_rules if prefix_rules else None,
        "notes": f"Extracted from {len([p for p in plate_types if p.get('processing_metadata', {}).get('character_modifications')])} plate types with character modifications"
    }

def parse_state_csv(csv_file, state_name):
    """Parse any state's CSV and extract plate type information"""
    plate_types = []
    
    with open(csv_file, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f)
        
        # Read first row for character rules
        first_row = next(reader)
        char_rules = extract_character_rules(first_row)
        
        # Skip next two header rows
        next(reader)  # Column headers
        next(reader)  # Sub-headers
        
        for row in reader:
            # Check if plate type column (index 1) has data
            if len(row) < 6 or not row[1].strip():
                continue
            
            # Extract data from row
            code_number = row[0].strip() if row[0].strip() else "0"
            plate_type = row[1].strip()
            image1 = row[2].strip() if len(row) > 2 else ""
            image2 = row[3].strip() if len(row) > 3 else ""
            image3 = row[4].strip() if len(row) > 4 else ""
            
            # Processing rules columns
            currently_processed = row[5].strip() if len(row) > 5 else "N"
            add_prefix = row[6].strip() if len(row) > 6 else "N"
            add_suffix = row[7].strip() if len(row) > 7 else "N"
            omit_add_chars = row[8].strip() if len(row) > 8 else "N"
            verify_state_abbrev = row[9].strip() if len(row) > 9 else "Y"
            visual_identifier = row[10].strip() if len(row) > 10 else ""
            vehicle_type_id = row[11].strip() if len(row) > 11 else "N"
            all_numeric = row[12].strip() if len(row) > 12 else "N"
            
            # Skip plates not currently being processed
            if not plate_type or currently_processed.upper() != 'Y':
                continue
            
            # Build plate type entry
            plate_entry = {
                "type_name": plate_type,
                "code_number": code_number,
                "category": determine_category(plate_type),
                "description": f"{state_name} {plate_type} plate",
                "background_color": "#FFFFFF",
                "text_color": "#000000",
                "has_stickers": True,
                "sticker_description": "Month/Year validation stickers",
                "processing_metadata": {
                    "currently_processed": True,
                    "requires_prefix": add_prefix.upper() == 'Y',
                    "requires_suffix": add_suffix.upper() == 'Y',
                    "character_modifications": omit_add_chars if omit_add_chars and omit_add_chars.upper() not in ['N', 'NO'] else None,
                    "verify_state_abbreviation": verify_state_abbrev.upper() == 'Y',
                    "visual_identifier": visual_identifier if visual_identifier and visual_identifier.upper() not in ['N', 'NO'] else None,
                    "vehicle_type_identification": vehicle_type_id if vehicle_type_id and vehicle_type_id.upper() not in ['N', 'NO'] else None,
                    "all_numeric_plate": all_numeric.upper() == 'Y',
                },
                "plate_characteristics": {
                    "stacked_characters": None,
                    "variations": []
                }
            }
            
            # Add variations
            for img in [image1, image2, image3]:
                if img and img not in plate_entry["plate_characteristics"]["variations"]:
                    plate_entry["plate_characteristics"]["variations"].append(img)
            
            plate_types.append(plate_entry)
    
    # Extract global stacked character rules
    stacked_char_rules = extract_stacked_character_rules(plate_types)
    
    return {
        "plate_types": plate_types,
        "character_rules": char_rules,
        "stacked_character_rules": stacked_char_rules
    }

def determine_category(plate_type):
    """Determine the category based on plate type name"""
    plate_lower = plate_type.lower()
    
    # Order matters - check more specific patterns first
    if 'motorcycle' in plate_lower or 'mc' in plate_lower or ' m/c' in plate_lower:
        return 'motorcycle'
    elif 'trailer' in plate_lower:
        return 'trailer'
    elif 'truck' in plate_lower or 'commercial' in plate_lower or 'apportioned' in plate_lower:
        return 'commercial'
    elif 'dealer' in plate_lower or 'manufacturer' in plate_lower or 'distributor' in plate_lower:
        return 'dealer'
    elif 'temporary' in plate_lower or 'permit' in plate_lower or 'transit' in plate_lower:
        return 'temporary'
    elif 'disabled' in plate_lower or 'veteran' in plate_lower or 'military' in plate_lower or 'pearl harbor' in plate_lower or 'purple heart' in plate_lower or 'medal of honor' in plate_lower or 'ex-pow' in plate_lower:
        return 'military'
    elif 'university' in plate_lower or 'college' in plate_lower or 'collegiate' in plate_lower:
        return 'collegiate'
    elif 'antique' in plate_lower or 'classic' in plate_lower or 'historic' in plate_lower or 'horseless' in plate_lower:
        return 'antique'
    elif 'government' in plate_lower or 'official' in plate_lower or 'exempt' in plate_lower or 'authority' in plate_lower or 'police' in plate_lower or 'fire' in plate_lower:
        return 'government'
    elif 'recreational' in plate_lower or 'rv' in plate_lower or 'camper' in plate_lower:
        return 'recreational'
    elif 'passenger' in plate_lower or 'default' in plate_lower or 'standard' in plate_lower:
        return 'passenger'
    elif 'environmental' in plate_lower or 'special interest' in plate_lower or 'specialty' in plate_lower or 'kids plates' in plate_lower:
        return 'specialty'
    else:
        return 'specialty'

def get_state_abbreviation(state_name):
    """Convert state name to abbreviation"""
    state_map = {
        'alabama': 'AL', 'alaska': 'AK', 'arizona': 'AZ', 'arkansas': 'AR',
        'california': 'CA', 'colorado': 'CO', 'connecticut': 'CT', 'delaware': 'DE',
        'florida': 'FL', 'georgia': 'GA', 'hawaii': 'HI', 'idaho': 'ID',
        'illinois': 'IL', 'indiana': 'IN', 'iowa': 'IA', 'kansas': 'KS',
        'kentucky': 'KY', 'louisiana': 'LA', 'maine': 'ME', 'maryland': 'MD',
        'massachusetts': 'MA', 'michigan': 'MI', 'minnesota': 'MN', 'mississippi': 'MS',
        'missouri': 'MO', 'montana': 'MT', 'nebraska': 'NE', 'nevada': 'NV',
        'new hampshire': 'NH', 'new jersey': 'NJ', 'new mexico': 'NM', 'new york': 'NY',
        'north carolina': 'NC', 'north dakota': 'ND', 'ohio': 'OH', 'oklahoma': 'OK',
        'oregon': 'OR', 'pennsylvania': 'PA', 'rhode island': 'RI', 'south carolina': 'SC',
        'south dakota': 'SD', 'tennessee': 'TN', 'texas': 'TX', 'utah': 'UT',
        'vermont': 'VT', 'virginia': 'VA', 'washington': 'WA', 'west virginia': 'WV',
        'wisconsin': 'WI', 'wyoming': 'WY',
        'district of columbia': 'DC', 'dist columbia': 'DC',
        'american samoa': 'AS', 'amer samoa': 'AS', 'guam': 'GU',
        'puerto rico': 'PR', 'virgin islands': 'VI'
    }
    return state_map.get(state_name.lower(), state_name[:2].upper())

def main():
    if len(sys.argv) < 2:
        print("Usage: python parse_state_csv.py <state_name>")
        print("Example: python parse_state_csv.py California")
        print("\nOr use 'all' to process all pending CSVs")
        return
    
    state_name = sys.argv[1]
    
    if state_name.lower() == 'all':
        # Process all pending CSVs
        pending_dir = Path(__file__).parent.parent / 'data' / 'pending'
        csv_files = list(pending_dir.glob('Plate_Type_Matrix_*.csv'))
        
        print(f"Found {len(csv_files)} CSV files to process")
        
        for csv_file in csv_files:
            # Extract state name from filename
            match = re.search(r'\(([^)]+)\)\.csv$', csv_file.name)
            if not match:
                print(f"Skipping {csv_file.name} - couldn't extract state name")
                continue
            
            state_name = match.group(1)
            process_single_state(str(csv_file), state_name)
    else:
        # Process single state
        csv_file = Path(__file__).parent.parent / 'data' / 'pending' / f'Plate_Type_Matrix_Vs_Jun_25[1] (1)({state_name}).csv'
        
        if not csv_file.exists():
            print(f"Error: CSV file not found: {csv_file}")
            return
        
        process_single_state(str(csv_file), state_name)

def process_single_state(csv_file, state_name):
    """Process a single state CSV file"""
    output_file = Path(__file__).parent.parent / 'data' / 'pending' / f'{state_name.lower().replace(" ", "_")}_parsed.json'
    
    print(f"\n{'='*60}")
    print(f"Processing: {state_name}")
    print(f"CSV: {Path(csv_file).name}")
    print(f"{'='*60}")
    
    try:
        result = parse_state_csv(csv_file, state_name)
        plate_types = result["plate_types"]
        char_rules = result["character_rules"]
        stacked_rules = result["stacked_character_rules"]
        
        print(f"✓ Found {len(plate_types)} plate types (currently processed)")
        
        # Print character rules summary
        if char_rules["uses_zero_for_o"]:
            print(f"✓ Uses zero '0' instead of letter 'O'")
        if char_rules["letter_restrictions"]:
            print(f"✓ Letter restrictions: {', '.join(char_rules['letter_restrictions'])}")
        
        # Print stacked character rules
        if stacked_rules["omit"]:
            print(f"✓ Omit patterns: {', '.join(stacked_rules['omit'][:10])}")
        if stacked_rules["include"]:
            print(f"✓ Include patterns: {', '.join(stacked_rules['include'][:10])}")
        
        # Category breakdown
        categories = {}
        for pt in plate_types:
            cat = pt['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        print(f"\nPlate types by category:")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print(f"  {cat}: {count}")
        
        # Write to JSON file
        output_data = {
            "state": state_name,
            "abbreviation": get_state_abbreviation(state_name),
            "character_rules": char_rules,
            "stacked_character_rules": stacked_rules,
            "plate_types": plate_types,
            "total_count": len(plate_types)
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"\n✓ Wrote parsed data to: {output_file.name}")
        
    except Exception as e:
        print(f"✗ Error processing {state_name}: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
