"""
Themed Component - Base class for theme-aware components
"""

from typing import Optional
from tkinter import Widget
from .base_component import BaseComponent

class ThemedComponent(BaseComponent):
    """Base class for components that support theming"""
    
    def __init__(self, parent: Widget, theme_manager=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.theme_manager = theme_manager
        
    def apply_theme(self) -> None:
        """Apply current theme to this component"""
        if self.theme_manager and self.widget:
            self.theme_manager.apply_theme_to_widget(self.widget)
            
    def get_theme_color(self, color_name: str) -> Optional[str]:
        """Get a color from the current theme"""
        if self.theme_manager:
            return self.theme_manager.get_color(color_name)
        return None
        
    def create_themed_widget(self, widget_class, **widget_kwargs):
        """Create a widget with theme applied"""
        widget = widget_class(self.parent, **widget_kwargs)
        if self.theme_manager:
            self.theme_manager.apply_theme_to_widget(widget)
        return widget