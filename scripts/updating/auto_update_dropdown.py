#!/usr/bin/env python3
"""
AUTO UPDATE DROPDOWN - Simple One-Click Script
Automatically extracts plate types from all state JSON files and updates the dropdown

USAGE:
    Just double-click this file or run: python auto_update_dropdown.py
    
No commands needed! This script will:
1. Scan all state JSON files
2. Extract all plate types
3. Update the dropdown data file
4. Show you a summary

Run this after:
- Adding new states
- Adding new plate types to existing states
- Updating any state JSON files
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


def generate_state_mapping(project_root: Path, state_breakdown: dict, all_plate_types: list):
    """Generate the state-to-plate-type mapping file that the app uses"""
    
    # Create bidirectional mapping
    plate_type_to_states = {}
    
    # Build plate_type -> [states] mapping
    for state_code, info in state_breakdown.items():
        for plate_type in info['types']:
            if plate_type not in plate_type_to_states:
                plate_type_to_states[plate_type] = []
            plate_type_to_states[plate_type].append(state_code)
    
    # Sort states for each plate type
    for plate_type in plate_type_to_states:
        plate_type_to_states[plate_type].sort()
    
    mapping_data = {
        "metadata": {
            "generation_date": datetime.now().strftime("%Y-%m-%d"),
            "total_states": len(state_breakdown),
            "total_plate_types": len(plate_type_to_states)
        },
        "plate_type_to_states": plate_type_to_states,
        "state_to_plate_types": {
            code: {
                "name": info["name"],
                "plate_types": info["types"]
            }
            for code, info in state_breakdown.items()
        }
    }
    
    # Save mapping file
    mapping_file = project_root / "data" / "state_plate_type_mapping.json"
    with open(mapping_file, 'w', encoding='utf-8') as f:
        json.dump(mapping_data, f, indent=2, ensure_ascii=False)
    
    print(f"  ✅ Saved state mapping to: {mapping_file.name}")
    print(f"  ✅ Mapping contains {len(plate_type_to_states)} plate types and {len(state_breakdown)} states")


def main():
    """Automatically update plate type dropdown data"""
    
    print("=" * 60)
    print("🚀 AUTO UPDATE PLATE TYPE DROPDOWN")
    print("=" * 60)
    print()
    
    # Setup paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    data_dir = project_root / "data" / "states"
    output_file = project_root / "data" / "extracted_plate_types.json"
    
    print(f"📁 Scanning directory: {data_dir}")
    print()
    
    # Extract plate types
    all_plate_types = set()
    state_breakdown = {}
    source_files = []
    
    json_files = sorted(data_dir.glob("*.json"))
    
    if not json_files:
        print("❌ No JSON files found in the states directory!")
        input("Press Enter to exit...")
        return
    
    print(f"🔍 Processing {len(json_files)} state files...")
    print()
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            state_name = data.get('name', json_file.stem.title())
            state_abbr = data.get('abbreviation', json_file.stem.upper())
            
            # Extract plate types
            plate_types = data.get('plate_types', [])
            state_plate_types = set()
            
            for plate in plate_types:
                type_name = plate.get('type_name', '').strip()
                if type_name:
                    all_plate_types.add(type_name)
                    state_plate_types.add(type_name)
            
            # Track state information
            state_breakdown[state_abbr] = {
                "name": state_name,
                "plate_count": len(state_plate_types),
                "types": sorted(list(state_plate_types))
            }
            source_files.append(json_file.name)
            
            # Show progress
            status = "✅" if len(state_plate_types) > 0 else "⚠️"
            print(f"  {status} {state_abbr:4s} - {state_name:30s} ({len(state_plate_types):3d} plate types)")
            
        except Exception as e:
            print(f"  ❌ Error processing {json_file.name}: {e}")
    
    print()
    print("-" * 60)
    
    # Prepare final data
    sorted_plate_types = sorted(list(all_plate_types))
    
    output_data = {
        "metadata": {
            "extraction_date": datetime.now().strftime("%Y-%m-%d"),
            "extraction_time": datetime.now().strftime("%H:%M:%S"),
            "source_files": sorted(source_files),
            "total_unique_types": len(sorted_plate_types),
            "total_states_processed": len(json_files),
            "state_breakdown": dict(sorted(state_breakdown.items()))
        },
        "plate_types": sorted_plate_types
    }
    
    # Save to file
    print(f"💾 Saving to: {output_file}")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print()
    print("=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"✅ Total Unique Plate Types: {len(sorted_plate_types)}")
    print(f"✅ States Processed: {len(json_files)}")
    print(f"✅ Output File: {output_file.name}")
    print()
    
    # Show top states by plate count
    top_states = sorted(state_breakdown.items(), 
                       key=lambda x: x[1]['plate_count'], 
                       reverse=True)[:5]
    
    print("🏆 Top 5 States by Plate Types:")
    for state_code, info in top_states:
        print(f"   {state_code}: {info['plate_count']:3d} types - {info['name']}")
    
    print()
    print("=" * 60)
    print("🎉 DROPDOWN DATA UPDATED SUCCESSFULLY!")
    print("=" * 60)
    print()
    
    # Also generate the state mapping file that the app uses
    print("🔄 Generating state-to-plate-type mapping...")
    print()
    generate_state_mapping(project_root, state_breakdown, sorted_plate_types)
    
    print()
    print("=" * 60)
    print("✅ ALL UPDATES COMPLETE!")
    print("=" * 60)
    print()
    print("The dropdown component will now show all available plate types")
    print("from all state JSON files when you restart the application.")
    print()
    
    # Pause so user can see the results
    input("Press Enter to close...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Update cancelled by user")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"\n\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
