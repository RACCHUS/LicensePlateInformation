"""Quick check of updated JSON files."""
import json
from pathlib import Path

states_dir = Path("data/states")

# Check Alabama
with open(states_dir / "alabama.json", encoding='utf-8') as f:
    alabama = json.load(f)

plates_with_images = [p for p in alabama['plate_types'] if p.get('images', {}).get('plate_sample')]

print(f"Alabama: {len(plates_with_images)} plate types now have images\n")
print("Sample plate types with images:")
for i, plate in enumerate(plates_with_images[:5], 1):
    name = plate.get('type_name') or plate.get('name', 'Unknown')
    print(f"  {i}. {name}")
    print(f"     Image: {plate['images']['plate_sample']}")
    if plate['images'].get('variations'):
        print(f"     Variations: {len(plate['images']['variations'])} images")

# Overall stats
total_plates_with_images = 0
total_states_updated = 0

for json_file in states_dir.glob("*.json"):
    with open(json_file, encoding='utf-8') as f:
        data = json.load(f)
    
    count = len([p for p in data['plate_types'] if p.get('images', {}).get('plate_sample')])
    if count > 0:
        total_plates_with_images += count
        total_states_updated += 1

print(f"\n{'='*60}")
print(f"OVERALL STATISTICS")
print(f"{'='*60}")
print(f"States with updated images: {total_states_updated}")
print(f"Total plate types with images: {total_plates_with_images}")
print(f"Average images per state: {total_plates_with_images / max(total_states_updated, 1):.1f}")
