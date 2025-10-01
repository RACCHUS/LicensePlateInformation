"""
State Selection Panel - Ultra-compact layout with state codes only
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional, Dict
from ...utils.widget_factory import WidgetFactory
from ...utils.layout_helpers import LayoutHelpers


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
            'ON': 'Ontario', 'AB': 'Alberta'
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
                           and code not in ['AS', 'GU', 'MP', 'PR', 'VI', 'GS', 'ON', 'AB', 'DC']],
            
            # Other jurisdictions (territories, government, Canadian, DC)
            'other_jurisdictions': ['AS', 'GU', 'MP', 'PR', 'VI', 'GS', 'ON', 'AB', 'DC']
        }
        
        # Initialize the panel
        self.setup_panel()
        
    def setup_panel(self):
        """Create tiny state selection panel for top-left positioning"""
        # Main container with border for visibility
        self.main_frame = self.widget_factory.create_frame(self.parent, padding="2")
        self.main_frame.configure(relief='solid', borderwidth=1)
        self.main_frame.pack(fill='x', padx=2, pady=2)
        
        # Create inner container with tiny size
        self.inner_frame = self.widget_factory.create_frame(self.main_frame)
        self.inner_frame.pack(anchor='nw', fill='x', padx=2, pady=2)  # Fill x to ensure visibility
        
        # Create unified button grid with all jurisdictions
        self._create_unified_grid()
        
        # Bind resize event for responsive behavior (minimal handling needed with fixed sizing)
        self.main_frame.bind('<Configure>', self._on_window_resize)
        
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
        
        # Add all states (excluding DC)
        states_only = [
            (code, name) for code, name in self.states_data.items() 
            if code not in ['AS', 'GU', 'MP', 'PR', 'VI', 'GS', 'ON', 'AB', 'DC']
        ]
        all_jurisdictions.extend(states_only)
        
        # Add other jurisdictions at the end (including DC - keeping purple color to identify as "others")
        others = [
            (code, name) for code, name in self.states_data.items()
            if code in ['AS', 'GU', 'MP', 'PR', 'VI', 'GS', 'ON', 'AB', 'DC']
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
            
            # Create button with responsive sizing (smaller for windowed mode)
            button = ttk.Button(
                parent,
                text=code,  # Only show state code - clean and compact
                style=style,
                width=4,  # Reduced from 6 to 4 for better windowed mode appearance
                command=lambda state_code=code: self._handle_state_selection(state_code)
            )
            
            # Grid with consistent 1px spacing all around
            button.grid(row=row, column=column, padx=1, pady=1, sticky='ew')
            
            # Store button reference
            self.state_buttons[code] = button
            
        # Configure columns for consistent spacing and sizing
        for col in range(columns):
            parent.grid_columnconfigure(col, weight=1, uniform="button")
            
    def _handle_state_selection(self, state_code: str):
        """Handle state button click"""
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
            self.on_state_selected(state_code, state_name)
            
    def highlight_state(self, state_code: str):
        """Highlight a specific state button"""
        if state_code in self.state_buttons:
            print(f"Highlighting: {state_code}")
    
    def clear_state_selection(self):
        """Clear any state button highlighting/selection"""
        print("🎨 Clearing state button highlighting")
        # Reset all buttons to their default colors based on their category
        for state_code, button in self.state_buttons.items():
            # Determine color based on state category
            if state_code == 'FL':
                button.config(background='#ff6600')  # Orange for Florida
            elif state_code in ['GA', 'SC', 'NC', 'TN', 'MS', 'AL']:
                button.config(background='#4caf50')  # Green for FL-adjacent
            elif state_code in ['Government Service', 'Ontario', 'Alberta']:
                button.config(background='#9c27b0')  # Purple for other jurisdictions
            else:
                button.config(background='#808080')  # Gray for other states
            
    def get_main_frame(self) -> tk.Widget:
        """Get the main panel frame"""
        return self.main_frame