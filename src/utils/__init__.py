"""
Utilities module for License Plate Information System
"""

from .helpers import (
    normalize_plate_text,
    get_ambiguous_character_pairs,
    generate_character_alternatives,
    expand_plate_with_alternatives,
    validate_plate_pattern,
    score_plate_match,
    format_color_display,
    get_image_path,
    ensure_data_directories,
    load_json_file,
    save_json_file
)

__all__ = [
    'normalize_plate_text',
    'get_ambiguous_character_pairs',
    'generate_character_alternatives',
    'expand_plate_with_alternatives',
    'validate_plate_pattern',
    'score_plate_match',
    'format_color_display',
    'get_image_path',
    'ensure_data_directories',
    'load_json_file',
    'save_json_file'
]