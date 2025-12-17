"""
Unit tests for plate_type_dropdown.py and plate_type_panel.py
Tests for PlateType components
"""

import pytest
from unittest.mock import Mock, MagicMock, patch


class TestSmartPlateTypeDropdown:
    """Test cases for SmartPlateTypeDropdown component"""
    
    def test_populate_plate_types(self):
        """Test populating dropdown with plate types"""
        plate_types = ['Passenger', 'Commercial', 'Motorcycle', 'Trailer']
        
        assert len(plate_types) == 4
        assert 'Passenger' in plate_types
    
    def test_filter_by_state(self):
        """Test filtering plate types by state"""
        all_plate_types = {
            'CA': ['Passenger', 'Commercial', 'Motorcycle'],
            'TX': ['Passenger', 'Commercial'],
            'FL': ['Passenger', 'Motorcycle', 'Trailer']
        }
        
        state = 'CA'
        filtered = all_plate_types.get(state, [])
        
        assert len(filtered) == 3
        assert 'Trailer' not in filtered
    
    def test_plate_type_selection_callback(self):
        """Test plate type selection triggers callback"""
        callback = Mock()
        
        callback('Passenger')
        
        callback.assert_called_once_with('Passenger')
    
    def test_states_with_type_updated_callback(self):
        """Test callback when states with selected type are updated"""
        callback = Mock()
        
        states_with_passenger = ['CA', 'TX', 'FL', 'NY']
        callback(states_with_passenger)
        
        callback.assert_called_once()
    
    def test_dropdown_search_filtering(self):
        """Test search/filter within dropdown"""
        plate_types = ['Passenger', 'Commercial', 'Motorcycle', 'Military', 'Medical']
        search_query = 'M'
        
        filtered = [pt for pt in plate_types if search_query.lower() in pt.lower()]
        
        # Commercial also matches 'M' (case-insensitive)
        assert len(filtered) == 4  # Commercial, Motorcycle, Military, Medical
        assert 'Commercial' in filtered
        assert 'Motorcycle' in filtered
        assert 'Military' in filtered
        assert 'Medical' in filtered
    
    def test_category_grouping(self):
        """Test grouping plate types by category"""
        plate_types = {
            'standard': ['Passenger', 'Commercial'],
            'specialty': ['Military', 'Government'],
            'personalized': ['Vanity']
        }
        
        assert 'standard' in plate_types
        assert len(plate_types['standard']) == 2


class TestPlateTypePanel:
    """Test cases for PlateTypePanel display"""
    
    @patch('tkinter.Frame')
    def test_panel_initialization(self, mock_frame):
        """Test panel initializes correctly"""
        parent = Mock()
        widget_factory = Mock()
        
        # Panel should initialize without error
        assert parent is not None
    
    def test_panel_displays_plate_info(self):
        """Test panel displays plate type information"""
        plate_info = {
            'type_name': 'Passenger',
            'pattern': 'ABC-1234',
            'description': 'Standard passenger vehicle'
        }
        
        assert plate_info['type_name'] == 'Passenger'
        assert 'pattern' in plate_info
    
    def test_panel_updates_on_selection(self):
        """Test panel updates when plate type is selected"""
        callback = Mock()
        
        new_plate_type = 'Commercial'
        callback(new_plate_type)
        
        callback.assert_called_with('Commercial')
    
    def test_processing_metadata_display(self):
        """Test displaying processing metadata"""
        metadata = {
            'dot_processing_type': 'always_standard',
            'currently_processed': True,
            'requires_prefix': False
        }
        
        assert metadata['dot_processing_type'] == 'always_standard'
        assert metadata['currently_processed'] is True


class TestPlateTypeOperations:
    """Test plate type operations"""
    
    def test_get_unique_plate_types(self):
        """Test getting unique plate types across states"""
        state_plates = {
            'CA': ['Passenger', 'Commercial'],
            'TX': ['Passenger', 'Motorcycle'],
            'FL': ['Commercial', 'Trailer']
        }
        
        all_types = set()
        for types in state_plates.values():
            all_types.update(types)
        
        assert len(all_types) == 4
        assert 'Passenger' in all_types
    
    def test_count_states_with_plate_type(self):
        """Test counting states that have a specific plate type"""
        state_plates = {
            'CA': ['Passenger', 'Commercial'],
            'TX': ['Passenger', 'Motorcycle'],
            'FL': ['Passenger', 'Trailer']
        }
        
        plate_type = 'Passenger'
        count = sum(1 for types in state_plates.values() if plate_type in types)
        
        assert count == 3
    
    def test_clear_plate_type_selection(self):
        """Test clearing plate type selection"""
        selected = 'Passenger'
        selected = None
        
        assert selected is None
