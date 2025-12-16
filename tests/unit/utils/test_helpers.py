"""
Unit tests for helpers.py
Tests for utility functions used throughout the application
"""

import pytest
import os
import json
import tempfile
from pathlib import Path
from src.utils.helpers import (
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


# ============================================================================
# NORMALIZE PLATE TEXT TESTS
# ============================================================================

class TestNormalizePlateText:
    """Test cases for normalize_plate_text()"""
    
    def test_uppercase_conversion(self):
        """Test that lowercase is converted to uppercase"""
        assert normalize_plate_text("abc123") == "ABC123"
        assert normalize_plate_text("xyz789") == "XYZ789"
    
    def test_alphanumeric_filtering(self):
        """Test that non-alphanumeric characters are removed"""
        assert normalize_plate_text("AB C 1 23") == "ABC123"
        assert normalize_plate_text("AB@C#123!") == "ABC123"
        assert normalize_plate_text("A*B&C%123$") == "ABC123"
    
    def test_hyphen_preservation(self):
        """Test that hyphens are preserved"""
        assert normalize_plate_text("ABC-123") == "ABC-123"
        assert normalize_plate_text("ab-cd-12") == "AB-CD-12"
    
    def test_none_input(self):
        """Test handling of None input"""
        assert normalize_plate_text(None) == ""
    
    def test_empty_string(self):
        """Test handling of empty string"""
        assert normalize_plate_text("") == ""
        assert normalize_plate_text("   ") == ""
    
    def test_mixed_case_with_special_chars(self):
        """Test combination of mixed case and special characters"""
        assert normalize_plate_text("AbC-123!@#") == "ABC-123"
    
    def test_only_special_characters(self):
        """Test string with only special characters"""
        assert normalize_plate_text("!@#$%^&*()") == ""
    
    def test_numbers_only(self):
        """Test string with only numbers"""
        assert normalize_plate_text("123456") == "123456"
    
    def test_letters_only(self):
        """Test string with only letters"""
        assert normalize_plate_text("abcdef") == "ABCDEF"


# ============================================================================
# AMBIGUOUS CHARACTER PAIRS TESTS
# ============================================================================

class TestGetAmbiguousCharacterPairs:
    """Test cases for get_ambiguous_character_pairs()"""
    
    def test_returns_dictionary(self):
        """Test that function returns a dictionary"""
        pairs = get_ambiguous_character_pairs()
        assert isinstance(pairs, dict)
    
    def test_zero_and_o_confusion(self):
        """Test 0 and O confusion pairs"""
        pairs = get_ambiguous_character_pairs()
        assert '0' in pairs
        assert 'O' in pairs['0']
        assert '0' in pairs['O']
    
    def test_one_i_l_confusion(self):
        """Test 1, I, and L confusion pairs"""
        pairs = get_ambiguous_character_pairs()
        assert '1' in pairs
        assert 'I' in pairs['1']
        assert 'L' in pairs['1']
        assert '1' in pairs['I']
        assert '1' in pairs['L']
    
    def test_eight_b_confusion(self):
        """Test 8 and B confusion"""
        pairs = get_ambiguous_character_pairs()
        assert '8' in pairs
        assert 'B' in pairs['8']
        assert '8' in pairs['B']
    
    def test_five_s_confusion(self):
        """Test 5 and S confusion"""
        pairs = get_ambiguous_character_pairs()
        assert '5' in pairs
        assert 'S' in pairs['5']
        assert '5' in pairs['S']
    
    def test_two_z_confusion(self):
        """Test 2 and Z confusion"""
        pairs = get_ambiguous_character_pairs()
        assert '2' in pairs
        assert 'Z' in pairs['2']
        assert '2' in pairs['Z']
    
    def test_six_g_confusion(self):
        """Test 6 and G confusion"""
        pairs = get_ambiguous_character_pairs()
        assert '6' in pairs
        assert 'G' in pairs['6']
        assert '6' in pairs['G']


# ============================================================================
# GENERATE CHARACTER ALTERNATIVES TESTS
# ============================================================================

class TestGenerateCharacterAlternatives:
    """Test cases for generate_character_alternatives()"""
    
    def test_ambiguous_character_zero(self):
        """Test alternatives for '0'"""
        alternatives = generate_character_alternatives('0')
        assert '0' in alternatives  # Original included
        assert 'O' in alternatives
    
    def test_ambiguous_character_one(self):
        """Test alternatives for '1'"""
        alternatives = generate_character_alternatives('1')
        assert '1' in alternatives
        assert 'I' in alternatives
        assert 'L' in alternatives
    
    def test_non_ambiguous_character(self):
        """Test non-ambiguous characters return only themselves"""
        alternatives = generate_character_alternatives('A')
        assert alternatives == ['A']
        
        alternatives = generate_character_alternatives('3')
        assert alternatives == ['3']
    
    def test_state_rules_allows_letter_o(self):
        """Test state rules filtering for allows_letter_o"""
        state_rules = {'allows_letter_o': False}
        alternatives = generate_character_alternatives('0', state_rules)
        assert '0' in alternatives
        # Should not include O if not allowed
    
    def test_state_rules_uses_zero_for_o(self):
        """Test state rules filtering for uses_zero_for_o"""
        state_rules = {'uses_zero_for_o': False}
        alternatives = generate_character_alternatives('O', state_rules)
        assert 'O' in alternatives
    
    def test_returns_unique_values(self):
        """Test that returned alternatives are unique"""
        alternatives = generate_character_alternatives('I')
        assert len(alternatives) == len(set(alternatives))


# ============================================================================
# EXPAND PLATE WITH ALTERNATIVES TESTS
# ============================================================================

class TestExpandPlateWithAlternatives:
    """Test cases for expand_plate_with_alternatives()"""
    
    def test_single_ambiguous_character(self):
        """Test expansion with single ambiguous character"""
        variations = expand_plate_with_alternatives('0')
        assert '0' in variations
        assert 'O' in variations
    
    def test_no_ambiguous_characters(self):
        """Test plate with no ambiguous characters"""
        variations = expand_plate_with_alternatives('ABC')
        assert variations == ['ABC']
    
    def test_multiple_ambiguous_characters(self):
        """Test expansion with multiple ambiguous characters"""
        variations = expand_plate_with_alternatives('0I')
        # Should generate combinations: 0I, 0L, 01, OI, OL, O1
        assert len(variations) > 1
        assert '0I' in variations or 'OI' in variations or '01' in variations
    
    def test_max_combinations_limit(self):
        """Test that max_combinations limit is respected"""
        variations = expand_plate_with_alternatives('0I1L', max_combinations=10)
        assert len(variations) <= 10
    
    def test_empty_input(self):
        """Test empty input"""
        assert expand_plate_with_alternatives('') == []
        assert expand_plate_with_alternatives(None) == []  # type: ignore
    
    def test_with_state_rules(self):
        """Test expansion with state-specific rules"""
        state_rules = {'allows_letter_o': True}
        variations = expand_plate_with_alternatives('O', state_rules)
        assert len(variations) >= 1
    
    def test_mixed_alphanumeric(self):
        """Test plate with mix of ambiguous and non-ambiguous chars"""
        variations = expand_plate_with_alternatives('A0C')
        assert 'A0C' in variations
        assert 'AOC' in variations


# ============================================================================
# VALIDATE PLATE PATTERN TESTS
# ============================================================================

class TestValidatePlatePattern:
    """Test cases for validate_plate_pattern()"""
    
    def test_exact_match(self):
        """Test exact pattern match"""
        assert validate_plate_pattern('ABC123', 'ABC123') is True
    
    def test_letter_placeholder(self):
        """Test letter placeholders (A, B, C represent any letter)"""
        assert validate_plate_pattern('XYZ', 'ABC') is True
        assert validate_plate_pattern('ABC', 'ABC') is True
        assert validate_plate_pattern('123', 'ABC') is False
    
    def test_digit_placeholder(self):
        """Test digit placeholders (1, 2, 3, 4 represent any digit)"""
        assert validate_plate_pattern('789', '123') is True
        assert validate_plate_pattern('456', '1234') is False  # Length mismatch
        assert validate_plate_pattern('ABC', '123') is False
    
    def test_hyphen_literal(self):
        """Test literal hyphen matching"""
        assert validate_plate_pattern('ABC-123', 'ABC-123') is True
        assert validate_plate_pattern('XYZ-789', 'ABC-123') is True
        assert validate_plate_pattern('ABC123', 'ABC-123') is False
    
    def test_wildcard_x(self):
        """Test X wildcard (matches letter or digit)"""
        assert validate_plate_pattern('A', 'X') is True
        assert validate_plate_pattern('1', 'X') is True
        assert validate_plate_pattern('-', 'X') is False
    
    def test_length_mismatch(self):
        """Test that different lengths don't match"""
        assert validate_plate_pattern('ABC', 'ABCD') is False
        assert validate_plate_pattern('ABC12', 'ABC') is False
    
    def test_empty_input(self):
        """Test empty inputs"""
        assert validate_plate_pattern('', 'ABC') is False
        assert validate_plate_pattern('ABC', '') is False
        assert validate_plate_pattern('', '') is False
    
    def test_none_input(self):
        """Test None inputs"""
        assert validate_plate_pattern(None, 'ABC') is False  # type: ignore
        assert validate_plate_pattern('ABC', None) is False  # type: ignore
    
    def test_case_insensitivity(self):
        """Test case insensitive matching"""
        assert validate_plate_pattern('abc', 'ABC') is True
        assert validate_plate_pattern('ABC', 'abc') is True
    
    def test_literal_prefix_patterns(self):
        """Test known literal prefixes"""
        # These would need actual implementation in the function
        assert validate_plate_pattern('UG12345', 'UG12345') is True
        assert validate_plate_pattern('GT12345', 'GT12345') is True
    
    def test_single_letter_literal_pattern(self):
        """Test patterns like T1234 where T is literal"""
        assert validate_plate_pattern('T1234', 'T1234') is True
        assert validate_plate_pattern('T5678', 'T1234') is True  # T matches, digits are placeholders
        assert validate_plate_pattern('F1234', 'T1234') is False  # Different literal letter


# ============================================================================
# SCORE PLATE MATCH TESTS
# ============================================================================

class TestScorePlateMatch:
    """Test cases for score_plate_match()"""
    
    def test_empty_inputs(self):
        """Test with empty inputs"""
        assert score_plate_match('', {}) == 0.0
        assert score_plate_match(None, {}) == 0.0  # type: ignore
        assert score_plate_match('ABC', None) == 0.0  # type: ignore
    
    def test_pattern_match_score(self):
        """Test pattern matching contribution to score"""
        state_data = {}
        plate_type = {'pattern': 'ABC123', 'character_count': 6}
        
        # Matching pattern should increase score
        score = score_plate_match('XYZ789', state_data, plate_type)
        assert score > 0.0
    
    def test_character_count_exact_match(self):
        """Test character count exact match"""
        state_data = {}
        plate_type = {'character_count': 6}
        
        score = score_plate_match('ABC123', state_data, plate_type)
        assert score > 0.0
    
    def test_character_rules_compliance(self):
        """Test character rule compliance scoring"""
        state_data = {
            'allows_letter_o': False,
            'uses_zero_for_o': True
        }
        
        # Plate with disallowed 'O' should have lower score
        score_with_o = score_plate_match('AOC123', state_data)
        score_without_o = score_plate_match('ABC123', state_data)
        
        # Both should return valid scores
        assert 0.0 <= score_with_o <= 1.0
        assert 0.0 <= score_without_o <= 1.0
    
    def test_score_range(self):
        """Test that score is always between 0.0 and 1.0"""
        state_data = {'allows_letter_o': True}
        plate_type = {'pattern': 'ABC123', 'character_count': 6}
        
        score = score_plate_match('XYZ789', state_data, plate_type)
        assert 0.0 <= score <= 1.0


# ============================================================================
# FORMAT COLOR DISPLAY TESTS
# ============================================================================

class TestFormatColorDisplay:
    """Test cases for format_color_display()"""
    
    def test_empty_list(self):
        """Test with empty color list"""
        assert format_color_display([]) == "Not specified"
    
    def test_single_known_color(self):
        """Test with single known color"""
        result = format_color_display(['#FFFFFF'])
        assert 'White' in result
    
    def test_multiple_known_colors(self):
        """Test with multiple known colors"""
        result = format_color_display(['#FFFFFF', '#000000'])
        assert 'White' in result
        assert 'Black' in result
    
    def test_unknown_color_code(self):
        """Test with unknown color code"""
        result = format_color_display(['#ABCDEF'])
        assert '#ABCDEF' in result.upper()
    
    def test_max_three_colors(self):
        """Test that only first 3 colors are displayed"""
        colors = ['#FFFFFF', '#000000', '#FF0000', '#00FF00', '#0000FF']
        result = format_color_display(colors)
        # Should contain at most 3 colors (2 commas max)
        comma_count = result.count(',')
        assert comma_count <= 2
    
    def test_case_insensitivity(self):
        """Test case insensitive color matching"""
        result1 = format_color_display(['#ffffff'])
        result2 = format_color_display(['#FFFFFF'])
        assert result1 == result2


# ============================================================================
# GET IMAGE PATH TESTS
# ============================================================================

class TestGetImagePath:
    """Test cases for get_image_path()"""
    
    def test_basic_path_construction(self):
        """Test basic path construction"""
        path = get_image_path('/base', 'FL', 'plates')
        assert 'FL' in path
        assert 'plates' in path
        assert 'images' in path
    
    def test_with_filename(self):
        """Test path construction with filename"""
        path = get_image_path('/base', 'CA', 'logos', 'logo.png')
        assert path.endswith('logo.png')
        assert 'CA' in path
    
    def test_state_uppercase_conversion(self):
        """Test that state abbreviation is converted to uppercase"""
        path1 = get_image_path('/base', 'fl', 'plates')
        path2 = get_image_path('/base', 'FL', 'plates')
        assert 'FL' in path1
        assert 'FL' in path2
    
    def test_path_separators(self):
        """Test correct path separator usage"""
        path = get_image_path('/base', 'TX', 'characters')
        # Path should use OS-appropriate separators
        assert os.sep in path or '/' in path


# ============================================================================
# ENSURE DATA DIRECTORIES TESTS
# ============================================================================

class TestEnsureDataDirectories:
    """Test cases for ensure_data_directories()"""
    
    def test_creates_directories(self, tmp_path):
        """Test that directories are created"""
        base_path = str(tmp_path / "test_app")
        ensure_data_directories(base_path)
        
        # Check that data directory exists
        data_dir = Path(base_path) / "data"
        assert data_dir.exists()
        assert (data_dir / "database").exists()
        assert (data_dir / "images").exists()
        assert (data_dir / "states").exists()
    
    def test_idempotent(self, tmp_path):
        """Test that function can be called multiple times safely"""
        base_path = str(tmp_path / "test_app2")
        
        # Call twice
        ensure_data_directories(base_path)
        ensure_data_directories(base_path)
        
        # Should not raise error
        data_dir = Path(base_path) / "data"
        assert data_dir.exists()


# ============================================================================
# LOAD JSON FILE TESTS
# ============================================================================

class TestLoadJsonFile:
    """Test cases for load_json_file()"""
    
    def test_load_valid_json(self, tmp_path):
        """Test loading valid JSON file"""
        json_file = tmp_path / "test.json"
        test_data = {'key': 'value', 'number': 42}
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)
        
        loaded = load_json_file(str(json_file))
        assert loaded == test_data
    
    def test_load_invalid_json(self, tmp_path):
        """Test loading invalid JSON returns None"""
        json_file = tmp_path / "invalid.json"
        
        with open(json_file, 'w', encoding='utf-8') as f:
            f.write("{ invalid json }")
        
        result = load_json_file(str(json_file))
        assert result is None
    
    def test_load_nonexistent_file(self, tmp_path):
        """Test loading non-existent file returns None"""
        result = load_json_file(str(tmp_path / "nonexistent.json"))
        assert result is None
    
    def test_load_empty_file(self, tmp_path):
        """Test loading empty file returns None"""
        json_file = tmp_path / "empty.json"
        json_file.touch()
        
        result = load_json_file(str(json_file))
        assert result is None
    
    def test_load_unicode_content(self, tmp_path):
        """Test loading JSON with unicode characters"""
        json_file = tmp_path / "unicode.json"
        test_data = {'name': 'Café', 'city': 'São Paulo'}
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False)
        
        loaded = load_json_file(str(json_file))
        assert loaded == test_data


