"""
State Information Panel - Displays detailed state information
"""

import tkinter as tk
from tkinter import ttk
import json
import os
import sys
from ...utils.widget_factory import WidgetFactory


class StateInfoPanel:
    """Panel for displaying state-specific information"""
    
    def __init__(self, parent: tk.Widget, widget_factory: WidgetFactory):
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
        """Create the state information panel"""
        # Note: parent is already the scrollable frame from main.py
        # No need for additional canvas/scrollbar wrapping
        
        # Adjustable wrap length for text (similar to search results panel)
        self.wrap_length = 300
        
        # Show default message
        self.show_default_message()
        
    def show_default_message(self):
        """Show default instructional message"""
        # Clear existing content
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        message = (
            "Select a state to view information:\n\n"
            "• State name and slogan\n"
            "• Character rules (O/0 usage)\n"
            "• Font and visual characteristics\n"
            "• Logo and plate text\n"
            "• Sticker format and positioning\n"
            "• Character formatting rules\n"
            "• Weather inclusion settings\n"
            "• Processing metadata\n"
            "• Special notes"
        )
        
        default_label = tk.Label(
            self.parent,
            text=message,
            bg='#2a2a2a',
            fg='#888888',
            font=('Segoe UI', 9),
            justify='left',
            anchor='nw',
            wraplength=self.wrap_length
        )
        default_label.pack(fill='x', padx=5, pady=5)
        
    def update_state_info(self, state_code: str):
        """Update panel with state information from JSON file"""
        self.current_state = state_code
        
        # Clear existing content
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        # Load state data
        state_data = self._load_state_data(state_code)
        
        if not state_data:
            self._show_error_message(state_code)
            return
            
        # Build and display information using labels
        self._display_state_info(state_code, state_data)
        
    def _load_state_data(self, state_code: str):
        """Load state data from JSON file"""
        try:
            filename = self.state_filename_map.get(state_code)
            if not filename:
                return None
            
            # Get base application path (works for both script and PyInstaller)
            if getattr(sys, 'frozen', False):
                application_path = sys._MEIPASS  # type: ignore
            else:
                application_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
                
            file_path = os.path.join(application_path, 'data', 'states', f'{filename}.json')
            
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return None
        except Exception as e:
            print(f"Error loading state data for {state_code}: {e}")
            return None
            
    def _display_state_info(self, state_code: str, state_data: dict):
        """Display formatted state information using labels with wraplength"""
        # Helper function to create a label
        def create_label(text, bold=False, color='#ffffff', pady_val=(2, 0)):
            font_style = ('Segoe UI', 9, 'bold') if bold else ('Segoe UI', 9)
            label = tk.Label(
                self.parent,
                text=text,
                bg='#2a2a2a',
                fg=color,
                font=font_style,
                justify='left',
                anchor='w',
                wraplength=self.wrap_length
            )
            label.pack(fill='x', padx=5, pady=pady_val)
            return label
        
        # Header
        name = state_data.get('name', state_code)
        create_label(f"STATE: {name} ({state_code})", bold=True, color='#4CAF50', pady_val=(5, 2))
        create_label("=" * 40, color='#4CAF50')
        
        # Basic Information
        slogan = state_data.get('slogan', 'N/A')
        create_label(f"Slogan: {slogan}", color='#81C784', pady_val=(5, 2))
        
        # Character Rules
        create_label("CHARACTER RULES:", bold=True, color='#FFD54F', pady_val=(8, 2))
        uses_zero = state_data.get('uses_zero_for_o', False)
        allows_o = state_data.get('allows_letter_o', False)
        zero_slashed = state_data.get('zero_is_slashed', False)
        create_label(f"• Uses zero for O: {uses_zero}")
        create_label(f"• Allows letter O: {allows_o}")
        create_label(f"• Zero is slashed: {zero_slashed}")
        
        # Visual Characteristics
        create_label("VISUAL CHARACTERISTICS:", bold=True, color='#FFD54F', pady_val=(8, 2))
        main_font = state_data.get('main_font', 'Not specified')
        main_logo = state_data.get('main_logo', 'Not specified')
        main_text = state_data.get('main_plate_text', 'Not specified')
        create_label(f"• Font: {main_font}")
        create_label(f"• Logo: {main_logo}")
        create_label(f"• Plate Text: {main_text}")
        
        # Primary Colors
        colors = state_data.get('primary_colors', [])
        if colors:
            color_str = ", ".join(colors)
            create_label(f"• Primary Colors: {color_str}")
        
        # Sticker Information
        sticker_format = state_data.get('sticker_format', {})
        if sticker_format:
            create_label("STICKER FORMAT:", bold=True, color='#FFD54F', pady_val=(8, 2))
            create_label(f"• Color: {sticker_format.get('color', 'Not specified')}")
            create_label(f"• Format: {sticker_format.get('format', 'Not specified')}")
            create_label(f"• Position: {sticker_format.get('position', 'Not specified')}")
            create_label(f"• Description: {sticker_format.get('description', 'Not specified')}")
        
        # Character Formatting
        char_format = state_data.get('character_formatting', {})
        if char_format:
            create_label("CHARACTER FORMATTING:", bold=True, color='#FFD54F', pady_val=(8, 2))
            create_label(f"• Stacked: {char_format.get('stacked_characters', False)}")
            create_label(f"• Slanted: {char_format.get('slanted_characters', False)}")
            if char_format.get('slant_direction'):
                create_label(f"• Slant Direction: {char_format.get('slant_direction')}")
            if char_format.get('stack_position'):
                create_label(f"• Stack Position: {char_format.get('stack_position')}")
        
        # Weather and Processing
        weather = state_data.get('weather_inclusion', True)
        create_label(f"Weather Inclusion: {weather}", pady_val=(8, 2))
        
        # Processing Metadata
        processing = state_data.get('processing_metadata', {})
        if processing:
            create_label("PROCESSING METADATA:", bold=True, color='#FFD54F', pady_val=(8, 2))
            description = processing.get('description', 'Not specified')
            create_label(f"• Description: {description}")
            
            global_rules = processing.get('global_rules', {})
            if global_rules:
                char_restrictions = global_rules.get('character_restrictions', 'None')
                font_changes = global_rules.get('font_changes', 'None')
                code_system = global_rules.get('code_system', 'Standard')
                create_label(f"• Character Restrictions: {char_restrictions}")
                create_label(f"• Font Changes: {font_changes}")
                create_label(f"• Code System: {code_system}")
        
        # Special Notes
        notes = state_data.get('notes', 'No special notes')
        create_label("SPECIAL NOTES:", bold=True, color='#FFD54F', pady_val=(8, 2))
        create_label(notes, color='#888888')
    
    def _show_error_message(self, state_code: str):
        """Show error message when state data cannot be loaded"""
        message = (
            f"Unable to load information for {state_code}\n\n"
            f"Possible reasons:\n"
            f"• State data file not found\n"
            f"• Invalid state code\n"
            f"• File format error\n\n"
            f"Please check the data/states/ directory"
        )
        
        error_label = tk.Label(
            self.parent,
            text=message,
            bg='#2a2a2a',
            fg='#ff5555',
            font=('Segoe UI', 9),
            justify='left',
            anchor='nw',
            wraplength=self.wrap_length
        )
        error_label.pack(fill='x', padx=5, pady=5)
        
    def clear_info(self):
        """Clear current information and show default"""
        self.current_state = None
        self.show_default_message()