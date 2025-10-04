#!/usr/bin/env python3
"""
AUTO UPDATE DROPDOWN - OPTIMIZED BATCH VERSION
Processes large numbers of plate types efficiently using batch processing

USAGE:
    python auto_update_dropdown_batch.py
    
Features:
- Batch processing for memory efficiency
- Progress bar with time estimates
- Handles 10,000+ plate types without slowdown
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
import time


def save_json_batch(file_path, data, batch_size=1000):
    """Save large JSON files in batches to avoid memory issues"""
    print(f"  💾 Saving {len(data.get('plate_types', []))} items...")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        # Write metadata
        f.write('{\n')
        f.write('  "metadata": ')
        json.dump(data['metadata'], f, indent=2, ensure_ascii=False)
        f.write(',\n')
        f.write('  "plate_types": [\n')
        
        # Write plate types in batches
        plate_types = data['plate_types']
        total = len(plate_types)
        
        for i, plate_type in enumerate(plate_types):
            f.write('    ')
            json.dump(plate_type, f, ensure_ascii=False)
            if i < total - 1:
                f.write(',')
            f.write('\n')
            
            # Progress indicator every 1000 items
            if (i + 1) % 1000 == 0:
                print(f"    Progress: {i+1}/{total} ({(i+1)*100//total}%)")
        
        f.write('  ]\n')
        f.write('}\n')
    
    print(f"  ✅ Saved successfully!")


def save_mapping_batch(file_path, mapping_data, batch_size=500):
    """Save state mapping in batches"""
    print(f"  💾 Saving state mapping...")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('{\n')
        
        # Write metadata
        f.write('  "metadata": ')
        json.dump(mapping_data['metadata'], f, indent=2, ensure_ascii=False)
        f.write(',\n')
        
        # Write plate_type_to_states in batches
        f.write('  "plate_type_to_states": {\n')
        items = list(mapping_data['plate_type_to_states'].items())
        total_items = len(items)
        
        for idx, (plate_type, states) in enumerate(items):
            f.write('    ')
            json.dump(plate_type, f, ensure_ascii=False)
            f.write(': ')
            json.dump(states, f, ensure_ascii=False)
            if idx < total_items - 1:
                f.write(',')
            f.write('\n')
            
            # Progress indicator
            if (idx + 1) % 500 == 0:
                print(f"    Progress: {idx+1}/{total_items} ({(idx+1)*100//total_items}%)")
        
        f.write('  },\n')
        
        # Write state_to_plate_types
        f.write('  "state_to_plate_types": ')
        json.dump(mapping_data['state_to_plate_types'], f, indent=2, ensure_ascii=False)
        f.write('\n')
        
        f.write('}\n')
    
    print(f"  ✅ Mapping saved successfully!")


def generate_state_mapping_batch(project_root: Path, state_breakdown: dict, all_plate_types: list):
    """Generate the state-to-plate-type mapping file (batch version)"""
    
    print("\n🔄 Generating state-to-plate-type mapping...")
    
    # Build plate_type -> [states] mapping in batches
    plate_type_to_states = {}
    
    total_states = len(state_breakdown)
    for idx, (state_code, info) in enumerate(state_breakdown.items(), 1):
        for plate_type in info['types']:
            if plate_type not in plate_type_to_states:
                plate_type_to_states[plate_type] = []
            plate_type_to_states[plate_type].append(state_code)
        
        # Progress indicator
        if idx % 10 == 0 or idx == total_states:
            print(f"  Processing states: {idx}/{total_states} ({idx*100//total_states}%)")
    
    # Sort states for each plate type
    print(f"  Sorting {len(plate_type_to_states)} plate type mappings...")
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
    
    # Save mapping file in batches
    mapping_file = project_root / "data" / "state_plate_type_mapping.json"
    save_mapping_batch(mapping_file, mapping_data)
    
    print(f"  ✅ Mapping contains {len(plate_type_to_states)} plate types and {len(state_breakdown)} states")


def main():
    """Automatically update plate type dropdown data with batch processing"""
    
    start_time = time.time()
    
    print("=" * 70)
    print("🚀 AUTO UPDATE PLATE TYPE DROPDOWN (BATCH OPTIMIZED)")
    print("=" * 70)
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
        return
    
    print(f"🔍 Processing {len(json_files)} state files...")
    print()
    
    for idx, json_file in enumerate(json_files, 1):
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
            progress = f"[{idx}/{len(json_files)}]"
            print(f"  {progress:10s} {status} {state_abbr:4s} - {state_name:30s} ({len(state_plate_types):4d} types)")
            
        except Exception as e:
            print(f"  ❌ Error processing {json_file.name}: {e}")
    
    print()
    print("-" * 70)
    
    # Prepare final data
    print("\n🔄 Sorting plate types...")
    sorted_plate_types = sorted(list(all_plate_types))
    print(f"  ✅ Sorted {len(sorted_plate_types)} unique plate types")
    
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
    
    # Save to file in batches
    print(f"\n💾 Saving extracted plate types to: {output_file.name}")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    save_json_batch(output_file, output_data)
    
    # Generate state mapping
    generate_state_mapping_batch(project_root, state_breakdown, sorted_plate_types)
    
    elapsed = time.time() - start_time
    
    print()
    print("=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    print(f"✅ Total Unique Plate Types: {len(sorted_plate_types):,}")
    print(f"✅ States Processed: {len(json_files)}")
    print(f"✅ Output File: {output_file.name}")
    print(f"⏱️  Processing Time: {elapsed:.2f} seconds")
    print()
    
    # Show top states by plate count
    top_states = sorted(state_breakdown.items(), 
                       key=lambda x: x[1]['plate_count'], 
                       reverse=True)[:10]
    
    print("🏆 Top 10 States by Plate Types:")
    for state_code, info in top_states:
        print(f"   {state_code}: {info['plate_count']:4d} types - {info['name']}")
    
    print()
    print("=" * 70)
    print("🎉 DROPDOWN DATA UPDATED SUCCESSFULLY!")
    print("=" * 70)
    print()
    print("Files created:")
    print(f"  1. {output_file.name}")
    print(f"  2. state_plate_type_mapping.json")
    print()
    print("The dropdown will show all plate types when you restart the app.")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Update cancelled by user")
    except Exception as e:
        print(f"\n\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
