#!/usr/bin/env python3
"""
UPDATE PLATE TYPE DROPDOWN - Main Script for Updating GUI Dropdown
Extracts plate types from all state JSON files and updates the dropdown component

MAIN COMMAND:
    python scripts/updating/update_plate_type_dropdown.py extract

OTHER COMMANDS:
    python scripts/updating/update_plate_type_dropdown.py list        # Show current plate types
    python scripts/updating/update_plate_type_dropdown.py add "Type"  # Add a plate type manually
    python scripts/updating/update_plate_type_dropdown.py remove "Type" # Remove a plate type
    python scripts/updating/update_plate_type_dropdown.py stats       # Show statistics

RUN THIS AFTER:
- Adding new states
- Adding new plate types to existing states
- Updating plate type names or descriptions
- Making any changes to plate_types sections in JSON files
"""

import json
import os
import sys
from typing import Set, List, Dict, Any, Optional
from pathlib import Path


class PlateTypeDropdownUpdater:
    """Updates the GUI dropdown component with plate types from all state JSON files"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.data_dir = self.project_root / "data" / "states"
        self.plate_types_file = self.project_root / "data" / "extracted_plate_types.json"
        
    def extract_from_json_files(self) -> Dict[str, Any]:
        """Extract all plate types from state JSON files"""
        print("🔍 Scanning JSON files for plate types...")
        
        all_plate_types = set()
        state_counts = {}
        extraction_metadata = {
            "extraction_date": "2025-09-30",
            "source_files": [],
            "total_unique_types": 0,
            "state_breakdown": {}
        }
        
        # Process all JSON files in the states directory
        json_files = list(self.data_dir.glob("*.json"))
        
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
                state_counts[state_abbr] = len(state_plate_types)
                extraction_metadata["state_breakdown"][state_abbr] = {
                    "name": state_name,
                    "plate_count": len(state_plate_types),
                    "types": sorted(list(state_plate_types))
                }
                extraction_metadata["source_files"].append(str(json_file.name))
                
                print(f"  ✅ {state_abbr}: {len(state_plate_types)} plate types")
                
            except Exception as e:
                print(f"  ❌ Error processing {json_file.name}: {e}")
        
        # Sort and prepare final data
        sorted_plate_types = sorted(list(all_plate_types))
        extraction_metadata["total_unique_types"] = len(sorted_plate_types)
        
        # Create the final data structure
        plate_types_data = {
            "metadata": extraction_metadata,
            "plate_types": sorted_plate_types
        }
        
        return plate_types_data
    
    def save_plate_types(self, data: Dict[str, Any]):
        """Save extracted plate types to file"""
        print(f"💾 Saving plate types to {self.plate_types_file}")
        
        # Ensure directory exists
        self.plate_types_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.plate_types_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Saved {len(data['plate_types'])} unique plate types")
    
    def load_plate_types(self) -> Dict[str, Any]:
        """Load plate types from file"""
        if not self.plate_types_file.exists():
            print(f"❌ Plate types file not found: {self.plate_types_file}")
            return {"metadata": {}, "plate_types": []}
        
        with open(self.plate_types_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def add_plate_type(self, plate_type: str):
        """Add a plate type manually"""
        data = self.load_plate_types()
        
        if plate_type in data["plate_types"]:
            print(f"⚠️  Plate type '{plate_type}' already exists")
            return
        
        data["plate_types"].append(plate_type)
        data["plate_types"].sort()
        
        # Update metadata
        if "metadata" not in data:
            data["metadata"] = {}
        data["metadata"]["manual_additions"] = data["metadata"].get("manual_additions", [])
        data["metadata"]["manual_additions"].append(plate_type)
        data["metadata"]["total_unique_types"] = len(data["plate_types"])
        
        self.save_plate_types(data)
        print(f"✅ Added plate type: '{plate_type}'")
    
    def remove_plate_type(self, plate_type: str):
        """Remove a plate type manually"""
        data = self.load_plate_types()
        
        if plate_type not in data["plate_types"]:
            print(f"⚠️  Plate type '{plate_type}' not found")
            return
        
        data["plate_types"].remove(plate_type)
        
        # Update metadata
        if "metadata" not in data:
            data["metadata"] = {}
        data["metadata"]["manual_removals"] = data["metadata"].get("manual_removals", [])
        data["metadata"]["manual_removals"].append(plate_type)
        data["metadata"]["total_unique_types"] = len(data["plate_types"])
        
        self.save_plate_types(data)
        print(f"✅ Removed plate type: '{plate_type}'")
    
    def show_statistics(self):
        """Show statistics about plate types"""
        data = self.load_plate_types()
        metadata = data.get("metadata", {})
        plate_types = data.get("plate_types", [])
        
        print("📊 PLATE TYPE STATISTICS")
        print("=" * 50)
        print(f"Total Unique Plate Types: {len(plate_types)}")
        print(f"Extraction Date: {metadata.get('extraction_date', 'Unknown')}")
        print(f"Source Files: {len(metadata.get('source_files', []))}")
        
        if "state_breakdown" in metadata:
            print(f"\nState Breakdown:")
            state_breakdown = metadata["state_breakdown"]
            for state_code, info in sorted(state_breakdown.items()):
                print(f"  {state_code}: {info['plate_count']} types ({info['name']})")
        
        if metadata.get("manual_additions"):
            print(f"\nManual Additions: {len(metadata['manual_additions'])}")
            for addition in metadata["manual_additions"]:
                print(f"  + {addition}")
        
        if metadata.get("manual_removals"):
            print(f"\nManual Removals: {len(metadata['manual_removals'])}")
            for removal in metadata["manual_removals"]:
                print(f"  - {removal}")
    
    def list_plate_types(self, limit: Optional[int] = None):
        """List all plate types"""
        data = self.load_plate_types()
        plate_types = data.get("plate_types", [])
        
        print(f"📋 PLATE TYPES ({len(plate_types)} total)")
        print("=" * 50)
        
        display_types = plate_types[:limit] if limit else plate_types
        
        for i, plate_type in enumerate(display_types, 1):
            print(f"{i:3d}. {plate_type}")
        
        if limit and len(plate_types) > limit:
            print(f"... and {len(plate_types) - limit} more")
    
    def extract_command(self):
        """Extract plate types from JSON files"""
        print("🚀 Starting plate type extraction...")
        data = self.extract_from_json_files()
        self.save_plate_types(data)
        self.show_statistics()
        print("\n🎉 Extraction complete!")


def main():
    """Main CLI interface"""
    manager = PlateTypeDropdownUpdater()
    
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    command = sys.argv[1].lower()
    
    if command == "extract":
        manager.extract_command()
    
    elif command == "list":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else None
        manager.list_plate_types(limit)
    
    elif command == "add":
        if len(sys.argv) < 3:
            print("❌ Usage: python dev_plate_type_manager.py add \"Plate Type Name\"")
            return
        manager.add_plate_type(sys.argv[2])
    
    elif command == "remove":
        if len(sys.argv) < 3:
            print("❌ Usage: python dev_plate_type_manager.py remove \"Plate Type Name\"")
            return
        manager.remove_plate_type(sys.argv[2])
    
    elif command == "stats":
        manager.show_statistics()
    
    else:
        print(f"❌ Unknown command: {command}")
        print(__doc__)


if __name__ == "__main__":
    main()