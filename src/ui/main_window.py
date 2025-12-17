"""
Main Window for License Plate Information System.

This is the main application window with menu bar, toolbar, and splitter-based layout.
"""

import json
import sys
from pathlib import Path
from typing import Optional

from PySide6.QtCore import Qt, Signal, QSettings
from PySide6.QtGui import QAction, QKeySequence, QCloseEvent, QShortcut
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QSplitter,
    QLabel,
    QComboBox,
    QToolBar,
    QStatusBar,
    QMessageBox,
    QApplication,
    QLineEdit,
    QFrame,
    QScrollArea,
    QGroupBox,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QSizePolicy,
    QFileDialog,
)

from ui.controllers.search_controller import SearchController, CategorizedResults
from ui.controllers.mode_controller import ModeController
from ui.controllers.state_data_manager import StateDataManager
from ui.widgets.font_preview import FontPreviewWidget
from ui.widgets.state_button import StateButton
from ui.widgets.image_panel import ImagePanel


class MainWindow(QMainWindow):
    """Main application window."""
    
    # Signals
    mode_changed = Signal(str)
    state_selected = Signal(str)
    plate_type_selected = Signal(str)
    
    def __init__(self):
        super().__init__()
        
        self.settings = QSettings("LicensePlateInfo", "LicensePlateInfo")
        self.modes_config = self._load_modes_config()
        self.current_mode: str = str(self.settings.value("default_mode", "All"))
        self.current_state: Optional[str] = None
        self.is_search_mode = False
        
        # Data path for images and other resources
        # __file__ is src/ui/main_window.py, so go up 2 levels to project root
        self.data_path = Path(__file__).parent.parent.parent / "data"
        
        # Initialize search controller
        self.search_controller = SearchController(self)
        self.search_controller.search_completed.connect(self._on_search_completed)
        self.search_controller.search_cleared.connect(self._on_search_cleared)
        self.search_controller.search_error.connect(self._on_search_error)
        
        # Initialize mode controller
        self.mode_controller = ModeController(self)
        self.mode_controller.mode_changed.connect(self._on_mode_changed_from_controller)
        
        # Initialize state data manager
        self.state_data_manager = StateDataManager(self)
        
        # State button references
        self.state_buttons: dict[str, StateButton] = {}
        
        self._setup_window()
        self._setup_menu_bar()
        self._setup_toolbar()
        self._setup_central_widget()
        self._setup_status_bar()
        self._setup_shortcuts()
        self._restore_state()
        
        # Apply stylesheet
        self._apply_stylesheet()
    
    def _load_modes_config(self) -> dict:
        """Load queue modes configuration."""
        config_path = Path(__file__).parent.parent.parent.parent / "config" / "queue_modes.json"
        try:
            with open(config_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            # Return default config if file not found
            return {
                "modes": {
                    "All": {"description": "All states equally", "primary": [], "secondary": [], "excluded": []}
                },
                "default_mode": "All"
            }
    
    def _setup_window(self):
        """Configure main window properties."""
        self.setWindowTitle("License Plate Information")
        self.setMinimumSize(1200, 800)
        
        # Set default geometry if not restored
        screen = QApplication.primaryScreen().availableGeometry()
        self.setGeometry(
            screen.width() // 8,
            screen.height() // 8,
            screen.width() * 3 // 4,
            screen.height() * 3 // 4
        )
    
    def _setup_menu_bar(self):
        """Create the menu bar with all menus."""
        menubar = self.menuBar()
        
        # ===== File Menu =====
        file_menu = menubar.addMenu("&File")
        
        export_state_action = QAction("Export State Data...", self)
        export_state_action.setShortcut(QKeySequence("Ctrl+E"))
        export_state_action.triggered.connect(self._on_export_state_data)
        file_menu.addAction(export_state_action)
        
        export_search_action = QAction("Export Search Results...", self)
        export_search_action.triggered.connect(self._on_export_search_results)
        file_menu.addAction(export_search_action)
        
        file_menu.addSeparator()
        
        settings_action = QAction("Settings", self)
        settings_action.setShortcut(QKeySequence("Ctrl+,"))
        settings_action.triggered.connect(self._on_settings)
        file_menu.addAction(settings_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence("Alt+F4"))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # ===== View Menu =====
        view_menu = menubar.addMenu("&View")
        
        toggle_state_panel_action = QAction("Toggle State Panel", self)
        toggle_state_panel_action.setShortcut(QKeySequence("Ctrl+1"))
        toggle_state_panel_action.triggered.connect(self._on_toggle_state_panel)
        view_menu.addAction(toggle_state_panel_action)
        
        toggle_info_bar_action = QAction("Toggle Quick Info Bar", self)
        toggle_info_bar_action.setShortcut(QKeySequence("Ctrl+2"))
        toggle_info_bar_action.triggered.connect(self._on_toggle_info_bar)
        view_menu.addAction(toggle_info_bar_action)
        
        view_menu.addSeparator()
        
        expand_all_action = QAction("Expand All Panels", self)
        expand_all_action.triggered.connect(self._on_expand_all_panels)
        view_menu.addAction(expand_all_action)
        
        collapse_all_action = QAction("Collapse All Panels", self)
        collapse_all_action.triggered.connect(self._on_collapse_all_panels)
        view_menu.addAction(collapse_all_action)
        
        view_menu.addSeparator()
        
        zoom_in_action = QAction("Zoom In", self)
        zoom_in_action.setShortcut(QKeySequence("Ctrl++"))
        zoom_in_action.triggered.connect(self._on_zoom_in)
        view_menu.addAction(zoom_in_action)
        
        zoom_out_action = QAction("Zoom Out", self)
        zoom_out_action.setShortcut(QKeySequence("Ctrl+-"))
        zoom_out_action.triggered.connect(self._on_zoom_out)
        view_menu.addAction(zoom_out_action)
        
        reset_zoom_action = QAction("Reset Zoom", self)
        reset_zoom_action.setShortcut(QKeySequence("Ctrl+0"))
        reset_zoom_action.triggered.connect(self._on_reset_zoom)
        view_menu.addAction(reset_zoom_action)
        
        view_menu.addSeparator()
        
        fullscreen_action = QAction("Full Screen", self)
        fullscreen_action.setShortcut(QKeySequence("F11"))
        fullscreen_action.triggered.connect(self._on_toggle_fullscreen)
        view_menu.addAction(fullscreen_action)
        
        reset_layout_action = QAction("Reset Layout", self)
        reset_layout_action.triggered.connect(self._on_reset_layout)
        view_menu.addAction(reset_layout_action)
        
        # ===== Mode Menu =====
        mode_menu = menubar.addMenu("&Mode")
        
        self.mode_actions = {}
        mode_shortcuts = {
            "All": "Ctrl+Shift+0",
            "V3": "Ctrl+Shift+1",
            "Express": "Ctrl+Shift+2",
            "I95": "Ctrl+Shift+3",
            "OOSV3": "Ctrl+Shift+4",
            "PlateType": "Ctrl+Shift+5",
        }
        
        for mode_name in self.modes_config.get("modes", {}).keys():
            action = QAction(mode_name, self)
            action.setCheckable(True)
            if mode_name in mode_shortcuts:
                action.setShortcut(QKeySequence(mode_shortcuts[mode_name]))
            action.triggered.connect(lambda checked, m=mode_name: self._on_mode_selected(m))
            mode_menu.addAction(action)
            self.mode_actions[mode_name] = action
        
        # Check current mode
        if self.current_mode in self.mode_actions:
            self.mode_actions[self.current_mode].setChecked(True)
        
        mode_menu.addSeparator()
        
        configure_modes_action = QAction("Configure Modes...", self)
        configure_modes_action.triggered.connect(self._on_configure_modes)
        mode_menu.addAction(configure_modes_action)
        
        # ===== Tools Menu =====
        tools_menu = menubar.addMenu("&Tools")
        
        search_action = QAction("Search All States", self)
        search_action.setShortcut(QKeySequence("Ctrl+F"))
        search_action.triggered.connect(self._on_search)
        tools_menu.addAction(search_action)
        
        jump_action = QAction("Jump to State...", self)
        jump_action.setShortcut(QKeySequence("Ctrl+G"))
        jump_action.triggered.connect(self._on_jump_to_state)
        tools_menu.addAction(jump_action)
        
        tools_menu.addSeparator()
        
        refresh_action = QAction("Refresh Database", self)
        refresh_action.setShortcut(QKeySequence("F5"))
        refresh_action.triggered.connect(self._on_refresh_database)
        tools_menu.addAction(refresh_action)
        
        clear_history_action = QAction("Clear Search History", self)
        clear_history_action.triggered.connect(self._on_clear_search_history)
        tools_menu.addAction(clear_history_action)
        
        # ===== Notes Menu (prominent for feedback) =====
        notes_menu = menubar.addMenu("&Notes")
        
        edit_notes_action = QAction("Edit Notes...", self)
        edit_notes_action.setShortcut(QKeySequence("Ctrl+N"))
        edit_notes_action.triggered.connect(self._on_edit_notes)
        notes_menu.addAction(edit_notes_action)
        
        notes_menu.addSeparator()
        
        open_notes_file_action = QAction("Open Notes File Location", self)
        open_notes_file_action.triggered.connect(self._on_open_notes_location)
        notes_menu.addAction(open_notes_file_action)
        
        # ===== Help Menu =====
        help_menu = menubar.addMenu("&Help")
        
        user_guide_action = QAction("User Guide", self)
        user_guide_action.setShortcut(QKeySequence("F1"))
        user_guide_action.triggered.connect(lambda: self._on_show_help("user_guide"))
        help_menu.addAction(user_guide_action)
        
        shortcuts_action = QAction("Keyboard Shortcuts", self)
        shortcuts_action.setShortcut(QKeySequence("Ctrl+/"))
        shortcuts_action.triggered.connect(lambda: self._on_show_help("shortcuts"))
        help_menu.addAction(shortcuts_action)
        
        help_menu.addSeparator()
        
        # Plate Reading Tips submenu
        tips_menu = help_menu.addMenu("Plate Reading Tips")
        
        obscured_action = QAction("Obscured/Partial Plates", self)
        obscured_action.triggered.connect(lambda: self._on_show_help("plate_reading_tips", "obscured"))
        tips_menu.addAction(obscured_action)
        
        damaged_action = QAction("Damaged Characters", self)
        damaged_action.triggered.connect(lambda: self._on_show_help("plate_reading_tips", "damaged"))
        tips_menu.addAction(damaged_action)
        
        stacked_action = QAction("Stacked Characters", self)
        stacked_action.triggered.connect(lambda: self._on_show_help("plate_reading_tips", "stacked"))
        tips_menu.addAction(stacked_action)
        
        # Button Reference submenu
        buttons_menu = help_menu.addMenu("Button Reference")
        
        accept_btn_action = QAction("Accept - Confirm Correct Entry", self)
        accept_btn_action.triggered.connect(lambda: self._on_show_help("button_reference", "accept"))
        buttons_menu.addAction(accept_btn_action)
        
        buttons_menu.addSeparator()
        
        p_btn_action = QAction("P - Plate Unreadable", self)
        p_btn_action.triggered.connect(lambda: self._on_show_help("button_reference", "p_unreadable"))
        buttons_menu.addAction(p_btn_action)
        
        o_btn_action = QAction("O - Plate Obscured", self)
        o_btn_action.triggered.connect(lambda: self._on_show_help("button_reference", "o_obscured"))
        buttons_menu.addAction(o_btn_action)
        
        n_btn_action = QAction("N - No Plate Visible", self)
        n_btn_action.triggered.connect(lambda: self._on_show_help("button_reference", "n_no_plate"))
        buttons_menu.addAction(n_btn_action)
        
        t_btn_action = QAction("T - Technical Issue", self)
        t_btn_action.triggered.connect(lambda: self._on_show_help("button_reference", "t_technical"))
        buttons_menu.addAction(t_btn_action)
        
        e_btn_action = QAction("E - Emergency Vehicle", self)
        e_btn_action.triggered.connect(lambda: self._on_show_help("button_reference", "e_emergency"))
        buttons_menu.addAction(e_btn_action)
        
        x_btn_action = QAction("X - Other", self)
        x_btn_action.triggered.connect(lambda: self._on_show_help("button_reference", "x_other"))
        buttons_menu.addAction(x_btn_action)
        
        r_btn_action = QAction("R - Mark for Review", self)
        r_btn_action.triggered.connect(lambda: self._on_show_help("button_reference", "r_review"))
        buttons_menu.addAction(r_btn_action)
        
        emergency_action = QAction("Emergency Vehicle Guide", self)
        emergency_action.triggered.connect(lambda: self._on_show_help("emergency_vehicles"))
        help_menu.addAction(emergency_action)
        
        char_recognition_action = QAction("Character Recognition (O vs 0)", self)
        char_recognition_action.triggered.connect(lambda: self._on_show_help("plate_reading_tips", "o_vs_0"))
        help_menu.addAction(char_recognition_action)
        
        help_menu.addSeparator()
        
        about_action = QAction("About License Plate Info", self)
        about_action.triggered.connect(self._on_about)
        help_menu.addAction(about_action)
    
    def _setup_toolbar(self):
        """Create the toolbar with mode selector."""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        # Mode label
        mode_label = QLabel("Mode:")
        mode_label.setStyleSheet("padding: 0 8px;")
        toolbar.addWidget(mode_label)
        
        # Mode dropdown
        self.mode_combo = QComboBox()
        self.mode_combo.setMinimumWidth(120)
        for mode_name, mode_config in self.modes_config.get("modes", {}).items():
            self.mode_combo.addItem(mode_name)
        
        # Set current mode
        index = self.mode_combo.findText(self.current_mode)
        if index >= 0:
            self.mode_combo.setCurrentIndex(index)
        
        self.mode_combo.currentTextChanged.connect(self._on_mode_selected)
        toolbar.addWidget(self.mode_combo)
        
        toolbar.addSeparator()
        
        # Current mode description
        self.mode_description = QLabel()
        self._update_mode_description()
        toolbar.addWidget(self.mode_description)
    
    def _setup_central_widget(self):
        """Create the central widget with splitter layout."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(4, 4, 4, 4)
        main_layout.setSpacing(0)
        
        # Main horizontal splitter (State Panel | Content Area)
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(self.main_splitter)
        
        # Left panel - Search & State selection
        self.state_panel = self._create_state_panel()
        self.main_splitter.addWidget(self.state_panel)
        
        # Right side - Content area with 2x2 grid
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Vertical splitter for top/bottom rows
        self.content_splitter = QSplitter(Qt.Orientation.Vertical)
        content_layout.addWidget(self.content_splitter)
        
        # Top row splitter (State Info | Character Rules)
        self.top_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # State Info Panel / Search Results Panel
        self.state_info_panel = self._create_state_info_panel()
        self.top_splitter.addWidget(self.state_info_panel)
        
        # Character Rules Panel
        self.char_rules_panel = self._create_char_rules_panel()
        self.top_splitter.addWidget(self.char_rules_panel)
        
        self.content_splitter.addWidget(self.top_splitter)
        
        # Bottom row splitter (Plate Type Info | Images)
        self.bottom_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Plate Type Info Panel
        self.plate_type_panel = self._create_plate_type_panel()
        self.bottom_splitter.addWidget(self.plate_type_panel)
        
        # Image Panel
        self.image_panel = ImagePanel(self.data_path)
        self.bottom_splitter.addWidget(self.image_panel)
        
        self.content_splitter.addWidget(self.bottom_splitter)
        
        self.main_splitter.addWidget(content_widget)
        
        # Set initial splitter sizes
        self.main_splitter.setSizes([300, 900])
        self.content_splitter.setSizes([400, 400])
        self.top_splitter.setSizes([500, 500])
        self.bottom_splitter.setSizes([500, 500])
    
    def _create_state_panel(self) -> QWidget:
        """Create the left panel with search controls and state buttons."""
        panel = QWidget()
        panel.setMinimumWidth(250)
        panel.setMaximumWidth(400)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(8)
        
        # ===== Search Section =====
        search_group = QGroupBox("🔍 Search")
        search_layout = QVBoxLayout(search_group)
        search_layout.setSpacing(8)
        
        # Search input with clear button
        search_input_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search all data...")
        self.search_input.textChanged.connect(self._on_search_text_changed)
        self.search_input.returnPressed.connect(self._on_search_enter)
        search_input_layout.addWidget(self.search_input)
        
        self.search_clear_btn = QPushButton("✕")
        self.search_clear_btn.setFixedWidth(30)
        self.search_clear_btn.setToolTip("Clear search")
        self.search_clear_btn.clicked.connect(self._on_clear_search)
        self.search_clear_btn.setVisible(False)
        search_input_layout.addWidget(self.search_clear_btn)
        search_layout.addLayout(search_input_layout)
        
        # State filter dropdown
        state_filter_layout = QHBoxLayout()
        state_filter_layout.addWidget(QLabel("State:"))
        self.state_filter_combo = QComboBox()
        self.state_filter_combo.addItem("All States", None)
        for state_code in sorted(self.search_controller.get_all_states()):
            self.state_filter_combo.addItem(state_code, state_code)
        self.state_filter_combo.currentIndexChanged.connect(self._on_filter_changed)
        state_filter_layout.addWidget(self.state_filter_combo, 1)
        search_layout.addLayout(state_filter_layout)
        
        # Category filter dropdown
        category_layout = QHBoxLayout()
        category_layout.addWidget(QLabel("Category:"))
        self.category_combo = QComboBox()
        for key, label in SearchController.CATEGORIES.items():
            self.category_combo.addItem(label, key)
        self.category_combo.currentIndexChanged.connect(self._on_filter_changed)
        category_layout.addWidget(self.category_combo, 1)
        search_layout.addLayout(category_layout)
        
        # Search result count
        self.search_result_label = QLabel("")
        self.search_result_label.setStyleSheet("color: #b0b0b0; font-style: italic;")
        search_layout.addWidget(self.search_result_label)
        
        layout.addWidget(search_group)
        
        # ===== Separator =====
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #404040;")
        layout.addWidget(separator)
        
        # ===== Mode Section =====
        mode_label = QLabel(f"Mode: {self.current_mode}")
        mode_label.setStyleSheet("font-weight: bold; color: #4CAF50; font-size: 10px;")
        self.state_panel_mode_label = mode_label
        layout.addWidget(mode_label)
        
        # ===== State Buttons - Single Grid with All States =====
        # Use a scroll area with flow layout for consistent button sizing
        self.states_scroll = QScrollArea()
        self.states_scroll.setWidgetResizable(True)
        self.states_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.states_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.states_scroll.setMinimumHeight(150)
        self.states_scroll.setMaximumHeight(300)
        self.states_scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        self.states_container = QWidget()
        self.states_container.setStyleSheet("background: transparent;")
        self.states_scroll.setWidget(self.states_container)
        
        # Use FlowLayout for proper wrapping
        from ui.widgets.flow_layout import FlowLayout
        self.states_flow = FlowLayout(self.states_container, margin=4, hSpacing=2, vSpacing=2)
        
        layout.addWidget(self.states_scroll)
        
        # Populate state buttons
        self._populate_state_buttons()
        
        layout.addStretch()
        
        # ===== Plate Type Dropdown =====
        plate_type_layout = QHBoxLayout()
        plate_type_layout.addWidget(QLabel("Plate Type:"))
        self.plate_type_combo = QComboBox()
        self.plate_type_combo.addItem("Standard", "standard")
        self.plate_type_combo.currentIndexChanged.connect(self._on_plate_type_changed)
        plate_type_layout.addWidget(self.plate_type_combo, 1)
        layout.addLayout(plate_type_layout)
        
        return panel
    
    def _create_state_info_panel(self) -> QScrollArea:
        """Create the state info / search results panel."""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        
        # Header
        self.state_info_header = QLabel("State Information")
        self.state_info_header.setProperty("class", "header")
        self.state_info_header.setStyleSheet("font-size: 16px; font-weight: bold; color: #4CAF50;")
        layout.addWidget(self.state_info_header)
        
        # Content area - will be populated by search results or state info
        self.state_info_content = QLabel("Select a state or search to see information.")
        self.state_info_content.setWordWrap(True)
        self.state_info_content.setStyleSheet("color: #b0b0b0;")
        layout.addWidget(self.state_info_content)
        
        # Results list (hidden by default, shown in search mode)
        self.state_results_list = QListWidget()
        self.state_results_list.setVisible(False)
        self.state_results_list.itemClicked.connect(self._on_state_result_clicked)
        layout.addWidget(self.state_results_list)
        
        layout.addStretch()
        scroll.setWidget(content)
        return scroll
    
    def _create_char_rules_panel(self) -> QScrollArea:
        """Create the character rules panel."""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        
        # Header
        self.char_rules_header = QLabel("Character Rules")
        self.char_rules_header.setStyleSheet("font-size: 16px; font-weight: bold; color: #4CAF50;")
        layout.addWidget(self.char_rules_header)
        
        # Content area
        self.char_rules_content = QLabel("Select a state or search to see character rules.")
        self.char_rules_content.setWordWrap(True)
        self.char_rules_content.setStyleSheet("color: #b0b0b0;")
        layout.addWidget(self.char_rules_content)
        
        # Results list (hidden by default)
        self.char_rules_list = QListWidget()
        self.char_rules_list.setVisible(False)
        self.char_rules_list.itemClicked.connect(self._on_char_rule_result_clicked)
        layout.addWidget(self.char_rules_list)
        
        # Font preview widget
        self.font_preview = FontPreviewWidget()
        layout.addWidget(self.font_preview, 1)  # Give it stretch factor
        
        scroll.setWidget(content)
        return scroll
    
    def _create_plate_type_panel(self) -> QScrollArea:
        """Create the plate type info panel."""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        
        # Header
        self.plate_type_header = QLabel("Plate Type Information")
        self.plate_type_header.setStyleSheet("font-size: 16px; font-weight: bold; color: #4CAF50;")
        layout.addWidget(self.plate_type_header)
        
        # Content area
        self.plate_type_content = QLabel("Select a state or search to see plate types.")
        self.plate_type_content.setWordWrap(True)
        self.plate_type_content.setStyleSheet("color: #b0b0b0;")
        layout.addWidget(self.plate_type_content)
        
        # Results list (hidden by default)
        self.plate_type_list = QListWidget()
        self.plate_type_list.setVisible(False)
        self.plate_type_list.itemClicked.connect(self._on_plate_type_result_clicked)
        layout.addWidget(self.plate_type_list)
        
        layout.addStretch()
        scroll.setWidget(content)
        return scroll
    
    def _setup_status_bar(self):
        """Create the status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Permanent widgets
        self.status_mode = QLabel(f"Mode: {self.current_mode}")
        self.status_state = QLabel("State: -")
        self.status_plate_type = QLabel("Plate: -")
        self.status_db = QLabel("DB: Connected")
        
        self.status_bar.addPermanentWidget(self.status_mode)
        self.status_bar.addPermanentWidget(QLabel("|"))
        self.status_bar.addPermanentWidget(self.status_state)
        self.status_bar.addPermanentWidget(QLabel("|"))
        self.status_bar.addPermanentWidget(self.status_plate_type)
        self.status_bar.addPermanentWidget(QLabel("|"))
        self.status_bar.addPermanentWidget(self.status_db)
        
        self.status_bar.showMessage("Ready")
    
    def _setup_shortcuts(self):
        """Set up additional keyboard shortcuts."""
        # Search - Ctrl+F
        self.shortcut_search = QShortcut(QKeySequence("Ctrl+F"), self)
        self.shortcut_search.activated.connect(self._on_search)
        
        # Jump to state - Ctrl+G
        self.shortcut_jump = QShortcut(QKeySequence("Ctrl+G"), self)
        self.shortcut_jump.activated.connect(self._on_jump_to_state)
        
        # Toggle state panel - Ctrl+1
        self.shortcut_toggle_panel = QShortcut(QKeySequence("Ctrl+1"), self)
        self.shortcut_toggle_panel.activated.connect(self._toggle_state_panel)
        
        # Mode shortcuts - Ctrl+Shift+1 through 6
        self.shortcut_mode_v3 = QShortcut(QKeySequence("Ctrl+Shift+1"), self)
        self.shortcut_mode_v3.activated.connect(lambda: self._switch_mode("V3"))
        
        self.shortcut_mode_express = QShortcut(QKeySequence("Ctrl+Shift+2"), self)
        self.shortcut_mode_express.activated.connect(lambda: self._switch_mode("Express"))
        
        self.shortcut_mode_i95 = QShortcut(QKeySequence("Ctrl+Shift+3"), self)
        self.shortcut_mode_i95.activated.connect(lambda: self._switch_mode("I95"))
        
        self.shortcut_mode_oosv3 = QShortcut(QKeySequence("Ctrl+Shift+4"), self)
        self.shortcut_mode_oosv3.activated.connect(lambda: self._switch_mode("OOSV3"))
        
        self.shortcut_mode_platetype = QShortcut(QKeySequence("Ctrl+Shift+5"), self)
        self.shortcut_mode_platetype.activated.connect(lambda: self._switch_mode("PlateType"))
        
        self.shortcut_mode_all = QShortcut(QKeySequence("Ctrl+Shift+0"), self)
        self.shortcut_mode_all.activated.connect(lambda: self._switch_mode("All"))
        
        # Clear search / Deselect - Escape
        self.shortcut_escape = QShortcut(QKeySequence("Escape"), self)
        self.shortcut_escape.activated.connect(self._on_escape)
    
    def _toggle_state_panel(self):
        """Toggle visibility of the state panel."""
        if self.state_panel.isVisible():
            self.state_panel.hide()
            self.status_bar.showMessage("State panel hidden (Ctrl+1 to show)", 2000)
        else:
            self.state_panel.show()
            self.status_bar.showMessage("State panel shown", 2000)
    
    def _switch_mode(self, mode_name: str):
        """Switch to the specified mode."""
        if mode_name in self.modes_config.get("modes", {}):
            index = self.mode_combo.findText(mode_name)
            if index >= 0:
                self.mode_combo.setCurrentIndex(index)
    
    def _on_escape(self):
        """Handle Escape key - clear search or deselect state."""
        if self.search_input.text():
            self._on_clear_search()
        elif self.current_state:
            self._deselect_state()
    
    def _apply_stylesheet(self):
        """Load and apply the dark theme stylesheet."""
        style_path = Path(__file__).parent / "resources" / "styles" / "dark_theme.qss"
        try:
            with open(style_path, "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print(f"Warning: Stylesheet not found at {style_path}")
    
    def _restore_state(self):
        """Restore window state from settings."""
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
        
        state = self.settings.value("windowState")
        if state:
            self.restoreState(state)
        
        # Restore splitter states
        main_splitter_state = self.settings.value("mainSplitter")
        if main_splitter_state:
            self.main_splitter.restoreState(main_splitter_state)
        
        content_splitter_state = self.settings.value("contentSplitter")
        if content_splitter_state:
            self.content_splitter.restoreState(content_splitter_state)
        
        top_splitter_state = self.settings.value("topSplitter")
        if top_splitter_state:
            self.top_splitter.restoreState(top_splitter_state)
        
        bottom_splitter_state = self.settings.value("bottomSplitter")
        if bottom_splitter_state:
            self.bottom_splitter.restoreState(bottom_splitter_state)
    
    def _save_state(self):
        """Save window state to settings."""
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
        self.settings.setValue("mainSplitter", self.main_splitter.saveState())
        self.settings.setValue("contentSplitter", self.content_splitter.saveState())
        self.settings.setValue("topSplitter", self.top_splitter.saveState())
        self.settings.setValue("bottomSplitter", self.bottom_splitter.saveState())
        self.settings.setValue("currentMode", self.current_mode)
    
    def _update_mode_description(self):
        """Update the mode description label."""
        mode_config = self.modes_config.get("modes", {}).get(self.current_mode, {})
        description = mode_config.get("description", "")
        self.mode_description.setText(f"  {description}")
        self.mode_description.setStyleSheet("color: #b0b0b0; padding: 0 8px;")
    
    def closeEvent(self, event: QCloseEvent):
        """Handle window close event."""
        self._save_state()
        event.accept()
    
    # ==================== Menu Action Handlers ====================
    
    def _on_export_state_data(self):
        """Export current state data to JSON or text file."""
        if not self.current_state:
            QMessageBox.information(
                self, "Export State Data",
                "Please select a state first."
            )
            return
        
        # Get state data
        state_info = self.state_data_manager.get_state_info_summary(self.current_state)
        char_rules = self.state_data_manager.get_character_rules(self.current_state)
        plate_types = self.state_data_manager.get_plate_types(self.current_state)
        
        if not state_info:
            QMessageBox.warning(
                self, "Export State Data",
                f"No data found for {self.current_state}."
            )
            return
        
        # Ask for save location
        file_path, selected_filter = QFileDialog.getSaveFileName(
            self,
            "Export State Data",
            f"{self.current_state}_data.json",
            "JSON Files (*.json);;Text Files (*.txt);;All Files (*)"
        )
        
        if not file_path:
            return
        
        try:
            export_data = {
                "state_code": self.current_state,
                "state_info": state_info,
                "character_rules": char_rules,
                "plate_types": plate_types
            }
            
            if file_path.endswith('.txt'):
                # Export as readable text
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"State Data Export: {self.current_state}\n")
                    f.write("=" * 50 + "\n\n")
                    
                    f.write("STATE INFORMATION\n")
                    f.write("-" * 30 + "\n")
                    for key, value in state_info.items():
                        f.write(f"{key}: {value}\n")
                    
                    f.write("\nCHARACTER RULES\n")
                    f.write("-" * 30 + "\n")
                    for key, value in char_rules.items():
                        f.write(f"{key}: {value}\n")
                    
                    f.write(f"\nPLATE TYPES ({len(plate_types)} total)\n")
                    f.write("-" * 30 + "\n")
                    for pt in plate_types:
                        name = pt.get('type_name', 'Unknown')
                        f.write(f"- {name}\n")
            else:
                # Export as JSON
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            self.status_bar.showMessage(f"Exported {self.current_state} data to {file_path}", 3000)
            
        except Exception as e:
            QMessageBox.critical(
                self, "Export Error",
                f"Failed to export data:\n{str(e)}"
            )
    
    def _on_export_search_results(self):
        """Export search results to JSON or text file."""
        if not self.is_search_mode or not hasattr(self, '_last_search_results'):
            QMessageBox.information(
                self, "Export Search Results",
                "Please perform a search first."
            )
            return
        
        results = self._last_search_results
        if not results or results.is_empty:
            QMessageBox.information(
                self, "Export Search Results",
                "No search results to export."
            )
            return
        
        # Ask for save location
        file_path, selected_filter = QFileDialog.getSaveFileName(
            self,
            "Export Search Results",
            f"search_results.json",
            "JSON Files (*.json);;Text Files (*.txt);;All Files (*)"
        )
        
        if not file_path:
            return
        
        try:
            if file_path.endswith('.txt'):
                # Export as readable text
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"Search Results Export\n")
                    f.write(f"Query: {self.search_input.text()}\n")
                    f.write("=" * 50 + "\n\n")
                    
                    if results.state_results:
                        f.write(f"STATE INFO ({len(results.state_results)} matches)\n")
                        f.write("-" * 30 + "\n")
                        for r in results.state_results:
                            f.write(f"  [{r.state_code}] {r.field}: {r.value[:100]}\n")
                    
                    if results.plate_type_results:
                        f.write(f"\nPLATE TYPES ({len(results.plate_type_results)} matches)\n")
                        f.write("-" * 30 + "\n")
                        for r in results.plate_type_results:
                            f.write(f"  [{r.state_code}] {r.plate_type or r.field}: {r.value[:100]}\n")
                    
                    if results.char_rules_results:
                        f.write(f"\nCHARACTER RULES ({len(results.char_rules_results)} matches)\n")
                        f.write("-" * 30 + "\n")
                        for r in results.char_rules_results:
                            f.write(f"  [{r.state_code}] {r.field}: {r.value[:100]}\n")
            else:
                # Export as JSON
                export_data = {
                    "query": self.search_input.text(),
                    "total_results": results.total_count,
                    "state_info": [r.to_dict() for r in results.state_results],
                    "plate_types": [r.to_dict() for r in results.plate_type_results],
                    "char_rules": [r.to_dict() for r in results.char_rules_results]
                }
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)
            
            self.status_bar.showMessage(f"Exported search results to {file_path}", 3000)
            
        except Exception as e:
            QMessageBox.critical(
                self, "Export Error",
                f"Failed to export search results:\n{str(e)}"
            )
    
    def _on_settings(self):
        """Open settings dialog."""
        self.status_bar.showMessage("Settings - Not yet implemented", 3000)
    
    def _on_toggle_state_panel(self):
        """Toggle state panel visibility."""
        self.state_panel.setVisible(not self.state_panel.isVisible())
    
    def _on_toggle_info_bar(self):
        """Toggle quick info bar visibility."""
        self.status_bar.showMessage("Toggle Info Bar - Not yet implemented", 3000)
    
    def _on_expand_all_panels(self):
        """Expand all collapsible panels."""
        self.status_bar.showMessage("Expand All - Not yet implemented", 3000)
    
    def _on_collapse_all_panels(self):
        """Collapse all collapsible panels."""
        self.status_bar.showMessage("Collapse All - Not yet implemented", 3000)
    
    def _on_zoom_in(self):
        """Zoom in on images."""
        self.status_bar.showMessage("Zoom In - Not yet implemented", 3000)
    
    def _on_zoom_out(self):
        """Zoom out on images."""
        self.status_bar.showMessage("Zoom Out - Not yet implemented", 3000)
    
    def _on_reset_zoom(self):
        """Reset image zoom."""
        self.status_bar.showMessage("Reset Zoom - Not yet implemented", 3000)
    
    def _on_toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
    
    def _on_reset_layout(self):
        """Reset layout to defaults."""
        self.main_splitter.setSizes([250, 950])
        self.content_splitter.setSizes([400, 400])
        self.top_splitter.setSizes([500, 500])
        self.bottom_splitter.setSizes([500, 500])
        self.status_bar.showMessage("Layout reset to defaults", 3000)
    
    def _on_mode_selected(self, mode_name: str):
        """Handle mode selection from menu or dropdown."""
        if mode_name == self.current_mode:
            return
        
        # Update mode via controller
        self.mode_controller.set_mode(mode_name)
        
        # Update mode
        self.current_mode = mode_name
        
        # Update UI
        self.mode_combo.blockSignals(True)
        index = self.mode_combo.findText(mode_name)
        if index >= 0:
            self.mode_combo.setCurrentIndex(index)
        self.mode_combo.blockSignals(False)
        
        # Update menu checkmarks
        for name, action in self.mode_actions.items():
            action.setChecked(name == mode_name)
        
        # Update status bar and description
        self.status_mode.setText(f"Mode: {mode_name}")
        self._update_mode_description()
        
        # Update state panel mode label
        if hasattr(self, 'state_panel_mode_label'):
            self.state_panel_mode_label.setText(f"Mode: {mode_name}")
        
        # Re-layout state buttons (colors are automatic based on category)
        self._layout_state_buttons()
        
        # Emit signal
        self.mode_changed.emit(mode_name)
        
        self.status_bar.showMessage(f"Switched to {mode_name} mode", 2000)
    
    def _on_mode_changed_from_controller(self, mode_name: str, config: dict):
        """Handle mode change from ModeController."""
        # This is called when mode changes via controller (not UI)
        pass
    
    def _populate_state_buttons(self):
        """Create all state buttons and organize by current mode."""
        # Clear existing buttons
        self.state_buttons.clear()
        
        # Create buttons for all jurisdictions (category auto-detected by StateButton)
        for state_code in self.mode_controller.ALL_JURISDICTIONS:
            btn = StateButton(state_code)
            btn.state_clicked.connect(self._on_state_button_clicked)
            self.state_buttons[state_code] = btn
        
        # Lay out all buttons in grid (8 columns to fit in panel)
        self._layout_state_buttons()
    
    def _layout_state_buttons(self):
        """Layout all state buttons using flow layout."""
        # Clear flow layout
        while self.states_flow.count():
            item = self.states_flow.takeAt(0)
            widget = item.widget() if item else None
            if widget:
                widget.setParent(None)
        
        # Order: FL first, then plate_type, nearby, distant_major, territories, normal, canadian
        ordered_states = []
        
        # Florida first
        ordered_states.extend([s for s in ['FL'] if s in self.state_buttons])
        
        # Plate Type states
        plate_type = ['MA', 'ME', 'OH', 'IN', 'IL']
        ordered_states.extend([s for s in plate_type if s in self.state_buttons])
        
        # Nearby states (sorted)
        nearby = ['GA', 'AL', 'SC', 'NC', 'TN', 'MS', 'LA']
        ordered_states.extend([s for s in nearby if s in self.state_buttons])
        
        # Distant major states
        distant = ['CA', 'TX', 'NY', 'PA', 'NJ', 'WA', 'AZ', 'CO', 'VA', 'MD']
        ordered_states.extend([s for s in distant if s in self.state_buttons])
        
        # Territories
        territories = ['DC', 'PR', 'GU', 'VI', 'AS', 'MP']
        ordered_states.extend([s for s in territories if s in self.state_buttons])
        
        # All other US states (alphabetical)
        used = set(ordered_states)
        other_us = sorted([s for s in self.state_buttons.keys() 
                          if s not in StateButton.CANADIAN and s not in used])
        ordered_states.extend(other_us)
        
        # Canadian provinces last
        canadian = ['ON', 'QC', 'BC', 'AB', 'MB', 'SK', 'NS', 'NB', 'NL', 'PE', 'NT', 'NU', 'YT']
        ordered_states.extend([s for s in canadian if s in self.state_buttons])
        
        # Add buttons to flow layout - they will wrap automatically
        for state in ordered_states:
            btn = self.state_buttons[state]
            self.states_flow.addWidget(btn)
        
        # Update selection highlight
        if self.current_state:
            self._highlight_selected_state(self.current_state)
    
    def _clear_grid(self, grid: QGridLayout):
        """Remove all widgets from a grid layout without deleting them."""
        while grid.count():
            item = grid.takeAt(0)
            widget = item.widget() if item else None
            if widget:
                widget.setParent(None)
    
    def _on_state_button_clicked(self, state_code: str):
        """Handle state button click."""
        self._select_state(state_code)
    
    def _select_state(self, state_code: str):
        """Select a state and update all panels. Toggle off if already selected."""
        # Clear search if active
        if self.is_search_mode:
            self._on_clear_search()
        
        # Toggle: if clicking the same state, deselect it
        if state_code == self.current_state:
            self._deselect_state()
            return
        
        # Update selection
        old_state = self.current_state
        self.current_state = state_code
        
        # Update button highlights
        if old_state and old_state in self.state_buttons:
            self.state_buttons[old_state].set_selected(False)
        if state_code in self.state_buttons:
            self.state_buttons[state_code].set_selected(True)
        
        # Update font preview
        self.font_preview.update_state(state_code)
        
        # Load state data and update all panels
        self._update_panels_with_state(state_code)
        
        # Update status
        state_data = self.state_data_manager.get_state_data(state_code)
        state_name = state_data.get('name', state_code) if state_data else state_code
        self.status_bar.showMessage(f"Selected: {state_name} ({state_code})", 2000)
        
        # Emit signal
        self.state_selected.emit(state_code)
    
    def _deselect_state(self):
        """Deselect the current state and clear panels."""
        if self.current_state and self.current_state in self.state_buttons:
            self.state_buttons[self.current_state].set_selected(False)
        
        self.current_state = None
        
        # Clear panels
        self.state_info_header.setText("State Information")
        self.state_info_content.setText("Select a state or search to see information.")
        self.state_info_content.setVisible(True)
        self.state_results_list.setVisible(False)
        
        self.char_rules_header.setText("Character Rules")
        self.char_rules_content.setText("Select a state or search to see character rules.")
        self.char_rules_content.setVisible(True)
        self.char_rules_list.setVisible(False)
        
        self.plate_type_header.setText("Plate Type Information")
        self.plate_type_content.setText("Select a state or search to see plate types.")
        self.plate_type_content.setVisible(True)
        self.plate_type_list.setVisible(False)
        
        # Clear font preview
        self.font_preview.clear()
        
        # Clear image panel
        self.image_panel.set_state(None)
        
        # Reset plate type dropdown
        self.plate_type_combo.blockSignals(True)
        self.plate_type_combo.clear()
        self.plate_type_combo.addItem("Standard", "standard")
        self.plate_type_combo.blockSignals(False)
        
        self.status_bar.showMessage("State deselected", 1500)
    
    def _update_panels_with_state(self, state_code: str):
        """Update all content panels with state information."""
        # Get state data
        state_info = self.state_data_manager.get_state_info_summary(state_code)
        char_rules = self.state_data_manager.get_character_rules(state_code)
        plate_types = self.state_data_manager.get_plate_types(state_code)
        
        # Update State Info Panel
        self._display_state_info(state_info)
        
        # Update Character Rules Panel
        self._display_char_rules(state_code, char_rules)
        
        # Update Plate Type Panel
        self._display_plate_types(state_code, plate_types)
        
        # Update Image Panel
        self.image_panel.set_state(state_code)
        
        # Update Plate Type Dropdown
        self._update_plate_type_dropdown(plate_types)
        
        # Update Font Preview with state character data
        self._update_font_preview(state_code, char_rules)
    
    def _display_state_info(self, info: dict):
        """Display state info in the State Info panel."""
        if not info:
            self.state_info_header.setText("State Information")
            self.state_info_content.setText("No data available")
            self.state_info_content.setVisible(True)
            self.state_results_list.setVisible(False)
            return
        
        # Hide search results, show content
        self.state_results_list.setVisible(False)
        self.state_info_content.setVisible(True)
        
        # Update header
        name = info.get('name', '')
        abbrev = info.get('abbreviation', '')
        self.state_info_header.setText(f"{name} ({abbrev})")
        
        # Build info text with color-coded sections
        lines = []
        
        # Slogan - blue icon
        if info.get('slogan'):
            lines.append(
                f'<span style="color:#2196F3;">📝</span> '
                f'<span style="color:#64B5F6;"><b>Slogan:</b></span> '
                f'<span style="color:#e0e0e0;">{info["slogan"]}</span>'
            )
        
        # Colors - palette icon with actual color swatches
        if info.get('primary_colors'):
            colors = info['primary_colors']
            color_boxes = ' '.join([
                f'<span style="background:{c}; color:{c}; padding:1px 10px; border-radius:2px; margin:0 2px;">▮</span>' 
                for c in colors[:4]
            ])
            lines.append(
                f'<span style="color:#E91E63;">🎨</span> '
                f'<span style="color:#F48FB1;"><b>Colors:</b></span> {color_boxes}'
            )
        
        # Font - text icon (orange)
        if info.get('main_font'):
            lines.append(
                f'<span style="color:#FF9800;">🔤</span> '
                f'<span style="color:#FFB74D;"><b>Font:</b></span> '
                f'<span style="color:#e0e0e0;">{info["main_font"]}</span>'
            )
        
        # Logo - image icon (purple)
        if info.get('main_logo'):
            lines.append(
                f'<span style="color:#9C27B0;">🏷️</span> '
                f'<span style="color:#CE93D8;"><b>Logo:</b></span> '
                f'<span style="color:#e0e0e0;">{info["main_logo"]}</span>'
            )
        
        # Plate Text - license plate icon (green)
        if info.get('main_plate_text'):
            lines.append(
                f'<span style="color:#4CAF50;">🚗</span> '
                f'<span style="color:#81C784;"><b>Plate Text:</b></span> '
                f'<span style="color:#e0e0e0;">{info["main_plate_text"]}</span>'
            )
        
        # Sticker - tag icon (teal)
        sticker = info.get('sticker_format', {})
        if sticker and sticker.get('description'):
            lines.append(
                f'<span style="color:#00BCD4;">🏷️</span> '
                f'<span style="color:#4DD0E1;"><b>Sticker:</b></span> '
                f'<span style="color:#e0e0e0;">{sticker["description"]}</span>'
            )
        
        # Notes - info icon (gray/muted)
        if info.get('notes'):
            # Truncate long notes
            notes = info['notes']
            if len(notes) > 300:
                notes = notes[:300] + "..."
            lines.append(
                f'<span style="color:#607D8B;">📋</span> '
                f'<span style="color:#90A4AE;"><b>Notes:</b></span> '
                f'<span style="color:#9e9e9e;">{notes}</span>'
            )
        
        self.state_info_content.setText("<br><br>".join(lines))
    
    def _display_char_rules(self, state_code: str, rules: dict):
        """Display character rules in the Char Rules panel."""
        if not rules:
            self.char_rules_header.setText("Character Rules")
            self.char_rules_content.setText("No data available")
            self.char_rules_content.setVisible(True)
            self.char_rules_list.setVisible(False)
            return
        
        # Hide search results, show content
        self.char_rules_list.setVisible(False)
        self.char_rules_content.setVisible(True)
        
        # Update header
        self.char_rules_header.setText(f"Character Rules - {state_code}")
        
        # Build rules text with color coding
        lines = []
        
        # O vs 0 rules - most important, prominent display
        if not rules.get('allows_letter_o', True):
            lines.append(
                '<div style="background:#4a1c1c; padding:8px; border-radius:4px; border-left:4px solid #f44336;">'
                '<span style="color:#ef5350; font-size:14px;">❌</span> '
                '<span style="color:#ef5350;"><b>Letter \'O\' NOT USED</b></span><br>'
                '<span style="color:#e57373;">Only number \'0\' appears on plates</span>'
                '</div>'
            )
        elif rules.get('uses_zero_for_o', False):
            lines.append(
                '<div style="background:#4a3c1c; padding:8px; border-radius:4px; border-left:4px solid #ff9800;">'
                '<span style="color:#ffb74d; font-size:14px;">⚠️</span> '
                '<span style="color:#ffb74d;"><b>Uses \'0\' for \'O\'</b></span><br>'
                '<span style="color:#ffe082;">Zero substitutes for letter O</span>'
                '</div>'
            )
        else:
            lines.append(
                '<div style="background:#1c4a2e; padding:8px; border-radius:4px; border-left:4px solid #4caf50;">'
                '<span style="color:#81c784; font-size:14px;">✅</span> '
                '<span style="color:#81c784;"><b>Both \'O\' and \'0\' allowed</b></span><br>'
                '<span style="color:#a5d6a7;">Standard letter O and number 0</span>'
                '</div>'
            )
        
        # Slashed zero - cyan
        if rules.get('zero_is_slashed'):
            lines.append(
                f'<span style="color:#00BCD4;">Ø</span> '
                f'<span style="color:#4DD0E1;"><b>Slashed Zero</b></span> - '
                f'<span style="color:#b0bec5;">Zero has diagonal slash through it</span>'
            )
        
        # Character restrictions - orange warning
        if rules.get('no_letter_o'):
            lines.append(
                f'<span style="color:#FF9800;">⚡</span> '
                f'<span style="color:#FFB74D;"><b>O Rule:</b></span> '
                f'<span style="color:#ffe0b2;">{rules["no_letter_o"]}</span>'
            )
        
        if rules.get('character_restrictions') and rules['character_restrictions'] != rules.get('no_letter_o'):
            lines.append(
                f'<span style="color:#F44336;">🚫</span> '
                f'<span style="color:#EF9A9A;"><b>Restrictions:</b></span> '
                f'<span style="color:#e0e0e0;">{rules["character_restrictions"][:200]}</span>'
            )
        
        # Stacked characters section - purple theme
        if rules.get('stacked_characters'):
            lines.append(
                f'<span style="color:#9C27B0;">📚</span> '
                f'<span style="color:#CE93D8;"><b>Stacked:</b></span> '
                f'<span style="color:#e0e0e0;">{rules["stacked_characters"]}</span>'
            )
        
        if rules.get('stacked_include'):
            include = ', '.join(rules['stacked_include'][:10])
            lines.append(
                f'<span style="color:#4CAF50;">✓</span> '
                f'<span style="color:#81C784;"><b>Include:</b></span> '
                f'<span style="color:#c8e6c9;">{include}</span>'
            )
        
        if rules.get('stacked_omit'):
            omit = ', '.join(rules['stacked_omit'][:10])
            if len(rules['stacked_omit']) > 10:
                omit += f" (+{len(rules['stacked_omit']) - 10} more)"
            lines.append(
                f'<span style="color:#F44336;">✗</span> '
                f'<span style="color:#EF9A9A;"><b>Omit:</b></span> '
                f'<span style="color:#ffcdd2;">{omit}</span>'
            )
        
        if rules.get('stacked_position'):
            lines.append(
                f'<span style="color:#2196F3;">📍</span> '
                f'<span style="color:#64B5F6;"><b>Position:</b></span> '
                f'<span style="color:#e0e0e0;">{rules["stacked_position"][:150]}</span>'
            )
        
        # Slanted characters - teal
        if rules.get('slanted_characters'):
            direction = rules.get('slant_direction', '')
            lines.append(
                f'<span style="color:#009688;">↗</span> '
                f'<span style="color:#4DB6AC;"><b>Slanted:</b></span> '
                f'<span style="color:#e0e0e0;">{rules["slanted_characters"]} {direction}</span>'
            )
        
        self.char_rules_content.setText("<br><br>".join(lines) if lines else "No specific character rules")
    
    def _display_plate_types(self, state_code: str, plate_types: list):
        """Display plate types in the Plate Type panel."""
        # Hide search results, show content
        self.plate_type_list.setVisible(False)
        self.plate_type_content.setVisible(True)
        
        # Update header
        count = len(plate_types)
        self.plate_type_header.setText(f"Plate Types - {state_code} ({count})")
        
        if not plate_types:
            self.plate_type_content.setText("No plate types defined")
            return
        
        # Build plate types text (show first few)
        lines = []
        for i, pt in enumerate(plate_types[:15]):  # Show max 15
            name = pt.get('type_name', 'Unknown')
            desc = pt.get('description', '')
            codes = pt.get('code_numbers', [])
            
            line = f"<b>{name}</b>"
            if codes:
                line += f" <span style='color:#666'>[{', '.join(codes[:3])}]</span>"
            if desc and len(desc) < 100:
                line += f"<br><span style='color:#999'>{desc}</span>"
            lines.append(line)
        
        if count > 15:
            lines.append(f"<span style='color:#666'>... and {count - 15} more plate types</span>")
        
        self.plate_type_content.setText("<br><br>".join(lines))
    
    def _update_plate_type_dropdown(self, plate_types: list):
        """Update the plate type dropdown with types for the current state."""
        # Block signals while updating
        self.plate_type_combo.blockSignals(True)
        
        # Clear and repopulate
        self.plate_type_combo.clear()
        self.plate_type_combo.addItem("Standard", "standard")
        
        for pt in plate_types:
            name = pt.get('type_name', 'Unknown')
            # Use type_name as data value
            self.plate_type_combo.addItem(name, name)
        
        self.plate_type_combo.blockSignals(False)
    
    def _update_font_preview(self, state_code: str, char_rules: dict):
        """Update the font preview widget with state character data."""
        if hasattr(self, 'font_preview'):
            # Determine O vs 0 behavior
            uses_zero_for_o = char_rules.get('uses_zero_for_o', False)
            allows_o = char_rules.get('allows_letter_o', True)
            
            # Update the font preview
            self.font_preview.set_state(state_code, uses_zero_for_o, not allows_o)
    
    def _highlight_selected_state(self, state_code: str):
        """Highlight the selected state button."""
        for code, btn in self.state_buttons.items():
            btn.set_selected(code == state_code)
    
    def _on_configure_modes(self):
        """Open mode configuration dialog."""
        self.status_bar.showMessage("Configure Modes - Not yet implemented", 3000)
    
    def _on_search(self):
        """Focus search input."""
        self.search_input.setFocus()
        self.search_input.selectAll()
    
    def _on_jump_to_state(self):
        """Open jump to state dialog."""
        self.status_bar.showMessage("Jump to State - Not yet implemented", 3000)
    
    def _on_refresh_database(self):
        """Refresh database."""
        self.status_bar.showMessage("Refreshing database...", 2000)
    
    def _on_clear_search_history(self):
        """Clear search history."""
        self.status_bar.showMessage("Search history cleared", 2000)
    
    def _on_edit_notes(self):
        """Open notes editor dialog."""
        from ui.dialogs.notes_dialog import NotesDialog
        dialog = NotesDialog(self.data_path, self)
        dialog.exec()
    
    def _on_open_notes_location(self):
        """Open the folder containing the notes file."""
        import subprocess
        import os
        notes_file = self.data_path / "user_notes.txt"
        
        # Create file if it doesn't exist
        if not notes_file.exists():
            notes_file.write_text(
                "# License Plate Information - User Notes\n"
                "# ==========================================\n"
                "# Use this file to record any missing information,\n"
                "# corrections, or suggestions for the app.\n"
                "# You can send this file to the developer for updates.\n"
                "#\n"
                "# Format suggestions:\n"
                "# - State: [STATE CODE]\n"
                "# - Issue: [Description of missing/incorrect info]\n"
                "# - Suggested fix: [What should be added/changed]\n"
                "# ==========================================\n\n",
                encoding='utf-8'
            )
        
        # Open folder and select file
        folder = str(notes_file.parent)
        if os.name == 'nt':  # Windows
            subprocess.run(['explorer', '/select,', str(notes_file)])
        else:
            subprocess.run(['xdg-open', folder])
        
        self.status_bar.showMessage(f"Notes file: {notes_file}", 3000)
    
    def _on_show_help(self, topic: str, section: Optional[str] = None):
        """Show help dialog with specified topic."""
        from ui.dialogs.help_dialog import HelpDialog
        dialog = HelpDialog(self, topic, section)
        dialog.exec()
    
    def _on_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About License Plate Info",
            "License Plate Information System\n\n"
            "Version 1.0.0\n\n"
            "A tool for quick license plate information lookup\n"
            "during toll processing workflows."
        )
    
    # ==================== Search Handlers ====================
    
    def _on_search_text_changed(self, text: str):
        """Handle search input text changes."""
        self.search_clear_btn.setVisible(bool(text))
        
        # Deselect current state when starting to search
        if text.strip() and self.current_state:
            if self.current_state in self.state_buttons:
                self.state_buttons[self.current_state].set_selected(False)
            self.current_state = None
        
        if not text.strip():
            self.search_controller.clear_search()
            return
        
        # Get current filter values
        state_filter = self.state_filter_combo.currentData()
        category = self.category_combo.currentData() or 'all'
        
        # Trigger debounced search
        self.search_controller.search(text, category, state_filter)
    
    def _on_search_enter(self):
        """Handle Enter key in search input - immediate search."""
        text = self.search_input.text().strip()
        if text:
            state_filter = self.state_filter_combo.currentData()
            category = self.category_combo.currentData() or 'all'
            self.search_controller.search(text, category, state_filter, immediate=True)
    
    def _on_clear_search(self):
        """Clear the search input and results."""
        self.search_input.clear()
        self.search_controller.clear_search()
    
    def _on_filter_changed(self):
        """Handle state or category filter change."""
        text = self.search_input.text().strip()
        if text:
            state_filter = self.state_filter_combo.currentData()
            category = self.category_combo.currentData() or 'all'
            self.search_controller.search(text, category, state_filter, immediate=True)
    
    def _on_search_completed(self, results: CategorizedResults):
        """Handle search results from controller."""
        self.is_search_mode = True
        self._last_search_results = results  # Store for export
        
        # Update result count label
        self.search_result_label.setText(
            f"Found {results.total_count} results in {results.state_count} states"
        )
        
        # Update status bar
        category_name = SearchController.CATEGORIES.get(results.category, results.category)
        self.status_bar.showMessage(
            f"Search: '{results.query}' - {results.total_count} results | Category: {category_name}"
        )
        
        # Update all panels with search results
        self._update_panels_with_search_results(results)
    
    def _on_search_cleared(self):
        """Handle search cleared - return to state mode."""
        self.is_search_mode = False
        self.search_result_label.setText("")
        
        # Hide result lists, show static content
        self.state_results_list.setVisible(False)
        self.state_info_content.setVisible(True)
        self.state_info_header.setText("State Information")
        self.state_info_content.setText("Select a state or search to see information.")
        
        self.char_rules_list.setVisible(False)
        self.char_rules_content.setVisible(True)
        self.char_rules_header.setText("Character Rules")
        self.char_rules_content.setText("Select a state or search to see character rules.")
        
        self.plate_type_list.setVisible(False)
        self.plate_type_content.setVisible(True)
        self.plate_type_header.setText("Plate Type Information")
        self.plate_type_content.setText("Select a state or search to see plate types.")
        
        self.status_bar.showMessage("Ready")
    
    def _on_search_error(self, error_message: str):
        """Handle search error."""
        self.status_bar.showMessage(f"Search error: {error_message}", 5000)
        self.search_result_label.setText(f"Error: {error_message}")
    
    def _update_panels_with_search_results(self, results: CategorizedResults):
        """Update all panels with categorized search results."""
        
        # ===== State Info Panel =====
        self.state_info_content.setVisible(False)
        self.state_results_list.setVisible(True)
        self.state_results_list.clear()
        self.state_info_header.setText(f"State Matches ({len(results.state_results)})")
        
        for result in results.state_results:
            item = QListWidgetItem(f"{result.state_code} - {result.state_name}")
            item.setToolTip(f"Field: {result.field}\nValue: {result.value}")
            item.setData(Qt.ItemDataRole.UserRole, result.state_code)
            self.state_results_list.addItem(item)
            
            # Add sub-item showing the match
            match_item = QListWidgetItem(f"    {result.field}: {result.value[:50]}...")
            match_item.setData(Qt.ItemDataRole.UserRole, result.state_code)
            match_item.setForeground(Qt.GlobalColor.gray)
            self.state_results_list.addItem(match_item)
        
        # ===== Character Rules Panel =====
        self.char_rules_content.setVisible(False)
        self.char_rules_list.setVisible(True)
        self.char_rules_list.clear()
        self.char_rules_header.setText(f"Character Rules Matches ({len(results.char_rules_results)})")
        
        for result in results.char_rules_results:
            item = QListWidgetItem(f"{result.state_code}: {result.field}")
            item.setToolTip(f"Value: {result.value}")
            item.setData(Qt.ItemDataRole.UserRole, result.state_code)
            self.char_rules_list.addItem(item)
            
            # Add value sub-item
            value_item = QListWidgetItem(f"    → {result.value[:60]}")
            value_item.setData(Qt.ItemDataRole.UserRole, result.state_code)
            value_item.setForeground(Qt.GlobalColor.gray)
            self.char_rules_list.addItem(value_item)
        
        if not results.char_rules_results:
            self.char_rules_list.addItem(QListWidgetItem("No character rule matches"))
        
        # ===== Plate Type Panel =====
        self.plate_type_content.setVisible(False)
        self.plate_type_list.setVisible(True)
        self.plate_type_list.clear()
        self.plate_type_header.setText(f"Plate Type Matches ({len(results.plate_type_results)})")
        
        for result in results.plate_type_results:
            plate_name = result.plate_type or result.field
            item = QListWidgetItem(f"{result.state_code}: {plate_name}")
            item.setToolTip(f"Value: {result.value}")
            item.setData(Qt.ItemDataRole.UserRole, result.state_code)
            self.plate_type_list.addItem(item)
            
            # Add value sub-item
            value_item = QListWidgetItem(f"    → {result.value[:60]}")
            value_item.setData(Qt.ItemDataRole.UserRole, result.state_code)
            value_item.setForeground(Qt.GlobalColor.gray)
            self.plate_type_list.addItem(value_item)
        
        if not results.plate_type_results:
            self.plate_type_list.addItem(QListWidgetItem("No plate type matches"))
    
    def _on_state_result_clicked(self, item: QListWidgetItem):
        """Handle click on a state search result."""
        state_code = item.data(Qt.ItemDataRole.UserRole)
        if state_code:
            # Select this state (will clear search and update all panels)
            self._select_state(state_code)
    
    def _on_char_rule_result_clicked(self, item: QListWidgetItem):
        """Handle click on a character rule search result."""
        state_code = item.data(Qt.ItemDataRole.UserRole)
        if state_code:
            # Select this state
            self._select_state(state_code)
    
    def _on_plate_type_result_clicked(self, item: QListWidgetItem):
        """Handle click on a plate type search result."""
        state_code = item.data(Qt.ItemDataRole.UserRole)
        if state_code:
            # Select this state
            self._select_state(state_code)
    
    def _on_plate_type_changed(self, index: int):
        """Handle plate type dropdown change."""
        plate_type = self.plate_type_combo.currentData()
        if not plate_type:
            return
        
        # Try to show the corresponding image
        if plate_type != "standard":
            found = self.image_panel.show_plate_type(plate_type)
            if found:
                self.status_bar.showMessage(f"Showing: {plate_type}", 2000)
            else:
                self.status_bar.showMessage(f"No image found for: {plate_type}", 2000)
        else:
            # For standard, just show first image
            self.image_panel.show_plate_type("standard")
            self.status_bar.showMessage("Showing standard plate", 2000)
        
        # Emit signal
        self.plate_type_selected.emit(plate_type)


def main():
    """Application entry point."""
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    app.setApplicationName("License Plate Info")
    app.setOrganizationName("LicensePlateInfo")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
