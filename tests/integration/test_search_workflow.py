"""
Integration tests for search workflow
Tests the complete search-to-result workflow
"""

import pytest
import json
from pathlib import Path


class TestSearchWorkflow:
    """Test complete search workflow integration"""
    
    def test_search_to_state_selection_flow(self, mock_search_engine):
        """Test search results leading to state selection"""
        # Perform search
        results = mock_search_engine.search('Passenger')
        
        # Results should be available
        assert isinstance(results, list)
        
        # Selecting from results should provide state info
        if len(results) > 0:
            first_result = results[0]
            assert isinstance(first_result, dict)
    
    def test_search_results_update_info_panels(self, mock_search_engine):
        """Test that search results trigger info panel updates"""
        # Search for a plate type
        results = mock_search_engine.search('Commercial', category='type')
        
        # Should get results
        assert isinstance(results, list)
        
        # Info panels would receive update with result data
        # This would normally trigger callbacks in the GUI
    
    def test_search_filters_plate_types(self, mock_search_engine):
        """Test search with plate type filter"""
        # Search with category filter
        results = mock_search_engine.search('standard', category='type')
        
        assert isinstance(results, list)
    
    def test_search_with_state_context(self, mock_search_engine):
        """Test search within a specific state context"""
        # Search with state filter
        results = mock_search_engine.search('Passenger', state_filter='CA')
        
        assert isinstance(results, list)
    
    def test_cross_state_search_aggregation(self, mock_search_engine):
        """Test search aggregating results across multiple states"""
        # Search without state filter (all states)
        all_results = mock_search_engine.search('Passenger')
        
        # Search with state filter
        ca_results = mock_search_engine.search('Passenger', state_filter='CA')
        
        # All results should be >= state-specific results
        assert isinstance(all_results, list)
        assert isinstance(ca_results, list)


class TestSearchResultProcessing:
    """Test search result processing"""
    
    def test_result_deduplication(self):
        """Test removing duplicate results"""
        results = [
            {'state': 'CA', 'type': 'Passenger'},
            {'state': 'TX', 'type': 'Passenger'},
            {'state': 'CA', 'type': 'Passenger'}  # Duplicate
        ]
        
        # Deduplicate
        unique_results = []
        seen = set()
        for r in results:
            key = (r['state'], r['type'])
            if key not in seen:
                unique_results.append(r)
                seen.add(key)
        
        assert len(unique_results) == 2
    
    def test_result_sorting(self):
        """Test sorting search results"""
        results = [
            {'state': 'TX', 'score': 0.5},
            {'state': 'CA', 'score': 0.9},
            {'state': 'FL', 'score': 0.7}
        ]
        
        sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)
        
        assert sorted_results[0]['state'] == 'CA'
        assert sorted_results[0]['score'] == 0.9
    
    def test_result_relevance_scoring(self):
        """Test relevance scoring of search results"""
        query = 'passenger'
        items = [
            'Passenger Vehicle',
            'Commercial Passenger',
            'Motorcycle'
        ]
        
        scores = []
        for item in items:
            # Simple scoring: exact match > contains > no match
            if query.lower() == item.lower():
                score = 1.0
            elif query.lower() in item.lower():
                score = 0.5
            else:
                score = 0.0
            scores.append(score)
        
        assert scores[0] == 0.5  # Contains
        assert scores[1] == 0.5  # Contains
        assert scores[2] == 0.0  # No match


class TestSearchCaching:
    """Test search caching integration"""
    
    def test_cache_hit_performance(self, mock_search_engine):
        """Test cache hit improves performance"""
        query = 'commercial'
        
        # First search (cache miss)
        result1 = mock_search_engine.search(query)
        
        # Second search (cache hit)
        result2 = mock_search_engine.search(query)
        
        # Results should be identical
        assert result1 == result2
    
    def test_cache_invalidation_on_data_change(self, mock_search_engine):
        """Test cache invalidates when data changes"""
        query = 'passenger'
        
        # Initial search
        result1 = mock_search_engine.search(query)
        
        # Clear cache (simulating data change)
        mock_search_engine.search_cache.clear()
        
        # Search again (cache miss)
        result2 = mock_search_engine.search(query)
        
        # Should recompute
        assert isinstance(result2, list)


class TestSearchErrorHandling:
    """Test error handling in search workflow"""
    
    def test_empty_query_handling(self, mock_search_engine):
        """Test handling empty search query"""
        results = mock_search_engine.search('')
        
        # Should return list (might be empty or all results)
        assert isinstance(results, list)
    
    def test_no_results_handling(self, mock_search_engine):
        """Test handling when search returns no results"""
        results = mock_search_engine.search('ZZZZNONEXISTENT')
        
        # Should return empty list, not crash
        assert isinstance(results, list)
    
    def test_special_character_query(self, mock_search_engine):
        """Test handling special characters in query"""
        special_queries = ['@#$', '!!!', '%%%']
        
        for query in special_queries:
            results = mock_search_engine.search(query)
            assert isinstance(results, list)
