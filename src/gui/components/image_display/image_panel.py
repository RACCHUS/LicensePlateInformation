"""
Image Panel - Displays license plate images
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from ...utils.widget_factory import WidgetFactory


class ImagePanel:
    """Panel for displaying license plate images"""
    
    def __init__(self, parent: tk.Widget, widget_factory: WidgetFactory):
        self.parent = parent
        self.widget_factory = widget_factory
        self.current_image = None
        self.current_state = None
        self.current_plate_type = None
        
        self.setup_panel()
        
    def setup_panel(self):
        """Create the image panel"""
        # Main container with border
        self.main_frame = self.widget_factory.create_frame(self.parent)
        self.main_frame.configure(relief='solid', borderwidth=1)
        self.main_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Image container
        self.image_frame = tk.Frame(self.main_frame, bg='#1a1a1a')
        self.image_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Image label
        self.image_label = tk.Label(
            self.image_frame,
            bg='#1a1a1a',
            fg='#ffffff',
            font=('Segoe UI', 10),
            text="Select a state and plate type to view image",
            justify='center'
        )
        self.image_label.pack(fill='both', expand=True)
        
        # Image info text
        self.info_label = tk.Label(
            self.image_frame,
            bg='#1a1a1a',
            fg='#888888',
            font=('Segoe UI', 8),
            text="",
            justify='center'
        )
        self.info_label.pack(side='bottom', pady=(5, 0))
        
    def update_image(self, state_code: str, plate_type: str = "Standard"):
        """Update panel with license plate image"""
        self.current_state = state_code
        self.current_plate_type = plate_type
        
        # Try to load actual image
        image_path = self._get_image_path(state_code, plate_type)
        
        if os.path.exists(image_path):
            self._load_and_display_image(image_path)
        else:
            self._show_placeholder_image(state_code, plate_type)
            
    def _get_image_path(self, state_code: str, plate_type: str) -> str:
        """Get path to license plate image"""
        # Standard path structure for license plate images
        base_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'images')
        
        # Try different naming conventions
        possible_paths = [
            os.path.join(base_path, f"{state_code}_{plate_type.lower()}.png"),
            os.path.join(base_path, f"{state_code.lower()}_{plate_type.lower()}.png"),
            os.path.join(base_path, f"{state_code}_standard.png"),
            os.path.join(base_path, f"{state_code.lower()}_standard.png"),
            os.path.join(base_path, f"{state_code}.png"),
            os.path.join(base_path, f"{state_code.lower()}.png"),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
                
        return ""
        
    def _load_and_display_image(self, image_path: str):
        """Load and display the license plate image"""
        try:
            # Load and resize image
            pil_image = Image.open(image_path)
            
            # Calculate size maintaining aspect ratio
            display_width = 300
            aspect_ratio = pil_image.height / pil_image.width
            display_height = int(display_width * aspect_ratio)
            
            # Resize image
            pil_image = pil_image.resize((display_width, display_height), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            self.current_image = ImageTk.PhotoImage(pil_image)
            
            # Display image
            self.image_label.configure(image=self.current_image, text="")
            
            # Update info
            info_text = f"{self.current_state} - {self.current_plate_type}"
            if image_path:
                filename = os.path.basename(image_path)
                info_text += f"\n{filename}"
            self.info_label.configure(text=info_text)
            
        except Exception as e:
            self._show_error_message(str(e))
            
    def _show_placeholder_image(self, state_code: str, plate_type: str):
        """Show placeholder when no image is available"""
        # Create a simple placeholder
        placeholder_text = (
            f"🚗\n\n"
            f"{state_code}\n"
            f"{plate_type}\n\n"
            f"Image not available\n"
            f"(Add to /images/ folder)"
        )
        
        self.image_label.configure(image="", text=placeholder_text)
        self.info_label.configure(text=f"Expected: {state_code}_{plate_type.lower()}.png")
        
    def _show_error_message(self, error: str):
        """Show error message when image loading fails"""
        error_text = f"❌\n\nImage Loading Error:\n{error}"
        self.image_label.configure(image="", text=error_text)
        self.info_label.configure(text="Check image file format and accessibility")
        
    def clear_image(self):
        """Clear current image and show default message"""
        self.current_image = None
        self.current_state = None
        self.current_plate_type = None
        
        self.image_label.configure(
            image="",
            text="Select a state and plate type to view image"
        )
        self.info_label.configure(text="")
        
    def get_main_frame(self) -> tk.Widget:
        """Get the main panel frame"""
        return self.main_frame
        
    def resize_image(self, width: int):
        """Resize displayed image to new width"""
        if self.current_image and self.current_state:
            self.update_image(self.current_state, self.current_plate_type or "Standard")