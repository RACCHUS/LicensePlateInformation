"""Verify Alabama images are accessible."""
import json
from pathlib import Path

al = json.load(open('data/states/alabama.json', encoding='utf-8'))
sample = [p for p in al['plate_types'] if p.get('images', {}).get('plate_sample')][:5]

print('\nVerifying Alabama image paths:\n')
for p in sample:
    path = Path(p['images']['plate_sample'])
    exists = '✅' if path.exists() else '❌'
    print(f'{exists} {p["type_name"]}: {path}')

total_with_images = len([p for p in al['plate_types'] if p.get('images', {}).get('plate_sample')])
print(f'\n✅ Alabama: {total_with_images}/78 plate types have images')
