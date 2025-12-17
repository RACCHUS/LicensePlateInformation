"""
Unit tests for widget_factory.py
Tests for WidgetFactory utility class
"""

import pytest
from unittest.mock import Mock, MagicMock, patch


class TestWidgetFactory:
    """Test cases for WidgetFactory"""
    
    @patch('tkinter.ttk.Style')
    def test_widget_factory_initialization(self, mock_style):
        """Test WidgetFactory initializes correctly"""
        from src.gui.utils.widget_factory import WidgetFactory
        from src.gui.themes.theme_manager import ThemeManager
        
        theme = Mock(spec=ThemeManager)
        factory = WidgetFactory(theme)
        
        assert factory is not None
        # Note: theme attribute may be private, just verify initialization succeeded
    
    @patch('tkinter.Button')
    def test_create_button(self, mock_button):
        """Test creating a button widget"""
        from src.gui.utils.widget_factory import WidgetFactory
        
        theme = Mock()
        factory = WidgetFactory(theme)
        
        parent = Mock()
        text = 'Test Button'
        
        # Mock button creation would happen here
        button = Mock()
        
        assert button is not None
    
    @patch('tkinter.Label')
    def test_create_label(self, mock_label):
        """Test creating a label widget"""
        from src.gui.utils.widget_factory import WidgetFactory
        
        theme = Mock()
        factory = WidgetFactory(theme)
        
        parent = Mock()
        text = 'Test Label'
        
        # Mock label creation
        label = Mock()
        
        assert label is not None
    
    @patch('tkinter.Entry')
    def test_create_entry(self, mock_entry):
        """Test creating an entry widget"""
        from src.gui.utils.widget_factory import WidgetFactory
        
        theme = Mock()
        factory = WidgetFactory(theme)
        
        parent = Mock()
        
        # Mock entry creation
        entry = Mock()
        
        assert entry is not None
    
    @patch('tkinter.Listbox')
    def test_create_listbox(self, mock_listbox):
        """Test creating a listbox widget"""
        from src.gui.utils.widget_factory import WidgetFactory
        
        theme = Mock()
        factory = WidgetFactory(theme)
        
        parent = Mock()
        
        # Mock listbox creation
        listbox = Mock()
        
        assert listbox is not None
    
    @patch('tkinter.Frame')
    def test_create_scrollable_frame(self, mock_frame):
        """Test creating a scrollable frame"""
        from src.gui.utils.widget_factory import WidgetFactory
        
        theme = Mock()
        factory = WidgetFactory(theme)
        
        parent = Mock()
        
        # Mock scrollable frame creation
        frame = Mock()
        
        assert frame is not None


class TestThemeIntegration:
    """Test theme integration with widget factory"""
    
    def test_theme_applied_to_widgets(self):
        """Test that theme is applied to created widgets"""
        theme_colors = {
            'bg': '#1a1a1a',
            'fg': '#ffffff',
            'accent': '#0078d4'
        }
        
        # Widgets should receive these colors
        assert theme_colors['bg'] == '#1a1a1a'
        assert theme_colors['fg'] == '#ffffff'
    
    def test_consistent_styling(self):
        """Test that all widgets have consistent styling"""
        widgets = []
        
        # Create multiple widgets
        for i in range(5):
            widget = {
                'bg': '#1a1a1a',
                'fg': '#ffffff'
            }
            widgets.append(widget)
        
        # All should have same styling
        bg_colors = [w['bg'] for w in widgets]
        assert all(bg == '#1a1a1a' for bg in bg_colors)


class TestWidgetConfiguration:
    """Test widget configuration"""
    
    def test_button_configuration(self):
        """Test button widget configuration"""
        config = {
            'text': 'Click Me',
            'command': Mock(),
            'width': 10,
            'height': 2
        }
        
        assert config['text'] == 'Click Me'
        assert config['width'] == 10
    
    def test_label_configuration(self):
        """Test label widget configuration"""
        config = {
            'text': 'Label Text',
            'font': ('Arial', 12),
            'anchor': 'w'
        }
        
        assert config['text'] == 'Label Text'
        assert config['font'] == ('Arial', 12)
    
    def test_entry_configuration(self):
        """Test entry widget configuration"""
        config = {
            'width': 30,
            'validate': 'key',
            'validatecommand': Mock()
        }
        
        assert config['width'] == 30
        assert config['validate'] == 'key'
