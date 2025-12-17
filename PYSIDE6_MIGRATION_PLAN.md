# PySide6 Migration Plan

## Overview
Migrate from Tkinter to PySide6 for improved DPI scaling, professional menus, and modern UI.

---

## Target Architecture

### Two Modes of Operation

**1. State Selection Mode** (default)
- Click a state → All panels show info for that state
- Traditional browsing experience

**2. Search Mode** (when search has text)
- Type in search → All panels update with matching results
- Panels show aggregated search results, not single-state info
- Click a result → switches to State Selection Mode for that state

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│ Menu Bar: File | View | Mode | Tools | Help                          [V3 Mode ▼]   │
├──────────────┬──────────────────────────────────────┬───────────────────────────────┤
│              │                                      │                               │
│ State Panel  │      Search Results / State Info     │    Character Rules Results    │
│ (Left)       │      (Center-Left)                   │    (Right)                    │
│              │                                      │                               │
│ ┌──────────┐ │  ┌─────────────────────────────────┐ │  ┌─────────────────────────┐  │
│ │🔍 Search │ │  │ Showing results for: "lincoln"  │ │  │ Character Rules Matches │  │
│ │[lincoln ]│ │  └─────────────────────────────────┘ │  │                         │  │
│ └──────────┘ │                                      │  │ IL: Uses 0 for O ✓      │  │
│ ┌──────────┐ │  STATE MATCHES (3):                  │  │ NE: Uses 0 for O ✓      │  │
│ │State: All│ │  ┌─────────────────────────────────┐ │  │ KY: Allows O ✓          │  │
│ └──────────┘ │  │ IL - Illinois                   │ │  │                         │  │
│ ┌──────────┐ │  │   Slogan: "Land of Lincoln"    ▶│ │  └─────────────────────────┘  │
│ │Category: │ │  ├─────────────────────────────────┤ │                               │
│ │[All     ]│ │  │ NE - Nebraska                   │ │  ┌─────────────────────────┐  │
│ └──────────┘ │  │   Plate: "Lincoln Heritage"    ▶│ │  │ Font Preview            │  │
│ ──────────── │  ├─────────────────────────────────┤ │  │ (for selected result)   │  │
│ Mode: V3     │  │ KY - Kentucky                   │ │  │ A B C 0 1 2 3           │  │
│ ┌──────────┐ │  │   Plate: "Lincoln Birthplace" ▶│ │  └─────────────────────────┘  │
│ │ FL ★     │ │  └─────────────────────────────────┘ │                               │
│ │ ──────── │ ├──────────────────────────────────────┼───────────────────────────────┤
│ │ GA  SC   │ │                                      │                               │
│ │ AL  NC   │ │      Plate Type Results              │    Image Results              │
│ │ ──────── │ │      (Center-Left Bottom)            │    (Right Bottom)             │
│ │ All States│ │                                      │                               │
│ └──────────┘ │  PLATE TYPE MATCHES (3):             │  ┌─────────────────────────┐  │
│              │  ┌─────────────────────────────────┐ │  │ Images for matched      │  │
│ ┌──────────┐ │  │ IL: Lincoln Heritage            │ │  │ states/plate types      │  │
│ │ Plate    │ │  │   Pattern: ABC-1234            ▶│ │  │                         │  │
│ │ Type ▼   │ │  ├─────────────────────────────────┤ │  │  [IL]  [NE]  [KY]       │  │
│ └──────────┘ │  │ KY: Lincoln Birthplace          │ │  │                         │  │
│              │  │   Special plate design         ▶│ │  └─────────────────────────┘  │
│              │  └─────────────────────────────────┘ │                               │
├──────────────┴──────────────────────────────────────┴───────────────────────────────┤
│ Status: Search: 3 states, 3 plate types │ Mode: V3 │ Category: All                  │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

**Key Design:** Search is PRIMARY - always visible, drives all panel content when active.

---

## Search-Driven Interface

### Search Controls (Always Visible in State Panel)
```
┌─────────────────────────────┐
│ 🔍 SEARCH                   │
│ ┌─────────────────────────┐ │
│ │ lincoln              [x]│ │  ← Clear button
│ └─────────────────────────┘ │
│                             │
│ State: [All States      ▼]  │  ← Filter to specific state
│                             │
│ Category: [All Fields   ▼]  │  ← Filter to specific field type
│   • All Fields              │
│   • Slogans                 │
│   • Plate Types             │
│   • Fonts                   │
│   • Colors                  │
│   • Character Rules         │
│   • Processing Rules        │
└─────────────────────────────┘
```

