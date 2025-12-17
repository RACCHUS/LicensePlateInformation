"""
Unit tests for StateDataManager.

Tests state data loading and caching.
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

# Skip all tests if PySide6 is not available
pytest.importorskip("PySide6")

from PySide6.QtCore import QCoreApplication
from src.ui.controllers.state_data_manager import StateDataManager


@pytest.fixture(scope="module")
def qapp():
    """Create a QCoreApplication for signal testing."""
    app = QCoreApplication.instance()
    if app is None:
        app = QCoreApplication([])
    yield app


@pytest.fixture
def temp_state_dir(tmp_path):
    """Create a temporary state data directory with sample files."""
    states_dir = tmp_path / "states"
    states_dir.mkdir()
    
    # Create Florida data (matching actual JSON structure)
    florida_data = {
        "name": "Florida",
        "abbreviation": "FL",
        "slogan": "Sunshine State",
        "primary_colors": ["#FF6B00", "#FFFFFF"],
        "main_font": "Arial Bold",
        "uses_zero_for_o": True,
        "allows_letter_o": False,
        "zero_is_slashed": False,
        "plate_types": [
            {"type_code": "STD", "type_name": "Standard", "pattern": "ABC 1234"},
            {"type_code": "SPL", "type_name": "Specialty", "pattern": "ABC 123"}
        ]
    }
    with open(states_dir / "florida.json", 'w') as f:
        json.dump(florida_data, f)
    
    # Create California data
    california_data = {
        "name": "California",
        "abbreviation": "CA",
        "slogan": "Golden State",
        "primary_colors": ["#003F87", "#FFFFFF"],
        "main_font": "California DMV",
        "uses_zero_for_o": False,
        "allows_letter_o": True,
        "zero_is_slashed": False,
        "plate_types": [
            {"type_code": "STD", "type_name": "Standard", "pattern": "1ABC234"}
        ]
    }
    with open(states_dir / "california.json", 'w') as f:
        json.dump(california_data, f)
    
    return states_dir


@pytest.fixture
def state_data_manager(qapp, temp_state_dir):
    """Create a StateDataManager with temp data dir."""
    manager = StateDataManager(data_dir=str(temp_state_dir))
    return manager


class TestStateDataManagerInit:
    """Test StateDataManager initialization."""
    
    def test_creates_successfully(self, state_data_manager):
        """Test manager creates successfully."""
        assert state_data_manager is not None
    
    def test_state_filename_map_exists(self):
        """Test STATE_FILENAME_MAP contains expected states."""
        assert 'FL' in StateDataManager.STATE_FILENAME_MAP
        assert 'CA' in StateDataManager.STATE_FILENAME_MAP
        assert 'NY' in StateDataManager.STATE_FILENAME_MAP
    
    def test_state_filename_map_values(self):
        """Test STATE_FILENAME_MAP has correct filename mappings."""
        assert StateDataManager.STATE_FILENAME_MAP['FL'] == 'florida'
        assert StateDataManager.STATE_FILENAME_MAP['CA'] == 'california'
        assert StateDataManager.STATE_FILENAME_MAP['NY'] == 'new_york'


class TestStateDataLoading:
    """Test loading state data."""
    
    def test_load_florida_data(self, state_data_manager):
        """Test loading Florida state data."""
        data = state_data_manager.get_state_data("FL")
        
        assert data is not None
        assert data["name"] == "Florida"
    
    def test_load_california_data(self, state_data_manager):
        """Test loading California state data."""
        data = state_data_manager.get_state_data("CA")
        
        assert data is not None
        assert data["name"] == "California"
    
    def test_load_nonexistent_state(self, state_data_manager):
        """Test loading non-existent state returns None."""
        data = state_data_manager.get_state_data("XX")
        assert data is None
    
    def test_case_insensitive_loading(self, state_data_manager):
        """Test state code is case-insensitive."""
        data_upper = state_data_manager.get_state_data("FL")
        data_lower = state_data_manager.get_state_data("fl")
        
        assert data_upper is not None
        assert data_lower is not None
        assert data_upper == data_lower
    
    def test_empty_state_code(self, state_data_manager):
        """Test empty state code returns None."""
        assert state_data_manager.get_state_data("") is None
        assert state_data_manager.get_state_data(None) is None


class TestCaching:
    """Test state data caching."""
    
    def test_data_is_cached(self, state_data_manager):
        """Test that data is cached after first load."""
        # First load
        data1 = state_data_manager.get_state_data("FL")
        
        # Should be in cache now
        assert "FL" in state_data_manager._cache
        
        # Second load should return cached data
        data2 = state_data_manager.get_state_data("FL")
        
        assert data1 is data2  # Same object (from cache)


class TestStateInfoSummary:
    """Test get_state_info_summary method."""
    
    def test_summary_includes_name(self, state_data_manager):
        """Test summary includes state name."""
        summary = state_data_manager.get_state_info_summary("FL")
        
        assert summary is not None
        assert "name" in summary
        assert summary["name"] == "Florida"
    
    def test_summary_includes_slogan(self, state_data_manager):
        """Test summary includes slogan."""
        summary = state_data_manager.get_state_info_summary("FL")
        
        assert "slogan" in summary
        assert summary["slogan"] == "Sunshine State"
    
    def test_summary_nonexistent_state(self, state_data_manager):
        """Test summary for non-existent state returns empty dict."""
        summary = state_data_manager.get_state_info_summary("XX")
        assert summary == {} or summary is None


class TestPlateTypes:
    """Test plate type retrieval."""
    
    def test_get_plate_types(self, state_data_manager):
        """Test getting plate types for a state."""
        plate_types = state_data_manager.get_plate_types("FL")
        
        assert plate_types is not None
        assert len(plate_types) >= 1
    
    def test_plate_type_has_name(self, state_data_manager):
        """Test plate types have type_name field."""
        plate_types = state_data_manager.get_plate_types("FL")
        
        for pt in plate_types:
            assert "type_name" in pt


class TestCharacterRules:
    """Test character rules retrieval."""
    
    def test_get_character_rules(self, state_data_manager):
        """Test getting character rules for a state."""
        rules = state_data_manager.get_character_rules("FL")
        
        assert rules is not None
    
    def test_character_rules_has_zero_for_o(self, state_data_manager):
        """Test character rules include uses_zero_for_o."""
        rules = state_data_manager.get_character_rules("FL")
        
        assert "uses_zero_for_o" in rules
        assert rules["uses_zero_for_o"] is True


class TestSignals:
    """Test StateDataManager signals."""
    
    def test_state_loaded_signal(self, state_data_manager):
        """Test state_loaded signal is emitted."""
        callback = Mock()
        state_data_manager.state_loaded.connect(callback)
        
        # Clear cache to force reload
        state_data_manager._cache.clear()
        
        state_data_manager.get_state_data("FL")
        
        callback.assert_called_once()
        args = callback.call_args[0]
        assert args[0] == "FL"  # state_code
        assert isinstance(args[1], dict)  # data
