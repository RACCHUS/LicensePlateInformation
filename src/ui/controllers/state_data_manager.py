"""
State Data Manager for License Plate Information System.

Handles loading and providing state data from JSON files.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional, List

from PySide6.QtCore import QObject, Signal


class StateDataManager(QObject):
    """
    Manager for loading and accessing state license plate data.
    
    Wraps the JSON files in data/states/ and provides easy access
    to state information for UI panels.
    """
    
    # Signals
    state_loaded = Signal(str, dict)  # state_code, data
    
    # State code to filename mapping - All 60 jurisdictions
    STATE_FILENAME_MAP = {
        'AL': 'alabama', 'AK': 'alaska', 'AS': 'american_samoa', 'AZ': 'arizona',
        'AR': 'arkansas', 'AB': 'alberta', 'CA': 'california', 'CO': 'colorado',
        'CT': 'connecticut', 'DE': 'delaware', 'DM': 'diplomatic', 'FL': 'florida',
        'GA': 'georgia', 'GU': 'guam', 'HI': 'hawaii', 'ID': 'idaho',
        'IL': 'illinois', 'IN': 'indiana', 'IA': 'iowa', 'KS': 'kansas',
        'KY': 'kentucky', 'LA': 'louisiana', 'ME': 'maine', 'MD': 'maryland',
        'MA': 'massachusetts', 'MI': 'michigan', 'MN': 'minnesota', 'MS': 'mississippi',
        'MO': 'missouri', 'MT': 'montana', 'NE': 'nebraska', 'NV': 'nevada',
        'NH': 'new_hampshire', 'NJ': 'new_jersey', 'NM': 'new_mexico', 'NY': 'new_york',
        'NC': 'north_carolina', 'ND': 'north_dakota', 'MP': 'northern_mariana_islands',
        'OH': 'ohio', 'OK': 'oklahoma', 'ON': 'ontario', 'OR': 'oregon',
        'PA': 'pennsylvania', 'PR': 'puerto_rico', 'QC': 'quebec', 'RI': 'rhode_island',
        'SC': 'south_carolina', 'SD': 'south_dakota', 'TN': 'tennessee', 'TX': 'texas',
        'UG': 'us_government', 'VI': 'us_virgin_islands', 'UT': 'utah', 'VT': 'vermont',
        'VA': 'virginia', 'WA': 'washington', 'DC': 'washington_dc', 'WV': 'west_virginia',
        'WI': 'wisconsin', 'WY': 'wyoming',
        # Canadian provinces
        'BC': 'british_columbia', 'MB': 'manitoba', 'NB': 'new_brunswick',
        'NL': 'newfoundland', 'NS': 'nova_scotia', 'NT': 'northwest_territories',
        'NU': 'nunavut', 'PE': 'prince_edward_island', 'SK': 'saskatchewan', 'YT': 'yukon'
    }
    
    def __init__(self, parent=None, data_dir: str = "data/states"):
        super().__init__(parent)
        
        self.data_dir = Path(data_dir)
        self._cache: Dict[str, dict] = {}
    
    def get_state_data(self, state_code: str) -> Optional[dict]:
        """
        Load and return data for a state.
        
        Args:
            state_code: Two-letter state abbreviation (e.g., 'FL', 'CA')
            
        Returns:
            Dict with state data, or None if not found
        """
        if not state_code:
            return None
            
        state_code = state_code.upper()
        
        # Check cache first
        if state_code in self._cache:
            return self._cache[state_code]
        
        # Get filename
        filename_base = self.STATE_FILENAME_MAP.get(state_code, state_code.lower())
        filepath = self.data_dir / f"{filename_base}.json"
        
        if not filepath.exists():
            print(f"⚠️ State file not found: {filepath}")
            return None
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self._cache[state_code] = data
            self.state_loaded.emit(state_code, data)
            return data
            
        except Exception as e:
            print(f"⚠️ Error loading state data for {state_code}: {e}")
            return None
    
    def get_state_info_summary(self, state_code: str) -> Dict[str, Any]:
        """
        Get summary info for the State Info panel.
        
        Returns key fields: name, slogan, colors, font, main_logo, etc.
        """
        data = self.get_state_data(state_code)
        if not data:
            return {}
        
        return {
            'name': data.get('name', state_code),
            'abbreviation': data.get('abbreviation', state_code),
            'slogan': data.get('slogan', ''),
            'primary_colors': data.get('primary_colors', []),
            'main_font': data.get('main_font', ''),
            'main_logo': data.get('main_logo', ''),
            'main_plate_text': data.get('main_plate_text', ''),
            'notes': data.get('notes', ''),
            'sticker_format': data.get('sticker_format', {}),
        }
    
    def get_character_rules(self, state_code: str) -> Dict[str, Any]:
        """
        Get character rules for the Character Rules panel.
        
        Returns: O/0 usage, stacked chars, slanted chars, restrictions, etc.
        """
        data = self.get_state_data(state_code)
        if not data:
            return {}
        
        # Get character formatting
        char_format = data.get('character_formatting', {}) or {}
        
        # Get processing metadata rules
        proc_meta = data.get('processing_metadata', {}) or {}
        global_rules = proc_meta.get('global_rules', {}) or {}
        stacked_rules = global_rules.get('stacked_characters', {}) or {}
        
        return {
            'allows_letter_o': data.get('allows_letter_o', True),
            'uses_zero_for_o': data.get('uses_zero_for_o', False),
            'zero_is_slashed': data.get('zero_is_slashed', False),
            'stacked_characters': char_format.get('stacked_characters'),
            'slanted_characters': char_format.get('slanted_characters'),
            'slant_direction': char_format.get('slant_direction'),
            'stack_position': char_format.get('stack_position'),
            'character_restrictions': global_rules.get('character_restrictions', ''),
            'no_letter_o': global_rules.get('no_letter_o', ''),
            'stacked_include': stacked_rules.get('include', []),
            'stacked_omit': stacked_rules.get('omit', []),
            'stacked_position': stacked_rules.get('position', ''),
            'stacked_notes': stacked_rules.get('notes', ''),
        }
    
    def get_plate_types(self, state_code: str) -> List[Dict[str, Any]]:
        """
        Get list of plate types for the Plate Type panel.
        
        Returns list of plate type dicts with name, description, pattern, etc.
        """
        data = self.get_state_data(state_code)
        if not data:
            return []
        
        plate_types = data.get('plate_types', [])
        if not plate_types:
            return []
        
        # Return simplified plate type info
        result = []
        for pt in plate_types:
            if isinstance(pt, dict):
                result.append({
                    'type_name': pt.get('type_name', 'Unknown'),
                    'description': pt.get('description', ''),
                    'code_numbers': pt.get('code_numbers', []),
                    'currently_processed': pt.get('currently_processed', True),
                    'character_modifications': pt.get('character_modifications'),
                    'visual_identifier': pt.get('visual_identifier', ''),
                    'vehicle_types': pt.get('vehicle_types', []),
                })
        
        return result
    
    def get_all_state_codes(self) -> List[str]:
        """Get list of all available state codes."""
        return list(self.STATE_FILENAME_MAP.keys())
