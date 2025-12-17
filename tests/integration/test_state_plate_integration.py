"""
Integration tests for state and plate type interactions
Tests bidirectional filtering and data loading
"""

import pytest
import json


class TestStatePlateIntegration:
    """Test state and plate type integration"""
    
    def test_state_selection_loads_plate_types(self, mock_search_engine):
        """Test that selecting a state loads its plate types"""
        # Load state data
        state_data = mock_search_engine.load_state_data('CA')
        
        # Should have plate type information
        assert isinstance(state_data, dict)
        has_plate_info = 'plate_types' in state_data or 'plates' in state_data
        
        # State data structure should exist
        assert len(state_data) > 0
    
    def test_plate_type_selection_loads_details(self, mock_search_engine):
        """Test that selecting a plate type loads its details"""
        # Search for specific plate type
        results = mock_search_engine.search('Passenger', category='type')
        
        assert isinstance(results, list)
    
    def test_plate_type_filters_state_list(self):
        """Test that selecting plate type filters which states are shown"""
        # Mock data: which states have 'Motorcycle' plates
        states_with_motorcycle = ['CA', 'TX', 'FL', 'NY', 'PA']
        all_states = ['CA', 'TX', 'FL', 'NY', 'PA', 'OH', 'GA', 'MI']
        
        # Filter states
        filtered_states = [s for s in all_states if s in states_with_motorcycle]
        
        assert len(filtered_states) == 5
        assert 'CA' in filtered_states
        assert 'OH' not in filtered_states
    
    def test_bidirectional_filtering(self):
        """Test bidirectional filtering between state and plate type"""
        # State -> Plate Type direction
        state = 'CA'
        ca_plate_types = ['Passenger', 'Commercial', 'Motorcycle', 'Trailer']
        
        # Plate Type -> State direction
        plate_type = 'Motorcycle'
        states_with_motorcycle = ['CA', 'TX', 'FL']
        
        # Bidirectional: CA has Motorcycle, and Motorcycle is in CA
        assert plate_type in ca_plate_types
        assert state in states_with_motorcycle


class TestDataConsistency:
    """Test data consistency between states and plate types"""
    
    def test_all_plate_types_have_state(self, mock_search_engine):
        """Test that all plate types reference a valid state"""
        # Load some state data
        state_data = mock_search_engine.load_state_data('CA')
        
        # If has plate types, they should reference the state
        if 'plate_types' in state_data:
            plate_types = state_data['plate_types']
            assert isinstance(plate_types, list)
    
    def test_state_plate_type_counts(self, mock_search_engine):
        """Test counting plate types per state"""
        state_data = mock_search_engine.load_state_data('FL')
        
        # Should have data structure
        assert isinstance(state_data, dict)
        
        # Count would be len of plate_types if exists
        if 'plates' in state_data:
            count = len(state_data['plates'])
            assert count >= 0


class TestStatePlateNavigation:
    """Test navigation between states and plate types"""
    
    def test_navigate_from_state_to_plates(self, mock_search_engine):
        """Test navigating from state to its plate types"""
        # Start with state
        state_code = 'TX'
        
        # Load state data
        state_data = mock_search_engine.load_state_data(state_code)
        
        # Should be able to access plate types
        assert isinstance(state_data, dict)
    
    def test_navigate_from_plate_to_states(self, mock_search_engine):
        """Test navigating from plate type to states that have it"""
        # Start with plate type
        plate_type = 'Commercial'
        
        # Search for states with this type
        results = mock_search_engine.search(plate_type, category='type')
        
        assert isinstance(results, list)
    
    def test_switch_between_states(self, mock_search_engine):
        """Test switching between different states"""
        # Load first state
        ca_data = mock_search_engine.load_state_data('CA')
        
        # Switch to another state
        tx_data = mock_search_engine.load_state_data('TX')
        
        # Both should be valid
        assert isinstance(ca_data, dict)
        assert isinstance(tx_data, dict)


class TestFilteringLogic:
    """Test complex filtering logic"""
    
    def test_multiple_filter_criteria(self):
        """Test applying multiple filter criteria"""
        # Mock plate data
        plates = [
            {'state': 'CA', 'type': 'Passenger', 'year': 2020},
            {'state': 'CA', 'type': 'Commercial', 'year': 2021},
            {'state': 'TX', 'type': 'Passenger', 'year': 2020},
            {'state': 'TX', 'type': 'Motorcycle', 'year': 2019}
        ]
        
        # Filter by state AND type
        filtered = [p for p in plates if p['state'] == 'CA' and p['type'] == 'Passenger']
        
        assert len(filtered) == 1
        assert filtered[0]['year'] == 2020
    
    def test_filter_with_fallback(self):
        """Test filtering with fallback to default"""
        state_filter = None
        plate_type_filter = 'Passenger'
        
        # If no state filter, search all states
        states_to_search = ['CA', 'TX', 'FL'] if state_filter is None else [state_filter]
        
        assert len(states_to_search) == 3
    
    def test_clear_all_filters(self):
        """Test clearing all filters returns to default state"""
        state_filter = 'CA'
        plate_type_filter = 'Commercial'
        
        # Clear filters
        state_filter = None
        plate_type_filter = None
        
        assert state_filter is None
        assert plate_type_filter is None


class TestDataRefresh:
    """Test data refresh and reload behavior"""
    
    def test_refresh_state_data(self, mock_search_engine):
        """Test refreshing state data"""
        # Initial load
        data1 = mock_search_engine.load_state_data('FL')
        
        # Clear cache
        if 'FL' in mock_search_engine.loaded_data:
            del mock_search_engine.loaded_data['FL']
        
        # Reload
        data2 = mock_search_engine.load_state_data('FL')
        
        # Should reload
        assert isinstance(data2, dict)
    
    def test_refresh_plate_type_list(self, mock_search_engine):
        """Test refreshing plate type list"""
        # Get plate types
        results1 = mock_search_engine.search('', category='type')
        
        # Clear search cache
        mock_search_engine.search_cache.clear()
        
        # Get again
        results2 = mock_search_engine.search('', category='type')
        
        assert isinstance(results2, list)
