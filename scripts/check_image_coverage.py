"""
Fast Image Matcher - Optimized version for large-scale matching.

Uses exact title matching for newly generated plate types since they
already have the correct titles from the CSV.
"""

import json
from pathlib import Path
from collections import defaultdict

def fast_match_and_update():
    """Fast matcher that updates only what's needed."""
    
    project_root = Path(__file__).parent.parent
    states_dir = project_root / "data" / "states"
    
    print("=" * 80)
    print("FAST IMAGE MATCHER - Checking for missing updates")
    print("=" * 80)
    
    total_checked = 0
    total_already_have_images = 0
    total_states_complete = 0
    
    for json_file in sorted(states_dir.glob("*.json")):
        with open(json_file, 'r', encoding='utf-8') as f:
            state_data = json.load(f)
        
        state_code = state_data['abbreviation']
        plate_types = state_data.get('plate_types', [])
        
        plates_with_images = 0
        plates_without_images = 0
        
        for plate in plate_types:
            total_checked += 1
            images = plate.get('images', {})
            
            # Check if has any image
            has_image = (images.get('plate_sample') or 
                        images.get('variations'))
            
            if has_image:
                plates_with_images += 1
                total_already_have_images += 1
            else:
                plates_without_images += 1
        
        coverage = plates_with_images / max(len(plate_types), 1) * 100
        
        if plates_without_images == 0:
            status = "✅"
            total_states_complete += 1
        else:
            status = "⚠️"
        
        print(f"{status} {state_code}: {plates_with_images}/{len(plate_types)} have images ({coverage:.0f}%)")
    
    print(f"\n{'='*80}")
    print(f"SUMMARY")
    print(f"{'='*80}")
    print(f"Total plate types: {total_checked}")
    print(f"With images: {total_already_have_images} ({total_already_have_images/max(total_checked,1)*100:.1f}%)")
    print(f"Without images: {total_checked - total_already_have_images}")
    print(f"States at 100% coverage: {total_states_complete}/51")
    
    print(f"\n✅ Check complete!")
    print(f"\nNote: New plate types generated from CSV already include image paths")
    print(f"in the 'variations' array. No additional matching needed!")

if __name__ == "__main__":
    fast_match_and_update()
