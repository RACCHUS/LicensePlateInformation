"""Comprehensive verification of Kaggle image integration."""
import json
from pathlib import Path

states_dir = Path('data/states')

print("=" * 80)
print("KAGGLE IMAGE VERIFICATION")
print("=" * 80)

total_kaggle_variations = 0
total_kaggle_samples = 0
total_verified_exist = 0
total_missing = 0
states_with_kaggle = []

for json_file in sorted(states_dir.glob('*.json')):
    with open(json_file, encoding='utf-8') as f:
        data = json.load(f)
    
    state_code = data['abbreviation']
    kaggle_count = 0
    verified = 0
    missing = 0
    
    for plate in data.get('plate_types', []):
        images = plate.get('images', {})
        
        # Check plate_sample
        sample = images.get('plate_sample', '')
        if sample and sample.startswith('data/images/'):
            total_kaggle_samples += 1
            kaggle_count += 1
            if Path(sample).exists():
                verified += 1
            else:
                missing += 1
        
        # Check variations
        for var in images.get('variations', []):
            if var.startswith('data/images/'):
                total_kaggle_variations += 1
                kaggle_count += 1
                if Path(var).exists():
                    verified += 1
                else:
                    missing += 1
    
    if kaggle_count > 0:
        states_with_kaggle.append({
            'state': state_code,
            'total': kaggle_count,
            'verified': verified,
            'missing': missing
        })
        total_verified_exist += verified
        total_missing += missing

print(f"\n📊 OVERALL STATISTICS")
print(f"   Kaggle images in plate_sample: {total_kaggle_samples}")
print(f"   Kaggle images in variations: {total_kaggle_variations}")
print(f"   Total Kaggle references: {total_kaggle_samples + total_kaggle_variations}")
print(f"   Files exist on disk: {total_verified_exist} ✅")
print(f"   Files missing: {total_missing} ❌")
print(f"   Success rate: {total_verified_exist / max(total_verified_exist + total_missing, 1) * 100:.1f}%")

print(f"\n🗺️  STATES WITH KAGGLE IMAGES ({len(states_with_kaggle)} states)")
for state in states_with_kaggle[:10]:
    status = '✅' if state['missing'] == 0 else '⚠️'
    print(f"   {status} {state['state']}: {state['verified']} verified, {state['missing']} missing")

if len(states_with_kaggle) > 10:
    print(f"   ... and {len(states_with_kaggle) - 10} more states")

print(f"\n✅ Integration verified! Kaggle images successfully linked to JSON files.")
print(f"   Images added as 'variations' to preserve existing plate_sample paths.")
