"""
Font Preview Widget for License Plate Information System.

Displays character samples using the appropriate font for each state's license plates.
Shows visual distinction for letter O / number 0 usage.
"""

import json
from pathlib import Path
from typing import Dict, Optional, Tuple

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel, QFrame, QScrollArea
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont


class FontPreviewWidget(QWidget):
    """
    Widget showing character font samples for a state's license plates.
    
    Displays A-Z and 0-9 in the state's plate font, with color coding
    for O/0 usage rules.
    """
    
    state_selected = Signal(str)  # Emitted when user clicks a character
    
    # Font mappings - maps state font descriptions to system fonts
    # Priority order matters - more specific matches first
    FONT_MAPPINGS = [
        # Narrow fonts (most common for license plates)
        (['narrow sans serif', 'narrow block'], ('Arial Narrow', 16, 'Bold')),
        (['narrow', 'condensed', 'compressed'], ('Arial Narrow', 16, 'Bold')),
        
        # Highway Gothic and derivatives (very common)
        (['highway gothic'], ('Arial', 16, 'Bold')),
        
        # Block/Bold fonts
        (['block sans serif', 'block style'], ('Arial Black', 15, 'Bold')),
        (['block'], ('Arial Black', 15, 'Bold')),
        
        # Custom/Proprietary (use distinctive font)
        (['proprietary', 'custom sans serif', 'custom'], ('Impact', 16, 'Normal')),
        
        # Special named fonts
        (['penitentiary gothic'], ('Arial Black', 16, 'Bold')),  # California
        (['fe-schrift'], ('Consolas', 15, 'Bold')),  # European-style
        (['interstate'], ('Arial', 16, 'Bold')),  # Similar to highway signs
        
        # Modified versions
        (['modified sans serif', 'modified block'], ('Arial', 16, 'Bold')),
        
        # General sans serif
        (['sans serif', 'sans-serif'], ('Arial', 16, 'Bold')),
        
        # Serif fonts (rare)
        (['serif script', 'serif'], ('Times New Roman', 15, 'Bold')),
        (['serifed'], ('Times New Roman', 15, 'Bold')),
        
        # Government/Diplomatic standard
        (['diplomatic', 'government'], ('Arial', 15, 'Bold')),
        
        # Monospace/Fixed (if any)
        (['monospace', 'courier', 'fixed'], ('Courier New', 15, 'Bold')),
        
        # Default fallback
        (['default'], ('Arial', 16, 'Bold'))
    ]
    
    # Colors
    COLOR_NORMAL = "#ffffff"       # White - normal character
    COLOR_NOT_USED = "#ff6666"     # Red - character not used
    COLOR_USED = "#66ff66"         # Green - character used (special note)
    COLOR_SPECIAL = "#ffaa66"      # Orange - conditional/partial usage
    COLOR_BG = "#3a3a3a"           # Cell background
    COLOR_PANEL_BG = "#2a2a2a"     # Panel background
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.current_state: Optional[str] = None
        self._character_labels: Dict[str, QLabel] = {}
        self._state_data_cache: Dict[str, dict] = {}
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Create the widget UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # Title
        self.title_label = QLabel("Character Font Preview")
        self.title_label.setObjectName("panelHeader")
        self.title_label.setStyleSheet("""
            QLabel#panelHeader {
                color: #4CAF50;
                font-size: 12px;
                font-weight: bold;
                padding: 2px;
            }
        """)
        layout.addWidget(self.title_label)
        
        # Character grid in scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; background: #2a2a2a; }")
        
        grid_widget = QWidget()
        grid_widget.setStyleSheet(f"background: {self.COLOR_PANEL_BG};")
        self.grid_layout = QGridLayout(grid_widget)
        self.grid_layout.setSpacing(3)
        self.grid_layout.setContentsMargins(5, 5, 5, 5)
        
        # Create character grid (6 columns)
        characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        for i, char in enumerate(characters):
            row = i // 6
            col = i % 6
            
            cell = self._create_character_cell(char)
            self.grid_layout.addWidget(cell, row, col)
        
        scroll.setWidget(grid_widget)
        layout.addWidget(scroll, 1)
        
        # Status/info label
        self.status_label = QLabel("Select a state to see font preview")
        self.status_label.setWordWrap(True)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                color: #888888;
                font-size: 10px;
                padding: 5px;
            }
        """)
        layout.addWidget(self.status_label)
    
    def _create_character_cell(self, char: str) -> QFrame:
        """Create a single character cell."""
        cell = QFrame()
        cell.setStyleSheet(f"""
            QFrame {{
                background: {self.COLOR_BG};
                border: 1px solid #505050;
                border-radius: 3px;
            }}
        """)
        cell.setFixedSize(36, 36)
        
        layout = QVBoxLayout(cell)
        layout.setContentsMargins(0, 0, 0, 0)
        
        label = QLabel(char)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(f"""
            QLabel {{
                color: {self.COLOR_NORMAL};
                font-family: 'Courier New';
                font-size: 16px;
                font-weight: bold;
                background: transparent;
            }}
        """)
        layout.addWidget(label)
        
        self._character_labels[char] = label
        return cell
    
    def _find_best_font(self, description: str) -> Tuple[str, int, str]:
        """Find the best matching system font for a plate font description."""
        if not description:
            return ('Arial', 16, 'Bold')
        
        desc_lower = description.lower()
        
        for keywords, font_spec in self.FONT_MAPPINGS:
            for keyword in keywords:
                if keyword in desc_lower:
                    return font_spec
        
        return ('Arial', 16, 'Bold')
    
    def _load_state_data(self, state_code: str) -> Optional[dict]:
        """Load state data from JSON file."""
        if state_code in self._state_data_cache:
            return self._state_data_cache[state_code]
        
        state_file = Path('data/states') / f'{state_code.lower()}.json'
        if not state_file.exists():
            return None
        
        try:
            with open(state_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self._state_data_cache[state_code] = data
            return data
        except Exception as e:
            print(f"Error loading state data for {state_code}: {e}")
            return None
    
    def _get_character_rules(self, state_data: dict) -> dict:
        """Extract character rules from state data."""
        rules = {
            'allows_letter_o': state_data.get('allows_letter_o', True),
            'uses_zero_for_o': state_data.get('uses_zero_for_o', False),
            'zero_is_slashed': state_data.get('zero_is_slashed', False),
        }
        
        # Check for Nevada's special dual system
        if 'letter_o_and_zero_usage' in state_data:
            rules['dual_system'] = state_data['letter_o_and_zero_usage']
        
        return rules
    
    def update_state(self, state_code: str, state_name: Optional[str] = None):
        """
        Update character font display for selected state.
        
        Args:
            state_code: State abbreviation (e.g., 'FL', 'CA')
            state_name: Full state name (optional, for display)
        """
        self.current_state = state_code
        
        if not state_code:
            self._reset_display()
            return
        
        state_data = self._load_state_data(state_code)
        if not state_data:
            self._reset_display()
            self.status_label.setText(f"No data found for {state_code}")
            return
        
        # Get font info
        main_font = state_data.get('main_font', '')
        font_family, font_size, font_weight = self._find_best_font(main_font)
        
        # Get character rules
        rules = self._get_character_rules(state_data)
        
        # Update each character
        for char, label in self._character_labels.items():
            color = self.COLOR_NORMAL
            display_char = char
            
            # Handle letter O
            if char == 'O':
                if not rules.get('allows_letter_o', True):
                    color = self.COLOR_NOT_USED
                elif 'dual_system' in rules:
                    color = self.COLOR_SPECIAL
            
            # Handle number 0
            elif char == '0':
                if rules.get('uses_zero_for_o', False):
                    color = self.COLOR_USED
                elif rules.get('zero_is_slashed', False):
                    display_char = 'Ø'
                    color = self.COLOR_USED
                elif 'dual_system' in rules:
                    color = self.COLOR_SPECIAL
                elif not rules.get('allows_letter_o', True):
                    # If O not allowed, 0 is likely used
                    color = self.COLOR_USED
            
            # Apply styling
            weight_val = QFont.Weight.Bold if font_weight == 'Bold' else QFont.Weight.Normal
            label.setText(display_char)
            label.setStyleSheet(f"""
                QLabel {{
                    color: {color};
                    font-family: '{font_family}';
                    font-size: {font_size}px;
                    font-weight: {'bold' if font_weight == 'Bold' else 'normal'};
                    background: transparent;
                }}
            """)
        
        # Update status
        display_name = state_name or state_code
        status_parts = [f"<b>{display_name}</b>"]
        
        if main_font:
            status_parts.append(f"Font: {main_font}")
        
        # Add character notes
        notes = []
        if not rules.get('allows_letter_o', True):
            notes.append("❌ No letter 'O'")
        if rules.get('uses_zero_for_o', False):
            notes.append("✅ Uses '0' only")
        if rules.get('zero_is_slashed', False):
            notes.append("Ø Slashed zero")
        if 'dual_system' in rules:
            notes.append("⚠️ O/0 varies by plate type")
        
        if notes:
            status_parts.append(' • '.join(notes))
        
        self.status_label.setText('<br>'.join(status_parts))
        self.status_label.setStyleSheet("""
            QLabel {
                color: #4CAF50;
                font-size: 10px;
                padding: 5px;
            }
        """)
    
    def _reset_display(self):
        """Reset display to default state."""
        default_style = f"""
            QLabel {{
                color: {self.COLOR_NORMAL};
                font-family: 'Courier New';
                font-size: 16px;
                font-weight: bold;
                background: transparent;
            }}
        """
        
        for char, label in self._character_labels.items():
            label.setText(char)
            label.setStyleSheet(default_style)
        
        self.status_label.setText("Select a state to see font preview")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #888888;
                font-size: 10px;
                padding: 5px;
            }
        """)
        
        self.current_state = None
    
    def clear(self):
        """Clear the font preview display."""
        self._reset_display()
    
    def set_state(self, state_code: str, uses_zero_for_o: bool = False, no_letter_o: bool = False):
        """
        Set the state and update display with O/0 rules.
        
        This is a convenience method that can be called with pre-extracted rules.
        
        Args:
            state_code: State abbreviation
            uses_zero_for_o: If True, state uses 0 in place of O
            no_letter_o: If True, state doesn't use letter O at all
        """
        if not state_code:
            self._reset_display()
            return
        
        # Try to load full state data first
        state_data = self._load_state_data(state_code)
        
        if state_data:
            # Use full update with all data
            self.update_state(state_code)
        else:
            # Use the passed rules for basic update
            self._update_with_rules(state_code, uses_zero_for_o, no_letter_o)
    
    def _update_with_rules(self, state_code: str, uses_zero_for_o: bool, no_letter_o: bool):
        """Update display using just the O/0 rules."""
        self.current_state = state_code
        
        # Use default font
        font_family = 'Arial'
        font_size = 16
        
        for char, label in self._character_labels.items():
            color = self.COLOR_NORMAL
            display_char = char
            
            if char == 'O':
                if no_letter_o:
                    color = self.COLOR_NOT_USED
            elif char == '0':
                if uses_zero_for_o or no_letter_o:
                    color = self.COLOR_USED
            
            label.setText(display_char)
            label.setStyleSheet(f"""
                QLabel {{
                    color: {color};
                    font-family: '{font_family}';
                    font-size: {font_size}px;
                    font-weight: bold;
                    background: transparent;
                }}
            """)
        
        # Update status
        status_parts = [f"<b>{state_code}</b>"]
        notes = []
        if no_letter_o:
            notes.append("❌ No letter 'O'")
        if uses_zero_for_o:
            notes.append("✅ Uses '0' for O")
        
        if notes:
            status_parts.append(' • '.join(notes))
        
        self.status_label.setText('<br>'.join(status_parts))
        self.status_label.setStyleSheet("""
            QLabel {
                color: #4CAF50;
                font-size: 10px;
                padding: 5px;
            }
        """)
