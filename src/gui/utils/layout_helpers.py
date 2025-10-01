"""
Layout Helpers - Utility functions for consistent layouts
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, List, Tuple

class LayoutHelpers:
    """Helper functions for consistent widget layouts"""
    
    @staticmethod
    def grid_configure_columns(widget: tk.Widget, columns: List[int], weight: int = 1) -> None:
        """Configure multiple columns with the same weight"""
        for col in columns:
            widget.columnconfigure(col, weight=weight)
            
    @staticmethod
    def grid_configure_rows(widget: tk.Widget, rows: List[int], weight: int = 1) -> None:
        """Configure multiple rows with the same weight"""
        for row in rows:
            widget.rowconfigure(row, weight=weight)
            
    @staticmethod
    def create_button_grid(parent: tk.Widget, buttons_data: List[Tuple], 
                          max_columns: int = 6, padx: int = 5, pady: int = 5) -> None:
        """Create a grid of buttons from button data"""
        row = 0
        col = 0
        
        for button_data in buttons_data:
            button = button_data[0]  # Assume first element is the button widget
            button.grid(row=row, column=col, padx=padx, pady=pady, sticky='ew')
            
            # Configure column weight
            parent.columnconfigure(col, weight=1)
            
            # Move to next position
            col += 1
            if col >= max_columns:
                col = 0
                row += 1
                
    @staticmethod
    def center_window(window: tk.Toplevel, width: int, height: int) -> None:
        """Center a window on the screen"""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        window.geometry(f"{width}x{height}+{x}+{y}")
        
    @staticmethod
    def apply_consistent_padding(widgets: List[tk.Widget], padx: int = 10, pady: int = 5) -> None:
        """Apply consistent padding to a list of widgets"""
        for widget in widgets:
            if hasattr(widget, 'grid'):
                current_info = widget.grid_info()
                if current_info:
                    # Update current_info with new padding values to avoid conflicts
                    current_info.update({'padx': padx, 'pady': pady})
                    widget.grid(**current_info)