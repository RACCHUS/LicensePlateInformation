"""
Data import script for License Plate Information System
Loads state data from JSON files into the database
"""

import os
import sys
import json

# Add src to path - get the parent directory (app root) then add src
app_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(app_root, 'src')
sys.path.insert(0, src_path)

from database.db_manager import DatabaseManager
from utils.helpers import ensure_data_directories

def load_state_data_from_json():
    """Load all state data from JSON files into database"""
    
    # Get paths
    app_dir = os.path.dirname(os.path.dirname(__file__))
    states_dir = os.path.join(app_dir, 'data', 'states')
    
    print(f"Loading state data from: {states_dir}")
    
    # Ensure directories exist
    ensure_data_directories(app_dir)
    
    # Initialize database
    db_manager = DatabaseManager()
    db_manager.initialize_database()
    
    try:
        # Get all JSON files in states directory
        if not os.path.exists(states_dir):
            print(f"States directory not found: {states_dir}")
            return
        
        json_files = [f for f in os.listdir(states_dir) if f.endswith('.json')]
        
        if not json_files:
            print("No JSON files found in states directory")
            return
        
        print(f"Found {len(json_files)} state files to load")
        
        for filename in json_files:
            filepath = os.path.join(states_dir, filename)
            print(f"Loading {filename}...")
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    state_data = json.load(f)
                
                # Insert state data using the database manager's method
                db_manager._insert_state_data(state_data)
                print(f"  ✓ Loaded {state_data['name']} ({state_data['abbreviation']})")
                
            except Exception as e:
                print(f"  ✗ Error loading {filename}: {e}")
        
        # Show summary
        total_states = db_manager.get_state_count()
        print(f"\nDatabase now contains {total_states} states")
        
        # Test search functionality
        print("\nTesting search functionality:")
        test_searches = ['FL', 'Georgia', 'AL', 'Carolina']
        
        for search_term in test_searches:
            results = db_manager.search_states(search_term)
            print(f"  '{search_term}' -> {len(results)} results")
            for result in results[:2]:  # Show first 2 results
                print(f"    - {result['name']} ({result['abbreviation']})")
        
    finally:
        db_manager.close()
    
    print("\nData loading complete!")

if __name__ == "__main__":
    load_state_data_from_json()