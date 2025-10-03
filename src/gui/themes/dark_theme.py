"""
Dark Theme - Complete dark theme implementation with compact button styling
"""

from tkinter import ttk
from typing import Union


class DarkTheme:
    """Dark theme configuration for the application"""
    
    def __init__(self, style: ttk.Style):
        self.style = style
        
        # Color palette
        self.colors = {
            'bg_primary': '#000000',      # Pure black background
            'bg_secondary': '#1a1a1a',    # Dark gray
            'bg_tertiary': '#2d2d2d',     # Medium gray
            'text_primary': '#ffffff',    # White text
            'text_secondary': '#cccccc',  # Light gray text
            'accent_blue': '#4A90E2',     # Blue accent
            'accent_green': '#7ED321',    # Green accent
            'accent_orange': '#FF6B35',   # Orange accent
            'accent_purple': '#BD10E0',   # Purple accent
            'border': '#404040'           # Border color
        }
        
    def apply(self) -> None:
        """Apply the dark theme to the application"""
        print("Applying dark theme with color overrides...")
        self._force_dark_defaults()  # Set theme FIRST
        self._configure_root()
        self._configure_ttk_styles()  # Then configure our styles
        print("Dark theme applied with forced overrides")
        
    def _force_dark_defaults(self) -> None:
        """Force dark theme by overriding system defaults"""
        # Override any system defaults that might be causing white backgrounds
        self.style.theme_use('clam')  # Use clam theme as base - do this FIRST
        
        # Force all default elements to be dark
        self.style.configure('.',
                           background='#000000',
                           foreground='#ffffff',
                           fieldbackground='#000000',
                           selectbackground='#4A90E2',
                           selectforeground='#ffffff')
        
    def _configure_root(self) -> None:
        """Configure root window and basic styles"""
        # Configure root window background
        self.style.configure('.', 
                           background=self.colors['bg_primary'],
                           foreground=self.colors['text_primary'])
                           
    def _configure_ttk_styles(self) -> None:
        """Configure all TTK widget styles"""
        # Frame styles
        self.style.configure('TFrame',
                           background=self.colors['bg_primary'],
                           borderwidth=0)
                           
        # Label styles
        self.style.configure('TLabel',
                           background=self.colors['bg_primary'],
                           foreground=self.colors['text_primary'],
                           font=('Segoe UI', 10))
                           
        # Title label style
        self.style.configure('Title.TLabel',
                           background=self.colors['bg_primary'],
                           foreground=self.colors['accent_blue'],
                           font=('Segoe UI', 16, 'bold'))
                           
        # Status label style  
        self.style.configure('Status.TLabel',
                           background=self.colors['bg_primary'],
                           foreground=self.colors['accent_green'],
                           font=('Segoe UI', 12))
                           
        # Button styles
        self.style.configure('TButton',
                           background=self.colors['bg_tertiary'],
                           foreground=self.colors['text_primary'],
                           borderwidth=1,
                           focuscolor='none',
                           font=('Segoe UI', 10))
                           
        # State button style
        self.style.configure('State.TButton',
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['text_primary'],
                           borderwidth=1,
                           focuscolor='none',
                           font=('Segoe UI', 8))  # Compact font for state buttons
                           
        # Florida main state - special orange color with border
        self.style.configure('Florida.TButton',
                           background='#FF6B35',  # Orange
                           foreground='#FFFFFF',
                           borderwidth=1,
                           focuscolor='none',
                           font=('Segoe UI', 8, 'bold'),  # Readable at all sizes
                           relief='solid',
                           padding=(2, 2),  # Internal padding for text
                           fieldbackground='#FF6B35')  # Force background
                           
        # Plate type states - special blue color with border
        self.style.configure('PlateType.TButton',
                           background='#4A90E2',  # Blue
                           foreground='#FFFFFF',
                           borderwidth=1,
                           focuscolor='none',
                           font=('Segoe UI', 8, 'bold'),  # Readable at all sizes
                           relief='solid',
                           padding=(2, 2),  # Internal padding for text
                           fieldbackground='#4A90E2')  # Force background
                           
        # Florida adjacent states - green color with border
        self.style.configure('FloridaAdjacent.TButton',
                           background='#7ED321',  # Green
                           foreground='#FFFFFF',
                           borderwidth=1,
                           focuscolor='none',
                           font=('Segoe UI', 8, 'bold'),  # Readable at all sizes
                           relief='solid',
                           padding=(2, 2),  # Internal padding for text
                           fieldbackground='#7ED321')  # Force background
                           
        # Other states - gray color with border
        self.style.configure('OtherState.TButton',
                           background='#9B9B9B',  # Gray
                           foreground='#FFFFFF',
                           borderwidth=1,
                           focuscolor='none',
                           font=('Segoe UI', 8),  # Readable at all sizes
                           relief='solid',
                           padding=(2, 2),  # Internal padding for text
                           fieldbackground='#9B9B9B')  # Force background
                           
        # Other jurisdictions - purple color with border
        self.style.configure('OtherJurisdiction.TButton',
                           background='#BD10E0',  # Purple
                           foreground='#FFFFFF',
                           borderwidth=1,
                           focuscolor='none',
                           font=('Segoe UI', 8),  # Readable at all sizes
                           relief='solid',
                           padding=(2, 2),  # Internal padding for text
                           fieldbackground='#BD10E0')  # Force background
                           
        # Configure hover effects for all button styles
        self._configure_hover_effects()
        
    def _configure_hover_effects(self) -> None:
        """Configure hover effects for buttons"""
        # Florida button hover
        self.style.map('Florida.TButton',
                      background=[('active', '#FF8C5C')])  # Lighter orange
                      
        # Plate type button hover
        self.style.map('PlateType.TButton',
                      background=[('active', '#6BA6F0')])  # Lighter blue
                      
        # Florida adjacent button hover
        self.style.map('FloridaAdjacent.TButton',
                      background=[('active', '#95E842')])  # Lighter green
                      
        # Other state button hover
        self.style.map('OtherState.TButton',
                      background=[('active', '#B5B5B5')])  # Lighter gray
                      
        # Other jurisdiction button hover
        self.style.map('OtherJurisdiction.TButton',
                      background=[('active', '#D531FF')])  # Lighter purple
                      
        # Standard button hover
        self.style.map('TButton',
                      background=[('active', self.colors['bg_secondary'])])