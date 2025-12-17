"""
Plate Information Panel - Displays plate-specific information
"""

import tkinter as tk
from tkinter import ttk
import json
import os
import sys
from ...utils.widget_factory import WidgetFactory
from ....utils.logger import log_error, log_warning, log_info


class PlateInfoPanel:
    """Panel for displaying plate type specific information"""
    
    def __init__(self, parent: tk.Widget, widget_factory: WidgetFactory):
        self.parent = parent
        self.widget_factory = widget_factory
        self.current_plate_type = None
        self.current_state_code = None
        
        # Load state-plate-type mapping for finding states when none selected
        self.plate_type_mapping = self._load_plate_type_mapping()
        
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
        # Note: parent is already the scrollable frame from main.py
        # No need for additional canvas/scrollbar wrapping
        
        # Adjustable wrap length for text (similar to state info panel)
        self.wrap_length = 300
        
        # Show default message
        self.show_default_message()
    
    def _load_plate_type_mapping(self) -> dict:
        """Load the state-plate-type mapping data"""
        # Get base application path (works for both script and PyInstaller)
        if getattr(sys, 'frozen', False):
            application_path = sys._MEIPASS  # type: ignore
        else:
            # Find project root by searching for main.py
            current_dir = os.path.dirname(__file__)
            search_dir = current_dir
            application_path = None
            
            for _ in range(10):
                if os.path.exists(os.path.join(search_dir, "main.py")):
                    application_path = search_dir
                    break
                parent = os.path.dirname(search_dir)
                if parent == search_dir:
                    break
                search_dir = parent
            
            if not application_path:
                log_warning("Could not find project root for plate type mapping")
                print("❌ Could not find project root")
                return {"plate_type_to_states": {}}
        
        mapping_file = os.path.join(application_path, 'data', 'state_plate_type_mapping.json')
        
        try:
            if os.path.exists(mapping_file):
                with open(mapping_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                log_warning(f"Plate type mapping file not found: {mapping_file}")
                print(f"⚠️  Plate type mapping file not found: {mapping_file}")
                return {"plate_type_to_states": {}}
        except json.JSONDecodeError as e:
            log_error(f"JSON parse error loading plate type mapping", exc=e)
            print(f"❌ Error loading plate type mapping: {e}")
            return {"plate_type_to_states": {}}
        except OSError as e:
            log_error(f"File read error loading plate type mapping", exc=e)
            print(f"❌ Error loading plate type mapping: {e}")
            return {"plate_type_to_states": {}}
        
    def show_default_message(self):
        """Show default instructional message"""
        # Clear existing content
        for widget in self.parent.winfo_children():
            widget.destroy()
        
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
    
    def update_plate_info(self, plate_type: str, state_code: str | None = None):
        """Update panel with plate type information from JSON file"""
        try:
            self.current_plate_type = plate_type
            self.current_state_code = state_code
            
            # Clear existing content
            for widget in self.parent.winfo_children():
                widget.destroy()
            
            # Load plate data (this may auto-select a state if none provided)
            plate_data = self._load_plate_data(plate_type, state_code)
            
            if not plate_data:
                self._show_error_message(plate_type, state_code)
                return
            
            # Get the actual state code used (may have been auto-selected)
            actual_state = self.current_state_code or "Unknown"
                
            # Build and display information using labels
            self._display_plate_info(plate_type, plate_data, actual_state, state_code is None)
        except Exception as e:
            log_error(f"Error updating plate info for {plate_type}", exc=e)
            self._show_error_message(plate_type, state_code)
        
    def _load_plate_data(self, plate_type: str, state_code: str | None = None):
        """Load plate data from JSON file"""
        # If no state provided, find one that has this plate type
        if not state_code:
            states_with_type = self.plate_type_mapping.get("plate_type_to_states", {}).get(plate_type, [])
            if states_with_type:
                # Use the first state alphabetically
                state_code = states_with_type[0]
                log_info(f"No state selected, using {state_code} for plate type '{plate_type}'")
                print(f"📋 No state selected, using {state_code} for plate type '{plate_type}'")
            else:
                log_warning(f"Plate type '{plate_type}' not found in any state")
                print(f"❌ Plate type '{plate_type}' not found in any state")
                return None
        
        # At this point, state_code is guaranteed to be a string
        assert state_code is not None, "state_code should not be None here"
            
        filename = self.state_filename_map.get(state_code)
        if not filename:
            log_warning(f"No filename mapping for state code: {state_code}")
            print(f"❌ No filename mapping for state code: {state_code}")
            return None
        
        try:
            # Get base application path (works for both script and PyInstaller)
            if getattr(sys, 'frozen', False):
                application_path = sys._MEIPASS  # type: ignore
            else:
                # Find project root by searching for main.py
                current_dir = os.path.dirname(__file__)
                search_dir = current_dir
                application_path = None
                
                for _ in range(10):
                    if os.path.exists(os.path.join(search_dir, "main.py")):
                        application_path = search_dir
                        break
                    parent = os.path.dirname(search_dir)
                    if parent == search_dir:
                        break
                    search_dir = parent
                
                if not application_path:
                    log_error(f"Could not find project root from {current_dir}")
                    print(f"❌ Could not find project root from {current_dir}")
                    return None
                
            file_path = os.path.join(application_path, 'data', 'states', f'{filename}.json')
            
            if not os.path.exists(file_path):
                log_warning(f"State file not found: {file_path}")
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                state_data = json.load(f)
                
            # Find the specific plate type
            plate_types = state_data.get('plate_types', [])
            for plate in plate_types:
                if plate.get('type_name') == plate_type:
                    # Store which state we actually loaded from
                    self.current_state_code = state_code
                    return plate
            
            log_warning(f"Plate type '{plate_type}' not found in {state_code} data")
            print(f"⚠️  Plate type '{plate_type}' not found in {state_code} data")
            return None
        except json.JSONDecodeError as e:
            log_error(f"JSON parse error for {state_code}", exc=e)
            print(f"Error loading plate data for {plate_type} in {state_code}: {e}")
            return None
        except OSError as e:
            log_error(f"File read error for {state_code}", exc=e)
            print(f"Error loading plate data for {plate_type} in {state_code}: {e}")
            return None
        except Exception as e:
            log_error(f"Unexpected error loading plate data for {plate_type} in {state_code}", exc=e)
            print(f"Error loading plate data for {plate_type} in {state_code}: {e}")
            return None
            
    def _display_plate_info(self, plate_type: str, plate_data: dict, state_code: str, auto_selected: bool = False):
        """Display formatted plate information using labels with wraplength"""
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
        create_label(f"PLATE TYPE: {plate_type}", bold=True, color='#4CAF50', pady_val=(5, 2))
        if state_code:
            if auto_selected:
                # Get all states that have this plate type
                states_with_type = self.plate_type_mapping.get("plate_type_to_states", {}).get(plate_type, [])
                if len(states_with_type) > 1:
                    create_label(f"STATE: {state_code} (showing data from {state_code})", bold=True, color='#FFD54F')
                    create_label(f"Also available in: {', '.join([s for s in states_with_type if s != state_code])}", color='#888888')
                else:
                    create_label(f"STATE: {state_code}", bold=True, color='#4CAF50')
            else:
                create_label(f"STATE: {state_code}", bold=True, color='#4CAF50')
        create_label("=" * 40, color='#4CAF50')
        
        # Basic Information
        pattern = plate_data.get('pattern', 'Not specified')
        char_count = plate_data.get('character_count', 'Not specified')
        description = plate_data.get('description', 'Not specified')
        create_label(f"Pattern: {pattern}", color='#81C784', pady_val=(5, 2))
        create_label(f"Character Count: {char_count}", color='#81C784')
        create_label(f"Description: {description}", color='#888888')
        
        # Category and Type Information
        category = plate_data.get('category', 'Not specified')
        subtype = plate_data.get('subtype', 'None')
        code_number = plate_data.get('code_number', 'Not specified')
        processing_type = plate_data.get('processing_type', 'Not specified')
        create_label(f"Category: {category}", pady_val=(5, 2))
        if subtype:
            create_label(f"Subtype: {subtype}")
        create_label(f"Code Number: {code_number}")
        create_label(f"Processing Type: {processing_type}")
        
        # Visual Design
        create_label("VISUAL DESIGN:", bold=True, color='#FFD54F', pady_val=(8, 2))
        bg_color = plate_data.get('background_color', 'Not specified')
        text_color = plate_data.get('text_color', 'Not specified')
        create_label(f"• Background Color: {bg_color}")
        create_label(f"• Text Color: {text_color}")
        
        # Sticker Information
        has_stickers = plate_data.get('has_stickers', False)
        sticker_desc = plate_data.get('sticker_description', 'Not specified')
        create_label(f"Stickers: {has_stickers}", pady_val=(5, 2))
        if has_stickers:
            create_label(f"• Description: {sticker_desc}")
        
        # Plate-Specific Characteristics
        plate_chars = plate_data.get('plate_characteristics', {})
        if plate_chars:
            create_label("PLATE CHARACTERISTICS:", bold=True, color='#FFD54F', pady_val=(8, 2))
            
            font = plate_chars.get('font', 'Uses state default')
            logo = plate_chars.get('logo', 'Uses state default')
            plate_text = plate_chars.get('plate_text', 'Uses state default')
            weather = plate_chars.get('weather_inclusion', 'Uses state default')
            
            create_label(f"• Font: {font}")
            create_label(f"• Logo: {logo}")
            create_label(f"• Plate Text: {plate_text}")
            create_label(f"• Weather Inclusion: {weather}")
            
            # Character Formatting
            char_format = plate_chars.get('character_formatting', {})
            if char_format and any(v is not None for v in char_format.values()):
                create_label("• Character Formatting:", color='#81C784')
                stacked = char_format.get('stacked_characters', 'Default')
                slanted = char_format.get('slanted_characters', 'Default')
                slant_dir = char_format.get('slant_direction', 'Default')
                stack_pos = char_format.get('stack_position', 'Default')
                
                create_label(f"  - Stacked: {stacked}")
                create_label(f"  - Slanted: {slanted}")
                create_label(f"  - Slant Direction: {slant_dir}")
                create_label(f"  - Stack Position: {stack_pos}")
            
            # Sticker Override
            sticker_override = plate_chars.get('sticker_override')
            if sticker_override:
                create_label("• Sticker Override:", color='#81C784')
                create_label(f"  - Color: {sticker_override.get('color', 'Not specified')}")
                create_label(f"  - Format: {sticker_override.get('format', 'Not specified')}")
                create_label(f"  - Position: {sticker_override.get('position', 'Not specified')}")
        
        # Processing Metadata
        processing_meta = plate_data.get('processing_metadata', {})
        if processing_meta:
            create_label("PROCESSING METADATA:", bold=True, color='#FFD54F', pady_val=(8, 2))
            currently_processed = processing_meta.get('currently_processed', 'Unknown')
            requires_prefix = processing_meta.get('requires_prefix', False)
            requires_suffix = processing_meta.get('requires_suffix', False)
            verify_state = processing_meta.get('verify_state_abbreviation', True)
            all_numeric = processing_meta.get('all_numeric_plate', False)
            
            create_label(f"• Currently Processed: {currently_processed}")
            create_label(f"• Requires Prefix: {requires_prefix}")
            create_label(f"• Requires Suffix: {requires_suffix}")
            create_label(f"• Verify State Abbreviation: {verify_state}")
            create_label(f"• All Numeric Plate: {all_numeric}")
            
            dot_processing = processing_meta.get('dot_processing_type')
            if dot_processing:
                create_label(f"• DOT Processing Type: {dot_processing}")
                
            dot_dropdown = processing_meta.get('dot_dropdown_identifier')
            if dot_dropdown:
                create_label(f"• DOT Dropdown ID: {dot_dropdown}")
            
            visual_id = processing_meta.get('visual_identifier')
            if visual_id:
                create_label(f"• Visual Identifier: {visual_id}")
                
            vehicle_type = processing_meta.get('vehicle_type_identification')
            if vehicle_type:
                create_label(f"• Vehicle Type ID: {vehicle_type}")
        
        # Visual Identifiers and Processing Rules
        visual_identifier = plate_data.get('visual_identifier')
        processing_rules = plate_data.get('processing_rules')
        requires_prefix = plate_data.get('requires_prefix', False)
        
        if visual_identifier or processing_rules is not None:
            create_label("ADDITIONAL INFO:", bold=True, color='#FFD54F', pady_val=(8, 2))
            if visual_identifier:
                create_label(f"• Visual Identifier: {visual_identifier}")
            if processing_rules is not None:
                create_label(f"• Processing Rules: {processing_rules}")
            create_label(f"• Requires Prefix: {requires_prefix}")
        
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
        self.current_plate_type = None
        self.show_default_message()