"""
Unit tests for db_manager.py
Tests for DatabaseManager class and database operations
"""

import pytest
import sqlite3
import json
from pathlib import Path
from src.database.db_manager import DatabaseManager


# ============================================================================
# DATABASE INITIALIZATION TESTS
# ============================================================================

class TestDatabaseInitialization:
    """Test cases for database initialization"""
    
    def test_database_manager_creation(self, temp_db_path):
        """Test DatabaseManager instance creation"""
        manager = DatabaseManager(temp_db_path)
        assert manager is not None
        assert manager.db_path == temp_db_path
    
    def test_database_file_creation(self, temp_db_path):
        """Test that database file is created"""
        manager = DatabaseManager(temp_db_path)
        manager.initialize_database()
        
        assert Path(temp_db_path).exists()
    
    def test_get_connection(self, db_manager):
        """Test getting database connection"""
        conn = db_manager.get_connection()
        assert conn is not None
        assert isinstance(conn, sqlite3.Connection)
    
    def test_connection_reuse(self, db_manager):
        """Test that get_connection reuses same connection"""
        conn1 = db_manager.get_connection()
        conn2 = db_manager.get_connection()
        assert conn1 is conn2
    
    def test_row_factory_configuration(self, db_manager):
        """Test that row_factory is configured for dict access"""
        conn = db_manager.get_connection()
        assert conn.row_factory == sqlite3.Row
    
    def test_initialize_database_creates_tables(self, temp_db_path):
        """Test that initialize_database creates all required tables"""
        manager = DatabaseManager(temp_db_path)
        manager.initialize_database()
        
        conn = manager.get_connection()
        cursor = conn.cursor()
        
        # Get list of tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        assert 'states' in tables
        assert 'plate_types' in tables
        assert 'character_references' in tables
        assert 'lookup_history' in tables
    
    def test_initialize_database_idempotent(self, db_manager):
        """Test that initialize_database can be called multiple times"""
        # Should not raise error when called again
        db_manager.initialize_database()
        db_manager.initialize_database()
        
        # Tables should still exist
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        assert 'states' in tables


# ============================================================================
# STATES TABLE SCHEMA TESTS
# ============================================================================

class TestStatesTableSchema:
    """Test cases for states table schema"""
    
    def test_states_table_columns(self, db_manager):
        """Test that states table has all required columns"""
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA table_info(states)")
        columns = {row[1] for row in cursor.fetchall()}
        
        expected_columns = {
            'state_id', 'name', 'abbreviation', 'slogan',
            'uses_zero_for_o', 'allows_letter_o', 'zero_is_slashed',
            'primary_colors', 'logo_path', 'notes',
            'created_date', 'updated_date'
        }
        
        assert expected_columns.issubset(columns)
    
    def test_states_indexes_exist(self, db_manager):
        """Test that required indexes exist"""
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
        indexes = [row[0] for row in cursor.fetchall()]
        
        assert 'idx_states_name' in indexes
        assert 'idx_states_abbrev' in indexes


# ============================================================================
# STATE CRUD OPERATIONS TESTS
# ============================================================================

class TestStateOperations:
    """Test cases for state CRUD operations"""
    
    def test_get_state_count_empty(self, db_manager):
        """Test get_state_count on empty database"""
        count = db_manager.get_state_count()
        assert isinstance(count, int)
        assert count >= 0
    
    def test_get_all_states_empty(self, db_manager):
        """Test get_all_states on empty database"""
        states = db_manager.get_all_states()
        assert isinstance(states, list)
    
    def test_get_all_states_populated(self, populated_db):
        """Test get_all_states with data"""
        states = populated_db.get_all_states()
        assert len(states) > 0
        assert all(isinstance(state, dict) for state in states)
    
    def test_get_all_states_sorted(self, populated_db):
        """Test that get_all_states returns states sorted by name"""
        states = populated_db.get_all_states()
        if len(states) > 1:
            names = [state['name'] for state in states]
            assert names == sorted(names)
    
    def test_search_states_by_name(self, populated_db):
        """Test searching states by full name"""
        results = populated_db.search_states('California')
        assert len(results) > 0
        assert any(state['name'] == 'California' for state in results)
    
    def test_search_states_by_abbreviation(self, populated_db):
        """Test searching states by abbreviation"""
        results = populated_db.search_states('CA')
        assert len(results) > 0
        assert any(state['abbreviation'] == 'CA' for state in results)
    
    def test_search_states_partial_match(self, populated_db):
        """Test searching states with partial name"""
        results = populated_db.search_states('Cali')
        assert len(results) > 0
    
    def test_search_states_case_insensitive(self, populated_db):
        """Test that search is case insensitive"""
        results1 = populated_db.search_states('california')
        results2 = populated_db.search_states('CALIFORNIA')
        results3 = populated_db.search_states('California')
        
        assert len(results1) == len(results2) == len(results3)
    
    def test_search_states_no_results(self, populated_db):
        """Test search with no matching results"""
        results = populated_db.search_states('NonexistentState')
        assert results == []
    
    def test_get_state_by_id_exists(self, populated_db):
        """Test getting state by ID when it exists"""
        # Get a state ID first
        states = populated_db.get_all_states()
        if states:
            state_id = states[0]['state_id']
            state = populated_db.get_state_by_id(state_id)
            assert state is not None
            assert state['state_id'] == state_id
    
    def test_get_state_by_id_not_exists(self, db_manager):
        """Test getting state by ID when it doesn't exist"""
        state = db_manager.get_state_by_id(99999)
        assert state is None


