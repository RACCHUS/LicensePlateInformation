"""
Utility functions for License Plate Information System
"""

import os
import json
from typing import Dict, List, Optional, Tuple
import re

def normalize_plate_text(plate_text: Optional[str]) -> str:
    """Normalize plate text for searching
    
    Args:
        plate_text: Raw plate text input
        
    Returns:
        Normalized uppercase text with only alphanumeric characters
    """
    if not plate_text:
        return ""
    
    # Convert to uppercase and remove non-alphanumeric except hyphens
    normalized = re.sub(r'[^A-Z0-9\-]', '', plate_text.upper())
    return normalized

def get_ambiguous_character_pairs() -> Dict[str, List[str]]:
    """Get mapping of commonly confused characters
    
    Returns:
        Dictionary mapping characters to list of confusing alternatives
    """
    return {
        '0': ['O'],
        'O': ['0'],
        '1': ['I', 'L'],
        'I': ['1', 'L'],
        'L': ['1', 'I'],
        '8': ['B'],
        'B': ['8'],
        '5': ['S'],
        'S': ['5'],
        '2': ['Z'],
        'Z': ['2'],
        '6': ['G'],
        'G': ['6']
    }

def generate_character_alternatives(char: str, state_rules: Optional[Dict] = None) -> List[str]:
    """Generate alternative characters for ambiguous input
    
    Args:
        char: Single character to find alternatives for
        state_rules: Optional state-specific rules to filter alternatives
        
    Returns:
        List of possible alternative characters
    """
    alternatives = [char]  # Always include original
    ambiguous_pairs = get_ambiguous_character_pairs()
    
    if char in ambiguous_pairs:
        for alt in ambiguous_pairs[char]:
            # Apply state-specific filtering if provided
            if state_rules:
                if char == '0' and alt == 'O' and not state_rules.get('allows_letter_o', True):
                    continue
                if char == 'O' and alt == '0' and not state_rules.get('uses_zero_for_o', True):
                    continue
            
            alternatives.append(alt)
    
    return list(set(alternatives))  # Remove duplicates

def expand_plate_with_alternatives(plate: str, state_rules: Optional[Dict] = None, max_combinations: int = 50) -> List[str]:
    """Expand plate text with character alternatives
    
    Args:
        plate: Input plate text
        state_rules: State-specific character rules
        max_combinations: Maximum number of combinations to generate
        
    Returns:
        List of possible plate text variations
    """
    if not plate:
        return []
    
    # Generate alternatives for each position
    position_alternatives = []
    for char in plate:
        if char.isalnum():
            alternatives = generate_character_alternatives(char, state_rules)
            position_alternatives.append(alternatives)
        else:
            position_alternatives.append([char])  # Keep non-alphanumeric as-is
    
    # Generate combinations (with limit to prevent explosion)
    combinations = ['']
    for alternatives in position_alternatives:
        new_combinations = []
        for combo in combinations:
            for alt in alternatives:
                new_combo = combo + alt
                new_combinations.append(new_combo)
                if len(new_combinations) >= max_combinations:
                    return new_combinations[:max_combinations]
        combinations = new_combinations
    
    return combinations

def validate_plate_pattern(plate: str, pattern: str) -> bool:
    """Check if plate matches a given pattern
    
    Args:
        plate: Plate text to validate
        pattern: Pattern to match against
        
    Pattern conventions:
        - Known literal prefixes: UG, CV, DV, GT (match exactly)
        - Standard patterns use placeholders:
          * A, B, C = any letter (placeholder)
          * 1, 2, 3, 4 = any digit (placeholder)
          * X = any letter or digit (wildcard)
          * - = literal hyphen
        - Single letter + numbers: T1234, F1234 = literal letter + placeholder digits
        
    Returns:
        True if plate matches pattern
    """
    if not plate or not pattern:
        return False
    
    plate = plate.upper().strip()
    pattern = pattern.upper().strip()
    
    # Check length match
    if len(plate) != len(pattern):
        return False
    
    # Known literal prefixes that should match exactly
    literal_prefixes = {
        'UG': 'University of Georgia',
        'GT': 'Georgia Tech', 
        'CV': 'Classic Vehicle',
        'DV': 'Disabled Veteran',
    }
    
    # Check for literal prefix patterns
    for prefix in literal_prefixes:
        if pattern.startswith(prefix):
            # This prefix must match exactly
            if not plate.startswith(prefix):
                return False
            # Validate the rest of the pattern
            return validate_plate_pattern(plate[len(prefix):], pattern[len(prefix):])
    
    # Check for single-letter literal patterns (T1234, F1234)
    if len(pattern) >= 2 and pattern[0].isalpha() and pattern[1].isdigit():
        # First character is literal, rest are digit placeholders
        if plate[0] != pattern[0]:
            return False
        # Check remaining digits
        for i in range(1, len(pattern)):
            if pattern[i].isdigit():
                if not plate[i].isdigit():
                    return False
            else:
                # Handle any other characters (shouldn't happen in this case)
                if plate[i] != pattern[i]:
                    return False
        return True
    
    # For all other patterns, treat as placeholders
    for i, (p_char, pat_char) in enumerate(zip(plate, pattern)):
        if pat_char == 'X':
            # X matches any letter or digit
            if not p_char.isalnum():
                return False
        elif pat_char == '-':
            # Literal hyphen
            if p_char != '-':
                return False
        elif pat_char.isalpha():
            # Pattern letter - treat as placeholder for any letter
            if not p_char.isalpha():
                return False
        elif pat_char.isdigit():
            # Pattern digit - treat as placeholder for any digit
            if not p_char.isdigit():
                return False
        else:
            # Any other character should match exactly
            if p_char != pat_char:
                return False
    
    return True

