"""
Comprehensive State JSON Validator
Checks for missing required fields, unexpected fields, and structural conformance
"""
import json
from pathlib import Path
from typing import Dict, List, Set, Any, Tuple
from collections import defaultdict


class TemplateValidator:
    """Validates state JSON files against the template structure"""
    
    def __init__(self, template_path: str = "data/templates/state_template.json"):
        with open(template_path, 'r', encoding='utf-8') as f:
            self.template = json.load(f)
        
        # Extract expected structures
        self.root_fields = set(self.template.keys())
        self.plate_type_fields = set(self.template['plate_types'][0].keys())
        self.plate_characteristics_fields = set(
            self.template['plate_types'][0]['plate_characteristics'].keys()
        )
        self.character_formatting_fields = set(
            self.template['plate_types'][0]['plate_characteristics']['character_formatting'].keys()
        )
        self.processing_metadata_fields = set(
            self.template['plate_types'][0]['processing_metadata'].keys()
        )
        self.images_fields = set(
            self.template['plate_types'][0]['images'].keys()
        )
        
    def validate_state(self, state_file: Path) -> Dict[str, List[str]]:
        """Validate a single state file"""
        issues = defaultdict(list)
        
        try:
            with open(state_file, 'r', encoding='utf-8') as f:
                state_data = json.load(f)
        except json.JSONDecodeError as e:
            issues['critical'].append(f"JSON parse error: {e}")
            return dict(issues)
        except Exception as e:
            issues['critical'].append(f"File read error: {e}")
            return dict(issues)
        
        # Check root level fields
        state_root_fields = set(state_data.keys())
        missing_root = self.root_fields - state_root_fields
        extra_root = state_root_fields - self.root_fields
        
        if missing_root:
            issues['missing_root_fields'].extend(sorted(missing_root))
        if extra_root:
            issues['unexpected_root_fields'].extend(sorted(extra_root))
        
        # Check plate_types array
        if 'plate_types' not in state_data:
            issues['critical'].append("Missing 'plate_types' array")
            return dict(issues)
        
        # Validate each plate type
        for idx, plate in enumerate(state_data['plate_types']):
            plate_prefix = f"Plate[{idx}] '{plate.get('type_name', 'unknown')}'"
            
            # Check plate type level fields
            plate_fields = set(plate.keys())
            missing_plate = self.plate_type_fields - plate_fields
            extra_plate = plate_fields - self.plate_type_fields
            
            if missing_plate:
                issues['missing_plate_fields'].append(
                    f"{plate_prefix}: {', '.join(sorted(missing_plate))}"
                )
            if extra_plate:
                issues['unexpected_plate_fields'].append(
                    f"{plate_prefix}: {', '.join(sorted(extra_plate))}"
                )
            
            # Check plate_characteristics
            if 'plate_characteristics' not in plate:
                issues['missing_plate_characteristics'].append(plate_prefix)
                continue
            
            plate_chars = plate['plate_characteristics']
            chars_fields = set(plate_chars.keys())
            missing_chars = self.plate_characteristics_fields - chars_fields
            extra_chars = chars_fields - self.plate_characteristics_fields
            
            if missing_chars:
                issues['missing_plate_characteristics_fields'].append(
                    f"{plate_prefix}: {', '.join(sorted(missing_chars))}"
                )
            if extra_chars:
                issues['unexpected_plate_characteristics_fields'].append(
                    f"{plate_prefix}: {', '.join(sorted(extra_chars))}"
                )
            
            # Check character_formatting
            if 'character_formatting' in plate_chars:
                char_fmt = plate_chars['character_formatting']
                if isinstance(char_fmt, dict):
                    fmt_fields = set(char_fmt.keys())
                    missing_fmt = self.character_formatting_fields - fmt_fields
                    extra_fmt = fmt_fields - self.character_formatting_fields
                    
                    if missing_fmt:
                        issues['missing_character_formatting_fields'].append(
                            f"{plate_prefix}: {', '.join(sorted(missing_fmt))}"
                        )
                    if extra_fmt:
                        issues['unexpected_character_formatting_fields'].append(
                            f"{plate_prefix}: {', '.join(sorted(extra_fmt))}"
                        )
            
            # Check processing_metadata
            if 'processing_metadata' in plate:
                proc_meta = plate['processing_metadata']
                if isinstance(proc_meta, dict):
                    meta_fields = set(proc_meta.keys())
                    missing_meta = self.processing_metadata_fields - meta_fields
                    extra_meta = meta_fields - self.processing_metadata_fields
                    
                    if missing_meta:
                        issues['missing_processing_metadata_fields'].append(
                            f"{plate_prefix}: {', '.join(sorted(missing_meta))}"
                        )
                    if extra_meta:
                        issues['unexpected_processing_metadata_fields'].append(
                            f"{plate_prefix}: {', '.join(sorted(extra_meta))}"
                        )
            
            # Check images
            if 'images' in plate:
                images = plate['images']
                if isinstance(images, dict):
                    img_fields = set(images.keys())
                    missing_img = self.images_fields - img_fields
                    extra_img = img_fields - self.images_fields
                    
                    if missing_img:
                        issues['missing_images_fields'].append(
                            f"{plate_prefix}: {', '.join(sorted(missing_img))}"
                        )
                    if extra_img:
                        issues['unexpected_images_fields'].append(
                            f"{plate_prefix}: {', '.join(sorted(extra_img))}"
                        )
        
        return dict(issues)
    
    def validate_all_states(self, states_dir: str = "data/states") -> Dict[str, Dict]:
        """Validate all state files"""
        states_path = Path(states_dir)
        state_files = sorted(states_path.glob("*.json"))
        
        all_issues = {}
        
        for state_file in state_files:
            state_name = state_file.stem
            issues = self.validate_state(state_file)
            
            if issues:
                all_issues[state_name] = issues
        
        return all_issues


