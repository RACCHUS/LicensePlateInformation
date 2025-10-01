"""
Plate Information Panel - Displays plate-specific information
"""

import tkinter as tk
from tkinter import ttk
import json
import os
from ...utils.widget_factory import WidgetFactory


class PlateInfoPanel:
    """Panel for displaying plate type specific information"""
    
    def __init__(self, parent: tk.Widget, widget_factory: WidgetFactory):
        self.parent = parent
        self.widget_factory = widget_factory
        self.current_plate_type = None
        self.current_state_code = None
        
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
        """Create the plate information panel"""
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
            "Select a plate type to view details:\n\n"
            "• Pattern and character count\n"
            "• Colors and visual design\n"
            "• Category and subtype\n"
            "• Processing type and requirements\n"
            "• Plate-specific characteristics\n"
            "• Font, logo, and text overrides\n"
            "• Character formatting rules\n"
            "• Sticker information\n"
            "• Processing metadata"
        )
        
        self.info_text.configure(state='normal')
        self.info_text.delete('1.0', 'end')
        self.info_text.insert('1.0', message)
        self.info_text.configure(state='disabled')
        
    def update_plate_info(self, plate_type: str, state_code: str | None = None):
        """Update panel with plate type information from JSON file"""
        self.current_plate_type = plate_type
        self.current_state_code = state_code
        
        # Load plate data
        plate_data = self._load_plate_data(plate_type, state_code)
        
        if not plate_data:
            self._show_error_message(plate_type, state_code)
            return
            
        # Build information display
        info_text = self._build_plate_info_text(plate_type, plate_data, state_code or "Unknown")
        
        self.info_text.configure(state='normal')
        self.info_text.delete('1.0', 'end')
        self.info_text.insert('1.0', info_text)
        self.info_text.configure(state='disabled')
        
    def _load_plate_data(self, plate_type: str, state_code: str | None = None):
        """Load plate data from JSON file"""
        if not state_code:
            return None
            
        try:
            filename = self.state_filename_map.get(state_code)
            if not filename:
                return None
                
            file_path = os.path.join('data', 'states', f'{filename}.json')
            
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    state_data = json.load(f)
                    
                # Find the specific plate type
                plate_types = state_data.get('plate_types', [])
                for plate in plate_types:
                    if plate.get('type_name') == plate_type:
                        return plate
                        
            return None
        except Exception as e:
            print(f"Error loading plate data for {plate_type} in {state_code}: {e}")
            return None
            
    def _build_plate_info_text(self, plate_type: str, plate_data: dict, state_code: str) -> str:
        """Build formatted plate information text"""
        lines = []
        
        # Header
        lines.append(f"PLATE TYPE: {plate_type}")
        if state_code:
            lines.append(f"STATE: {state_code}")
        lines.append("=" * 30)
        lines.append("")
        
        # Basic Information
        pattern = plate_data.get('pattern', 'Not specified')
        char_count = plate_data.get('character_count', 'Not specified')
        description = plate_data.get('description', 'Not specified')
        lines.append(f"Pattern: {pattern}")
        lines.append(f"Character Count: {char_count}")
        lines.append(f"Description: {description}")
        lines.append("")
        
        # Category and Type Information
        category = plate_data.get('category', 'Not specified')
        subtype = plate_data.get('subtype', 'None')
        code_number = plate_data.get('code_number', 'Not specified')
        processing_type = plate_data.get('processing_type', 'Not specified')
        lines.append(f"Category: {category}")
        if subtype:
            lines.append(f"Subtype: {subtype}")
        lines.append(f"Code Number: {code_number}")
        lines.append(f"Processing Type: {processing_type}")
        lines.append("")
        
        # Visual Design
        lines.append("VISUAL DESIGN:")
        bg_color = plate_data.get('background_color', 'Not specified')
        text_color = plate_data.get('text_color', 'Not specified')
        lines.append(f"• Background Color: {bg_color}")
        lines.append(f"• Text Color: {text_color}")
        lines.append("")
        
        # Sticker Information
        has_stickers = plate_data.get('has_stickers', False)
        sticker_desc = plate_data.get('sticker_description', 'Not specified')
        lines.append(f"Stickers: {has_stickers}")
        if has_stickers:
            lines.append(f"• Description: {sticker_desc}")
        lines.append("")
        
        # Plate-Specific Characteristics
        plate_chars = plate_data.get('plate_characteristics', {})
        if plate_chars:
            lines.append("PLATE CHARACTERISTICS:")
            
            font = plate_chars.get('font', 'Uses state default')
            logo = plate_chars.get('logo', 'Uses state default')
            plate_text = plate_chars.get('plate_text', 'Uses state default')
            weather = plate_chars.get('weather_inclusion', 'Uses state default')
            
            lines.append(f"• Font: {font}")
            lines.append(f"• Logo: {logo}")
            lines.append(f"• Plate Text: {plate_text}")
            lines.append(f"• Weather Inclusion: {weather}")
            
            # Character Formatting
            char_format = plate_chars.get('character_formatting', {})
            if char_format and any(v is not None for v in char_format.values()):
                lines.append("• Character Formatting:")
                stacked = char_format.get('stacked_characters', 'Default')
                slanted = char_format.get('slanted_characters', 'Default')
                slant_dir = char_format.get('slant_direction', 'Default')
                stack_pos = char_format.get('stack_position', 'Default')
                
                lines.append(f"  - Stacked: {stacked}")
                lines.append(f"  - Slanted: {slanted}")
                lines.append(f"  - Slant Direction: {slant_dir}")
                lines.append(f"  - Stack Position: {stack_pos}")
            
            # Sticker Override
            sticker_override = plate_chars.get('sticker_override')
            if sticker_override:
                lines.append("• Sticker Override:")
                lines.append(f"  - Color: {sticker_override.get('color', 'Not specified')}")
                lines.append(f"  - Format: {sticker_override.get('format', 'Not specified')}")
                lines.append(f"  - Position: {sticker_override.get('position', 'Not specified')}")
            
            lines.append("")
        
        # Processing Metadata
        processing_meta = plate_data.get('processing_metadata', {})
        if processing_meta:
            lines.append("PROCESSING METADATA:")
            currently_processed = processing_meta.get('currently_processed', 'Unknown')
            requires_prefix = processing_meta.get('requires_prefix', False)
            requires_suffix = processing_meta.get('requires_suffix', False)
            verify_state = processing_meta.get('verify_state_abbreviation', True)
            all_numeric = processing_meta.get('all_numeric_plate', False)
            
            lines.append(f"• Currently Processed: {currently_processed}")
            lines.append(f"• Requires Prefix: {requires_prefix}")
            lines.append(f"• Requires Suffix: {requires_suffix}")
            lines.append(f"• Verify State Abbreviation: {verify_state}")
            lines.append(f"• All Numeric Plate: {all_numeric}")
            
            dot_processing = processing_meta.get('dot_processing_type')
            if dot_processing:
                lines.append(f"• DOT Processing Type: {dot_processing}")
                
            dot_dropdown = processing_meta.get('dot_dropdown_identifier')
            if dot_dropdown:
                lines.append(f"• DOT Dropdown ID: {dot_dropdown}")
            
            visual_id = processing_meta.get('visual_identifier')
            if visual_id:
                lines.append(f"• Visual Identifier: {visual_id}")
                
            vehicle_type = processing_meta.get('vehicle_type_identification')
            if vehicle_type:
                lines.append(f"• Vehicle Type ID: {vehicle_type}")
            
            lines.append("")
        
        # Visual Identifiers and Processing Rules
        visual_identifier = plate_data.get('visual_identifier')
        processing_rules = plate_data.get('processing_rules')
        requires_prefix = plate_data.get('requires_prefix', False)
        
        if visual_identifier or processing_rules is not None:
            lines.append("ADDITIONAL INFO:")
            if visual_identifier:
                lines.append(f"• Visual Identifier: {visual_identifier}")
            if processing_rules is not None:
                lines.append(f"• Processing Rules: {processing_rules}")
            lines.append(f"• Requires Prefix: {requires_prefix}")
        
        return "\n".join(lines)
        
    def _show_error_message(self, plate_type: str, state_code: str | None):
        """Show error message when plate data cannot be loaded"""
        message = (
            f"Unable to load information for '{plate_type}'\n"
            f"State: {state_code or 'Not specified'}\n\n"
            f"Possible reasons:\n"
            f"• Plate type not found in state data\n"
            f"• State data file not available\n"
            f"• File format error\n\n"
            f"Please verify the plate type exists in the selected state"
        )
        
        self.info_text.configure(state='normal')
        self.info_text.delete('1.0', 'end')
        self.info_text.insert('1.0', message)
        self.info_text.configure(state='disabled')
        
    def clear_info(self):
        """Clear current information and show default"""
        self.current_plate_type = None
        self.show_default_message()
        
    def get_main_frame(self) -> tk.Widget:
        """Get the main panel frame"""
        return self.main_frame