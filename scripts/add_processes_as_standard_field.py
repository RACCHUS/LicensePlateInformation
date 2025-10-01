#!/usr/bin/env python3
"""
Add processes_as_standard field to existing Florida JSON files
This field indicates whether a specialty plate processes through standard DOT system
"""

import json
import os
from pathlib import Path

def add_processes_as_standard_field():
    """Add the processes_as_standard field to Florida JSON files"""
    
    # File paths
    base_path = Path(__file__).parent.parent
    florida_files = [
        base_path / 'data' / 'states' / 'florida.json'
    ]
    
    for file_path in florida_files:
        if not file_path.exists():
            print(f"⚠️  File not found: {file_path}")
            continue
            
        print(f"📝 Processing: {file_path}")
        
        try:
            # Load existing JSON
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Count plates processed
            plates_updated = 0
            
            # Add processes_as_standard field to each plate type
            for plate in data.get('plate_types', []):
                if 'processing_metadata' in plate:
                    # Only add if not already present
                    if 'processes_as_standard' not in plate['processing_metadata']:
                        # Default to False (special processing) - user will specify which ones are standard
                        plate['processing_metadata']['processes_as_standard'] = False
                        plates_updated += 1
                else:
                    # Add processing_metadata if missing
                    plate['processing_metadata'] = {
                        'processes_as_standard': False
                    }
                    plates_updated += 1
            
            # Save updated JSON
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            
            print(f"✅ Updated {plates_updated} plate types in {file_path.name}")
            
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
    
    print("\n🎯 NEXT STEPS:")
    print("- All plate types now have 'processes_as_standard': false by default")
    print("- You can now specify which specialty plates actually process as standard")
    print("- Most specialty plates likely process as standard despite being categorized differently")
    print("- Government, emergency, and some commercial plates may require special processing")

if __name__ == '__main__':
    print("ADDING PROCESSES_AS_STANDARD FIELD TO FLORIDA DATA")
    print("=" * 60)
    add_processes_as_standard_field()