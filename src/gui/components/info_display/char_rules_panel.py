"""
Character Handling Rules Panel
Displays include/omit rules for stacked and slanted characters for selected state
"""

import tkinter as tk
from tkinter import ttk
import json
import os
from typing import Optional


class CharacterRulesPanel:
    """Panel showing character handling rules (include/omit) for the selected state"""
    
    def __init__(self, parent: tk.Widget, widget_factory):
        self.parent = parent
        self.widget_factory = widget_factory
        self.current_state = None
        
        # State filename mapping
        self.state_filename_map = {
            'AL': 'alabama', 'AK': 'alaska', 'AS': 'american_samoa', 'AZ': 'arizona',
            'AR': 'arkansas', 'CA': 'california', 'CO': 'colorado', 'CT': 'connecticut',
            'DE': 'delaware', 'DC': 'district_of_columbia', 'FM': 'federated_states_of_micronesia',
            'FL': 'florida', 'GA': 'georgia', 'GU': 'guam', 'HI': 'hawaii', 'ID': 'idaho',
            'IL': 'illinois', 'IN': 'indiana', 'IA': 'iowa', 'KS': 'kansas', 'KY': 'kentucky',
            'LA': 'louisiana', 'ME': 'maine', 'MH': 'marshall_islands', 'MD': 'maryland',
            'MA': 'massachusetts', 'MI': 'michigan', 'MN': 'minnesota', 'MS': 'mississippi',
            'MO': 'missouri', 'MT': 'montana', 'NE': 'nebraska', 'NV': 'nevada',
            'NH': 'new_hampshire', 'NJ': 'new_jersey', 'NM': 'new_mexico', 'NY': 'new_york',
            'NC': 'north_carolina', 'ND': 'north_dakota', 'MP': 'northern_mariana_islands',
            'OH': 'ohio', 'OK': 'oklahoma', 'OR': 'oregon', 'PW': 'palau', 'PA': 'pennsylvania',
            'PR': 'puerto_rico', 'RI': 'rhode_island', 'SC': 'south_carolina', 'SD': 'south_dakota',
            'TN': 'tennessee', 'TX': 'texas', 'UT': 'utah', 'VT': 'vermont',
            'VI': 'virgin_islands', 'VA': 'virginia', 'WA': 'washington', 'WV': 'west_virginia',
            'WI': 'wisconsin', 'WY': 'wyoming', 'AB': 'alberta', 'BC': 'british_columbia',
            'MB': 'manitoba', 'NB': 'new_brunswick', 'NL': 'newfoundland_and_labrador',
            'NT': 'northwest_territories', 'NS': 'nova_scotia', 'NU': 'nunavut', 'ON': 'ontario',
            'PE': 'prince_edward_island', 'QC': 'quebec', 'SK': 'saskatchewan', 'YT': 'yukon',
            'DIP': 'diplomatic'
        }
        
        self.setup_panel()
        
    def setup_panel(self):
        """Create the character rules panel"""
        # Main frame with border
        self.main_frame = tk.Frame(
            self.parent,
            bg='#2a2a2a',
            relief='solid',
            borderwidth=1
        )
        self.main_frame.pack(fill='both', expand=True)
        
        # Scrollable content area
        canvas = tk.Canvas(self.main_frame, bg='#2a2a2a', highlightthickness=0)
        scrollbar = tk.Scrollbar(self.main_frame, orient='vertical', command=canvas.yview)
        self.content_frame = tk.Frame(canvas, bg='#2a2a2a')
        
        self.content_frame.bind(
            "<Configure>",
            lambda e: self._configure_scroll_region(canvas, scrollbar)
        )
        
        canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        
        # Default content
        self._show_default_message()
    
    def _configure_scroll_region(self, canvas, scrollbar):
        """Configure scroll region and show/hide scrollbar"""
        canvas.configure(scrollregion=canvas.bbox("all"))
        
        canvas.update_idletasks()
        canvas_height = canvas.winfo_height()
        content_height = canvas.bbox("all")[3] if canvas.bbox("all") else 0
        
        if content_height > canvas_height:
            scrollbar.pack(side="right", fill="y")
        else:
            scrollbar.pack_forget()
    
    def _show_default_message(self):
        """Show default message when no state is selected"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        message = tk.Label(
            self.content_frame,
            text="Select a state to view character handling rules\n\n"
                 "Rules include:\n"
                 "• Letter O vs Zero 0 usage\n"
                 "• Stacked characters to INCLUDE\n"
                 "• Stacked characters to OMIT\n"
                 "• Special prefix/symbol rules",
            bg='#2a2a2a',
            fg='#888888',
            font=('Segoe UI', 9),
            justify='left'
        )
        message.pack(padx=15, pady=15, anchor='w')
    
    def update_rules(self, state_code: Optional[str]):
        """Update panel with rules for the selected state"""
        self.current_state = state_code
        
        if not state_code:
            self._show_default_message()
            return
        
        # Load state data
        state_data = self._load_state_data(state_code)
        
        if not state_data:
            self._show_error_message(state_code)
            return
        
        # Clear existing content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Display rules
        self._display_rules(state_data, state_code)
    
    def _load_state_data(self, state_code: str) -> Optional[dict]:
        """Load state JSON data"""
        try:
            # Find project root
            current_dir = os.path.dirname(__file__)
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
                print("❌ Could not find project root")
                return None
            
            # Load state JSON using filename mapping
            filename = self.state_filename_map.get(state_code)
            if not filename:
                print(f"⚠️  No filename mapping for state code: {state_code}")
                return None
            
            state_file = os.path.join(project_root, "data", "states", f"{filename}.json")
            
            if os.path.exists(state_file):
                with open(state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                print(f"⚠️  State file not found: {state_file}")
                return None
                
        except Exception as e:
            print(f"❌ Error loading state data: {e}")
            return None
    
    def _show_error_message(self, state_code: str):
        """Show error message when state data cannot be loaded"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        message = tk.Label(
            self.content_frame,
            text=f"Could not load character rules for {state_code}\n\n"
                 "State data may not be available.",
            bg='#2a2a2a',
            fg='#ff6b6b',
            font=('Segoe UI', 9)
        )
        message.pack(padx=15, pady=15)
    
    def _display_rules(self, state_data: dict, state_code: str):
        """Display character handling rules"""
        # State name header
        state_name = state_data.get('name', state_code)
        header = tk.Label(
            self.content_frame,
            text=f"{state_name} Character Rules",
            bg='#2a2a2a',
            fg='#4CAF50',
            font=('Segoe UI', 10, 'bold')
        )
        header.pack(anchor='w', padx=10, pady=(10, 5))
        
        # O vs 0 Rules
        self._display_o_vs_zero_rules(state_data)
        
        # Stacked Character Rules
        self._display_stacked_rules(state_data)
        
        # Add some padding at bottom
        tk.Frame(self.content_frame, bg='#2a2a2a', height=10).pack()
    
    def _display_o_vs_zero_rules(self, state_data: dict):
        """Display O vs 0 usage rules"""
        section_frame = tk.Frame(self.content_frame, bg='#2a2a2a')
        section_frame.pack(fill='x', padx=10, pady=5)
        
        # Section title
        title = tk.Label(
            section_frame,
            text="🔤 Letter O vs Zero 0",
            bg='#2a2a2a',
            fg='#ffffff',
            font=('Segoe UI', 9, 'bold')
        )
        title.pack(anchor='w', pady=(5, 2))
        
        uses_zero = state_data.get('uses_zero_for_o', False)
        allows_o = state_data.get('allows_letter_o', False)
        
        if not uses_zero and not allows_o:
            rule_text = "No specific O/0 rules defined"
            color = '#888888'
        elif not allows_o:
            rule_text = "❌ Does NOT use letter 'O'\n✅ Always use zero '0'"
            color = '#ff6b6b'
        elif uses_zero and allows_o:
            rule_text = "✅ Use 'O' with letters\n✅ Use '0' with numbers"
            color = '#81C784'
        else:
            rule_text = "Uses both O and 0"
            color = '#81C784'
        
        rule_label = tk.Label(
            section_frame,
            text=rule_text,
            bg='#2a2a2a',
            fg=color,
            font=('Segoe UI', 8),
            justify='left'
        )
        rule_label.pack(anchor='w', padx=20, pady=2)
    
    def _display_stacked_rules(self, state_data: dict):
        """Display stacked character rules"""
        # Get stacked character rules
        stacked_rules = None
        if 'processing_metadata' in state_data:
            if 'global_rules' in state_data['processing_metadata']:
                stacked_rules = state_data['processing_metadata']['global_rules'].get('stacked_characters')
        
        if not stacked_rules:
            return
        
        section_frame = tk.Frame(self.content_frame, bg='#2a2a2a')
        section_frame.pack(fill='x', padx=10, pady=5)
        
        # Section title
        title = tk.Label(
            section_frame,
            text="📐 Stacked/Slanted Characters",
            bg='#2a2a2a',
            fg='#ffffff',
            font=('Segoe UI', 9, 'bold')
        )
        title.pack(anchor='w', pady=(5, 2))
        
        # INCLUDE rules
        include_chars = stacked_rules.get('include', [])
        if include_chars:
            include_label = tk.Label(
                section_frame,
                text="✅ INCLUDE:",
                bg='#2a2a2a',
                fg='#4CAF50',
                font=('Segoe UI', 8, 'bold')
            )
            include_label.pack(anchor='w', padx=20, pady=(5, 2))
            
            include_text = ", ".join(include_chars)
            include_value = tk.Label(
                section_frame,
                text=include_text,
                bg='#2a2a2a',
                fg='#81C784',
                font=('Segoe UI', 8),
                wraplength=400,
                justify='left'
            )
            include_value.pack(anchor='w', padx=35, pady=1)
        
        # OMIT rules
        omit_chars = stacked_rules.get('omit', [])
        if omit_chars:
            omit_label = tk.Label(
                section_frame,
                text="❌ OMIT:",
                bg='#2a2a2a',
                fg='#ff6b6b',
                font=('Segoe UI', 8, 'bold')
            )
            omit_label.pack(anchor='w', padx=20, pady=(5, 2))
            
            omit_text = ", ".join(str(x) for x in omit_chars)
            omit_value = tk.Label(
                section_frame,
                text=omit_text,
                bg='#2a2a2a',
                fg='#ff9999',
                font=('Segoe UI', 8),
                wraplength=400,
                justify='left'
            )
            omit_value.pack(anchor='w', padx=35, pady=1)
        
        # Special rules/notes
        notes = stacked_rules.get('notes')
        if notes:
            notes_label = tk.Label(
                section_frame,
                text="ℹ️ Special Rules:",
                bg='#2a2a2a',
                fg='#64B5F6',
                font=('Segoe UI', 8, 'bold')
            )
            notes_label.pack(anchor='w', padx=20, pady=(5, 2))
            
            notes_value = tk.Label(
                section_frame,
                text=notes,
                bg='#2a2a2a',
                fg='#90CAF9',
                font=('Segoe UI', 8),
                wraplength=400,
                justify='left'
            )
            notes_value.pack(anchor='w', padx=35, pady=1)
        
        # Max characters rule
        max_chars = stacked_rules.get('max_characters')
        if max_chars:
            max_label = tk.Label(
                section_frame,
                text=f"⚠️ Max Characters: {max_chars}",
                bg='#2a2a2a',
                fg='#FFA726',
                font=('Segoe UI', 8, 'bold')
            )
            max_label.pack(anchor='w', padx=20, pady=(5, 1))
        
        # Symbols allowed
        symbols = stacked_rules.get('symbols_allowed')
        if symbols:
            symbol_label = tk.Label(
                section_frame,
                text="🔣 Symbols Allowed:",
                bg='#2a2a2a',
                fg='#AB47BC',
                font=('Segoe UI', 8, 'bold')
            )
            symbol_label.pack(anchor='w', padx=20, pady=(5, 2))
            
            symbol_text = ", ".join(symbols)
            symbol_value = tk.Label(
                section_frame,
                text=symbol_text,
                bg='#2a2a2a',
                fg='#CE93D8',
                font=('Segoe UI', 8)
            )
            symbol_value.pack(anchor='w', padx=35, pady=1)
        
        # Prefix rules
        prefix_rules = stacked_rules.get('prefix_rules')
        if prefix_rules:
            prefix_label = tk.Label(
                section_frame,
                text="🏷️ Prefix Rules:",
                bg='#2a2a2a',
                fg='#FFB74D',
                font=('Segoe UI', 8, 'bold')
            )
            prefix_label.pack(anchor='w', padx=20, pady=(5, 2))
            
            for key, value in prefix_rules.items():
                prefix_text = f"{key.replace('_', ' ').title()}: {value}"
                prefix_value = tk.Label(
                    section_frame,
                    text=prefix_text,
                    bg='#2a2a2a',
                    fg='#FFCC80',
                    font=('Segoe UI', 8),
                    wraplength=400,
                    justify='left'
                )
                prefix_value.pack(anchor='w', padx=35, pady=1)
    
    def clear_rules(self):
        """Clear the rules panel"""
        self.current_state = None
        self._show_default_message()
    
    def get_main_frame(self) -> tk.Widget:
        """Get the main panel frame"""
        return self.main_frame
