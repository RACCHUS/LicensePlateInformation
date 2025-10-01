"""
JSON Search Engine - Handles searching through license plate JSON data
"""

import json
import re
from typing import Dict, List, Any, Optional
from pathlib import Path


class JSONSearchEngine:
    """Advanced search engine for license plate JSON data"""
    
    def __init__(self, data_directory: Optional[str] = None):
        self.data_directory = data_directory or "data/states"
        self.loaded_data: Dict[str, Any] = {}
        self.search_cache: Dict[str, List[Dict]] = {}
        
        # State code to filename mapping - All 60 jurisdictions
        self.state_filename_map = {
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
            'PA': 'pennsylvania', 'PR': 'puerto_rico', 'RI': 'rhode_island',
            'SC': 'south_carolina', 'SD': 'south_dakota', 'TN': 'tennessee', 'TX': 'texas',
            'UG': 'us_government', 'VI': 'us_virgin_islands', 'UT': 'utah', 'VT': 'vermont',
            'VA': 'virginia', 'WA': 'washington', 'DC': 'washington_dc', 'WV': 'west_virginia',
            'WI': 'wisconsin', 'WY': 'wyoming'
        }
        
        # Define searchable field mappings (easily expandable)
        self.field_mappings = {
            'fonts': ['font', 'typeface', 'text_style', 'main_font'],
            'slogans': ['slogan', 'motto', 'tagline', 'text'],
            'colors': ['color', 'background_color', 'text_color', 'accent_color', 'primary_colors'],
            'logos': ['logo', 'emblem', 'symbol', 'graphic', 'main_logo'],
            'text': ['text', 'characters', 'lettering', 'numbers', 'main_plate_text'],
            'background': ['background', 'base', 'substrate'],
            'design': ['design', 'pattern', 'style', 'artwork'],
            'year': ['year', 'period', 'era', 'issued'],
            'type': ['type', 'category', 'classification', 'class', 'type_name'],
            'handling_rules': [
                'uses_zero_for_o', 'allows_letter_o', 'zero_is_slashed',
                'character_formatting', 'stacked_characters', 'slanted_characters',
                'character_restrictions', 'vertical_handling', 'omit_characters',
                'character_modifications', 'stack_position', 'slant_direction'
            ],
            'processing': [
                'processing_metadata', 'processing_type', 'dot_processing_type',
                'character_modifications', 'global_rules', 'currently_processed'
            ],
            'restrictions': [
                'character_restrictions', 'allows_letter_o', 'uses_zero_for_o',
                'omit_characters', 'vertical_handling'
            ]
        }
        
    def get_all_state_codes(self) -> List[str]:
        """Get list of all available state codes from state_filename_map"""
        return list(self.state_filename_map.keys())
    
    def load_state_data(self, state_code: str) -> Dict[str, Any]:
        """Load JSON data for a specific state"""
        if state_code in self.loaded_data:
            return self.loaded_data[state_code]
            
        # Try to load from file using correct filename
        try:
            filename_base = self.state_filename_map.get(state_code, state_code.lower())
            filename = f"{filename_base}.json"
            data_file = Path(self.data_directory) / filename
            
            if data_file.exists():
                with open(data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.loaded_data[state_code] = data
                    print(f"✅ Loaded real data for {state_code} from {filename}")
                    return data
            else:
                print(f"⚠️ File not found: {data_file}")
        except Exception as e:
            print(f"⚠️ Could not load data for {state_code}: {e}")
            
        # Return sample data structure for demonstration
        return self._get_sample_data(state_code)
        
    def _get_sample_data(self, state_code: str) -> Dict[str, Any]:
        """Generate sample data structure for demonstration"""
        sample_data = {
            "state_info": {
                "code": state_code,
                "name": self._get_state_name(state_code),
                "processing_type": "Digital Processing" if state_code in ['FL', 'CA', 'TX'] else "Standard Processing"
            },
            "plates": [
                {
                    "type": "standard",
                    "plate_type": "Standard Issue",
                    "year": "2020",
                    "colors": ["blue", "white"],
                    "text": f"{state_code} sample text",
                    "font": "Arial",
                    "slogan": f"Sample {state_code} slogan",
                    "background": "gradient",
                    "design": "modern",
                    "logo": "state symbol",
                    "processing_type": "Digital Processing"
                },
                {
                    "type": "specialty", 
                    "plate_type": "Specialty Plate",
                    "year": "2019",
                    "colors": ["green", "gold"],
                    "text": "SPECIAL",
                    "font": "Georgia",
                    "slogan": "Special edition",
                    "background": "solid",
                    "design": "classic",
                    "logo": "custom emblem",
                    "processing_type": "Manual Processing"
                },
                {
                    "type": "vanity",
                    "plate_type": "Personalized Plate", 
                    "year": "2021",
                    "colors": ["red", "white"],
                    "text": "CUSTOM",
                    "font": "Impact",
                    "slogan": "Your choice",
                    "background": "solid",
                    "design": "bold",
                    "logo": "custom text",
                    "processing_type": "Digital Processing"
                }
            ]
        }
        
        self.loaded_data[state_code] = sample_data
        return sample_data
        
    def _get_state_name(self, state_code: str) -> str:
        """Get full state name from code"""
        state_names = {
            'FL': 'Florida', 'CA': 'California', 'TX': 'Texas', 'NY': 'New York',
            'PA': 'Pennsylvania', 'IL': 'Illinois', 'OH': 'Ohio', 'GA': 'Georgia',
            'NC': 'North Carolina', 'MI': 'Michigan'
        }
        return state_names.get(state_code, f"State {state_code}")
        
    def search(self, query: str, category: str = 'all', state_filter: Optional[str] = None) -> List[Dict]:
        """Perform comprehensive search across JSON data"""
        results = []
        search_key = f"{query}_{category}_{state_filter}"
        
        # Check cache first
        if search_key in self.search_cache:
            return self.search_cache[search_key]
            
        # Determine which states to search - all 60 jurisdictions
        if state_filter:
            states_to_search = [state_filter]
        else:
            # Search all available states
            states_to_search = self.get_all_state_codes()
        
        for state_code in states_to_search:
            state_data = self.load_state_data(state_code)
            state_results = self._search_state_data(query, category, state_code, state_data)
            results.extend(state_results)
            
        # Cache results
        self.search_cache[search_key] = results
        return results
        
    def _search_state_data(self, query: str, category: str, state_code: str, data: Dict[str, Any]) -> List[Dict]:
        """Search within a single state's data"""
        results = []
        query_lower = query.lower()
        
        # Get fields to search based on category
        fields_to_search = self._get_search_fields(category)
        
        # First, search top-level state fields (like slogan, name, etc.)
        state_matches = self._find_matches_in_state_info(data, query_lower, fields_to_search)
        if state_matches:
            for match in state_matches:
                result = {
                    'state': state_code,
                    'state_name': data.get('name', state_code),
                    'field': match['field'],
                    'value': match['value'],
                    'match_type': 'state_info'
                }
                results.append(result)
        
        # Then search through plates - try both 'plate_types' and 'plates' for compatibility
        plates = data.get('plate_types', data.get('plates', []))
        for i, plate in enumerate(plates):
            matches = self._find_matches_in_plate(plate, query_lower, fields_to_search)
            
            if matches:
                for match in matches:
                    result = {
                        'state': state_code,
                        'state_name': data.get('name', state_code),
                        'plate_type': plate.get('type_name', f"Plate {i+1}"),
                        'field': match['field'],
                        'value': match['value'],
                        'match_type': 'plate_type'
                    }
                    results.append(result)
                
        return results
    
    def _find_matches_in_state_info(self, data: Dict[str, Any], query_lower: str, fields_to_search: List[str]) -> List[Dict]:
        """Find matches in top-level state information"""
        matches = []
        
        # Search specific top-level fields - ONLY if they match the category filter
        searchable_state_fields = {
            'slogan': data.get('slogan', ''),
            'name': data.get('name', ''),
            'abbreviation': data.get('abbreviation', ''),
            'notes': data.get('notes', '')
        }
        
        for field_name, field_value in searchable_state_fields.items():
            # Check if this field is allowed by the category filter
            if 'all' in fields_to_search or field_name in fields_to_search:
                if isinstance(field_value, str) and query_lower in field_value.lower():
                    matches.append({
                        'field': field_name,
                        'value': field_value,
                        'match_type': 'exact'
                    })
        
        # Search boolean handling rule fields
        if 'uses_zero_for_o' in fields_to_search or 'all' in fields_to_search:
            if 'uses_zero_for_o' in data:
                bool_val = data['uses_zero_for_o']
                searchable_text = f"uses zero for o: {bool_val}" if bool_val else "allows letter o"
                if query_lower in searchable_text.lower():
                    matches.append({
                        'field': 'uses_zero_for_o',
                        'value': f"Uses '0' instead of 'O': {bool_val}",
                        'match_type': 'boolean'
                    })
        
        if 'allows_letter_o' in fields_to_search or 'all' in fields_to_search:
            if 'allows_letter_o' in data:
                bool_val = data['allows_letter_o']
                searchable_text = f"allows letter o: {bool_val}" if bool_val else "does not allow letter o"
                if query_lower in searchable_text.lower():
                    matches.append({
                        'field': 'allows_letter_o',
                        'value': f"Allows letter 'O': {bool_val}",
                        'match_type': 'boolean'
                    })
        
        if 'zero_is_slashed' in fields_to_search or 'all' in fields_to_search:
            if 'zero_is_slashed' in data:
                bool_val = data['zero_is_slashed']
                searchable_text = f"zero is slashed: {bool_val}"
                if query_lower in searchable_text.lower():
                    matches.append({
                        'field': 'zero_is_slashed',
                        'value': f"Zero is slashed: {bool_val}",
                        'match_type': 'boolean'
                    })
        
        # Search character_formatting fields
        if 'character_formatting' in data:
            char_fmt = data['character_formatting']
            if isinstance(char_fmt, dict):
                for fmt_field, fmt_value in char_fmt.items():
                    if isinstance(fmt_value, str) and query_lower in fmt_value.lower():
                        matches.append({
                            'field': f'character_formatting.{fmt_field}',
                            'value': fmt_value,
                            'match_type': 'nested'
                        })
                    elif isinstance(fmt_value, bool):
                        searchable_text = f"{fmt_field}: {fmt_value}"
                        if query_lower in searchable_text.lower():
                            matches.append({
                                'field': f'character_formatting.{fmt_field}',
                                'value': f"{fmt_field.replace('_', ' ').title()}: {fmt_value}",
                                'match_type': 'boolean'
                            })
        
        # Search processing_metadata and nested fields
        if 'processing_metadata' in data:
            proc_meta = data['processing_metadata']
            if isinstance(proc_meta, dict) and 'global_rules' in proc_meta:
                global_rules = proc_meta['global_rules']
                if isinstance(global_rules, dict):
                    # Search string fields in global_rules
                    for rule_field in ['character_restrictions', 'vertical_handling', 'omit_characters', 'font_changes']:
                        if rule_field in global_rules:
                            rule_value = global_rules[rule_field]
                            if isinstance(rule_value, str) and query_lower in rule_value.lower():
                                matches.append({
                                    'field': f'processing_metadata.{rule_field}',
                                    'value': rule_value,
                                    'match_type': 'nested'
                                })
                    
                    # Search stacked_characters include/omit lists
                    if 'stacked_characters' in global_rules:
                        stacked = global_rules['stacked_characters']
                        if isinstance(stacked, dict):
                            # Search include list
                            if 'include' in stacked and isinstance(stacked['include'], list):
                                for item in stacked['include']:
                                    if isinstance(item, str) and query_lower in item.lower():
                                        matches.append({
                                            'field': 'stacked_characters.include',
                                            'value': f"Include: {', '.join(stacked['include'])}",
                                            'match_type': 'array'
                                        })
                                        break
                            
                            # Search omit list
                            if 'omit' in stacked and isinstance(stacked['omit'], list):
                                for item in stacked['omit']:
                                    if isinstance(item, str) and query_lower in item.lower():
                                        matches.append({
                                            'field': 'stacked_characters.omit',
                                            'value': f"Omit: {', '.join(stacked['omit'])}",
                                            'match_type': 'array'
                                        })
                                        break
                            
                            # Search other stacked_characters fields
                            for stacked_field in ['position', 'notes']:
                                if stacked_field in stacked:
                                    stacked_value = stacked[stacked_field]
                                    if isinstance(stacked_value, str) and query_lower in stacked_value.lower():
                                        matches.append({
                                            'field': f'stacked_characters.{stacked_field}',
                                            'value': stacked_value,
                                            'match_type': 'nested'
                                        })
        
        return matches
        
    def _get_search_fields(self, category: str) -> List[str]:
        """Get list of fields to search based on category"""
        if category == 'all':
            # Return 'all' as a special marker to search everything
            return ['all']
        else:
            return self.field_mappings.get(category, [])
            
    def _find_matches_in_plate(self, plate: Dict[str, Any], query: str, fields: List[str]) -> List[Dict]:
        """Find matches within a single plate record"""
        matches = []
        
        # If searching 'all', search common plate fields directly
        if 'all' in fields:
            searchable_fields = ['type_name', 'pattern', 'description', 'category', 'subtype', 
                               'processing_type', 'code_number']
            for field in searchable_fields:
                if field in plate:
                    value = plate[field]
                    if isinstance(value, str) and query in value.lower():
                        matches.append({
                            'field': field,
                            'value': value,
                            'match_type': 'exact' if query == value.lower() else 'partial'
                        })
        else:
            # Search specific fields
            for field in fields:
                if field in plate:
                    value = plate[field]
                    if isinstance(value, str) and query in value.lower():
                        matches.append({
                            'field': field,
                            'value': value,
                            'match_type': 'exact' if query == value.lower() else 'partial'
                        })
                    elif isinstance(value, list):
                        for item in value:
                            if isinstance(item, str) and query in item.lower():
                                matches.append({
                                    'field': field,
                                    'value': item,
                                    'match_type': 'list_item'
                                })
        
        # Search nested plate_characteristics fields - respect category filter
        if 'plate_characteristics' in plate:
            plate_chars = plate['plate_characteristics']
            if isinstance(plate_chars, dict):
                # Search direct string fields in plate_characteristics
                for char_field in ['font', 'logo', 'plate_text']:
                    # Only search if 'all' or if the field is in the allowed fields for this category
                    if 'all' in fields or char_field in fields:
                        if char_field in plate_chars:
                            char_value = plate_chars[char_field]
                            if isinstance(char_value, str) and query in char_value.lower():
                                matches.append({
                                    'field': f'plate_characteristics.{char_field}',
                                    'value': char_value,
                                    'match_type': 'nested'
                                })
                
                # Search design_variants array - only if 'all' or 'design' category
                if 'all' in fields or 'design' in fields or 'design_variants' in fields:
                    if 'design_variants' in plate_chars:
                        design_variants = plate_chars['design_variants']
                        if isinstance(design_variants, list):
                            for variant in design_variants:
                                if isinstance(variant, str) and query in variant.lower():
                                    matches.append({
                                        'field': 'plate_characteristics.design_variants',
                                        'value': f"Design variant: {variant}",
                                        'match_type': 'array'
                                    })
                                    break  # Only report once per plate type
                
                # Search character_formatting nested object
                if 'character_formatting' in plate_chars:
                    char_fmt = plate_chars['character_formatting']
                    if isinstance(char_fmt, dict):
                        for fmt_field, fmt_value in char_fmt.items():
                            if isinstance(fmt_value, str) and query in fmt_value.lower():
                                matches.append({
                                    'field': f'character_formatting.{fmt_field}',
                                    'value': fmt_value,
                                    'match_type': 'nested'
                                })
        
        # Search processing_metadata at plate level
        if 'processing_metadata' in plate:
            proc_meta = plate['processing_metadata']
            if isinstance(proc_meta, dict):
                for proc_field in ['character_modifications', 'visual_identifier']:
                    if proc_field in proc_meta:
                        proc_value = proc_meta[proc_field]
                        if isinstance(proc_value, str) and query in proc_value.lower():
                            matches.append({
                                'field': f'processing_metadata.{proc_field}',
                                'value': proc_value,
                                'match_type': 'nested'
                            })
                            
        return matches
        
    def get_suggestions(self, partial_query: str, category: str = 'all') -> List[str]:
        """Get search suggestions based on partial query and category"""
        suggestions = []
        
        # Category-specific suggestions
        if category == 'colors':
            color_terms = ['blue', 'red', 'white', 'green', 'yellow', 'black', 'orange', 'purple', 'rainbow', 'gradient']
            suggestions = [c for c in color_terms if partial_query.lower() in c.lower()]
        elif category == 'fonts':
            font_terms = ['Arial', 'Times New Roman', 'Helvetica', 'Georgia', 'Verdana', 'Impact', 'Custom']
            suggestions = [f for f in font_terms if partial_query.lower() in f.lower()]
        elif category == 'slogans':
            slogan_terms = ['Sunshine State', 'The Natural State', 'Empire State', 'Golden State', 'Lone Star State']
            suggestions = [s for s in slogan_terms if partial_query.lower() in s.lower()]
        elif category == 'logos':
            logo_terms = ['palm tree', 'mountain', 'star', 'eagle', 'sun', 'flag', 'seal', 'emblem']
            suggestions = [l for l in logo_terms if partial_query.lower() in l.lower()]
        else:
            # General suggestions
            general_terms = ['standard', 'specialty', 'vanity', 'commercial', 'motorcycle', 'trailer']
            suggestions = [g for g in general_terms if partial_query.lower() in g.lower()]
            
        return suggestions[:5]  # Return top 5
        
    def add_search_category(self, category: str, fields: List[str]):
        """Add new search category (for easy expansion)"""
        self.field_mappings[category] = fields
        print(f"➕ Added search category '{category}' with fields: {fields}")
        
    def clear_cache(self):
        """Clear search cache"""
        self.search_cache.clear()
        print("🔄 Search cache cleared")
        
    def get_category_stats(self, state_filter: Optional[str] = None) -> Dict[str, int]:
        """Get statistics about available data in each category"""
        stats = {}
        states_to_check = [state_filter] if state_filter else ['FL', 'CA', 'TX', 'NY', 'PA']
        
        for category in self.field_mappings.keys():
            count = 0
            for state_code in states_to_check:
                state_data = self.load_state_data(state_code)
                plates = state_data.get('plates', [])
                for plate in plates:
                    fields = self._get_search_fields(category)
                    if any(field in plate for field in fields):
                        count += 1
            stats[category] = count
            
        return stats