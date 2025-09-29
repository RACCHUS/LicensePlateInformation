"""
Main window for License Plate Information System
Provides fast state lookup and plate information display
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
from typing import List, Dict, Optional
import json
import os
from PIL import Image, ImageTk

from database.db_manager import DatabaseManager

class MainWindow:
    """Main application window for license plate lookup"""
    
    def __init__(self, root: tk.Tk, db_manager: DatabaseManager):
        """Initialize main window
        
        Args:
            root: Tkinter root window
            db_manager: Database manager instance
        """
        self.root = root
        self.db_manager = db_manager
        self.current_state = None
        self.current_plate_types = []
        
        self._setup_window()
        self._create_widgets()
        self._setup_bindings()
        
        # Focus on search entry for immediate use
        self.search_entry.focus_set()
    
    def _setup_window(self):
        """Configure main window properties"""
        self.root.title("License Plate Information System - Toll Reader")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Custom colors for toll reading interface
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Info.TLabel', font=('Arial', 10))
        style.configure('Search.TEntry', font=('Arial', 14))
        style.configure('Quick.TButton', font=('Arial', 10, 'bold'))
    
    def _create_widgets(self):
        """Create and layout all widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky='nsew')
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="License Plate Information System", 
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Search section
        self._create_search_section(main_frame)
        
        # Main content area (split into three columns)
        self._create_content_area(main_frame)
        
        # Status bar
        self._create_status_bar(main_frame)
    
    def _create_search_section(self, parent):
        """Create search input section"""
        search_frame = ttk.Frame(parent)
        search_frame.grid(row=1, column=0, columnspan=3, sticky='ew', pady=(0, 10))
        search_frame.columnconfigure(1, weight=1)
        
        # Search label
        ttk.Label(search_frame, text="State Search:", style='Header.TLabel').grid(
            row=0, column=0, padx=(0, 10), sticky=tk.W)
        
        # Search entry
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, 
                                     style='Search.TEntry', width=40)
        self.search_entry.grid(row=0, column=1, padx=(0, 10), sticky='ew')
        
        # Quick buttons for common states
        quick_frame = ttk.Frame(search_frame)
        quick_frame.grid(row=0, column=2, sticky=tk.E)
        
        common_states = [('FL', 'Florida'), ('GA', 'Georgia'), ('AL', 'Alabama'), 
                        ('SC', 'South Carolina'), ('NC', 'North Carolina')]
        
        for i, (abbrev, name) in enumerate(common_states):
            btn = ttk.Button(quick_frame, text=abbrev, width=4, style='Quick.TButton',
                           command=lambda a=abbrev: self._quick_search(a))
            btn.grid(row=0, column=i, padx=2)
    
    def _create_content_area(self, parent):
        """Create main content area with three panels"""
        content_frame = ttk.Frame(parent)
        content_frame.grid(row=2, column=0, columnspan=3, sticky='nsew')
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        content_frame.columnconfigure(2, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        # Left panel - State information
        self._create_state_panel(content_frame)
        
        # Middle panel - Plate types
        self._create_plate_types_panel(content_frame)
        
        # Right panel - Character references
        self._create_character_panel(content_frame)
    
    def _create_state_panel(self, parent):
        """Create state information panel"""
        state_frame = ttk.LabelFrame(parent, text="State Information", padding="10")
        state_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 5))
        state_frame.columnconfigure(0, weight=1)
        state_frame.rowconfigure(1, weight=1)
        
        # State basic info frame
        info_frame = ttk.Frame(state_frame)
        info_frame.grid(row=0, column=0, sticky='ew', pady=(0, 10))
        info_frame.columnconfigure(1, weight=1)
        
        # State name and abbreviation
        self.state_name_var = tk.StringVar(value="Select a state...")
        ttk.Label(info_frame, textvariable=self.state_name_var, 
                 style='Header.TLabel').grid(row=0, column=0, columnspan=2, sticky=tk.W)
        
        # Character usage info
        char_info_frame = ttk.LabelFrame(state_frame, text="Character Rules", padding="5")
        char_info_frame.grid(row=1, column=0, sticky='nsew', pady=(0, 10))
        char_info_frame.columnconfigure(1, weight=1)
        
        # 0 vs O usage
        ttk.Label(char_info_frame, text="Uses 0 (zero):").grid(row=0, column=0, sticky=tk.W)
        self.uses_zero_var = tk.StringVar(value="--")
        ttk.Label(char_info_frame, textvariable=self.uses_zero_var, 
                 style='Info.TLabel').grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(char_info_frame, text="Uses O (letter):").grid(row=1, column=0, sticky=tk.W)
        self.uses_o_var = tk.StringVar(value="--")
        ttk.Label(char_info_frame, textvariable=self.uses_o_var, 
                 style='Info.TLabel').grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(char_info_frame, text="Zero is slashed:").grid(row=2, column=0, sticky=tk.W)
        self.zero_slashed_var = tk.StringVar(value="--")
        ttk.Label(char_info_frame, textvariable=self.zero_slashed_var, 
                 style='Info.TLabel').grid(row=2, column=1, sticky=tk.W, padx=(10, 0))
        
        # Visual info
        visual_frame = ttk.LabelFrame(state_frame, text="Visual Information", padding="5")
        visual_frame.grid(row=2, column=0, sticky='nsew')
        visual_frame.columnconfigure(1, weight=1)
        
        ttk.Label(visual_frame, text="Colors:").grid(row=0, column=0, sticky=tk.W)
        self.colors_var = tk.StringVar(value="--")
        ttk.Label(visual_frame, textvariable=self.colors_var, 
                 style='Info.TLabel').grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(visual_frame, text="Slogan:").grid(row=1, column=0, sticky=tk.W)
        self.slogan_var = tk.StringVar(value="--")
        ttk.Label(visual_frame, textvariable=self.slogan_var, 
                 style='Info.TLabel').grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        
        # Notes
        notes_frame = ttk.LabelFrame(state_frame, text="Notes", padding="5")
        notes_frame.grid(row=3, column=0, sticky='nsew')
        notes_frame.columnconfigure(0, weight=1)
        notes_frame.rowconfigure(0, weight=1)
        
        self.notes_text = tk.Text(notes_frame, height=4, wrap=tk.WORD, 
                                 font=('Arial', 9), state=tk.DISABLED)
        notes_scroll = ttk.Scrollbar(notes_frame, orient=tk.VERTICAL, command=self.notes_text.yview)
        self.notes_text.configure(yscrollcommand=notes_scroll.set)
        
        self.notes_text.grid(row=0, column=0, sticky='nsew')
        notes_scroll.grid(row=0, column=1, sticky='ns')
    
    def _create_plate_types_panel(self, parent):
        """Create plate types panel"""
        types_frame = ttk.LabelFrame(parent, text="Plate Types", padding="10")
        types_frame.grid(row=0, column=1, sticky='nsew', padx=5)
        types_frame.columnconfigure(0, weight=1)
        types_frame.rowconfigure(0, weight=1)
        
        # Treeview for plate types
        columns = ('Type', 'Pattern', 'Colors', 'Stickers')
        self.plate_types_tree = ttk.Treeview(types_frame, columns=columns, show='headings', height=10)
        
        # Configure columns
        self.plate_types_tree.heading('Type', text='Type')
        self.plate_types_tree.heading('Pattern', text='Pattern')
        self.plate_types_tree.heading('Colors', text='Colors')
        self.plate_types_tree.heading('Stickers', text='Stickers')
        
        self.plate_types_tree.column('Type', width=100)
        self.plate_types_tree.column('Pattern', width=80)
        self.plate_types_tree.column('Colors', width=80)
        self.plate_types_tree.column('Stickers', width=60)
        
        # Scrollbar for treeview
        types_scroll = ttk.Scrollbar(types_frame, orient=tk.VERTICAL, 
                                   command=self.plate_types_tree.yview)
        self.plate_types_tree.configure(yscrollcommand=types_scroll.set)
        
        self.plate_types_tree.grid(row=0, column=0, sticky='nsew')
        types_scroll.grid(row=0, column=1, sticky='ns')
        
        # Plate type details
        details_frame = ttk.LabelFrame(types_frame, text="Selected Type Details", padding="5")
        details_frame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(10, 0))
        details_frame.columnconfigure(0, weight=1)
        
        self.type_details_text = tk.Text(details_frame, height=4, wrap=tk.WORD, 
                                        font=('Arial', 9), state=tk.DISABLED)
        self.type_details_text.grid(row=0, column=0, sticky='ew')
    
    def _create_character_panel(self, parent):
        """Create character reference panel"""
        char_frame = ttk.LabelFrame(parent, text="Character Reference", padding="10")
        char_frame.grid(row=0, column=2, sticky='nsew', padx=(5, 0))
        char_frame.columnconfigure(0, weight=1)
        char_frame.rowconfigure(1, weight=1)
        
        # Quick character lookup buttons
        quick_char_frame = ttk.Frame(char_frame)
        quick_char_frame.grid(row=0, column=0, sticky='ew', pady=(0, 10))
        
        ttk.Label(quick_char_frame, text="Quick Lookup:", style='Header.TLabel').grid(
            row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        # Common ambiguous characters
        ambiguous_chars = ['0', 'O', '1', 'I', 'L', '8', 'B', '5', 'S', '2', 'Z']
        char_buttons_frame = ttk.Frame(quick_char_frame)
        char_buttons_frame.grid(row=1, column=0, sticky='ew')
        
        for i, char in enumerate(ambiguous_chars):
            btn = ttk.Button(char_buttons_frame, text=char, width=3,
                           command=lambda c=char: self._show_character_info(c))
            btn.grid(row=i // 6, column=i % 6, padx=2, pady=2)
        
        # Character display area
        display_frame = ttk.LabelFrame(char_frame, text="Character Display", padding="5")
        display_frame.grid(row=1, column=0, sticky='nsew')
        display_frame.columnconfigure(0, weight=1)
        display_frame.rowconfigure(0, weight=1)
        
        # Character info display
        self.char_info_text = tk.Text(display_frame, wrap=tk.WORD, font=('Arial', 10),
                                     state=tk.DISABLED)
        char_scroll = ttk.Scrollbar(display_frame, orient=tk.VERTICAL, 
                                   command=self.char_info_text.yview)
        self.char_info_text.configure(yscrollcommand=char_scroll.set)
        
        self.char_info_text.grid(row=0, column=0, sticky='nsew')
        char_scroll.grid(row=0, column=1, sticky='ns')
    
    def _create_status_bar(self, parent):
        """Create status bar"""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=3, column=0, columnspan=3, sticky='ew', pady=(10, 0))
        status_frame.columnconfigure(0, weight=1)
        
        self.status_var = tk.StringVar(value="Ready - Type state name or abbreviation to search")
        ttk.Label(status_frame, textvariable=self.status_var, 
                 style='Info.TLabel').grid(row=0, column=0, sticky=tk.W)
        
        # Database info
        state_count = self.db_manager.get_state_count()
        info_text = f"Database: {state_count} states loaded"
        ttk.Label(status_frame, text=info_text, style='Info.TLabel').grid(
            row=0, column=1, sticky=tk.E)
    
    def _setup_bindings(self):
        """Setup event bindings"""
        # Search as you type
        self.search_var.trace('w', self._on_search_changed)
        
        # Enter key for search
        self.search_entry.bind('<Return>', self._on_search_enter)
        
        # Plate type selection
        self.plate_types_tree.bind('<<TreeviewSelect>>', self._on_plate_type_selected)
        
        # Escape to clear search
        self.root.bind('<Escape>', self._clear_search)
        
        # F1 for help
        self.root.bind('<F1>', self._show_help)
    
    def _on_search_changed(self, *args):
        """Handle search text changes"""
        search_term = self.search_var.get().strip()
        
        if len(search_term) >= 2:  # Start searching after 2 characters
            self._perform_search(search_term)
        elif len(search_term) == 0:
            self._clear_results()
    
    def _on_search_enter(self, event):
        """Handle Enter key in search"""
        search_term = self.search_var.get().strip()
        if search_term:
            self._perform_search(search_term, select_first=True)
    
    def _quick_search(self, state_abbrev: str):
        """Perform quick search for common state"""
        self.search_var.set(state_abbrev)
        self._perform_search(state_abbrev, select_first=True)
    
    def _perform_search(self, search_term: str, select_first: bool = False):
        """Perform state search and update display"""
        try:
            results = self.db_manager.search_states(search_term)
            
            if results:
                # If select_first or exact match, select the first result
                if select_first or len(results) == 1 or \
                   results[0]['abbreviation'].upper() == search_term.upper():
                    self._display_state(results[0])
                    self.status_var.set(f"Found: {results[0]['name']} ({results[0]['abbreviation']})")
                else:
                    # Multiple results - show first one but indicate others available
                    self._display_state(results[0])
                    self.status_var.set(f"Found {len(results)} matches - showing {results[0]['name']}")
            else:
                self._clear_results()
                self.status_var.set(f"No states found matching '{search_term}'")
            
            # Log the search
            state_found = results[0]['name'] if results else None
            self.db_manager.add_lookup_to_history(search_term, state_found)
            
        except Exception as e:
            messagebox.showerror("Search Error", f"Error searching for states: {str(e)}")
            self.status_var.set("Search error occurred")
    
    def _display_state(self, state_data: Dict):
        """Display state information in the interface"""
        self.current_state = state_data
        
        # Update state info
        state_name = f"{state_data['name']} ({state_data['abbreviation']})"
        self.state_name_var.set(state_name)
        
        # Character usage
        self.uses_zero_var.set("Yes" if state_data.get('uses_zero_for_o') else "No")
        self.uses_o_var.set("Yes" if state_data.get('allows_letter_o') else "No")
        self.zero_slashed_var.set("Yes" if state_data.get('zero_is_slashed') else "No")
        
        # Visual info
        colors = state_data.get('primary_colors')
        if colors:
            try:
                color_list = json.loads(colors) if isinstance(colors, str) else colors
                self.colors_var.set(", ".join(color_list))
            except:
                self.colors_var.set(str(colors))
        else:
            self.colors_var.set("--")
        
        self.slogan_var.set(state_data.get('slogan', '--'))
        
        # Notes
        self.notes_text.config(state=tk.NORMAL)
        self.notes_text.delete(1.0, tk.END)
        notes = state_data.get('notes', 'No additional notes available.')
        self.notes_text.insert(1.0, notes)
        self.notes_text.config(state=tk.DISABLED)
        
        # Load plate types
        self._load_plate_types(state_data['state_id'])
    
    def _load_plate_types(self, state_id: int):
        """Load and display plate types for the state"""
        try:
            plate_types = self.db_manager.get_plate_types_for_state(state_id)
            self.current_plate_types = plate_types
            
            # Clear existing items
            for item in self.plate_types_tree.get_children():
                self.plate_types_tree.delete(item)
            
            # Add plate types
            for plate_type in plate_types:
                sticker_text = "Yes" if plate_type.get('has_stickers') else "No"
                bg_color = plate_type.get('background_color', '')
                text_color = plate_type.get('text_color', '')
                colors_text = f"BG: {bg_color[:7]}..." if bg_color else "--"
                
                self.plate_types_tree.insert('', tk.END, values=(
                    plate_type['type_name'],
                    plate_type.get('pattern', '--'),
                    colors_text,
                    sticker_text
                ))
            
            # Select first item if available
            if plate_types:
                first_item = self.plate_types_tree.get_children()[0]
                self.plate_types_tree.selection_set(first_item)
                self._on_plate_type_selected()
                
        except Exception as e:
            messagebox.showerror("Database Error", f"Error loading plate types: {str(e)}")
    
    def _on_plate_type_selected(self, event=None):
        """Handle plate type selection"""
        selection = self.plate_types_tree.selection()
        if selection and self.current_plate_types:
            # Get selected index
            selected_item = selection[0]
            item_index = self.plate_types_tree.index(selected_item)
            
            if item_index < len(self.current_plate_types):
                plate_type = self.current_plate_types[item_index]
                
                # Update details display
                self.type_details_text.config(state=tk.NORMAL)
                self.type_details_text.delete(1.0, tk.END)
                
                details = []
                details.append(f"Type: {plate_type['type_name']}")
                details.append(f"Pattern: {plate_type.get('pattern', 'Not specified')}")
                details.append(f"Character Count: {plate_type.get('character_count', 'Variable')}")
                details.append(f"Description: {plate_type.get('description', 'No description')}")
                
                if plate_type.get('has_stickers'):
                    details.append(f"Stickers: {plate_type.get('sticker_description', 'Present')}")
                
                self.type_details_text.insert(1.0, "\n".join(details))
                self.type_details_text.config(state=tk.DISABLED)
    
    def _show_character_info(self, character: str):
        """Show information about a specific character"""
        if not self.current_state:
            self.char_info_text.config(state=tk.NORMAL)
            self.char_info_text.delete(1.0, tk.END)
            self.char_info_text.insert(1.0, "Please select a state first.")
            self.char_info_text.config(state=tk.DISABLED)
            return
        
        try:
            char_refs = self.db_manager.get_character_references_for_state(
                self.current_state['state_id'])
            
            self.char_info_text.config(state=tk.NORMAL)
            self.char_info_text.delete(1.0, tk.END)
            
            # Find references for this character
            relevant_refs = [ref for ref in char_refs if ref['character'] == character]
            
            if relevant_refs:
                for ref in relevant_refs:
                    info = f"Character: {ref['character']}\n"
                    info += f"Type: {ref.get('character_type', 'Unknown')}\n"
                    info += f"Description: {ref.get('description', 'No description')}\n"
                    if ref.get('confusion_chars'):
                        info += f"Can be confused with: {ref['confusion_chars']}\n"
                    info += "\n"
                    self.char_info_text.insert(tk.END, info)
            else:
                # General character info based on state rules
                info = f"Character: {character}\n\n"
                
                if character == '0':
                    if self.current_state.get('uses_zero_for_o'):
                        info += "This state USES digit 0 in plates.\n"
                    if self.current_state.get('zero_is_slashed'):
                        info += "Zero appears with a slash through it.\n"
                    else:
                        info += "Zero appears without a slash.\n"
                        
                elif character == 'O':
                    if self.current_state.get('allows_letter_o'):
                        info += "This state ALLOWS letter O in plates.\n"
                    else:
                        info += "This state does NOT use letter O in plates.\n"
                        info += "If you see this character, it's likely a zero (0).\n"
                
                elif character in ['1', 'I', 'L']:
                    info += "These characters are commonly confused:\n"
                    info += "1 = digit one\n"
                    info += "I = letter I (uppercase i)\n"
                    info += "L = letter L (uppercase L)\n"
                    info += "Check state-specific font examples if available.\n"
                
                elif character in ['8', 'B']:
                    info += "These characters can be confused:\n"
                    info += "8 = digit eight\n"
                    info += "B = letter B\n"
                    info += "Look for curved vs angular shapes.\n"
                
                elif character in ['5', 'S']:
                    info += "These characters can be confused:\n"
                    info += "5 = digit five\n"
                    info += "S = letter S\n"
                    info += "Check position rules for this state.\n"
                
                elif character in ['2', 'Z']:
                    info += "These characters can be confused:\n"
                    info += "2 = digit two\n"
                    info += "Z = letter Z\n"
                    info += "Less common confusion in most states.\n"
                
                else:
                    info += "No specific information available for this character.\n"
                
                self.char_info_text.insert(1.0, info)
            
            self.char_info_text.config(state=tk.DISABLED)
            
        except Exception as e:
            self.char_info_text.config(state=tk.NORMAL)
            self.char_info_text.delete(1.0, tk.END)
            self.char_info_text.insert(1.0, f"Error loading character info: {str(e)}")
            self.char_info_text.config(state=tk.DISABLED)
    
    def _clear_search(self, event=None):
        """Clear search and results"""
        self.search_var.set("")
        self._clear_results()
        self.search_entry.focus_set()
    
    def _clear_results(self):
        """Clear all result displays"""
        self.current_state = None
        self.current_plate_types = []
        
        # Clear state info
        self.state_name_var.set("Select a state...")
        self.uses_zero_var.set("--")
        self.uses_o_var.set("--")
        self.zero_slashed_var.set("--")
        self.colors_var.set("--")
        self.slogan_var.set("--")
        
        # Clear notes
        self.notes_text.config(state=tk.NORMAL)
        self.notes_text.delete(1.0, tk.END)
        self.notes_text.config(state=tk.DISABLED)
        
        # Clear plate types
        for item in self.plate_types_tree.get_children():
            self.plate_types_tree.delete(item)
        
        self.type_details_text.config(state=tk.NORMAL)
        self.type_details_text.delete(1.0, tk.END)
        self.type_details_text.config(state=tk.DISABLED)
        
        # Clear character info
        self.char_info_text.config(state=tk.NORMAL)
        self.char_info_text.delete(1.0, tk.END)
        self.char_info_text.config(state=tk.DISABLED)
        
        self.status_var.set("Ready - Type state name or abbreviation to search")
    
    def _show_help(self, event=None):
        """Show help dialog"""
        help_text = """License Plate Information System - Help

QUICK USAGE:
• Type state name or abbreviation in search box
• Use quick buttons (FL, GA, etc.) for common states  
• Press Enter to select first match
• Click character buttons (0, O, 1, I, etc.) to see state-specific info

KEYBOARD SHORTCUTS:
• Enter: Search and select first result
• Escape: Clear search and results
• F1: Show this help

FEATURES:
• Fast state lookup for toll reading
• Character disambiguation (0 vs O, I vs 1, etc.)
• Plate type information and patterns
• Visual references (colors, logos, slogans)
• Sticker and validation information

DESIGNED FOR:
Toll plaza operators who need quick identification
of hard-to-read license plates, especially Florida
plates with occasional out-of-state vehicles.
"""
        
        messagebox.showinfo("Help - License Plate Information System", help_text)