"""
State Information Panel - Displays detailed state information
"""

import tkinter as tk
from tkinter import ttk
import json
import os
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
        # Main container with border
        self.main_frame = self.widget_factory.create_frame(self.parent)
        self.main_frame.configure(relief='solid', borderwidth=1)
        self.main_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Text display with scrollbar
        text_frame = tk.Frame(self.main_frame, bg='#1a1a1a')
        text_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.info_text = tk.Text(
            text_frame,
            bg='#1a1a1a',
            fg='#ffffff',
            font=('Segoe UI', 9),
            wrap=tk.WORD,
            insertbackground='#ffffff',
            state='disabled',
            yscrollcommand=scrollbar.set
        )
        self.info_text.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.info_text.yview)
        
        # Show default message
        self.show_default_message()
        
    def show_default_message(self):
        """Show default instructional message"""
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
        
        self.info_text.configure(state='normal')
        self.info_text.delete('1.0', 'end')
        self.info_text.insert('1.0', message)
        self.info_text.configure(state='disabled')
        
    def update_state_info(self, state_code: str):
        """Update panel with state information from JSON file"""
        self.current_state = state_code
        
        # Load state data
        state_data = self._load_state_data(state_code)
        
        if not state_data:
            self._show_error_message(state_code)
            return
            
        # Build information display
        info_text = self._build_state_info_text(state_code, state_data)
        
        self.info_text.configure(state='normal')
        self.info_text.delete('1.0', 'end')
        self.info_text.insert('1.0', info_text)
        self.info_text.configure(state='disabled')
        
    def _load_state_data(self, state_code: str):
        """Load state data from JSON file"""
        try:
            filename = self.state_filename_map.get(state_code)
            if not filename:
                return None
                
            file_path = os.path.join('data', 'states', f'{filename}.json')
            
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return None
        except Exception as e:
            print(f"Error loading state data for {state_code}: {e}")
            return None
            
    def _build_state_info_text(self, state_code: str, state_data: dict) -> str:
        """Build formatted state information text"""
        lines = []
        
        # Header
        name = state_data.get('name', state_code)
        lines.append(f"STATE: {name} ({state_code})")
        lines.append("=" * (len(name) + len(state_code) + 10))
        lines.append("")
        
        # Basic Information
        slogan = state_data.get('slogan', 'N/A')
        lines.append(f"Slogan: {slogan}")
        lines.append("")
        
        # Character Rules
        lines.append("CHARACTER RULES:")
        uses_zero = state_data.get('uses_zero_for_o', False)
        allows_o = state_data.get('allows_letter_o', False)
        zero_slashed = state_data.get('zero_is_slashed', False)
        lines.append(f"• Uses zero for O: {uses_zero}")
        lines.append(f"• Allows letter O: {allows_o}")
        lines.append(f"• Zero is slashed: {zero_slashed}")
        lines.append("")
        
        # Visual Characteristics
        lines.append("VISUAL CHARACTERISTICS:")
        main_font = state_data.get('main_font', 'Not specified')
        main_logo = state_data.get('main_logo', 'Not specified')
        main_text = state_data.get('main_plate_text', 'Not specified')
        lines.append(f"• Font: {main_font}")
        lines.append(f"• Logo: {main_logo}")
        lines.append(f"• Plate Text: {main_text}")
        
        # Primary Colors
        colors = state_data.get('primary_colors', [])
        if colors:
            color_str = ", ".join(colors)
            lines.append(f"• Primary Colors: {color_str}")
        lines.append("")
        
        # Sticker Information
        sticker_format = state_data.get('sticker_format', {})
        if sticker_format:
            lines.append("STICKER FORMAT:")
            lines.append(f"• Color: {sticker_format.get('color', 'Not specified')}")
            lines.append(f"• Format: {sticker_format.get('format', 'Not specified')}")
            lines.append(f"• Position: {sticker_format.get('position', 'Not specified')}")
            lines.append(f"• Description: {sticker_format.get('description', 'Not specified')}")
            lines.append("")
        
        # Character Formatting
        char_format = state_data.get('character_formatting', {})
        if char_format:
            lines.append("CHARACTER FORMATTING:")
            lines.append(f"• Stacked: {char_format.get('stacked_characters', False)}")
            lines.append(f"• Slanted: {char_format.get('slanted_characters', False)}")
            if char_format.get('slant_direction'):
                lines.append(f"• Slant Direction: {char_format.get('slant_direction')}")
            if char_format.get('stack_position'):
                lines.append(f"• Stack Position: {char_format.get('stack_position')}")
            lines.append("")
        
        # Weather and Processing
        weather = state_data.get('weather_inclusion', True)
        lines.append(f"Weather Inclusion: {weather}")
        lines.append("")
        
        # Processing Metadata
        processing = state_data.get('processing_metadata', {})
        if processing:
            lines.append("PROCESSING METADATA:")
            description = processing.get('description', 'Not specified')
            lines.append(f"• Description: {description}")
            
            global_rules = processing.get('global_rules', {})
            if global_rules:
                char_restrictions = global_rules.get('character_restrictions', 'None')
                font_changes = global_rules.get('font_changes', 'None')
                code_system = global_rules.get('code_system', 'Standard')
                lines.append(f"• Character Restrictions: {char_restrictions}")
                lines.append(f"• Font Changes: {font_changes}")
                lines.append(f"• Code System: {code_system}")
            lines.append("")
        
        # Special Notes
        notes = state_data.get('notes', 'No special notes')
        lines.append("SPECIAL NOTES:")
        lines.append(notes)
        
        return "\n".join(lines)
        
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
        
        self.info_text.configure(state='normal')
        self.info_text.delete('1.0', 'end')
        self.info_text.insert('1.0', message)
        self.info_text.configure(state='disabled')
        
    def clear_info(self):
        """Clear current information and show default"""
        self.current_state = None
        self.show_default_message()
        
    def get_main_frame(self) -> tk.Widget:
        """Get the main panel frame"""
        return self.main_frame