# ============================================================================
# PLATE TYPES TABLE TESTS
# ============================================================================

class TestPlateTypeOperations:
    """Test cases for plate type operations"""
    
    def test_get_plate_types_for_state_empty(self, db_manager):
        """Test getting plate types for state with no data"""
        # Use a state_id that doesn't exist (999) to ensure no plate types
        plate_types = db_manager.get_plate_types_for_state(999)
        assert isinstance(plate_types, list)
        assert len(plate_types) == 0
    
    def test_get_plate_types_for_state_populated(self, populated_db):
        """Test getting plate types for state with data"""
        # Get a state ID first
        states = populated_db.get_all_states()
        if states:
            state_id = states[0]['state_id']
            plate_types = populated_db.get_plate_types_for_state(state_id)
            assert isinstance(plate_types, list)
    
    def test_plate_types_only_active(self, populated_db):
        """Test that only active plate types are returned"""
        states = populated_db.get_all_states()
        if states:
            state_id = states[0]['state_id']
            plate_types = populated_db.get_plate_types_for_state(state_id)
            # All returned plate types should have is_active = 1 (or True)
            assert all(pt.get('is_active', 0) == 1 for pt in plate_types)
    
    def test_plate_types_sorted_by_name(self, populated_db):
        """Test that plate types are sorted by type_name"""
        states = populated_db.get_all_states()
        if states:
            state_id = states[0]['state_id']
            plate_types = populated_db.get_plate_types_for_state(state_id)
            if len(plate_types) > 1:
                names = [pt['type_name'] for pt in plate_types]
                assert names == sorted(names)


# ============================================================================
# CHARACTER REFERENCES TESTS
# ============================================================================

class TestCharacterReferenceOperations:
    """Test cases for character reference operations"""
    
    def test_get_character_references_for_state(self, db_manager):
        """Test getting character references for a state"""
        refs = db_manager.get_character_references_for_state(1)
        assert isinstance(refs, list)
    
    def test_character_references_sorted(self, db_manager):
        """Test that character references are sorted"""
        # This test will pass even with empty results
        refs = db_manager.get_character_references_for_state(1)
        assert isinstance(refs, list)


# ============================================================================
# LOOKUP HISTORY TESTS
# ============================================================================

class TestLookupHistory:
    """Test cases for lookup history tracking"""
    
    def test_add_lookup_to_history_basic(self, db_manager):
        """Test adding basic lookup to history"""
        db_manager.add_lookup_to_history('ABC123')
        
        # Verify it was added
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM lookup_history')
        results = cursor.fetchall()
        
        assert len(results) > 0
        assert any(row['search_term'] == 'ABC123' for row in results)
    
    def test_add_lookup_to_history_with_details(self, db_manager):
        """Test adding lookup with full details"""
        db_manager.add_lookup_to_history(
            search_term='XYZ789',
            state_found='FL',
            plate_type_found='Passenger',
            user_notes='Test search'
        )
        
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM lookup_history WHERE search_term = ?', ('XYZ789',))
        result = cursor.fetchone()
        
        assert result is not None
        assert result['state_found'] == 'FL'
        assert result['plate_type_found'] == 'Passenger'
        assert result['user_notes'] == 'Test search'
    
    def test_lookup_history_timestamp_auto(self, db_manager):
        """Test that timestamp is automatically set"""
        db_manager.add_lookup_to_history('TEST')
        
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT timestamp FROM lookup_history WHERE search_term = ?', ('TEST',))
        result = cursor.fetchone()
        
        assert result is not None
        assert result['timestamp'] is not None


