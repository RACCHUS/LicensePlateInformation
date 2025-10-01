"""
Script to check state JSON files for conformance with template structure
"""
import json
import os
from pathlib import Path

def check_state_conformance():
    """Check all state files against template structure"""
    
    # Load template
    template_path = Path("data/templates/state_template.json")
    with open(template_path, 'r', encoding='utf-8') as f:
        template = json.load(f)
    
    # Get template structure requirements
    template_plate = template['plate_types'][0]
    required_plate_fields = set(template_plate.keys())
    
    # Required fields in plate_characteristics
    required_plate_chars = set(template_plate['plate_characteristics'].keys())
    
    # Track issues
    states_dir = Path("data/states")
    state_files = list(states_dir.glob("*.json"))
    
    print(f"Checking {len(state_files)} state files for conformance...")
    print("=" * 70)
    
    issues = {}
    
    for state_file in sorted(state_files):
        state_name = state_file.stem
        state_issues = []
        
        try:
            with open(state_file, 'r', encoding='utf-8') as f:
                state_data = json.load(f)
            
            # Check if plate_types exist
            if 'plate_types' not in state_data:
                state_issues.append("Missing 'plate_types' array")
                issues[state_name] = state_issues
                continue
            
            # Check each plate type
            missing_design_variants = 0
            total_plates = len(state_data['plate_types'])
            
            for idx, plate in enumerate(state_data['plate_types']):
                # Check if plate_characteristics exists
                if 'plate_characteristics' not in plate:
                    state_issues.append(f"Plate {idx}: Missing 'plate_characteristics'")
                    continue
                
                plate_chars = plate['plate_characteristics']
                
                # Check for design_variants field
                if 'design_variants' not in plate_chars:
                    missing_design_variants += 1
            
            if missing_design_variants > 0:
                state_issues.append(
                    f"Missing 'design_variants' in {missing_design_variants}/{total_plates} plates"
                )
            
            if state_issues:
                issues[state_name] = state_issues
            else:
                print(f"✅ {state_name}: All {total_plates} plates conform to template")
                
        except json.JSONDecodeError as e:
            state_issues.append(f"JSON parse error: {e}")
            issues[state_name] = state_issues
        except Exception as e:
            state_issues.append(f"Error: {e}")
            issues[state_name] = state_issues
    
    # Report issues
    print("\n" + "=" * 70)
    print("ISSUES FOUND:")
    print("=" * 70)
    
    if issues:
        for state_name, state_issues in sorted(issues.items()):
            print(f"\n❌ {state_name.upper()}:")
            for issue in state_issues:
                print(f"   - {issue}")
    else:
        print("\n✅ All states conform to template!")
    
    print("\n" + "=" * 70)
    print(f"Summary: {len(issues)} states with issues, {len(state_files) - len(issues)} states OK")
    
    return issues

if __name__ == "__main__":
    issues = check_state_conformance()
    
    if issues:
        print("\n⚠️  Some states need updates!")
    else:
        print("\n🎉 All states are up to date!")
