"""
Update state JSON files with font information from the font document.
"""

import json
from pathlib import Path

# Font mapping from the document
FONT_DATA = {
    'alabama': 'Series of custom block numerals, similar to FE-Schrift derivative',
    'alaska': 'Custom condensed sans serif, proprietary',
    'arizona': 'Modified block sans serif, similar to Highway Gothic',
    'arkansas': 'Narrow block sans serif, proprietary',
    'california': 'Penitentiary Gothic (custom)',
    'colorado': 'Modified block sans serif, Highway Gothic influence',
    'connecticut': 'Block sans serif, similar to Highway Gothic',
    'delaware': 'Serifed block style, similar to "Delaware" font replicas',
    'florida': 'Narrow sans serif, proprietary variant of Highway Gothic',
    'georgia': 'Modified sans serif, based on Highway Gothic',
    'hawaii': 'Custom sans serif, similar to Highway Gothic',
    'idaho': 'Modified block sans serif, proprietary',
    'illinois': 'Narrow sans serif, Highway Gothic derivative',
    'indiana': 'Custom sans serif, close to Interstate',
    'iowa': 'Modified sans serif, proprietary variant',
    'kansas': 'Block sans serif, similar to Highway Gothic',
    'kentucky': 'Custom sans serif, proprietary',
    'louisiana': 'Serif script for state name, block sans serif for numbers (Highway Gothic style)',
    'maine': 'Modified sans serif, proprietary',
    'maryland': 'Narrow sans serif, Highway Gothic influence',
    'massachusetts': 'Custom sans serif, similar to Massachusetts Block',
    'michigan': 'Narrow sans serif, Highway Gothic derivative',
    'minnesota': 'Modified sans serif, proprietary',
    'mississippi': 'Custom sans serif, proprietary',
    'missouri': 'Highway Gothic derivative',
    'montana': 'Narrow block sans serif, proprietary',
    'nebraska': 'Modified block sans serif, Highway Gothic style',
    'nevada': 'Custom sans serif, proprietary',
    'new_hampshire': 'Narrow sans serif, Highway Gothic derivative',
    'new_jersey': 'Modified sans serif, proprietary',
    'new_mexico': 'Custom sans serif, proprietary',
    'new_york': 'Modified block sans serif, Highway Gothic derivative',
    'north_carolina': 'Custom sans serif, proprietary',
    'north_dakota': 'Modified sans serif, proprietary',
    'ohio': 'Narrow sans serif, Highway Gothic influence',
    'oklahoma': 'Custom sans serif, proprietary',
    'oregon': 'Modified sans serif, Highway Gothic style',
    'pennsylvania': 'Custom sans serif, replicated as "Pennsylvania" font',
    'rhode_island': 'Narrow sans serif, Highway Gothic derivative',
    'south_carolina': 'Custom sans serif, proprietary',
    'south_dakota': 'Custom sans serif, proprietary',
    'tennessee': 'Modified sans serif, Highway Gothic derivative',
    'texas': 'Block sans serif, proprietary (Highway Gothic influence)',
    'utah': 'Custom sans serif, proprietary',
    'vermont': 'Narrow sans serif, Highway Gothic style',
    'virginia': 'Modified sans serif, proprietary',
    'washington': 'Custom sans serif, replicated as "Washington License Plate" font',
    'west_virginia': 'Narrow sans serif, Highway Gothic derivative',
    'wisconsin': 'Modified sans serif, proprietary',
    'wyoming': 'Custom sans serif, proprietary',
    'american_samoa': 'Custom sans serif, proprietary',
    'guam': 'Modified sans serif, proprietary',
    'northern_mariana_islands': 'Custom sans serif, proprietary',
    'puerto_rico': 'Narrow sans serif, Highway Gothic influence',
    'us_virgin_islands': 'Custom sans serif, proprietary',
    'washington_dc': 'Modified sans serif, Highway Gothic derivative',
    'ontario': 'Narrow sans serif, similar to "Ontario" proprietary font',
    'alberta': 'Block sans serif, Highway Gothic derivative',
    # States not in the document - keep defaults
    'diplomatic': 'Standard diplomatic plate font',
    'us_government': 'Standard government plate font',
}

def update_state_fonts():
    """Update main_font field in all state JSON files."""
    states_dir = Path(__file__).parent.parent / "data" / "states"
    
    updated_count = 0
    skipped_count = 0
    error_count = 0
    
    details = []
    
    for json_file in sorted(states_dir.glob("*.json")):
        state_filename = json_file.stem
        
        try:
            # Load the JSON file
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check if we have font data for this state
            if state_filename in FONT_DATA:
                font_info = FONT_DATA[state_filename]
                old_value = data.get('main_font', 'Not set')
                
                # Update the font
                data['main_font'] = font_info
                
                # Write back to file
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                
                updated_count += 1
                
                # Only show details if it was actually changed
                if old_value != font_info:
                    details.append(f"\n{state_filename.upper().replace('_', ' ')}:")
                    details.append(f"  Old: {old_value}")
                    details.append(f"  New: {font_info}")
            else:
                skipped_count += 1
                details.append(f"\n{state_filename.upper().replace('_', ' ')}: ⚠️  No font data available")
        
        except Exception as e:
            error_count += 1
            details.append(f"\n{state_filename.upper().replace('_', ' ')}: ❌ Error - {e}")
    
    # Print summary
    print("=" * 80)
    print("FONT UPDATE SUMMARY")
    print("=" * 80)
    print(f"\nFiles updated: {updated_count}")
    print(f"Files skipped (no font data): {skipped_count}")
    print(f"Errors: {error_count}")
    
    if details:
        print("\n" + "=" * 80)
        print("DETAILS")
        print("=" * 80)
        for detail in details:
            print(detail)
    
    print("\n" + "=" * 80)
    if error_count == 0:
        print("✅ FONT UPDATE COMPLETE")
    else:
        print("⚠️  FONT UPDATE COMPLETE WITH ERRORS")
    print("=" * 80)

if __name__ == "__main__":
    update_state_fonts()