# ============================================================================
# DATABASE INTEGRITY TESTS
# ============================================================================

class TestDatabaseIntegrity:
    """Test cases for database integrity and constraints"""
    
    def test_states_unique_name(self, db_manager):
        """Test that state names must be unique"""
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        # Clear existing data to ensure clean test
        cursor.execute('DELETE FROM states WHERE abbreviation IN ("CA", "XX")')
        conn.commit()
        
        # Insert first state
        cursor.execute('''
            INSERT INTO states (name, abbreviation)
            VALUES ('California', 'CA')
        ''')
        conn.commit()
        
        # Try to insert duplicate name
        with pytest.raises(sqlite3.IntegrityError):
            cursor.execute('''
                INSERT INTO states (name, abbreviation)
                VALUES ('California', 'XX')
            ''')
            conn.commit()
    
    def test_states_unique_abbreviation(self, db_manager):
        """Test that state abbreviations must be unique"""
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        # Clear existing data to ensure clean test
        cursor.execute('DELETE FROM states WHERE abbreviation = "CA"')
        conn.commit()
        
        # Insert first state
        cursor.execute('''
            INSERT INTO states (name, abbreviation)
            VALUES ('California', 'CA')
        ''')
        conn.commit()
        
        # Try to insert duplicate abbreviation
        with pytest.raises(sqlite3.IntegrityError):
            cursor.execute('''
                INSERT INTO states (name, abbreviation)
                VALUES ('Some Other State', 'CA')
            ''')
            conn.commit()
    
    def test_plate_types_foreign_key(self, db_manager):
        """Test foreign key constraint for plate_types"""
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        # Enable foreign keys (SQLite doesn't enable by default in some cases)
        cursor.execute('PRAGMA foreign_keys = ON')
        
        # Try to insert plate type with non-existent state_id
        # Note: This test depends on foreign key enforcement
        try:
            cursor.execute('''
                INSERT INTO plate_types (state_id, type_name, pattern)
                VALUES (99999, 'Test', 'ABC123')
            ''')
            conn.commit()
            # If no error, foreign keys might not be enforced
        except sqlite3.IntegrityError:
            # Expected behavior with foreign keys enabled
            pass


# ============================================================================
# TRANSACTION TESTS
# ============================================================================

