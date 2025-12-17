"""
State Button Widget for License Plate Information System.

A styled button representing a US state or jurisdiction with fixed color coding.
Colors are based on static categories (FL, plate type, nearby, etc.).
Ordering in the UI changes based on the current mode.
"""

from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QFont


class StateButton(QPushButton):
    """
    A styled button for state selection.
    
    Fixed color categories (do not change with mode):
    - florida: FL only (orange, prominent)
    - plate_type: MA, ME, OH, IN, IL (purple)
    - nearby: States near Florida - GA, AL, SC, NC, TN, MS, LA (blue)
    - distant_major: Major states far from FL - CA, TX, NY, PA, etc. (teal)
    - territory: US territories - PR, GU, VI, etc. (brown)
    - canadian: Canadian provinces (red/maple)
    - normal: All other US states (gray)
    """
    
    # Signal emitted when state is clicked
    state_clicked = Signal(str)  # state_code
    
    # Single size for all buttons
    BUTTON_SIZE = {'width': 26, 'height': 20, 'font_size': 9}
    
    # Aliases for test compatibility
    SIZE_NORMAL = BUTTON_SIZE
    SIZE_PRIMARY = BUTTON_SIZE
    SIZE_SECONDARY = BUTTON_SIZE
    
    # Color schemes for different categories (fixed, not mode-dependent)
    COLORS = {
        'florida': {
            'bg': '#FF9800', 'bg_hover': '#FFB74D', 'bg_pressed': '#F57C00',
            'text': '#000000', 'border': '#FF9800',
        },
        'plate_type': {
            'bg': '#7B1FA2', 'bg_hover': '#9C27B0', 'bg_pressed': '#6A1B9A',
            'text': '#ffffff', 'border': '#7B1FA2',
        },
        'nearby': {
            'bg': '#1565C0', 'bg_hover': '#1976D2', 'bg_pressed': '#0D47A1',
            'text': '#ffffff', 'border': '#1565C0',
        },
        'distant_major': {
            'bg': '#00838F', 'bg_hover': '#0097A7', 'bg_pressed': '#006064',
            'text': '#ffffff', 'border': '#00838F',
        },
        'territory': {
            'bg': '#5D4037', 'bg_hover': '#6D4C41', 'bg_pressed': '#4E342E',
            'text': '#ffffff', 'border': '#5D4037',
        },
        'canadian': {
            'bg': '#C62828', 'bg_hover': '#D32F2F', 'bg_pressed': '#B71C1C',
            'text': '#ffffff', 'border': '#C62828',
        },
        'normal': {
            'bg': '#424242', 'bg_hover': '#616161', 'bg_pressed': '#303030',
            'text': '#e0e0e0', 'border': '#424242',
        },
        # Aliases for test compatibility
        'primary': {
            'bg': '#FF9800', 'bg_hover': '#FFB74D', 'bg_pressed': '#F57C00',
            'text': '#000000', 'border': '#FF9800',
        },
        'secondary': {
            'bg': '#1565C0', 'bg_hover': '#1976D2', 'bg_pressed': '#0D47A1',
            'text': '#ffffff', 'border': '#1565C0',
        },
        'excluded': {
            'bg': '#424242', 'bg_hover': '#616161', 'bg_pressed': '#303030',
            'text': '#e0e0e0', 'border': '#424242',
        },
        'selected': {
            'border': '#4CAF50',
            'border_width': '2px',
        }
    }
    
    # Static categorization (colors are fixed based on these)
    FLORIDA = {'FL'}
    PLATE_TYPE_STATES = {'MA', 'ME', 'OH', 'IN', 'IL'}
    NEARBY_STATES = {'GA', 'AL', 'SC', 'NC', 'TN', 'MS', 'LA'}
    DISTANT_MAJOR = {'CA', 'TX', 'NY', 'PA', 'NJ', 'WA', 'AZ', 'CO', 'VA', 'MD'}
    TERRITORIES = {'PR', 'GU', 'VI', 'AS', 'MP', 'DC'}
    CANADIAN = {'AB', 'BC', 'MB', 'NB', 'NL', 'NS', 'NT', 'NU', 'ON', 'PE', 'QC', 'SK', 'YT'}
    
    @classmethod
    def get_category(cls, state_code: str) -> str:
        """Determine the fixed color category for a state code."""
        if state_code in cls.FLORIDA:
            return 'florida'
        elif state_code in cls.PLATE_TYPE_STATES:
            return 'plate_type'
        elif state_code in cls.NEARBY_STATES:
            return 'nearby'
        elif state_code in cls.DISTANT_MAJOR:
            return 'distant_major'
        elif state_code in cls.TERRITORIES:
            return 'territory'
        elif state_code in cls.CANADIAN:
            return 'canadian'
        else:
            return 'normal'
    
    def __init__(self, state_code: str, parent=None):
        super().__init__(state_code)
        if parent:
            self.setParent(parent)
        
        self.state_code = state_code
        self._category = self.get_category(state_code)
        self._is_selected = False
        self._is_excluded = False
        
        # CRITICAL: Set size policy to Fixed so buttons don't stretch
        from PySide6.QtWidgets import QSizePolicy
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        self.clicked.connect(self._on_clicked)
        self._apply_style()
    
    @property
    def category(self) -> str:
        return self._category
    
    @property
    def is_excluded(self) -> bool:
        return self._is_excluded
    
    def set_mode_category(self, is_primary: bool, is_secondary: bool, is_excluded: bool):
        """Called when mode changes - only affects ordering, not color."""
        # Colors stay the same, this is just for compatibility
        self._is_excluded = is_excluded
        # Don't change _category - it's fixed based on state
    
    def set_category(self, category: str):
        """For compatibility - doesn't change actual color category."""
        pass
    
    @property
    def is_selected(self) -> bool:
        return self._is_selected
    
    @is_selected.setter
    def is_selected(self, value: bool):
        self._is_selected = value
        self._apply_style()
    
    def set_selected(self, selected: bool):
        """Set the selected state of the button."""
        self.is_selected = selected
    
    def _on_clicked(self):
        """Handle button click."""
        self.state_clicked.emit(self.state_code)
    
    def _apply_style(self):
        """Apply styling based on fixed category and selection state."""
        size = self.BUTTON_SIZE
        colors = self.COLORS.get(self._category, self.COLORS['normal'])
        selected = self.COLORS['selected']
        
        # Set fixed size
        self.setFixedWidth(size['width'])
        self.setFixedHeight(size['height'])
        
        # Build stylesheet
        border_color = selected['border'] if self._is_selected else colors['border']
        border_width = selected['border_width'] if self._is_selected else '1px'
        
        style = f"""
            QPushButton {{
                background-color: {colors['bg']};
                color: {colors['text']};
                border: {border_width} solid {border_color};
                border-radius: 2px;
                font-size: {size['font_size']}px;
                font-weight: bold;
                padding: 0px;
            }}
            QPushButton:hover {{
                background-color: {colors['bg_hover']};
            }}
            QPushButton:pressed {{
                background-color: {colors['bg_pressed']};
            }}
        """
        
        self.setStyleSheet(style)
