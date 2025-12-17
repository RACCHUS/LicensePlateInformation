"""
Notes dialog for user feedback and missing information.

Provides a simple interface for users to record notes about
missing information, corrections, or suggestions that can be
sent to the developer.
"""

from pathlib import Path
from datetime import datetime
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTextEdit, 
    QPushButton, QLabel, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class NotesDialog(QDialog):
    """Dialog for editing user notes."""
    
    def __init__(self, data_path: Path, parent=None):
        super().__init__(parent)
        self.data_path = data_path
        self.notes_file = data_path / "user_notes.txt"
        
        self.setWindowTitle("User Notes - Missing Information & Feedback")
        self.setMinimumSize(600, 500)
        self.resize(700, 550)
        
        self._setup_ui()
        self._load_notes()
        self._apply_styles()
    
    def _setup_ui(self):
        """Set up the dialog UI."""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Header with instructions
        header = QLabel(
            "📝 <b>User Notes</b><br>"
            "<span style='color: #888; font-size: 11px;'>"
            "Record any missing information, corrections, or suggestions here.<br>"
            "This file can be sent to the developer for app updates."
            "</span>"
        )
        header.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(header)
        
        # Quick add section
        quick_layout = QHBoxLayout()
        quick_layout.setSpacing(5)
        
        self.quick_state_btn = QPushButton("+ State Issue")
        self.quick_state_btn.setToolTip("Add a template for reporting a state-related issue")
        self.quick_state_btn.clicked.connect(self._add_state_template)
        quick_layout.addWidget(self.quick_state_btn)
        
        self.quick_plate_btn = QPushButton("+ Plate Type Issue")
        self.quick_plate_btn.setToolTip("Add a template for reporting a plate type issue")
        self.quick_plate_btn.clicked.connect(self._add_plate_template)
        quick_layout.addWidget(self.quick_plate_btn)
        
        self.quick_general_btn = QPushButton("+ General Note")
        self.quick_general_btn.setToolTip("Add a general note entry")
        self.quick_general_btn.clicked.connect(self._add_general_template)
        quick_layout.addWidget(self.quick_general_btn)
        
        quick_layout.addStretch()
        layout.addLayout(quick_layout)
        
        # Main text editor
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText(
            "Enter your notes here...\n\n"
            "Example:\n"
            "State: CA\n"
            "Issue: Missing plate type 'Clean Air Vehicle'\n"
            "Details: This is a special plate for electric vehicles\n"
        )
        
        # Set monospace font for better readability
        font = QFont("Consolas", 10)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.text_edit.setFont(font)
        
        layout.addWidget(self.text_edit, 1)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #888; font-size: 10px;")
        layout.addWidget(self.status_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.open_file_btn = QPushButton("Open in Editor")
        self.open_file_btn.setToolTip("Open the notes file in your default text editor")
        self.open_file_btn.clicked.connect(self._open_in_editor)
        button_layout.addWidget(self.open_file_btn)
        
        button_layout.addStretch()
        
        self.save_btn = QPushButton("Save")
        self.save_btn.setToolTip("Save notes (Ctrl+S)")
        self.save_btn.clicked.connect(self._save_notes)
        button_layout.addWidget(self.save_btn)
        
        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self._on_close)
        button_layout.addWidget(self.close_btn)
        
        layout.addLayout(button_layout)
    
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
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                padding: 8px;
                selection-background-color: #264f78;
            }
            QPushButton {
                background-color: #3c3c3c;
                color: #e0e0e0;
                border: 1px solid #4a4a4a;
                border-radius: 4px;
                padding: 6px 12px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
                border-color: #5a5a5a;
            }
            QPushButton:pressed {
                background-color: #2a2a2a;
            }
        """)
        
        # Style save button differently
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #0e639c;
                color: white;
                border: 1px solid #1177bb;
                border-radius: 4px;
                padding: 6px 12px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #1177bb;
            }
            QPushButton:pressed {
                background-color: #0d5289;
            }
        """)
    
    def _get_file_header(self) -> str:
        """Get the default file header."""
        return (
            "# License Plate Information - User Notes\n"
            "# ==========================================\n"
            "# Use this file to record any missing information,\n"
            "# corrections, or suggestions for the app.\n"
            "# You can send this file to the developer for updates.\n"
            "#\n"
            "# Format suggestions:\n"
            "# - State: [STATE CODE]\n"
            "# - Issue: [Description of missing/incorrect info]\n"
            "# - Suggested fix: [What should be added/changed]\n"
            "# ==========================================\n\n"
        )
    
    def _load_notes(self):
        """Load existing notes from file."""
        try:
            if self.notes_file.exists():
                content = self.notes_file.read_text(encoding='utf-8')
                self.text_edit.setPlainText(content)
                self._update_status(f"Loaded from {self.notes_file.name}")
            else:
                # Start with header template
                self.text_edit.setPlainText(self._get_file_header())
                self._update_status("New notes file will be created on save")
        except Exception as e:
            self._update_status(f"Error loading notes: {e}")
    
    def _save_notes(self):
        """Save notes to file."""
        try:
            content = self.text_edit.toPlainText()
            self.notes_file.write_text(content, encoding='utf-8')
            self._update_status(f"Saved to {self.notes_file.name} at {datetime.now().strftime('%H:%M:%S')}")
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Could not save notes:\n{e}")
    
    def _update_status(self, message: str):
        """Update the status label."""
        self.status_label.setText(message)
    
    def _add_state_template(self):
        """Add a state issue template."""
        template = (
            f"\n--- STATE ISSUE ({datetime.now().strftime('%Y-%m-%d %H:%M')}) ---\n"
            "State: [STATE CODE]\n"
            "Issue: [Description]\n"
            "Expected: [What should be there]\n"
            "Notes: \n"
            "-----------------------------------------\n"
        )
        self._insert_template(template)
    
    def _add_plate_template(self):
        """Add a plate type issue template."""
        template = (
            f"\n--- PLATE TYPE ISSUE ({datetime.now().strftime('%Y-%m-%d %H:%M')}) ---\n"
            "State: [STATE CODE]\n"
            "Plate Type: [Type name]\n"
            "Issue: [missing / incorrect / needs update]\n"
            "Details: \n"
            "-----------------------------------------\n"
        )
        self._insert_template(template)
    
    def _add_general_template(self):
        """Add a general note template."""
        template = (
            f"\n--- NOTE ({datetime.now().strftime('%Y-%m-%d %H:%M')}) ---\n"
            "Subject: \n"
            "Details: \n"
            "-----------------------------------------\n"
        )
        self._insert_template(template)
    
    def _insert_template(self, template: str):
        """Insert a template at the cursor position."""
        cursor = self.text_edit.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        cursor.insertText(template)
        self.text_edit.setTextCursor(cursor)
        self.text_edit.setFocus()
    
    def _open_in_editor(self):
        """Open the notes file in the system default editor."""
        import subprocess
        import os
        
        # Save first
        self._save_notes()
        
        try:
            if os.name == 'nt':  # Windows
                os.startfile(str(self.notes_file))
            else:
                subprocess.run(['xdg-open', str(self.notes_file)])
        except Exception as e:
            QMessageBox.warning(
                self, "Open Error", 
                f"Could not open file in editor:\n{e}\n\n"
                f"File location: {self.notes_file}"
            )
    
    def _on_close(self):
        """Handle close button click."""
        # Check if content changed
        current_content = self.text_edit.toPlainText()
        saved_content = ""
        
        if self.notes_file.exists():
            try:
                saved_content = self.notes_file.read_text(encoding='utf-8')
            except:
                pass
        else:
            saved_content = self._get_file_header()
        
        if current_content != saved_content:
            reply = QMessageBox.question(
                self, "Unsaved Changes",
                "You have unsaved changes. Save before closing?",
                QMessageBox.StandardButton.Save | 
                QMessageBox.StandardButton.Discard | 
                QMessageBox.StandardButton.Cancel
            )
            
            if reply == QMessageBox.StandardButton.Save:
                self._save_notes()
                self.accept()
            elif reply == QMessageBox.StandardButton.Discard:
                self.reject()
            # Cancel does nothing, dialog stays open
        else:
            self.accept()
    
    def keyPressEvent(self, event):
        """Handle key press events."""
        from PySide6.QtCore import Qt
        
        # Ctrl+S to save
        if event.key() == Qt.Key.Key_S and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self._save_notes()
            return
        
        # Escape to close
        if event.key() == Qt.Key.Key_Escape:
            self._on_close()
            return
        
        super().keyPressEvent(event)
