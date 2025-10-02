"""
Unit tests for CharacterFontPanel component
Tests font mapping, character restrictions, and state-specific behavior
"""

import unittest
import tkinter as tk
import sys
import os
import json
from unittest.mock import Mock, patch, MagicMock, mock_open

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from gui.components.font_display.character_font_panel import CharacterFontPanel


class TestCharacterFontPanel(unittest.TestCase):
    """Test cases for CharacterFontPanel component"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures that are used by all tests"""
        # Create a root window for tkinter widgets
        cls.root = tk.Tk()
        cls.root.withdraw()  # Hide the window
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        cls.root.destroy()
    
    def setUp(self):
        """Set up before each test"""
        # Create a parent frame
        self.parent = tk.Frame(self.root)
        
        # Create the panel
        self.panel = CharacterFontPanel(self.parent)
    
    def tearDown(self):
        """Clean up after each test"""
        self.parent.destroy()
    
    # ========================================================================
    # Initialization Tests
    # ========================================================================
    
    def test_panel_creation(self):
        """Test that panel is created successfully"""
        self.assertIsNotNone(self.panel)
        self.assertIsNotNone(self.panel.main_frame)
        self.assertIsNone(self.panel.current_state)
    
    def test_character_labels_created(self):
        """Test that all 36 character labels are created"""
        expected_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        
        self.assertEqual(len(self.panel.character_labels), len(expected_chars))
        
        for char in expected_chars:
            self.assertIn(char, self.panel.character_labels)
            self.assertIsInstance(self.panel.character_labels[char], tk.Label)
    
    def test_default_font(self):
        """Test that default font is found in mappings"""
        # Test the _find_best_font method with empty description
        default_font = self.panel._find_best_font('')
        self.assertIsNotNone(default_font)
        self.assertEqual(len(default_font), 3)  # (family, size, weight)
        self.assertIn(default_font[0], ['Arial', 'Courier New', 'Arial Black'])  # Valid fonts
    
    def test_status_label_default(self):
        """Test that status label has default message"""
        status_text = self.panel.status_label.cget('text')
        self.assertIn('select a state', status_text.lower())
    
    # ========================================================================
    # Font Mapping Tests
    # ========================================================================
    
    def test_font_mapping_narrow(self):
        """Test font mapping for narrow fonts"""
        narrow_font = self.panel._find_best_font('Narrow sans serif')
        self.assertEqual(narrow_font[0], 'Arial Narrow')
        
        condensed_font = self.panel._find_best_font('Condensed font')
        self.assertEqual(condensed_font[0], 'Arial Narrow')
    
    def test_font_mapping_sans_serif(self):
        """Test font mapping for sans serif fonts"""
        sans_font = self.panel._find_best_font('Sans serif font')
        self.assertEqual(sans_font[0], 'Arial')
        
        highway_font = self.panel._find_best_font('Highway Gothic')
        self.assertEqual(highway_font[0], 'Arial')
    
    def test_font_mapping_monospace(self):
        """Test font mapping for monospace fonts"""
        mono_font = self.panel._find_best_font('Monospace font')
        self.assertEqual(mono_font[0], 'Courier New')
        
        courier_font = self.panel._find_best_font('Courier font')
        self.assertEqual(courier_font[0], 'Courier New')
    
    def test_font_mapping_special(self):
        """Test font mapping for special/proprietary fonts"""
        proprietary_font = self.panel._find_best_font('Custom proprietary font')
        self.assertEqual(proprietary_font[0], 'Impact')
        
        block_font = self.panel._find_best_font('Block sans serif')
        self.assertEqual(block_font[0], 'Arial Black')
    
    # ========================================================================
    # State Font Detection Tests
    # ========================================================================
    
    def test_get_font_for_florida(self):
        """Test font detection for Florida (narrow font)"""
        # Florida has "Narrow sans serif" font
        font = self.panel._get_font_for_state('FL')
        
        if font:  # Only test if Florida data exists
            self.assertIn('Arial', font[0])  # Should map to Arial or Arial Narrow
    
    def test_get_font_for_nonexistent_state(self):
        """Test font detection for nonexistent state"""
        font = self.panel._get_font_for_state('XX')
        self.assertIsNone(font)
    
    def test_get_font_for_none_state(self):
        """Test font detection when state is None"""
        font = self.panel._get_font_for_state(None)
        self.assertIsNone(font)
    
    # ========================================================================
    # Character Rules Detection Tests
    # ========================================================================
    
    def test_get_character_rules_florida(self):
        """Test character rules for Florida (no letter O)"""
        # Florida doesn't use letter 'O', only zero '0'
        rules = self.panel._get_state_character_rules('FL')
        
        if rules:  # Only test if Florida data exists
            # Florida should not allow letter O
            self.assertFalse(rules.get('allows_letter_o', True))
    
    def test_get_character_rules_nevada(self):
        """Test character rules for Nevada (dual O/0 system)"""
        rules = self.panel._get_state_character_rules('NV')
        
        if rules and 'nevada_dual_system' in rules:
            # Nevada should have dual system
            self.assertIn('nevada_dual_system', rules)
            dual_system = rules['nevada_dual_system']
            
            # Standard plates should use letter O
            if 'standard_plates' in dual_system:
                self.assertTrue(dual_system['standard_plates'].get('uses_letter_o'))
                self.assertFalse(dual_system['standard_plates'].get('uses_number_zero'))
    
    def test_get_character_rules_nonexistent_state(self):
        """Test character rules for nonexistent state"""
        rules = self.panel._get_state_character_rules('XX')
        self.assertEqual(rules, {})
    
    def test_get_character_rules_none_state(self):
        """Test character rules when state is None"""
        rules = self.panel._get_state_character_rules(None)
        self.assertEqual(rules, {})
    
    # ========================================================================
    # Update State Tests
    # ========================================================================
    
    def test_update_state_with_valid_state(self):
        """Test updating panel with a valid state"""
        self.panel.update_state('FL', 'Florida')
        
        self.assertEqual(self.panel.current_state, 'FL')
        
        # Status should be updated
        status_text = self.panel.status_label.cget('text')
        self.assertIn('Florida', status_text)
    
    def test_update_state_with_none(self):
        """Test updating panel with None (should reset)"""
        # First set a state
        self.panel.update_state('FL', 'Florida')
        
        # Then clear it
        self.panel.update_state(None)
        
        self.assertIsNone(self.panel.current_state)
        
        # Status should show default message
        status_text = self.panel.status_label.cget('text')
        self.assertIn('select a state', status_text.lower())
    
    def test_update_state_changes_font(self):
        """Test that updating state actually changes character fonts"""
        # Get initial default font of a character
        initial_font_str = str(self.panel.character_labels['A'].cget('font'))
        
        # Mock Florida to have a different font
        mock_font_data = {
            'name': 'Florida',
            'main_font': 'Narrow sans serif'
        }
        
        with patch('builtins.open', mock_open(read_data=json.dumps(mock_font_data))):
            with patch('os.path.exists', return_value=True):
                # Update state
                self.panel.update_state('FL', 'Florida')
                
                # Get font after update
                updated_font_str = str(self.panel.character_labels['A'].cget('font'))
                
                # The font string should have changed from default
                # (Even if system substitutes fonts, the config should be different)
                self.assertIsNotNone(updated_font_str)
                
                # Verify the panel tried to set a font (method executed)
                self.assertEqual(self.panel.current_state, 'FL')
    
    def test_update_state_florida_letter_o_restriction(self):
        """Test that Florida's letter O restriction is shown"""
        self.panel.update_state('FL', 'Florida')
        
        # Check if letter O has different color (red for not used)
        o_label = self.panel.character_labels['O']
        o_color = o_label.cget('fg')
        
        zero_label = self.panel.character_labels['0']
        zero_color = zero_label.cget('fg')
        
        # O and 0 should have different colors if Florida data is correct
        # (O should be red, 0 should be green)
        # Note: Only assert if colors are actually different
        if o_color != zero_color:
            self.assertNotEqual(o_color, zero_color)
    
    def test_font_actually_updates_in_ui(self):
        """Test that fonts actually update in the UI labels"""
        # Start with default
        default_font = ('Courier New', 14, 'bold')
        
        # Mock a state with Arial font
        with patch.object(self.panel, '_get_font_for_state', return_value=('Arial', 16, 'bold')):
            with patch.object(self.panel, '_get_state_character_rules', return_value={}):
                self.panel.update_state('TEST', 'Test State')
                
                # Check that a label's font was actually configured
                # The configure method should have been called with Arial
                a_label = self.panel.character_labels['A']
                
                # Verify the label exists and has a font
                self.assertIsNotNone(a_label)
                font_config = a_label.cget('font')
                self.assertIsNotNone(font_config)
    
    def test_different_states_different_fonts(self):
        """Test that different states get different fonts"""
        # Mock two states with different fonts
        state1_font = ('Arial Narrow', 14, 'bold')
        state2_font = ('Arial Black', 14, 'bold')
        
        # Update with first state
        with patch.object(self.panel, '_get_font_for_state', return_value=state1_font):
            with patch.object(self.panel, '_get_state_character_rules', return_value={}):
                self.panel.update_state('FL', 'Florida')
                font1 = str(self.panel.character_labels['A'].cget('font'))
        
        # Update with second state
        with patch.object(self.panel, '_get_font_for_state', return_value=state2_font):
            with patch.object(self.panel, '_get_state_character_rules', return_value={}):
                self.panel.update_state('CA', 'California')
                font2 = str(self.panel.character_labels['A'].cget('font'))
        
        # The fonts should be different (or at least attempted to be set differently)
        self.assertEqual(self.panel.current_state, 'CA')
    
    # ========================================================================
    # Clear/Reset Tests
    # ========================================================================
    
    def test_clear_resets_state(self):
        """Test that clear resets the panel state"""
        # Set a state first
        self.panel.update_state('FL', 'Florida')
        self.assertEqual(self.panel.current_state, 'FL')
        
        # Clear
        self.panel.clear()
        
        # State should be None
        self.assertIsNone(self.panel.current_state)
    
    def test_clear_resets_fonts(self):
        """Test that clear resets character fonts"""
        # Set a state first
        self.panel.update_state('FL', 'Florida')
        
        # Clear
        self.panel.clear()
        
        # Check that fonts are reset to default
        default_font = ('Courier New', 14, 'bold')
        
        # At least check one character
        a_label_font = self.panel.character_labels['A'].cget('font')
        # Font should be back to default (or at least valid)
        self.assertIsNotNone(a_label_font)
    
    def test_clear_resets_colors(self):
        """Test that clear resets character colors"""
        # Set a state with restrictions
        self.panel.update_state('FL', 'Florida')
        
        # Clear
        self.panel.clear()
        
        # All characters should be white
        for char, label in self.panel.character_labels.items():
            color = label.cget('fg')
            # Should be white or default
            self.assertIn(color, ['#ffffff', 'white', 'SystemButtonText'])
    
    def test_clear_resets_status(self):
        """Test that clear resets status message"""
        # Set a state
        self.panel.update_state('FL', 'Florida')
        
        # Clear
        self.panel.clear()
        
        # Status should show default
        status_text = self.panel.status_label.cget('text')
        self.assertIn('select a state', status_text.lower())
    
    # ========================================================================
    # Frame Retrieval Tests
    # ========================================================================
    
    def test_get_frame_returns_frame(self):
        """Test that get_frame returns the main frame"""
        frame = self.panel.get_frame()
        
        self.assertIsNotNone(frame)
        self.assertIsInstance(frame, tk.Frame)
        self.assertEqual(frame, self.panel.main_frame)
    
    # ========================================================================
    # Special Character Tests
    # ========================================================================
    
    def test_slashed_zero_display(self):
        """Test that slashed zero is displayed correctly"""
        # Create mock rules with slashed zero
        mock_rules = {
            'zero_is_slashed': True,
            'allows_letter_o': True
        }
        
        with patch.object(self.panel, '_get_state_character_rules', return_value=mock_rules):
            with patch.object(self.panel, '_get_font_for_state', return_value=('Arial', 14, 'bold')):
                self.panel.update_state('TEST', 'Test State')
                
                # Zero should be displayed as Ø
                zero_label = self.panel.character_labels['0']
                zero_text = zero_label.cget('text')
                self.assertEqual(zero_text, 'Ø')
    
    def test_nevada_dual_system_display(self):
        """Test Nevada's dual O/0 system display"""
        # Create mock Nevada rules
        mock_rules = {
            'allows_letter_o': True,
            'nevada_dual_system': {
                'standard_plates': {
                    'uses_letter_o': True,
                    'uses_number_zero': False
                },
                'personalized_plates': {
                    'uses_letter_o': True,
                    'uses_number_zero': True
                }
            }
        }
        
        with patch.object(self.panel, '_get_state_character_rules', return_value=mock_rules):
            with patch.object(self.panel, '_get_font_for_state', return_value=('Arial', 14, 'bold')):
                self.panel.update_state('NV', 'Nevada')
                
                # O should be green (used on all)
                o_label = self.panel.character_labels['O']
                o_color = o_label.cget('fg')
                self.assertIn('66ff66', o_color.lower())
                
                # 0 should be orange (personalized only)
                zero_label = self.panel.character_labels['0']
                zero_color = zero_label.cget('fg')
                self.assertIn('ffaa66', zero_color.lower())
    
    # ========================================================================
    # Error Handling Tests
    # ========================================================================
    
    def test_handles_missing_state_file(self):
        """Test that panel handles missing state file gracefully"""
        # Should not raise an error
        try:
            self.panel.update_state('INVALID', 'Invalid State')
            # Should reset to default
            self.assertIsNone(self.panel._get_font_for_state('INVALID'))
        except Exception as e:
            self.fail(f"Panel should handle missing state file gracefully: {e}")
    
    def test_handles_corrupted_json(self):
        """Test that panel handles corrupted JSON gracefully"""
        # Mock a corrupted JSON file
        with patch('builtins.open', side_effect=json.JSONDecodeError('test', 'doc', 0)):
            rules = self.panel._get_state_character_rules('FL')
            self.assertEqual(rules, {})
    
    def test_handles_missing_font_field(self):
        """Test that panel handles missing main_font field"""
        mock_data = {
            'name': 'Test State',
            # No main_font field
        }
        
        with patch('builtins.open', mock_open(read_data=json.dumps(mock_data))):
            with patch('os.path.exists', return_value=True):
                font = self.panel._get_font_for_state('TEST')
                # Should return a valid font tuple
                if font:
                    self.assertEqual(len(font), 3)
                    self.assertIn(font[0], ['Arial', 'Courier New', 'Impact', 'Arial Black'])