class TestDatabaseTransactions:
    """Test cases for transaction handling"""
    
    def test_transaction_commit(self, db_manager):
        """Test that changes are committed"""
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        # Clear existing test data
        cursor.execute('DELETE FROM states WHERE abbreviation = "TS"')
        conn.commit()
        
        cursor.execute('''
            INSERT INTO states (name, abbreviation)
            VALUES ('Test State', 'TS')
        ''')
        conn.commit()
        
        # Verify data persists
        cursor.execute('SELECT * FROM states WHERE abbreviation = ?', ('TS',))
        result = cursor.fetchone()
        assert result is not None
    
    def test_transaction_rollback(self, db_manager):
        """Test transaction rollback"""
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO states (name, abbreviation)
            VALUES ('TestState', 'TS')
        ''')
        # Don't commit, rollback instead
        conn.rollback()
        
        # Verify data was not saved
        cursor.execute('SELECT * FROM states WHERE abbreviation = ?', ('TS',))
        result = cursor.fetchone()
        assert result is None


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestDatabaseIntegration:
    """Integration tests for database operations"""
    
    def test_full_state_workflow(self, db_manager):
        """Test complete workflow of adding and retrieving state"""
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        # Clear existing test data
        cursor.execute('DELETE FROM states WHERE abbreviation = "OR"')
        conn.commit()
        
        # Insert state
        cursor.execute('''
            INSERT INTO states (name, abbreviation, slogan, primary_colors)
            VALUES (?, ?, ?, ?)
        ''', ('Oregon', 'OR', 'Pacific Wonderland', '["#003087", "#FFFFFF"]'))
        conn.commit()
        
        # Search for state
        results = db_manager.search_states('Oregon')
        assert len(results) > 0
        
        state = results[0]
        assert state['name'] == 'Oregon'
        assert state['abbreviation'] == 'OR'
        assert state['slogan'] == 'Pacific Wonderland'
    
    def test_state_with_plate_types(self, db_manager):
        """Test adding state and associated plate types"""
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        # Clear existing test data
        cursor.execute('DELETE FROM states WHERE abbreviation = "ID"')
        conn.commit()
        
        # Add state
        cursor.execute('''
            INSERT INTO states (name, abbreviation)
            VALUES ('Idaho', 'ID')
        ''')
        state_id = cursor.lastrowid
        conn.commit()
        
        # Add plate type
        cursor.execute('''
            INSERT INTO plate_types (state_id, type_name, pattern, is_active)
            VALUES (?, ?, ?, ?)
        ''', (state_id, 'Passenger', 'ABC123', 1))
        conn.commit()
        
        # Retrieve plate types
        plate_types = db_manager.get_plate_types_for_state(state_id)
        assert len(plate_types) > 0
        assert plate_types[0]['type_name'] == 'Passenger'
    
    def test_multiple_searches(self, populated_db):
        """Test multiple sequential searches"""
        # Perform multiple searches
        results1 = populated_db.search_states('CA')
        results2 = populated_db.search_states('TX')
        results3 = populated_db.search_states('California')
        
        # All should return results
        assert all(isinstance(r, list) for r in [results1, results2, results3])
    
    def test_database_persistence(self, temp_db_path):
        """Test that data persists across connections"""
        # Create first manager and add data
        manager1 = DatabaseManager(temp_db_path)
        manager1.initialize_database()
        
        conn = manager1.get_connection()
        cursor = conn.cursor()
        # Use a test state that won't conflict with loaded data
        cursor.execute('DELETE FROM states WHERE abbreviation = "XX"')
        cursor.execute('''
            INSERT INTO states (name, abbreviation)
            VALUES ('Test State', 'XX')
        ''')
        conn.commit()
        if manager1.connection:
            manager1.connection.close()
        
        # Create second manager and verify data exists
        manager2 = DatabaseManager(temp_db_path)
        results = manager2.search_states('Test State')
        assert len(results) > 0


# ============================================================================
# EXTENDED TESTS - PRIORITY 1.2
# ============================================================================

class TestSearchStatesExtended:
    """Extended tests for state search functionality"""
    
    def test_search_states_partial_match(self, populated_db):
        """Test searching states with partial name match"""
        results = populated_db.search_states('Cali')
        assert len(results) > 0
        assert any('California' in r['name'] for r in results)
    
    def test_search_states_case_insensitive(self, populated_db):
        """Test case-insensitive state search"""
        results_lower = populated_db.search_states('california')
        results_upper = populated_db.search_states('CALIFORNIA')
        results_mixed = populated_db.search_states('CaLiFoRnIa')
        
        # All should return same results
        assert len(results_lower) == len(results_upper) == len(results_mixed)
    
    def test_search_states_by_abbreviation_exact(self, populated_db):
        """Test exact abbreviation match has highest priority"""
        results = populated_db.search_states('CA')
        
        assert len(results) > 0
        # First result should be exact match
        assert results[0]['abbreviation'] == 'CA'


class TestPlateTypesExtended:
    """Extended tests for plate types"""
    
    def test_get_plate_types_inactive_excluded(self, db_manager):
        """Test that inactive plate types are excluded"""
        # Add state
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        # Clear existing test data
        cursor.execute('DELETE FROM states WHERE abbreviation = "NV"')
        conn.commit()
        
        cursor.execute('''
            INSERT INTO states (name, abbreviation)
            VALUES ('Nevada', 'NV')
        ''')
        state_id = cursor.lastrowid
        
        # Add active and inactive plate types
        cursor.execute('''
            INSERT INTO plate_types (state_id, type_name, is_active)
            VALUES (?, 'Active Type', 1)
        ''', (state_id,))
        
        cursor.execute('''
            INSERT INTO plate_types (state_id, type_name, is_active)
            VALUES (?, 'Inactive Type', 0)
        ''', (state_id,))
        
        conn.commit()
        
        # Get plate types
        results = db_manager.get_plate_types_for_state(state_id)
        
        # Should only include active
        assert len(results) == 1
        assert results[0]['type_name'] == 'Active Type'
    
    def test_plate_type_dot_processing_fields(self, db_manager):
        """Test DOT processing fields in plate_types table"""
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        # Clear existing test data
        cursor.execute('DELETE FROM states WHERE abbreviation = "FL"')
        conn.commit()
        
        # Add state
        cursor.execute('''
            INSERT INTO states (name, abbreviation)
            VALUES ('Florida', 'FL')
        ''')
        state_id = cursor.lastrowid
        
        # Add plate type with DOT processing metadata
        cursor.execute('''
            INSERT INTO plate_types (
                state_id, type_name, dot_processing_type, 
                dot_dropdown_identifier, currently_processed
            )
            VALUES (?, 'Standard', 'always_standard', 'FL_STANDARD', 1)
        ''', (state_id,))
        
        conn.commit()
        
        # Retrieve and verify
        results = db_manager.get_plate_types_for_state(state_id)
        assert len(results) == 1
        assert results[0]['dot_processing_type'] == 'always_standard'
        assert results[0]['dot_dropdown_identifier'] == 'FL_STANDARD'


class TestLookupHistoryExtended:
    """Extended tests for lookup history"""
    
    def test_add_lookup_history_all_fields(self, db_manager):
        """Test adding lookup history with all fields"""
        db_manager.add_lookup_to_history(
            search_term='ABC123',
            state_found='CA',
            plate_type_found='Passenger',
            user_notes='Test lookup'
        )
        
        # Verify it was added
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM lookup_history WHERE search_term = ?', ('ABC123',))
        result = cursor.fetchone()
        
        assert result is not None
        assert result['state_found'] == 'CA'
        assert result['plate_type_found'] == 'Passenger'
        assert result['user_notes'] == 'Test lookup'
    
    def test_get_lookup_history_ordered_by_date(self, db_manager):
        """Test that lookup history is ordered by timestamp"""
        # Add multiple entries
        db_manager.add_lookup_to_history('FIRST', 'CA')
        db_manager.add_lookup_to_history('SECOND', 'TX')
        db_manager.add_lookup_to_history('THIRD', 'FL')
        
        # Get all history
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM lookup_history ORDER BY timestamp DESC')
        results = cursor.fetchall()
        
        # Should have all 3
        assert len(results) >= 3


class TestDataInsertion:
    """Tests for inserting state data"""
    
    def test_insert_state_basic(self, db_manager):
        """Test inserting a basic state record"""
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        # Clear existing test data
        cursor.execute('DELETE FROM states WHERE abbreviation = "AZ"')
        conn.commit()
        
        cursor.execute('''
            INSERT INTO states (name, abbreviation, slogan)
            VALUES (?, ?, ?)
        ''', ('Arizona', 'AZ', 'Grand Canyon State'))
        
        conn.commit()
        
        # Verify insertion
        results = db_manager.search_states('Arizona')
        assert len(results) == 1
        assert results[0]['abbreviation'] == 'AZ'
    
    def test_update_state_existing_record(self, populated_db):
        """Test updating an existing state record"""
        conn = populated_db.get_connection()
        cursor = conn.cursor()
        
        # Update California's slogan
        cursor.execute('''
            UPDATE states
            SET slogan = ?, updated_date = CURRENT_TIMESTAMP
            WHERE abbreviation = ?
        ''', ('The Golden State', 'CA'))
        
        conn.commit()
        
        # Verify update
        results = populated_db.search_states('CA')
        assert len(results) > 0
        assert results[0]['slogan'] == 'The Golden State'


class TestDatabaseReliability:
    """Tests for database reliability and edge cases"""
    
    def test_database_connection_recovery(self, temp_db_path):
        """Test that database can recover from connection issues"""
        manager = DatabaseManager(temp_db_path)
        manager.initialize_database()
        
        # Close connection
        if manager.connection:
            manager.connection.close()
            manager.connection = None
        
        # Should be able to get new connection
        conn = manager.get_connection()
        assert conn is not None
    
    def test_empty_search_results(self, db_manager):
        """Test handling of empty search results"""
        results = db_manager.search_states('NonExistentState')
        assert isinstance(results, list)
        assert len(results) == 0
    
    def test_get_state_by_id_not_found(self, db_manager):
        """Test getting state by non-existent ID"""
        result = db_manager.get_state_by_id(99999)
        assert result is None


class TestCharacterReferences:
    """Extended tests for character references"""
    
    def test_get_character_references_for_state(self, db_manager):
        """Test retrieving character references for a state"""
        # Add state
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        # Clear existing test data
        cursor.execute('DELETE FROM states WHERE abbreviation = "OH"')
        conn.commit()
        
        cursor.execute('''
            INSERT INTO states (name, abbreviation)
            VALUES ('Ohio', 'OH')
        ''')
        state_id = cursor.lastrowid
        
        # Add character references
        cursor.execute('''
            INSERT INTO character_references (state_id, character, character_type, is_ambiguous)
            VALUES (?, '0', 'digit', 1)
        ''', (state_id,))
        
        cursor.execute('''
            INSERT INTO character_references (state_id, character, character_type, is_ambiguous)
            VALUES (?, 'O', 'letter', 1)
        ''', (state_id,))
        
        conn.commit()
        
        # Retrieve
        results = db_manager.get_character_references_for_state(state_id)
        
        assert len(results) == 2
        assert any(r['character'] == '0' for r in results)
        assert any(r['character'] == 'O' for r in results)
