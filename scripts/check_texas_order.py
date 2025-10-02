"""
Script to check Texas image ordering
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.gui.components.image_display.image_viewer import PlateImageViewer

# Create a dummy viewer to access the methods
class DummyViewer:
    def __init__(self):
        self.TYPE_PRIORITY = PlateImageViewer.TYPE_PRIORITY
        self.IMAGE_TYPE_PRIORITY = PlateImageViewer.IMAGE_TYPE_PRIORITY
    
    def _parse_image_filename(self, filename, state_code):
        """Copy of the parsing method"""
        name_without_ext = os.path.splitext(filename)[0]
        name_lower = name_without_ext.lower()
        
        # Determine image type
        image_type = 'sample'
        if 'blank' in name_lower or 'template' in name_lower:
            image_type = 'blank'
        elif 'font' in name_lower:
            image_type = 'font'
        elif 'variation' in name_lower or 'variant' in name_lower:
            image_type = 'variation'
        
        # Determine plate type category
        plate_type_category = None
        
        # Check for specific types first
        if 'semi-trailer' in name_lower or 'semitrailer' in name_lower:
            plate_type_category = 'semi-trailer'
        elif 'semi' in name_lower:
            plate_type_category = 'semi'
        elif 'trailer' in name_lower:
            plate_type_category = 'trailer'
        elif 'truck' in name_lower:
            plate_type_category = 'truck'
        elif 'commercial' in name_lower:
            plate_type_category = 'commercial'
        elif 'passenger' in name_lower or 'standard' in name_lower:
            plate_type_category = 'passenger'
        elif 'motorcycle' in name_lower or 'mc' in name_lower:
            plate_type_category = 'motorcycle'
        elif 'specialty' in name_lower or 'special' in name_lower:
            plate_type_category = 'specialty'
        elif 'vanity' in name_lower or 'personalized' in name_lower:
            plate_type_category = 'vanity'
        elif 'government' in name_lower or 'govt' in name_lower:
            plate_type_category = 'government'
        elif 'dealer' in name_lower:
            plate_type_category = 'dealer'
        elif 'apportioned' in name_lower:
            plate_type_category = 'apportioned'
        
        # If no specific type found and it's a generic "plate" file, mark as generic
        if plate_type_category is None:
            if 'plate' in name_lower and ('sample' in name_lower or 'blank' in name_lower or 'template' in name_lower):
                plate_type_category = 'generic'
            else:
                plate_type_category = 'passenger'  # default fallback
        
        display_name = name_without_ext.replace('_', ' ').title()
        
        return {
            'filename': filename,
            'display_name': display_name,
            'image_type': image_type,
            'plate_type_category': plate_type_category,
            'state_code': state_code
        }

# Test Texas images
viewer = DummyViewer()
texas_files = [
    'plate_sample.jpg',
    'sample_passenger.png',
    'truck_sample.jpg',
    'blank_template.png',
    'trailer_sample.jpg',
    'semi_trailer_sample.png',
    'passenger_plate.jpg'
]

print("=" * 80)
print("TEXAS IMAGE ORDERING TEST")
print("=" * 80)

images = []
for filename in texas_files:
    info = viewer._parse_image_filename(filename, 'TX')
    images.append(info)
    
    print(f"\nFile: {filename}")
    print(f"  Display Name: {info['display_name']}")
    print(f"  Image Type: {info['image_type']}")
    print(f"  Plate Type: {info['plate_type_category']}")
    print(f"  Type Priority: {viewer.TYPE_PRIORITY.get(info['plate_type_category'], 99)}")
    print(f"  Image Priority: {viewer.IMAGE_TYPE_PRIORITY.get(info['image_type'], 99)}")

# Sort by priority
images.sort(key=lambda x: (
    viewer.TYPE_PRIORITY.get(x['plate_type_category'], 99),
    viewer.IMAGE_TYPE_PRIORITY.get(x['image_type'], 99),
    x['display_name']
))

print("\n" + "=" * 80)
print("SORTED ORDER:")
print("=" * 80)
for i, img in enumerate(images, 1):
    print(f"{i}. {img['filename']}")
    print(f"   → {img['display_name']} ({img['plate_type_category']}, {img['image_type']})")
    print(f"   → Priority: ({viewer.TYPE_PRIORITY.get(img['plate_type_category'], 99)}, "
          f"{viewer.IMAGE_TYPE_PRIORITY.get(img['image_type'], 99)})")
    print()
