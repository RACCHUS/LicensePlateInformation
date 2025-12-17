"""
PySide6 UI Package for License Plate Information System.

This package contains the modern Qt-based user interface.
"""

# Defer MainWindow import to avoid circular imports during testing
# from .main_window import MainWindow

__all__ = ["MainWindow"]

def get_main_window():
    """Lazy import of MainWindow to avoid import issues."""
    from .main_window import MainWindow
    return MainWindow