def print_validation_report(validator: TemplateValidator, all_issues: Dict):
    """Print a comprehensive validation report"""
    
    print("=" * 80)
    print("STATE JSON VALIDATION REPORT")
    print("=" * 80)
    
    states_with_issues = len(all_issues)
    total_states = len(list(Path("data/states").glob("*.json")))
    states_ok = total_states - states_with_issues
    
    print(f"\nTotal States: {total_states}")
    print(f"✅ States OK: {states_ok}")
    print(f"❌ States with Issues: {states_with_issues}")
    
    if not all_issues:
        print("\n" + "=" * 80)
        print("🎉 ALL STATES CONFORM TO TEMPLATE!")
        print("=" * 80)
        return
    
    # Categorize issues
    issue_categories = defaultdict(list)
    for state_name, issues in all_issues.items():
        for issue_type, issue_list in issues.items():
            issue_categories[issue_type].append((state_name, issue_list))
    
    # Print by category
    print("\n" + "=" * 80)
    print("ISSUES BY CATEGORY")
    print("=" * 80)
    
    category_order = [
        'critical',
        'missing_root_fields',
        'unexpected_root_fields',
        'missing_plate_fields',
        'unexpected_plate_fields',
        'missing_plate_characteristics',
        'missing_plate_characteristics_fields',
        'unexpected_plate_characteristics_fields',
        'missing_character_formatting_fields',
        'unexpected_character_formatting_fields',
        'missing_processing_metadata_fields',
        'unexpected_processing_metadata_fields',
        'missing_images_fields',
        'unexpected_images_fields'
    ]
    
    for category in category_order:
        if category not in issue_categories:
            continue
        
        states = issue_categories[category]
        print(f"\n{'=' * 80}")
        print(f"⚠️  {category.replace('_', ' ').upper()} ({len(states)} states)")
        print(f"{'=' * 80}")
        
        for state_name, issue_list in sorted(states):
            print(f"\n{state_name.upper()}:")
            if isinstance(issue_list, list):
                for issue in issue_list:
                    print(f"  • {issue}")
    
    # Print summary by state
    print("\n" + "=" * 80)
    print("ISSUES BY STATE")
    print("=" * 80)
    
    for state_name in sorted(all_issues.keys()):
        issues = all_issues[state_name]
        total_issue_types = len(issues)
        total_issues = sum(len(v) if isinstance(v, list) else 1 for v in issues.values())
        
        print(f"\n❌ {state_name.upper()}: {total_issues} issue(s) in {total_issue_types} category(ies)")
        for issue_type, issue_list in sorted(issues.items()):
            count = len(issue_list) if isinstance(issue_list, list) else 1
            print(f"   - {issue_type}: {count}")
    
    print("\n" + "=" * 80)


def main():
    """Main validation function"""
    print("Initializing validator with template...")
    validator = TemplateValidator()
    
    print("Scanning all state files...")
    all_issues = validator.validate_all_states()
    
    print_validation_report(validator, all_issues)
    
    # Exit code based on results
    if all_issues:
        print("\n⚠️  VALIDATION FAILED: Issues found in state files")
        return 1
    else:
        print("\n✅ VALIDATION PASSED: All state files conform to template")
        return 0


if __name__ == "__main__":
    exit(main())
