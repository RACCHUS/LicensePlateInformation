"""
GUI module for License Plate Information System.

Note: The Tkinter GUI has been replaced with PySide6 (see src/ui/).
This module only contains the JSONSearchEngine which is reused by the new UI.
"""

from .utils.json_search_engine import JSONSearchEngine

__all__ = ['JSONSearchEngine']
