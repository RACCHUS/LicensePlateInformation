"""
Batch Update State JSON Files
Merges parsed CSV data into existing state JSON files
Preserves existing data while adding/updating character rules and plate types
"""
import json
import sys
from pathlib import Path
import re

def load_json(file_path):
    """Load JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(file_path, data):
    """Save JSON file with pretty formatting"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_state_json_path(state_name, states_dir):
    """Convert state name to JSON file path"""
    # Handle special cases
    name_map = {
        'dist columbia': 'district_of_columbia',
        'amer samoa': 'american_samoa',
        'government services': 'government_services'
    }
    
    state_lower = state_name.lower()
    if state_lower in name_map:
        file_name = name_map[state_lower]
    else:
        file_name = state_lower.replace(' ', '_')
    
    return states_dir / f'{file_name}.json'

def update_state_json(state_json_path, parsed_data):
    """Update existing state JSON with parsed CSV data"""
    
    if not state_json_path.exists():
        print(f"  ⚠ State JSON not found: {state_json_path.name}")
        print(f"    Creating new JSON file...")
        create_new_state_json(state_json_path, parsed_data)
        return {
            'status': 'created',
            'added_plates': len(parsed_data['plate_types']),
            'updated_rules': True
        }
    
    # Load existing state JSON
    state_data = load_json(state_json_path)
    
    changes = {
        'status': 'updated',
        'added_plates': 0,
        'updated_plates': 0,
        'updated_rules': False,
        'existing_plates': len(state_data.get('plate_types', []))
    }
    
    # Update character handling rules in global_rules
    if 'processing_metadata' not in state_data:
        state_data['processing_metadata'] = {}
    if 'global_rules' not in state_data['processing_metadata']:
        state_data['processing_metadata']['global_rules'] = {}
    
    global_rules = state_data['processing_metadata']['global_rules']
    
    # Update stacked_characters section
    csv_stacked_rules = parsed_data.get('stacked_character_rules', {})
    
    if csv_stacked_rules.get('omit') or csv_stacked_rules.get('include'):
        changes['updated_rules'] = True
        
        if 'stacked_characters' not in global_rules:
            global_rules['stacked_characters'] = {}
        
        stacked_chars = global_rules['stacked_characters']
        
        # Merge omit rules
        existing_omit = stacked_chars.get('omit', [])
        csv_omit = csv_stacked_rules.get('omit', [])
        merged_omit = list(set(existing_omit + csv_omit))
        stacked_chars['omit'] = sorted(merged_omit)
        
        # Merge include rules
        existing_include = stacked_chars.get('include', [])
        csv_include = csv_stacked_rules.get('include', [])
        merged_include = list(set(existing_include + csv_include))
        stacked_chars['include'] = sorted(merged_include)
        
        # Update position if more detailed
        if csv_stacked_rules.get('position') and len(csv_stacked_rules['position']) > 20:
            stacked_chars['position'] = csv_stacked_rules['position']
        
        # Update notes
        csv_notes = csv_stacked_rules.get('notes', '')
        existing_notes = stacked_chars.get('notes', '')
        if csv_notes and csv_notes not in existing_notes:
            if existing_notes:
                stacked_chars['notes'] = f"{existing_notes}; {csv_notes}"
            else:
                stacked_chars['notes'] = csv_notes
        
        # Add prefix rules if present
        if csv_stacked_rules.get('prefix_rules'):
            if 'prefix_rules' not in stacked_chars:
                stacked_chars['prefix_rules'] = {}
            stacked_chars['prefix_rules'].update(csv_stacked_rules['prefix_rules'])
    
    # Update character restrictions from CSV
    csv_char_rules = parsed_data.get('character_rules', {})
    if csv_char_rules.get('special_notes'):
        if 'character_restrictions' in global_rules:
            # Append to existing
            existing = global_rules['character_restrictions']
            new_note = csv_char_rules['special_notes'][0]
            if new_note not in existing:
                global_rules['character_restrictions'] = f"{existing}; {new_note}"
        else:
            global_rules['character_restrictions'] = csv_char_rules['special_notes'][0]
        changes['updated_rules'] = True
    
    # Merge plate types
    existing_plate_types = {pt.get('type_name', ''): pt for pt in state_data.get('plate_types', [])}
    
    for csv_plate in parsed_data.get('plate_types', []):
        plate_name = csv_plate.get('type_name', '')
        
        if plate_name in existing_plate_types:
            # Update existing plate with CSV data
            existing_plate = existing_plate_types[plate_name]
            
            # Merge processing_metadata
            if 'processing_metadata' in csv_plate:
                if 'processing_metadata' not in existing_plate:
                    existing_plate['processing_metadata'] = {}
                
                csv_meta = csv_plate['processing_metadata']
                existing_meta = existing_plate['processing_metadata']
                
                # Update fields if CSV has more detailed info
                if csv_meta.get('character_modifications'):
                    existing_meta['character_modifications'] = csv_meta['character_modifications']
                if csv_meta.get('visual_identifier'):
                    existing_meta['visual_identifier'] = csv_meta['visual_identifier']
                if csv_meta.get('requires_prefix'):
                    existing_meta['requires_prefix'] = csv_meta['requires_prefix']
                if csv_meta.get('requires_suffix'):
                    existing_meta['requires_suffix'] = csv_meta['requires_suffix']
                
                changes['updated_plates'] += 1
        else:
            # Add new plate type
            state_data['plate_types'].append(csv_plate)
            changes['added_plates'] += 1
    
    # Save updated JSON
    save_json(state_json_path, state_data)
    
    return changes

