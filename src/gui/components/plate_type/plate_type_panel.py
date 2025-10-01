"""
Plate Type Selection Panel - Component for selecting plate types
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional
from ...utils.widget_factory import WidgetFactory


class PlateTypePanel:
    """Panel for selecting different plate types"""
    
    def __init__(self, parent: tk.Widget, widget_factory: WidgetFactory,
                 on_plate_type_selected: Optional[Callable] = None):
        self.parent = parent
        self.widget_factory = widget_factory
        self.on_plate_type_selected = on_plate_type_selected
        self.plate_type_buttons = {}
        self.selected_plate_type = None
        
        # Available plate types
        self.plate_types = [
            'Standard', 'Specialty', 'Vanity', 'Commercial',
            'Motorcycle', 'Trailer', 'Temporary', 'Dealer'
        ]
        
        self.setup_panel()
        
    def setup_panel(self):
        """Create the plate type selection panel"""
        # Main container with border
        self.main_frame = self.widget_factory.create_frame(self.parent)
        self.main_frame.configure(relief='solid', borderwidth=1)
        self.main_frame.pack(fill='x', padx=2, pady=2)
        
        # Inner container
        inner_frame = self.widget_factory.create_frame(self.main_frame)
        inner_frame.pack(fill='x', padx=4, pady=4)
        
        # Create plate type buttons in grid
        for i, plate_type in enumerate(self.plate_types):
            row = i // 4
            col = i % 4
            
            button = ttk.Button(
                inner_frame,
                text=plate_type,
                width=10,
                command=lambda pt=plate_type: self._handle_selection(pt),
                style='TButton'
            )
            button.grid(row=row, column=col, padx=1, pady=1, sticky='ew')
            self.plate_type_buttons[plate_type] = button
            
        # Configure grid weights
        for col in range(4):
            inner_frame.grid_columnconfigure(col, weight=1)
            
    def _handle_selection(self, plate_type: str):
        """Handle plate type selection"""
        # Reset previous selection
        if self.selected_plate_type:
            self.plate_type_buttons[self.selected_plate_type].configure(style='TButton')
            
        # Set new selection
        self.selected_plate_type = plate_type
        self.plate_type_buttons[plate_type].configure(style='Accent.TButton')
        
        print(f"🎯 Plate type selected: {plate_type}")
        
        if self.on_plate_type_selected:
            self.on_plate_type_selected(plate_type)
            
    def clear_selection(self):
        """Clear current selection"""
        if self.selected_plate_type:
            self.plate_type_buttons[self.selected_plate_type].configure(style='TButton')
            self.selected_plate_type = None
            
    def get_main_frame(self) -> tk.Widget:
        """Get the main panel frame"""
        return self.main_frame