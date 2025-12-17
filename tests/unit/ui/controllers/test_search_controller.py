"""
Unit tests for SearchController.

Tests search functionality, debouncing, and result categorization.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Skip all tests if PySide6 is not available
pytest.importorskip("PySide6")

from PySide6.QtCore import QCoreApplication
from src.ui.controllers.search_controller import (
    SearchController, SearchResult, CategorizedResults, MIN_SEARCH_CHARS
)


@pytest.fixture
def search_controller(qapp):
    """Create a SearchController instance."""
    controller = SearchController()
    return controller


class TestSearchResult:
    """Test SearchResult dataclass."""
    
    def test_create_search_result(self):
        """Test creating a SearchResult."""
        result = SearchResult(
            state_code="FL",
            state_name="Florida",
            field="slogan",
            value="Sunshine State",
            match_type="state_info"
        )
        assert result.state_code == "FL"
        assert result.state_name == "Florida"
        assert result.match_type == "state_info"
    
    def test_search_result_to_dict(self):
        """Test SearchResult.to_dict() method."""
        result = SearchResult(
            state_code="CA",
            state_name="California",
            field="plate_type",
            value="Amateur Radio",
            match_type="plate_type",
            plate_type="Amateur Radio"
        )
        d = result.to_dict()
        
        assert d['state'] == "CA"
        assert d['state_name'] == "California"
        assert d['plate_type'] == "Amateur Radio"


class TestCategorizedResults:
    """Test CategorizedResults dataclass."""
    
    def test_empty_results(self):
        """Test empty CategorizedResults."""
        results = CategorizedResults(
            query="test",
            category="all",
            state_filter=None
        )
        assert results.is_empty is True
        assert results.total_count == 0
        assert results.state_count == 0
    
    def test_results_with_data(self):
        """Test CategorizedResults with data."""
        r1 = SearchResult("FL", "Florida", "slogan", "Sunshine", "state_info")
        r2 = SearchResult("CA", "California", "slogan", "Golden", "state_info")
        
        results = CategorizedResults(
            query="test",
            category="all",
            state_filter=None,
            all_results=[r1, r2],
            state_results=[r1, r2]
        )
        
        assert results.is_empty is False
        assert results.total_count == 2
        assert results.state_count == 2
    
    def test_state_count_unique(self):
        """Test state_count counts unique states."""
        r1 = SearchResult("FL", "Florida", "slogan", "Sunshine", "state_info")
        r2 = SearchResult("FL", "Florida", "color", "Orange", "state_info")
        r3 = SearchResult("CA", "California", "slogan", "Golden", "state_info")
        
        results = CategorizedResults(
            query="test",
            category="all",
            state_filter=None,
            all_results=[r1, r2, r3]
        )
        
        # FL appears twice but should count as 1
        assert results.state_count == 2


class TestSearchControllerInit:
    """Test SearchController initialization."""
    
    def test_controller_creates(self, search_controller):
        """Test controller creates successfully."""
        assert search_controller is not None
    
    def test_categories_defined(self, search_controller):
        """Test search categories are defined."""
        assert 'all' in SearchController.CATEGORIES
        assert 'slogans' in SearchController.CATEGORIES
        assert 'type' in SearchController.CATEGORIES
    
    def test_min_search_chars(self):
        """Test minimum search characters constant."""
        assert MIN_SEARCH_CHARS == 2


class TestSearchExecution:
    """Test search execution."""
    
    def test_search_too_short_clears(self, search_controller):
        """Test search with too few chars clears results."""
        callback = Mock()
        search_controller.search_cleared.connect(callback)
        
        # Search with 1 character (below minimum)
        search_controller.search("a")
        
        # Should emit cleared signal
        callback.assert_called()
    
    def test_search_with_valid_query(self, search_controller):
        """Test search with valid query length."""
        # Just verify it doesn't crash - actual results depend on data
        search_controller.search("florida")
    
    def test_search_with_category_filter(self, search_controller):
        """Test search with category filter."""
        search_controller.search("sunshine", category="slogans")
    
    def test_search_with_state_filter(self, search_controller):
        """Test search with state filter."""
        search_controller.search("plate", state_filter="FL")


class TestSearchSignals:
    """Test SearchController signals."""
    
    def test_search_started_signal(self, search_controller):
        """Test search_started signal is emitted on immediate search."""
        callback = Mock()
        search_controller.search_started.connect(callback)
        
        # Use immediate=True to bypass debounce
        search_controller.search("test query", immediate=True)
        
        callback.assert_called()
    
    def test_search_cleared_on_empty(self, search_controller):
        """Test search_cleared signal on empty query."""
        callback = Mock()
        search_controller.search_cleared.connect(callback)
        
        search_controller.clear_search()
        
        callback.assert_called()


class TestCategoryMappings:
    """Test category and field mappings."""
    
    def test_char_rules_fields_defined(self):
        """Test character rules fields are defined."""
        assert 'uses_zero_for_o' in SearchController.CHAR_RULES_FIELDS
        assert 'allows_letter_o' in SearchController.CHAR_RULES_FIELDS
    
    def test_categories_defined(self):
        """Test search categories are defined."""
        assert 'all' in SearchController.CATEGORIES
        assert 'slogans' in SearchController.CATEGORIES
        assert 'type' in SearchController.CATEGORIES
