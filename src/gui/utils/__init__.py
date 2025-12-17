"""
GUI Utilities - Search engine for license plate data.

Note: Most utilities have been moved to src/ui/ for the PySide6 migration.
Only JSONSearchEngine remains here as it's reused by the new UI.
"""

from .json_search_engine import JSONSearchEngine

__all__ = ['JSONSearchEngine']
