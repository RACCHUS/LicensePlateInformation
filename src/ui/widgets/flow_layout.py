"""
Flow Layout for PySide6.

A layout that arranges widgets like words in a paragraph - wrapping to the next line
when there's not enough horizontal space. This ensures widgets maintain their
preferred size regardless of container width.

Based on Qt's official FlowLayout example.
"""

from PySide6.QtCore import Qt, QRect, QSize, QPoint
from PySide6.QtWidgets import QLayout, QLayoutItem, QSizePolicy, QWidget


class FlowLayout(QLayout):
    """
    A layout that flows widgets left-to-right, wrapping to new rows as needed.
    
    Unlike QGridLayout, this layout:
    - Never stretches widgets beyond their preferred size
    - Automatically wraps to new rows based on available width
    - Maintains consistent spacing between items
    """
    
    def __init__(self, parent=None, margin: int = 0, hSpacing: int = -1, vSpacing: int = -1):
        super().__init__(parent)
        
        self._items: list[QLayoutItem] = []
        self._hSpacing = hSpacing
        self._vSpacing = vSpacing
        
        if margin >= 0:
            self.setContentsMargins(margin, margin, margin, margin)
    
    def addItem(self, item: QLayoutItem):
        """Add an item to the layout."""
        self._items.append(item)
    
    def addWidget(self, widget: QWidget):
        """Add a widget to the layout."""
        super().addWidget(widget)
    
    def horizontalSpacing(self) -> int:
        """Return the horizontal spacing between items."""
        if self._hSpacing >= 0:
            return self._hSpacing
        return self._smartSpacing(QSizePolicy.ControlType.PushButton)
    
    def verticalSpacing(self) -> int:
        """Return the vertical spacing between items."""
        if self._vSpacing >= 0:
            return self._vSpacing
        return self._smartSpacing(QSizePolicy.ControlType.PushButton)
    
    def count(self) -> int:
        """Return the number of items in the layout."""
        return len(self._items)
    
    def itemAt(self, index: int) -> QLayoutItem | None:
        """Return the item at the given index."""
        if 0 <= index < len(self._items):
            return self._items[index]
        return None
    
    def takeAt(self, index: int) -> QLayoutItem:  # type: ignore[override]
        """Remove and return the item at the given index."""
        if 0 <= index < len(self._items):
            return self._items.pop(index)
        return None  # type: ignore[return-value]
    
    def expandingDirections(self) -> Qt.Orientation:
        """Return which directions the layout can expand."""
        return Qt.Orientation(0)  # Don't expand
    
    def hasHeightForWidth(self) -> bool:
        """Return True - height depends on width for flow layout."""
        return True
    
    def heightForWidth(self, width: int) -> int:
        """Calculate the height needed for the given width."""
        return self._doLayout(QRect(0, 0, width, 0), testOnly=True)
    
    def setGeometry(self, rect: QRect):
        """Set the geometry of the layout."""
        super().setGeometry(rect)
        self._doLayout(rect, testOnly=False)
    
    def sizeHint(self) -> QSize:
        """Return the preferred size of the layout."""
        return self.minimumSize()
    
    def minimumSize(self) -> QSize:
        """Return the minimum size of the layout."""
        size = QSize()
        for item in self._items:
            size = size.expandedTo(item.minimumSize())
        
        margins = self.contentsMargins()
        size += QSize(margins.left() + margins.right(), margins.top() + margins.bottom())
        return size
    
    def _doLayout(self, rect: QRect, testOnly: bool) -> int:
        """
        Perform the actual layout.
        
        Args:
            rect: The rectangle to lay out within
            testOnly: If True, just calculate height without moving widgets
            
        Returns:
            The height of the layout
        """
        margins = self.contentsMargins()
        effectiveRect = rect.adjusted(margins.left(), margins.top(), -margins.right(), -margins.bottom())
        
        x = effectiveRect.x()
        y = effectiveRect.y()
        lineHeight = 0
        
        hSpace = self.horizontalSpacing()
        vSpace = self.verticalSpacing()
        
        for item in self._items:
            widget = item.widget()
            if widget is None:
                continue
                
            # Get the widget's preferred size
            itemSize = item.sizeHint()
            
            # Check if we need to wrap to next line
            nextX = x + itemSize.width()
            if nextX > effectiveRect.right() and lineHeight > 0:
                x = effectiveRect.x()
                y = y + lineHeight + vSpace
                nextX = x + itemSize.width()
                lineHeight = 0
            
            if not testOnly:
                item.setGeometry(QRect(QPoint(x, y), itemSize))
            
            x = nextX + hSpace
            lineHeight = max(lineHeight, itemSize.height())
        
        return y + lineHeight - rect.y() + margins.bottom()
    
    def _smartSpacing(self, controlType: QSizePolicy.ControlType) -> int:
        """Calculate smart spacing based on parent widget style."""
        parent = self.parent()
        if parent is None:
            return -1
        elif isinstance(parent, QWidget):
            from PySide6.QtWidgets import QStyle
            return parent.style().pixelMetric(
                QStyle.PixelMetric.PM_LayoutHorizontalSpacing, None, parent
            )
        elif isinstance(parent, QLayout):
            return parent.spacing()
        return -1