### Search Behavior
1. **Empty search** → Panels show selected state info (normal mode)
2. **Typing search** → After 300ms debounce, search executes
3. **Results found** → All 4 panels update to show categorized results
4. **Click result** → Clears search, selects that state/plate type
5. **Low result count** → Updates live as you type (< 50 results)
6. **High result count** → Shows "Press Enter to search" or debounce

### Panel Content in Search Mode

| Panel | Shows |
|-------|-------|
| State Info | List of matching states with matched field highlighted |
| Plate Type | List of matching plate types across all states |
| Character Rules | Matching character/handling rules |
| Images | Thumbnail grid of plates from matching states |

---

## Queue Mode System

### Mode Definitions
```python
QUEUE_MODES = {
    "V3": {
        "description": "Florida primary, common out-of-state",
        "primary": ["FL"],
        "secondary": ["GA", "AL", "SC", "NC", "TN", "MS", "LA", "TX"],  # Common I-95/I-10 corridor
        "show_all": True  # Can still access any state
    },
    "Express": {
        "description": "Florida primary, common out-of-state", 
        "primary": ["FL"],
        "secondary": ["GA", "AL", "SC", "NC", "TN", "MS", "LA", "TX"],
        "show_all": True
    },
    "I95": {
        "description": "Florida primary, I-95 corridor states",
        "primary": ["FL"],
        "secondary": ["GA", "SC", "NC", "VA", "MD", "DE", "NJ", "NY", "CT", "MA"],
        "show_all": True
    },
    "OOSV3": {
        "description": "Out-of-state plates (excludes FL and Plate Type states)",
        "primary": [],  # No primary
        "excluded": ["FL", "MA", "ME", "OH", "IN", "IL"],  # FL + Plate Type states
        "secondary": ["GA", "AL", "SC", "NC", ...],  # All other states
        "show_all": True
    },
    "PlateType": {
        "description": "Plate Type queue states (excludes Florida)",
        "primary": ["MA", "ME", "OH", "IN", "IL"],  # Plate Type states (not FL)
        "excluded": ["FL"],
        "show_all": True
    },
    "All": {
        "description": "All states equally weighted",
        "primary": [],
        "secondary": [],
        "show_all": True
    }
}
```

### Mode UI Behavior

**State Panel Layout by Mode:**
```
┌─────────────────────────────┐
│ Mode: [V3           ▼]      │  ← Dropdown in toolbar AND state panel
├─────────────────────────────┤
│ ★ PRIMARY                   │  ← Large, prominent button
│ ┌─────────────────────────┐ │
│ │         FL              │ │  ← Extra large for V3/Express/I95
│ └─────────────────────────┘ │
├─────────────────────────────┤
│ FREQUENT                    │  ← Secondary states, medium buttons
│ ┌─────┬─────┬─────┬─────┐   │
│ │ GA  │ SC  │ AL  │ NC  │   │
│ ├─────┼─────┼─────┼─────┤   │
│ │ TN  │ MS  │ LA  │ TX  │   │
│ └─────┴─────┴─────┴─────┘   │
├─────────────────────────────┤
│ ▼ ALL STATES                │  ← Collapsible, full grid
│ ┌───┬───┬───┬───┬───┬───┐   │
│ │AK │AZ │AR │CA │CO │CT │   │
│ │...                    │   │
│ └───┴───┴───┴───┴───┴───┘   │
└─────────────────────────────┘
```

**OOSV3 Mode Layout:**
```
┌─────────────────────────────┐
│ Mode: [OOSV3        ▼]      │
├─────────────────────────────┤
│ OUT-OF-STATE (excl. FL)     │
│ ┌─────┬─────┬─────┬─────┐   │
│ │ GA  │ SC  │ AL  │ NC  │   │
│ ├─────┼─────┼─────┼─────┤   │
│ │ TN  │ MS  │ VA  │ OH  │   │
│ └─────┴─────┴─────┴─────┘   │
├─────────────────────────────┤
│ ▼ ALL STATES (incl. FL)     │  ← Still accessible!
└─────────────────────────────┘
```

