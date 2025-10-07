"""
Image Viewer - Advanced license plate image viewer with navigation
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import json
from typing import List, Dict, Optional, Tuple


class PlateImageViewer:
    """Advanced image viewer for license plates with navigation and smart ordering"""
    
    # Priority order for plate types (generic first, then commercial, then passenger)
    TYPE_PRIORITY = {
        'generic': 0,         # plate_sample without type specified
        'truck': 1,
        'trailer': 1,
        'semi-trailer': 1,
        'semi': 1,
        'commercial': 1,
        'passenger': 2,
        'standard': 2,
        'motorcycle': 3,
        'specialty': 4,
        'vanity': 5,
        'government': 6,
        'dealer': 7,
        'apportioned': 8
    }
    
    # Priority order for image types within each plate type
    IMAGE_TYPE_PRIORITY = {
        'sample': 1,          # plate_sample - most common
        'blank': 2,           # blank_template - useful reference
        'font': 3,            # character_font_sample
        'variation': 4        # variations
    }
    
    def __init__(self, parent: tk.Widget):
        self.parent = parent
        self.current_state = None
        self.current_images: List[Dict] = []  # List of {path, name, type, plate_type}
        self.current_index = 0
        self.photo_image = None  # Keep reference to prevent garbage collection
        
        self.setup_viewer()
        
    def setup_viewer(self):
        """Create the image viewer interface"""
        # Main container
        self.main_frame = tk.Frame(self.parent, bg='#2a2a2a', relief='solid', borderwidth=1)
        self.main_frame.pack(fill='both', expand=True)
        
        # Top navigation bar
        nav_bar = tk.Frame(self.main_frame, bg='#1a1a1a', height=40)
        nav_bar.pack(fill='x', side='top')
        nav_bar.pack_propagate(False)
        
        # Previous button
        self.prev_button = tk.Button(
            nav_bar,
            text="◀ Previous",
            bg='#404040',
            fg='#ffffff',
            font=('Segoe UI', 9),
            relief='flat',
            borderwidth=0,
            padx=15,
            pady=5,
            command=self.show_previous,
            cursor='hand2'
        )
        self.prev_button.pack(side='left', padx=10, pady=5)
        
        # Image counter
        self.counter_label = tk.Label(
            nav_bar,
            text="No images",
            bg='#1a1a1a',
            fg='#888888',
            font=('Segoe UI', 9)
        )
        self.counter_label.pack(side='left', expand=True)
        
        # Next button
        self.next_button = tk.Button(
            nav_bar,
            text="Next ▶",
            bg='#404040',
            fg='#ffffff',
            font=('Segoe UI', 9),
            relief='flat',
            borderwidth=0,
            padx=15,
            pady=5,
            command=self.show_next,
            cursor='hand2'
        )
        self.next_button.pack(side='right', padx=10, pady=5)
        
        # Image display area with fixed size
        self.image_frame = tk.Frame(self.main_frame, bg='#2a2a2a', width=450, height=300)
        self.image_frame.pack(fill='both', expand=True, padx=10, pady=10)
        self.image_frame.pack_propagate(False)  # Prevent frame from resizing to content
        
        # Image label
        self.image_label = tk.Label(
            self.image_frame,
            bg='#2a2a2a',
            fg='#888888',
            font=('Segoe UI', 11),
            text="Select a state to view images",
            justify='center'
        )
        self.image_label.pack(fill='both', expand=True)
        
        # Info bar at bottom
        info_bar = tk.Frame(self.main_frame, bg='#1a1a1a', height=60)
        info_bar.pack(fill='x', side='bottom')
        info_bar.pack_propagate(False)
        
        # Image name
        self.image_name_label = tk.Label(
            info_bar,
            text="",
            bg='#1a1a1a',
            fg='#ffffff',
            font=('Segoe UI', 9, 'bold'),
            anchor='w'
        )
        self.image_name_label.pack(fill='x', padx=10, pady=(5, 0))
        
        # Image details
        self.image_details_label = tk.Label(
            info_bar,
            text="",
            bg='#1a1a1a',
            fg='#888888',
            font=('Segoe UI', 8),
            anchor='w'
        )
        self.image_details_label.pack(fill='x', padx=10, pady=(2, 5))
        
        # Disable navigation buttons initially
        self._update_navigation_buttons()
        
    def update_state(self, state_code: str, plate_type: Optional[str] = None):
        """Update viewer with images from the selected state and optionally filter by plate type"""
        self.current_state = state_code
        self.current_index = 0
        
        # Scan for available images
        all_images = self._scan_state_images(state_code)
        
        # Filter by plate type if specified
        if plate_type:
            # Normalize plate type name for matching
            plate_type_normalized = plate_type.lower().replace(' ', '_').replace('-', '_')
            self.current_images = [
                img for img in all_images 
                if plate_type_normalized in img['display_name'].lower().replace(' ', '_').replace('-', '_')
                or plate_type_normalized in img.get('plate_type', '').lower().replace(' ', '_').replace('-', '_')
            ]
            # If no matches with filtered type, show all images
            if not self.current_images:
                self.current_images = all_images
        else:
            self.current_images = all_images
        
        if self.current_images:
            # Show first image
            self._display_current_image()
        else:
            # Show "no images" message
            self._show_no_images_message(state_code)
        
        self._update_navigation_buttons()
        
    def show_next(self):
        """Show next image"""
        if self.current_images and self.current_index < len(self.current_images) - 1:
            self.current_index += 1
            self._display_current_image()
            self._update_navigation_buttons()
            
    def show_previous(self):
        """Show previous image"""
        if self.current_images and self.current_index > 0:
            self.current_index -= 1
            self._display_current_image()
            self._update_navigation_buttons()
            
    def _scan_state_images(self, state_code: str) -> List[Dict]:
        """Scan for all available images for a state, ordered by priority"""
        images = []
        
        # Load state JSON to get plate type information
        state_json = self._load_state_json(state_code)
        plate_types_map = self._build_plate_types_map(state_json)
        
        # Base path for images
        base_path = os.path.join(
            os.path.dirname(__file__), '..', '..', '..', '..', 
            'data', 'images', state_code
        )
        base_path = os.path.normpath(base_path)
        
        if not os.path.exists(base_path):
            return []
        
        # Check for plates subdirectory
        plates_dir = os.path.join(base_path, 'plates')
        
        # Also check the Plates directory with state name
        state_folder_name = self._get_state_folder_name(state_code)
        if state_folder_name:
            plates_state_dir = os.path.join(
                os.path.dirname(__file__), '..', '..', '..', '..', 
                'data', 'images', 'Plates', state_folder_name
            )
            plates_state_dir = os.path.normpath(plates_state_dir)
        else:
            plates_state_dir = None
        
        # Scan both base directory and plates subdirectory
        search_dirs = [base_path]
        if os.path.exists(plates_dir):
            search_dirs.append(plates_dir)
        if plates_state_dir and os.path.exists(plates_state_dir):
            search_dirs.append(plates_state_dir)
        
        for search_dir in search_dirs:
            if not os.path.exists(search_dir):
                continue
                
            # Find all image files
            for filename in os.listdir(search_dir):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    # Skip metadata files
                    if filename.endswith('.meta.json'):
                        continue
                    
                    file_path = os.path.join(search_dir, filename)
                    
                    # Parse filename to determine type and plate type
                    image_info = self._parse_image_filename(filename, state_code, plate_types_map)
                    image_info['path'] = file_path
                    
                    images.append(image_info)
        
        # Sort images by priority
        images.sort(key=lambda x: (
            self.TYPE_PRIORITY.get(x['plate_type_category'], 99),
            self.IMAGE_TYPE_PRIORITY.get(x['image_type'], 99),
            x['display_name']
        ))
        
        return images
    
    def _parse_image_filename(self, filename: str, state_code: str, plate_types_map: Optional[Dict] = None) -> Dict:
        """Parse filename to extract image information"""
        if plate_types_map is None:
            plate_types_map = {}
            
        # Remove extension
        name_without_ext = os.path.splitext(filename)[0]
        
        # Common patterns
        name_lower = name_without_ext.lower()
        
        # Try to find matching plate type from JSON
        plate_type_name = None
        for img_path, type_name in plate_types_map.items():
            img_name = os.path.basename(img_path).lower()
            if img_name == filename.lower() or img_name == name_lower:
                plate_type_name = type_name
                break
        
        # Determine image type
        image_type = 'sample'  # default
        if 'blank' in name_lower or 'template' in name_lower:
            image_type = 'blank'
        elif 'font' in name_lower:
            image_type = 'font'
        elif 'variation' in name_lower or 'variant' in name_lower:
            image_type = 'variation'
        
        # Determine plate type category
        # Check if this is a generic plate_sample (no type keywords)
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
        
        # Create display name
        display_name = name_without_ext.replace('_', ' ').title()
        
        return {
            'filename': filename,
            'display_name': display_name,
            'image_type': image_type,
            'plate_type_category': plate_type_category,
            'plate_type_name': plate_type_name,  # Actual plate type name from JSON
            'state_code': state_code
        }
    
    def _display_current_image(self):
        """Display the current image"""
        if not self.current_images or self.current_index >= len(self.current_images):
            return
        
        current_image = self.current_images[self.current_index]
        image_path = current_image['path']
        
        try:
            # Load image
            pil_image = Image.open(image_path)
            
            # Get actual frame dimensions (use update to get current size)
            self.image_frame.update_idletasks()
            frame_width = self.image_frame.winfo_width() - 20  # Padding
            frame_height = self.image_frame.winfo_height() - 20  # Padding
            
            # Ensure minimum dimensions
            if frame_width < 100:
                frame_width = 430  # Default from fixed size
            if frame_height < 100:
                frame_height = 280
            
            # Maintain aspect ratio, prioritize width
            img_width, img_height = pil_image.size
            
            # Calculate scaling based on width first
            width_scale = frame_width / img_width
            new_width = frame_width
            new_height = int(img_height * width_scale)
            
            # If height exceeds frame, scale by height instead
            if new_height > frame_height:
                height_scale = frame_height / img_height
                new_width = int(img_width * height_scale)
                new_height = frame_height
            
            # Resize image
            pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            self.photo_image = ImageTk.PhotoImage(pil_image)
            
            # Display
            self.image_label.configure(image=self.photo_image, text="", bg='#2a2a2a')
            
            # Update info labels
            self._update_info_labels(current_image)
            
            # Update counter
            total = len(self.current_images)
            self.counter_label.configure(
                text=f"Image {self.current_index + 1} of {total}",
                fg='#4CAF50'
            )
            
        except Exception as e:
            # Show error
            self.image_label.configure(
                image="",
                text=f"❌ Error loading image:\n{str(e)}",
                bg='#2a2a2a',
                fg='#ff5555'
            )
            self._update_info_labels(current_image, error=True)
    
    def _update_info_labels(self, image_info: Dict, error: bool = False):
        """Update the information labels below the image"""
        if error:
            self.image_name_label.configure(
                text=f"Error: {image_info['filename']}",
                fg='#ff5555'
            )
            self.image_details_label.configure(
                text="Could not load this image file",
                fg='#ff5555'
            )
        else:
            # Name - show plate type name if available, otherwise display name
            plate_type_name = image_info.get('plate_type_name')
            if plate_type_name:
                display_text = f"{plate_type_name}"
            else:
                display_text = image_info['display_name']
            
            self.image_name_label.configure(
                text=display_text,
                fg='#ffffff'
            )
            
            # Details - show filename and category
            state = image_info['state_code']
            filename = image_info['filename']
            
            # Build details text
            details_parts = [state]
            
            if plate_type_name:
                # If we have the actual plate type name, show it
                details_parts.append(f"Plate Type: {plate_type_name}")
            else:
                # Otherwise show the category we detected
                plate_type = image_info['plate_type_category'].title()
                details_parts.append(f"Category: {plate_type}")
            
            details_parts.append(f"File: {filename}")
            
            details_text = " • ".join(details_parts)
            self.image_details_label.configure(
                text=details_text,
                fg='#888888'
            )
    
    def _update_navigation_buttons(self):
        """Enable/disable navigation buttons based on current position"""
        if not self.current_images:
            self.prev_button.configure(state='disabled', bg='#2a2a2a')
            self.next_button.configure(state='disabled', bg='#2a2a2a')
            self.counter_label.configure(text="No images available", fg='#888888')
            return
        
        # Previous button
        if self.current_index > 0:
            self.prev_button.configure(state='normal', bg='#404040')
        else:
            self.prev_button.configure(state='disabled', bg='#2a2a2a')
        
        # Next button
        if self.current_index < len(self.current_images) - 1:
            self.next_button.configure(state='normal', bg='#404040')
        else:
            self.next_button.configure(state='disabled', bg='#2a2a2a')
    
    def _show_no_images_message(self, state_code: str):
        """Show message when no images are available"""
        message = (
            f"📷\n\n"
            f"No images available for {state_code}\n\n"
            f"Add images to:\n"
            f"data/images/{state_code}/plates/\n\n"
            f"Supported formats: PNG, JPG, JPEG, GIF"
        )
        
        self.image_label.configure(
            image="",
            text=message,
            bg='#2a2a2a',
            fg='#888888',
            font=('Segoe UI', 10)
        )
        
        self.image_name_label.configure(text=f"{state_code} - No Images", fg='#888888')
        self.image_details_label.configure(text="Add images to see them here", fg='#888888')
        self.counter_label.configure(text="0 images", fg='#888888')
    
    def clear(self):
        """Clear the viewer"""
        self.current_state = None
        self.current_images = []
        self.current_index = 0
        self.photo_image = None
        
        self.image_label.configure(
            image="",
            text="Select a state to view images",
            bg='#2a2a2a',
            fg='#888888',
            font=('Segoe UI', 11)
        )
        
        self.image_name_label.configure(text="", fg='#ffffff')
        self.image_details_label.configure(text="", fg='#888888')
        self.counter_label.configure(text="No images", fg='#888888')
        
        self._update_navigation_buttons()
    
    def get_frame(self) -> tk.Frame:
        """Get the main frame"""
        return self.main_frame
    
    def _load_state_json(self, state_code: str) -> Optional[Dict]:
        """Load the state JSON file to get plate type information"""
        try:
            # Get the state filename
            state_filename = self._get_state_json_filename(state_code)
            if not state_filename:
                return None
            
            json_path = os.path.join(
                os.path.dirname(__file__), '..', '..', '..', '..', 
                'data', 'states', state_filename
            )
            json_path = os.path.normpath(json_path)
            
            if not os.path.exists(json_path):
                return None
            
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return None
    
    def _build_plate_types_map(self, state_json: Optional[Dict]) -> Dict[str, str]:
        """Build a mapping of image paths to plate type names from JSON"""
        plate_types_map = {}
        
        if not state_json:
            return plate_types_map
        
        # Get plate types
        plate_types = state_json.get('plate_types', [])
        
        for plate_type in plate_types:
            type_name = plate_type.get('type_name', '')
            images = plate_type.get('images', {})
            
            # Map all image paths to this plate type name
            for img_key, img_path in images.items():
                if img_path:
                    # Handle both single paths and lists of paths (variations)
                    if isinstance(img_path, list):
                        for path in img_path:
                            if path:
                                plate_types_map[path] = type_name
                    else:
                        plate_types_map[img_path] = type_name
        
        return plate_types_map
    
    def _get_state_json_filename(self, state_code: str) -> Optional[str]:
        """Get the JSON filename for a state code"""
        # Mapping of state codes to JSON filenames
        state_map = {
            'AL': 'alabama.json', 'AK': 'alaska.json', 'AZ': 'arizona.json',
            'AR': 'arkansas.json', 'CA': 'california.json', 'CO': 'colorado.json',
            'CT': 'connecticut.json', 'DE': 'delaware.json', 'FL': 'florida.json',
            'GA': 'georgia.json', 'HI': 'hawaii.json', 'ID': 'idaho.json',
            'IL': 'illinois.json', 'IN': 'indiana.json', 'IA': 'iowa.json',
            'KS': 'kansas.json', 'KY': 'kentucky.json', 'LA': 'louisiana.json',
            'ME': 'maine.json', 'MD': 'maryland.json', 'MA': 'massachusetts.json',
            'MI': 'michigan.json', 'MN': 'minnesota.json', 'MS': 'mississippi.json',
            'MO': 'missouri.json', 'MT': 'montana.json', 'NE': 'nebraska.json',
            'NV': 'nevada.json', 'NH': 'new_hampshire.json', 'NJ': 'new_jersey.json',
            'NM': 'new_mexico.json', 'NY': 'new_york.json', 'NC': 'north_carolina.json',
            'ND': 'north_dakota.json', 'OH': 'ohio.json', 'OK': 'oklahoma.json',
            'OR': 'oregon.json', 'PA': 'pennsylvania.json', 'RI': 'rhode_island.json',
            'SC': 'south_carolina.json', 'SD': 'south_dakota.json', 'TN': 'tennessee.json',
            'TX': 'texas.json', 'UT': 'utah.json', 'VT': 'vermont.json',
            'VA': 'virginia.json', 'WA': 'washington.json', 'WV': 'west_virginia.json',
            'WI': 'wisconsin.json', 'WY': 'wyoming.json'
        }
        return state_map.get(state_code)
    
    def _get_state_folder_name(self, state_code: str) -> Optional[str]:
        """Get the folder name in data/images/Plates for a state code"""
        # Mapping of state codes to folder names in Plates directory
        folder_map = {
            'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona',
            'AR': 'Arkansas', 'CA': 'California', 'CO': 'Colorado',
            'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida',
            'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho',
            'IL': 'Illinios',  # Note: typo in folder name
            'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
            'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine',
            'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan',
            'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri',
            'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
            'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico',
            'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota',
            'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon',
            'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
            'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas',
            'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia',
            'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin',
            'WY': 'Wyoming'
        }
        return folder_map.get(state_code)
