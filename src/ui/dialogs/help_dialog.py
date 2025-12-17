"""
Help Dialog for License Plate Information System.

Displays help content with tree navigation and markdown rendering.
"""

from pathlib import Path
from typing import Optional, Any

# Try to import markdown, set to None if not available
markdown: Any = None
try:
    import markdown as md_module
    markdown = md_module
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QSplitter,
    QTreeWidget,
    QTreeWidgetItem,
    QTextBrowser,
    QPushButton,
    QLineEdit,
    QLabel,
)


class HelpDialog(QDialog):
    """Help dialog with tree navigation and content browser."""
    
    HELP_STRUCTURE = {
        "Getting Started": {
            "file": "user_guide.md",
            "children": {}
        },
        "Keyboard Shortcuts": {
            "file": "shortcuts.md",
            "children": {}
        },
        "Button Reference": {
            "file": "button_reference.md",
            "children": {
                "Accept": {"anchor": "accept"},
                "P - Plate Unreadable": {"anchor": "p_unreadable"},
                "O - Plate Obscured": {"anchor": "o_obscured"},
                "N - No Plate Visible": {"anchor": "n_no_plate"},
                "T - Technical Issue": {"anchor": "t_technical"},
                "E - Emergency Vehicle": {"anchor": "e_emergency"},
                "X - Other": {"anchor": "x_other"},
                "R - Mark for Review": {"anchor": "r_review"},
            }
        },
        "Plate Reading Tips": {
            "file": "plate_reading_tips.md",
            "children": {
                "Obscured/Partial Plates": {"anchor": "obscuredpartial-plates"},
                "Damaged Characters": {"anchor": "damaged-characters"},
                "Stacked Characters": {"anchor": "stacked-characters"},
                "O vs 0 (Oh vs Zero)": {"anchor": "o-vs-0-oh-vs-zero"},
            }
        },
        "Emergency Vehicle Guide": {
            "file": "emergency_vehicles.md",
            "children": {}
        },
    }
    
    # Mapping from topic names to tree items
    TOPIC_MAPPING = {
        "user_guide": "Getting Started",
        "shortcuts": "Keyboard Shortcuts",
        "button_reference": "Button Reference",
        "plate_reading_tips": "Plate Reading Tips",
        "emergency_vehicles": "Emergency Vehicle Guide",
    }
    
    SECTION_MAPPING = {
        "obscured": "Obscured/Partial Plates",
        "damaged": "Damaged Characters",
        "stacked": "Stacked Characters",
        "o_vs_0": "O vs 0 (Oh vs Zero)",
        "accept": "Accept",
        "p_unreadable": "P - Plate Unreadable",
        "o_obscured": "O - Plate Obscured",
        "n_no_plate": "N - No Plate Visible",
        "t_technical": "T - Technical Issue",
        "e_emergency": "E - Emergency Vehicle",
        "x_other": "X - Other",
        "r_review": "R - Mark for Review",
    }
    
    def __init__(
        self,
        parent=None,
        topic: Optional[str] = None,
        section: Optional[str] = None
    ):
        super().__init__(parent)
        
        self.help_dir = Path(__file__).parent.parent / "resources" / "help"
        self.current_file: Optional[str] = None
        
        self._setup_ui()
        self._populate_tree()
        
        # Navigate to requested topic
        if topic:
            self._navigate_to_topic(topic, section)
        else:
            # Default to user guide
            self._navigate_to_topic("user_guide")
    
    def _setup_ui(self):
        """Set up the dialog UI."""
        self.setWindowTitle("Help - License Plate Information")
        self.setMinimumSize(900, 600)
        self.resize(1000, 700)
        
        layout = QVBoxLayout(self)
        
        # Search bar
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search help content...")
        self.search_input.textChanged.connect(self._on_search)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Main splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left side - Tree navigation
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Topics")
        self.tree.setMinimumWidth(200)
        self.tree.setMaximumWidth(300)
        self.tree.itemClicked.connect(self._on_tree_item_clicked)
        splitter.addWidget(self.tree)
        
        # Right side - Content browser
        self.browser = QTextBrowser()
        self.browser.setOpenExternalLinks(True)
        splitter.addWidget(self.browser)
        
        splitter.setSizes([250, 750])
        layout.addWidget(splitter)
        
        # Close button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)
    
    def _populate_tree(self):
        """Populate the tree widget with help topics."""
        self.tree.clear()
        self.tree_items = {}
        
        for topic_name, topic_data in self.HELP_STRUCTURE.items():
            item = QTreeWidgetItem([topic_name])
            item.setData(0, Qt.ItemDataRole.UserRole, topic_data.get("file"))
            self.tree.addTopLevelItem(item)
            self.tree_items[topic_name] = item
            
            # Add children
            for child_name, child_data in topic_data.get("children", {}).items():
                child_item = QTreeWidgetItem([child_name])
                child_item.setData(0, Qt.ItemDataRole.UserRole, topic_data.get("file"))
                child_item.setData(0, Qt.ItemDataRole.UserRole + 1, child_data.get("anchor"))
                item.addChild(child_item)
                self.tree_items[child_name] = child_item
        
        self.tree.expandAll()
    
    def _navigate_to_topic(self, topic: str, section: Optional[str] = None):
        """Navigate to a specific topic."""
        topic_name = self.TOPIC_MAPPING.get(topic, topic)
        
        if topic_name in self.tree_items:
            item = self.tree_items[topic_name]
            self.tree.setCurrentItem(item)
            self._load_content(item)
            
            # Navigate to section if specified
            if section:
                section_name = self.SECTION_MAPPING.get(section, section)
                if section_name in self.tree_items:
                    section_item = self.tree_items[section_name]
                    self.tree.setCurrentItem(section_item)
                    anchor = section_item.data(0, Qt.ItemDataRole.UserRole + 1)
                    if anchor:
                        self.browser.scrollToAnchor(anchor)
    
    def _on_tree_item_clicked(self, item: QTreeWidgetItem, column: int):
        """Handle tree item click."""
        self._load_content(item)
    
    def _load_content(self, item: QTreeWidgetItem):
        """Load content for the selected tree item."""
        filename = item.data(0, Qt.ItemDataRole.UserRole)
        anchor = item.data(0, Qt.ItemDataRole.UserRole + 1)
        
        if not filename:
            return
        
        # Only reload if different file
        if filename != self.current_file:
            self.current_file = filename
            file_path = self.help_dir / filename
            
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Convert markdown to HTML
                if HAS_MARKDOWN and markdown is not None:
                    html_content = markdown.markdown(
                        content,
                        extensions=['tables', 'fenced_code', 'toc']
                    )
                else:
                    # Fallback: basic conversion
                    html_content = self._basic_markdown_to_html(content)
                
                # Wrap in styled HTML
                styled_html = self._wrap_html(html_content)
                self.browser.setHtml(styled_html)
                
            except FileNotFoundError:
                self.browser.setHtml(f"<p>Help file not found: {filename}</p>")
        
        # Scroll to anchor if specified
        if anchor:
            self.browser.scrollToAnchor(anchor)
    
    def _basic_markdown_to_html(self, content: str) -> str:
        """Basic markdown to HTML conversion (fallback if markdown package not available)."""
        import re
        
        # Headers
        content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
        content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
        content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', content, flags=re.MULTILINE)
        
        # Bold and italic
        content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
        content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', content)
        
        # Code blocks
        content = re.sub(r'`(.+?)`', r'<code>\1</code>', content)
        
        # Lists
        content = re.sub(r'^- (.+)$', r'<li>\1</li>', content, flags=re.MULTILINE)
        
        # Paragraphs (simple)
        paragraphs = content.split('\n\n')
        content = ''.join(
            f'<p>{p}</p>' if not p.startswith('<') else p
            for p in paragraphs
        )
        
        return content
    
    def _wrap_html(self, content: str) -> str:
        """Wrap HTML content with styling."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
        <style>
            body {{
                font-family: "Segoe UI", Arial, sans-serif;
                font-size: 14px;
                line-height: 1.6;
                color: #ffffff;
                background-color: #252525;
                padding: 20px;
            }}
            h1 {{
                color: #4CAF50;
                border-bottom: 2px solid #404040;
                padding-bottom: 10px;
            }}
            h2 {{
                color: #66BB6A;
                margin-top: 24px;
            }}
            h3 {{
                color: #81C784;
                margin-top: 20px;
            }}
            code {{
                background-color: #1e1e1e;
                padding: 2px 6px;
                border-radius: 3px;
                font-family: "Consolas", monospace;
            }}
            pre {{
                background-color: #1e1e1e;
                padding: 12px;
                border-radius: 6px;
                overflow-x: auto;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 16px 0;
            }}
            th, td {{
                border: 1px solid #404040;
                padding: 10px 12px;
                text-align: left;
            }}
            th {{
                background-color: #2d2d2d;
                color: #4CAF50;
            }}
            tr:nth-child(even) {{
                background-color: #2d2d2d;
            }}
            a {{
                color: #4CAF50;
            }}
            ul, ol {{
                padding-left: 24px;
            }}
            li {{
                margin: 6px 0;
            }}
            hr {{
                border: none;
                border-top: 1px solid #404040;
                margin: 24px 0;
            }}
        </style>
        </head>
        <body>
        {content}
        </body>
        </html>
        """
    
    def _on_search(self, text: str):
        """Handle search input."""
        if not text:
            # Show all items
            for i in range(self.tree.topLevelItemCount()):
                item = self.tree.topLevelItem(i)
                if item is None:
                    continue
                item.setHidden(False)
                for j in range(item.childCount()):
                    child = item.child(j)
                    if child is not None:
                        child.setHidden(False)
            return
        
        text = text.lower()
        
        # Search tree items
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            if item is None:
                continue
            item_matches = text in item.text(0).lower()
            
            # Check children
            any_child_matches = False
            for j in range(item.childCount()):
                child = item.child(j)
                if child is None:
                    continue
                child_matches = text in child.text(0).lower()
                child.setHidden(not child_matches and not item_matches)
                if child_matches:
                    any_child_matches = True
            
            item.setHidden(not item_matches and not any_child_matches)
            
            # Expand if children match
            if any_child_matches:
                item.setExpanded(True)
