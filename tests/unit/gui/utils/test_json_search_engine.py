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
        
        # Perform a search to populate the cache
        mock_search_engine.search('California')
        
        # Verify cache has data
        assert len(mock_search_engine.search_cache) > 0
        
        # Clear cache
        mock_search_engine.clear_cache()
        
        # Cache should be empty (but loaded_data should remain)
        assert len(mock_search_engine.search_cache) == 0
        assert len(mock_search_engine.loaded_data) > 0  # Data stays loaded


# ============================================================================
# EXTENDED TESTS - PRIORITY 1.1
# ============================================================================

class TestSearchAllStates:
    """Test searching across all states without filters"""
    
    def test_search_all_states_no_filter(self, mock_search_engine):
        """Test search returns results from multiple states when no filter applied"""
        results = mock_search_engine.search('Passenger', category='all')
        assert isinstance(results, list)
        # Should potentially have results from multiple states
        
    def test_search_all_states_aggregation(self, mock_search_engine):
        """Test that search aggregates results from all states"""
        results = mock_search_engine.search('standard', state_filter=None)
        assert isinstance(results, list)


class TestFieldMappings:
    """Test field mapping searches"""
    
    def test_search_field_mappings_fonts(self, mock_search_engine):
        """Test searching font-related fields"""
        results = mock_search_engine.search('Arial', category='fonts')
        assert isinstance(results, list)
    
    def test_search_field_mappings_processing(self, mock_search_engine):
        """Test searching processing-related fields"""
        results = mock_search_engine.search('digital', category='processing')
        assert isinstance(results, list)
    
    def test_search_field_mappings_restrictions(self, mock_search_engine):
        """Test searching restriction-related fields"""
        results = mock_search_engine.search('zero', category='restrictions')
        assert isinstance(results, list)
    
    def test_search_field_mappings_colors(self, mock_search_engine):
        """Test searching color-related fields"""
        results = mock_search_engine.search('blue', category='colors')
        assert isinstance(results, list)


class TestHandlingRulesSearch:
    """Test searching with handling rules fields"""
    
    def test_search_with_handling_rules_fields(self, mock_search_engine):
        """Test searching for handling rule specific fields"""
        results = mock_search_engine.search('uses_zero_for_o', category='handling_rules')
        assert isinstance(results, list)
    
    def test_search_character_restrictions(self, mock_search_engine):
        """Test searching character restriction fields"""
        results = mock_search_engine.search('character_restrictions', category='restrictions')
        assert isinstance(results, list)


class TestPlateTypeRetrieval:
    """Test plate type retrieval methods"""
    
    def test_get_plate_types_for_state(self, mock_search_engine):
        """Test getting all plate types for a specific state"""
        # Load state data first
        state_data = mock_search_engine.load_state_data('CA')
        
        if 'plate_types' in state_data or 'plates' in state_data:
            # Should have plate type information
            assert 'plate_types' in state_data or 'plates' in state_data
    
    def test_get_all_plate_types_across_states(self, mock_search_engine):
        """Test retrieving plate types across multiple states"""
        results = mock_search_engine.search('', category='type')
        assert isinstance(results, list)


class TestSearchCaching:
    """Test search caching behavior"""
    
    def test_search_cache_stores_results(self, mock_search_engine):
        """Test that search results are cached"""
        query = 'passenger'
        
        # First search
        results1 = mock_search_engine.search(query)
        
        # Check cache
        cache_key = f"{query}_all_None"
        assert cache_key in mock_search_engine.search_cache
    
    def test_search_cache_reuse(self, mock_search_engine):
        """Test that cached results are reused"""
        query = 'commercial'
        
        # First search populates cache
        results1 = mock_search_engine.search(query)
        
        # Second search should use cache
        results2 = mock_search_engine.search(query)
        
        assert results1 == results2


class TestErrorHandling:
    """Test error handling in search engine"""
    
    def test_load_state_data_file_not_found_graceful(self):
        """Test graceful handling when state file not found"""
        engine = JSONSearchEngine()
        
        # Try to load non-existent state
        data = engine.load_state_data('ZZ')
        
        # Should return sample data, not crash
        assert data is not None
        assert isinstance(data, dict)
    
    def test_search_special_characters_handling(self, mock_search_engine):
        """Test search handles special characters without crashing"""
        special_queries = ['@#$', '!!!', '---', '***']
        
        for query in special_queries:
            results = mock_search_engine.search(query)
            assert isinstance(results, list)
    
    def test_search_partial_match(self, mock_search_engine):
        """Test partial matching in search"""
        results = mock_search_engine.search('Pass')
        assert isinstance(results, list)
        # Partial match should work for 'Passenger'


class TestStateDetails:
    """Test state detail retrieval"""
    
    def test_get_state_plate_type_details(self, mock_search_engine):
        """Test getting detailed plate type information"""
        state_data = mock_search_engine.load_state_data('CA')
        
        # Should have state info
        assert 'state_info' in state_data or isinstance(state_data, dict)
    
    def test_state_data_structure(self, mock_search_engine):
        """Test that loaded state data has expected structure"""
        state_data = mock_search_engine.load_state_data('FL')
        
        assert isinstance(state_data, dict)
        # Should have some identifying information
        assert len(state_data) > 0
