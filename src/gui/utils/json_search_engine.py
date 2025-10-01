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
        
        # State code to filename mapping
        self.state_filename_map = {
            'FL': 'florida.json',
            'AL': 'alabama.json',
            'GA': 'georgia.json',
            'CA': 'california.json',
            'TX': 'texas.json',
            'NY': 'new_york.json',
            'PA': 'pennsylvania.json',
            # Add more as needed
        }
        
        # Define searchable field mappings (easily expandable)
        self.field_mappings = {
            'fonts': ['font', 'typeface', 'text_style'],
            'slogans': ['slogan', 'motto', 'tagline', 'text'],
            'colors': ['color', 'background_color', 'text_color', 'accent_color'],
            'logos': ['logo', 'emblem', 'symbol', 'graphic'],
            'text': ['text', 'characters', 'lettering', 'numbers'],
            'background': ['background', 'base', 'substrate'],
            'design': ['design', 'pattern', 'style', 'artwork'],
            'year': ['year', 'period', 'era', 'issued'],
            'type': ['type', 'category', 'classification', 'class']
        }
        
    def load_state_data(self, state_code: str) -> Dict[str, Any]:
        """Load JSON data for a specific state"""
        if state_code in self.loaded_data:
            return self.loaded_data[state_code]
            
        # Try to load from file using correct filename
        try:
            filename = self.state_filename_map.get(state_code, f"{state_code.lower()}.json")
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
            
        # Determine which states to search - expand to include more states
        if state_filter:
            states_to_search = [state_filter]
        else:
            # Search common states, focusing on ones we have data for
            states_to_search = ['FL', 'AL', 'GA', 'CA', 'TX', 'NY', 'PA']
        
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
        
        # Then search through plates
        plates = data.get('plate_types', [])  # Changed from 'plates' to 'plate_types' to match FL structure
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
        
        # Search specific top-level fields
        searchable_state_fields = {
            'slogan': data.get('slogan', ''),
            'name': data.get('name', ''),
            'abbreviation': data.get('abbreviation', ''),
            'notes': data.get('notes', '')
        }
        
        for field_name, field_value in searchable_state_fields.items():
            if isinstance(field_value, str) and query_lower in field_value.lower():
                matches.append({
                    'field': field_name,
                    'value': field_value,
                    'match_type': 'exact'
                })
        
        return matches
        
    def _get_search_fields(self, category: str) -> List[str]:
        """Get list of fields to search based on category"""
        if category == 'all':
            # Return all possible fields
            all_fields = []
            for field_list in self.field_mappings.values():
                all_fields.extend(field_list)
            return list(set(all_fields))  # Remove duplicates
        else:
            return self.field_mappings.get(category, [])
            
    def _find_matches_in_plate(self, plate: Dict[str, Any], query: str, fields: List[str]) -> List[Dict]:
        """Find matches within a single plate record"""
        matches = []
        
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