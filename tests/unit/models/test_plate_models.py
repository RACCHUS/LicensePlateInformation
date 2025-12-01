"""
Unit tests for plate_models.py
Tests for State, PlateType, CharacterReference, and LookupHistory dataclasses
"""

import pytest
import json
from src.models.plate_models import State, PlateType, CharacterReference, LookupHistory


# ============================================================================
# STATE MODEL TESTS
# ============================================================================

class TestStateModel:
    """Test cases for State dataclass"""
    
    def test_state_creation_with_all_fields(self, sample_state_dict):
        """Test creating a State with all fields populated"""
        state = State(**sample_state_dict)
        
        assert state.state_id == 1
        assert state.name == 'California'
        assert state.abbreviation == 'CA'
        assert state.slogan == 'Golden State'
        assert state.uses_zero_for_o is False
        assert state.allows_letter_o is True
        assert state.zero_is_slashed is False
        assert state.primary_colors == ['#003F87', '#FFFFFF']
        assert state.notes == 'Test state data'
    
    def test_state_creation_minimal_fields(self):
        """Test creating a State with only required fields"""
        state = State(name='Texas', abbreviation='TX')
        
        assert state.name == 'Texas'
        assert state.abbreviation == 'TX'
        assert state.state_id is None
        assert state.slogan is None
        assert state.uses_zero_for_o is False
        assert state.allows_letter_o is True
        assert state.primary_colors == []  # Default empty list
    
    def test_state_post_init_colors(self):
        """Test that __post_init__ initializes colors as empty list"""
        state = State(name='Nevada', abbreviation='NV')
        assert state.primary_colors == []
        assert isinstance(state.primary_colors, list)
    
    def test_state_colors_json_property(self):
        """Test colors_json property returns JSON string"""
        state = State(
            name='California',
            abbreviation='CA',
            primary_colors=['#003F87', '#FFFFFF']
        )
        
        colors_json = state.colors_json
        assert isinstance(colors_json, str)
        
        # Verify it's valid JSON
        parsed = json.loads(colors_json)
        assert parsed == ['#003F87', '#FFFFFF']
    
    def test_state_colors_json_empty_list(self):
        """Test colors_json with empty colors list"""
        state = State(name='Texas', abbreviation='TX')
        colors_json = state.colors_json
        
        parsed = json.loads(colors_json)
        assert parsed == []
    
    def test_state_from_dict_complete(self, sample_state_dict):
        """Test State.from_dict() with complete data"""
        state = State.from_dict(sample_state_dict)
        
        assert state.name == 'California'
        assert state.abbreviation == 'CA'
        assert state.slogan == 'Golden State'
        assert state.primary_colors == ['#003F87', '#FFFFFF']
    
    def test_state_from_dict_with_json_colors(self):
        """Test State.from_dict() when colors is JSON string"""
        data = {
            'name': 'Florida',
            'abbreviation': 'FL',
            'primary_colors': '["#FF0000", "#00FF00"]'  # JSON string
        }
        
        state = State.from_dict(data)
        assert state.primary_colors == ['#FF0000', '#00FF00']
    
    def test_state_from_dict_with_list_colors(self):
        """Test State.from_dict() when colors is already a list"""
        data = {
            'name': 'Georgia',
            'abbreviation': 'GA',
            'primary_colors': ['#AABBCC', '#DDEEFF']  # Already a list
        }
        
        state = State.from_dict(data)
        assert state.primary_colors == ['#AABBCC', '#DDEEFF']
    
    def test_state_from_dict_invalid_json_colors(self):
        """Test State.from_dict() with invalid JSON in colors"""
        data = {
            'name': 'Hawaii',
            'abbreviation': 'HI',
            'primary_colors': 'invalid json string'
        }
        
        state = State.from_dict(data)
        assert state.primary_colors == []  # Falls back to empty list
    
    def test_state_boolean_conversions(self):
        """Test boolean field conversions"""
        data = {
            'name': 'Ohio',
            'abbreviation': 'OH',
            'uses_zero_for_o': 1,  # Integer
            'allows_letter_o': 0,  # Integer
            'zero_is_slashed': True  # Boolean
        }
        
        state = State.from_dict(data)
        assert state.uses_zero_for_o is True
        assert state.allows_letter_o is False
        assert state.zero_is_slashed is True
    
    def test_state_from_dict_missing_fields(self):
        """Test State.from_dict() with missing optional fields"""
        data = {
            'name': 'Idaho',
            'abbreviation': 'ID'
        }
        
        state = State.from_dict(data)
        assert state.name == 'Idaho'
        assert state.slogan is None
        assert state.uses_zero_for_o is False
        assert state.allows_letter_o is True


