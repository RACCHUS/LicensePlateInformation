"""
Unit tests for FlowLayout widget.

Tests the custom flow layout that wraps widgets.
"""

import pytest
from unittest.mock import Mock, MagicMock

# Skip all tests if PySide6 is not available
pytest.importorskip("PySide6")

from PySide6.QtWidgets import QApplication, QWidget, QPushButton
from PySide6.QtCore import QRect, QSize, QPoint

from src.ui.widgets.flow_layout import FlowLayout


@pytest.fixture(scope="module")
def qapp():
    """Create a QApplication for widget testing."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


@pytest.fixture
def flow_layout(qapp):
    """Create a FlowLayout instance."""
    layout = FlowLayout(margin=10, hSpacing=5, vSpacing=5)
    return layout


@pytest.fixture
def container_widget(qapp):
    """Create a container widget for layout testing."""
    widget = QWidget()
    widget.setMinimumSize(300, 200)
    return widget


class TestFlowLayoutInit:
    """Test FlowLayout initialization."""
    
    def test_creates_successfully(self, flow_layout):
        """Test layout creates successfully."""
        assert flow_layout is not None
    
    def test_default_margins(self, qapp):
        """Test default margins."""
        layout = FlowLayout()
        assert layout.contentsMargins() is not None
    
    def test_custom_margins(self, qapp):
        """Test custom margin setting."""
        layout = FlowLayout(margin=20)
        margins = layout.contentsMargins()
        assert margins.left() == 20
        assert margins.top() == 20
    
    def test_custom_spacing(self, qapp):
        """Test custom spacing settings."""
        layout = FlowLayout(hSpacing=10, vSpacing=15)
        assert layout.horizontalSpacing() == 10
        assert layout.verticalSpacing() == 15


class TestFlowLayoutItems:
    """Test adding and removing items."""
    
    def test_add_widget(self, qapp):
        """Test adding a widget."""
        layout = FlowLayout()
        btn = QPushButton("Test")
        layout.addWidget(btn)
        
        assert layout.count() == 1
    
    def test_add_multiple_widgets(self, qapp):
        """Test adding multiple widgets."""
        layout = FlowLayout()
        for i in range(5):
            layout.addWidget(QPushButton(f"Button {i}"))
        
        assert layout.count() == 5
    
    def test_item_at(self, qapp):
        """Test itemAt method."""
        layout = FlowLayout()
        btn = QPushButton("Test")
        layout.addWidget(btn)
        
        item = layout.itemAt(0)
        assert item is not None
        assert item.widget() == btn
    
    def test_item_at_invalid_index(self, qapp):
        """Test itemAt with invalid index."""
        layout = FlowLayout()
        item = layout.itemAt(999)
        assert item is None
    
    def test_take_at(self, qapp):
        """Test takeAt method."""
        layout = FlowLayout()
        btn = QPushButton("Test")
        layout.addWidget(btn)
        
        assert layout.count() == 1
        
        item = layout.takeAt(0)
        assert item is not None
        assert layout.count() == 0


class TestFlowLayoutSizing:
    """Test size hint calculations."""
    
    def test_size_hint_empty(self, qapp):
        """Test sizeHint when empty."""
        layout = FlowLayout()
        hint = layout.sizeHint()
        assert hint.isValid()
    
    def test_size_hint_with_widgets(self, qapp):
        """Test sizeHint with widgets."""
        layout = FlowLayout()
        for i in range(3):
            layout.addWidget(QPushButton(f"Btn {i}"))
        
        hint = layout.sizeHint()
        assert hint.width() > 0
        assert hint.height() > 0
    
    def test_minimum_size(self, qapp):
        """Test minimumSize."""
        layout = FlowLayout()
        layout.addWidget(QPushButton("Test Button"))
        
        min_size = layout.minimumSize()
        assert min_size.width() > 0
        assert min_size.height() > 0


class TestFlowLayoutBehavior:
    """Test flow layout wrapping behavior."""
    
    def test_expanding_directions(self, qapp):
        """Test expandingDirections returns none (no expansion)."""
        layout = FlowLayout()
        from PySide6.QtCore import Qt
        directions = layout.expandingDirections()
        # FlowLayout returns Qt.Orientation(0) - no expansion
        assert directions == Qt.Orientation(0)
    
    def test_has_height_for_width(self, qapp):
        """Test hasHeightForWidth returns True."""
        layout = FlowLayout()
        assert layout.hasHeightForWidth() is True
    
    def test_height_for_width(self, qapp):
        """Test heightForWidth calculation."""
        layout = FlowLayout()
        for i in range(10):
            layout.addWidget(QPushButton(f"Button {i}"))
        
        # Narrow width should require more height (more rows)
        height_narrow = layout.heightForWidth(100)
        height_wide = layout.heightForWidth(500)
        
        # Narrow should need more height than wide
        assert height_narrow >= height_wide
