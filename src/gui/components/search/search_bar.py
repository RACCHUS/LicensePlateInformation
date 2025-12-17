"""
Advanced Search Bar Component - JSON field search with category filtering
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional, List, Dict, Any

from ...utils.widget_factory import WidgetFactory
from ....utils.logger import log_error, log_warning


class SearchBar:
    """Advanced search component for searching JSON data by category"""
    
    def __init__(self, parent: tk.Widget, widget_factory: WidgetFactory,
                 on_search: Optional[Callable] = None):
        self.parent = parent
        self.widget_factory = widget_factory
        self.on_search = on_search
        self.search_history: List[str] = []
        self.current_search = tk.StringVar()
        self.selected_category = tk.StringVar()
        self.selected_state = None  # Will be set by state button selection
        
        # Define searchable categories (easily expandable)
        self.search_categories = {
            'all': 'All Fields',
            'fonts': 'Fonts',
            'slogans': 'Slogans', 
            'colors': 'Colors',
            'logos': 'Logos',
            'text': 'Plate Text',
            'background': 'Background',
            'design': 'Design Elements',
            'year': 'Year/Period',
            'type': 'Plate Type',
            'handling_rules': 'Character Handling Rules',
            'processing': 'Processing Rules',
            'restrictions': 'Character Restrictions'
        }
        
        # Setup the search bar
        self.setup_search_bar()
        
    def setup_search_bar(self):
        """Create the advanced search bar interface"""
        # Main container with border
        self.main_frame = self.widget_factory.create_frame(self.parent)
        self.main_frame.configure(relief='solid', borderwidth=1)
        self.main_frame.pack(fill='x', padx=4, pady=4)
        
        # Inner container for layout
        self.inner_frame = self.widget_factory.create_frame(self.main_frame)
        self.inner_frame.pack(fill='x', padx=6, pady=6)
        
        # Search controls row
        controls_row = self.widget_factory.create_frame(self.inner_frame)
        controls_row.pack(fill='x', pady=2)
        
        # Category selector
        category_frame = self.widget_factory.create_frame(controls_row)
        category_frame.pack(side='left', padx=(0, 8))
        
        category_label = self.widget_factory.create_label(
            category_frame, 
            "Search In:", 
            style='TLabel'
        )
        category_label.pack(anchor='w')
        
        self.category_combobox = ttk.Combobox(
            category_frame,
            textvariable=self.selected_category,
            values=list(self.search_categories.values()),
            state='readonly',
            width=12,
            style='TCombobox'
        )
        self.category_combobox.pack()
        self.category_combobox.set('All Fields')
        self.category_combobox.bind('<<ComboboxSelected>>', self._on_category_changed)
        
        # Search scope selector
        scope_frame = self.widget_factory.create_frame(controls_row)
        scope_frame.pack(side='left', padx=8)
        
        scope_label = self.widget_factory.create_label(
            scope_frame,
            "Search Scope:",
            style='TLabel'
        )
        scope_label.pack(anchor='w')
        
        self.search_scope_var = tk.StringVar(value="all")
        
        scope_button_frame = self.widget_factory.create_frame(scope_frame)
        scope_button_frame.pack()
        
        self.scope_current_radio = ttk.Radiobutton(
            scope_button_frame,
            text="Current State",
            variable=self.search_scope_var,
            value="current",
            state='disabled'
        )
        self.scope_current_radio.pack(side='left', padx=2)
        
        self.scope_all_radio = ttk.Radiobutton(
            scope_button_frame,
            text="All States",
            variable=self.search_scope_var,
            value="all"
        )
        self.scope_all_radio.pack(side='left', padx=2)
        
        # Main search input
        search_input_frame = self.widget_factory.create_frame(controls_row)
        search_input_frame.pack(side='left', fill='x', expand=True, padx=8)
        
        input_label = self.widget_factory.create_label(
            search_input_frame, 
            "Search Terms:", 
            style='TLabel'
        )
        input_label.pack(anchor='w')
        
        self.search_entry = ttk.Entry(
            search_input_frame,
            textvariable=self.current_search,
            font=('Segoe UI', 10),
            style='TEntry'
        )
        self.search_entry.pack(fill='x')
        self.search_entry.bind('<Return>', self._on_search_enter)
        self.search_entry.bind('<KeyRelease>', self._on_search_change)
        
        # Search button
        button_frame = self.widget_factory.create_frame(controls_row)
        button_frame.pack(side='right', padx=(8, 0))
        
        button_spacer = self.widget_factory.create_label(button_frame, " ", style='TLabel')
        button_spacer.pack()
        
        self.search_button = ttk.Button(
            button_frame,
            text="Search",
            command=self._perform_search,
            style='TButton',
            width=10
        )
        self.search_button.pack()
        
        # State filter indicator (shows when state is selected)
        self.state_indicator_frame = self.widget_factory.create_frame(self.inner_frame)
        # Initially hidden
        
        self.state_indicator_label = self.widget_factory.create_label(
            self.state_indicator_frame,
            "",
            style='Status.TLabel'
        )
        self.state_indicator_label.pack(anchor='w')
        
        # Search suggestions (initially hidden)
        self.suggestions_frame = self.widget_factory.create_frame(self.inner_frame)
        
    def _on_search_enter(self, event):
        """Handle Enter key in search field"""
        try:
            self._perform_search()
        except Exception as e:
            log_error("Error handling search enter", exc=e)
        
    def _on_search_change(self, event):
        """Handle search text changes for suggestions"""
        try:
            search_text = self.current_search.get().strip()
            if len(search_text) >= 2:
                self._show_suggestions(search_text)
            else:
                self._hide_suggestions()
        except Exception as e:
            log_error("Error handling search change", exc=e)
            
    def _on_category_changed(self, event):
        """Handle category selection changes"""
        category_display = self.selected_category.get()
        category_key = self._get_category_key(category_display)
        
        # Update placeholder text based on category
        placeholders = {
            'all': 'Search all fields...',
            'fonts': 'e.g., Arial, Times New Roman, Custom Font',
            'slogans': 'e.g., "Sunshine State", "The Natural State"',
            'colors': 'e.g., blue, red, white, rainbow',
            'logos': 'e.g., palm tree, mountain, star',
            'text': 'e.g., "Florida", numbers, letters',
            'background': 'e.g., gradient, solid, pattern',
            'design': 'e.g., border, graphics, artwork',
            'year': 'e.g., 2020, 1990s, current',
            'type': 'e.g., standard, specialty, vanity',
            'handling_rules': 'e.g., O vs 0, stacked, X2, omit, include',
            'processing': 'e.g., vertical, standard, digital processing',
            'restrictions': 'e.g., does not allow, must use, restrictions'
        }
        
        # Visual feedback for category change
        print(f"🎯 Search category changed to: {category_display}")
        
    def _perform_search(self):
        """Execute comprehensive JSON search"""
        try:
            search_text = self.current_search.get().strip()
            category_display = self.selected_category.get()
            category_key = self._get_category_key(category_display)
            
            if search_text:
                # Add to search history
                if search_text not in self.search_history:
                    self.search_history.insert(0, search_text)
                    self.search_history = self.search_history[:10]  # Keep last 10
                
                # Build search parameters
                # Only use state filter if scope is 'current' and a state is selected
                state_filter = self.selected_state if (self.search_scope_var.get() == 'current' and self.selected_state) else None
                
                search_params = {
                    'query': search_text,
                    'category': category_key,
                    'state_filter': state_filter,
                    'search_scope': self.search_scope_var.get(),
                    'search_type': 'json_field_search'
                }
                
                # Log search for debugging
                state_info = f" in {self.selected_state}" if self.selected_state else " (all states)"
                print(f"🔍 Searching '{search_text}' in {category_display}{state_info}")
                
                if self.on_search:
                    try:
                        self.on_search(search_params)
                    except Exception as e:
                        log_error(f"Search callback failed for query: {search_text}", exc=e)
        except Exception as e:
            log_error("Error performing search", exc=e)
                
    def _get_category_key(self, category_display: str) -> str:
        """Get category key from display name"""
        for key, display in self.search_categories.items():
            if display == category_display:
                return key
        return 'all'
        
    def _show_suggestions(self, search_text: str):
        """Show contextual search suggestions"""
        category_key = self._get_category_key(self.selected_category.get())
        
        # Category-specific suggestions
        suggestions = []
        if category_key == 'colors':
            color_suggestions = ['blue', 'red', 'white', 'green', 'yellow', 'black', 'rainbow']
            suggestions = [c for c in color_suggestions if search_text.lower() in c.lower()]
        elif category_key == 'fonts':
            font_suggestions = ['Arial', 'Times New Roman', 'Helvetica', 'Georgia', 'Custom']
            suggestions = [f for f in font_suggestions if search_text.lower() in f.lower()]
        elif category_key == 'slogans':
            # Add from search history that were slogans
            suggestions = [item for item in self.search_history if search_text.lower() in item.lower()]
        else:
            # General suggestions from history
            suggestions = [item for item in self.search_history if search_text.lower() in item.lower()]
        
        if suggestions:
            self.suggestions_frame.pack(fill='x', pady=(4, 0))
            
            # Clear existing suggestions
            for widget in self.suggestions_frame.winfo_children():
                widget.destroy()
                
            # Add suggestion buttons
            for suggestion in suggestions[:5]:  # Show max 5
                suggestion_btn = ttk.Button(
                    self.suggestions_frame,
                    text=f"💡 {suggestion}",
                    command=lambda s=suggestion: self._select_suggestion(s),
                    style='TButton'
                )
                suggestion_btn.pack(fill='x', pady=1)
        else:
            self._hide_suggestions()
            
    def _hide_suggestions(self):
        """Hide search suggestions"""
        self.suggestions_frame.pack_forget()
        
    def _select_suggestion(self, suggestion: str):
        """Select a search suggestion"""
        self.current_search.set(suggestion)
        self._hide_suggestions()
        self._perform_search()
        
    def set_state_filter(self, state_code: str, state_name: str):
        """Set state filter from state button selection"""
        self.selected_state = state_code
        
        # Enable "Current State" radio button
        self.scope_current_radio.config(state='normal')
        # Set scope to current state by default
        self.search_scope_var.set('current')
        
        # Show state filter indicator
        self.state_indicator_frame.pack(fill='x', pady=(4, 0))
        self._update_state_indicator(state_code, state_name)
        
        print(f"🎯 State filter set to: {state_code} - {state_name}")
    
    def _update_state_indicator(self, state_code: Optional[str] = None, state_name: Optional[str] = None):
        """Update state indicator text based on search scope"""
        if not state_code:
            state_code = self.selected_state or ""
        if not state_name:
            # Would need to look up state name - for now use code
            state_name = state_code
        
        if self.selected_state and self.search_scope_var.get() == 'current':
            indicator_text = f"🔍 Searching in: {state_code} - {state_name}"
        elif self.selected_state and self.search_scope_var.get() == 'all':
            indicator_text = f"� Searching all states (State selected: {state_code})"
        else:
            indicator_text = "🌍 Searching all states"
        
        self.state_indicator_label.config(text=indicator_text)
        
    def add_search_category(self, key: str, display_name: str):
        """Add new search category (for easy expansion)"""
        self.search_categories[key] = display_name
        
        # Update combobox values
        self.category_combobox['values'] = list(self.search_categories.values())
        
        print(f"➕ Added search category: {display_name}")
        
    def focus_search(self):
        """Focus the search input field"""
        self.search_entry.focus_set()
        
    def clear_search(self):
        """Clear the search input"""
        self.current_search.set('')
        self._hide_suggestions()
        
    def clear_state_filter(self):
        """Clear the state filter indicator"""
        self.selected_state = None
        # Disable "Current State" radio button and set to "All States"
        self.scope_current_radio.config(state='disabled')
        self.search_scope_var.set('all')
        self.state_indicator_frame.pack_forget()
        print("🔄 Search state filter cleared")
        
    def get_main_frame(self) -> tk.Widget:
        """Get the main search bar frame"""
        return self.main_frame