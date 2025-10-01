"""
Test Suite for JSON Search Engine
Tests all search capabilities including handling rules search
"""

import unittest
import json
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from gui.utils.json_search_engine import JSONSearchEngine


class TestSearchEngine(unittest.TestCase):
    """Test cases for the JSON search engine"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.search_engine = JSONSearchEngine()
        self.test_state = 'AL'  # Alabama has comprehensive data
        
    def test_basic_search_all_categories(self):
        """Test basic search across all categories"""
        results = self.search_engine.search(query="Alabama", category="all")
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0, "Should find 'Alabama' in state data")
        
    def test_search_with_state_filter(self):
        """Test search limited to specific state"""
        results = self.search_engine.search(
            query="passenger",
            category="all",
            state_filter="AL"
        )
        self.assertIsInstance(results, list)
        # All results should be from Alabama
        for result in results:
            self.assertEqual(result['state'], 'AL')
            
    def test_search_design_elements(self):
        """Test searching design elements category"""
        results = self.search_engine.search(
            query="standard",
            category="design"
        )
        self.assertIsInstance(results, list)
        
    def test_search_fonts(self):
        """Test searching fonts category"""
        results = self.search_engine.search(
            query="Arial",
            category="fonts"
        )
        self.assertIsInstance(results, list)
        
    def test_search_colors(self):
        """Test searching colors category"""
        results = self.search_engine.search(
            query="white",
            category="colors"
        )
        self.assertIsInstance(results, list)


class TestHandlingRulesSearch(unittest.TestCase):
    """Test cases for searching character handling rules"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.search_engine = JSONSearchEngine()
        
    def test_search_o_vs_zero_rules(self):
        """Test searching for O vs 0 usage rules"""
        # This should find states with O/0 rules
        results = self.search_engine.search(
            query="zero",
            category="handling_rules"  # New category needed
        )
        # Note: Will fail until handling_rules category is implemented
        self.assertIsInstance(results, list)
        
    def test_search_stacked_characters(self):
        """Test searching for stacked character rules"""
        results = self.search_engine.search(
            query="stacked",
            category="handling_rules"
        )
        self.assertIsInstance(results, list)
        
    def test_search_character_restrictions(self):
        """Test searching character restrictions"""
        results = self.search_engine.search(
            query="does not allow",
            category="handling_rules"
        )
        self.assertIsInstance(results, list)
        
    def test_search_include_omit_rules(self):
        """Test searching include/omit stacked character rules"""
        # Search for states with specific include rules
        results = self.search_engine.search(
            query="X2",  # Stacked character to include
            category="handling_rules"
        )
        self.assertIsInstance(results, list)
        
    def test_search_processing_metadata(self):
        """Test searching processing metadata and rules"""
        results = self.search_engine.search(
            query="vertical characters",
            category="handling_rules"
        )
        self.assertIsInstance(results, list)


