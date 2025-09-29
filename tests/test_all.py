"""
Unit tests for License Plate Information System
"""

import unittest
import sys
import os

# Add src to path for imports - get parent directory then add src
test_dir = os.path.dirname(os.path.abspath(__file__))
app_root = os.path.dirname(test_dir)
src_path = os.path.join(app_root, 'src')
sys.path.insert(0, src_path)

from database.db_manager import DatabaseManager
from utils.helpers import (
    normalize_plate_text,
    generate_character_alternatives,
    validate_plate_pattern,
    score_plate_match
)

class TestDatabaseManager(unittest.TestCase):
    """Test database operations"""
    
    def setUp(self):
        """Set up test database"""
        self.db_manager = DatabaseManager(':memory:')  # Use in-memory database for tests
        self.db_manager.initialize_database()
    
    def test_database_initialization(self):
        """Test that database is properly initialized"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        
        # Check that tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        expected_tables = ['states', 'plate_types', 'character_references', 'lookup_history']
        for table in expected_tables:
            self.assertIn(table, tables)
    
    def test_state_search(self):
        """Test state search functionality"""
        # Should have sample states loaded
        results = self.db_manager.search_states('FL')
        self.assertGreater(len(results), 0)
        
        results = self.db_manager.search_states('Florida')
        self.assertGreater(len(results), 0)
        
        # Test case insensitive search
        results = self.db_manager.search_states('fl')
        self.assertGreater(len(results), 0)
    
    def test_plate_types_loading(self):
        """Test loading plate types for a state"""
        # Get Florida state
        states = self.db_manager.search_states('FL')
        self.assertGreater(len(states), 0)
        
        state_id = states[0]['state_id']
        plate_types = self.db_manager.get_plate_types_for_state(state_id)
        self.assertGreater(len(plate_types), 0)
    
    def tearDown(self):
        """Clean up test database"""
        self.db_manager.close()

class TestHelperFunctions(unittest.TestCase):
    """Test utility helper functions"""
    
    def test_normalize_plate_text(self):
        """Test plate text normalization"""
        self.assertEqual(normalize_plate_text('abc-123'), 'ABC-123')
        self.assertEqual(normalize_plate_text('  ABC 123  '), 'ABC123')
        self.assertEqual(normalize_plate_text('ab@c#123'), 'ABC123')
        self.assertEqual(normalize_plate_text(''), '')
        self.assertEqual(normalize_plate_text(None), '')
    
    def test_generate_character_alternatives(self):
        """Test character alternative generation"""
        # Test 0/O alternatives
        alternatives = generate_character_alternatives('0')
        self.assertIn('0', alternatives)
        self.assertIn('O', alternatives)
        
        alternatives = generate_character_alternatives('O')
        self.assertIn('0', alternatives)
        self.assertIn('O', alternatives)
        
        # Test with state rules
        state_rules = {'allows_letter_o': False}
        alternatives = generate_character_alternatives('0', state_rules)
        self.assertIn('0', alternatives)
        # Should not include O since state doesn't allow it
        
        # Test non-ambiguous character
        alternatives = generate_character_alternatives('A')
        self.assertEqual(alternatives, ['A'])
    
    def test_validate_plate_pattern(self):
        """Test plate pattern validation"""
        # Test simple patterns
        self.assertTrue(validate_plate_pattern('ABC123', 'ABC123'))
        self.assertTrue(validate_plate_pattern('ABC-123', 'ABC-123'))
        self.assertFalse(validate_plate_pattern('AB123', 'ABC-123'))
        self.assertFalse(validate_plate_pattern('', 'ABC-123'))
        self.assertFalse(validate_plate_pattern('ABC-123', ''))
    
    def test_score_plate_match(self):
        """Test plate matching score calculation"""
        state_data = {
            'allows_letter_o': False,
            'uses_zero_for_o': True
        }
        
        plate_type = {
            'pattern': 'ABC-123',
            'character_count': 6
        }
        
        # Perfect match should score high
        score = score_plate_match('ABC-123', state_data, plate_type)
        self.assertGreater(score, 0.5)
        
        # Wrong pattern should score lower
        score = score_plate_match('ABCD-123', state_data, plate_type)
        self.assertLess(score, 0.5)
        
        # Empty inputs should score 0
        score = score_plate_match('', state_data, plate_type)
        self.assertEqual(score, 0.0)

class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def setUp(self):
        """Set up for integration tests"""
        self.db_manager = DatabaseManager(':memory:')
        self.db_manager.initialize_database()
    
    def test_florida_plate_lookup(self):
        """Test complete Florida plate lookup workflow"""
        # Search for Florida
        states = self.db_manager.search_states('FL')
        self.assertGreater(len(states), 0)
        
        florida = states[0]
        self.assertEqual(florida['abbreviation'], 'FL')
        self.assertEqual(florida['name'], 'Florida')
        
        # Check character rules
        self.assertTrue(florida['uses_zero_for_o'])
        self.assertFalse(florida['allows_letter_o'])
        
        # Get plate types
        plate_types = self.db_manager.get_plate_types_for_state(florida['state_id'])
        self.assertGreater(len(plate_types), 0)
        
        # Check that passenger plate type exists
        passenger_types = [pt for pt in plate_types if 'Passenger' in pt['type_name']]
        self.assertGreater(len(passenger_types), 0)
    
    def test_georgia_vs_florida_differences(self):
        """Test that Georgia and Florida have different character rules"""
        fl_states = self.db_manager.search_states('FL')
        ga_states = self.db_manager.search_states('GA')
        
        self.assertGreater(len(fl_states), 0)
        self.assertGreater(len(ga_states), 0)
        
        florida = fl_states[0]
        georgia = ga_states[0]
        
        # Florida uses 0 but not O
        self.assertTrue(florida['uses_zero_for_o'])
        self.assertFalse(florida['allows_letter_o'])
        
        # Georgia uses both 0 and O
        self.assertTrue(georgia['uses_zero_for_o'])
        self.assertTrue(georgia['allows_letter_o'])
        
        # Georgia has slashed zero, Florida doesn't
        self.assertTrue(georgia['zero_is_slashed'])
        self.assertFalse(florida['zero_is_slashed'])
    
    def tearDown(self):
        """Clean up"""
        self.db_manager.close()

if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)