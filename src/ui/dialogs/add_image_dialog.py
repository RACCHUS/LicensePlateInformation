"""
Add Image Dialog for user-submitted license plate images.

Provides an interface for users to add their own license plate images
with optional metadata including plate type, description, and character
rule information.
"""

from pathlib import Path
from typing import Optional, List

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, 
    QPushButton, QComboBox, QLineEdit, QTextEdit, QCheckBox,
    QFileDialog, QMessageBox, QFrame, QScrollArea, QWidget,
    QSizePolicy, QGroupBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QDragEnterEvent, QDropEvent, QFont

# Handle both relative and absolute imports for bundled exe compatibility
try:
    from ...utils.user_image_manager import UserImageManager
except ImportError:
    from utils.user_image_manager import UserImageManager


class TagWidget(QWidget):
    """Widget for displaying removable tags/chips."""
    
    tag_removed = Signal(str)
    
    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        self.text = text
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 2, 2, 2)
        layout.setSpacing(4)
        
        label = QLabel(self.text)
        label.setStyleSheet("color: #e0e0e0; font-size: 11px;")
        layout.addWidget(label)
        
        remove_btn = QPushButton("×")
        remove_btn.setFixedSize(16, 16)
        remove_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #888;
                border: none;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #ff6b6b;
            }
        """)
        remove_btn.clicked.connect(self._on_remove)
        layout.addWidget(remove_btn)
        
        self.setStyleSheet("""
            QWidget {
                background-color: #3c5c3c;
                border-radius: 10px;
            }
        """)
        self.setFixedHeight(24)
    
    def _on_remove(self):
        self.tag_removed.emit(self.text)
        self.deleteLater()


class TagContainer(QWidget):
    """Container for multiple tag widgets with add functionality."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tags: List[str] = []
        self._setup_ui()
    
    def _setup_ui(self):
        self._container_layout = QHBoxLayout(self)
        self._container_layout.setContentsMargins(0, 0, 0, 0)
        self._container_layout.setSpacing(4)
        self._container_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # Add button
        self.add_btn = QPushButton("+ Add")
        self.add_btn.setFixedHeight(24)
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #3c3c3c;
                color: #4CAF50;
                border: 1px dashed #4CAF50;
                border-radius: 10px;
                padding: 2px 8px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
            }
        """)
        self.add_btn.clicked.connect(self._on_add_clicked)
        self._container_layout.addWidget(self.add_btn)
        
        self._container_layout.addStretch()
    
    def _on_add_clicked(self):
        """Show input for adding a new tag."""
        # Simple approach: use input dialog
        from PySide6.QtWidgets import QInputDialog
        text, ok = QInputDialog.getText(
            self, "Add Character",
            "Enter character(s) (e.g., DV, EX, CO):"
        )
        if ok and text.strip():
            self.add_tag(text.strip().upper())
    
    def add_tag(self, text: str):
        """Add a tag to the container."""
        if text in self.tags:
            return
        
        self.tags.append(text)
        
        # Insert tag widget before add button
        tag_widget = TagWidget(text)
        tag_widget.tag_removed.connect(self._on_tag_removed)
        self._container_layout.insertWidget(self._container_layout.count() - 2, tag_widget)
    
    def _on_tag_removed(self, text: str):
        """Handle tag removal."""
        if text in self.tags:
            self.tags.remove(text)
    
    def get_tags(self) -> List[str]:
        """Get all current tags."""
        return self.tags.copy()
    
    def clear(self):
        """Remove all tags."""
        while self.tags:
            self.tags.pop()
        # Remove all tag widgets
        for i in reversed(range(self._container_layout.count())):
            item = self._container_layout.itemAt(i)
            if item:
                widget = item.widget()
                if widget and isinstance(widget, TagWidget):
                    widget.deleteLater()


class DropArea(QLabel):
    """Drag and drop area for images."""
    
    file_dropped = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumSize(300, 200)
        self._set_default_state()
    
    def _set_default_state(self):
        """Set the default appearance."""
        self.setText(
            "🖼️ Drag & Drop Image Here\n\n"
            "or click Browse below"
        )
        self.setStyleSheet("""
            QLabel {
                background-color: #1e1e1e;
                border: 2px dashed #4a4a4a;
                border-radius: 8px;
                color: #888;
                font-size: 14px;
            }
        """)
    
    def set_preview(self, pixmap: QPixmap):
        """Set a preview image."""
        scaled = pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.setPixmap(scaled)
        self.setStyleSheet("""
            QLabel {
                background-color: #1e1e1e;
                border: 2px solid #4CAF50;
                border-radius: 8px;
            }
        """)
    
    def clear_preview(self):
        """Clear the preview and reset to default state."""
        self.clear()
        self._set_default_state()
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter."""
        if event.mimeData().hasUrls():
            # Check if any URL is an image
            for url in event.mimeData().urls():
                if url.toLocalFile().lower().endswith(
                    ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp')
                ):
                    event.acceptProposedAction()
                    self.setStyleSheet("""
                        QLabel {
                            background-color: #2a3a2a;
                            border: 2px dashed #4CAF50;
                            border-radius: 8px;
                            color: #4CAF50;
                        }
                    """)
                    return
        event.ignore()
    
    def dragLeaveEvent(self, event):
        """Handle drag leave."""
        if not self.pixmap():
            self._set_default_state()
    
    def dropEvent(self, event: QDropEvent):
        """Handle drop."""
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith(
                ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp')
            ):
                self.file_dropped.emit(file_path)
                event.acceptProposedAction()
                return
        event.ignore()


