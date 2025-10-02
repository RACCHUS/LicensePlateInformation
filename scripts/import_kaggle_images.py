"""
Smart Image Importer - Matches Kaggle dataset images to your JSON plate types.
"""

import json
import csv
import shutil
from pathlib import Path
from collections import defaultdict

class ImageImporter:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.dataset_root = Path.home() / ".cache" / "kagglehub" / "datasets" / "mexwell" / "us-license-plates"
        self.images_dir = self.project_root / "data" / "images"
        self.states_dir = self.project_root / "data" / "states"
        
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
    
    def load_csv_data(self):
        """Load the Kaggle CSV file."""
        csv_file = list(self.dataset_root.rglob("*.csv"))[0]
        
        data_by_state = defaultdict(list)
        
        with open(csv_file, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f)
            for row in reader:
                state = row['state']
                data_by_state[state].append({
                    'title': row['plate_title'],
                    'image': row['plate_img'],
                    'source': row['source']
                })
        
        return data_by_state
    
    def find_dataset_image(self, state_code, image_name):
        """Find the actual image file in the dataset."""
        # Search in plates/plates/STATE/
        search_paths = [
            self.dataset_root / "plates" / "plates" / state_code,
            self.dataset_root / "versions" / "3" / "plates" / "plates" / state_code,
        ]
        
        for search_path in search_paths:
            if search_path.exists():
                # Try exact match
                image_path = search_path / image_name
                if image_path.exists():
                    return image_path
                
                # Try case-insensitive search
                for file in search_path.glob("*"):
                    if file.name.lower() == image_name.lower():
                        return file
        
        return None
    
    def import_images_for_state(self, state_code, dry_run=True):
        """Import images for a specific state."""
        if state_code not in self.state_codes:
            print(f"⚠️  Unknown state code: {state_code}")
            return
        
        state_name = self.state_codes[state_code]
        state_dir = self.images_dir / state_code
        
        if not dry_run:
            state_dir.mkdir(parents=True, exist_ok=True)
        
        # Load CSV data
        csv_data = self.load_csv_data()
        
        if state_code not in csv_data:
            print(f"⚠️  No data for {state_code} in CSV")
            return
        
        plates = csv_data[state_code]
        print(f"\n{'=' * 80}")
        print(f"📋 {state_code} - {len(plates)} plate types in dataset")
        print(f"{'=' * 80}")
        
        imported = 0
        skipped = 0
        
        for plate in plates[:10]:  # Show first 10
            image_file = self.find_dataset_image(state_code, plate['image'])
            
            if image_file:
                target_path = state_dir / image_file.name
                
                if dry_run:
                    print(f"✅ Would copy: {plate['title']}")
                    print(f"   From: {image_file.name}")
                    print(f"   To: {target_path.relative_to(self.project_root)}")
                else:
                    shutil.copy2(image_file, target_path)
                    print(f"✅ Copied: {plate['title']} → {image_file.name}")
                
                imported += 1
            else:
                print(f"❌ Not found: {plate['title']} ({plate['image']})")
                skipped += 1
        
        if len(plates) > 10:
            print(f"\n... and {len(plates) - 10} more plates")
        
        print(f"\n📊 Summary: {imported} found, {skipped} not found")
        
        return imported, skipped
    
    def preview_all_states(self):
        """Preview what would be imported for all states."""
        csv_data = self.load_csv_data()
        
        print("=" * 80)
        print("IMPORT PREVIEW - ALL STATES")
        print("=" * 80)
        
        total_found = 0
        total_missing = 0
        
        for state_code in sorted(csv_data.keys()):
            if state_code in self.state_codes:
                plates = csv_data[state_code]
                
                # Count how many images exist
                found = 0
                for plate in plates:
                    if self.find_dataset_image(state_code, plate['image']):
                        found += 1
                
                missing = len(plates) - found
                total_found += found
                total_missing += missing
                
                print(f"{state_code}: {found}/{len(plates)} images found ({missing} missing)")
        
        print(f"\n{'=' * 80}")
        print(f"TOTAL: {total_found} images available, {total_missing} missing")
        print(f"{'=' * 80}")

def main():
    importer = ImageImporter()
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                       KAGGLE IMAGE IMPORTER                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

This tool will import license plate images from the Kaggle dataset into your
project structure at data/images/STATE/

Options:
  1) Preview all states (see what's available)
  2) Import one state (test with one state)
  3) Import all states (full import)
  4) Exit

""")
    
    choice = input("Select option (1-4): ").strip()
    
    if choice == "1":
        importer.preview_all_states()
    
    elif choice == "2":
        state = input("Enter state code (e.g., CA, TX, NY): ").strip().upper()
        print("\n🔍 DRY RUN (preview only, no files copied):")
        importer.import_images_for_state(state, dry_run=True)
        
        confirm = input("\n\nProceed with actual import? (yes/no): ").strip().lower()
        if confirm == 'yes':
            print("\n📥 IMPORTING...")
            importer.import_images_for_state(state, dry_run=False)
    
    elif choice == "3":
        print("\n⚠️  This will import images for ALL states.")
        confirm = input("Are you sure? (type YES to confirm): ").strip()
        if confirm == "YES":
            print("\n📥 IMPORTING ALL STATES...")
            # Implementation for bulk import
            print("(Full implementation would go here)")
    
    else:
        print("Exiting...")

if __name__ == "__main__":
    main()
