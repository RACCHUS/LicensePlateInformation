"""
Bulk Image Importer - Import ALL Kaggle images for ALL states at once.
"""

import json
import csv
import shutil
from pathlib import Path
from collections import defaultdict

class BulkImageImporter:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.dataset_root = Path.home() / ".cache" / "kagglehub" / "datasets" / "mexwell" / "us-license-plates"
        self.images_dir = self.project_root / "data" / "images"
        
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
    
    def find_dataset_image(self, state_code, image_name):
        """Find the actual image file in the dataset."""
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
    
    def bulk_import_all(self):
        """Import images for ALL states."""
        print("=" * 80)
        print("BULK IMAGE IMPORT - ALL STATES")
        print("=" * 80)
        
        # Load CSV
        csv_file = list(self.dataset_root.rglob("*.csv"))[0]
        
        csv_data = defaultdict(list)
        with open(csv_file, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f)
            for row in reader:
                csv_data[row['state']].append({
                    'title': row['plate_title'],
                    'image': row['plate_img']
                })
        
        total_states = 0
        total_imported = 0
        total_skipped = 0
        total_already_exist = 0
        
        state_summary = []
        
        # Process each state
        for state_code in sorted(csv_data.keys()):
            if state_code not in self.state_codes:
                continue
            
            # Create state directory
            state_dir = self.images_dir / state_code
            state_dir.mkdir(parents=True, exist_ok=True)
            
            plates = csv_data[state_code]
            imported = 0
            skipped = 0
            already_exist = 0
            
            for plate in plates:
                target_path = state_dir / plate['image']
                
                # Skip if already exists
                if target_path.exists():
                    already_exist += 1
                    continue
                
                # Find source image
                source_image = self.find_dataset_image(state_code, plate['image'])
                
                if source_image:
                    try:
                        shutil.copy2(source_image, target_path)
                        imported += 1
                    except Exception as e:
                        print(f"   ⚠️  Error copying {plate['image']}: {e}")
                        skipped += 1
                else:
                    skipped += 1
            
            # Print state summary
            status = "✅" if imported > 0 or already_exist == len(plates) else "⚠️"
            print(f"{status} {state_code}: {imported} imported, {already_exist} already exist, {skipped} missing ({len(plates)} total)")
            
            state_summary.append({
                'state': state_code,
                'imported': imported,
                'already_exist': already_exist,
                'skipped': skipped,
                'total': len(plates)
            })
            
            total_states += 1
            total_imported += imported
            total_skipped += skipped
            total_already_exist += already_exist
        
        # Final summary
        print("\n" + "=" * 80)
        print("IMPORT COMPLETE")
        print("=" * 80)
        print(f"\nStates processed: {total_states}")
        print(f"Images imported: {total_imported}")
        print(f"Already existed: {total_already_exist}")
        print(f"Not found/skipped: {total_skipped}")
        print(f"Total images in dataset: {total_imported + total_already_exist + total_skipped}")
        
        # Top states by import count
        print("\n📊 Top 10 States by New Images Imported:")
        sorted_states = sorted(state_summary, key=lambda x: x['imported'], reverse=True)
        for i, state in enumerate(sorted_states[:10], 1):
            print(f"   {i}. {state['state']}: {state['imported']} new images")
        
        return {
            'total_states': total_states,
            'total_imported': total_imported,
            'total_already_exist': total_already_exist,
            'total_skipped': total_skipped
        }

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                     BULK IMAGE IMPORTER                                      ║
║                                                                              ║
║  This will import ALL license plate images from the Kaggle dataset          ║
║  into your project structure at data/images/STATE/                          ║
║                                                                              ║
║  Estimated time: 2-5 minutes                                                ║
║  Estimated images: ~6,500                                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")
    
    confirm = input("Proceed with bulk import? (yes/no): ").strip().lower()
    
    if confirm == 'yes':
        print("\n🚀 Starting bulk import...\n")
        
        importer = BulkImageImporter()
        results = importer.bulk_import_all()
        
        print("\n✅ Bulk import complete!")
        print(f"\n📁 Images are now in: data/images/STATE/")
        print(f"\n💡 Next step: Run the image matcher to link images to JSON files")
    else:
        print("Import cancelled.")