class TestSearchAllStates(unittest.TestCase):
    """Test searching across all states vs single state"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.search_engine = JSONSearchEngine()
        
    def test_search_all_states(self):
        """Test search across all available states"""
        results = self.search_engine.search(
            query="passenger",
            category="all",
            state_filter=None  # No filter = all states
        )
        self.assertIsInstance(results, list)
        
        # Should have results from multiple states
        states_found = set(r['state'] for r in results)
        self.assertGreater(len(states_found), 1, "Should find results in multiple states")
        
    def test_search_single_state_only(self):
        """Test search limited to one state"""
        results = self.search_engine.search(
            query="passenger",
            category="all",
            state_filter="AL"
        )
        self.assertIsInstance(results, list)
        
        # All results should be from Alabama only
        for result in results:
            self.assertEqual(result['state'], 'AL')
            
    def test_compare_all_vs_filtered(self):
        """Test that filtering produces subset of all results"""
        all_results = self.search_engine.search(
            query="standard",
            category="all",
            state_filter=None
        )
        
        filtered_results = self.search_engine.search(
            query="standard",
            category="all",
            state_filter="AL"
        )
        
        # Filtered should be <= all results
        self.assertLessEqual(len(filtered_results), len(all_results))


class TestSearchCategories(unittest.TestCase):
    """Test all search categories"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.search_engine = JSONSearchEngine()
        
    def test_category_fonts(self):
        """Test fonts category search"""
        results = self.search_engine.search(query="font", category="fonts")
        self.assertIsInstance(results, list)
        
    def test_category_slogans(self):
        """Test slogans category search"""
        results = self.search_engine.search(query="Heart", category="slogans", state_filter="AL")
        self.assertIsInstance(results, list)
        
    def test_category_colors(self):
        """Test colors category search"""
        results = self.search_engine.search(query="red", category="colors")
        self.assertIsInstance(results, list)
        
    def test_category_logos(self):
        """Test logos category search"""
        results = self.search_engine.search(query="logo", category="logos")
        self.assertIsInstance(results, list)
        
    def test_category_text(self):
        """Test plate text category search"""
        results = self.search_engine.search(query="Alabama", category="text")
        self.assertIsInstance(results, list)
        
    def test_category_design(self):
        """Test design elements category search"""
        results = self.search_engine.search(query="standard", category="design")
        self.assertIsInstance(results, list)
        
    def test_category_type(self):
        """Test plate type category search"""
        results = self.search_engine.search(query="passenger", category="type")
        self.assertIsInstance(results, list)
        
    def test_category_handling_rules_implemented(self):
        """Test that handling_rules category is now implemented"""
        # This should return a list of fields now that it's implemented
        fields = self.search_engine._get_search_fields("handling_rules")
        self.assertIsInstance(fields, list, "handling_rules should return a list of fields")
        self.assertGreater(len(fields), 0, "handling_rules should have at least one field")
        # Check for specific expected fields
        expected_fields = ['uses_zero_for_o', 'allows_letter_o', 'stacked_characters']
        for field in expected_fields:
            self.assertIn(field, fields, f"handling_rules should include {field}")


class TestSearchResultStructure(unittest.TestCase):
    """Test the structure of search results"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.search_engine = JSONSearchEngine()
        
    def test_result_has_required_fields(self):
        """Test that results have all required fields"""
        results = self.search_engine.search(query="Alabama", category="all", state_filter="AL")
        
        if len(results) > 0:
            result = results[0]
            self.assertIn('state', result)
            self.assertIn('field', result)
            self.assertIn('value', result)
            self.assertIn('match_type', result)
            
    def test_result_state_code_format(self):
        """Test that state codes are properly formatted"""
        results = self.search_engine.search(query="passenger", category="all")
        
        for result in results:
            state = result.get('state')
            self.assertIsNotNone(state)
            if state:
                self.assertEqual(len(state), 2, "State code should be 2 characters")
                self.assertTrue(state.isupper(), "State code should be uppercase")


class TestSearchCaching(unittest.TestCase):
    """Test search caching functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.search_engine = JSONSearchEngine()
        
    def test_cache_stores_results(self):
        """Test that results are cached"""
        query = "test_cache_query"
        
        # First search
        results1 = self.search_engine.search(query=query, category="all")
        
        # Check cache
        cache_key = f"{query}_all_None"
        self.assertIn(cache_key, self.search_engine.search_cache)
        
        # Second search should use cache
        results2 = self.search_engine.search(query=query, category="all")
        
        # Results should be identical (from cache)
        self.assertEqual(results1, results2)
        
    def test_cache_clear(self):
        """Test cache clearing"""
        self.search_engine.search(query="test", category="all")
        self.assertGreater(len(self.search_engine.search_cache), 0)
        
        self.search_engine.clear_cache()
        self.assertEqual(len(self.search_engine.search_cache), 0)


class TestSearchSuggestions(unittest.TestCase):
    """Test search suggestion functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.search_engine = JSONSearchEngine()
        
    def test_get_color_suggestions(self):
        """Test getting color suggestions"""
        suggestions = self.search_engine.get_suggestions("blu", category="colors")
        self.assertIsInstance(suggestions, list)
        self.assertIn("blue", suggestions)
        
    def test_get_font_suggestions(self):
        """Test getting font suggestions"""
        suggestions = self.search_engine.get_suggestions("ari", category="fonts")
        self.assertIsInstance(suggestions, list)
        
    def test_suggestions_limit(self):
        """Test that suggestions are limited to 5"""
        suggestions = self.search_engine.get_suggestions("a", category="all")
        self.assertLessEqual(len(suggestions), 5)


if __name__ == '__main__':
    unittest.main()
