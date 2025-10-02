"""
Update state JSON files with logo information from the logo descriptions document.
"""

import json
from pathlib import Path

# Logo mapping from the document
LOGO_DATA = {
    'alabama': 'Red script "Sweet Home Alabama" with star/shooting star',
    'alaska': 'Grizzly bear and North Star / Big Dipper',
    'arizona': 'Desert scene with mountains and cactus',
    'arkansas': 'Diamond emblem (state gem)',
    'california': 'Red cursive "California" wordmark',
    'colorado': 'Green mountain range silhouette',
    'connecticut': 'Simple two-tone blue gradient, no major logo',
    'delaware': 'Plain blue background with gold text (no main logo)',
    'florida': 'Orange with blossoms between letters',
    'georgia': 'Peach emblem above/between characters',
    'hawaii': 'Rainbow arc across plate',
    'idaho': 'Red gradient sky with pine trees and mountains',
    'illinois': 'Bust of Abraham Lincoln (state slogan "Land of Lincoln")',
    'indiana': 'Torch and stars (state flag symbol)',
    'iowa': 'Skyline with barns, silos, and capitol dome',
    'kansas': 'State seal with rising sun and wagon wheel',
    'kentucky': 'Stylized state outline with "Unbridled Spirit" horse logo',
    'louisiana': 'Red script "Louisiana" with pelican option (most common plain has no large logo)',
    'maine': 'Chickadee bird on branch with pine cone',
    'maryland': 'State flag shield emblem',
    'massachusetts': 'Pilgrim ship (Mayflower)',
    'michigan': 'Outline of the state with a cherry or Great Lakes depiction',
    'minnesota': 'State outline with loon and sunset over water',
    'mississippi': 'Magnolia flower (state flower)',
    'missouri': 'Gateway Arch silhouette',
    'montana': 'Mountains and plains scene with rising sun',
    'nebraska': 'State outline with prairie scene',
    'nevada': 'Mountain range with sun rays',
    'new_hampshire': 'Old Man of the Mountain rock formation (historic emblem)',
    'new_jersey': 'State silhouette with garden state slogan or plain text, small state outline in some versions',
    'new_mexico': 'Zia sun symbol',
    'new_york': 'Statue of Liberty silhouette or state outline with "Empire State"',
    'north_carolina': 'Cardinal (state bird) or mountains/coastline scene',
    'north_dakota': 'State outline with bison or plains scene',
    'ohio': 'State outline with "Ohio" in red, white, and blue',
    'oklahoma': 'State outline with Native American peace pipe / olive branch',
    'oregon': 'Beaver (state animal) or mountains with trees',
    'pennsylvania': 'Keystones or state outline with Liberty Bell',
    'rhode_island': 'Anchor emblem (state symbol)',
    'south_carolina': 'Palmetto tree and crescent moon',
    'south_dakota': 'Mount Rushmore or sun over prairie scene',
    'tennessee': 'Tri-star emblem (from state flag)',
    'texas': 'Lone Star or state outline with star',
    'utah': 'Delicate Arch or beehive emblem',
    'vermont': 'Green Mountains with maple leaf or state outline',
    'virginia': 'State outline or cardinal (state bird)',
    'washington': 'Mount Rainier or state outline',
    'west_virginia': 'State outline with mountains and rivers',
    'wisconsin': 'Cow or state outline with dairy imagery',
    'wyoming': 'Bucking horse and rider',
    'american_samoa': 'Tropical island scene with traditional canoe and palm trees',
    'guam': 'Latte stone with palm tree and coastline',
    'northern_mariana_islands': 'Star and latte stone emblem',
    'puerto_rico': 'Coquí frog or El Morro fortress silhouette',
    'us_virgin_islands': 'Palm tree with state outline or territorial seal',
    'washington_dc': 'Washington Monument or stylized "DC" seal',
    'ontario': 'Trillium flower (provincial emblem)',
    'alberta': 'Rocky Mountains with wheat field background',
    # States not in the document - defaults
    'diplomatic': 'Diplomatic seal or flag emblem',
    'us_government': 'Federal government seal or "U.S. GOVERNMENT" text',
}

def update_state_logos():
    """Update main_logo field in all state JSON files."""
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
            
            # Check if we have logo data for this state
            if state_filename in LOGO_DATA:
                logo_info = LOGO_DATA[state_filename]
                old_value = data.get('main_logo', 'Not set')
                
                # Update the logo
                data['main_logo'] = logo_info
                
                # Write back to file
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                
                updated_count += 1
                
                # Only show details if it was actually changed
                if old_value != logo_info:
                    details.append(f"\n{state_filename.upper().replace('_', ' ')}:")
                    details.append(f"  Old: {old_value}")
                    details.append(f"  New: {logo_info}")
            else:
                skipped_count += 1
                details.append(f"\n{state_filename.upper().replace('_', ' ')}: No logo data available")
        
        except Exception as e:
            error_count += 1
            details.append(f"\n{state_filename.upper().replace('_', ' ')}: Error - {e}")
    
    # Print summary
    print("=" * 80)
    print("LOGO UPDATE SUMMARY")
    print("=" * 80)
    print(f"\nFiles updated: {updated_count}")
    print(f"Files skipped (no logo data): {skipped_count}")
    print(f"Errors: {error_count}")
    
    if details:
        print("\n" + "=" * 80)
        print("DETAILS")
        print("=" * 80)
        for detail in details:
            print(detail)
    
    print("\n" + "=" * 80)
    if error_count == 0:
        print("LOGO UPDATE COMPLETE")
    else:
        print("LOGO UPDATE COMPLETE WITH ERRORS")
    print("=" * 80)

if __name__ == "__main__":
    update_state_logos()