### Mode Features
1. **Quick Switch**: Dropdown in toolbar + keyboard shortcut (Ctrl+M)
2. **Visual Priority**: Primary states are larger/highlighted
3. **Always Accessible**: "All States" section always available (collapsible)
4. **Persistent**: Remembers last mode on restart
5. **Customizable**: Users can edit mode definitions in settings (future)

---

## File Structure

```
src/
├── ui/                          # NEW - PySide6 UI layer
│   ├── __init__.py
│   ├── main_window.py           # QMainWindow - app shell
│   ├── resources/
│   │   ├── icons/               # SVG icons for toolbar/menu
│   │   ├── styles/
│   │   │   └── dark_theme.qss   # Qt stylesheet
│   │   └── help/
│   │       ├── user_guide.md
│   │       ├── shortcuts.md
│   │       ├── emergency_vehicles.md
│   │       └── plate_reading_tips.md
│   ├── widgets/                 # Reusable custom widgets
│   │   ├── __init__.py
│   │   ├── state_button.py      # Styled state code button
│   │   ├── search_widget.py     # Search input with dropdown
│   │   ├── image_viewer.py      # Plate image viewer with nav
│   │   ├── info_card.py         # Styled info display card
│   │   └── font_preview.py      # Character font preview widget
│   ├── panels/                  # Main content panels
│   │   ├── __init__.py
│   │   ├── state_panel.py       # Left sidebar - state grid + mode
│   │   ├── state_info_panel.py  # State details (top center-left)
│   │   ├── plate_type_panel.py  # Plate type info (bottom center-left)
│   │   ├── char_rules_panel.py  # Character rules + font preview (top right)
│   │   ├── image_panel.py       # Images (bottom right)
│   │   └── search_panel.py      # Global search panel (in state panel or dialog)
│   ├── dialogs/                 # Modal dialogs
│   │   ├── __init__.py
│   │   ├── help_dialog.py       # Help browser window
│   │   ├── search_dialog.py     # Global search dialog (Ctrl+F)
│   │   ├── settings_dialog.py   # App settings (incl. mode config)
│   │   └── about_dialog.py      # About window
│   └── controllers/             # Business logic separation
│       ├── __init__.py
│       ├── state_controller.py  # State selection logic
│       ├── mode_controller.py   # Queue mode management
│       ├── search_controller.py # Search handling (wraps JSONSearchEngine)
│       └── image_controller.py  # Image loading/caching
├── config/
│   └── queue_modes.json         # User-editable mode definitions
├── database/                    # KEEP - No changes needed
├── models/                      # KEEP - No changes needed
├── utils/                       # KEEP - Minor updates
├── gui/
│   └── utils/
│       └── json_search_engine.py  # REUSE - Already implemented!
└── gui/                         # DEPRECATE after migration (except search engine)
```

---

## Menu Structure

### File Menu
```
File
├── Export State Data...        Ctrl+E
├── Export Search Results...
├── ─────────────────────
├── Settings                    Ctrl+,
├── ─────────────────────
└── Exit                        Alt+F4
```

### View Menu
```
View
├── Toggle State Panel          Ctrl+1
├── Toggle Quick Info Bar       Ctrl+2
├── ─────────────────────
├── Expand All Panels           
├── Collapse All Panels
├── ─────────────────────
├── Zoom In                     Ctrl++
├── Zoom Out                    Ctrl+-
├── Reset Zoom                  Ctrl+0
├── ─────────────────────
├── Full Screen                 F11
└── Reset Layout
```

### Mode Menu
```
Mode
├── V3                          Ctrl+Shift+1
├── Express                     Ctrl+Shift+2
├── I95                         Ctrl+Shift+3
├── OOSV3                       Ctrl+Shift+4
├── Plate Type                  Ctrl+Shift+5
├── All States                  Ctrl+Shift+0
├── ─────────────────────
└── Configure Modes...
```

### Tools Menu
```
Tools
├── Search All States           Ctrl+F
├── Jump to State...            Ctrl+G
├── ─────────────────────
├── Refresh Database            F5
└── Clear Search History
```

### Help Menu
```
Help
├── User Guide                  F1
├── Keyboard Shortcuts          Ctrl+/
├── ─────────────────────
├── Plate Reading Tips
│   ├── Obscured/Partial Plates
│   ├── Damaged Characters
│   └── Stacked Characters
├── Emergency Vehicle Guide
├── Character Recognition (O vs 0)
├── ─────────────────────
├── Check for Updates
└── About License Plate Info
```

