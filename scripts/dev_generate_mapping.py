"""
Enhanced Plate Type Manager - Adds state-to-plate-type mapping functionality
"""

import json
import os
from typing import Dict, List, Set
from pathlib import Path


class EnhancedPlateTypeManager:
    """Enhanced manager with state-to-plate-type mapping"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.data_dir = self.project_root / "data" / "states"
        self.mapping_file = self.project_root / "data" / "state_plate_type_mapping.json"
        
    def generate_state_mapping(self) -> Dict:
        """Generate bidirectional mapping between states and plate types"""
        print("🔍 Generating state-to-plate-type mapping...")
        
        # plate_type -> [states]
        plate_type_to_states = {}
        # state -> [plate_types]  
        state_to_plate_types = {}
        
        json_files = list(self.data_dir.glob("*.json"))
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                state_abbr = data.get('abbreviation', json_file.stem.upper())
                state_name = data.get('name', json_file.stem.title())
                
                # Get plate types for this state
                plate_types = data.get('plate_types', [])
                state_plate_list = []
                
                for plate in plate_types:
                    type_name = plate.get('type_name', '').strip()
                    if type_name:
                        state_plate_list.append(type_name)
                        
                        # Add to plate_type -> states mapping
                        if type_name not in plate_type_to_states:
                            plate_type_to_states[type_name] = []
                        plate_type_to_states[type_name].append(state_abbr)
                
                # Add to state -> plate_types mapping
                state_to_plate_types[state_abbr] = {
                    "name": state_name,
                    "plate_types": sorted(state_plate_list)
                }
                
                print(f"  ✅ {state_abbr}: {len(state_plate_list)} plate types")
                
            except Exception as e:
                print(f"  ❌ Error processing {json_file.name}: {e}")
        
        # Sort everything
        for plate_type in plate_type_to_states:
            plate_type_to_states[plate_type].sort()
        
        mapping_data = {
            "metadata": {
                "generation_date": "2025-09-30",
                "total_states": len(state_to_plate_types),
                "total_plate_types": len(plate_type_to_states)
            },
            "plate_type_to_states": plate_type_to_states,
            "state_to_plate_types": state_to_plate_types
        }
        
        return mapping_data
    
    def save_mapping(self, data: Dict):
        """Save the mapping data"""
        print(f"💾 Saving mapping to {self.mapping_file}")
        
        self.mapping_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.mapping_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Saved mapping for {data['metadata']['total_states']} states and {data['metadata']['total_plate_types']} plate types")
    
    def generate_command(self):
        """Generate the state-plate-type mapping"""
        print("🚀 Generating state-to-plate-type mapping...")
        data = self.generate_state_mapping()
        self.save_mapping(data)
        
        print("\n📊 MAPPING STATISTICS")
        print("=" * 40)
        print(f"States processed: {data['metadata']['total_states']}")
        print(f"Unique plate types: {data['metadata']['total_plate_types']}")
        
        # Show some examples
        print(f"\nExample - States with 'Passenger Default':")
        if 'Passenger Default' in data['plate_type_to_states']:
            states = data['plate_type_to_states']['Passenger Default']
            print(f"  {', '.join(states[:10])}{'...' if len(states) > 10 else ''}")
        
        print(f"\nExample - Florida plate types (first 10):")
        if 'FL' in data['state_to_plate_types']:
            fl_types = data['state_to_plate_types']['FL']['plate_types']
            print(f"  {', '.join(fl_types[:10])}{'...' if len(fl_types) > 10 else ''}")
        
        print("\n🎉 Mapping generation complete!")


if __name__ == "__main__":
    manager = EnhancedPlateTypeManager()
    manager.generate_command()