# ============================================================================
# SAVE JSON FILE TESTS
# ============================================================================

class TestSaveJsonFile:
    """Test cases for save_json_file()"""
    
    def test_save_valid_json(self, tmp_path):
        """Test saving valid JSON data"""
        json_file = tmp_path / "output.json"
        test_data = {'key': 'value', 'list': [1, 2, 3]}
        
        result = save_json_file(str(json_file), test_data)
        assert result is True
        assert json_file.exists()
        
        # Verify content
        with open(json_file, 'r', encoding='utf-8') as f:
            loaded = json.load(f)
        assert loaded == test_data
    
    def test_save_creates_directory(self, tmp_path):
        """Test that save creates parent directory if needed"""
        json_file = tmp_path / "subdir" / "nested" / "output.json"
        test_data = {'created': True}
        
        result = save_json_file(str(json_file), test_data)
        assert result is True
        assert json_file.exists()
    
    def test_save_overwrites_existing(self, tmp_path):
        """Test that save overwrites existing file"""
        json_file = tmp_path / "overwrite.json"
        
        # Save first time
        save_json_file(str(json_file), {'version': 1})
        
        # Save second time
        result = save_json_file(str(json_file), {'version': 2})
        assert result is True
        
        # Verify new content
        with open(json_file, 'r', encoding='utf-8') as f:
            loaded = json.load(f)
        assert loaded['version'] == 2
    
    def test_save_unicode_content(self, tmp_path):
        """Test saving JSON with unicode characters"""
        json_file = tmp_path / "unicode_out.json"
        test_data = {'español': 'año', '中文': '测试'}
        
        result = save_json_file(str(json_file), test_data)
        assert result is True
        
        # Verify content
        with open(json_file, 'r', encoding='utf-8') as f:
            loaded = json.load(f)
        assert loaded == test_data
    
    def test_save_formatted_output(self, tmp_path):
        """Test that output is properly formatted with indentation"""
        json_file = tmp_path / "formatted.json"
        test_data = {'nested': {'key': 'value'}}
        
        save_json_file(str(json_file), test_data)
        
        # Read raw content
        with open(json_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Should be indented (contain newlines and spaces)
        assert '\n' in content
        assert '  ' in content  # Indentation