class AddImageDialog(QDialog):
    """
    Dialog for adding user-submitted license plate images.
    
    Allows users to:
    - Select/drag-drop an image
    - Choose a state (required)
    - Add optional metadata (plate type, description, etc.)
    - Mark as character rule example with excluded characters
    """
    
    image_added = Signal(str, str)  # state_code, filename
    
    def __init__(
        self, 
        data_path: Path,
        state_codes: List[str],
        current_state: Optional[str] = None,
        parent=None
    ):
        super().__init__(parent)
        
        self.data_path = data_path
        self.state_codes = sorted(state_codes)
        self.current_state = current_state
        self.selected_file: Optional[str] = None
        self.plate_types: List[str] = []
        
        self.user_image_manager = UserImageManager(data_path)
        
        self.setWindowTitle("Add License Plate Image")
        self.setMinimumSize(500, 600)
        self.resize(550, 700)
        
        self._setup_ui()
        self._apply_styles()
        self._connect_signals()
        
        # Pre-select current state if provided
        if current_state:
            idx = self.state_combo.findData(current_state)
            if idx >= 0:
                self.state_combo.setCurrentIndex(idx)
    
    def _setup_ui(self):
        """Set up the dialog UI."""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Scroll area so all fields (include/omit) stay reachable on smaller screens
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(12)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header = QLabel("📷 <b>Add License Plate Image</b>")
        header.setTextFormat(Qt.TextFormat.RichText)
        header.setStyleSheet("font-size: 16px; color: #4CAF50;")
        layout.addWidget(header)
        
        # Drop area for image
        self.drop_area = DropArea()
        layout.addWidget(self.drop_area)
        
        # Browse button
        browse_layout = QHBoxLayout()
        browse_layout.addStretch()
        self.browse_btn = QPushButton("📁 Browse...")
        self.browse_btn.clicked.connect(self._on_browse)
        browse_layout.addWidget(self.browse_btn)
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self._on_clear_image)
        self.clear_btn.setEnabled(False)
        browse_layout.addWidget(self.clear_btn)
        browse_layout.addStretch()
        layout.addLayout(browse_layout)
        
        # File info label
        self.file_label = QLabel("")
        self.file_label.setStyleSheet("color: #888; font-size: 11px;")
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.file_label)
        
        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background-color: #404040;")
        layout.addWidget(sep)
        
        # State selection (required)
        state_layout = QHBoxLayout()
        state_label = QLabel("State*:")
        state_label.setStyleSheet("font-weight: bold;")
        state_layout.addWidget(state_label)
        
        self.state_combo = QComboBox()
        self.state_combo.addItem("-- Select State --", None)
        for code in self.state_codes:
            self.state_combo.addItem(code, code)
        self.state_combo.setMinimumWidth(100)
        state_layout.addWidget(self.state_combo)
        state_layout.addStretch()
        layout.addLayout(state_layout)
        
        # Optional fields group
        optional_group = QGroupBox("Optional Information")
        optional_layout = QVBoxLayout(optional_group)
        optional_layout.setSpacing(10)
        
        # Plate type dropdown
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Plate Type:"))
        self.plate_type_combo = QComboBox()
        self.plate_type_combo.addItem("-- None --", None)
        self.plate_type_combo.setMinimumWidth(200)
        self.plate_type_combo.setEnabled(False)
        type_layout.addWidget(self.plate_type_combo, 1)
        optional_layout.addLayout(type_layout)
        
        # Description
        desc_layout = QHBoxLayout()
        desc_layout.addWidget(QLabel("Description:"))
        self.description_edit = QLineEdit()
        self.description_edit.setPlaceholderText("Brief description (optional)")
        desc_layout.addWidget(self.description_edit, 1)
        optional_layout.addLayout(desc_layout)
        
        # Character rule checkboxes
        self.omit_check = QCheckBox("Omit example (do NOT allow these)")
        self.omit_check.setToolTip(
            "Omit example: marks characters that should never appear (e.g., disallowed stacked blocks)."
        )
        optional_layout.addWidget(self.omit_check)

        self.include_check = QCheckBox("Include example (explicitly allow these)")
        self.include_check.setToolTip(
            "Include example: marks characters that are explicitly allowed/expected."
        )
        optional_layout.addWidget(self.include_check)

        # Omit characters container (shown when omit checkbox is checked)
        self.omit_container = QWidget()
        omit_layout = QVBoxLayout(self.omit_container)
        omit_layout.setContentsMargins(20, 0, 0, 0)
        omit_layout.setSpacing(4)

        omit_label = QLabel("Omit Characters (do not allow):")
        omit_label.setStyleSheet("color: #888; font-size: 11px;")
        omit_label.setToolTip(
            "Add characters that must be omitted (not allowed)."
        )
        omit_layout.addWidget(omit_label)

        omit_hint = QLabel(
            "Tip: These characters are NOT allowed. If you also have characters to allow, use the Include section below."
        )
        omit_hint.setStyleSheet("color: #666; font-size: 10px;")
        omit_layout.addWidget(omit_hint)

        self.omit_tags = TagContainer()
        omit_layout.addWidget(self.omit_tags)

        # Quick add common omits
        quick_omit_layout = QHBoxLayout()
        quick_omit_layout.setSpacing(4)
        for char in ["DV", "EX", "CO", "CY", "HC", "ST"]:
            btn = QPushButton(char)
            btn.setFixedSize(36, 22)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2d2d2d;
                    color: #888;
                    border: 1px solid #3c3c3c;
                    border-radius: 4px;
                    font-size: 10px;
                }
                QPushButton:hover {
                    background-color: #3c3c3c;
                    color: #e0e0e0;
                }
            """)
            btn.setToolTip(f"Add {char} to the OMIT list (do not allow)")
            btn.clicked.connect(lambda checked, c=char: self.omit_tags.add_tag(c))
            quick_omit_layout.addWidget(btn)
        quick_omit_layout.addStretch()
        omit_layout.addLayout(quick_omit_layout)
        
        self.omit_container.setVisible(False)
        optional_layout.addWidget(self.omit_container)

        # Include characters container (shown when include checkbox is checked)
        self.include_container = QWidget()
        include_layout = QVBoxLayout(self.include_container)
        include_layout.setContentsMargins(20, 0, 0, 0)
        include_layout.setSpacing(4)

        include_label = QLabel("Include Characters (explicitly allow):")
        include_label.setStyleSheet("color: #888; font-size: 11px;")
        include_label.setToolTip(
            "Add characters that are explicitly allowed/expected (include list)."
        )
        include_layout.addWidget(include_label)

        include_hint = QLabel(
            "Tip: These characters ARE allowed/expected. Use this when you need a clear include list."
        )
        include_hint.setStyleSheet("color: #666; font-size: 10px;")
        include_layout.addWidget(include_hint)

        self.include_tags = TagContainer()
        include_layout.addWidget(self.include_tags)

        # Quick add common includes (same shortcuts for convenience)
        quick_include_layout = QHBoxLayout()
        quick_include_layout.setSpacing(4)
        for char in ["DV", "EX", "CO", "CY", "HC", "ST"]:
            btn = QPushButton(char)
            btn.setFixedSize(36, 22)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2d2d2d;
                    color: #888;
                    border: 1px solid #3c3c3c;
                    border-radius: 4px;
                    font-size: 10px;
                }
                QPushButton:hover {
                    background-color: #3c3c3c;
                    color: #e0e0e0;
                }
            """)
            btn.setToolTip(f"Add {char} to the INCLUDE list (explicitly allow)")
            btn.clicked.connect(lambda checked, c=char: self.include_tags.add_tag(c))
            quick_include_layout.addWidget(btn)
        quick_include_layout.addStretch()
        include_layout.addLayout(quick_include_layout)

        self.include_container.setVisible(False)
        optional_layout.addWidget(self.include_container)
        
        # Notes
        notes_label = QLabel("Notes:")
        optional_layout.addWidget(notes_label)
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Additional notes (optional)")
        self.notes_edit.setMaximumHeight(80)
        optional_layout.addWidget(self.notes_edit)
        
        layout.addWidget(optional_group)

        layout.addStretch()

        scroll.setWidget(content)
        main_layout.addWidget(scroll, 1)

        # Buttons stay anchored at bottom
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_btn)
        
        self.add_btn = QPushButton("Add Image")
        self.add_btn.setEnabled(False)
        self.add_btn.clicked.connect(self._on_add_image)
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5CBF60;
            }
            QPushButton:disabled {
                background-color: #3c3c3c;
                color: #666;
            }
        """)
        btn_layout.addWidget(self.add_btn)
        
        main_layout.addLayout(btn_layout)
    
    def _apply_styles(self):
        """Apply dark theme styling."""
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
                color: #e0e0e0;
            }
            QLabel {
                color: #e0e0e0;
            }
            QGroupBox {
                color: #e0e0e0;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                margin-top: 8px;
                padding-top: 8px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QComboBox {
                background-color: #3c3c3c;
                color: #e0e0e0;
                border: 1px solid #4a4a4a;
                border-radius: 4px;
                padding: 4px 8px;
            }
            QComboBox:hover {
                border-color: #5a5a5a;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #3c3c3c;
                color: #e0e0e0;
                selection-background-color: #4CAF50;
            }
            QLineEdit, QTextEdit {
                background-color: #1e1e1e;
                color: #e0e0e0;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                padding: 4px;
            }
            QLineEdit:focus, QTextEdit:focus {
                border-color: #4CAF50;
            }
            QCheckBox {
                color: #e0e0e0;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            QPushButton {
                background-color: #3c3c3c;
                color: #e0e0e0;
                border: 1px solid #4a4a4a;
                border-radius: 4px;
                padding: 6px 16px;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
            }
        """)
    
    def _connect_signals(self):
        """Connect widget signals."""
        self.drop_area.file_dropped.connect(self._on_file_selected)
        self.state_combo.currentIndexChanged.connect(self._on_state_changed)
        self.omit_check.toggled.connect(self._on_omit_toggled)
        self.include_check.toggled.connect(self._on_include_toggled)
    
    def _on_browse(self):
        """Open file browser."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select License Plate Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif *.webp);;All Files (*)"
        )
        if file_path:
            self._on_file_selected(file_path)
    
    def _on_file_selected(self, file_path: str):
        """Handle file selection."""
        self.selected_file = file_path
        
        # Show preview
        pixmap = QPixmap(file_path)
        if not pixmap.isNull():
            self.drop_area.set_preview(pixmap)
            
            # Show file info
            path = Path(file_path)
            size_kb = path.stat().st_size / 1024
            self.file_label.setText(f"{path.name} ({size_kb:.1f} KB)")
            self.clear_btn.setEnabled(True)
        
        self._update_add_button()
    
    def _on_clear_image(self):
        """Clear selected image."""
        self.selected_file = None
        self.drop_area.clear_preview()
        self.file_label.setText("")
        self.clear_btn.setEnabled(False)
        self._update_add_button()
    
    def _on_state_changed(self, index: int):
        """Handle state selection change."""
        state_code = self.state_combo.currentData()
        
        # Load plate types for selected state
        self.plate_type_combo.clear()
        self.plate_type_combo.addItem("-- None --", None)
        
        if state_code:
            self.plate_type_combo.setEnabled(True)
            plate_types = self._load_plate_types(state_code)
            for pt in plate_types:
                self.plate_type_combo.addItem(pt, pt)
        else:
            self.plate_type_combo.setEnabled(False)
        
        self._update_add_button()
    
    def _load_plate_types(self, state_code: str) -> List[str]:
        """Load plate types for a state from JSON file."""
        import json
        
        # Try to load from state JSON file
        state_file = self.data_path / 'states' / f'{state_code.lower()}.json'
        
        if not state_file.exists():
            # Try alternate naming
            for f in (self.data_path / 'states').iterdir():
                if f.suffix == '.json':
                    try:
                        with open(f, 'r', encoding='utf-8') as file:
                            data = json.load(file)
                            if data.get('abbreviation', '').upper() == state_code.upper():
                                state_file = f
                                break
                    except:
                        continue
        
        plate_types = set()
        
        if state_file.exists():
            try:
                with open(state_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # Extract plate types from various possible locations
                    if 'plate_types' in data:
                        for pt in data['plate_types']:
                            if isinstance(pt, dict):
                                name = pt.get('type_name') or pt.get('name', '')
                                if name:
                                    plate_types.add(name)
                            elif isinstance(pt, str):
                                plate_types.add(pt)
            except Exception as e:
                print(f"Error loading plate types: {e}")
        
        # Add common defaults if none found
        if not plate_types:
            plate_types = {
                'Passenger', 'Commercial', 'Motorcycle', 'Trailer',
                'Temporary', 'Dealer', 'Government', 'Specialty'
            }
        
        return sorted(plate_types)
    
    def _on_omit_toggled(self, checked: bool):
        """Show/hide omit characters section."""
        self.omit_container.setVisible(checked)
        self._update_add_button()

    def _on_include_toggled(self, checked: bool):
        """Show/hide include characters section."""
        self.include_container.setVisible(checked)
        self._update_add_button()
    
    def _update_add_button(self):
        """Update add button enabled state."""
        has_file = self.selected_file is not None
        has_state = self.state_combo.currentData() is not None
        self.add_btn.setEnabled(has_file and has_state)
    
    def _on_add_image(self):
        """Handle add image button click."""
        if not self.selected_file:
            QMessageBox.warning(self, "No Image", "Please select an image file.")
            return
        
        state_code = self.state_combo.currentData()
        if not state_code:
            QMessageBox.warning(self, "No State", "Please select a state.")
            return
        
        # Gather optional metadata
        plate_type = self.plate_type_combo.currentData()
        description = self.description_edit.text().strip() or None
        is_char_example = self.omit_check.isChecked() or self.include_check.isChecked()
        excluded_chars = self.omit_tags.get_tags() if self.omit_check.isChecked() else None
        included_chars = self.include_tags.get_tags() if self.include_check.isChecked() else None
        notes = self.notes_edit.toPlainText().strip() or None
        
        # Save the image
        user_image = self.user_image_manager.save_image(
            source_path=self.selected_file,
            state_code=state_code,
            plate_type=plate_type,
            description=description,
            is_character_example=is_char_example,
            excluded_characters=excluded_chars,
            included_characters=included_chars,
            notes=notes
        )
        
        if user_image:
            QMessageBox.information(
                self,
                "Image Added",
                f"Image added successfully for {state_code}!\n\n"
                f"Filename: {user_image.filename}"
            )
            self.image_added.emit(state_code, user_image.filename)
            self.accept()
        else:
            QMessageBox.critical(
                self,
                "Error",
                "Failed to add image. Please check the file and try again."
            )