---

## Layout Specifications

### Panel Grid (QSplitter-based)
```
┌──────────────────────────────────────────────────────────────┐
│                        Main Window                           │
│  ┌─────────┬────────────────────────────────────────────┐   │
│  │         │  ┌─────────────────┬─────────────────────┐ │   │
│  │  State  │  │  State Info     │  Character Rules    │ │   │
│  │  Panel  │  │  Panel          │  Panel              │ │   │
│  │         │  │                 │                     │ │   │
│  │  250px  │  ├─────────────────┼─────────────────────┤ │   │
│  │  fixed  │  │  Plate Type     │  Image Panel        │ │   │
│  │  min    │  │  Panel          │                     │ │   │
│  │         │  │                 │                     │ │   │
│  │         │  └─────────────────┴─────────────────────┘ │   │
│  └─────────┴────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

### Splitter Properties
- **Horizontal Main**: State Panel | Content Area (draggable)
- **Vertical Content**: Top Row | Bottom Row (draggable)
- **Horizontal Top**: State Info | Char Rules (draggable)
- **Horizontal Bottom**: Plate Type | Images (draggable)
- **All positions saved** on close, restored on open

---

## Component Specifications

### 1. Main Window (`main_window.py`)
```python
class MainWindow(QMainWindow):
    # Responsibilities:
    # - Menu bar setup
    # - Mode selector in toolbar
    # - Splitter-based central widget
    # - Status bar
    # - Window state persistence
    # - Global keyboard shortcuts
    
    # Signals:
    mode_changed = Signal(str)
    state_selected = Signal(str)
    plate_type_selected = Signal(str)
```

### 2. State Panel (`state_panel.py`)
```python
class StatePanel(QWidget):
    # Signals:
    state_selected = Signal(str)
    
    # Sections:
    # - Mode dropdown
    # - Search input
    # - Primary states (mode-dependent)
    # - Frequent states (mode-dependent)
    # - All states (collapsible)
    # - Plate type dropdown
    
    def set_mode(self, mode_name: str):
        """Reorganize state buttons based on mode"""
        
    def highlight_state(self, state_code: str):
        """Visual feedback for selected state"""
```

### 3. Info Panels (All Similar Structure)
```python
class InfoPanel(QScrollArea):
    """Base class for info display panels"""
    
    # Features:
    # - Scrollable content
    # - Collapsible sections
    # - Copy buttons for key fields
    # - Visual hierarchy with headers
    
    def update_content(self, data: dict):
        """Refresh display with new data"""
        
    def clear(self):
        """Reset to empty state"""
```

### 4. Mode Controller (`mode_controller.py`)
```python
class ModeController(QObject):
    mode_changed = Signal(str, dict)  # mode_name, mode_config
    
    def __init__(self):
        self.modes = self._load_modes()
        self.current_mode = "V3"  # Default
    
    def _load_modes(self) -> dict:
        """Load from config/queue_modes.json"""
        
    def set_mode(self, mode_name: str):
        """Switch active mode"""
        
    def get_primary_states(self) -> list:
        """Get primary states for current mode"""
        
    def get_secondary_states(self) -> list:
        """Get secondary/frequent states"""
        
    def is_state_excluded(self, state_code: str) -> bool:
        """Check if state is excluded in current mode"""
```

---

## Styling (Dark Theme)

### Color Palette
```css
/* dark_theme.qss */
$bg-primary: #1e1e1e;      /* Main background */
$bg-secondary: #2d2d2d;    /* Cards, panels */
$bg-tertiary: #3c3c3c;     /* Hover states */
$accent: #4CAF50;          /* Green accent (selected state) */
$accent-hover: #66BB6A;
$primary-highlight: #FF9800; /* Orange - primary state in mode */
$text-primary: #ffffff;
$text-secondary: #b0b0b0;
$border: #404040;
```

### State Button Styles by Mode
```css
/* Primary state (e.g., FL in V3 mode) */
QPushButton.state-primary {
    background-color: #FF9800;
    font-size: 18px;
    min-height: 50px;
    font-weight: bold;
}

/* Secondary/frequent state */
QPushButton.state-secondary {
    background-color: #2d2d2d;
    font-size: 12px;
    min-height: 35px;
}

/* All other states */
QPushButton.state-normal {
    background-color: #252525;
    font-size: 10px;
    min-height: 28px;
}

