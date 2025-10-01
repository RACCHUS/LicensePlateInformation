#!/usr/bin/env python3
"""
Multi-State License Plate System Validation
Comprehensive validation of all state implementations and O/0 character usage
"""

import json
import os
from pathlib import Path

def validate_state_files():
    """Validate all state JSON files for completeness and consistency"""
    
    states_dir = Path(__file__).parent.parent / 'data' / 'states'
    state_files = list(states_dir.glob('*.json'))
    
    print("MULTI-STATE LICENSE PLATE SYSTEM VALIDATION")
    print("=" * 50)
    print(f"Total state files found: {len(state_files)}")
    print()
    
    # Categories based on O/0 usage
    no_o_states = []
    o_with_letters_states = []
    o_only_personalized_states = []
    special_cases = []
    validation_errors = []
    
    for state_file in sorted(state_files):
        try:
            with open(state_file, 'r', encoding='utf-8') as f:
                state_data = json.load(f)
            
            state_name = state_data.get('name', 'Unknown')
            abbrev = state_data.get('abbreviation', 'XX')
            uses_zero = state_data.get('uses_zero_for_o', None)
            allows_o = state_data.get('allows_letter_o', None)
            
            # Categorize by O/0 usage
            if uses_zero is True and allows_o is False:
                # Check if it has conditional personalized plates
                has_personalized = any(
                    plate.get('processing_metadata', {}).get('dot_processing_type') == 'conditional'
                    for plate in state_data.get('plate_types', [])
                )
                if has_personalized:
                    o_only_personalized_states.append((state_name, abbrev))
                else:
                    no_o_states.append((state_name, abbrev))
            elif uses_zero is False and allows_o is True:
                o_with_letters_states.append((state_name, abbrev))
            else:
                special_cases.append((state_name, abbrev, uses_zero, allows_o))
            
            # Validate required fields
            required_fields = ['name', 'abbreviation', 'slogan', 'plate_types']
            missing_fields = [field for field in required_fields if field not in state_data]
            if missing_fields:
                validation_errors.append(f"{state_name}: Missing fields: {missing_fields}")
            
            # Validate plate types
            plate_types = state_data.get('plate_types', [])
            if not plate_types:
                validation_errors.append(f"{state_name}: No plate types defined")
            
            for plate in plate_types:
                if 'processing_metadata' not in plate:
                    validation_errors.append(f"{state_name}: Plate '{plate.get('type_name', 'Unknown')}' missing processing_metadata")
                else:
                    metadata = plate['processing_metadata']
                    if 'dot_processing_type' not in metadata:
                        validation_errors.append(f"{state_name}: Plate '{plate.get('type_name', 'Unknown')}' missing dot_processing_type")
                        
        except Exception as e:
            validation_errors.append(f"{state_file.name}: Error reading file - {str(e)}")
    
    # Print categorization results
    print("O/0 CHARACTER USAGE CATEGORIZATION:")
    print("-" * 40)
    
    print(f"\nNO O STATES ({len(no_o_states)}):")
    print("Uses only number '0', no letter 'O' on standard plates")
    for name, abbrev in sorted(no_o_states):
        print(f"  • {name} ({abbrev})")
    
    print(f"\nO WITH LETTERS STATES ({len(o_with_letters_states)}):")
    print("Uses 'O' with letters and '0' with numbers")
    for name, abbrev in sorted(o_with_letters_states):
        print(f"  • {name} ({abbrev})")
    
    print(f"\nO ONLY ON PERSONALIZED STATES ({len(o_only_personalized_states)}):")
    print("'O' only on personalized plates, standard uses '0'")
    for name, abbrev in sorted(o_only_personalized_states):
        print(f"  • {name} ({abbrev})")
    
    if special_cases:
        print(f"\nSPECIAL CASES ({len(special_cases)}):")
        for name, abbrev, uses_zero, allows_o in special_cases:
            print(f"  • {name} ({abbrev}): uses_zero={uses_zero}, allows_o={allows_o}")
    
    # Print validation results
    print(f"\nVALIDATION RESULTS:")
    print("-" * 20)
    
    if validation_errors:
        print(f"❌ VALIDATION ERRORS ({len(validation_errors)}):")
        for error in validation_errors[:10]:  # Show first 10 errors
            print(f"  • {error}")
        if len(validation_errors) > 10:
            print(f"  ... and {len(validation_errors) - 10} more errors")
    else:
        print("✅ ALL VALIDATIONS PASSED")
    
    # System summary
    total_categorized = len(no_o_states) + len(o_with_letters_states) + len(o_only_personalized_states)
    
    print(f"\nSYSTEM SUMMARY:")
    print("-" * 15)
    print(f"Total States: {len(state_files)}")
    print(f"Properly Categorized: {total_categorized}")
    print(f"Special Cases: {len(special_cases)}")
    print(f"Validation Errors: {len(validation_errors)}")
    
    # Check for comprehensive states
    comprehensive_states = []
    for state_file in state_files:
        with open(state_file, 'r', encoding='utf-8') as f:
            state_data = json.load(f)
        
        plate_count = len(state_data.get('plate_types', []))
        if plate_count > 10:  # Consider comprehensive if more than 10 plate types
            comprehensive_states.append((state_data['name'], plate_count))
    
    if comprehensive_states:
        print(f"\nCOMPREHENSIVE IMPLEMENTATIONS:")
        print("-" * 30)
        for name, count in sorted(comprehensive_states, key=lambda x: x[1], reverse=True):
            print(f"  • {name}: {count} plate types")
    
    print(f"\n🎯 SYSTEM STATUS: {'READY FOR PRODUCTION' if len(validation_errors) == 0 else 'NEEDS FIXES'}")
    
    return len(validation_errors) == 0

if __name__ == '__main__':
    success = validate_state_files()
    exit(0 if success else 1)