def create_new_state_json(state_json_path, parsed_data):
    """Create a new state JSON file from parsed CSV data"""
    state_name = parsed_data.get('state', 'Unknown')
    abbreviation = parsed_data.get('abbreviation', 'XX')
    
    # Get character restrictions safely
    special_notes = parsed_data['character_rules'].get('special_notes', [])
    char_restrictions = special_notes[0] if special_notes else "Information needed"
    
    state_data = {
        "name": state_name,
        "abbreviation": abbreviation,
        "slogan": f"{state_name} State",
        "uses_zero_for_o": parsed_data['character_rules'].get('uses_zero_for_o', False),
        "allows_letter_o": not parsed_data['character_rules'].get('uses_zero_for_o', False),
        "zero_is_slashed": False,
        "primary_colors": ["#FFFFFF", "#000000"],
        "notes": f"Imported from DMV CSV data - {len(parsed_data['plate_types'])} plate types",
        "processing_metadata": {
            "description": f"Official {state_name} DMV processing rules",
            "global_rules": {
                "character_restrictions": char_restrictions,
                "font_changes": None,
                "code_system": None,
                "stacked_characters": {
                    "include": parsed_data['stacked_character_rules'].get('include', []),
                    "omit": parsed_data['stacked_character_rules'].get('omit', []),
                    "position": parsed_data['stacked_character_rules'].get('position', 'Varies by plate type'),
                    "max_characters": None,
                    "prefix_rules": parsed_data['stacked_character_rules'].get('prefix_rules'),
                    "symbols_allowed": None,
                    "notes": parsed_data['stacked_character_rules'].get('notes', '')
                }
            }
        },
        "plate_types": parsed_data['plate_types']
    }
    
    save_json(state_json_path, state_data)

def process_all_states(pending_dir, states_dir):
    """Process all parsed JSON files from pending directory"""
    
    # Find all parsed JSON files
    parsed_files = list(pending_dir.glob('*_parsed.json'))
    
    # Skip old format files
    parsed_files = [f for f in parsed_files if f.name != 'texas_plate_types_parsed.json']
    
    if not parsed_files:
        print("No parsed JSON files found in pending directory!")
        print("Run parse_state_csv.py first to generate parsed data.")
        return
    
    print(f"\n{'='*70}")
    print(f"Batch Update: Found {len(parsed_files)} parsed state files")
    print(f"{'='*70}\n")
    
    results = {
        'created': [],
        'updated': [],
        'errors': [],
        'skipped': []
    }
    
    for parsed_file in sorted(parsed_files):
        state_name = parsed_file.stem.replace('_parsed', '').replace('_', ' ').title()
        parsed_data = None
        
        try:
            # Load parsed data
            parsed_data = load_json(parsed_file)
            
            # Validate format - should be dict with 'state' key
            if not isinstance(parsed_data, dict) or 'state' not in parsed_data:
                print(f"Skipping: {parsed_file.name} (old/incompatible format)\n")
                results['skipped'].append(parsed_file.name)
                continue
            
            # Get target state JSON path
            state_json_path = get_state_json_path(parsed_data['state'], states_dir)
            
            print(f"Processing: {parsed_data['state']}")
            print(f"  Source: {parsed_file.name}")
            print(f"  Target: {state_json_path.name}")
            
            # Update state JSON
            changes = update_state_json(state_json_path, parsed_data)
            
            # Report changes
            if changes['status'] == 'created':
                print(f"  ✓ Created new state JSON")
                print(f"  ✓ Added {changes['added_plates']} plate types")
                results['created'].append(parsed_data['state'])
            else:
                print(f"  ✓ Updated existing state JSON")
                if changes['updated_rules']:
                    print(f"  ✓ Updated character handling rules")
                if changes['added_plates'] > 0:
                    print(f"  ✓ Added {changes['added_plates']} new plate types")
                if changes['updated_plates'] > 0:
                    print(f"  ✓ Updated {changes['updated_plates']} existing plate types")
                results['updated'].append(parsed_data['state'])
            
            print()
            
        except Exception as e:
            print(f"  ✗ Error: {str(e)}\n")
            error_state = parsed_data['state'] if parsed_data else state_name
            results['errors'].append((error_state, str(e)))
    
    # Print summary
    print(f"{'='*70}")
    print("BATCH UPDATE SUMMARY")
    print(f"{'='*70}")
    print(f"✓ Created: {len(results['created'])} state(s)")
    if results['created']:
        for state in results['created']:
            print(f"    - {state}")
    
    print(f"\n✓ Updated: {len(results['updated'])} state(s)")
    if results['updated']:
        for state in results['updated']:
            print(f"    - {state}")
    
    if results['skipped']:
        print(f"\n⊘ Skipped: {len(results['skipped'])} file(s)")
        for file in results['skipped']:
            print(f"    - {file}")
    
    if results['errors']:
        print(f"\n✗ Errors: {len(results['errors'])} state(s)")
        for state, error in results['errors']:
            print(f"    - {state}: {error}")
    
    print(f"\n{'='*70}")
    print(f"Total Processed: {len(results['created']) + len(results['updated'])} / {len(parsed_files)}")
    print(f"{'='*70}\n")

def main():
    project_root = Path(__file__).parent.parent
    pending_dir = project_root / 'data' / 'pending'
    states_dir = project_root / 'data' / 'states'
    
    if not pending_dir.exists():
        print(f"Error: Pending directory not found: {pending_dir}")
        return
    
    if not states_dir.exists():
        print(f"Error: States directory not found: {states_dir}")
        return
    
    process_all_states(pending_dir, states_dir)

if __name__ == '__main__':
    main()