/* Selected state (any category) */
QPushButton.state-selected {
    border: 2px solid #4CAF50;
    background-color: #3c3c3c;
}
```

---

## Keyboard Shortcuts

| Action | Shortcut | Description |
|--------|----------|-------------|
| Search | Ctrl+F | Focus search input |
| Jump to State | Ctrl+G | Open state jump dialog |
| Mode: V3 | Ctrl+Shift+1 | Switch to V3 mode |
| Mode: Express | Ctrl+Shift+2 | Switch to Express mode |
| Mode: I95 | Ctrl+Shift+3 | Switch to I95 mode |
| Mode: OOSV3 | Ctrl+Shift+4 | Switch to OOSV3 mode |
| Mode: Plate Type | Ctrl+Shift+5 | Switch to Plate Type mode |
| Mode: All | Ctrl+Shift+0 | Switch to All States mode |
| Next Image | Right Arrow | Next plate image |
| Prev Image | Left Arrow | Previous plate image |
| Toggle State Panel | Ctrl+1 | Show/hide state panel |
| Help | F1 | Open help dialog |
| Settings | Ctrl+, | Open settings |

---

## Migration Phases

### Phase 1: Foundation (3-4 days) ✅ COMPLETE
- [x] Add PySide6 to requirements.txt
- [x] Create `src/ui/` directory structure
- [x] Implement `MainWindow` shell with menu bar
- [x] Create dark theme stylesheet
- [x] Add help content markdown files
- [x] Implement `HelpDialog` with content browser
- [x] Create `config/queue_modes.json`
- [x] Implement `SearchController` wrapping `JSONSearchEngine`
- [x] Add search controls to state panel (search input, state filter, category filter)
- [x] Implement search-driven panel updates (all 4 panels show categorized results)

**Deliverable:** App launches with menu bar, help system, and search-driven interface working ✅

### Phase 2: Mode System + State Panel (3-4 days) ✅ COMPLETE
- [x] Add mode dropdown to toolbar
- [x] Add mode display in state panel
- [x] Implement `ModeController` class (separate file)
- [x] Create `StateButton` widget with category-based color coding
- [x] Implement `FlowLayout` for proper button wrapping at any screen size
- [x] State buttons organized by category (FL, plate_type, nearby, distant_major, territory, canadian, normal)
- [x] Click state button → selects state, updates panels
- [x] Toggle behavior - click selected state to deselect
- [x] Deselect state when starting new search
- [x] Search requires minimum 2 characters before executing
- [x] Implement `StateDataManager` for loading state JSON data
- [x] Implement `FontPreviewWidget` showing character grid with O/0 color coding

**Deliverable:** Can select modes, click states to see info, color-coded buttons work ✅

### Phase 3: Content Panels (4-5 days) ✅ COMPLETE
- [x] Implement basic panel shells with splitter layout
- [x] Panels show search results when searching
- [x] FontPreviewWidget updates with state font data and O/0 coloring
- [x] Click search result → clear search, show state info
- [x] Click state button → load and display state info in all panels
- [x] StateInfoPanel shows: name, slogan, colors, font, notes
- [x] CharRulesPanel shows: O/0 rules, stacked chars, restrictions
- [x] PlateTypePanel shows: list of plate types
- [x] Implement `ImagePanel` with viewer and navigation (prev/next, keyboard arrows)
- [x] Image category filter (All, Standard, Specialty, Government, Characters)
- [x] Plate type dropdown population from state data
- [x] Plate type selection shows corresponding image in ImagePanel

**Deliverable:** Full content display working, all panels visible ✅

### Phase 4: Polish & Refinement (2-3 days) ✅ COMPLETE
- [x] Add all keyboard shortcuts (Ctrl+F search, Ctrl+G jump, mode shortcuts Ctrl+Shift+1-5/0, Escape clear)
- [x] Window state persistence (size, splitters, mode)
- [x] Error handling and user feedback (throughout controllers and export functions)
- [x] Zoom in/out for images (+/- buttons, Ctrl+=/-, Ctrl+0 reset)
- [x] Export functionality (Export State Data Ctrl+E, Export Search Results)
- [x] Image panel responsive layout (split controls into nav row + zoom row)

**Deliverable:** Feature-complete application ✅

### Phase 5: Testing & Cleanup (2-3 days)
- [ ] Update/add tests for new UI components
- [ ] Remove old Tkinter code (keep json_search_engine.py)
- [ ] Update build scripts
- [ ] Documentation updates
- [ ] Performance testing

**Deliverable:** Production-ready release

---

## New Components Added

### `FlowLayout` (`ui/widgets/flow_layout.py`)
A custom layout that flows widgets left-to-right, wrapping to new rows automatically.
- Never stretches widgets beyond their preferred size
- Works consistently at any screen size/DPI
- Based on Qt's official FlowLayout example

### `StateButton` Categories
Color-coded buttons by category for visual organization:
- 🟠 **florida** (#FF9800) - FL only
- 🟣 **plate_type** (#7B1FA2) - MA, ME, OH, IN, IL
- 🔵 **nearby** (#1565C0) - GA, AL, SC, NC, TN, MS, LA
- 🔷 **distant_major** (#00838F) - CA, TX, NY, PA, NJ, WA, AZ, CO, VA, MD
- 🟤 **territory** (#5D4037) - PR, GU, VI, AS, MP, DC
- 🔴 **canadian** (#C62828) - Canadian provinces
- ⬛ **normal** (#424242) - All other US states

---

## Queue Mode Configuration File

### `config/queue_modes.json`
```json
{
  "modes": {
    "V3": {
      "description": "Florida primary, common out-of-state",
      "primary": ["FL"],
      "secondary": ["GA", "AL", "SC", "NC", "TN", "MS", "LA", "TX"],
      "excluded": [],
      "show_all_states": true
    },
    "Express": {
      "description": "Florida primary, common out-of-state",
      "primary": ["FL"],
      "secondary": ["GA", "AL", "SC", "NC", "TN", "MS", "LA", "TX"],
      "excluded": [],
      "show_all_states": true
    },
    "I95": {
      "description": "Florida primary, I-95 corridor",
      "primary": ["FL"],
      "secondary": ["GA", "SC", "NC", "VA", "MD", "DE", "NJ", "NY", "CT", "MA", "RI", "NH", "ME"],
      "excluded": [],
      "show_all_states": true
    },
    "OOSV3": {
      "description": "Out-of-state (excludes FL and Plate Type states)",
      "primary": [],
      "secondary": ["GA", "AL", "SC", "NC", "TN", "MS", "LA", "AR", "OK", "KS", "MO", "KY", "WV", "VA", "MD", "DE", "NJ", "NY", "PA", "CT", "RI", "NH", "VT", "MI", "WI", "MN", "IA", "NE", "SD", "ND", "MT", "WY", "CO", "NM", "AZ", "UT", "NV", "ID", "OR", "WA", "CA", "TX", "AK", "HI"],
      "excluded": ["FL", "MA", "ME", "OH", "IN", "IL"],
      "show_all_states": true
    },
    "PlateType": {
      "description": "Plate Type queue states (MA, ME, OH, IN, IL)",
      "primary": ["MA", "ME", "OH", "IN", "IL"],
      "secondary": [],
      "excluded": ["FL"],
      "show_all_states": true
    },
    "All": {
      "description": "All states equally",
      "primary": [],
      "secondary": [],
      "excluded": [],
      "show_all_states": true
    }
  },
  "default_mode": "V3"
}
```

---

## Success Criteria

1. **Scaling**: App looks correct on 100%, 125%, 150%, 200% display scaling
2. **Speed**: State selection updates all panels in <100ms
3. **All-at-once**: All 4 info panels visible without clicking/scrolling
4. **Mode switching**: Mode change reorganizes state panel in <50ms
5. **Menus**: All menu items functional with keyboard shortcuts
6. **Help**: All help content accessible and searchable
7. **Tests**: 90%+ of existing tests pass with minimal changes

---

## Estimated Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Foundation | 3-4 days | 4 days |
| Phase 2: Mode + State Panel | 3-4 days | 8 days |
| Phase 3: Content Panels | 4-5 days | 13 days |
| Phase 4: Search & Polish | 2-3 days | 16 days |
| Phase 5: Testing & Cleanup | 2-3 days | 19 days |

**Total: ~3-4 weeks**

---

## Next Steps

1. **Approve this plan** or request modifications
2. **Define exact states** for each mode (especially OOSV3 and PlateType exclusions)
3. **Install PySide6**: `pip install PySide6`
4. **Start Phase 1**: Create main window shell with menus
