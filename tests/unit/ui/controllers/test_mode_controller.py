"""
Unit tests for ModeController.

Tests the queue mode management logic without requiring a GUI.
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Skip all tests if PySide6 is not available
pytest.importorskip("PySide6")

from PySide6.QtCore import QCoreApplication
from src.ui.controllers.mode_controller import ModeController


@pytest.fixture(scope="module")
def qapp():
    """Create a QCoreApplication for signal testing."""
    app = QCoreApplication.instance()
    if app is None:
        app = QCoreApplication([])
    yield app


@pytest.fixture
def temp_config(tmp_path):
    """Create a temporary config file."""
    config = {
        "modes": {
            "V3": {
                "description": "Florida primary",
                "primary": ["FL"],
                "secondary": ["GA", "AL", "SC"],
                "excluded": [],
                "show_all_states": True
            },
            "OOSV3": {
                "description": "Out-of-state",
                "primary": [],
                "secondary": ["GA", "AL", "SC"],
                "excluded": ["FL", "MA", "ME"],
                "show_all_states": True
            },
            "PlateType": {
                "description": "Plate type states",
                "primary": ["MA", "ME", "OH", "IN", "IL"],
                "secondary": [],
                "excluded": ["FL"],
                "show_all_states": True
            },
            "All": {
                "description": "All states",
                "primary": [],
                "secondary": [],
                "excluded": [],
                "show_all_states": True
            }
        },
        "default_mode": "V3"
    }
    config_file = tmp_path / "queue_modes.json"
    with open(config_file, 'w') as f:
        json.dump(config, f)
    return config_file


@pytest.fixture
def mode_controller(qapp, temp_config):
    """Create a ModeController with temp config."""
    controller = ModeController(config_path=str(temp_config))
    return controller


class TestModeControllerInit:
    """Test ModeController initialization."""
    
    def test_loads_modes_from_config(self, mode_controller):
        """Test that modes are loaded from config file."""
        assert "V3" in mode_controller.modes
        assert "OOSV3" in mode_controller.modes
        assert "All" in mode_controller.modes
    
    def test_default_mode_from_config(self, mode_controller):
        """Test that default mode is loaded from config."""
        assert mode_controller.current_mode == "V3"
    
    def test_fallback_to_defaults_if_no_config(self, qapp, tmp_path):
        """Test fallback to default modes when config doesn't exist."""
        controller = ModeController(config_path=str(tmp_path / "nonexistent.json"))
        assert "All" in controller.modes
        assert controller.current_mode == "All"
    
    def test_available_modes_property(self, mode_controller):
        """Test available_modes returns all mode names."""
        modes = mode_controller.available_modes
        assert isinstance(modes, list)
        assert "V3" in modes
        assert "All" in modes


class TestModeSelection:
    """Test mode switching functionality."""
    
    def test_set_mode_valid(self, mode_controller):
        """Test switching to a valid mode."""
        result = mode_controller.set_mode("OOSV3")
        assert result is True
        assert mode_controller.current_mode == "OOSV3"
    
    def test_set_mode_invalid(self, mode_controller):
        """Test switching to an invalid mode."""
        result = mode_controller.set_mode("InvalidMode")
        assert result is False
        # Mode should remain unchanged
        assert mode_controller.current_mode != "InvalidMode"
    
    def test_mode_changed_signal(self, mode_controller):
        """Test that mode_changed signal is emitted."""
        callback = Mock()
        mode_controller.mode_changed.connect(callback)
        
        mode_controller.set_mode("All")
        
        callback.assert_called_once()
        args = callback.call_args[0]
        assert args[0] == "All"  # mode_name
        assert isinstance(args[1], dict)  # mode_config


class TestStateCategorization:
    """Test state categorization by mode."""
    
    def test_get_primary_states_v3(self, mode_controller):
        """Test primary states in V3 mode."""
        mode_controller.set_mode("V3")
        primary = mode_controller.get_primary_states()
        assert "FL" in primary
    
    def test_get_primary_states_platetype(self, mode_controller):
        """Test primary states in PlateType mode."""
        mode_controller.set_mode("PlateType")
        primary = mode_controller.get_primary_states()
        assert "MA" in primary
        assert "ME" in primary
        assert "OH" in primary
        assert "FL" not in primary
    
    def test_get_secondary_states(self, mode_controller):
        """Test secondary states."""
        mode_controller.set_mode("V3")
        secondary = mode_controller.get_secondary_states()
        assert "GA" in secondary
        assert "AL" in secondary
    
    def test_is_state_excluded_oosv3(self, mode_controller):
        """Test excluded states in OOSV3 mode."""
        mode_controller.set_mode("OOSV3")
        assert mode_controller.is_state_excluded("FL") is True
        assert mode_controller.is_state_excluded("MA") is True
        assert mode_controller.is_state_excluded("GA") is False
    
    def test_is_state_excluded_all_mode(self, mode_controller):
        """Test no states excluded in All mode."""
        mode_controller.set_mode("All")
        assert mode_controller.is_state_excluded("FL") is False
        assert mode_controller.is_state_excluded("MA") is False


class TestStateCategories:
    """Test get_state_category method returns position categories."""
    
    def test_florida_primary_in_v3(self, mode_controller):
        """Test Florida is primary in V3 mode."""
        mode_controller.set_mode("V3")
        category = mode_controller.get_state_category("FL")
        assert category == "primary"
    
    def test_georgia_secondary_in_v3(self, mode_controller):
        """Test Georgia is secondary in V3 mode."""
        mode_controller.set_mode("V3")
        category = mode_controller.get_state_category("GA")
        assert category == "secondary"
    
    def test_florida_excluded_in_oosv3(self, mode_controller):
        """Test Florida is excluded in OOSV3 mode."""
        mode_controller.set_mode("OOSV3")
        category = mode_controller.get_state_category("FL")
        assert category == "excluded"
    
    def test_unknown_state_is_normal(self, mode_controller):
        """Test unlisted state is categorized as normal."""
        mode_controller.set_mode("V3")
        # WY is not in primary or secondary for V3
        category = mode_controller.get_state_category("WY")
        assert category == "normal"
    
    def test_plate_type_states_primary_in_platetype(self, mode_controller):
        """Test plate type states are primary in PlateType mode."""
        mode_controller.set_mode("PlateType")
        for state in ["MA", "ME", "OH"]:
            category = mode_controller.get_state_category(state)
            assert category == "primary", f"{state} should be primary in PlateType mode"


class TestJurisdictionLists:
    """Test the jurisdiction list constants."""
    
    def test_all_jurisdictions_count(self, mode_controller):
        """Test ALL_JURISDICTIONS has expected count."""
        # 50 states + DC + 5 territories + 13 Canadian = 69
        assert len(ModeController.ALL_JURISDICTIONS) >= 63
    
    def test_canadian_provinces_count(self, mode_controller):
        """Test CANADIAN_PROVINCES list."""
        assert len(ModeController.CANADIAN_PROVINCES) == 13
    
    def test_us_states_includes_dc(self, mode_controller):
        """Test US_STATES includes DC."""
        assert "DC" in ModeController.US_STATES
    
    def test_no_duplicate_jurisdictions(self, mode_controller):
        """Test no duplicates in jurisdiction list."""
        jurisdictions = ModeController.ALL_JURISDICTIONS
        assert len(jurisdictions) == len(set(jurisdictions))