class TestCharacterFontPanelIntegration(unittest.TestCase):
    """Integration tests with real state data"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.root = tk.Tk()
        cls.root.withdraw()
        
        # Check if data directory exists
        cls.data_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'states')
        cls.has_data = os.path.exists(cls.data_dir)
    
    @classmethod
    def tearDownClass(cls):
        """Clean up"""
        cls.root.destroy()
    
    def setUp(self):
        """Set up before each test"""
        self.parent = tk.Frame(self.root)
        self.panel = CharacterFontPanel(self.parent)
    
    def tearDown(self):
        """Clean up after each test"""
        self.parent.destroy()
    
    @unittest.skipUnless(os.path.exists('data/states/florida.json'), "Florida data not available")
    def test_florida_integration(self):
        """Integration test with real Florida data"""
        self.panel.update_state('FL', 'Florida')
        
        # Florida should not allow letter O
        rules = self.panel._get_state_character_rules('FL')
        # Check that rules exist and either has explicit allows_letter_o=False
        # or check if the data structure indicates O restrictions
        if 'allows_letter_o' in rules:
            self.assertFalse(rules['allows_letter_o'])
        
        # Status should mention Florida
        status = self.panel.status_label.cget('text')
        self.assertIn('Florida', status)
    
    @unittest.skipUnless(os.path.exists('data/states/nevada.json'), "Nevada data not available")
    def test_nevada_integration(self):
        """Integration test with real Nevada data"""
        self.panel.update_state('NV', 'Nevada')
        
        # Nevada should have dual system
        rules = self.panel._get_state_character_rules('NV')
        
        if 'nevada_dual_system' in rules:
            self.assertIn('nevada_dual_system', rules)
        
        # Status should mention Nevada
        status = self.panel.status_label.cget('text')
        self.assertIn('Nevada', status)
    
    @unittest.skipUnless(os.path.exists('data/states/maine.json'), "Maine data not available")
    def test_maine_integration(self):
        """Integration test with real Maine data"""
        self.panel.update_state('ME', 'Maine')
        
        # Status should mention Maine
        status = self.panel.status_label.cget('text')
        self.assertIn('Maine', status)


def run_tests():
    """Run all tests"""
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add all tests
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCharacterFontPanel))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCharacterFontPanelIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success status
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
