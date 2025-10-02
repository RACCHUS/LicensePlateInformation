"""
Florida Processing Types Validation Script
Validates all Florida plate types have proper processing type definitions.
"""

import json
from collections import Counter

def validate_florida_data():
    # Load Florida data
    with open('data/states/florida.json', 'r', encoding='utf-8') as f:
        florida_data = json.load(f)
    
    print("="*70)
    print("FLORIDA PROCESSING TYPES VALIDATION")
    print("="*70)
    print()
    
    # Basic counts
    total_plates = len(florida_data['plate_types'])
    print(f"✅ Total plate types: {total_plates}")
    
    # Check all plates have processing_type
    with_processing_type = sum(1 for p in florida_data['plate_types'] if 'processing_type' in p)
    print(f"✅ Plates with processing_type: {with_processing_type}/{total_plates}")
    
    # Check all plates have processing_info
    with_processing_info = sum(1 for p in florida_data['plate_types'] if 'processing_info' in p)
    print(f"✅ Plates with processing_info: {with_processing_info}/{total_plates}")
    
    # Check processing types defined in metadata
    has_metadata = 'processing_types' in florida_data['processing_metadata']
    print(f"✅ Processing types in metadata: {has_metadata}")
    
    if has_metadata:
        processing_types_count = len(florida_data['processing_metadata']['processing_types'])
        print(f"✅ Unique processing types defined: {processing_types_count}")
    
    print()
    print("="*70)
    print("PROCESSING TYPE VALIDATION")
    print("="*70)
    print()
    
    # Count processing types
    processing_type_counts = Counter()
    for plate in florida_data['plate_types']:
        pt = plate.get('processing_type', 'MISSING')
        processing_type_counts[pt] += 1
    
    print("Processing type distribution:")
    for pt, count in processing_type_counts.most_common():
        percentage = (count / total_plates * 100) if total_plates > 0 else 0
        status = "✅" if pt != 'MISSING' else "❌"
        print(f"  {status} {pt:.<45} {count:>4} ({percentage:>5.1f}%)")
    
    print()
    print("="*70)
    print("DROPDOWN PLATES VALIDATION")
    print("="*70)
    print()
    
    # Check dropdown plates
    dropdown_plates = []
    for plate in florida_data['plate_types']:
        if plate.get('processing_info', {}).get('requires_dropdown', False):
            dropdown_plates.append(plate)
    
    expected_dropdown = [
        ("Seminole Indian", "125"),
        ("Seminole Indian Motorcycle", "125"),
        ("Miccosukee Indian", "129"),
        ("Miccosukee Indian Motorcycle", "129"),
        ("State Senator", "127"),
        ("House Speaker", "123"),
        ("Member of Congress", "124"),
        ("US Senator", "128")
    ]
    
    print(f"Expected dropdown plates: {len(expected_dropdown)}")
    print(f"Found dropdown plates: {len(dropdown_plates)}")
    print()
    
    # Check each expected dropdown plate
    all_found = True
    for name, code in expected_dropdown:
        found = any(p['type_name'] == name and p.get('code_number') == code for p in dropdown_plates)
        status = "✅" if found else "❌"
        print(f"  {status} {name} (Code {code})")
        if not found:
            all_found = False
    
    if all_found:
        print()
        print("✅ All expected dropdown plates found!")
    
    print()
    print("="*70)
    print("EXCEPTION PLATES VALIDATION")
    print("="*70)
    print()
    
    # Check exception plates (Official/Retired)
    exception_plates = []
    for plate in florida_data['plate_types']:
        if 'official' in plate['type_name'].lower() or 'retired' in plate['type_name'].lower():
            exception_plates.append(plate)
    
    expected_exceptions = [
        "Official Congress",
        "Official House",
        "Official Senate",
        "Retired House",
        "Retired Senate"
    ]
    
    print(f"Expected exception plates: {len(expected_exceptions)}")
    print(f"Found exception plates: {len(exception_plates)}")
    print()
    
    # Check each exception plate
    all_correct = True
    for name in expected_exceptions:
        plate = next((p for p in florida_data['plate_types'] if p['type_name'] == name), None)
        if plate:
            is_standard = plate.get('processing_type') == 'standard'
            no_dropdown = not plate.get('processing_info', {}).get('requires_dropdown', False)
            has_note = 'special_note' in plate.get('processing_info', {})
            
            status = "✅" if (is_standard and no_dropdown) else "❌"
            note_status = "✅" if has_note else "⚠️"
            print(f"  {status} {name}")
            print(f"     Processing type: {plate.get('processing_type')}")
            print(f"     Requires dropdown: {plate.get('processing_info', {}).get('requires_dropdown', False)}")
            print(f"     {note_status} Has special note: {has_note}")
            
            if not (is_standard and no_dropdown):
                all_correct = False
        else:
            print(f"  ❌ {name} - NOT FOUND")
            all_correct = False
    
    if all_correct:
        print()
        print("✅ All exception plates correctly configured!")
    
    print()
    print("="*70)
    print("CODE DISTRIBUTION VALIDATION")
    print("="*70)
    print()
    
    # Check code distribution
    code_counts = Counter()
    for plate in florida_data['plate_types']:
        code = plate.get('code_number', '0')
        code_counts[code] += 1
    
    print(f"Total unique codes: {len(code_counts)}")
    print()
    print("Top 10 codes:")
    for code, count in code_counts.most_common(10):
        print(f"  Code {code:.<6} {count:>4} plates")
    
    # Check dropdown codes specifically
    print()
    print("Dropdown codes validation:")
    dropdown_codes = ['123', '124', '125', '127', '128', '129']
    for code in dropdown_codes:
        count = code_counts.get(code, 0)
        status = "✅" if count > 0 else "❌"
        print(f"  {status} Code {code}: {count} plate(s)")
    
    print()
    print("="*70)
    print("GLOBAL RULES VALIDATION")
    print("="*70)
    print()
    
    # Check global rules
    global_rules = florida_data.get('processing_metadata', {}).get('global_rules', {})
    
    rules_to_check = [
        ('no_letter_o', 'Letter O restriction'),
        ('font_changes', 'Font changes'),
        ('code_system', 'Code system'),
        ('has_variable_processing_types', 'Variable processing types')
    ]
    
    for rule_key, rule_name in rules_to_check:
        has_rule = rule_key in global_rules
        status = "✅" if has_rule else "❌"
        print(f"  {status} {rule_name}: {has_rule}")
    
    print()
    print("="*70)
    print("FINAL VALIDATION SUMMARY")
    print("="*70)
    print()
    
    # Overall validation
    checks = []
    checks.append(("All plates have processing_type", with_processing_type == total_plates))
    checks.append(("All plates have processing_info", with_processing_info == total_plates))
    checks.append(("Processing types defined in metadata", has_metadata))
    checks.append(("No missing processing types", processing_type_counts.get('MISSING', 0) == 0))
    checks.append(("All dropdown plates found", all_found))
    checks.append(("All exception plates correct", all_correct))
    checks.append(("Global rules present", all(rule_key in global_rules for rule_key, _ in rules_to_check)))
    
    passed = sum(1 for _, check in checks if check)
    total_checks = len(checks)
    
    for check_name, result in checks:
        status = "✅" if result else "❌"
        print(f"{status} {check_name}")
    
    print()
    print(f"Validation Result: {passed}/{total_checks} checks passed")
    
    if passed == total_checks:
        print()
        print("🎉 " + "="*66)
        print("🎉 ALL VALIDATIONS PASSED - FLORIDA IS PRODUCTION READY!")
        print("🎉 " + "="*66)
        return True
    else:
        print()
        print("⚠️  " + "="*66)
        print("⚠️  SOME VALIDATIONS FAILED - REVIEW REQUIRED")
        print("⚠️  " + "="*66)
        return False

if __name__ == "__main__":
    validate_florida_data()
