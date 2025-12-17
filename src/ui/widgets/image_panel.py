"""
Image Panel Widget for License Plate Information System.

Displays plate images for the selected state with navigation controls.
"""

from pathlib import Path
from typing import Optional

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
    """
    
    # Signal emitted when image changes
    image_changed = Signal(str)  # image_path
    
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
    
    def _load_images(self):
        """Load images for the current state and category."""
        if not self.current_state:
            self.current_images = []
            return
        
        state_path = self.images_path / self.current_state
        if not state_path.exists():
            self.current_images = []
            self._show_no_images()
            return
        
        # Get all image files
        all_images = []
        image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp'}
        
        for file in state_path.iterdir():
            if file.is_file() and file.suffix.lower() in image_extensions:
                all_images.append(file)
        
        # Filter by category if needed
        category = self.current_category
        if category == "all":
            self.current_images = sorted(all_images, key=lambda p: p.name.lower())
        elif category == "standard":
            # Standard plates typically have state code in name or "standard"
            self.current_images = sorted([
                f for f in all_images 
                if 'standard' in f.name.lower() or 
                   f.name.lower().startswith(self.current_state.lower()) or
                   f.name.lower().startswith('plate')
            ], key=lambda p: p.name.lower())
        elif category == "specialty":
            # Specialty plates - exclude standard patterns
            self.current_images = sorted([
                f for f in all_images 
                if not f.name.lower().startswith(self.current_state.lower()) and
                   'standard' not in f.name.lower() and
                   not f.name.lower().startswith('plate') and
                   'gov' not in f.name.lower() and
                   'police' not in f.name.lower() and
                   'fire' not in f.name.lower() and
                   'exempt' not in f.name.lower()
            ], key=lambda p: p.name.lower())
        elif category == "government":
            # Government/official plates
            self.current_images = sorted([
                f for f in all_images 
                if any(kw in f.name.lower() for kw in [
                    'gov', 'police', 'fire', 'exempt', 'state', 'city', 
                    'county', 'sheriff', 'highway patrol', 'marshal'
                ])
            ], key=lambda p: p.name.lower())
        elif category == "characters":
            # Character reference images
            chars_path = state_path / "characters"
            if chars_path.exists():
                self.current_images = sorted([
                    f for f in chars_path.iterdir()
                    if f.is_file() and f.suffix.lower() in image_extensions
                ], key=lambda p: p.name.lower())
            else:
                self.current_images = []
        
        # Reset to first image
        self.current_index = 0
        
        if self.current_images:
            self._show_current_image()
        else:
            self._show_no_images()
        
        self._update_nav_state()
    
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
