"""
Smart Plate Type Dropdown - Bidirectional state/plate type filtering
"""

import tkinter as tk
from tkinter import ttk
import json
import os
import sys
from typing import Callable, Optional, List, Dict, Set

from ...utils.widget_factory import WidgetFactory
from utils.logger import log_error, log_warning, log_info


class SmartPlateTypeDropdown:
    """Smart dropdown with bidirectional state/plate type filtering"""
    
    def __init__(self, parent: tk.Widget, widget_factory: WidgetFactory,
                 on_plate_type_selected: Optional[Callable] = None,
                 on_states_with_type_updated: Optional[Callable] = None):
        self.parent = parent
        self.widget_factory = widget_factory
        self.on_plate_type_selected = on_plate_type_selected
        self.on_states_with_type_updated = on_states_with_type_updated
        
        # State
        self.selected_plate_type = None
        self.current_state_filter = None
        self.all_plate_types = []
        self.filtered_plate_types = []
        
        # Load mapping data
        self.mapping_data = self._load_mapping_data()
        
        # Initialize all plate types
        self.all_plate_types = sorted(list(self.mapping_data.get("plate_type_to_states", {}).keys()))
        self.filtered_plate_types = self.all_plate_types.copy()
        
        print(f"🚀 Smart dropdown initialized with {len(self.all_plate_types)} total plate types")
        
        self.setup_panel()
        
    def setup_panel(self):
        """Create the smart dropdown panel"""
        # Main container with border
        self.main_frame = self.widget_factory.create_frame(self.parent)
        self.main_frame.configure(relief='solid', borderwidth=1)
        self.main_frame.pack(fill='x', padx=2, pady=2)
        
        # Inner container
        inner_frame = tk.Frame(self.main_frame, bg='#1a1a1a')
        inner_frame.pack(fill='x', padx=8, pady=8)
        
        # Dropdown selection row
        dropdown_frame = tk.Frame(inner_frame, bg='#1a1a1a')
        dropdown_frame.pack(fill='x')
        
        # Label
        label = tk.Label(
            dropdown_frame,
            text="Select Plate Type:",
            bg='#1a1a1a',
            fg='#ffffff',
            font=('Segoe UI', 9)
        )
        label.pack(side='left', padx=(0, 10))
        
        # Dropdown combobox
        self.plate_type_var = tk.StringVar()
        self.plate_type_var.set("Select plate type...")
        
        style = ttk.Style()
        style.configure('Custom.TCombobox',
                       fieldbackground='#2d2d2d',
                       background='#2d2d2d',
                       foreground='#ffffff',
                       borderwidth=1,
                       relief='solid')
        
        self.dropdown = ttk.Combobox(
            dropdown_frame,
            textvariable=self.plate_type_var,
            values=self.filtered_plate_types,  # Use filtered_plate_types instead of all_plate_types
            state='readonly',
            width=40,
            style='Custom.TCombobox'
        )
        self.dropdown.pack(side='left', padx=(0, 10))
        self.dropdown.bind('<<ComboboxSelected>>', self._on_selection_change)
        
        # Status display
        self.status_label = tk.Label(
            inner_frame,
            text=self._get_status_text(),
            bg='#1a1a1a',
            fg='#888888',
            font=('Segoe UI', 8),
            justify='left'
        )
        self.status_label.pack(anchor='w', pady=(5, 0))
        
        # States display (for when no state selected and plate type chosen)
        self.states_frame = tk.Frame(inner_frame, bg='#1a1a1a')
        self.states_frame.pack(fill='x', pady=(5, 0))
        
        self.states_label = tk.Label(
            self.states_frame,
            text="",
            bg='#1a1a1a',
            fg='#00ff00',
            font=('Segoe UI', 8),
            justify='left',
            wraplength=600
        )
        self.states_label.pack(anchor='w')
        
        # Initialize with all plate types
        self._update_dropdown_options()
        
    def _load_mapping_data(self) -> Dict:
        """Load the state-plate-type mapping data
        
        Returns:
            Mapping dictionary with plate_type_to_states and state_to_plate_types
        """
        # Get base application path (works for both script and PyInstaller)
        if getattr(sys, 'frozen', False):
            project_root = sys._MEIPASS  # type: ignore
        else:
            current_dir = os.path.dirname(__file__)
            
            # Find project root
            search_dir = current_dir
            project_root = None
            
            for _ in range(10):
                if os.path.exists(os.path.join(search_dir, "main.py")):
                    project_root = search_dir
                    break
                parent = os.path.dirname(search_dir)
                if parent == search_dir:
                    break
                search_dir = parent
            
            if not project_root:
                log_warning("Could not find project root for mapping data")
                return {"plate_type_to_states": {}, "state_to_plate_types": {}}
        
        mapping_file = os.path.join(project_root, "data", "state_plate_type_mapping.json")
        
        try:
            if os.path.exists(mapping_file):
                with open(mapping_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    log_info("Loaded state-plate mapping data")
                    return data
            else:
                log_warning(f"Mapping file not found: {mapping_file}")
                return {"plate_type_to_states": {}, "state_to_plate_types": {}}
                
        except json.JSONDecodeError as e:
            log_error(f"Invalid JSON in mapping file: {mapping_file}", exc=e)
            return {"plate_type_to_states": {}, "state_to_plate_types": {}}
        except OSError as e:
            log_error(f"Error reading mapping file: {mapping_file}", exc=e)
            return {"plate_type_to_states": {}, "state_to_plate_types": {}}
    
    def set_state_filter(self, state_code: str | None = None):
        """Set the state filter for plate types"""
        print(f"🔧 Setting state filter to: {state_code}")
        self.current_state_filter = state_code
        self._update_dropdown_options()
        
    def _update_dropdown_options(self):
        """Update dropdown options based on current state filter"""
        if self.current_state_filter:
            # Show only plate types for selected state
            state_data = self.mapping_data.get("state_to_plate_types", {}).get(self.current_state_filter, {})
            self.filtered_plate_types = state_data.get("plate_types", [])
            print(f"📋 Filtered to {len(self.filtered_plate_types)} plate types for {self.current_state_filter}")
        else:
            # Show all plate types
            self.filtered_plate_types = sorted(list(self.mapping_data.get("plate_type_to_states", {}).keys()))
            print(f"📋 Showing all {len(self.filtered_plate_types)} plate types")
        
        # Update dropdown
        self.dropdown['values'] = self.filtered_plate_types
        
        # Force dropdown to refresh
        current_selection = self.plate_type_var.get()
        if current_selection == "Select plate type..." or current_selection not in self.filtered_plate_types:
            self.plate_type_var.set("Select plate type...")
        
        self.status_label.configure(text=self._get_status_text())
        
    def _get_status_text(self) -> str:
        """Get status text for current state"""
        if self.current_state_filter:
            return f"Showing {len(self.filtered_plate_types)} plate types for {self.current_state_filter}"
        else:
            return f"Showing all {len(self.filtered_plate_types)} plate types from all states"
    
    def _on_selection_change(self, event):
        """Handle dropdown selection change"""
        try:
            selected = self.plate_type_var.get()
            if selected and selected != "Select plate type...":
                self.selected_plate_type = selected
                
                # Update status
                if self.current_state_filter:
                    self.status_label.configure(
                        text=f"Selected: {selected} (available in {self.current_state_filter})",
                        fg='#ffffff'
                    )
                    self.states_label.configure(text="")
                else:
                    # Show which states have this plate type
                    states_with_type = self.mapping_data.get("plate_type_to_states", {}).get(selected, [])
                    self.status_label.configure(
                        text=f"Selected: {selected}",
                        fg='#ffffff'
                    )
                    
                    if states_with_type:
                        states_text = f"Available in {len(states_with_type)} states: {', '.join(states_with_type)}"
                        self.states_label.configure(text=states_text)
                        
                        # Notify callback about states with this type
                        if self.on_states_with_type_updated:
                            try:
                                self.on_states_with_type_updated(states_with_type)
                            except Exception as e:
                                log_error(f"States update callback failed for {selected}", exc=e)
                    else:
                        self.states_label.configure(text="No state data available for this plate type")
                
                # Notify main callback
                if self.on_plate_type_selected:
                    try:
                        self.on_plate_type_selected(selected)
                    except Exception as e:
                        log_error(f"Plate type selection callback failed for {selected}", exc=e)
        except Exception as e:
            log_error("Error handling plate type selection change", exc=e)
                
    def get_main_frame(self) -> tk.Widget:
        """Get the main panel frame"""
        return self.main_frame
        
    def set_selection(self, plate_type: str):
        """Programmatically set the selection"""
        if plate_type in self.filtered_plate_types:
            self.plate_type_var.set(plate_type)
            self._on_selection_change(None)