# ============================================================================
# PLATE TYPE MODEL TESTS
# ============================================================================

class TestPlateTypeModel:
    """Test cases for PlateType dataclass"""
    
    def test_plate_type_creation_complete(self, sample_plate_type_dict):
        """Test creating PlateType with all fields"""
        plate_type = PlateType(**sample_plate_type_dict)
        
        assert plate_type.type_id == 1
        assert plate_type.state_id == 1
        assert plate_type.type_name == 'Passenger'
        assert plate_type.pattern == '^[0-9][A-Z]{3}[0-9]{3}$'
        assert plate_type.character_count == 7
        assert plate_type.description == 'Standard passenger vehicle plate'
        assert plate_type.category == 'standard'
        assert plate_type.is_active is True
        assert plate_type.example_plate == '1ABC123'
    
    def test_plate_type_creation_minimal(self):
        """Test creating PlateType with minimal fields"""
        plate_type = PlateType(
            type_name='Commercial',
            pattern='^[A-Z]{3}[0-9]{4}$'
        )
        
        assert plate_type.type_name == 'Commercial'
        assert plate_type.pattern == '^[A-Z]{3}[0-9]{4}$'
        assert plate_type.type_id is None
        assert plate_type.state_id is None
    
    def test_plate_type_from_dict_complete(self, sample_plate_type_dict):
        """Test PlateType.from_dict() with complete data"""
        plate_type = PlateType.from_dict(sample_plate_type_dict)
        
        assert plate_type.type_name == 'Passenger'
        assert plate_type.pattern == '^[0-9][A-Z]{3}[0-9]{3}$'
        assert plate_type.character_count == 7
        assert plate_type.is_active is True
    
    def test_plate_type_from_dict_minimal(self):
        """Test PlateType.from_dict() with minimal data"""
        data = {
            'type_name': 'Motorcycle',
            'pattern': '^[0-9]{4}[A-Z]{2}$'
        }
        
        plate_type = PlateType.from_dict(data)
        assert plate_type.type_name == 'Motorcycle'
        assert plate_type.pattern == '^[0-9]{4}[A-Z]{2}$'
    
    def test_plate_type_optional_fields(self):
        """Test PlateType with various optional fields"""
        plate_type = PlateType(
            type_name='Government',
            pattern='^G[0-9]{5}$',
            background_color='#FF0000',
            text_color='#FFFFFF',
            has_stickers=False,
            notes='Government vehicle plates'
        )
        
        assert plate_type.background_color == '#FF0000'
        assert plate_type.text_color == '#FFFFFF'
        assert plate_type.has_stickers is False
        assert plate_type.notes == 'Government vehicle plates'


# ============================================================================
# CHARACTER REFERENCE MODEL TESTS
# ============================================================================