def score_plate_match(plate: str, state_data: Dict, plate_type: Optional[Dict] = None) -> float:
    """Score how well a plate matches state and type rules
    
    Args:
        plate: Plate text to score
        state_data: State information dictionary
        plate_type: Optional plate type information
        
    Returns:
        Score from 0.0 to 1.0 (higher is better match)
    """
    if not plate or state_data is None:
        return 0.0
    
    score = 0.0
    max_score = 0.0
    
    # Pattern match score (if plate type provided)
    if plate_type and plate_type.get('pattern'):
        max_score += 0.5
        if validate_plate_pattern(plate, plate_type['pattern']):
            score += 0.5
    
    # Character count score (if specified)
    if plate_type and plate_type.get('character_count'):
        max_score += 0.2
        expected_count = plate_type['character_count']
        actual_count = len(re.sub(r'[^A-Z0-9]', '', plate))
        if actual_count == expected_count:
            score += 0.2
        elif abs(actual_count - expected_count) <= 1:
            score += 0.1
    
    # Character rule compliance
    max_score += 0.3
    char_score = 0.0
    
    for char in plate:
        if char == 'O' and not state_data.get('allows_letter_o', True):
            char_score -= 0.1  # Penalty for disallowed letter O
        elif char == '0' and not state_data.get('uses_zero_for_o', True):
            char_score -= 0.1  # Penalty for disallowed zero
        else:
            char_score += 0.01  # Small bonus for allowed characters
    
    score += max(0, min(0.3, char_score))
    
    # Normalize score
    if max_score > 0:
        return min(1.0, max(0.0, score / max_score))
    return 0.0

def format_color_display(colors: List[str]) -> str:
    """Format color list for display
    
    Args:
        colors: List of hex color codes
        
    Returns:
        Formatted color string for display
    """
    if not colors:
        return "Not specified"
    
    color_names = {
        '#FF8C00': 'Orange',
        '#FFFFFF': 'White',
        '#000000': 'Black',
        '#FF0000': 'Red',
        '#0000FF': 'Blue',
        '#00FF00': 'Green',
        '#FFFF00': 'Yellow',
        '#FDB827': 'Gold',
        '#002868': 'Navy Blue',
        '#1B365D': 'Dark Blue',
        '#C60C30': 'Red',
        '#0033A0': 'Blue'
    }
    
    display_colors = []
    for color in colors[:3]:  # Limit to first 3 colors
        color_upper = color.upper()
        if color_upper in color_names:
            display_colors.append(color_names[color_upper])
        else:
            display_colors.append(color)
    
    return ", ".join(display_colors)

def get_image_path(base_path: str, state_abbrev: str, image_type: str, filename: Optional[str] = None) -> str:
    """Construct standardized image path
    
    Args:
        base_path: Base directory for images
        state_abbrev: State abbreviation (e.g., 'FL')
        image_type: Type of image ('plates', 'logos', 'characters')
        filename: Optional specific filename
        
    Returns:
        Constructed file path
    """
    path_parts = [base_path, 'images', state_abbrev.upper(), image_type]
    if filename:
        path_parts.append(filename)
    
    return os.path.join(*path_parts)

def ensure_data_directories(base_path: str) -> None:
    """Ensure all required data directories exist
    
    Args:
        base_path: Base application directory
    """
    required_dirs = [
        'data',
        'data/database',
        'data/images',
        'data/states',
        'data/user_images'
    ]
    
    for dir_name in required_dirs:
        dir_path = os.path.join(base_path, dir_name)
        os.makedirs(dir_path, exist_ok=True)

def load_json_file(file_path: str) -> Optional[Dict]:
    """Safely load JSON file
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Dictionary if successful, None if failed
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON file {file_path}: {e}")
        return None

def save_json_file(file_path: str, data: Dict) -> bool:
    """Safely save dictionary to JSON file
    
    Args:
        file_path: Path to save JSON file
        data: Dictionary to save
        
    Returns:
        True if successful, False if failed
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving JSON file {file_path}: {e}")
        return False