#!/usr/bin/env python3
"""
License Plate Information System
Main application entry point for toll reading assistance
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Add the src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

from gui.main_window import MainWindow
from database.db_manager import DatabaseManager

def main():
    """Initialize and run the application"""
    try:
        # Initialize database
        db_manager = DatabaseManager()
        db_manager.initialize_database()
        
        # Create and run GUI
        root = tk.Tk()
        app = MainWindow(root, db_manager)
        
        # Center window on screen
        root.geometry("1200x800")
        root.eval('tk::PlaceWindow . center')
        
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("Startup Error", f"Failed to start application:\n{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()