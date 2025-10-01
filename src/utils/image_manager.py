#!/usr/bin/env python3
"""
License Plate Image Management System
Copy of the image manager for proper importing within src structure
"""

import os
import shutil
import json
from pathlib import Path
from PIL import Image
from typing import Dict
import hashlib

class LicensePlateImageManager:
    """Manage license plate images with comprehensive categorization and tagging"""
    
    def __init__(self, project_root=None):
        if project_root is None:
            project_root = Path(__file__).parent.parent.parent
        
        self.project_root = Path(project_root)
        self.images_dir = self.project_root / 'data' / 'images'
        self.supported_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
        
        # Enhanced categorization system
        self.categories = {
            'plates': {
                'description': 'Complete license plate examples',
                'subdirectories': ['passenger', 'commercial', 'motorcycle', 'trailer', 'specialty', 'government', 'temporary', 'antique']
            },
            'characters': {
                'description': 'Individual character references',
                'subdirectories': ['letters', 'numbers', 'ambiguous', 'fonts', 'damaged']
            },
            'stickers': {
                'description': 'Registration stickers and validation tags',
                'subdirectories': ['month', 'year', 'county', 'inspection', 'specialty_tags']
            },
            'logos': {
                'description': 'State logos, seals, and graphic elements',
                'subdirectories': ['seals', 'logos', 'graphics', 'watermarks']
            },
            'processing': {
                'description': 'Images for processing rule validation',
                'subdirectories': ['stacked_chars', 'slanted_text', 'prefix_suffix', 'spacing', 'alignment']
            },
            'reference': {
                'description': 'Documentation and reference materials',
                'subdirectories': ['specifications', 'samples', 'variations', 'historical']
            }
        }
        
        # Tag system for detailed classification
        self.tag_categories = {
            'plate_type': ['passenger', 'commercial', 'motorcycle', 'trailer', 'specialty', 'government', 'temporary', 'antique', 'personalized'],
            'character_type': ['letter', 'number', 'symbol', 'separator'],
            'character_issues': ['O_vs_0', 'I_vs_1', 'S_vs_5', 'B_vs_8', 'damaged', 'unclear'],
            'sticker_type': ['month', 'year', 'county', 'inspection', 'renewal'],
            'sticker_color': ['red', 'blue', 'green', 'yellow', 'white', 'black', 'orange', 'purple'],
            'processing_rule': ['stacked', 'slanted', 'prefix', 'suffix', 'spacing', 'omit_char', 'include_char'],
            'condition': ['clean', 'dirty', 'faded', 'damaged', 'partially_obscured'],
            'lighting': ['daylight', 'artificial', 'flash', 'backlit', 'shadow'],
            'angle': ['straight', 'slight_angle', 'steep_angle', 'side_view'],
            'quality': ['high', 'medium', 'low', 'reference_only']
        }
        
        # Create base directories if they don't exist
        self.images_dir.mkdir(parents=True, exist_ok=True)
    
    def create_state_structure(self, state_abbrev):
        """Create the enhanced directory structure for a state"""
        state_dir = self.images_dir / state_abbrev.upper()
        
        # Create main categories and their subdirectories
        for category, info in self.categories.items():
            category_dir = state_dir / category
            category_dir.mkdir(parents=True, exist_ok=True)
            
            # Create subdirectories for each category
            for subdir in info['subdirectories']:
                (category_dir / subdir).mkdir(parents=True, exist_ok=True)
        
        print(f"[+] Created enhanced directory structure for {state_abbrev}")
        return state_dir
    
    def import_image(self, source_path, state_abbrev, category, subcategory=None, filename=None, description=None, tags=None, plate_type_code=None):
        """Import a single image with enhanced categorization and tagging"""
        source_path = Path(source_path)
        
        if not source_path.exists():
            print(f"[-] Source file not found: {source_path}")
            return False
        
        if source_path.suffix.lower() not in self.supported_formats:
            print(f"[-] Unsupported format: {source_path.suffix}")
            return False
        
        # Validate category
        if category not in self.categories:
            print(f"[-] Invalid category: {category}")
            print(f"    Valid categories: {list(self.categories.keys())}")
            return False
        
        # Create state structure if needed
        state_dir = self.create_state_structure(state_abbrev)
        
        # Determine destination directory
        category_dir = state_dir / category
        if subcategory:
            if subcategory not in self.categories[category]['subdirectories']:
                print(f"[-] Invalid subcategory '{subcategory}' for category '{category}'")
                print(f"    Valid subcategories: {self.categories[category]['subdirectories']}")
                return False
            category_dir = category_dir / subcategory
            category_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename if not provided
        if filename is None:
            filename = source_path.name
        
        # Ensure proper extension
        if not any(filename.lower().endswith(ext) for ext in self.supported_formats):
            filename += source_path.suffix.lower()
        
        dest_path = category_dir / filename
        
        try:
            # Copy and optimize image based on category
            with Image.open(source_path) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                
                # Category-specific resizing
                max_size = self._get_max_size_for_category(category, subcategory)
                if img.width > max_size[0] or img.height > max_size[1]:
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # Save optimized image
                if dest_path.suffix.lower() in ['.jpg', '.jpeg']:
                    img.save(dest_path, 'JPEG', quality=85, optimize=True)
                else:
                    img.save(dest_path, optimize=True)
            
            # Create enhanced metadata file
            self._create_enhanced_metadata(dest_path, description, source_path, tags, plate_type_code, category, subcategory)
            
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
    
    def _get_max_size_for_category(self, category, subcategory=None):
        """Get maximum image size based on category and subcategory"""
        size_map = {
            'plates': (1920, 1080),  # Full plate images
            'characters': (200, 200),  # Individual characters
            'stickers': (300, 300),  # Sticker close-ups
            'logos': (500, 500),  # State logos/seals
            'processing': (1920, 1080),  # Processing examples need detail
            'reference': (1920, 1080)  # Reference materials
        }
        
        # Subcategory-specific overrides
        if category == 'characters' and subcategory == 'ambiguous':
            return (400, 400)  # Need more detail for ambiguous characters
        elif category == 'stickers' and subcategory in ['month', 'year']:
            return (150, 150)  # Small stickers
        elif category == 'processing' and subcategory == 'stacked_chars':
            return (800, 600)  # Need detail for stacking analysis
        
        return size_map.get(category, (1920, 1080))
    
    def _create_enhanced_metadata(self, image_path, description, source_path, tags, plate_type_code, category, subcategory):
        """Create enhanced metadata file with comprehensive tagging"""
        metadata = {
            'filename': image_path.name,
            'description': description or 'Imported image',
            'source': str(source_path),
            'imported_date': '2025-09-30',
            'file_size': image_path.stat().st_size,
            'checksum': self._calculate_checksum(image_path),
            'category': category,
            'subcategory': subcategory,
            'plate_type_code': plate_type_code,
            'tags': tags or [],
            'usage_notes': self._generate_usage_notes(category, subcategory, tags)
        }
        
        # Try to get image dimensions
        try:
            with Image.open(image_path) as img:
                metadata['dimensions'] = {'width': img.width, 'height': img.height}
                metadata['format'] = img.format
                metadata['color_mode'] = img.mode
        except:
            pass
        
        # Add category-specific metadata
        if category == 'plates' and plate_type_code:
            metadata['plate_processing'] = {
                'type_code': plate_type_code,
                'expected_pattern': self._get_pattern_for_type_code(plate_type_code),
                'processing_rules': self._get_processing_rules_for_type(plate_type_code)
            }
        
        metadata_path = image_path.with_suffix(image_path.suffix + '.meta.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def _generate_usage_notes(self, category, subcategory, tags):
        """Generate usage notes based on category and tags"""
        notes = []
        
        if category == 'plates':
            notes.append("Use for plate type identification and pattern validation")
            if subcategory == 'passenger':
                notes.append("Standard passenger plate reference")
            elif subcategory == 'specialty':
                notes.append("Specialty plate with unique design elements")
        
        elif category == 'characters':
            notes.append("Character recognition training and validation")
            if subcategory == 'ambiguous':
                notes.append("Critical for O/0, I/1, S/5, B/8 disambiguation")
            elif subcategory == 'damaged':
                notes.append("Examples of damaged or unclear characters")
        
        elif category == 'stickers':
            notes.append("Registration sticker identification and color validation")
            if subcategory in ['month', 'year']:
                notes.append("Date validation and expiration checking")
        
        elif category == 'processing':
            notes.append("Processing rule validation and algorithm training")
            if subcategory == 'stacked_chars':
                notes.append("Determine if stacked characters should be omitted or included")
            elif subcategory == 'slanted_text':
                notes.append("Handle slanted or angled text processing")
        
        if tags:
            for tag in tags:
                if tag in ['O_vs_0', 'I_vs_1', 'S_vs_5', 'B_vs_8']:
                    notes.append(f"Specifically addresses {tag} character confusion")
                elif tag in ['stacked', 'slanted']:
                    notes.append(f"Example of {tag} text layout requiring special handling")
        
        return notes
    
    def _get_pattern_for_type_code(self, type_code):
        """Get expected pattern for a plate type code (placeholder - would load from state data)"""
        # This would integrate with your existing state JSON data
        return "ABC123"  # Placeholder
    
    def _get_processing_rules_for_type(self, type_code):
        """Get processing rules for a plate type (placeholder - would load from state data)"""
        # This would integrate with your existing processing metadata
        return {"requires_prefix": False, "requires_suffix": False}  # Placeholder
    
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
    
    def list_images(self, state_abbrev=None, category=None, subcategory=None, tags=None, plate_type_code=None):
        """List all images with enhanced filtering options"""
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
                    img_subcategory = path_parts[2] if len(path_parts) >= 3 else None
                    
                    # Filter by category if specified
                    if category and img_category != category:
                        continue
                    
                    # Filter by subcategory if specified
                    if subcategory and img_subcategory != subcategory:
                        continue
                    
                    # Load metadata for tag and plate type filtering
                    metadata_path = image_file.with_suffix(image_file.suffix + '.meta.json')
                    metadata = {}
                    if metadata_path.exists():
                        try:
                            with open(metadata_path, 'r') as f:
                                metadata = json.load(f)
                        except:
                            pass
                    
                    # Filter by tags if specified
                    if tags:
                        image_tags = metadata.get('tags', [])
                        if not any(tag in image_tags for tag in tags):
                            continue
                    
                    # Filter by plate type code if specified
                    if plate_type_code and metadata.get('plate_type_code') != plate_type_code:
                        continue
                    
                    results.append({
                        'path': image_file,
                        'state': img_state,
                        'category': img_category,
                        'subcategory': img_subcategory,
                        'filename': image_file.name,
                        'size': image_file.stat().st_size,
                        'metadata': metadata
                    })
        
        return results
    
    def find_images_by_plate_type(self, plate_type_code, state_abbrev=None):
        """Find all images for a specific plate type code"""
        return self.list_images(
            state_abbrev=state_abbrev, 
            category='plates', 
            plate_type_code=plate_type_code
        )
    
    def find_character_examples(self, character, state_abbrev=None, issue_type=None):
        """Find character examples, optionally filtered by specific issues"""
        tags = [character]
        if issue_type:
            tags.append(issue_type)
        
        return self.list_images(
            state_abbrev=state_abbrev,
            category='characters',
            tags=tags
        )
    
    def find_sticker_examples(self, sticker_type=None, color=None, state_abbrev=None):
        """Find sticker examples by type and/or color"""
        tags = []
        if sticker_type:
            tags.append(sticker_type)
        if color:
            tags.append(color)
        
        subcategory = sticker_type if sticker_type in ['month', 'year', 'county', 'inspection'] else None
        
        return self.list_images(
            state_abbrev=state_abbrev,
            category='stickers',
            subcategory=subcategory,
            tags=tags
        )
    
    def find_processing_examples(self, processing_rule, state_abbrev=None):
        """Find examples for specific processing rules"""
        return self.list_images(
            state_abbrev=state_abbrev,
            category='processing',
            tags=[processing_rule]
        )
    
    def generate_inventory_report(self):
        """Generate a comprehensive inventory report with enhanced categorization"""
        print("LICENSE PLATE IMAGE INVENTORY")
        print("=" * 40)
        
        states_with_images = set()
        total_images = 0
        category_counts = {}
        tag_counts = {}
        plate_type_counts = {}
        
        for state_dir in self.images_dir.iterdir():
            if state_dir.is_dir() and state_dir.name != '__pycache__':
                state_images = self.list_images(state_dir.name)
                if state_images:
                    states_with_images.add(state_dir.name)
                    
                    print(f"\n{state_dir.name} ({len(state_images)} images):")
                    
                    # Count by category and subcategory
                    state_categories = {}
                    for img in state_images:
                        cat = img['category']
                        subcat = img['subcategory']
                        
                        cat_key = f"{cat}/{subcat}" if subcat else cat
                        state_categories[cat_key] = state_categories.get(cat_key, 0) + 1
                        category_counts[cat_key] = category_counts.get(cat_key, 0) + 1
                        total_images += 1
                        
                        # Count tags
                        for tag in img['metadata'].get('tags', []):
                            tag_counts[tag] = tag_counts.get(tag, 0) + 1
                        
                        # Count plate types
                        plate_type = img['metadata'].get('plate_type_code')
                        if plate_type:
                            plate_type_counts[plate_type] = plate_type_counts.get(plate_type, 0) + 1
                    
                    for cat, count in sorted(state_categories.items()):
                        print(f"  • {cat}: {count} images")
        
        print(f"\nSUMMARY:")
        print(f"States with images: {len(states_with_images)}")
        print(f"Total images: {total_images}")
        
        print(f"\nCATEGORIES:")
        for cat, count in sorted(category_counts.items()):
            print(f"  • {cat}: {count} images")
        
        if tag_counts:
            print(f"\nTOP TAGS:")
            for tag, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
                print(f"  • {tag}: {count} images")
        
        if plate_type_counts:
            print(f"\nPLATE TYPES:")
            for ptype, count in sorted(plate_type_counts.items()):
                print(f"  • Type {ptype}: {count} images")
    
    def get_images_for_plate_type_from_state_data(self, state_abbrev, plate_type_name):
        """Get images that match a specific plate type from state JSON data"""
        # This method would integrate with your state JSON files
        # to find images that correspond to specific plate types
        
        try:
            state_file = self.project_root / 'data' / 'states' / f'{state_abbrev.lower()}.json'
            if not state_file.exists():
                return []
            
            with open(state_file, 'r') as f:
                state_data = json.load(f)
            
            # Find the plate type
            matching_plate_type = None
            for plate_type in state_data.get('plate_types', []):
                if plate_type.get('type_name') == plate_type_name:
                    matching_plate_type = plate_type
                    break
            
            if not matching_plate_type:
                return []
            
            # Look for images with matching plate type code
            type_code = matching_plate_type.get('code_number')
            if type_code:
                return self.find_images_by_plate_type(type_code, state_abbrev)
            
            # Fallback: look for images with tags matching the plate type name
            return self.list_images(
                state_abbrev=state_abbrev,
                category='plates',
                tags=[plate_type_name.lower().replace(' ', '_')]
            )
            
        except Exception as e:
            print(f"[-] Error loading state data for {state_abbrev}: {e}")
            return []
    
    def add_tags_to_image(self, image_path, new_tags):
        """Add tags to an existing image"""
        metadata_path = Path(image_path).with_suffix(Path(image_path).suffix + '.meta.json')
        
        if not metadata_path.exists():
            print(f"[-] No metadata file found for {image_path}")
            return False
        
        try:
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            
            existing_tags = set(metadata.get('tags', []))
            existing_tags.update(new_tags)
            metadata['tags'] = list(existing_tags)
            
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            print(f"[+] Added tags {new_tags} to {image_path}")
            return True
            
        except Exception as e:
            print(f"[-] Error adding tags to {image_path}: {e}")
            return False
    
    def get_image_metadata(self, image_path: str) -> Dict:
        """Get metadata for a specific image"""
        try:
            # Look for companion metadata file
            metadata_path = Path(image_path).with_suffix('.json')
            
            if metadata_path.exists():
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Generate basic metadata from file path
                path_parts = Path(image_path).parts
                
                # Try to extract state, category, subcategory from path
                metadata = {
                    'filename': Path(image_path).name,
                    'category': 'unknown',
                    'subcategory': 'unknown',
                    'tags': [],
                    'description': 'No metadata file found'
                }
                
                # Look for state abbreviation and category in path
                if 'images' in path_parts:
                    images_index = path_parts.index('images')
                    if len(path_parts) > images_index + 1:
                        metadata['state'] = path_parts[images_index + 1]
                    if len(path_parts) > images_index + 2:
                        metadata['category'] = path_parts[images_index + 2]
                    if len(path_parts) > images_index + 3:
                        metadata['subcategory'] = path_parts[images_index + 3]
                
                return metadata
                
        except Exception as e:
            print(f"Error loading metadata for {image_path}: {e}")
            return {
                'filename': Path(image_path).name,
                'category': 'unknown',
                'subcategory': 'unknown',
                'tags': [],
                'description': f'Error loading metadata: {str(e)}'
            }