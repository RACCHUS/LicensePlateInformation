"""
Comprehensive License Plate Information System
Multi-panel interface with state selection, search, and information display
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gui.themes.theme_manager import ThemeManager
from gui.utils.widget_factory import WidgetFactory
from gui.components.state_selection.state_selector import StateSelectionPanel
from gui.components.search.search_bar import SearchBar
from gui.components.plate_type.plate_type_dropdown import SmartPlateTypeDropdown
from gui.components.info_display.state_info_panel import StateInfoPanel
from gui.components.info_display.plate_info_panel import PlateInfoPanel
from gui.components.info_display.char_rules_panel import CharacterRulesPanel
from gui.components.font_display.character_font_panel import CharacterFontPanel
from gui.utils.json_search_engine import JSONSearchEngine
from gui.components.image_display.image_viewer import PlateImageViewer


class LicensePlateApp:
    """Main application with comprehensive multi-panel interface"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("License Plate Information System")
        self.root.geometry("1400x900")
        
        # Initialize theme and widget factory
        style = ttk.Style()
        self.theme = ThemeManager(style)
        self.theme.initialize(self.root)
        self.widget_factory = WidgetFactory(self.theme)
        
        # Initialize search engine
        self.search_engine = JSONSearchEngine()
        
        # Current selections
        self.current_state = None
        self.current_plate_type = None
        
        self.setup_interface()
        
    def setup_interface(self):
        """Create the main interface layout"""
        # Main container
        main_container = tk.Frame(self.root, bg='#1a1a1a')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Top section: Search/Plate Type (left) and State Selection (right) side by side
        top_section = tk.Frame(main_container, bg='#1a1a1a')
        top_section.pack(fill='both', pady=(0, 10))
        
        # Left column: Search bar + Plate Type (stacked, matches state panel height)
        left_column = tk.Frame(top_section, bg='#1a1a1a')
        left_column.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Search section (no title to save space)
        self.search_bar = SearchBar(left_column, self.widget_factory, 
                                   on_search=self.on_search)
        
        # Plate Type section (no title to save space)
        self.plate_type_panel = SmartPlateTypeDropdown(left_column, self.widget_factory,
                                                      on_plate_type_selected=self.on_plate_type_selected,
                                                      on_states_with_type_updated=self.on_states_with_type_updated)
        
        # Right column: State selection panel  
        state_column = tk.Frame(top_section, bg='#1a1a1a')
        state_column.pack(side='right', fill='both', expand=True)
        
        state_header_frame = tk.Frame(state_column, bg='#1a1a1a')
        state_header_frame.pack(fill='x')
        
        state_label = tk.Label(
            state_header_frame, 
            text="State Selection", 
            bg='#1a1a1a', 
            fg='#ffffff', 
            font=('Segoe UI', 10, 'bold')
        )
        state_label.pack(side='left', pady=(0, 2))
        
        # Clear state filter button
        clear_state_btn = tk.Button(
            state_header_frame,
            text="Clear Filter",
            bg='#404040',
            fg='#ffffff',
            font=('Segoe UI', 8),
            relief='solid',
            borderwidth=1,
            command=self.clear_state_filter
        )
        clear_state_btn.pack(side='right', pady=(0, 2))
        
        self.state_panel = StateSelectionPanel(state_column, self.widget_factory, 
                                             on_state_selected=self.on_state_selected)
        
        # Middle section: Search Results (left) and Image Display (right)
        middle_section = tk.Frame(main_container, bg='#1a1a1a')
        middle_section.pack(fill='both', expand=True, pady=(5, 5))
        
        # Left: Search Results
        search_results_column = tk.Frame(middle_section, bg='#1a1a1a')
        search_results_column.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        search_results_label = tk.Label(
            search_results_column, 
            text="Search Results", 
            bg='#1a1a1a', 
            fg='#ffffff', 
            font=('Segoe UI', 10, 'bold')
        )
        search_results_label.pack(anchor='w', pady=(0, 2))
        
        self.search_results_panel = self._create_search_results_panel(search_results_column)
        
        # Right: Image Display
        image_column = tk.Frame(middle_section, bg='#1a1a1a')
        image_column.pack(side='right', fill='both', expand=True)
        
        image_label = tk.Label(
            image_column, 
            text="License Plate Images", 
            bg='#1a1a1a', 
            fg='#ffffff', 
            font=('Segoe UI', 10, 'bold')
        )
        image_label.pack(anchor='w', pady=(0, 2))
        
        # Image viewer with navigation
        self.image_viewer = PlateImageViewer(image_column)
        self.image_viewer.get_frame().pack(fill='both', expand=True)
        
        # Bottom section: Information Panels (4 columns for better space usage)
        info_section = tk.Frame(main_container, bg='#1a1a1a')
        info_section.pack(fill='both', expand=True)
        
        # Column 1: State Information (compact)
        state_info_column = tk.Frame(info_section, bg='#1a1a1a')
        state_info_column.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        state_info_label = tk.Label(
            state_info_column, 
            text="State Information", 
            bg='#1a1a1a', 
            fg='#ffffff', 
            font=('Segoe UI', 10, 'bold')
        )
        state_info_label.pack(anchor='w', pady=(0, 2))
        
        # Scrollable state info
        state_info_scroll_frame = tk.Frame(state_info_column, bg='#2a2a2a', relief='solid', borderwidth=1)
        state_info_scroll_frame.pack(fill='both', expand=True)
        
        state_info_canvas = tk.Canvas(state_info_scroll_frame, bg='#2a2a2a', highlightthickness=0)
        state_info_scrollbar = tk.Scrollbar(state_info_scroll_frame, orient='vertical', command=state_info_canvas.yview)
        self.state_info_scrollable_frame = tk.Frame(state_info_canvas, bg='#2a2a2a')
        
        self.state_info_scrollable_frame.bind(
            "<Configure>",
            lambda e: self._configure_scroll_region(state_info_canvas, state_info_scrollbar)
        )
        
        state_info_canvas.create_window((0, 0), window=self.state_info_scrollable_frame, anchor="nw")
        state_info_canvas.configure(yscrollcommand=state_info_scrollbar.set)
        
        state_info_canvas.pack(side="left", fill="both", expand=True)
        
        self.state_info_panel = StateInfoPanel(self.state_info_scrollable_frame, self.widget_factory)
        
        # Column 2: Plate Type Information (compact)
        plate_info_column = tk.Frame(info_section, bg='#1a1a1a')
        plate_info_column.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        plate_info_label = tk.Label(
            plate_info_column, 
            text="Plate Type Information", 
            bg='#1a1a1a', 
            fg='#ffffff', 
            font=('Segoe UI', 10, 'bold')
        )
        plate_info_label.pack(anchor='w', pady=(0, 2))
        
        # Scrollable plate info
        plate_info_scroll_frame = tk.Frame(plate_info_column, bg='#2a2a2a', relief='solid', borderwidth=1)
        plate_info_scroll_frame.pack(fill='both', expand=True)
        
        plate_info_canvas = tk.Canvas(plate_info_scroll_frame, bg='#2a2a2a', highlightthickness=0)
        plate_info_scrollbar = tk.Scrollbar(plate_info_scroll_frame, orient='vertical', command=plate_info_canvas.yview)
        self.plate_info_scrollable_frame = tk.Frame(plate_info_canvas, bg='#2a2a2a')
        
        self.plate_info_scrollable_frame.bind(
            "<Configure>",
            lambda e: self._configure_scroll_region(plate_info_canvas, plate_info_scrollbar)
        )
        
        plate_info_canvas.create_window((0, 0), window=self.plate_info_scrollable_frame, anchor="nw")
        plate_info_canvas.configure(yscrollcommand=plate_info_scrollbar.set)
        
        plate_info_canvas.pack(side="left", fill="both", expand=True)
        
        self.plate_info_panel = PlateInfoPanel(self.plate_info_scrollable_frame, self.widget_factory)
        
        # Column 3: Character Handling Rules
        char_rules_column = tk.Frame(info_section, bg='#1a1a1a')
        char_rules_column.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        char_rules_label = tk.Label(
            char_rules_column, 
            text="Character Handling Rules", 
            bg='#1a1a1a', 
            fg='#ffffff', 
            font=('Segoe UI', 10, 'bold')
        )
        char_rules_label.pack(anchor='w', pady=(0, 2))
        
        self.char_rules_panel = CharacterRulesPanel(char_rules_column, self.widget_factory)
        
        # Column 4: Character Font Preview
        font_column = tk.Frame(info_section, bg='#1a1a1a')
        font_column.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        font_preview_label = tk.Label(
            font_column, 
            text="Character Font Preview", 
            bg='#1a1a1a', 
            fg='#ffffff', 
            font=('Segoe UI', 10, 'bold')
        )
        font_preview_label.pack(anchor='w', pady=(0, 2))
        
        # Use CharacterFontPanel component
        self.character_font_panel = CharacterFontPanel(font_column, self.widget_factory)
    
    def _create_search_results_panel(self, parent):
        """Create search results panel"""
        # Main frame with border
        main_frame = tk.Frame(
            parent,
            bg='#2a2a2a',
            relief='solid',
            borderwidth=1
        )
        main_frame.pack(fill='both', expand=True)
        
        # Scrollable results area
        results_canvas = tk.Canvas(main_frame, bg='#2a2a2a', highlightthickness=0)
        results_scrollbar = tk.Scrollbar(main_frame, orient='vertical', command=results_canvas.yview)
        self.search_results_scrollable_frame = tk.Frame(results_canvas, bg='#2a2a2a')
        
        self.search_results_scrollable_frame.bind(
            "<Configure>",
            lambda e: self._configure_scroll_region(results_canvas, results_scrollbar)
        )
        
        results_canvas.create_window((0, 0), window=self.search_results_scrollable_frame, anchor="nw")
        results_canvas.configure(yscrollcommand=results_scrollbar.set)
        
        results_canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        # Scrollbar will be managed by _configure_scroll_region
        
        # Default content
        self.search_results_content = tk.Label(
            self.search_results_scrollable_frame,
            text="Enter a search term to see results\\n\\nResults will show:\\n• States where term is found\\n• Plate types containing term\\n• Organized by state",
            bg='#2a2a2a',
            fg='#888888',
            font=('Segoe UI', 9),
            justify='left',
            anchor='nw'
        )
        self.search_results_content.pack(fill='both', expand=True, padx=10, pady=10)
        
        return main_frame
    
    def update_search_results(self, search_term, results):
        """Update search results panel with search findings"""
        # Clear existing content
        for widget in self.search_results_scrollable_frame.winfo_children():
            widget.destroy()
        
        if not results or not search_term:
            # Show default message
            self.search_results_content = tk.Label(
                self.search_results_scrollable_frame,
                text="Enter a search term to see results\\n\\nResults will show:\\n• States where term is found\\n• Plate types containing term\\n• Organized by state",
                bg='#2a2a2a',
                fg='#888888',
                font=('Segoe UI', 9),
                justify='left',
                anchor='nw'
            )
            self.search_results_content.pack(fill='both', expand=True, padx=10, pady=10)
            return
        
        # Title
        title_label = tk.Label(
            self.search_results_scrollable_frame,
            text=f"Search Results for: '{search_term}'",
            bg='#2a2a2a',
            fg='#ffffff',
            font=('Segoe UI', 10, 'bold')
        )
        title_label.pack(anchor='w', padx=10, pady=(10, 5))
        
        # Group results by state
        states_with_results = {}
        for result in results:
            state = result.get('state', 'Unknown')
            if state not in states_with_results:
                states_with_results[state] = []
            states_with_results[state].append(result)
        
        # Display results by state
        for state, state_results in states_with_results.items():
            # State header
            state_frame = tk.Frame(self.search_results_scrollable_frame, bg='#2a2a2a')
            state_frame.pack(fill='x', padx=10, pady=(5, 0))
            
            state_label = tk.Label(
                state_frame,
                text=f"🏛️ {state} ({len(state_results)} results)",
                bg='#2a2a2a',
                fg='#4CAF50',
                font=('Segoe UI', 9, 'bold')
            )
            state_label.pack(anchor='w')
            
            # Show individual results with field information
            for result in state_results:
                result_frame = tk.Frame(state_frame, bg='#2a2a2a')
                result_frame.pack(fill='x', padx=20, pady=1)
                
                # Field where match was found
                field_name = result.get('field', 'Unknown')
                field_value = result.get('value', '')
                
                if 'plate_type' in result:
                    match_text = f"📋 {result['plate_type']} - {field_name}: {field_value}"
                else:
                    match_text = f"🔍 {field_name}: {field_value}"
                
                match_label = tk.Label(
                    result_frame,
                    text=match_text,
                    bg='#2a2a2a',
                    fg='#81C784',
                    font=('Segoe UI', 8),
                    wraplength=400,
                    anchor='w',
                    justify='left'
                )
                match_label.pack(anchor='w')
        
        print(f"🔍 Updated search results for '{search_term}' - {len(results)} total results")
    
    def on_state_selected(self, state_code: str, state_name: str):
        """Handle state selection"""
        self.current_state = state_code
        
        # Update state information panel
        self.state_info_panel.update_state_info(state_code)
        
        # Update search bar to filter by state
        self.search_bar.set_state_filter(state_code, state_name)
        
        # Filter plate types to this state only
        self.plate_type_panel.set_state_filter(state_code)
        
        # Update character rules panel
        self.char_rules_panel.update_rules(state_code)
        
        # Update character font preview
        self.character_font_panel.update_state(state_code, state_name)
        
        # Update image viewer with state images
        self.image_viewer.update_state(state_code)
            
    def on_plate_type_selected(self, plate_type: str):
        """Handle plate type selection"""
        self.current_plate_type = plate_type
        
        # Update plate information panel
        self.plate_info_panel.update_plate_info(plate_type, self.current_state)
        
        # Update image viewer if state is also selected
        if self.current_state:
            self.image_viewer.update_state(self.current_state, plate_type)
            
    def clear_state_filter(self):
        """Clear the current state filter"""
        print("🧹 Clear State Filter button clicked")
        self.current_state = None
        
        # Reset plate type filter to show all types
        self.plate_type_panel.set_state_filter(None)
        
        # Also clear any plate type selection
        self.plate_type_panel.plate_type_var.set("Select plate type...")
        self.plate_type_panel.selected_plate_type = None
        
        # Clear state info panel
        self.state_info_panel.clear_info()
        
        # Clear search bar state filter indicator
        self.search_bar.clear_state_filter()
        
        # Clear character rules panel
        self.char_rules_panel.update_rules(None)
        
        # Clear character font preview
        self.character_font_panel.clear()
        
        # Clear search results
        self.update_search_results("", [])
        
        # Clear image viewer
        self.image_viewer.clear()
        
        # Clear any visual state selection (reset button colors)
        self._reset_state_button_colors()
        
        print("✅ State filter, plate type selection, and search state cleared - showing all 288 plate types")
    
    def _reset_state_button_colors(self):
        """Reset all state button colors to default"""
        print("🎨 Resetting state button colors")
        if hasattr(self.state_panel, 'clear_state_selection'):
            self.state_panel.clear_state_selection()
        else:
            print("⚠️ Warning: State panel doesn't have clear_state_selection method")
        
    def on_states_with_type_updated(self, states_with_type: list):
        """Handle when plate type shows which states have it"""
        if states_with_type:
            # TODO: Highlight these states in the state panel
            print(f"🎯 Plate type available in: {', '.join(states_with_type)}")
        else:
            # TODO: Clear state highlighting
            print("🔍 No states highlighted")
    
    def on_search(self, search_params: dict):
        """Handle search query"""
        query = search_params.get('query', '')
        category = search_params.get('category', 'all')
        
        if not query.strip():
            self.update_search_results("", [])
            return
            
        print(f"🔍 Search: '{query}' in category '{category}' with state filter: {self.current_state}")
        
        # Perform real search using the JSON search engine
        try:
            search_results = self.search_engine.search(
                query=query,
                category=category,
                state_filter=self.current_state
            )
            
            # Transform search results to include field information
            formatted_results = []
            for result in search_results:
                # Each result should have state, field, value, and possibly plate_type
                formatted_result = {
                    'state': result.get('state', 'Unknown'),
                    'field': result.get('field', 'Unknown'),
                    'value': result.get('value', ''),
                    'match_type': result.get('match_type', 'text')
                }
                
                # Add plate type if it exists in the result
                if 'plate_type' in result:
                    formatted_result['plate_type'] = result['plate_type']
                
                formatted_results.append(formatted_result)
            
            print(f"🔍 Found {len(formatted_results)} results for '{query}'")
            
        except Exception as e:
            print(f"❌ Search error: {e}")
            # Fallback to show search attempt
            formatted_results = []
        
        # Update the search results panel
        self.update_search_results(query, formatted_results)
        
    def run(self):
        """Start the application"""
        self.root.mainloop()
    
    def _configure_scroll_region(self, canvas, scrollbar):
        """Configure scroll region and show/hide scrollbar as needed."""
        canvas.configure(scrollregion=canvas.bbox("all"))
        
        # Get canvas and content dimensions
        canvas.update_idletasks()
        canvas_height = canvas.winfo_height()
        content_height = canvas.bbox("all")[3] if canvas.bbox("all") else 0
        
        # Show/hide scrollbar based on content size
        if content_height > canvas_height:
            scrollbar.pack(side="right", fill="y")
        else:
            scrollbar.pack_forget()


def main():
    """Entry point for the application"""
    try:
        app = LicensePlateApp()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()