"""
Pytest Configuration and Shared Fixtures
Global fixtures available to all tests
"""

import pytest
import json
import sqlite3
import tempfile
from pathlib import Path
from typing import Dict, Any
import sys
import os

# Add src to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))


# ============================================================================
# DATABASE FIXTURES
# ============================================================================

@pytest.fixture
def temp_db_path(tmp_path):
    """Provide a temporary database path"""
    db_path = tmp_path / "test_license_plates.db"
    return str(db_path)


@pytest.fixture
def db_manager(temp_db_path):
    """Provide a DatabaseManager instance with initialized schema"""
    from src.database.db_manager import DatabaseManager
    
    manager = DatabaseManager(temp_db_path)
    manager.initialize_database()
    yield manager
    
    # Cleanup
    if manager.connection:
        manager.connection.close()


@pytest.fixture
def populated_db(db_manager):
    """Provide a database populated with sample data"""
    # Add sample states
    states = [
        {
            'name': 'California',
            'abbreviation': 'CA',
            'slogan': 'Golden State',
            'uses_zero_for_o': False,
            'allows_letter_o': True,
            'zero_is_slashed': False,
            'primary_colors': json.dumps(['#003F87', '#FFFFFF']),
            'notes': 'Sample California data'
        },
        {
            'name': 'Texas',
            'abbreviation': 'TX',
            'slogan': 'The Lone Star State',
            'uses_zero_for_o': False,
            'allows_letter_o': True,
            'zero_is_slashed': False,
            'primary_colors': json.dumps(['#002868', '#FFFFFF']),
            'notes': 'Sample Texas data'
        }
    ]
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    # Delete any existing test states to avoid UNIQUE constraint violations
    # First delete related plate_types to avoid orphaned foreign keys
    for state in states:
        cursor.execute('DELETE FROM plate_types WHERE state_id IN (SELECT state_id FROM states WHERE abbreviation = ?)', (state['abbreviation'],))
        cursor.execute('DELETE FROM character_references WHERE state_id IN (SELECT state_id FROM states WHERE abbreviation = ?)', (state['abbreviation'],))
        cursor.execute('DELETE FROM states WHERE abbreviation = ?', (state['abbreviation'],))
    
    # Insert test states
    for state in states:
        cursor.execute('''
            INSERT INTO states (name, abbreviation, slogan, uses_zero_for_o, 
                              allows_letter_o, zero_is_slashed, primary_colors, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (state['name'], state['abbreviation'], state['slogan'],
              state['uses_zero_for_o'], state['allows_letter_o'],
              state['zero_is_slashed'], state['primary_colors'], state['notes']))
    
    conn.commit()
    return db_manager


# ============================================================================
# FILE SYSTEM FIXTURES
# ============================================================================

@pytest.fixture
def temp_dir(tmp_path):
    """Provide a temporary directory"""
    return tmp_path


@pytest.fixture
def sample_data_dir(tmp_path):
    """Create a temporary directory with sample JSON data"""
    data_dir = tmp_path / "data" / "states"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Create sample state JSON file
    california_data = {
        "state_info": {
            "name": "California",
            "abbreviation": "CA",
            "slogan": "Golden State",
            "primary_colors": ["#003F87", "#FFFFFF"],
            "uses_zero_for_o": False,
            "allows_letter_o": True
        },
        "plate_types": [
            {
                "type_name": "Passenger",
                "pattern": "^[0-9][A-Z]{3}[0-9]{3}$",
                "character_count": 7,
                "description": "Standard passenger vehicle plate",
                "category": "standard",
                "example_plate": "1ABC123"
            },
            {
                "type_name": "Commercial",
                "pattern": "^[0-9][A-Z][0-9]{5}$",
                "character_count": 7,
                "description": "Commercial vehicle plate",
                "category": "commercial",
                "example_plate": "1A12345"
            }
        ],
        "character_references": [
            {
                "character": "0",
                "type": "number",
                "confusion_chars": ["O"],
                "notes": "Zero vs letter O"
            }
        ]
    }
    
    with open(data_dir / "california.json", 'w', encoding='utf-8') as f:
        json.dump(california_data, f, indent=2)
    
    return data_dir


@pytest.fixture
def sample_image_dir(tmp_path):
    """Create a temporary directory structure for images"""
    from PIL import Image
    
    images_dir = tmp_path / "data" / "images"
    ca_dir = images_dir / "CA" / "plates" / "passenger"
    ca_dir.mkdir(parents=True, exist_ok=True)
    
    # Create a simple test image
    img = Image.new('RGB', (100, 50), color='blue')
    img.save(ca_dir / "test_plate.jpg")
    
    return images_dir


# ============================================================================
# DATA FIXTURES
# ============================================================================

@pytest.fixture
def sample_state_dict():
    """Provide sample state dictionary data"""
    return {
        'state_id': 1,
        'name': 'California',
        'abbreviation': 'CA',
        'slogan': 'Golden State',
        'uses_zero_for_o': False,
        'allows_letter_o': True,
        'zero_is_slashed': False,
        'primary_colors': ['#003F87', '#FFFFFF'],
        'notes': 'Test state data'
    }


@pytest.fixture
def sample_plate_type_dict():
    """Provide sample plate type dictionary data"""
    return {
        'type_id': 1,
        'state_id': 1,
        'type_name': 'Passenger',
        'pattern': '^[0-9][A-Z]{3}[0-9]{3}$',
        'character_count': 7,
        'description': 'Standard passenger vehicle plate',
        'is_active': True,
        'example_plate': '1ABC123',
        'background_color': '#003F87',
        'text_color': '#FFFFFF',
        'has_stickers': True,
        'sticker_description': 'Month/Year validation stickers'
    }


@pytest.fixture
def sample_character_reference_dict():
    """Provide sample character reference dictionary data"""
    return {
        'character': '0',
        'character_type': 'digit',
        'confusion_chars': ['O'],
        'description': 'Zero vs letter O confusion',
        'is_ambiguous': True
    }


# ============================================================================
# MOCK FIXTURES
# ============================================================================

@pytest.fixture
def mock_search_engine(sample_data_dir):
    """Provide a JSONSearchEngine with mocked data directory"""
    from src.gui.utils.json_search_engine import JSONSearchEngine
    
    engine = JSONSearchEngine(str(sample_data_dir))
    return engine


# ============================================================================
# UTILITY FIXTURES
# ============================================================================

@pytest.fixture
def project_root():
    """Get the project root directory"""
    return Path(__file__).parent.parent


@pytest.fixture
def data_directory(project_root):
    """Get the data directory path"""
    return project_root / "data"


@pytest.fixture
def states_directory(data_directory):
    """Get the states data directory path"""
    return data_directory / "states"


# ============================================================================
# PARAMETRIZE HELPERS
# ============================================================================

# Common test data for parametrized tests
AMBIGUOUS_CHAR_PAIRS = [
    ('0', 'O'),
    ('O', '0'),
    ('1', 'I'),
    ('1', 'L'),
    ('I', '1'),
    ('I', 'L'),
    ('L', '1'),
    ('L', 'I'),
    ('8', 'B'),
    ('B', '8'),
    ('5', 'S'),
    ('S', '5'),
    ('2', 'Z'),
    ('Z', '2'),
    ('6', 'G'),
    ('G', '6')
]

VALID_STATE_CODES = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA']
SAMPLE_PLATE_PATTERNS = [
    'ABC123',
    '123ABC',
    'ABC-123',
    '1ABC234',
    'A12-3BC'
]
