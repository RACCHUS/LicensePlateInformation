"""
Script to add missing plate_characteristics structure to all state JSON files
"""
import json
import os
from pathlib import Path
from typing import Dict, Any

def get_default_plate_characteristics() -> Dict[str, Any]:
    """Get default plate_characteristics structure from template"""
    return {
        "font": None,
        "logo": None,
        "plate_text": None,
        "design_variants": None,
        "character_formatting": {
            "stacked_characters": None,
            "slanted_characters": None,
            "slant_direction": None,
            "stack_position": None
        },
        "sticker_override": None
    }

def update_state_file(state_file: Path) -> Dict[str, int]:
    """Update a single state file with missing plate_characteristics"""
    stats = {
        'updated': 0,
        'skipped': 0,
        'total': 0
    }
    
    try:
        with open(state_file, 'r', encoding='utf-8') as f:
            state_data = json.load(f)
        
        if 'plate_types' not in state_data:
            print(f"  ⚠️  No plate_types array found, skipping")
            return stats
        
        modified = False
        
        for plate in state_data['plate_types']:
            stats['total'] += 1
            
            # Check if plate_characteristics exists
            if 'plate_characteristics' not in plate:
                # Add default structure
                plate['plate_characteristics'] = get_default_plate_characteristics()
                stats['updated'] += 1
                modified = True
            else:
                # Check if design_variants exists in existing plate_characteristics
                if 'design_variants' not in plate['plate_characteristics']:
                    plate['plate_characteristics']['design_variants'] = None
                    stats['updated'] += 1
                    modified = True
                else:
                    stats['skipped'] += 1
        
        # Save if modified
        if modified:
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(state_data, f, indent=2)
            print(f"  ✅ Updated {stats['updated']}/{stats['total']} plates")
        else:
            print(f"  ✓  Already up to date ({stats['total']} plates)")
        
        return stats
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return stats

def update_all_states():
    """Update all state files with missing structures"""
    states_dir = Path("data/states")
    state_files = sorted(states_dir.glob("*.json"))
    
    print(f"Updating {len(state_files)} state files...")
    print("=" * 70)
    
    total_stats = {
        'updated': 0,
        'skipped': 0,
        'total': 0,
        'files_modified': 0,
        'files_skipped': 0
    }
    
    for state_file in state_files:
        state_name = state_file.stem
        print(f"\n{state_name.upper()}:")
        
        stats = update_state_file(state_file)
        
        total_stats['updated'] += stats['updated']
        total_stats['skipped'] += stats['skipped']
        total_stats['total'] += stats['total']
        
        if stats['updated'] > 0:
            total_stats['files_modified'] += 1
        else:
            total_stats['files_skipped'] += 1
    
    print("\n" + "=" * 70)
    print("SUMMARY:")
    print("=" * 70)
    print(f"Files processed: {len(state_files)}")
    print(f"Files modified: {total_stats['files_modified']}")
    print(f"Files already OK: {total_stats['files_skipped']}")
    print(f"\nPlate types processed: {total_stats['total']}")
    print(f"Plate types updated: {total_stats['updated']}")
    print(f"Plate types already OK: {total_stats['skipped']}")
    print("=" * 70)
    
    if total_stats['files_modified'] > 0:
        print(f"\n✅ Successfully updated {total_stats['files_modified']} state files!")
    else:
        print("\n✅ All files already up to date!")

if __name__ == "__main__":
    update_all_states()
