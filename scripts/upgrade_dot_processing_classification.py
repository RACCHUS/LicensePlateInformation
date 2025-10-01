#!/usr/bin/env python3
"""
Upgrade Florida data to comprehensive DOT processing classification
Replaces simple boolean with sophisticated processing type system
"""

import json
import os
from pathlib import Path

def upgrade_dot_processing_classification():
    """Upgrade Florida JSON files to comprehensive DOT processing classification"""
    
    # File paths
    base_path = Path(__file__).parent.parent
    florida_files = [
        base_path / 'data' / 'states' / 'florida.json'
    ]
    
    print("UPGRADING TO COMPREHENSIVE DOT PROCESSING CLASSIFICATION")
    print("=" * 70)
    
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
            
            # Upgrade each plate type's processing metadata
            for plate in data.get('plate_types', []):
                if 'processing_metadata' in plate:
                    proc_meta = plate['processing_metadata']
                    
                    # Remove old boolean field if it exists
                    old_value = proc_meta.pop('processes_as_standard', None)
                    
                    # Add new comprehensive fields
                    if 'dot_processing_type' not in proc_meta:
                        # Determine processing type based on category and characteristics
                        category = plate.get('category', '').lower()
                        type_name = plate.get('type_name', '').lower()
                        all_numeric = proc_meta.get('all_numeric_plate', False)
                        
                        # Classification logic
                        if category in ['government', 'military'] or 'fhp' in type_name or 'fdle' in type_name:
                            proc_meta['dot_processing_type'] = 'never_standard'
                            proc_meta['dot_dropdown_identifier'] = f"{category.upper()}_PLATES"
                            proc_meta['dot_conditional_rules'] = None
                        elif category in ['university', 'sports', 'conservation', 'specialty']:
                            if all_numeric:
                                proc_meta['dot_processing_type'] = 'conditional'
                                proc_meta['dot_dropdown_identifier'] = f"{category.upper()}_PLATES"
                                proc_meta['dot_conditional_rules'] = {
                                    "all_numeric": {
                                        "action": "use_dropdown",
                                        "dropdown": f"NUMERIC_{category.upper()}"
                                    },
                                    "alphanumeric": {
                                        "action": "standard_processing"
                                    }
                                }
                            else:
                                proc_meta['dot_processing_type'] = 'always_standard'
                                proc_meta['dot_dropdown_identifier'] = None
                                proc_meta['dot_conditional_rules'] = None
                        elif category in ['commercial', 'antique']:
                            proc_meta['dot_processing_type'] = 'never_standard'
                            proc_meta['dot_dropdown_identifier'] = f"{category.upper()}_PLATES"
                            proc_meta['dot_conditional_rules'] = None
                        elif category == 'veterans':
                            proc_meta['dot_processing_type'] = 'conditional'
                            proc_meta['dot_dropdown_identifier'] = 'VETERAN_PLATES'
                            proc_meta['dot_conditional_rules'] = {
                                "disabled_veteran": {
                                    "action": "use_dropdown",
                                    "dropdown": "DISABLED_VETERAN"
                                },
                                "standard_veteran": {
                                    "action": "standard_processing"
                                }
                            }
                        else:
                            # Default to unknown for manual classification
                            proc_meta['dot_processing_type'] = 'unknown'
                            proc_meta['dot_dropdown_identifier'] = None
                            proc_meta['dot_conditional_rules'] = None
                        
                        plates_updated += 1
            
            # Save updated JSON
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            
            print(f"✅ Upgraded {plates_updated} plate types in {file_path.name}")
            
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
    
    print("\n🎯 DOT PROCESSING CLASSIFICATION TYPES:")
    print("-" * 50)
    print("• always_standard: Always uses standard passenger processing")
    print("• never_standard: Always uses specific dropdown (has dot_dropdown_identifier)")
    print("• conditional: Uses standard OR dropdown based on rules (has dot_conditional_rules)")
    print("• unknown: Needs manual classification")
    print()
    print("🔍 EXAMPLES:")
    print("• University plates: conditional (standard unless all numeric)")
    print("• Government plates: never_standard (GOVERNMENT_PLATES dropdown)")
    print("• Veterans plates: conditional (standard unless disabled veteran)")
    print("• Conservation plates: always_standard (most cases)")
    print()
    print("📋 NEXT STEPS:")
    print("- Review and refine the automatic classifications")
    print("- Research actual DOT dropdown identifiers") 
    print("- Update conditional rules based on real DOT logic")
    print("- Test with actual plate processing scenarios")

if __name__ == '__main__':
    upgrade_dot_processing_classification()