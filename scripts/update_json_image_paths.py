"""
Script to update JSON files with image paths from data/images/Plates folders.

This script scans the data/images/Plates directory structure and updates
the corresponding state JSON files with the correct image paths for:
- plate_sample
- truck_sample
- trailer_sample
- semi-trailer_sample
- fleet-trailer_sample
- rental-trailer_sample
- permanent-trailer_sample
"""

import os
import json
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
PLATES_DIR = BASE_DIR / "data" / "images" / "Plates"
STATES_DIR = BASE_DIR / "data" / "states"

# Mapping of folder names to JSON filenames and state codes
STATE_MAPPING = {
    "Alabama": ("alabama.json", "AL"),
    "Alaska": ("alaska.json", "AK"),
    "Arizona": ("arizona.json", "AZ"),
    "Arkansas": ("arkansas.json", "AR"),
    "California": ("california.json", "CA"),
    "Colorado": ("colorado.json", "CO"),
    "Connecticut": ("connecticut.json", "CT"),
    "Delaware": ("delaware.json", "DE"),
    "Florida": ("florida.json", "FL"),
    "Georgia": ("georgia.json", "GA"),
    "Hawaii": ("hawaii.json", "HI"),
    "Idaho": ("idaho.json", "ID"),
    "Illinios": ("illinois.json", "IL"),  # Note: folder has typo
    "Indiana": ("indiana.json", "IN"),
    "Iowa": ("iowa.json", "IA"),
    "Kansas": ("kansas.json", "KS"),
    "Kentucky": ("kentucky.json", "KY"),
    "Louisiana": ("louisiana.json", "LA"),
    "Maine": ("maine.json", "ME"),
    "Maryland": ("maryland.json", "MD"),
    "Massachusetts": ("massachusetts.json", "MA"),
    "Michigan": ("michigan.json", "MI"),
    "Minnesota": ("minnesota.json", "MN"),
    "Mississippi": ("mississippi.json", "MS"),
    "Missouri": ("missouri.json", "MO"),
    "Montana": ("montana.json", "MT"),
    "Nebraska": ("nebraska.json", "NE"),
    "Nevada": ("nevada.json", "NV"),
    "New Hampshire": ("new_hampshire.json", "NH"),
    "New Jersey": ("new_jersey.json", "NJ"),
    "New Mexico": ("new_mexico.json", "NM"),
    "New York": ("new_york.json", "NY"),
    "North Carolina": ("north_carolina.json", "NC"),
    "North Dakota": ("north_dakota.json", "ND"),
    "Ohio": ("ohio.json", "OH"),
    "Oklahoma": ("oklahoma.json", "OK"),
    "Oregon": ("oregon.json", "OR"),
    "Pennsylvania": ("pennsylvania.json", "PA"),
    "Rhode Island": ("rhode_island.json", "RI"),
    "South Carolina": ("south_carolina.json", "SC"),
    "South Dakota": ("south_dakota.json", "SD"),
    "Tennessee": ("tennessee.json", "TN"),
    "Utah": ("utah.json", "UT"),
    "Vermont": ("vermont.json", "VT"),
    "Virginia": ("virginia.json", "VA"),
    "Washington": ("washington.json", "WA"),
    "West Virginia": ("west_virginia.json", "WV"),
    "Wisconsin": ("wisconsin.json", "WI"),
    "Wyoming": ("wyoming.json", "WY"),
}

# Mapping of image filenames to plate type keywords
IMAGE_TO_TYPE_MAPPING = {
    "plate_sample.png": ["Passenger", "Standard", "Regular"],
    "truck_sample.png": ["Truck"],
    "trailer_sample.png": ["Trailer"],
    "semi-trailer_sample.png": ["Semi Trailer", "Semi-Trailer", "Semitrailer"],
    "fleet-trailer_sample.png": ["Fleet"],
    "rental-trailer_sample.png": ["Rental"],
    "permanent-trailer_sample.png": ["Permanent"],
}


def scan_state_images(state_folder_name):
    """Scan a state folder for images and return mapping."""
    folder_path = PLATES_DIR / state_folder_name
    if not folder_path.exists():
        return {}
    
    images = {}
    for file in folder_path.iterdir():
        if file.is_file() and file.suffix.lower() in ['.png', '.jpg', '.jpeg']:
            images[file.name] = str(file.relative_to(BASE_DIR)).replace("\\", "/")
    
    return images


