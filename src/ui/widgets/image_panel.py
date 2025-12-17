"""
Image Panel Widget for License Plate Information System.

Displays plate images for the selected state with navigation controls.
"""

from pathlib import Path
from typing import Optional, Dict, Tuple

from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QPixmap, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QSizePolicy, QComboBox, QFrame
)


class ImagePanel(QWidget):
    """
    Panel for displaying plate images with navigation.
    
    Features:
    - Image viewer with scaling
    - Previous/Next navigation
    - Image counter display
    - Keyboard navigation (Left/Right arrows)
    - Category filter dropdown
    - Smart image ordering by plate type priority
    """
    
    # Signal emitted when image changes
    image_changed = Signal(str)  # image_path
    
    # Priority order for plate types (lower = shown first)
    # Generic/common plates first, commercial vehicles, then passenger
    PLATE_TYPE_PRIORITY: Dict[str, int] = {
        'generic': 0,         # plate_sample without type specified
        'apportioned': 1,     # IRP apportioned plates (commercial priority)
        'truck': 1,
        'trailer': 1,
        'semi-trailer': 1,
        'semi': 1,
        'commercial': 1,
        'passenger': 2,
        'standard': 2,
        'motorcycle': 3,
        'government': 4,      # Government plates
        'dealer': 5,          # Dealer plates (third to last)
        'specialty': 6,       # Specialty plates (second to last)
        'vanity': 7,          # Vanity/personalized (last)
    }
    
    # Priority order for image types within each plate type
    IMAGE_TYPE_PRIORITY: Dict[str, int] = {
        'sample': 1,          # plate_sample - most common
        'blank': 2,           # blank_template - useful reference
        'font': 3,            # character_font_sample
        'variation': 4        # variations
    }
    
    # Mapping of state codes to folder names in data/images/Plates directory
    STATE_FOLDER_MAP: Dict[str, str] = {
        'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona',
        'AR': 'Arkansas', 'CA': 'California', 'CO': 'Colorado',
        'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida',
        'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho',
        'IL': 'Illinios',  # Note: typo in folder name preserved
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
    
    def __init__(self, data_path: Path, parent=None):
        super().__init__(parent)
        
        self.data_path = data_path
        self.images_path = data_path / "images"
        
        self.current_state: Optional[str] = None
        self.current_images: list[Path] = []
        self.current_index: int = 0
        self.current_category: str = "all"
        self.zoom_level: float = 1.0  # 1.0 = fit to panel
        self.current_pixmap: Optional[QPixmap] = None
        
        self._setup_ui()
        self._setup_shortcuts()
    
    def _setup_ui(self):
        """Set up the panel UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)
        
        # Header with title and category filter
        header = QHBoxLayout()
        
        self.title_label = QLabel("Plate Images")
        self.title_label.setStyleSheet("font-weight: bold; color: #4CAF50; font-size: 14px;")
        header.addWidget(self.title_label)
        
        header.addStretch()
        
        # Category filter
        self.category_combo = QComboBox()
        self.category_combo.setMinimumWidth(120)
        self.category_combo.addItem("All Images", "all")
        self.category_combo.addItem("Standard Plates", "standard")
        self.category_combo.addItem("Specialty Plates", "specialty")
        self.category_combo.addItem("Government", "government")
        self.category_combo.addItem("Characters", "characters")
        self.category_combo.currentIndexChanged.connect(self._on_category_changed)
        header.addWidget(self.category_combo)
        
        layout.addLayout(header)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #404040;")
        layout.addWidget(separator)
        
        # Image display area
        self.image_scroll = QScrollArea()
        self.image_scroll.setWidgetResizable(True)
        self.image_scroll.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_scroll.setStyleSheet("""
            QScrollArea {
                border: 1px solid #404040;
                background-color: #1a1a1a;
                border-radius: 4px;
            }
        """)
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.image_label.setScaledContents(False)
        self.image_scroll.setWidget(self.image_label)
        
        layout.addWidget(self.image_scroll, 1)
        
        # Image name label
        self.image_name_label = QLabel("")
        self.image_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_name_label.setStyleSheet("color: #b0b0b0; font-size: 11px;")
        self.image_name_label.setWordWrap(True)
        layout.addWidget(self.image_name_label)
        
        # Navigation controls (row 1: prev/next and counter)
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(4)
        
        self.prev_btn = QPushButton("◀")
        self.prev_btn.setFixedWidth(40)
        self.prev_btn.clicked.connect(self.show_previous)
        self.prev_btn.setToolTip("Previous image (Left Arrow)")
        nav_layout.addWidget(self.prev_btn)
        
        nav_layout.addStretch()
        
        self.counter_label = QLabel("0 / 0")
        self.counter_label.setStyleSheet("color: #e0e0e0; font-weight: bold;")
        nav_layout.addWidget(self.counter_label)
        
        nav_layout.addStretch()
        
        self.next_btn = QPushButton("▶")
        self.next_btn.setFixedWidth(40)
        self.next_btn.clicked.connect(self.show_next)
        self.next_btn.setToolTip("Next image (Right Arrow)")
        nav_layout.addWidget(self.next_btn)
        
        layout.addLayout(nav_layout)
        
        # Zoom controls (row 2: compact)
        zoom_layout = QHBoxLayout()
        zoom_layout.setSpacing(2)
        
        zoom_layout.addStretch()
        
        self.zoom_out_btn = QPushButton("−")
        self.zoom_out_btn.setFixedSize(28, 24)
        self.zoom_out_btn.clicked.connect(self.zoom_out)
        self.zoom_out_btn.setToolTip("Zoom out (Ctrl+-)")
        zoom_layout.addWidget(self.zoom_out_btn)
        
        self.zoom_label = QLabel("Fit")
        self.zoom_label.setFixedWidth(35)
        self.zoom_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.zoom_label.setStyleSheet("color: #888; font-size: 10px;")
        zoom_layout.addWidget(self.zoom_label)
        
        self.zoom_in_btn = QPushButton("+")
        self.zoom_in_btn.setFixedSize(28, 24)
        self.zoom_in_btn.clicked.connect(self.zoom_in)
        self.zoom_in_btn.setToolTip("Zoom in (Ctrl++)")
        zoom_layout.addWidget(self.zoom_in_btn)
        
        self.zoom_reset_btn = QPushButton("⊙")
        self.zoom_reset_btn.setFixedSize(28, 24)
        self.zoom_reset_btn.clicked.connect(self.zoom_reset)
        self.zoom_reset_btn.setToolTip("Reset zoom (Ctrl+0)")
        zoom_layout.addWidget(self.zoom_reset_btn)
        
        zoom_layout.addStretch()
        
        layout.addLayout(zoom_layout)
        
        # Initial state
        self._update_nav_state()
        self._show_placeholder()
    
    def _setup_shortcuts(self):
        """Set up keyboard shortcuts for navigation."""
        # Left arrow for previous
        self.shortcut_prev = QShortcut(QKeySequence(Qt.Key.Key_Left), self)
        self.shortcut_prev.activated.connect(self.show_previous)
        
        # Right arrow for next
        self.shortcut_next = QShortcut(QKeySequence(Qt.Key.Key_Right), self)
        self.shortcut_next.activated.connect(self.show_next)
        
        # Zoom shortcuts
        self.shortcut_zoom_in = QShortcut(QKeySequence("Ctrl+="), self)
        self.shortcut_zoom_in.activated.connect(self.zoom_in)
        
        self.shortcut_zoom_out = QShortcut(QKeySequence("Ctrl+-"), self)
        self.shortcut_zoom_out.activated.connect(self.zoom_out)
        
        self.shortcut_zoom_reset = QShortcut(QKeySequence("Ctrl+0"), self)
        self.shortcut_zoom_reset.activated.connect(self.zoom_reset)
    
    def zoom_in(self):
        """Zoom in on the current image."""
        if self.current_pixmap:
            self.zoom_level = min(self.zoom_level * 1.25, 5.0)
            self._apply_zoom()
    
    def zoom_out(self):
        """Zoom out on the current image."""
        if self.current_pixmap:
            self.zoom_level = max(self.zoom_level / 1.25, 0.25)
            self._apply_zoom()
    
    def zoom_reset(self):
        """Reset zoom to fit."""
        self.zoom_level = 1.0
        if self.current_pixmap:
            self._apply_zoom()
    
    def _apply_zoom(self):
        """Apply current zoom level to the image."""
        if not self.current_pixmap:
            return
        
        if self.zoom_level == 1.0:
            # Fit to panel
            scaled = self.current_pixmap.scaled(
                self.image_scroll.size() - QSize(20, 20),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.zoom_label.setText("Fit")
        else:
            # Apply zoom factor to original size
            new_size = self.current_pixmap.size() * self.zoom_level
            scaled = self.current_pixmap.scaled(
                new_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.zoom_label.setText(f"{int(self.zoom_level * 100)}%")
        
        self.image_label.setPixmap(scaled)
        self.image_label.adjustSize()
    
    def set_state(self, state_code: Optional[str]):
        """Set the current state and load its images."""
        self.current_state = state_code
        self.current_index = 0
        
        if state_code:
            self.title_label.setText(f"Plate Images - {state_code}")
            self._load_images()
        else:
            self.title_label.setText("Plate Images")
            self.current_images = []
            self._show_placeholder()
        
        self._update_nav_state()
    
    def _get_image_search_dirs(self) -> list[Path]:
        """
        Get list of directories to search for images.
        
        Priority order:
        1. data/images/Plates/{State Name}/ (e.g., data/images/Plates/Florida/)
        2. data/images/{STATE_CODE}/ (e.g., data/images/FL/)
        3. data/images/{STATE_CODE}/plates/ subdirectory if exists
        """
        search_dirs = []
        
        if not self.current_state:
            return search_dirs
        
        # Priority 1: Check Plates directory with full state name
        state_folder_name = self.STATE_FOLDER_MAP.get(self.current_state.upper())
        if state_folder_name:
            plates_state_dir = self.images_path / "Plates" / state_folder_name
            if plates_state_dir.exists():
                search_dirs.append(plates_state_dir)
        
        # Priority 2: Check state code directory
        state_code_dir = self.images_path / self.current_state
        if state_code_dir.exists():
            search_dirs.append(state_code_dir)
            
            # Also check plates subdirectory
            plates_subdir = state_code_dir / "plates"
            if plates_subdir.exists():
                search_dirs.append(plates_subdir)
        
        return search_dirs
    
    def _load_images(self):
        """Load images for the current state and category."""
        if not self.current_state:
            self.current_images = []
            return
        
        # Get all directories to search for images
        search_dirs = self._get_image_search_dirs()
        
        if not search_dirs:
            self.current_images = []
            self._show_no_images()
            return
        
        # Get all image files from all search directories
        all_images = []
        image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp'}
        seen_names = set()  # Avoid duplicates if same image in multiple dirs
        
        for search_dir in search_dirs:
            if not search_dir.exists():
                continue
            for file in search_dir.iterdir():
                if file.is_file() and file.suffix.lower() in image_extensions:
                    # Use filename as key to avoid duplicates
                    if file.name.lower() not in seen_names:
                        all_images.append(file)
                        seen_names.add(file.name.lower())
        
        # Filter by category if needed
        category = self.current_category
        if category == "all":
            # Apply smart sorting by plate type and image type priority
            self.current_images = self._sort_images_by_priority(all_images)
        elif category == "standard":
            # Standard plates typically have state code in name or "standard"
            filtered = [
                f for f in all_images 
                if 'standard' in f.name.lower() or 
                   f.name.lower().startswith(self.current_state.lower()) or
                   f.name.lower().startswith('plate')
            ]
            self.current_images = self._sort_images_by_priority(filtered)
        elif category == "specialty":
            # Specialty plates - exclude standard patterns
            filtered = [
                f for f in all_images 
                if not f.name.lower().startswith(self.current_state.lower()) and
                   'standard' not in f.name.lower() and
                   not f.name.lower().startswith('plate') and
                   'gov' not in f.name.lower() and
                   'police' not in f.name.lower() and
                   'fire' not in f.name.lower() and
                   'exempt' not in f.name.lower()
            ]
            self.current_images = self._sort_images_by_priority(filtered)
        elif category == "government":
            # Government/official plates
            filtered = [
                f for f in all_images 
                if any(kw in f.name.lower() for kw in [
                    'gov', 'police', 'fire', 'exempt', 'state', 'city', 
                    'county', 'sheriff', 'highway patrol', 'marshal'
                ])
            ]
            self.current_images = self._sort_images_by_priority(filtered)
        elif category == "characters":
            # Character reference images - search in all directories
            char_images = []
            seen_names = set()
            for search_dir in search_dirs:
                chars_path = search_dir / "characters"
                if chars_path.exists():
                    for f in chars_path.iterdir():
                        if f.is_file() and f.suffix.lower() in image_extensions:
                            if f.name.lower() not in seen_names:
                                char_images.append(f)
                                seen_names.add(f.name.lower())
            self.current_images = sorted(char_images, key=lambda p: p.name.lower())
        
        # Reset to first image
        self.current_index = 0
        
        if self.current_images:
            self._show_current_image()
        else:
            self._show_no_images()
        
        self._update_nav_state()
    
    def _sort_images_by_priority(self, images: list[Path]) -> list[Path]:
        """
        Sort images by plate type priority, then image type priority, then alphabetically.
        
        Priority order:
        1. Generic/sample plates (priority 0)
        2. Apportioned/Commercial/Truck/Trailer (priority 1)
        3. Passenger/Standard (priority 2)
        4. Motorcycle (priority 3)
        5. Government (priority 4)
        6. Dealer (priority 5)
        7. Specialty (priority 6)
        8. Vanity (priority 7)
        """
        return sorted(images, key=lambda p: self._get_image_sort_key(p))
    
    def _get_image_sort_key(self, image_path: Path) -> Tuple[int, int, str]:
        """
        Get a sort key for an image based on its filename.
        
        Returns a tuple of (plate_type_priority, image_type_priority, filename)
        """
        filename = image_path.stem.lower()
        
        # Determine plate type category
        plate_type_priority = self._detect_plate_type_priority(filename)
        
        # Determine image type priority
        image_type_priority = self._detect_image_type_priority(filename)
        
        return (plate_type_priority, image_type_priority, filename)
    
    def _detect_plate_type_priority(self, filename: str) -> int:
        """Detect the plate type category from filename and return its priority."""
        # Check for specific types (order matters - more specific first)
        if 'semi-trailer' in filename or 'semitrailer' in filename:
            return self.PLATE_TYPE_PRIORITY.get('semi-trailer', 99)
        elif 'semi' in filename:
            return self.PLATE_TYPE_PRIORITY.get('semi', 99)
        elif 'trailer' in filename:
            return self.PLATE_TYPE_PRIORITY.get('trailer', 99)
        elif 'truck' in filename:
            return self.PLATE_TYPE_PRIORITY.get('truck', 99)
        elif 'commercial' in filename:
            return self.PLATE_TYPE_PRIORITY.get('commercial', 99)
        elif 'apportioned' in filename or 'irp' in filename:
            return self.PLATE_TYPE_PRIORITY.get('apportioned', 99)
        elif 'vanity' in filename or 'personalized' in filename:
            return self.PLATE_TYPE_PRIORITY.get('vanity', 99)
        elif 'specialty' in filename or 'special' in filename:
            return self.PLATE_TYPE_PRIORITY.get('specialty', 99)
        elif 'dealer' in filename:
            return self.PLATE_TYPE_PRIORITY.get('dealer', 99)
        elif any(kw in filename for kw in ['government', 'govt', 'gov', 'police', 'fire', 'exempt', 'official']):
            return self.PLATE_TYPE_PRIORITY.get('government', 99)
        elif 'motorcycle' in filename or filename.startswith('mc'):
            return self.PLATE_TYPE_PRIORITY.get('motorcycle', 99)
        elif 'passenger' in filename or 'standard' in filename:
            return self.PLATE_TYPE_PRIORITY.get('passenger', 99)
        # Generic plate_sample with no specific type
        elif 'plate' in filename and ('sample' in filename or 'blank' in filename or 'template' in filename):
            return self.PLATE_TYPE_PRIORITY.get('generic', 99)
        else:
            # Default to passenger priority for unrecognized
            return self.PLATE_TYPE_PRIORITY.get('passenger', 99)
    
    def _detect_image_type_priority(self, filename: str) -> int:
        """Detect the image type from filename and return its priority."""
        if 'blank' in filename or 'template' in filename:
            return self.IMAGE_TYPE_PRIORITY.get('blank', 99)
        elif 'font' in filename:
            return self.IMAGE_TYPE_PRIORITY.get('font', 99)
        elif 'variation' in filename or 'variant' in filename:
            return self.IMAGE_TYPE_PRIORITY.get('variation', 99)
        else:
            # Default to sample
            return self.IMAGE_TYPE_PRIORITY.get('sample', 99)
    
    def _show_current_image(self):
        """Display the current image."""
        if not self.current_images or self.current_index >= len(self.current_images):
            self._show_placeholder()
            return
        
        image_path = self.current_images[self.current_index]
        pixmap = QPixmap(str(image_path))
        
        if pixmap.isNull():
            self.current_pixmap = None
            self.image_label.setText(f"Failed to load:\n{image_path.name}")
            self.image_label.setStyleSheet("color: #ff6b6b;")
        else:
            # Store original pixmap for zoom
            self.current_pixmap = pixmap
            self.zoom_level = 1.0  # Reset zoom when changing images
            self._apply_zoom()
            self.image_label.setStyleSheet("")
        
        # Update name label
        self.image_name_label.setText(image_path.stem)
        
        # Emit signal
        self.image_changed.emit(str(image_path))
    
    def _show_placeholder(self):
        """Show placeholder when no state is selected."""
        self.image_label.clear()
        self.image_label.setText("Select a state to view plate images")
        self.image_label.setStyleSheet("color: #707070; font-size: 12px;")
        self.image_name_label.setText("")
        self.counter_label.setText("0 / 0")
    
    def _show_no_images(self):
        """Show message when no images are available."""
        self.image_label.clear()
        if self.current_category == "all":
            self.image_label.setText(f"No images available for {self.current_state}")
        else:
            self.image_label.setText(f"No {self.current_category} images for {self.current_state}")
        self.image_label.setStyleSheet("color: #707070; font-size: 12px;")
        self.image_name_label.setText("")
    
    def _update_nav_state(self):
        """Update navigation button states and counter."""
        count = len(self.current_images)
        has_images = count > 0
        
        self.prev_btn.setEnabled(has_images and self.current_index > 0)
        self.next_btn.setEnabled(has_images and self.current_index < count - 1)
        
        if has_images:
            self.counter_label.setText(f"{self.current_index + 1} / {count}")
        else:
            self.counter_label.setText("0 / 0")
    
    def show_previous(self):
        """Show the previous image."""
        if self.current_images and self.current_index > 0:
            self.current_index -= 1
            self._show_current_image()
            self._update_nav_state()
    
    def show_next(self):
        """Show the next image."""
        if self.current_images and self.current_index < len(self.current_images) - 1:
            self.current_index += 1
            self._show_current_image()
            self._update_nav_state()
    
    def _on_category_changed(self, index: int):
        """Handle category filter change."""
        self.current_category = self.category_combo.currentData()
        self._load_images()
    
    def show_plate_type(self, plate_type_name: str) -> bool:
        """
        Try to find and display an image matching the plate type name.
        
        Args:
            plate_type_name: Name of the plate type to find (e.g., "Amateur Radio")
            
        Returns:
            True if a matching image was found, False otherwise
        """
        if not self.current_state or not plate_type_name:
            return False
        
        # Ensure we're showing all images so we can search through them
        if self.current_category != "all":
            self.category_combo.setCurrentIndex(0)  # "All Images"
            self._load_images()
        
        if not self.current_images:
            return False
        
        # Normalize the plate type name for matching
        search_terms = plate_type_name.lower().replace('-', ' ').replace('_', ' ').split()
        
        # Try to find a matching image
        best_match_idx = -1
        best_match_score = 0
        
        for idx, img_path in enumerate(self.current_images):
            img_name = img_path.stem.lower().replace('-', ' ').replace('_', ' ')
            
            # Count how many search terms match
            score = sum(1 for term in search_terms if term in img_name)
            
            # Exact match gets bonus
            if plate_type_name.lower() == img_path.stem.lower():
                score += 100
            
            # Partial exact match (contains full plate type name)
            if plate_type_name.lower().replace(' ', '-') in img_path.stem.lower():
                score += 50
            if plate_type_name.lower().replace(' ', '_') in img_path.stem.lower():
                score += 50
            if plate_type_name.lower().replace(' ', '') in img_path.stem.lower().replace(' ', ''):
                score += 25
            
            if score > best_match_score:
                best_match_score = score
                best_match_idx = idx
        
        if best_match_idx >= 0 and best_match_score > 0:
            self.current_index = best_match_idx
            self._show_current_image()
            self._update_nav_state()
            return True
        
        return False
    
    def resizeEvent(self, event):
        """Handle resize to re-scale the image."""
        super().resizeEvent(event)
        if self.current_pixmap and self.zoom_level == 1.0:
            # Only re-fit if we're in "fit" mode
            self._apply_zoom()
