#!/usr/bin/env python3
"""
Migrate Legacy State Files to New Processing Metadata Format
Updates older state files to include comprehensive processing metadata
"""

import json
import os
from pathlib import Path

def migrate_legacy_state_file(state_file_path):
    """Migrate a legacy state file to new format with processing metadata"""
    
    with open(state_file_path, 'r', encoding='utf-8') as f:
        state_data = json.load(f)
    
    state_name = state_data.get('name', 'Unknown')
    print(f"Migrating {state_name}...")
    
    # Add processing_metadata to state level if missing
    if 'processing_metadata' not in state_data:
        state_data['processing_metadata'] = {
            "description": f"Official {state_name} DMV processing rules and validation requirements",
            "global_rules": {
                "font_changes": "Information needed - check historical changes",
                "code_system": "Information needed - research plate type code system"
            }
        }
    
    # Determine character restrictions based on O/0 usage
    uses_zero = state_data.get('uses_zero_for_o', False)
    allows_o = state_data.get('allows_letter_o', True)
    
    if uses_zero and not allows_o:
        char_restriction = "Does not use letter 'O' on standard plates - only number zero '0'"
    elif not uses_zero and allows_o:
        char_restriction = "Uses both O and 0 - O with letters, 0 with numbers"
    else:
        char_restriction = "Mixed O/0 usage - requires verification"
    
    state_data['processing_metadata']['global_rules']['character_restrictions'] = char_restriction
    
    # Update each plate type
    plates_updated = 0
    for plate in state_data.get('plate_types', []):
        if 'processing_metadata' not in plate:
            # Add comprehensive processing metadata
            plate['processing_metadata'] = {
                "currently_processed": True,
                "requires_prefix": plate.get('requires_prefix', False),
                "requires_suffix": False,
                "character_modifications": None,
                "verify_state_abbreviation": True,
                "visual_identifier": None,
                "vehicle_type_identification": None,
                "all_numeric_plate": False,
                "dot_processing_type": "always_standard",  # Default for most plates
                "dot_dropdown_identifier": None,
                "dot_conditional_rules": None,
                "date_ranges": {"period_1": None, "period_2": None},
                "plate_images_available": None
            }
            
            # Adjust DOT processing type based on plate category
            category = plate.get('category', 'passenger')
            type_name = plate.get('type_name', '').lower()
            
            if 'commercial' in type_name or 'truck' in type_name:
                plate['processing_metadata']['dot_processing_type'] = 'never_standard'
                plate['processing_metadata']['dot_dropdown_identifier'] = 'COMMERCIAL_PLATES'
            elif 'personalized' in type_name or 'vanity' in type_name or 'custom' in type_name:
                plate['processing_metadata']['dot_processing_type'] = 'conditional'
                plate['processing_metadata']['dot_dropdown_identifier'] = 'PERSONALIZED_PLATES'
                plate['processing_metadata']['dot_conditional_rules'] = {
                    "plate_type": {
                        "action": "allow_letter_o" if allows_o else "use_zero_for_o",
                        "description": f"{'Letter O allowed' if allows_o else 'Use zero for O'} on personalized plates"
                    }
                }
            elif 'antique' in type_name or 'classic' in type_name or 'vintage' in type_name:
                plate['processing_metadata']['dot_processing_type'] = 'conditional'
                plate['processing_metadata']['dot_dropdown_identifier'] = 'ANTIQUE_PLATES'
            
            plates_updated += 1
    
    # Add source attribution note if missing
    if 'notes' not in state_data:
        if uses_zero and not allows_o:
            usage_note = f"{state_name} does not use the letter 'O' on standard plates. Only the number zero '0' is used to avoid confusion."
        elif not uses_zero and allows_o:
            usage_note = f"{state_name} uses letter 'O' with letters/personalized plates and number '0' with numbers. Standard format varies."
        else:
            usage_note = f"{state_name} has mixed O/0 usage patterns."
        
        state_data['notes'] = f"{usage_note} Migrated to new processing metadata format - requires verification with official DMV documentation."
    
    # Write updated file
    with open(state_file_path, 'w', encoding='utf-8') as f:
        json.dump(state_data, f, indent=2)
    
    print(f"  ✅ Updated {plates_updated} plate types with processing metadata")
    return plates_updated

def main():
    """Main migration function"""
    
    states_dir = Path(__file__).parent.parent / 'data' / 'states'
    state_files = list(states_dir.glob('*.json'))
    
    print("LEGACY STATE FILE MIGRATION TO NEW PROCESSING METADATA FORMAT")
    print("=" * 65)
    print(f"Found {len(state_files)} state files to check\n")
    
    total_migrated = 0
    total_plates_updated = 0
    files_needing_migration = []
    
    # First pass - identify files needing migration
    for state_file in sorted(state_files):
        try:
            with open(state_file, 'r', encoding='utf-8') as f:
                state_data = json.load(f)
            
            needs_migration = False
            
            # Check if any plate lacks processing_metadata
            for plate in state_data.get('plate_types', []):
                if 'processing_metadata' not in plate:
                    needs_migration = True
                    break
            
            if needs_migration:
                files_needing_migration.append(state_file)
                
        except Exception as e:
            print(f"❌ Error checking {state_file.name}: {str(e)}")
    
    print(f"Files needing migration: {len(files_needing_migration)}")
    
    if not files_needing_migration:
        print("✅ All state files already have proper processing metadata!")
        return
    
    print("\nMigrating files:")
    print("-" * 20)
    
    # Second pass - migrate files
    for state_file in files_needing_migration:
        try:
            plates_updated = migrate_legacy_state_file(state_file)
            total_migrated += 1
            total_plates_updated += plates_updated
            
        except Exception as e:
            print(f"❌ Error migrating {state_file.name}: {str(e)}")
    
    print(f"\nMIGRATION SUMMARY:")
    print("-" * 18)
    print(f"Files migrated: {total_migrated}")
    print(f"Plate types updated: {total_plates_updated}")
    print(f"✅ Migration complete!")
    
    print(f"\nRecommended next steps:")
    print(f"1. Run validation script to verify all files")
    print(f"2. Review migrated files for accuracy")
    print(f"3. Update with official DMV data where available")

if __name__ == '__main__':
    main()