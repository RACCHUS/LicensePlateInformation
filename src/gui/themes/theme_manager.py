"""
Theme Manager - Orchestrates theming across the application
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, List, Union
from .dark_theme import DarkTheme
from .color_palette import ColorPalette

class ThemeManager:
    """Centralized theme management for the application"""
    
    def __init__(self, style: ttk.Style):
        self.style = style
        self.dark_theme = DarkTheme(style)
        self.current_theme = 'dark'
        self._root_widgets: List[Union[tk.Widget, tk.Tk, tk.Toplevel]] = []
        
    def initialize(self, root: tk.Tk) -> None:
        """Initialize theme system with root window"""
        self._root_widgets.append(root)
        self.apply_dark_theme()
        
    def apply_dark_theme(self) -> None:
        """Apply dark theme to all components"""
        print("Applying comprehensive dark theme...")
        
        # Apply theme through style system
        self.dark_theme.apply()
        
        # Apply to root widgets
        for root_widget in self._root_widgets:
            self._apply_to_widget_tree(root_widget)
            
        print("Dark theme applied successfully")
        
    def _apply_to_widget_tree(self, widget: Union[tk.Widget, tk.Tk, tk.Toplevel]) -> None:
        """Recursively apply theme to widget and all children"""
        try:
            # Apply dark theme background to tkinter widgets
            if isinstance(widget, (tk.Tk, tk.Toplevel, tk.Frame, tk.Label)):
                widget.configure(bg='#000000')
            if isinstance(widget, tk.Label):
                widget.configure(fg='#ffffff')
            
            # Apply to all children
            if hasattr(widget, 'winfo_children'):
                for child in widget.winfo_children():
                    self._apply_to_widget_tree(child)
        except Exception as e:
            print(f"Warning: Could not apply theme to widget {widget}: {e}")
            
    def apply_theme_to_widget(self, widget: Union[tk.Widget, tk.Tk, tk.Toplevel]) -> None:
        """Apply theme to a specific widget"""
        self._apply_to_widget_tree(widget)
        
    def get_color(self, color_name: str) -> str:
        """Get a color from the current theme"""
        if hasattr(self.dark_theme, 'colors') and color_name in self.dark_theme.colors:
            return self.dark_theme.colors[color_name]
        return '#ffffff'  # Default fallback
        
    def switch_theme(self, theme_name: str) -> None:
        """Switch to a different theme"""
        if theme_name == 'dark':
            self.apply_dark_theme()
            self.current_theme = 'dark'