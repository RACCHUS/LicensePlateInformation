"""
Unit tests for json_search_engine.py
Tests for JSONSearchEngine class
"""

import pytest
import json
from pathlib import Path
from src.gui.utils.json_search_engine import JSONSearchEngine


# ============================================================================
# INITIALIZATION TESTS
# ============================================================================

class TestJSONSearchEngineInit:
    """Test cases for JSONSearchEngine initialization"""
    
    def test_init_with_default_directory(self):
        """Test initialization with default data directory"""
        engine = JSONSearchEngine()
        assert engine is not None
        assert engine.data_directory is not None
    
    def test_init_with_custom_directory(self, sample_data_dir):
        """Test initialization with custom data directory"""
        engine = JSONSearchEngine(str(sample_data_dir))
        assert engine.data_directory == str(sample_data_dir)
    
    def test_state_filename_map_exists(self):
        """Test that state filename mapping is defined"""
        engine = JSONSearchEngine()
        assert isinstance(engine.state_filename_map, dict)
        assert 'CA' in engine.state_filename_map
        assert 'FL' in engine.state_filename_map
        assert 'TX' in engine.state_filename_map


# ============================================================================
# STATE DATA LOADING TESTS
# ============================================================================

class TestLoadStateData:
    """Test cases for load_state_data()"""
    
    def test_load_state_data_existing(self, mock_search_engine):
        """Test loading existing state data"""
        data = mock_search_engine.load_state_data('CA')
        assert data is not None
        assert isinstance(data, dict)
    
    def test_load_state_data_caching(self, mock_search_engine):
        """Test that loaded data is cached"""
        # Load twice
        data1 = mock_search_engine.load_state_data('CA')
        data2 = mock_search_engine.load_state_data('CA')
        
        # Should return same object (cached)
        assert data1 is data2
    
    def test_load_state_data_nonexistent(self):
        """Test loading non-existent state data"""
        engine = JSONSearchEngine()
        data = engine.load_state_data('INVALID')
        
        # Should return sample data or handle gracefully
        assert data is not None or data == {}


# ============================================================================
# SEARCH TESTS
# ============================================================================

class TestSearch:
    """Test cases for search()"""
    
    def test_search_basic(self, mock_search_engine):
        """Test basic search functionality"""
        results = mock_search_engine.search('Passenger')
        assert isinstance(results, list)
    
    def test_search_with_category(self, mock_search_engine):
        """Test search with category filter"""
        results = mock_search_engine.search('Passenger', category='all')
        assert isinstance(results, list)
    
    def test_search_with_state_filter(self, mock_search_engine):
        """Test search with state filter"""
        results = mock_search_engine.search('plate', state_filter='CA')
        assert isinstance(results, list)
    
    def test_search_case_insensitive(self, mock_search_engine):
        """Test that search is case insensitive"""
        results1 = mock_search_engine.search('passenger')
        results2 = mock_search_engine.search('PASSENGER')
        
        # Should return same number of results
        assert len(results1) == len(results2)
    
    def test_search_empty_query(self, mock_search_engine):
        """Test search with empty query"""
        results = mock_search_engine.search('')
        assert isinstance(results, list)


# ============================================================================
# STATE CODE TESTS
# ============================================================================

class TestGetAllStateCodes:
    """Test cases for get_all_state_codes()"""
    
    def test_get_all_state_codes(self):
        """Test getting all state codes"""
        engine = JSONSearchEngine()
        codes = engine.get_all_state_codes()
        
        assert isinstance(codes, list)
        assert len(codes) > 0
        assert 'CA' in codes
        assert 'FL' in codes
        assert 'TX' in codes
    
    def test_state_codes_all_uppercase(self):
        """Test that all state codes are uppercase"""
        engine = JSONSearchEngine()
        codes = engine.get_all_state_codes()
        
        assert all(code.isupper() for code in codes)


# ============================================================================
# SUGGESTIONS TESTS
# ============================================================================

class TestGetSuggestions:
    """Test cases for get_suggestions()"""
    
    def test_get_suggestions_basic(self, mock_search_engine):
        """Test getting suggestions"""
        suggestions = mock_search_engine.get_suggestions('Pass')
        assert isinstance(suggestions, list)
    
    def test_get_suggestions_empty(self, mock_search_engine):
        """Test suggestions with empty query"""
        suggestions = mock_search_engine.get_suggestions('')
        assert isinstance(suggestions, list)


# ============================================================================
# CATEGORY STATS TESTS
# ============================================================================

class TestGetCategoryStats:
    """Test cases for get_category_stats()"""
    
    def test_get_category_stats(self, mock_search_engine):
        """Test getting category statistics"""
        stats = mock_search_engine.get_category_stats()
        assert isinstance(stats, dict)
    
    def test_get_category_stats_with_filter(self, mock_search_engine):
        """Test getting category stats with state filter"""
        stats = mock_search_engine.get_category_stats(state_filter='CA')
        assert isinstance(stats, dict)


# ============================================================================
# CACHE TESTS
# ============================================================================

class TestCacheOperations:
    """Test cases for cache operations"""
    
    def test_clear_cache(self, mock_search_engine):
        """Test clearing the cache"""
        # Load some data
        mock_search_engine.load_state_data('CA')
        
        # Clear cache
        mock_search_engine.clear_cache()
        
        # Cache should be empty
        assert len(mock_search_engine.loaded_data) == 0
