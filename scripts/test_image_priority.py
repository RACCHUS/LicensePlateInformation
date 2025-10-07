"""
Test script to verify that priority images appear first for each state.

This script checks:
1. Images are ordered correctly according to TYPE_PRIORITY and IMAGE_TYPE_PRIORITY
2. Default sample images (plate_sample, truck_sample, etc.) appear first
3. Validates the image paths exist in the filesystem
"""

import os
import json
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
PLATES_DIR = BASE_DIR / "data" / "images" / "Plates"
STATES_DIR = BASE_DIR / "data" / "states"

# Priority mappings (from image_viewer.py)
TYPE_PRIORITY = {
    'generic': 0,
    'truck': 1,
    'trailer': 1,
    'semi-trailer': 1,
    'semi': 1,
    'commercial': 1,
    'passenger': 2,
    'motorcycle': 3,
    'specialty': 4,
    'government': 5,
    'military': 5,
    'dealer': 6,
    'temporary': 7,
    'antique': 8,
    'other': 9
}

IMAGE_TYPE_PRIORITY = {
    'sample': 1,
    'blank': 2,
    'font': 3,
    'variation': 4
}

# Expected first images for each type
EXPECTED_PRIORITY_IMAGES = [
    'plate_sample.png',
    'truck_sample.png',
    'trailer_sample.png',
    'semi-trailer_sample.png',
    'fleet-trailer_sample.png',
    'rental-trailer_sample.png',
    'permanent-trailer_sample.png',
]


def parse_image_type(filename):
    """Parse image type from filename (simplified version)."""
    name_lower = filename.lower()
    
    # Check for image type keywords
    img_type = 'other'
    for keyword in IMAGE_TYPE_PRIORITY.keys():
        if keyword in name_lower:
            img_type = keyword
            break
    
    # Check for plate type keywords
    plate_type = 'other'
    if 'truck' in name_lower:
        plate_type = 'truck'
    elif 'semi' in name_lower or 'semitrailer' in name_lower:
        plate_type = 'semi-trailer'
    elif 'trailer' in name_lower:
        plate_type = 'trailer'
    elif any(word in name_lower for word in ['passenger', 'plate_sample', 'standard']):
        plate_type = 'generic'
    
    return plate_type, img_type


def get_sort_key(filename):
    """Get sort key for a filename."""
    plate_type, img_type = parse_image_type(filename)
    
    type_priority = TYPE_PRIORITY.get(plate_type, 9)
    img_priority = IMAGE_TYPE_PRIORITY.get(img_type, 4)
    
    return (type_priority, img_priority, filename.lower())


def test_state_images(state_folder_name):
    """Test image ordering for a specific state."""
    folder_path = PLATES_DIR / state_folder_name
    
    if not folder_path.exists():
        return {
            'state': state_folder_name,
            'status': 'ERROR',
            'message': 'Folder does not exist',
            'images': []
        }
    
    # Get all image files
    images = []
    for file in folder_path.iterdir():
        if file.is_file() and file.suffix.lower() in ['.png', '.jpg', '.jpeg']:
            images.append(file.name)
    
    if not images:
        return {
            'state': state_folder_name,
            'status': 'WARNING',
            'message': 'No images found',
            'images': []
        }
    
    # Sort images using the same logic as image_viewer.py
    sorted_images = sorted(images, key=get_sort_key)
    
    # Check if priority images appear first
    priority_images_found = []
    for img in sorted_images[:7]:  # Check first 7 images
        if img in EXPECTED_PRIORITY_IMAGES:
            priority_images_found.append(img)
    
    # Analyze ordering
    first_three = sorted_images[:3] if len(sorted_images) >= 3 else sorted_images
    
    result = {
        'state': state_folder_name,
        'status': 'PASS',
        'total_images': len(images),
        'first_three': first_three,
        'priority_images_found': priority_images_found,
        'all_images_ordered': sorted_images
    }
    
    # Check if plate_sample is first (most common case)
    if 'plate_sample.png' in images and sorted_images[0] != 'plate_sample.png':
        result['status'] = 'WARNING'
        result['message'] = f"plate_sample.png exists but '{sorted_images[0]}' appears first"
    
    return result


def test_all_states():
    """Test image ordering for all states."""
    print("=" * 80)
    print("Testing Image Priority Ordering for All States")
    print("=" * 80)
    print()
    
    # Get all state folders
    state_folders = [f.name for f in PLATES_DIR.iterdir() if f.is_dir()]
    state_folders.sort()
    
    results = []
    pass_count = 0
    warning_count = 0
    error_count = 0
    
    for state_folder in state_folders:
        result = test_state_images(state_folder)
        results.append(result)
        
        # Print result
        status_symbol = {
            'PASS': '✅',
            'WARNING': '⚠️',
            'ERROR': '❌'
        }.get(result['status'], '❓')
        
        print(f"{status_symbol} {result['state']:<25} ", end='')
        
        if result['status'] == 'ERROR':
            print(f"ERROR: {result['message']}")
            error_count += 1
        elif result['status'] == 'WARNING':
            print(f"WARNING: {result.get('message', 'Check ordering')}")
            print(f"   First 3: {', '.join(result['first_three'])}")
            warning_count += 1
        else:
            print(f"OK ({result['total_images']} images)")
            if result['priority_images_found']:
                print(f"   Priority images: {', '.join(result['priority_images_found'])}")
            print(f"   First 3: {', '.join(result['first_three'])}")
            pass_count += 1
        
        print()
    
    # Summary
    print("=" * 80)
    print("Summary:")
    print(f"  ✅ Passed: {pass_count}")
    print(f"  ⚠️  Warnings: {warning_count}")
    print(f"  ❌ Errors: {error_count}")
    print(f"  Total: {len(results)}")
    print("=" * 80)
    
    # Detailed warnings if any
    if warning_count > 0:
        print("\n" + "=" * 80)
        print("Detailed Warnings:")
        print("=" * 80)
        for result in results:
            if result['status'] == 'WARNING':
                print(f"\n{result['state']}:")
                print(f"  Message: {result.get('message', 'N/A')}")
                print(f"  All images in order:")
                for i, img in enumerate(result['all_images_ordered'], 1):
                    plate_type, img_type = parse_image_type(img)
                    type_pri = TYPE_PRIORITY.get(plate_type, 9)
                    img_pri = IMAGE_TYPE_PRIORITY.get(img_type, 4)
                    print(f"    {i}. {img:<40} (type={plate_type}, img_type={img_type}, priority={type_pri},{img_pri})")
    
    return results


def main():
    """Main function."""
    results = test_all_states()
    
    # Return exit code based on errors
    error_count = sum(1 for r in results if r['status'] == 'ERROR')
    return 1 if error_count > 0 else 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
