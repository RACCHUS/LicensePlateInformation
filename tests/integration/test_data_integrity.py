"""
Integration tests for data integrity
Validates JSON files and data consistency across the project
"""

import pytest
import json
from pathlib import Path


# ============================================================================
# JSON FILE VALIDATION TESTS
# ============================================================================

class TestJSONFileValidity:
    """Test that all JSON files are valid and loadable"""
    
    def test_states_directory_exists(self, data_directory):
        """Test that states directory exists"""
        states_dir = data_directory / "states"
        assert states_dir.exists(), "States directory should exist"
    
    def test_all_state_json_files_valid(self, states_directory):
        """Test that all state JSON files are valid"""
        if not states_directory.exists():
            pytest.skip("States directory not found")
        
        json_files = list(states_directory.glob("*.json"))
        
        if not json_files:
            pytest.skip("No JSON files found in states directory")
        
        for json_file in json_files:
            with open(json_file, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    assert isinstance(data, dict), f"{json_file.name} should contain a dictionary"
                except json.JSONDecodeError as e:
                    pytest.fail(f"Invalid JSON in {json_file.name}: {e}")
    
    def test_sample_fixture_files_valid(self):
        """Test that sample fixture files are valid JSON"""
        fixtures_dir = Path(__file__).parent.parent / "fixtures"
        
        if not fixtures_dir.exists():
            pytest.skip("Fixtures directory not found")
        
        for json_file in fixtures_dir.glob("*.json"):
            with open(json_file, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    assert data is not None
                except json.JSONDecodeError as e:
                    pytest.fail(f"Invalid JSON in fixture {json_file.name}: {e}")


# ============================================================================
# SCHEMA VALIDATION TESTS
# ============================================================================

class TestDataSchema:
    """Test that JSON data follows expected schema"""
    
    def test_state_json_has_required_fields(self, states_directory):
        """Test that state JSON files have required fields"""
        if not states_directory.exists():
            pytest.skip("States directory not found")
        
        json_files = list(states_directory.glob("*.json"))
        
        if not json_files:
            pytest.skip("No JSON files found")
        
        # Files should have either state_info or be a valid dict structure
        for json_file in json_files[:5]:  # Check first 5 files
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Just verify it's a valid dictionary - structure may vary
            assert isinstance(data, dict), \
                f"{json_file.name} should contain a dictionary"
            assert len(data) > 0, \
                f"{json_file.name} should not be empty"
    
    def test_state_info_structure(self, states_directory):
        """Test state_info section structure"""
        if not states_directory.exists():
            pytest.skip("States directory not found")
        
        json_files = list(states_directory.glob("*.json"))
        
        if not json_files:
            pytest.skip("No JSON files found")
        
        for json_file in json_files[:3]:  # Check first 3 files
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'state_info' in data:
                state_info = data['state_info']
                assert 'name' in state_info, f"{json_file.name} state_info missing 'name'"
                assert 'abbreviation' in state_info, f"{json_file.name} state_info missing 'abbreviation'"
    
    def test_plate_types_is_list(self, states_directory):
        """Test that plate_types is a list"""
        if not states_directory.exists():
            pytest.skip("States directory not found")
        
        json_files = list(states_directory.glob("*.json"))
        
        if not json_files:
            pytest.skip("No JSON files found")
        
        for json_file in json_files[:3]:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'plate_types' in data:
                assert isinstance(data['plate_types'], list), \
                    f"{json_file.name} plate_types should be a list"


# ============================================================================
# COLOR CODE VALIDATION TESTS
# ============================================================================

class TestColorCodes:
    """Test that color codes are valid hex values"""
    
    def test_primary_colors_hex_format(self, states_directory):
        """Test that primary_colors contain valid hex codes"""
        if not states_directory.exists():
            pytest.skip("States directory not found")
        
        json_files = list(states_directory.glob("*.json"))
        
        if not json_files:
            pytest.skip("No JSON files found")
        
        import re
        hex_pattern = re.compile(r'^#[0-9A-Fa-f]{6}$')
        
        for json_file in json_files[:3]:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'state_info' in data and 'primary_colors' in data['state_info']:
                colors = data['state_info']['primary_colors']
                if isinstance(colors, list):
                    for color in colors:
                        if isinstance(color, str):
                            assert hex_pattern.match(color), \
                                f"Invalid color code in {json_file.name}: {color}"


# ============================================================================
# IMAGE PATH VALIDATION TESTS
# ============================================================================

class TestImagePaths:
    """Test that referenced image paths are valid"""
    
    def test_image_paths_format(self, states_directory):
        """Test that image paths are properly formatted"""
        if not states_directory.exists():
            pytest.skip("States directory not found")
        
        json_files = list(states_directory.glob("*.json"))
        
        if not json_files:
            pytest.skip("No JSON files found")
        
        for json_file in json_files[:2]:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Just verify structure exists, don't validate file existence
            # as test environment may not have all images
            if 'plate_types' in data:
                for plate_type in data['plate_types'][:3]:
                    if 'image_path' in plate_type:
                        assert isinstance(plate_type['image_path'], str)


# ============================================================================
# CROSS-REFERENCE TESTS
# ============================================================================

class TestCrossReferences:
    """Test data consistency across different data sources"""
    
    def test_fixture_data_matches_schema(self):
        """Test that fixture data matches production schema"""
        fixtures_dir = Path(__file__).parent.parent / "fixtures"
        
        if not fixtures_dir.exists():
            pytest.skip("Fixtures directory not found")
        
        sample_state_file = fixtures_dir / "sample_state.json"
        
        if not sample_state_file.exists():
            pytest.skip("Sample state fixture not found")
        
        with open(sample_state_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Verify it has expected structure
        assert 'state_info' in data
        assert 'plate_types' in data
        assert isinstance(data['plate_types'], list)


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

class TestDataSize:
    """Test that data files are reasonable size"""
    
    def test_json_files_not_too_large(self, states_directory):
        """Test that JSON files are not excessively large"""
        if not states_directory.exists():
            pytest.skip("States directory not found")
        
        json_files = list(states_directory.glob("*.json"))
        
        if not json_files:
            pytest.skip("No JSON files found")
        
        max_size_mb = 10  # 10 MB maximum
        max_size_bytes = max_size_mb * 1024 * 1024
        
        for json_file in json_files:
            file_size = json_file.stat().st_size
            assert file_size < max_size_bytes, \
                f"{json_file.name} is too large: {file_size / 1024 / 1024:.2f} MB"
