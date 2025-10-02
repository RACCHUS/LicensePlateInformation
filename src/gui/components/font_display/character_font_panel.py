"""
Character Font Panel Component
Displays character font examples based on selected state's license plate fonts
"""

import tkinter as tk
from tkinter import font as tkfont
import json
import os


class CharacterFontPanel:
    """Panel showing character font examples for license plates"""
    
    # Font mappings for different state plate fonts
    # Maps state font descriptions to actual Windows system fonts
    # Priority order matters - more specific matches first
    FONT_MAPPINGS = [
        # Narrow fonts (most common for license plates)
        (['narrow sans serif', 'narrow block'], ('Arial Narrow', 15, 'bold')),
        (['narrow', 'condensed', 'compressed'], ('Arial Narrow', 15, 'bold')),
        
        # Highway Gothic and derivatives (very common)
        (['highway gothic'], ('Arial', 15, 'bold')),
        
        # Block/Bold fonts
        (['block sans serif', 'block style'], ('Arial Black', 14, 'bold')),
        (['block'], ('Arial Black', 14, 'bold')),
        
        # Custom/Proprietary (use distinctive font)
        (['proprietary', 'custom sans serif', 'custom'], ('Impact', 15, 'normal')),
        
        # Special named fonts
        (['penitentiary gothic'], ('Arial Black', 15, 'bold')),  # California
        (['fe-schrift'], ('Consolas', 14, 'bold')),  # European-style
        (['interstate'], ('Arial', 15, 'bold')),  # Similar to highway signs
        
        # Modified versions
        (['modified sans serif', 'modified block'], ('Arial', 15, 'bold')),
        
        # General sans serif
        (['sans serif', 'sans-serif'], ('Arial', 15, 'bold')),
        
        # Serif fonts (rare)
        (['serif script', 'serif'], ('Times New Roman', 14, 'bold')),
        (['serifed'], ('Times New Roman', 14, 'bold')),
        
        # Government/Diplomatic standard
        (['diplomatic', 'government'], ('Arial', 14, 'bold')),
        
        # Monospace/Fixed (if any)
        (['monospace', 'courier', 'fixed'], ('Courier New', 14, 'bold')),
        
        # Default fallback
        (['default'], ('Arial', 15, 'bold'))
    ]
    
    @staticmethod
    def _find_best_font(description):
        """
        Find the best matching system font for a plate font description
        
        Args:
            description: Font description from state JSON
            
        Returns:
            tuple: (font_family, size, weight)
        """
        if not description:
            return ('Arial', 15, 'bold')
        
        desc_lower = description.lower()
        
        # Try each mapping in priority order
        for keywords, font_spec in CharacterFontPanel.FONT_MAPPINGS:
            for keyword in keywords:
                if keyword in desc_lower:
                    return font_spec
        
        # Ultimate fallback
        return ('Arial', 15, 'bold')
    
    def __init__(self, parent, widget_factory=None):
        """
        Initialize character font panel
        
        Args:
            parent: Parent tkinter widget
            widget_factory: Optional WidgetFactory for consistent styling
        """
        self.parent = parent
        self.widget_factory = widget_factory
        self.current_state = None
        self.character_labels = {}
        
        # Create the main panel
        self.main_frame = self._create_panel()
        
    def _create_panel(self):
        """Create the character font preview panel"""
        # Main frame with border
        main_frame = tk.Frame(
            self.parent,
            bg='#2a2a2a',
            relief='solid',
            borderwidth=1
        )
        main_frame.pack(fill='both', expand=True)
        
        # Content container
        content_container = tk.Frame(main_frame, bg='#2a2a2a')
        content_container.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Character grid frame
        self.grid_frame = tk.Frame(content_container, bg='#2a2a2a')
        self.grid_frame.pack(fill='both', expand=True)
        
        # Create character grid
        self._create_character_grid()
        
        # Status/Info label at bottom
        self.status_label = tk.Label(
            content_container,
            text="Select a state to see character font examples",
            bg='#2a2a2a',
            fg='#888888',
            font=('Segoe UI', 9),
            wraplength=250,
            justify='center'
        )
        self.status_label.pack(pady=(5, 0))
        
        return main_frame
    
    def _create_character_grid(self):
        """Create grid of character samples"""
        # Characters to display
        characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        
        # Create grid (6 columns)
        for i, char in enumerate(characters):
            row = i // 6
            col = i % 6
            
            # Character cell frame
            char_frame = tk.Frame(
                self.grid_frame,
                bg='#3a3a3a',
                relief='solid',
                borderwidth=1
            )
            char_frame.grid(row=row, column=col, padx=1, pady=1, sticky='ew')
            
            # Character label
            char_label = tk.Label(
                char_frame,
                text=char,
                bg='#3a3a3a',
                fg='#ffffff',
                font=('Courier New', 14, 'bold'),  # Default font
                width=2,
                height=1
            )
            char_label.pack()
            
            # Store reference for later updates
            self.character_labels[char] = char_label
        
        # Configure grid weights for equal spacing
        for col in range(6):
            self.grid_frame.columnconfigure(col, weight=1)
    
    def _get_font_for_state(self, state_code):
        """
        Get appropriate font for a state's license plates
        
        Args:
            state_code: State abbreviation (e.g., 'FL', 'CA')
            
        Returns:
            tuple: (font_family, size, weight) or None
        """
        if not state_code:
            return None
        
        # Load state data
        state_file = os.path.join('data', 'states', f'{state_code.lower()}.json')
        if not os.path.exists(state_file):
            return None
        
        try:
            with open(state_file, 'r', encoding='utf-8') as f:
                state_data = json.load(f)
            
            # Get main font information
            main_font_desc = state_data.get('main_font', '')
            
            # Use the smart matching system
            font_spec = self._find_best_font(main_font_desc)
            
            print(f"🔤 Font mapping: {state_code} '{main_font_desc}' → {font_spec[0]}")
            
            return font_spec
            
        except Exception as e:
            print(f"⚠️ Error loading font for {state_code}: {e}")
            return ('Arial', 15, 'bold')
    
    def _get_state_character_rules(self, state_code):
        """
        Get character-specific rules for a state (like O/0 usage)
        
        Args:
            state_code: State abbreviation
            
        Returns:
            dict: Character rules and restrictions
        """
        if not state_code:
            return {}
        
        state_file = os.path.join('data', 'states', f'{state_code.lower()}.json')
        if not os.path.exists(state_file):
            return {}
        
        try:
            with open(state_file, 'r', encoding='utf-8') as f:
                state_data = json.load(f)
            
            rules = {}
            
            # Check for letter O and zero usage
            rules['allows_letter_o'] = state_data.get('allows_letter_o', True)
            rules['uses_zero_for_o'] = state_data.get('uses_zero_for_o', False)
            rules['zero_is_slashed'] = state_data.get('zero_is_slashed', False)
            
            # Check for Nevada's special dual system
            if 'letter_o_and_zero_usage' in state_data:
                rules['nevada_dual_system'] = state_data['letter_o_and_zero_usage']
            
            # Check for special character restrictions
            char_restrictions = state_data.get('processing_metadata', {}).get('global_rules', {}).get('character_restrictions', {})
            if isinstance(char_restrictions, dict):
                rules['restrictions'] = char_restrictions
            
            return rules
            
        except Exception as e:
            print(f"⚠️ Error loading character rules for {state_code}: {e}")
            return {}
    
    def update_state(self, state_code, state_name=None):
        """
        Update character font display for selected state
        
        Args:
            state_code: State abbreviation (e.g., 'FL', 'CA')
            state_name: Full state name (optional)
        """
        self.current_state = state_code
        
        if not state_code:
            self._reset_display()
            return
        
        # Get font for this state
        state_font = self._get_font_for_state(state_code)
        
        # Get character rules
        char_rules = self._get_state_character_rules(state_code)
        
        # Update each character label
        for char, label in self.character_labels.items():
            # Apply state font
            if state_font:
                label.config(font=state_font)
            
            # Check for character restrictions
            fg_color = '#ffffff'  # Default white
            display_char = char  # Default character
            
            # Handle letter O restrictions
            if char == 'O':
                if not char_rules.get('allows_letter_o', True):
                    fg_color = '#ff6666'  # Red - not used
                elif 'nevada_dual_system' in char_rules:
                    fg_color = '#66ff66'  # Green - used on all plates
            
            # Handle number 0 restrictions
            elif char == '0':
                if char_rules.get('uses_zero_for_o', False):
                    # State uses zero instead of O (like Florida)
                    fg_color = '#66ff66'  # Green - used
                elif char_rules.get('zero_is_slashed', False):
                    # Slashed zero
                    display_char = 'Ø'
                    fg_color = '#66ff66'  # Green - special form
                elif 'nevada_dual_system' in char_rules:
                    nevada_rules = char_rules['nevada_dual_system']
                    if nevada_rules.get('personalized_plates', {}).get('uses_number_zero'):
                        fg_color = '#ffaa66'  # Orange - personalized only
                    else:
                        fg_color = '#ff6666'  # Red - not used
                elif not char_rules.get('allows_letter_o', True):
                    # If O is not allowed, zero might be used instead
                    fg_color = '#66ff66'  # Green - used
            
            # Update label
            label.config(fg=fg_color, text=display_char)
        
        # Update status label
        display_name = state_name if state_name else state_code
        status_text = f"Font preview for {display_name}"
        
        # Add special notes
        notes = []
        if not char_rules.get('allows_letter_o', True):
            notes.append("❌ Letter 'O' not used")
        if char_rules.get('uses_zero_for_o', False):
            notes.append("✅ Only uses '0', not 'O'")
        if char_rules.get('zero_is_slashed', False):
            notes.append("Ø Zero is slashed")
        if 'nevada_dual_system' in char_rules:
            notes.append("⚠️ O/0 depends on plate type")
        
        if notes:
            status_text += f"\n{' • '.join(notes)}"
        
        self.status_label.config(text=status_text, fg='#4CAF50')
        
        print(f"🔤 Updated character font preview for {state_code}")
    
    def _reset_display(self):
        """Reset display to default state"""
        # Reset all character labels to default
        default_font = ('Courier New', 14, 'bold')
        for char, label in self.character_labels.items():
            label.config(
                font=default_font,
                fg='#ffffff',
                text=char
            )
        
        # Reset status
        self.status_label.config(
            text="Select a state to see character font examples",
            fg='#888888'
        )
        
        self.current_state = None
        print("🔤 Reset character font preview")
    
    def clear(self):
        """Clear the character font display"""
        self._reset_display()
    
    def get_frame(self):
        """Get the main frame widget"""
        return self.main_frame
