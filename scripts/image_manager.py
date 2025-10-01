#!/usr/bin/env python3
"""
License Plate Image Management System
Comprehensive tool for importing, organizing, and managing license plate images
"""

import os
import shutil
import json
from pathlib import Path
from PIL import Image
import hashlib

class LicensePlateImageManager:
    """Manage license plate images with automatic organization and validation"""
    
    def __init__(self, project_root=None):
        if project_root is None:
            project_root = Path(__file__).parent.parent
        
        self.project_root = Path(project_root)
        self.images_dir = self.project_root / 'data' / 'images'
        self.supported_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
        
        # Create base directories if they don't exist
        self.images_dir.mkdir(parents=True, exist_ok=True)
    
    def create_state_structure(self, state_abbrev):
        """Create the directory structure for a state"""
        state_dir = self.images_dir / state_abbrev.upper()
        
        subdirs = ['plates', 'logos', 'characters', 'reference']
        for subdir in subdirs:
            (state_dir / subdir).mkdir(parents=True, exist_ok=True)
        
        print(f"[+] Created directory structure for {state_abbrev}")
        return state_dir
    
    def import_image(self, source_path, state_abbrev, category, filename=None, description=None):
        """Import a single image with proper organization"""
        source_path = Path(source_path)
        
        if not source_path.exists():
            print(f"[-] Source file not found: {source_path}")
            return False
        
        if source_path.suffix.lower() not in self.supported_formats:
            print(f"[-] Unsupported format: {source_path.suffix}")
            return False
        
        # Create state structure if needed
        state_dir = self.create_state_structure(state_abbrev)
        
        # Determine destination directory
        category_dir = state_dir / category
        if not category_dir.exists():
            print(f"[-] Invalid category: {category}")
            return False
        
        # Generate filename if not provided
        if filename is None:
            filename = source_path.name
        
        # Ensure proper extension
        if not any(filename.lower().endswith(ext) for ext in self.supported_formats):
            filename += source_path.suffix.lower()
        
        dest_path = category_dir / filename
        
        try:
            # Copy and optimize image
            with Image.open(source_path) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                
                # Resize if too large (max 1920x1080 for plates)
                if category == 'plates' and (img.width > 1920 or img.height > 1080):
                    img.thumbnail((1920, 1080), Image.Resampling.LANCZOS)
                elif category == 'characters' and (img.width > 200 or img.height > 200):
                    img.thumbnail((200, 200), Image.Resampling.LANCZOS)
                elif category == 'logos' and (img.width > 500 or img.height > 500):
                    img.thumbnail((500, 500), Image.Resampling.LANCZOS)
                
                # Save optimized image
                if dest_path.suffix.lower() in ['.jpg', '.jpeg']:
                    img.save(dest_path, 'JPEG', quality=85, optimize=True)
                else:
                    img.save(dest_path, optimize=True)
            
            # Create metadata file
            self._create_image_metadata(dest_path, description, source_path)
            
            print(f"[+] Imported: {dest_path.relative_to(self.project_root)}")
            return True
            
        except Exception as e:
            print(f"[-] Error importing {source_path}: {e}")
            return False
    
    def import_batch(self, source_directory, state_abbrev, mapping_rules=None):
        """Import multiple images from a directory with automatic categorization"""
        source_dir = Path(source_directory)
        
        if not source_dir.exists():
            print(f"[-] Source directory not found: {source_dir}")
            return
        
        # Default mapping rules
        if mapping_rules is None:
            mapping_rules = {
                'plate': 'plates',
                'license': 'plates',
                'logo': 'logos',
                'seal': 'logos',
                'char': 'characters',
                'letter': 'characters',
                'number': 'characters',
                'font': 'characters'
            }
        
        imported_count = 0
        skipped_count = 0
        
        print(f"Importing images from {source_dir} for {state_abbrev}...")
        
        for file_path in source_dir.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in self.supported_formats:
                # Determine category from filename
                category = 'reference'  # default
                filename_lower = file_path.name.lower()
                
                for keyword, cat in mapping_rules.items():
                    if keyword in filename_lower:
                        category = cat
                        break
                
                if self.import_image(file_path, state_abbrev, category):
                    imported_count += 1
                else:
                    skipped_count += 1
        
        print(f"Batch import complete: {imported_count} imported, {skipped_count} skipped")
    
    def _create_image_metadata(self, image_path, description, source_path):
        """Create metadata file for an image"""
        metadata = {
            'filename': image_path.name,
            'description': description or 'Imported image',
            'source': str(source_path),
            'imported_date': '2025-09-30',  # Current date
            'file_size': image_path.stat().st_size,
            'checksum': self._calculate_checksum(image_path)
        }
        
        # Try to get image dimensions
        try:
            with Image.open(image_path) as img:
                metadata['dimensions'] = {'width': img.width, 'height': img.height}
                metadata['format'] = img.format
        except:
            pass
        
        metadata_path = image_path.with_suffix(image_path.suffix + '.meta.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def _calculate_checksum(self, file_path):
        """Calculate MD5 checksum for file integrity"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def list_images(self, state_abbrev=None, category=None):
        """List all images with optional filtering"""
        results = []
        
        search_dir = self.images_dir
        if state_abbrev:
            search_dir = search_dir / state_abbrev.upper()
            if not search_dir.exists():
                print(f"[-] No images found for state: {state_abbrev}")
                return results
        
        for image_file in search_dir.rglob('*'):
            if (image_file.is_file() and 
                image_file.suffix.lower() in self.supported_formats and
                not image_file.name.startswith('.')):
                
                # Extract state and category from path
                rel_path = image_file.relative_to(self.images_dir)
                path_parts = rel_path.parts
                
                if len(path_parts) >= 2:
                    img_state = path_parts[0]
                    img_category = path_parts[1]
                    
                    # Filter by category if specified
                    if category and img_category != category:
                        continue
                    
                    results.append({
                        'path': image_file,
                        'state': img_state,
                        'category': img_category,
                        'filename': image_file.name,
                        'size': image_file.stat().st_size
                    })
        
        return results
    
    def generate_inventory_report(self):
        """Generate a comprehensive inventory report"""
        print("LICENSE PLATE IMAGE INVENTORY")
        print("=" * 40)
        
        states_with_images = set()
        total_images = 0
        category_counts = {}
        
        for state_dir in self.images_dir.iterdir():
            if state_dir.is_dir() and state_dir.name != '__pycache__':
                state_images = self.list_images(state_dir.name)
                if state_images:
                    states_with_images.add(state_dir.name)
                    
                    print(f"\n{state_dir.name} ({len(state_images)} images):")
                    
                    # Count by category
                    state_categories = {}
                    for img in state_images:
                        cat = img['category']
                        state_categories[cat] = state_categories.get(cat, 0) + 1
                        category_counts[cat] = category_counts.get(cat, 0) + 1
                        total_images += 1
                    
                    for cat, count in sorted(state_categories.items()):
                        print(f"  • {cat}: {count} images")
        
        print(f"\nSUMMARY:")
        print(f"States with images: {len(states_with_images)}")
        print(f"Total images: {total_images}")
        print(f"Categories:")
        for cat, count in sorted(category_counts.items()):
            print(f"  • {cat}: {count} images")
    
    def create_sample_structure(self):
        """Create sample directory structure for demonstration"""
        sample_states = ['FL', 'TX', 'CA', 'NY', 'GA']
        
        print("Creating sample image directory structure...")
        for state in sample_states:
            self.create_state_structure(state)
        
        # Create sample readme files
        for state in sample_states:
            state_dir = self.images_dir / state
            readme_content = f"""# {state} License Plate Images

## Directory Structure

- **plates/**: Example license plate images for {state}
- **logos/**: State logos, seals, and graphic elements
- **characters/**: Character reference images showing {state}-specific fonts
- **reference/**: Additional reference materials

## Adding Images

To add images for {state}:

1. Place plate images in `plates/` directory
2. Place logos/seals in `logos/` directory  
3. Place character references in `characters/` directory
4. Use descriptive filenames
5. Supported formats: JPG, PNG, BMP, TIFF, WebP

## Image Guidelines

- **Plates**: Clear, well-lit photos showing complete plates
- **Logos**: High-resolution PNG files with transparency when possible
- **Characters**: Individual character images showing font details
- **Quality**: High resolution but reasonable file sizes (under 1MB)

## File Naming Examples

- `passenger_standard.jpg` - Standard passenger plate
- `commercial_truck.jpg` - Commercial truck plate
- `specialty_university.jpg` - University specialty plate
- `character_O_letter.png` - Letter O character reference
- `character_0_number.png` - Number 0 character reference
- `state_seal.png` - Official state seal
"""
            
            readme_path = state_dir / 'README.md'
            with open(readme_path, 'w') as f:
                f.write(readme_content)

def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='License Plate Image Management')
    parser.add_argument('action', choices=['import', 'batch', 'list', 'inventory', 'setup'],
                       help='Action to perform')
    parser.add_argument('--source', help='Source file or directory')
    parser.add_argument('--state', help='State abbreviation (e.g., FL, TX)')
    parser.add_argument('--category', choices=['plates', 'logos', 'characters', 'reference'],
                       help='Image category')
    parser.add_argument('--filename', help='Destination filename')
    parser.add_argument('--description', help='Image description')
    
    args = parser.parse_args()
    
    manager = LicensePlateImageManager()
    
    if args.action == 'import':
        if not args.source or not args.state or not args.category:
            print("[-] Import requires --source, --state, and --category")
            return
        manager.import_image(args.source, args.state, args.category, 
                           args.filename, args.description)
    
    elif args.action == 'batch':
        if not args.source or not args.state:
            print("[-] Batch import requires --source and --state")
            return
        manager.import_batch(args.source, args.state)
    
    elif args.action == 'list':
        images = manager.list_images(args.state, args.category)
        for img in images:
            print(f"{img['state']}/{img['category']}/{img['filename']} ({img['size']} bytes)")
    
    elif args.action == 'inventory':
        manager.generate_inventory_report()
    
    elif args.action == 'setup':
        manager.create_sample_structure()
        print("[+] Sample structure created")

if __name__ == '__main__':
    main()