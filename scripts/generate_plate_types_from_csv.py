"""
Plate Type Generator - Automatically create new plate types from Kaggle CSV data.

This script analyzes unmatched images and generates proper plate type entries
that can be added to state JSON files, dramatically improving match rates.
"""

import json
import csv
from pathlib import Path
from collections import defaultdict
from difflib import SequenceMatcher
import re

class PlateTypeGenerator:
    def __init__(self, dry_run=True):
        self.project_root = Path(__file__).parent.parent
        self.states_dir = self.project_root / "data" / "states"
        self.dataset_root = Path.home() / ".cache" / "kagglehub" / "datasets" / "mexwell" / "us-license-plates"
        self.template_path = self.project_root / "data" / "templates" / "state_template.json"
        self.dry_run = dry_run
        
        # State code mapping
        self.state_codes = {
            'AL': 'alabama', 'AK': 'alaska', 'AZ': 'arizona', 'AR': 'arkansas',
            'CA': 'california', 'CO': 'colorado', 'CT': 'connecticut', 'DE': 'delaware',
            'FL': 'florida', 'GA': 'georgia', 'HI': 'hawaii', 'ID': 'idaho',
            'IL': 'illinois', 'IN': 'indiana', 'IA': 'iowa', 'KS': 'kansas',
            'KY': 'kentucky', 'LA': 'louisiana', 'ME': 'maine', 'MD': 'maryland',
            'MA': 'massachusetts', 'MI': 'michigan', 'MN': 'minnesota', 'MS': 'mississippi',
            'MO': 'missouri', 'MT': 'montana', 'NE': 'nebraska', 'NV': 'nevada',
            'NH': 'new_hampshire', 'NJ': 'new_jersey', 'NM': 'new_mexico', 'NY': 'new_york',
            'NC': 'north_carolina', 'ND': 'north_dakota', 'OH': 'ohio', 'OK': 'oklahoma',
            'OR': 'oregon', 'PA': 'pennsylvania', 'RI': 'rhode_island', 'SC': 'south_carolina',
            'SD': 'south_dakota', 'TN': 'tennessee', 'TX': 'texas', 'UT': 'utah',
            'VT': 'vermont', 'VA': 'virginia', 'WA': 'washington', 'DC': 'washington_dc',
            'WV': 'west_virginia', 'WI': 'wisconsin', 'WY': 'wyoming'
        }
        
        # Category mapping based on keywords
        self.category_keywords = {
            'passenger': ['passenger', 'standard', 'regular', 'personal'],
            'commercial': ['commercial', 'truck', 'trailer', 'dealer', 'transporter'],
            'government': ['government', 'official', 'municipal', 'state', 'federal', 'police', 'fire'],
            'military': ['veteran', 'military', 'armed forces', 'army', 'navy', 'marine', 'air force', 'coast guard', 'national guard'],
            'specialty': ['collegiate', 'university', 'college', 'organization', 'wildlife', 'conservation', 'charity', 'special'],
            'antique': ['antique', 'classic', 'vintage', 'historic', 'restored'],
            'motorcycle': ['motorcycle', 'moped', 'scooter'],
            'recreational': ['rv', 'recreational', 'camper', 'boat', 'trailer'],
            'disabled': ['disabled', 'handicapped', 'wheelchair', 'mobility'],
            'temporary': ['temporary', 'temp', 'transit', 'in-transit']
        }
    
    def normalize_text(self, text):
        """Normalize text for comparison."""
        if not text:
            return ""
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def categorize_plate_title(self, title):
        """Determine category and subtype from plate title."""
        title_lower = self.normalize_text(title)
        
        for category, keywords in self.category_keywords.items():
            for keyword in keywords:
                if keyword in title_lower:
                    return category, title
        
        return 'specialty', title
    
    def similarity_score(self, str1, str2):
        """Calculate similarity between two strings (0-1)."""
        return SequenceMatcher(None, 
                             self.normalize_text(str1), 
                             self.normalize_text(str2)).ratio()
    
    def check_existing_match(self, title, existing_plates, threshold=0.6):
        """Check if this title already matches an existing plate type."""
        for plate in existing_plates:
            type_name = plate.get('type_name', '')
            subtype = plate.get('subtype', '')
            category = plate.get('category', '')
            
            # Check various combinations
            scores = [
                self.similarity_score(title, type_name),
                self.similarity_score(title, subtype),
                self.similarity_score(title, f"{category} {subtype}"),
            ]
            
            if max(scores) >= threshold:
                return True, plate
        
        return False, None
    
    def load_csv_data(self):
        """Load CSV metadata from Kaggle dataset."""
        csv_file = list(self.dataset_root.rglob("*.csv"))[0]
        
        csv_data = defaultdict(list)
        with open(csv_file, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f)
            for row in reader:
                csv_data[row['state']].append({
                    'title': row['plate_title'],
                    'image': row['plate_img'],
                    'source': row.get('source', '')
                })
        
        return csv_data
    
    def create_plate_type_template(self, title, category, state_code):
        """Create a new plate type entry based on template."""
        # Generate clean type name
        type_name = title.strip()
        
        # Basic plate type structure
        new_plate = {
            "type_name": type_name,
            "pattern": "ABC123",  # Default pattern
            "character_count": 6,  # Default
            "description": f"{state_code} {type_name} plate",
            "background_color": "#FFFFFF",
            "text_color": "#000000",
            "has_stickers": True,
            "sticker_description": "Standard validation stickers",
            "category": category,
            "subtype": type_name.lower().replace(' ', '_'),
            "code_number": "0",  # Default
            "processing_type": "standard",
            "plate_characteristics": {
                "font": None,
                "logo": None,
                "plate_text": None,
                "character_formatting": {
                    "stacked_characters": None,
                    "slanted_characters": None,
                    "slant_direction": None,
                    "stack_position": None
                },
                "sticker_override": None,
                "design_variants": []
            },
            "processing_metadata": {
                "currently_processed": True,
                "requires_prefix": False,
                "requires_suffix": False,
                "allows_custom_text": False,
                "special_validation": None,
                "notes": f"Generated from Kaggle dataset for {type_name}"
            },
            "date_ranges": {
                "period_1": None,
                "period_2": None
            },
            "images": {
                "plate_sample": None,
                "character_font_sample": None,
                "blank_template": None,
                "variations": []
            },
            "visual_identifier": "N",
            "processing_rules": "N",
            "requires_prefix": False
        }
        
        return new_plate
    
    def analyze_state(self, state_code):
        """Analyze one state and generate new plate types."""
        if state_code not in self.state_codes:
            return None
        
        state_name = self.state_codes[state_code]
        json_path = self.states_dir / f"{state_name}.json"
        
        if not json_path.exists():
            return None
        
        # Load state JSON
        with open(json_path, 'r', encoding='utf-8') as f:
            state_data = json.load(f)
        
        existing_plates = state_data.get('plate_types', [])
        
        # Load CSV data
        csv_data = self.load_csv_data()
        plates_metadata = csv_data.get(state_code, [])
        
        # Analyze unmatched plates
        new_plates = []
        duplicates = []
        
        # Group by title to avoid duplicates
        unique_titles = {}
        for plate_meta in plates_metadata:
            title = plate_meta['title']
            if title not in unique_titles:
                unique_titles[title] = []
            unique_titles[title].append(plate_meta)
        
        for title, images in unique_titles.items():
            # Check if already exists
            exists, matched_plate = self.check_existing_match(title, existing_plates)
            
            if exists:
                duplicates.append({
                    'title': title,
                    'matched_to': matched_plate.get('type_name') if matched_plate else 'Unknown',
                    'image_count': len(images)
                })
            else:
                # Create new plate type
                category, subtype = self.categorize_plate_title(title)
                new_plate = self.create_plate_type_template(title, category, state_code)
                
                # Add image references
                for img in images:
                    img_path = f"data/images/{state_code}/{img['image']}"
                    if Path(img_path).exists():
                        new_plate['images']['variations'].append(img_path)
                
                # Set first image as sample if available
                if new_plate['images']['variations']:
                    new_plate['images']['plate_sample'] = new_plate['images']['variations'][0]
                
                new_plates.append(new_plate)
        
        return {
            'state': state_code,
            'state_name': state_name,
            'existing_count': len(existing_plates),
            'new_count': len(new_plates),
            'duplicate_count': len(duplicates),
            'total_images': len(plates_metadata),
            'new_plates': new_plates,
            'duplicates_sample': duplicates[:5]
        }
    
    def generate_all_states(self):
        """Generate new plate types for all states."""
        print("=" * 80)
        mode = "DRY RUN" if self.dry_run else "LIVE UPDATE"
        print(f"PLATE TYPE GENERATOR - {mode}")
        print("=" * 80)
        
        total_existing = 0
        total_new = 0
        total_duplicates = 0
        
        results = []
        
        for state_code in sorted(self.state_codes.keys()):
            result = self.analyze_state(state_code)
            if result:
                results.append(result)
                
                status = "📋" if result['new_count'] > 0 else "✅"
                print(f"{status} {state_code}: {result['existing_count']} existing, "
                      f"{result['new_count']} new, {result['duplicate_count']} duplicates")
                
                total_existing += result['existing_count']
                total_new += result['new_count']
                total_duplicates += result['duplicate_count']
        
        # Summary
        print("\n" + "=" * 80)
        print("GENERATION COMPLETE")
        print("=" * 80)
        print(f"\nExisting plate types: {total_existing}")
        print(f"New plate types generated: {total_new}")
        print(f"Duplicates identified: {total_duplicates}")
        print(f"Total after adding: {total_existing + total_new}")
        print(f"Coverage increase: {total_new / max(total_existing, 1) * 100:.1f}%")
        
        if self.dry_run:
            print("\n⚠️  DRY RUN MODE - No files were modified")
            print("Review the output, then run with --add to actually add plate types")
            print("Or use --export to save to separate files for review")
        
        # Show sample new plate types
        print("\n📋 SAMPLE NEW PLATE TYPES:")
        for result in results[:5]:
            if result['new_plates']:
                plate = result['new_plates'][0]
                print(f"\n   {result['state']}: {plate['type_name']}")
                print(f"      Category: {plate['category']}")
                print(f"      Images: {len(plate['images']['variations'])}")
        
        # Show states with most new types
        print("\n🎯 STATES WITH MOST NEW PLATE TYPES:")
        sorted_results = sorted(results, key=lambda x: x['new_count'], reverse=True)
        for i, result in enumerate(sorted_results[:10], 1):
            if result['new_count'] > 0:
                print(f"   {i:2d}. {result['state']}: {result['new_count']} new types "
                      f"({result['existing_count']} → {result['existing_count'] + result['new_count']})")
        
        return results
    
    def add_to_json_files(self, results):
        """Actually add new plate types to JSON files."""
        print("\n" + "=" * 80)
        print("ADDING PLATE TYPES TO JSON FILES")
        print("=" * 80)
        
        for result in results:
            if result['new_count'] == 0:
                continue
            
            state_name = result['state_name']
            json_path = self.states_dir / f"{state_name}.json"
            
            # Load state JSON
            with open(json_path, 'r', encoding='utf-8') as f:
                state_data = json.load(f)
            
            # Add new plate types
            state_data['plate_types'].extend(result['new_plates'])
            
            # Save updated JSON
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(state_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ {result['state']}: Added {result['new_count']} plate types")
        
        print("\n✅ JSON files updated successfully!")
    
    def export_to_files(self, results):
        """Export new plate types to separate files for review."""
        export_dir = self.project_root / "data" / "pending" / "generated_plate_types"
        export_dir.mkdir(parents=True, exist_ok=True)
        
        print("\n" + "=" * 80)
        print("EXPORTING NEW PLATE TYPES")
        print("=" * 80)
        
        for result in results:
            if result['new_count'] == 0:
                continue
            
            export_file = export_dir / f"{result['state']}_new_plates.json"
            
            export_data = {
                'state': result['state'],
                'state_name': result['state_name'],
                'existing_count': result['existing_count'],
                'new_count': result['new_count'],
                'new_plate_types': result['new_plates']
            }
            
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            print(f"📄 {result['state']}: Exported to {export_file.name}")
        
        print(f"\n✅ Exported to {export_dir}")
        print("Review the files, then run with --add to import them")

def main():
    import sys
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                     PLATE TYPE GENERATOR                                     ║
║                                                                              ║
║  This will analyze Kaggle CSV data and generate new plate types for         ║
║  unmatched images, dramatically improving match rates.                       ║
║                                                                              ║
║  Options:                                                                    ║
║    --preview : Preview new plate types without modifying files (default)     ║
║    --export  : Export new plate types to files for manual review             ║
║    --add     : Add new plate types to JSON files                             ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")
    
    dry_run = True
    action = 'preview'
    
    if '--add' in sys.argv:
        dry_run = False
        action = 'add'
        confirm = input("\n⚠️  This will modify JSON files. Continue? (yes/no): ")
        if confirm.lower() != 'yes':
            print("Cancelled.")
            return
    elif '--export' in sys.argv:
        action = 'export'
    
    print(f"\n🚀 Starting plate type generator ({action} mode)...\n")
    
    generator = PlateTypeGenerator(dry_run=dry_run)
    results = generator.generate_all_states()
    
    if action == 'export':
        generator.export_to_files(results)
    elif action == 'add':
        generator.add_to_json_files(results)
        print("\n💡 Next step: Re-run the image matcher to link images to new plate types")
        print("   python scripts\\match_images_to_json.py --live")
    else:
        print("\n💡 Options:")
        print("   --export : Export to files for review")
        print("   --add    : Add directly to JSON files")

if __name__ == "__main__":
    main()