class TestCharacterReferenceModel:
    """Test cases for CharacterReference dataclass"""
    
    def test_character_reference_creation_complete(self, sample_character_reference_dict):
        """Test creating CharacterReference with all fields"""
        char_ref = CharacterReference(**sample_character_reference_dict)
        
        assert char_ref.character == '0'
        assert char_ref.type == 'number'
        assert char_ref.confusion_chars == ['O']
        assert char_ref.is_letter is False
        assert char_ref.is_number is True
        assert char_ref.notes == 'Zero vs letter O confusion'
    
    def test_character_reference_creation_minimal(self):
        """Test creating CharacterReference with minimal fields"""
        char_ref = CharacterReference(
            character='A',
            type='letter'
        )
        
        assert char_ref.character == 'A'
        assert char_ref.type == 'letter'
        assert char_ref.confusion_chars == []  # Default from __post_init__
    
    def test_character_reference_post_init(self):
        """Test __post_init__ initializes confusion_chars"""
        char_ref = CharacterReference(character='B', type='letter')
        
        assert char_ref.confusion_chars == []
        assert isinstance(char_ref.confusion_chars, list)
    
    def test_character_reference_confusion_chars_json(self):
        """Test confusion_chars_json property"""
        char_ref = CharacterReference(
            character='I',
            type='letter',
            confusion_chars=['1', 'L']
        )
        
        json_str = char_ref.confusion_chars_json
        assert isinstance(json_str, str)
        
        parsed = json.loads(json_str)
        assert parsed == ['1', 'L']
    
    def test_character_reference_from_dict_complete(self, sample_character_reference_dict):
        """Test CharacterReference.from_dict() with complete data"""
        char_ref = CharacterReference.from_dict(sample_character_reference_dict)
        
        assert char_ref.character == '0'
        assert char_ref.type == 'number'
        assert char_ref.confusion_chars == ['O']
    
    def test_character_reference_from_dict_with_json_confusion_chars(self):
        """Test from_dict when confusion_chars is JSON string"""
        data = {
            'character': 'I',
            'type': 'letter',
            'confusion_chars': '["1", "L"]'  # JSON string
        }
        
        char_ref = CharacterReference.from_dict(data)
        assert char_ref.confusion_chars == ['1', 'L']
    
    def test_character_reference_from_dict_with_list_confusion_chars(self):
        """Test from_dict when confusion_chars is already a list"""
        data = {
            'character': 'S',
            'type': 'letter',
            'confusion_chars': ['5']  # Already a list
        }
        
        char_ref = CharacterReference.from_dict(data)
        assert char_ref.confusion_chars == ['5']
    
    def test_character_reference_from_dict_invalid_json(self):
        """Test from_dict with invalid JSON in confusion_chars"""
        data = {
            'character': 'Z',
            'type': 'letter',
            'confusion_chars': 'invalid json'
        }
        
        char_ref = CharacterReference.from_dict(data)
        assert char_ref.confusion_chars == []  # Falls back to empty list


# ============================================================================
# LOOKUP HISTORY MODEL TESTS
# ============================================================================

class TestLookupHistoryModel:
    """Test cases for LookupHistory dataclass"""
    
    def test_lookup_history_creation(self):
        """Test creating LookupHistory"""
        history = LookupHistory(
            lookup_id=1,
            query='ABC123',
            state_code='CA',
            timestamp='2024-01-15 10:30:00',
            results_count=5
        )
        
        assert history.lookup_id == 1
        assert history.query == 'ABC123'
        assert history.state_code == 'CA'
        assert history.timestamp == '2024-01-15 10:30:00'
        assert history.results_count == 5
    
    def test_lookup_history_minimal(self):
        """Test creating LookupHistory with minimal fields"""
        history = LookupHistory(
            query='XYZ789'
        )
        
        assert history.query == 'XYZ789'
        assert history.lookup_id is None
        assert history.state_code is None
    
    def test_lookup_history_from_dict(self):
        """Test LookupHistory.from_dict()"""
        data = {
            'lookup_id': 42,
            'query': 'TEST123',
            'state_code': 'TX',
            'timestamp': '2024-01-20 15:45:00',
            'results_count': 10
        }
        
        history = LookupHistory.from_dict(data)
        assert history.lookup_id == 42
        assert history.query == 'TEST123'
        assert history.state_code == 'TX'
        assert history.results_count == 10
    
    def test_lookup_history_from_dict_missing_fields(self):
        """Test from_dict with missing optional fields"""
        data = {
            'query': 'MINIMAL'
        }
        
        history = LookupHistory.from_dict(data)
        assert history.query == 'MINIMAL'
        assert history.lookup_id is None


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestModelIntegration:
    """Integration tests for models working together"""
    
    def test_state_with_colors_roundtrip(self):
        """Test State colors JSON serialization/deserialization"""
        original = State(
            name='Colorado',
            abbreviation='CO',
            primary_colors=['#002868', '#BF0A30']
        )
        
        # Convert to JSON and back
        json_str = original.colors_json
        data = {
            'name': original.name,
            'abbreviation': original.abbreviation,
            'primary_colors': json_str
        }
        
        restored = State.from_dict(data)
        assert restored.primary_colors == original.primary_colors
    
    def test_character_reference_confusion_roundtrip(self):
        """Test CharacterReference confusion_chars serialization/deserialization"""
        original = CharacterReference(
            character='0',
            type='number',
            confusion_chars=['O']
        )
        
        # Convert to JSON and back
        json_str = original.confusion_chars_json
        data = {
            'character': original.character,
            'type': original.type,
            'confusion_chars': json_str
        }
        
        restored = CharacterReference.from_dict(data)
        assert restored.confusion_chars == original.confusion_chars