def update_state_json(json_filename, state_code, images_found):
    """Update a state JSON file with the correct image paths."""
    json_path = STATES_DIR / json_filename
    
    if not json_path.exists():
        print(f"❌ JSON file not found: {json_filename}")
        return False
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error reading {json_filename}: {e}")
        return False
    
    updated = False
    plate_types = data.get('plate_types', [])
    
    # Update plate_sample (generic passenger/standard plate)
    if 'plate_sample.png' in images_found:
        for plate_type in plate_types:
            type_name = plate_type.get('type_name', '')
            category = plate_type.get('category', '')
            
            # Update standard/passenger plate
            if any(keyword.lower() in type_name.lower() 
                   for keyword in IMAGE_TO_TYPE_MAPPING['plate_sample.png']):
                if 'images' not in plate_type:
                    plate_type['images'] = {}
                
                old_path = plate_type['images'].get('plate_sample')
                plate_type['images']['plate_sample'] = images_found['plate_sample.png']
                if old_path != images_found['plate_sample.png']:
                    print(f"  ✓ Updated {type_name}: {images_found['plate_sample.png']}")
                    updated = True
    
    # Update truck_sample
    if 'truck_sample.png' in images_found:
        for plate_type in plate_types:
            type_name = plate_type.get('type_name', '')
            
            if 'Truck' in type_name and 'Tractor' not in type_name:
                if 'images' not in plate_type:
                    plate_type['images'] = {}
                
                old_path = plate_type['images'].get('plate_sample')
                plate_type['images']['plate_sample'] = images_found['truck_sample.png']
                if old_path != images_found['truck_sample.png']:
                    print(f"  ✓ Updated {type_name}: {images_found['truck_sample.png']}")
                    updated = True
    
    # Update trailer_sample
    if 'trailer_sample.png' in images_found:
        for plate_type in plate_types:
            type_name = plate_type.get('type_name', '')
            
            if 'Trailer' in type_name and 'Semi' not in type_name and 'Fleet' not in type_name and 'Rental' not in type_name and 'Permanent' not in type_name:
                if 'images' not in plate_type:
                    plate_type['images'] = {}
                
                old_path = plate_type['images'].get('plate_sample')
                plate_type['images']['plate_sample'] = images_found['trailer_sample.png']
                if old_path != images_found['trailer_sample.png']:
                    print(f"  ✓ Updated {type_name}: {images_found['trailer_sample.png']}")
                    updated = True
    
    # Update semi-trailer_sample
    if 'semi-trailer_sample.png' in images_found:
        for plate_type in plate_types:
            type_name = plate_type.get('type_name', '')
            
            if any(keyword in type_name for keyword in ['Semi Trailer', 'Semi-Trailer', 'Semitrailer']):
                if 'images' not in plate_type:
                    plate_type['images'] = {}
                
                old_path = plate_type['images'].get('plate_sample')
                plate_type['images']['plate_sample'] = images_found['semi-trailer_sample.png']
                if old_path != images_found['semi-trailer_sample.png']:
                    print(f"  ✓ Updated {type_name}: {images_found['semi-trailer_sample.png']}")
                    updated = True
    
    # Update fleet-trailer_sample
    if 'fleet-trailer_sample.png' in images_found:
        for plate_type in plate_types:
            type_name = plate_type.get('type_name', '')
            
            if 'Fleet' in type_name:
                if 'images' not in plate_type:
                    plate_type['images'] = {}
                
                old_path = plate_type['images'].get('plate_sample')
                plate_type['images']['plate_sample'] = images_found['fleet-trailer_sample.png']
                if old_path != images_found['fleet-trailer_sample.png']:
                    print(f"  ✓ Updated {type_name}: {images_found['fleet-trailer_sample.png']}")
                    updated = True
    
    # Update rental-trailer_sample
    if 'rental-trailer_sample.png' in images_found:
        for plate_type in plate_types:
            type_name = plate_type.get('type_name', '')
            
            if 'Rental' in type_name and 'Trailer' in type_name:
                if 'images' not in plate_type:
                    plate_type['images'] = {}
                
                old_path = plate_type['images'].get('plate_sample')
                plate_type['images']['plate_sample'] = images_found['rental-trailer_sample.png']
                if old_path != images_found['rental-trailer_sample.png']:
                    print(f"  ✓ Updated {type_name}: {images_found['rental-trailer_sample.png']}")
                    updated = True
    
    # Update permanent-trailer_sample
    if 'permanent-trailer_sample.png' in images_found:
        for plate_type in plate_types:
            type_name = plate_type.get('type_name', '')
            
            if 'Permanent' in type_name and 'Trailer' in type_name:
                if 'images' not in plate_type:
                    plate_type['images'] = {}
                
                old_path = plate_type['images'].get('plate_sample')
                plate_type['images']['plate_sample'] = images_found['permanent-trailer_sample.png']
                if old_path != images_found['permanent-trailer_sample.png']:
                    print(f"  ✓ Updated {type_name}: {images_found['permanent-trailer_sample.png']}")
                    updated = True
    
    # Update font samples (font0.png, fontO.png)
    for font_file in ['font0.png', 'fontO.png']:
        if font_file in images_found:
            # Add to state-level images
            if 'images' not in data:
                data['images'] = {}
            
            old_path = data['images'].get('character_font_reference')
            data['images']['character_font_reference'] = images_found[font_file]
            if old_path != images_found[font_file]:
                print(f"  ✓ Updated state font reference: {images_found[font_file]}")
                updated = True
    
    # Save the updated JSON
    if updated:
        try:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"✅ Saved updates to {json_filename}")
            return True
        except Exception as e:
            print(f"❌ Error saving {json_filename}: {e}")
            return False
    else:
        print(f"ℹ️  No updates needed for {json_filename}")
        return False


def main():
    """Main function to process all states."""
    print("=" * 80)
    print("Updating JSON files with image paths from data/images/Plates")
    print("=" * 80)
    print()
    
    total_updated = 0
    total_processed = 0
    
    # Process each state folder
    for state_folder, (json_file, state_code) in STATE_MAPPING.items():
        print(f"\n📁 Processing {state_folder} ({state_code})...")
        
        # Scan for images
        images = scan_state_images(state_folder)
        
        if not images:
            print(f"  ⚠️  No images found in {state_folder}")
            continue
        
        print(f"  Found {len(images)} image(s): {', '.join(images.keys())}")
        
        # Update JSON
        if update_state_json(json_file, state_code, images):
            total_updated += 1
        
        total_processed += 1
    
    print("\n" + "=" * 80)
    print(f"Summary: {total_updated} of {total_processed} states updated")
    print("=" * 80)


if __name__ == "__main__":
    main()
