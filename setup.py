#!/usr/bin/env python3
"""
Setup script for License Plate Information System
Run this once to prepare the application for first use
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is adequate"""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✓ Python version OK: {sys.version.split()[0]}")
    return True

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Required packages installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing packages: {e}")
        return False

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    try:
        import tkinter
        print("✓ Tkinter available")
        
        try:
            import PIL
            print("✓ Pillow (PIL) available")
        except ImportError:
            print("! Pillow not available - images won't display")
            
        import sqlite3
        print("✓ SQLite3 available")
        
        return True
    except ImportError as e:
        print(f"Error: Missing required module: {e}")
        return False

def setup_directories():
    """Create required directories"""
    print("Setting up directories...")
    
    # Get current directory
    app_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Add src to path for imports
    sys.path.insert(0, os.path.join(app_dir, 'src'))
    
    try:
        from utils.helpers import ensure_data_directories
        ensure_data_directories(app_dir)
        print("✓ Data directories created")
        return True
    except Exception as e:
        print(f"Error creating directories: {e}")
        return False

def initialize_database():
    """Initialize the database with sample data"""
    print("Initializing database...")
    
    try:
        # Add src to path
        app_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, os.path.join(app_dir, 'src'))
        
        from database.db_manager import DatabaseManager
        
        db_manager = DatabaseManager()
        db_manager.initialize_database()
        
        state_count = db_manager.get_state_count()
        print(f"✓ Database initialized with {state_count} states")
        
        db_manager.close()
        return True
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False

def test_application():
    """Test that the application can start"""
    print("Testing application startup...")
    
    try:
        # Add src to path
        app_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, os.path.join(app_dir, 'src'))
        
        from database.db_manager import DatabaseManager
        from gui.main_window import MainWindow
        
        # Test database connection
        db_manager = DatabaseManager()
        states = db_manager.search_states('FL')
        if len(states) > 0:
            print(f"✓ Database test passed - found {states[0]['name']}")
        else:
            print("! Warning: No states found in database")
        
        db_manager.close()
        
        print("✓ Application components loaded successfully")
        return True
        
    except Exception as e:
        print(f"Error testing application: {e}")
        return False

def main():
    """Run setup process"""
    print("License Plate Information System - Setup")
    print("=" * 50)
    
    # Check requirements
    if not check_python_version():
        input("Press Enter to exit...")
        return
    
    if not test_imports():
        print("\nTrying to install missing packages...")
        if not install_requirements():
            input("Press Enter to exit...")
            return
        
        # Test imports again
        if not test_imports():
            input("Press Enter to exit...")
            return
    
    # Setup application
    if not setup_directories():
        input("Press Enter to exit...")
        return
    
    if not initialize_database():
        input("Press Enter to exit...")
        return
    
    if not test_application():
        input("Press Enter to exit...")
        return
    
    print("\n" + "=" * 50)
    print("✓ Setup completed successfully!")
    print("\nYou can now run the application by:")
    print("1. Double-clicking 'run_app.bat' (Windows)")
    print("2. Running 'python main.py' from command line")
    print("3. Double-clicking 'main.py' if Python is associated")
    print("\nFor quick reference, see USER_GUIDE.md")
    
    # Ask if user wants to start the app now
    try:
        start_now = input("\nStart the application now? (y/n): ").lower().strip()
        if start_now in ['y', 'yes']:
            print("\nStarting application...")
            os.system("python main.py")
    except KeyboardInterrupt:
        print("\nSetup complete.")

if __name__ == "__main__":
    main()