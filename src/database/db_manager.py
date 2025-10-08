"""
Database management for License Plate Information System
Handles SQLite database creation, updates, and queries
"""

import sqlite3
import os
import sys
import json
from typing import List, Dict, Optional, Tuple

class DatabaseManager:
    """Manages SQLite database operations for license plate data"""
    
    def __init__(self, db_path: Optional[str] = None):
        """Initialize database manager
        
        Args:
            db_path: Path to SQLite database file. If None, uses default location.
        """
        if db_path is None:
            # Get base application path (works for both script and PyInstaller)
            if getattr(sys, 'frozen', False):
                # When frozen, use the directory where the executable is located (writable)
                application_path = os.path.dirname(sys.executable)
            else:
                application_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            
            # Create data directory if it doesn't exist
            data_dir = os.path.join(application_path, 'data', 'database')
            os.makedirs(data_dir, exist_ok=True)
            db_path = os.path.join(data_dir, 'license_plates.db')
        
        self.db_path = db_path
        self.connection = None
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection, creating if necessary"""
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # Enable column access by name
        return self.connection
    
    def initialize_database(self):
        """Create database tables if they don't exist"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # States table - core state information
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS states (
                state_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                abbreviation TEXT NOT NULL UNIQUE,
                slogan TEXT,
                uses_zero_for_o BOOLEAN DEFAULT 0,
                allows_letter_o BOOLEAN DEFAULT 1,
                zero_is_slashed BOOLEAN DEFAULT 0,
                primary_colors TEXT,  -- JSON array of hex colors
                logo_path TEXT,
                notes TEXT,
                created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Plate types - different plate formats within each state
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS plate_types (
                type_id INTEGER PRIMARY KEY AUTOINCREMENT,
                state_id INTEGER NOT NULL,
                type_name TEXT NOT NULL,  -- e.g., "Passenger", "Commercial", "Motorcycle"
                pattern TEXT,  -- Regex or pattern like "ABC-1234"
                character_count INTEGER,
                description TEXT,
                category TEXT,  -- New field for plate type category (government, military, etc.)
                is_active BOOLEAN DEFAULT 1,
                example_plate TEXT,
                background_color TEXT,  -- Hex color
                text_color TEXT,  -- Hex color
                has_stickers BOOLEAN DEFAULT 0,
                sticker_description TEXT,
                image_path TEXT,
                notes TEXT,
                -- COMPREHENSIVE PROCESSING METADATA
                code_number TEXT,  -- DMV code number
                currently_processed BOOLEAN DEFAULT 0,  -- Is currently being processed
                requires_prefix BOOLEAN DEFAULT 0,  -- Add prefix to plate string
                requires_suffix BOOLEAN DEFAULT 0,  -- Add suffix to plate string
                character_modifications TEXT,  -- Omit or add any characters
                verify_state_abbreviation BOOLEAN DEFAULT 0,  -- Verify state abbreviation
                visual_identifier TEXT,  -- Viewable plate type identifier
                vehicle_type_identification TEXT,  -- Vehicle type identification rules
                all_numeric_plate BOOLEAN DEFAULT 0,  -- Is the plate all numeric
                date_ranges TEXT,  -- JSON date ranges
                plate_images_available TEXT,  -- Available plate images
                -- CRITICAL DOT PROCESSING CLASSIFICATION
                dot_processing_type TEXT DEFAULT 'unknown',  -- 'always_standard', 'never_standard', 'conditional', 'unknown'
                dot_dropdown_identifier TEXT,  -- Specific dropdown ID/name for non-standard processing
                dot_conditional_rules TEXT,  -- JSON rules for conditional processing (e.g., all_numeric conditions)
                FOREIGN KEY (state_id) REFERENCES states (state_id)
            )
        ''')
        
        # Character references - state-specific character appearance
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS character_references (
                ref_id INTEGER PRIMARY KEY AUTOINCREMENT,
                state_id INTEGER NOT NULL,
                character TEXT NOT NULL,  -- Single character: '0', 'O', '1', 'I', etc.
                character_type TEXT,  -- 'digit' or 'letter'
                image_path TEXT,
                description TEXT,  -- e.g., "Slashed zero", "Serif font"
                is_ambiguous BOOLEAN DEFAULT 0,
                confusion_chars TEXT,  -- JSON array of easily confused characters
                FOREIGN KEY (state_id) REFERENCES states (state_id)
            )
        ''')
        
        # Lookup history - track searches for analysis
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lookup_history (
                lookup_id INTEGER PRIMARY KEY AUTOINCREMENT,
                search_term TEXT,
                state_found TEXT,
                plate_type_found TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_notes TEXT
            )
        ''')
        
        # Create indexes for fast searching
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_states_name ON states (name)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_states_abbrev ON states (abbreviation)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_plate_types_state ON plate_types (state_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_char_refs_state ON character_references (state_id)')
        
        conn.commit()
        
        # Load initial data if database is empty
        if self.get_state_count() == 0:
            self._load_initial_data()
    
    def get_state_count(self) -> int:
        """Get total number of states in database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM states')
        return cursor.fetchone()[0]
    
    def search_states(self, search_term: str) -> List[Dict]:
        """Search states by name or abbreviation
        
        Args:
            search_term: State name or abbreviation to search for
            
        Returns:
            List of matching state records
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        search_term = search_term.strip().upper()
        
        cursor.execute('''
            SELECT * FROM states 
            WHERE UPPER(name) LIKE ? OR UPPER(abbreviation) LIKE ?
            ORDER BY 
                CASE 
                    WHEN UPPER(abbreviation) = ? THEN 1
                    WHEN UPPER(name) = ? THEN 2
                    WHEN UPPER(abbreviation) LIKE ? THEN 3
                    ELSE 4
                END,
                name
        ''', (f'%{search_term}%', f'%{search_term}%', search_term, search_term.title(), f'{search_term}%'))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def get_all_states(self) -> List[Dict]:
        """Get all states in alphabetical order
        
        Returns:
            List of all state records sorted by name
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM states ORDER BY name')
        return [dict(row) for row in cursor.fetchall()]
    
    def get_state_by_id(self, state_id: int) -> Optional[Dict]:
        """Get state by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM states WHERE state_id = ?', (state_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_plate_types_for_state(self, state_id: int) -> List[Dict]:
        """Get all plate types for a specific state"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM plate_types 
            WHERE state_id = ? AND is_active = 1
            ORDER BY type_name
        ''', (state_id,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def get_character_references_for_state(self, state_id: int) -> List[Dict]:
        """Get character references for a specific state"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM character_references 
            WHERE state_id = ?
            ORDER BY character_type, character
        ''', (state_id,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def add_lookup_to_history(self, search_term: str, state_found: Optional[str] = None, 
                             plate_type_found: Optional[str] = None, user_notes: Optional[str] = None):
        """Add a lookup to history for tracking"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO lookup_history (search_term, state_found, plate_type_found, user_notes)
            VALUES (?, ?, ?, ?)
        ''', (search_term, state_found, plate_type_found, user_notes))
        
        conn.commit()
    
    def _load_initial_data(self):
        """Load initial state data into database"""
        # Get base application path (works for both script and PyInstaller)
        if getattr(sys, 'frozen', False):
            application_path = sys._MEIPASS  # type: ignore
        else:
            application_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        
        # This will load from JSON files in data/states/ directory
        states_dir = os.path.join(application_path, 'data', 'states')
        
        if not os.path.exists(states_dir):
            # Create sample states if directory doesn't exist
            self._create_sample_states()
            return
        
        # Load all JSON files from states directory
        for filename in os.listdir(states_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(states_dir, filename)
                try:
                    with open(filepath, 'r') as f:
                        state_data = json.load(f)
                    self._insert_state_data(state_data)
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
    
    def _create_sample_states(self):
        """Create sample state data for Florida and a few common out-of-state plates"""
        sample_states = [
            {
                "name": "Florida",
                "abbreviation": "FL",
                "slogan": "Sunshine State",
                "uses_zero_for_o": True,
                "allows_letter_o": False,
                "zero_is_slashed": False,
                "primary_colors": ["#FF8C00", "#FFFFFF", "#000000"],  # Orange, White, Black
                "notes": "Primary toll state. Uses digits 0-9, no letter O in standard plates.",
                "plate_types": [
                    {
                        "type_name": "Passenger",
                        "pattern": "ABC-123D",
                        "character_count": 7,
                        "description": "Standard passenger vehicle plate",
                        "background_color": "#FF8C00",
                        "text_color": "#000000",
                        "has_stickers": True,
                        "sticker_description": "Registration sticker top-left, validation sticker varies"
                    },
                    {
                        "type_name": "Commercial",
                        "pattern": "A12-34BC",
                        "character_count": 7,
                        "description": "Commercial vehicle plate",
                        "background_color": "#FFFFFF",
                        "text_color": "#000000",
                        "has_stickers": True,
                        "sticker_description": "Registration and weight class stickers"
                    }
                ]
            },
            {
                "name": "Georgia",
                "abbreviation": "GA",
                "slogan": "Peach State",
                "uses_zero_for_o": True,
                "allows_letter_o": True,
                "zero_is_slashed": True,
                "primary_colors": ["#FFFFFF", "#000000"],
                "notes": "Common out-of-state plate. Uses both 0 and O, zero is slashed.",
                "plate_types": [
                    {
                        "type_name": "Passenger",
                        "pattern": "ABC-1234",
                        "character_count": 7,
                        "description": "Standard format with county sticker",
                        "background_color": "#FFFFFF",
                        "text_color": "#000000",
                        "has_stickers": True,
                        "sticker_description": "County name sticker at top"
                    }
                ]
            },
            {
                "name": "Alabama",
                "abbreviation": "AL",
                "slogan": "Heart of Dixie",
                "uses_zero_for_o": False,
                "allows_letter_o": True,
                "zero_is_slashed": False,
                "primary_colors": ["#FFFFFF", "#FF0000", "#000000"],
                "notes": "Uses letter O in plates, zero not slashed.",
                "plate_types": [
                    {
                        "type_name": "Passenger",
                        "pattern": "12A-34BC",
                        "character_count": 7,
                        "description": "Standard passenger format",
                        "background_color": "#FFFFFF",
                        "text_color": "#000000",
                        "has_stickers": False
                    }
                ]
            }
        ]
        
        for state_data in sample_states:
            self._insert_state_data(state_data)
    
    def _insert_state_data(self, state_data: Dict):
        """Insert state data from dictionary into database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Insert state
            cursor.execute('''
                INSERT OR REPLACE INTO states 
                (name, abbreviation, slogan, uses_zero_for_o, allows_letter_o, 
                 zero_is_slashed, primary_colors, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                state_data['name'],
                state_data['abbreviation'],
                state_data.get('slogan'),
                state_data.get('uses_zero_for_o', False),
                state_data.get('allows_letter_o', True),
                state_data.get('zero_is_slashed', False),
                json.dumps(state_data.get('primary_colors', [])),
                state_data.get('notes')
            ))
            
            state_id = cursor.lastrowid
            
            # Insert plate types
            for plate_type in state_data.get('plate_types', []):
                # Extract processing metadata
                proc_meta = plate_type.get('processing_metadata', {})
                
                cursor.execute('''
                    INSERT INTO plate_types 
                    (state_id, type_name, pattern, character_count, description, category,
                     background_color, text_color, has_stickers, sticker_description,
                     code_number, currently_processed, requires_prefix, requires_suffix,
                     character_modifications, verify_state_abbreviation, visual_identifier,
                     vehicle_type_identification, all_numeric_plate, date_ranges, plate_images_available,
                     dot_processing_type, dot_dropdown_identifier, dot_conditional_rules)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    state_id,
                    plate_type['type_name'],
                    plate_type.get('pattern'),
                    plate_type.get('character_count'),
                    plate_type.get('description'),
                    plate_type.get('category'),
                    plate_type.get('background_color'),
                    plate_type.get('text_color'),
                    plate_type.get('has_stickers', False),
                    plate_type.get('sticker_description'),
                    # Processing metadata
                    plate_type.get('code_number'),
                    proc_meta.get('currently_processed', False),
                    proc_meta.get('requires_prefix', False),
                    proc_meta.get('requires_suffix', False),
                    proc_meta.get('character_modifications'),
                    proc_meta.get('verify_state_abbreviation', False),
                    proc_meta.get('visual_identifier'),
                    proc_meta.get('vehicle_type_identification'),
                    proc_meta.get('all_numeric_plate', False),
                    str(proc_meta.get('date_ranges', {})) if proc_meta.get('date_ranges') else None,
                    proc_meta.get('plate_images_available'),
                    # CRITICAL DOT processing fields
                    proc_meta.get('dot_processing_type', 'unknown'),
                    proc_meta.get('dot_dropdown_identifier'),
                    str(proc_meta.get('dot_conditional_rules', {})) if proc_meta.get('dot_conditional_rules') else None
                ))
            
            conn.commit()
            
        except Exception as e:
            conn.rollback()
            print(f"Error inserting state data for {state_data.get('name', 'Unknown')}: {e}")
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None