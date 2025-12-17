"""
Unit tests for StateButton widget.

Tests the styled state button with category-based coloring.
"""

import pytest
from unittest.mock import Mock

# Skip all tests if PySide6 is not available
pytest.importorskip("PySide6")

from PySide6.QtWidgets import QApplication

from src.ui.widgets.state_button import StateButton



@pytest.fixture
def state_button(qapp):
    """Create a StateButton instance."""
    btn = StateButton("FL")
    return btn


class TestStateButtonInit:
    """Test StateButton initialization."""
    
    def test_creates_successfully(self, state_button):
        """Test button creates successfully."""
        assert state_button is not None
    
    def test_displays_state_code(self, state_button):
        """Test button displays state code."""
        assert state_button.text() == "FL"
    
    def test_stores_state_code(self, state_button):
        """Test button stores state_code property."""
        assert state_button.state_code == "FL"
    
    def test_auto_determines_category(self, state_button):
        """Test button auto-determines category."""
        assert state_button.category == "florida"


class TestCategoryDetermination:
    """Test automatic category determination."""
    
    def test_florida_category(self, qapp):
        """Test Florida is categorized as 'florida'."""
        btn = StateButton("FL")
        assert btn.category == "florida"
    
    def test_plate_type_category(self, qapp):
        """Test plate_type states are categorized correctly."""
        for state in ["MA", "ME", "OH", "IN", "IL"]:
            btn = StateButton(state)
            assert btn.category == "plate_type", f"{state} should be plate_type"
    
    def test_nearby_category(self, qapp):
        """Test nearby states are categorized correctly."""
        for state in ["GA", "AL", "SC", "NC", "TN", "MS", "LA"]:
            btn = StateButton(state)
            assert btn.category == "nearby", f"{state} should be nearby"
    
    def test_distant_major_category(self, qapp):
        """Test distant major states are categorized correctly."""
        for state in ["CA", "TX", "NY"]:
            btn = StateButton(state)
            assert btn.category == "distant_major", f"{state} should be distant_major"
    
    def test_territory_category(self, qapp):
        """Test territories are categorized correctly."""
        for terr in ["PR", "GU", "VI", "DC"]:
            btn = StateButton(terr)
            assert btn.category == "territory", f"{terr} should be territory"
    
    def test_canadian_category(self, qapp):
        """Test Canadian provinces are categorized correctly."""
        for prov in ["ON", "QC", "BC", "AB"]:
            btn = StateButton(prov)
            assert btn.category == "canadian", f"{prov} should be canadian"
    
    def test_normal_category(self, qapp):
        """Test other states are categorized as 'normal'."""
        # Pick a state not in any special category
        btn = StateButton("WY")
        assert btn.category == "normal"


class TestGetCategoryClassMethod:
    """Test the get_category class method."""
    
    def test_get_category_florida(self):
        """Test get_category returns 'florida' for FL."""
        assert StateButton.get_category("FL") == "florida"
    
    def test_get_category_plate_type(self):
        """Test get_category returns 'plate_type' for MA."""
        assert StateButton.get_category("MA") == "plate_type"
    
    def test_get_category_nearby(self):
        """Test get_category returns 'nearby' for GA."""
        assert StateButton.get_category("GA") == "nearby"
    
    def test_get_category_normal(self):
        """Test get_category returns 'normal' for unlisted states."""
        assert StateButton.get_category("WY") == "normal"


class TestSelectedState:
    """Test selected state styling."""
    
    def test_set_selected(self, state_button):
        """Test setting selected state."""
        state_button.set_selected(True)
        assert state_button.is_selected is True
    
    def test_clear_selected(self, state_button):
        """Test clearing selected state."""
        state_button.set_selected(True)
        state_button.set_selected(False)
        assert state_button.is_selected is False
    
    def test_initial_not_selected(self, state_button):
        """Test button starts unselected."""
        btn = StateButton("CA")
        assert btn.is_selected is False


class TestButtonSignals:
    """Test StateButton signals."""
    
    def test_clicked_signal(self, qapp):
        """Test clicked signal emits state code."""
        btn = StateButton("CA")
        callback = Mock()
        btn.state_clicked.connect(callback)
        
        # Simulate click
        btn.click()
        
        callback.assert_called_once_with("CA")
    
    def test_multiple_clicks(self, qapp):
        """Test multiple clicks emit correctly."""
        btn = StateButton("TX")
        callback = Mock()
        btn.state_clicked.connect(callback)
        
        btn.click()
        btn.click()
        btn.click()
        
        assert callback.call_count == 3


class TestButtonSizing:
    """Test StateButton sizing."""
    
    def test_has_fixed_size(self, state_button):
        """Test button has a fixed size."""
        size = state_button.size()
        assert size.width() > 0
        assert size.height() > 0
    
    def test_size_matches_preset(self, state_button):
        """Test button size matches BUTTON_SIZE preset."""
        expected = StateButton.BUTTON_SIZE
        assert state_button.width() == expected['width']
        assert state_button.height() == expected['height']


class TestColorConstants:
    """Test color constant definitions."""
    
    def test_colors_dict_exists(self):
        """Test COLORS dict has expected categories."""
        colors = StateButton.COLORS
        
        assert "florida" in colors
        assert "plate_type" in colors
        assert "nearby" in colors
        assert "distant_major" in colors
        assert "territory" in colors
        assert "canadian" in colors
        assert "normal" in colors
        assert "selected" in colors
    
    def test_color_has_bg(self):
        """Test each color category has background color."""
        for cat in ["florida", "plate_type", "nearby", "normal"]:
            assert "bg" in StateButton.COLORS[cat]


class TestStateSets:
    """Test state category set definitions."""
    
    def test_florida_set(self):
        """Test FLORIDA set contains only FL."""
        assert StateButton.FLORIDA == {"FL"}
    
    def test_plate_type_states_set(self):
        """Test PLATE_TYPE_STATES set."""
        expected = {"MA", "ME", "OH", "IN", "IL"}
        assert StateButton.PLATE_TYPE_STATES == expected
    
    def test_nearby_states_set(self):
        """Test NEARBY_STATES set."""
        assert "GA" in StateButton.NEARBY_STATES
        assert "AL" in StateButton.NEARBY_STATES
    
    def test_canadian_set(self):
        """Test CANADIAN set has Canadian provinces."""
        assert "ON" in StateButton.CANADIAN
        assert "QC" in StateButton.CANADIAN
        assert len(StateButton.CANADIAN) == 13
