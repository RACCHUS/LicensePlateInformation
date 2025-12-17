"""
State Selection Panel - Ultra-compact layout with state codes only
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional, Dict

from ...utils.widget_factory import WidgetFactory
from ...utils.layout_helpers import LayoutHelpers
from ....utils.logger import log_error, log_warning


class StateSelectionPanel:
    """Panel with ultra-compact layout showing only state codes"""
    
    def __init__(self, parent: tk.Widget, widget_factory: WidgetFactory, 
                 on_state_selected: Optional[Callable] = None):
        self.parent = parent
        self.widget_factory = widget_factory
        self.on_state_selected = on_state_selected
        self.state_buttons: Dict[str, ttk.Button] = {}
        
        # Complete list of all jurisdictions with color groupings
        self.states_data = {
            # States
            'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas',
            'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware',
            'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho',
            'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
            'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
            'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
            'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
            'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
            'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma',
            'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
            'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah',
            'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia',
            'WI': 'Wisconsin', 'WY': 'Wyoming',
            
            # Federal District
            'DC': 'District of Columbia',
            
            # Other Jurisdictions (Territories, Government, Canadian)
            'AS': 'American Samoa', 'GU': 'Guam', 'MP': 'Northern Mariana Islands',
            'PR': 'Puerto Rico', 'VI': 'US Virgin Islands',
            'GS': 'Government Service',
            'ON': 'Ontario', 'AB': 'Alberta', 'QC': 'Quebec'
        }
        
        # Color groupings based on plate types and geographic proximity to Florida
        self.color_groups = {
            # Florida - Main state (special color)
            'florida_main': ['FL'],
            
            # Plate type states (Maine, Mass, Ohio, Indiana, Illinois) - special color
            'plate_type_states': ['ME', 'MA', 'OH', 'IN', 'IL'],
            
            # States closest to Florida - one color
            'florida_adjacent': ['AL', 'GA', 'SC', 'NC', 'TN', 'MS', 'LA'],
            
            # All other states (excluding DC which goes with others)
            'other_states': [code for code in self.states_data.keys() 
                           if code not in ['FL', 'ME', 'MA', 'OH', 'IN', 'IL', 'AL', 'GA', 'SC', 'NC', 'TN', 'MS', 'LA'] 
                           and code not in ['AS', 'GU', 'MP', 'PR', 'VI', 'GS', 'ON', 'AB', 'QC', 'DC']],
            
            # Other jurisdictions (territories, government, Canadian, DC)
            'other_jurisdictions': ['AS', 'GU', 'MP', 'PR', 'VI', 'GS', 'ON', 'AB', 'QC', 'DC']
        }
        
        # Initialize the panel
        self.setup_panel()
        
    def setup_panel(self):
        """Create tiny state selection panel for top-left positioning"""
        # Main container with border for visibility
        self.main_frame = self.widget_factory.create_frame(self.parent, padding="2")
        self.main_frame.configure(relief='solid', borderwidth=1)
        self.main_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Create inner container that fills all available space (no scrollbar)
        self.inner_frame = self.widget_factory.create_frame(self.main_frame)
        self.inner_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Create unified button grid with all jurisdictions
        self._create_unified_grid()
        
        return self.main_frame
        
    def _on_window_resize(self, event):
        """Handle window resize - minimal handling needed with fixed button sizes"""
        # With fixed button sizes, minimal resize handling needed
        pass
        
    def _create_unified_grid(self):
        """Create one unified grid with all jurisdictions"""
        # Single grid container with tasteful border - use tk.Frame for background color
        grid_frame = tk.Frame(self.inner_frame, relief='solid', borderwidth=1, bg='#2d2d2d')
        grid_frame.pack(fill='x', padx=2, pady=2)  # Fill x and add spacing
        
        # Create ordered list: States first, then others at the end (keeping purple color)
        all_jurisdictions = []
        
        # Add all states (excluding DC and Canadian provinces)
        states_only = [
            (code, name) for code, name in self.states_data.items() 
            if code not in ['AS', 'GU', 'MP', 'PR', 'VI', 'GS', 'ON', 'AB', 'QC', 'DC']
        ]
        all_jurisdictions.extend(states_only)
        
        # Add other jurisdictions at the end (including DC - keeping purple color to identify as "others")
        others = [
            (code, name) for code, name in self.states_data.items()
            if code in ['AS', 'GU', 'MP', 'PR', 'VI', 'GS', 'ON', 'AB', 'QC', 'DC']
        ]
        all_jurisdictions.extend(others)
        
        # Use 12 columns for better space utilization
        self._create_button_grid(grid_frame, all_jurisdictions, columns=12)
        
    def _create_button_grid(self, parent: tk.Widget, items_list: list, columns: int):
        """Create responsive grid with professional button sizing"""
        for i, (code, name) in enumerate(items_list):
            row = i // columns
            column = i % columns
            
            # Determine button style based on color groups
            if code in self.color_groups['florida_main']:
                style = 'Florida.TButton'
            elif code in self.color_groups['plate_type_states']:
                style = 'PlateType.TButton'
            elif code in self.color_groups['florida_adjacent']:
                style = 'FloridaAdjacent.TButton'
            elif code in self.color_groups['other_jurisdictions']:
                style = 'OtherJurisdiction.TButton'
            else:
                style = 'OtherState.TButton'
            
            # Create button with responsive sizing
            button = ttk.Button(
                parent,
                text=code,  # Only show state code - clean and compact
                style=style,
                width=4,  # Minimum width to ensure text is visible
                command=lambda state_code=code: self._handle_state_selection(state_code)
            )
            
            # Grid with consistent spacing - buttons will expand beyond minimum width
            button.grid(row=row, column=column, padx=1, pady=1, sticky='nsew', ipadx=2, ipady=2)
            
            # Store button reference
            self.state_buttons[code] = button
            
        # Configure columns and rows for responsive layout
        for col in range(columns):
            parent.grid_columnconfigure(col, weight=1, uniform="button")
        
        # Configure rows to allow vertical expansion
        num_rows = (len(items_list) + columns - 1) // columns
        for row in range(num_rows):
            parent.grid_rowconfigure(row, weight=1)
            
    def _handle_state_selection(self, state_code: str):
        """Handle state button click"""
        try:
            state_name = self.states_data.get(state_code, state_code)
            
            # Determine category and add appropriate styling
            if state_code in self.color_groups['florida_main']:
                print(f"🟠 FLORIDA (Main): {state_code} - {state_name}")
            elif state_code in self.color_groups['plate_type_states']:
                print(f"🔵 PLATE TYPE STATE: {state_code} - {state_name}")
            elif state_code in self.color_groups['florida_adjacent']:
                print(f"🟢 FLORIDA ADJACENT: {state_code} - {state_name}")
            elif state_code in self.color_groups['other_jurisdictions']:
                print(f"🟣 OTHER JURISDICTION: {state_code} - {state_name}")
            else:
                print(f"⚪ OTHER STATE: {state_code} - {state_name}")
            
            if self.on_state_selected:
                try:
                    self.on_state_selected(state_code, state_name)
                except Exception as e:
                    log_error(f"State selection callback failed for {state_code}", exc=e)
        except Exception as e:
            log_error(f"Error handling state selection: {state_code}", exc=e)
            
    def highlight_state(self, state_code: str):
        """Highlight a specific state button"""
        if state_code in self.state_buttons:
            print(f"Highlighting: {state_code}")
    
    def clear_state_selection(self):
        """Clear any state button highlighting/selection"""
        print("🎨 Clearing state button highlighting")
        # Note: ttk.Button styling is controlled by themes, not direct background config
        # Buttons automatically revert to their defined style (Florida.TButton, etc.)
        # No manual reset needed - the theme handles it
            
    def get_main_frame(self) -> tk.Widget:
        """Get the main panel frame"""
        return self.main_frame