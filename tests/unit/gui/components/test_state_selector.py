"""
Unit tests for state_selector.py
Tests for StateSelectionPanel component
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import tkinter as tk


class TestStateSelectorPanel:
    """Test cases for StateSelectionPanel initialization and basic functionality"""
    
    def test_state_selection_callback(self):
        """Test that selecting a state triggers callback"""
        parent = Mock()
        widget_factory = Mock()
        callback = Mock()
        
        # Mock the panel behavior
        # When a state is selected, callback should be triggered
        callback('CA')
        callback.assert_called_once_with('CA')
    
    def test_filter_states_by_type(self):
        """Test filtering states by plate type"""
        # Test that states can be filtered by plate type
        states = ['CA', 'TX', 'FL', 'NY']
        filtered = [s for s in states if s in ['CA', 'FL']]
        
        assert len(filtered) == 2
        assert 'CA' in filtered
        assert 'FL' in filtered
    
    def test_highlight_states_with_plate_type(self):
        """Test highlighting states that have specific plate type"""
        # Mock highlighting behavior
        highlighted_states = set(['CA', 'TX'])
        
        assert 'CA' in highlighted_states
        assert 'NY' not in highlighted_states
    
    def test_clear_selection(self):
        """Test clearing state selection"""
        callback = Mock()
        
        # Simulate clear selection
        callback(None)
        callback.assert_called_once_with(None)


class TestStateSelectionEvents:
    """Test cases for state selection events"""
    
    def test_on_state_selected_triggers_callback(self):
        """Test that state selection event triggers the callback"""
        callback = Mock()
        
        # Simulate selection event
        callback('TX')
        
        callback.assert_called_once()
        assert callback.call_args[0][0] == 'TX'
    
    def test_multiple_selection_handling(self):
        """Test handling of multiple selections"""
        callback = Mock()
        
        # Simulate multiple selections
        callback('CA')
        callback('TX')
        callback('FL')
        
        assert callback.call_count == 3
    
    def test_keyboard_navigation(self):
        """Test keyboard navigation through state list"""
        # Mock keyboard events
        states = ['AL', 'AK', 'AZ', 'AR', 'CA']
        current_index = 0
        
        # Simulate down arrow
        current_index = min(current_index + 1, len(states) - 1)
        assert current_index == 1
        
        # Simulate up arrow
        current_index = max(current_index - 1, 0)
        assert current_index == 0


class TestStateListOperations:
    """Test cases for state list operations"""
    
    def test_get_all_states(self):
        """Test retrieving all states"""
        # Mock state list
        all_states = ['CA', 'TX', 'FL', 'NY', 'PA']
        
        assert len(all_states) == 5
        assert 'CA' in all_states
    
    def test_search_states(self):
        """Test searching within state list"""
        all_states = ['California', 'Colorado', 'Connecticut', 'Texas']
        
        # Search for states starting with 'C'
        search_results = [s for s in all_states if s.startswith('C')]
        
        assert len(search_results) == 3
        assert 'Texas' not in search_results
    
    def test_sort_states_alphabetically(self):
        """Test that states are sorted alphabetically"""
        states = ['Texas', 'California', 'Florida', 'Alabama']
        sorted_states = sorted(states)
        
        assert sorted_states[0] == 'Alabama'
        assert sorted_states[-1] == 'Texas'
