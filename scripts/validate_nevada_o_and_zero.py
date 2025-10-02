"""
Nevada Letter O and Number 0 Validation Script
Simple validation without unicode characters
"""

import json

# Load Nevada data
with open('data/states/nevada.json', 'r', encoding='utf-8') as f:
    nevada_data = json.load(f)

print("="*70)
print("NEVADA LETTER O AND NUMBER 0 VALIDATION")
print("="*70)
print()

# Check top-level fields
print("Top-Level Fields:")
print("   uses_zero_for_o:", nevada_data.get('uses_zero_for_o'))
print("   allows_letter_o:", nevada_data.get('allows_letter_o'))
print("   zero_is_slashed:", nevada_data.get('zero_is_slashed'))
print()

# Check letter_o_and_zero_usage
if 'letter_o_and_zero_usage' in nevada_data:
    print("Letter O and Zero Usage Structure: PRESENT")
    usage = nevada_data['letter_o_and_zero_usage']
    
    print("\n   Standard Plates:")
    if 'standard_plates' in usage:
        std = usage['standard_plates']
        print("     - Uses letter O:", std.get('uses_letter_o'))
        print("     - Uses number 0:", std.get('uses_number_zero'))
        print("     - Description:", std.get('description', 'N/A')[:80])
    
    print("\n   Personalized Plates:")
    if 'personalized_plates' in usage:
        pers = usage['personalized_plates']
        print("     - Uses letter O:", pers.get('uses_letter_o'))
        print("     - Uses number 0:", pers.get('uses_number_zero'))
        print("     - Visual distinction:", pers.get('visual_distinction', 'N/A')[:80])
else:
    print("Letter O and Zero Usage Structure: NOT FOUND")

print()

# Check processing_metadata
if 'processing_metadata' in nevada_data:
    meta = nevada_data['processing_metadata']
    print("Processing Metadata: PRESENT")
    
    if 'global_rules' in meta:
        rules = meta['global_rules']
        print("Global Rules: PRESENT")
        
        if 'character_restrictions' in rules:
            print("Character Restrictions: PRESENT")
            restrictions = rules['character_restrictions']
            
            if isinstance(restrictions, dict):
                print("\n   Character Restrictions Structure: DICT (Correct)")
                
                if 'standard_plates' in restrictions:
                    print("     Standard plates rules: DEFINED")
                    std = restrictions['standard_plates']
                    print("        - Uses letter O:", std.get('uses_letter_o'))
                    print("        - Uses number 0:", std.get('uses_number_zero'))
                
                if 'personalized_plates' in restrictions:
                    print("     Personalized plates rules: DEFINED")
                    pers = restrictions['personalized_plates']
                    print("        - Uses letter O:", pers.get('uses_letter_o'))
                    print("        - Uses number 0:", pers.get('uses_number_zero'))
                
                if 'summary' in restrictions:
                    print("\n   Summary:", restrictions['summary'][:120], "...")
            else:
                print("   Character restrictions: NOT A DICT (old format)")
        else:
            print("   Character restrictions: NOT FOUND")
    else:
        print("Global Rules: NOT FOUND")
else:
    print("Processing Metadata: NOT FOUND")

print()
print("="*70)
print("VALIDATION SUMMARY")
print("="*70)
print()

checks = [
    ("uses_zero_for_o is False", nevada_data.get('uses_zero_for_o') == False),
    ("allows_letter_o is True", nevada_data.get('allows_letter_o') == True),
    ("letter_o_and_zero_usage present", 'letter_o_and_zero_usage' in nevada_data),
    ("processing_metadata present", 'processing_metadata' in nevada_data),
    ("character_restrictions is dict", isinstance(nevada_data.get('processing_metadata', {}).get('global_rules', {}).get('character_restrictions'), dict)),
    ("standard_plates defined", 'standard_plates' in nevada_data.get('letter_o_and_zero_usage', {})),
    ("personalized_plates defined", 'personalized_plates' in nevada_data.get('letter_o_and_zero_usage', {}))
]

passed = sum(1 for _, check in checks if check)
total = len(checks)

for check_name, result in checks:
    status = "PASS" if result else "FAIL"
    print(f"[{status}] {check_name}")

print()
print(f"Validation Result: {passed}/{total} checks passed")

if passed == total:
    print()
    print("="*70)
    print("SUCCESS - NEVADA UPDATE COMPLETE - ALL VALIDATIONS PASSED!")
    print("="*70)
else:
    print()
    print("WARNING - Some validations failed - review needed")
