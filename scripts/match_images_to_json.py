"""
Smart Image Matcher - Link imported images to JSON plate types.

This script uses fuzzy matching and intelligent heuristics to:
1. Match Kaggle image titles to JSON plate type names
2. Update the 'images' section in each plate type
3. Categorize images as plate_sample, blank_template, or variations
"""

import json
import csv
from pathlib import Path
from difflib import SequenceMatcher
from collections import defaultdict
import re

class SmartImageMatcher:
    def __init__(self, dry_run=True):
        self.project_root = Path(__file__).parent.parent
        self.states_dir = self.project_root / "data" / "states"
        self.images_dir = self.project_root / "data" / "images"
        self.dataset_root = Path.home() / ".cache" / "kagglehub" / "datasets" / "mexwell" / "us-license-plates"
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
    
    def normalize_text(self, text):
        """Normalize text for comparison."""
        if not text:
            return ""
        # Remove punctuation, lowercase, remove extra spaces
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def similarity_score(self, str1, str2):
        """Calculate similarity between two strings (0-1)."""
        return SequenceMatcher(None, 
                             self.normalize_text(str1), 
                             self.normalize_text(str2)).ratio()
    
    def find_best_match(self, image_title, plate_types):
        """Find best matching plate type for an image title."""
        best_score = 0
        best_match = None
        
        for plate_type in plate_types:
            name = plate_type.get('name', '')
            subtype = plate_type.get('subtype', '')
            category = plate_type.get('category', '')
            
            # Try matching against various fields
            scores = [
                self.similarity_score(image_title, name),
                self.similarity_score(image_title, subtype),
                self.similarity_score(image_title, f"{category} {subtype}"),
                self.similarity_score(image_title, f"{name} {subtype}")
            ]
            
            # Check if key words match
            title_words = set(self.normalize_text(image_title).split())
            name_words = set(self.normalize_text(name).split())
            subtype_words = set(self.normalize_text(subtype).split())
            
            word_overlap = len(title_words & (name_words | subtype_words)) / max(len(title_words), 1)
            scores.append(word_overlap * 0.8)  # Weight word overlap
            
            max_score = max(scores)
            
            if max_score > best_score:
                best_score = max_score
                best_match = plate_type
        
        # Only return if confidence is reasonable
        if best_score >= 0.4:  # Threshold
            return best_match, best_score
        
        return None, 0
    
    def categorize_image(self, image_name):
        """Determine if image is sample, blank, or variation."""
        image_lower = image_name.lower()
        
        if 'blank' in image_lower or 'template' in image_lower:
            return 'blank_template'
        elif 'sample' in image_lower:
            return 'plate_sample'
        else:
            # Default to sample if actual plate image
            return 'plate_sample'
    
    def load_csv_metadata(self):
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
    
    def process_state(self, state_code):
        """Process one state's images and JSON."""
        if state_code not in self.state_codes:
            return None
        
        state_name = self.state_codes[state_code]
        json_path = self.states_dir / f"{state_name}.json"
        
        if not json_path.exists():
            return None
        
        # Load state JSON
        with open(json_path, 'r', encoding='utf-8') as f:
            state_data = json.load(f)
        
        plate_types = state_data.get('plate_types', [])
        
        # Load CSV metadata
        csv_data = self.load_csv_metadata()
        plates_metadata = csv_data.get(state_code, [])
        
        # Match images
        matches = []
        unmatched = []
        updates_made = 0
        
        for plate_meta in plates_metadata:
            image_name = plate_meta['image']
            image_title = plate_meta['title']
            
            # Check if image exists
            image_path = self.images_dir / state_code / image_name
            if not image_path.exists():
                continue
            
            # Find best matching plate type
            best_match, score = self.find_best_match(image_title, plate_types)
            
            if best_match:
                # Determine image category
                category = self.categorize_image(image_name)
                
                matches.append({
                    'image': image_name,
                    'title': image_title,
                    'matched_plate': best_match.get('name'),
                    'confidence': score,
                    'category': category
                })
                
                # Update JSON (if not dry run)
                if not self.dry_run:
                    images_section = best_match.get('images', {})
                    
                    # Add to appropriate category
                    if category == 'plate_sample':
                        if 'plate_sample' not in images_section or not images_section['plate_sample']:
                            images_section['plate_sample'] = f"data/images/{state_code}/{image_name}"
                            updates_made += 1
                    elif category == 'blank_template':
                        if 'blank_template' not in images_section or not images_section['blank_template']:
                            images_section['blank_template'] = f"data/images/{state_code}/{image_name}"
                            updates_made += 1
                    
                    # Update variations array
                    if 'variations' not in images_section:
                        images_section['variations'] = []
                    
                    variation_path = f"data/images/{state_code}/{image_name}"
                    if variation_path not in images_section['variations']:
                        images_section['variations'].append(variation_path)
                        updates_made += 1
                    
                    best_match['images'] = images_section
            else:
                unmatched.append({
                    'image': image_name,
                    'title': image_title
                })
        
        # Save updated JSON
        if not self.dry_run and updates_made > 0:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(state_data, f, indent=2, ensure_ascii=False)
        
        return {
            'state': state_code,
            'state_name': state_name,
            'total_images': len(plates_metadata),
            'matched': len(matches),
            'unmatched': len(unmatched),
            'updates_made': updates_made,
            'matches': matches[:5],  # Sample
            'unmatched_sample': unmatched[:5]
        }
    
    def run_all_states(self):
        """Process all states."""
        print("=" * 80)
        mode = "DRY RUN" if self.dry_run else "LIVE UPDATE"
        print(f"IMAGE MATCHER - {mode}")
        print("=" * 80)
        
        total_matched = 0
        total_unmatched = 0
        total_updates = 0
        
        results = []
        
        for state_code in sorted(self.state_codes.keys()):
            result = self.process_state(state_code)
            if result:
                results.append(result)
                
                status = "✅" if result['matched'] > 0 else "⚠️"
                print(f"{status} {state_code}: {result['matched']}/{result['total_images']} matched, "
                      f"{result['updates_made']} updates")
                
                total_matched += result['matched']
                total_unmatched += result['unmatched']
                total_updates += result['updates_made']
        
        # Summary
        print("\n" + "=" * 80)
        print("MATCHING COMPLETE")
        print("=" * 80)
        print(f"\nTotal images: {total_matched + total_unmatched}")
        print(f"Successfully matched: {total_matched}")
        print(f"Unmatched: {total_unmatched}")
        print(f"JSON updates made: {total_updates}")
        
        if self.dry_run:
            print("\n⚠️  DRY RUN MODE - No files were modified")
            print("Run with --live to actually update JSON files")
        else:
            print(f"\n✅ Updated {len([r for r in results if r['updates_made'] > 0])} state JSON files")
        
        # Show sample matches
        print("\n📊 Sample Matches (High Confidence):")
        high_confidence = []
        for result in results:
            for match in result.get('matches', []):
                if match['confidence'] > 0.7:
                    high_confidence.append((result['state'], match))
        
        for state, match in high_confidence[:10]:
            print(f"   {state}: '{match['title']}' → '{match['matched_plate']}' "
                  f"(confidence: {match['confidence']:.2f})")
        
        return results

def main():
    import sys
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                     SMART IMAGE MATCHER                                      ║
║                                                                              ║
║  This will match imported images to JSON plate types using fuzzy matching   ║
║  and update the 'images' section in each plate type automatically.          ║
║                                                                              ║
║  Options:                                                                    ║
║    --preview : Preview matches without modifying files (default)             ║
║    --live    : Actually update JSON files                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")
    
    dry_run = True
    if '--live' in sys.argv:
        dry_run = False
        confirm = input("\n⚠️  LIVE MODE: This will modify JSON files. Continue? (yes/no): ")
        if confirm.lower() != 'yes':
            print("Cancelled.")
            return
    
    print(f"\n🚀 Starting image matcher ({'DRY RUN' if dry_run else 'LIVE MODE'})...\n")
    
    matcher = SmartImageMatcher(dry_run=dry_run)
    results = matcher.run_all_states()
    
    if dry_run:
        print("\n💡 To actually update files, run: python scripts\\match_images_to_json.py --live")

if __name__ == "__main__":
    main()
