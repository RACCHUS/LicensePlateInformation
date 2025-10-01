"""
Color Palette - Centralized color definitions
"""

from typing import Dict

class ColorPalette:
    """Centralized color definitions for consistent theming"""
    
    # Pure Dark Theme Colors
    DARK_THEME = {
        # Core colors
        'bg_primary': '#000000',      # Pure black background
        'bg_secondary': '#1a1a1a',    # Slightly lighter black
        'bg_tertiary': '#2d2d2d',     # Dark gray for cards/panels
        
        # Text colors
        'text_primary': '#ffffff',     # Pure white text
        'text_secondary': '#e0e0e0',   # Light gray text
        'text_muted': '#b0b0b0',       # Muted gray text
        
        # Interactive colors
        'accent_blue': '#4a9eff',      # Primary blue accent
        'accent_green': '#4caf50',     # Success/available green
        'accent_orange': '#ff9800',    # Warning orange
        'accent_red': '#f44336',       # Error red
        
        # State colors
        'hover': '#333333',            # Hover state
        'active': '#404040',           # Active/pressed state
        'selected': '#1976d2',         # Selected state
        'disabled': '#666666',         # Disabled state
        
        # Border colors
        'border_light': '#404040',     # Light border
        'border_medium': '#606060',    # Medium border
        'border_dark': '#808080',      # Dark border
    }
    
    @classmethod
    def get_dark_colors(cls) -> Dict[str, str]:
        """Get all dark theme colors"""
        return cls.DARK_THEME.copy()
        
    @classmethod
    def get_color(cls, color_name: str, theme: str = 'dark') -> str:
        """Get specific color by name"""
        if theme == 'dark':
            return cls.DARK_THEME.get(color_name, '#ffffff')
        return '#ffffff'  # Fallback