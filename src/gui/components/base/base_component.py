"""
Base Component - Abstract base class for all UI components
"""

from abc import ABC, abstractmethod
from tkinter import Widget
from typing import Optional, Dict, Any

class BaseComponent(ABC):
    """Abstract base class for all UI components"""
    
    def __init__(self, parent: Widget, **kwargs):
        self.parent = parent
        self.kwargs = kwargs
        self.widget: Optional[Widget] = None
        self._is_created = False
        
    @abstractmethod
    def create(self) -> Widget:
        """Create the component widget"""
        pass
    
    @abstractmethod
    def destroy(self) -> None:
        """Clean up component resources"""
        pass
    
    def get_widget(self) -> Optional[Widget]:
        """Get the main widget for this component"""
        return self.widget
    
    def is_created(self) -> bool:
        """Check if component has been created"""
        return self._is_created