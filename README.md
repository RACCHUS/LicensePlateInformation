# License Plate Information System

A desktop application for quickly identifying license plate details for toll reading, optimized for Florida with support for out-of-state plates.

## Features

- **Modern PySide6 UI**: High DPI scaling support, professional appearance
- **Fast State Lookup**: Quickly find state-specific plate information
- **Search-Driven Interface**: Type to search across all states and plate types
- **Character Disambiguation**: Identify whether plates use 0 vs O, and other ambiguous characters  
- **Plate Type Support**: Handle different plate types (passenger, commercial, specialty, etc.)
- **Visual References**: Support for plate images, logos, and character examples
- **Queue Mode System**: Optimized for V3, Express, I95, OOSV3, and PlateType workflows
- **Keyboard Shortcuts**: Efficient navigation with Ctrl+F (search), arrow keys, mode shortcuts
- **Offline Operation**: No internet required - all data stored locally
- **Easy Data Management**: Simple structure for adding new states, plate types, and images

## Quick Start

1. Install Python 3.10+ if not already installed
2. Install required packages: `pip install -r requirements.txt`
3. Run the application: `python main_pyside.py`

## Usage

### Main Interface
- **Search**: Type in the search bar (Ctrl+F) to find states, plate types, or character rules
- **State Selection**: Click state buttons (color-coded by category) or use Ctrl+G to jump
- **Queue Modes**: Switch modes with Ctrl+Shift+1-5 or the mode dropdown
- **Image Navigation**: Use arrow keys or buttons to browse plate images
- **Export**: Export state data (Ctrl+E) or search results to JSON/TXT

### Keyboard Shortcuts
| Action | Shortcut |
|--------|----------|
| Focus Search | Ctrl+F |
| Jump to State | Ctrl+G |
| Mode: V3 | Ctrl+Shift+1 |
| Mode: Express | Ctrl+Shift+2 |
| Mode: I95 | Ctrl+Shift+3 |
| Mode: OOSV3 | Ctrl+Shift+4 |
| Mode: PlateType | Ctrl+Shift+5 |
| Mode: All | Ctrl+Shift+0 |
| Next Image | Right Arrow |
| Previous Image | Left Arrow |
| Zoom In | Ctrl++ |
| Zoom Out | Ctrl+- |
| Clear/Close | Escape |
| Export State | Ctrl+E |
| Help | F1 |

### Adding Data
- **Images**: Place in `data/images/[state]/` folders
- **State Data**: Edit JSON files in `data/states/` 
- **Database**: Automatic SQLite database creation and updates

## Building

### Development Run
```bash
python main.py
```

### Build Executable (PySide6)
```bash
build_pyside.bat
```
Output will be in `dist/LicensePlateInfo/`

## Testing

The project includes comprehensive test suites for all states and functionality:

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run UI controller tests
python -m pytest tests/unit/ui -v

# Run specific test suite
python run_tests.py georgia_comprehensive
python run_tests.py florida_comprehensive 
python run_tests.py tennessee_comprehensive
python run_tests.py state_comparison
```

### Test Organization

- `tests/test_all.py` - Core system tests (database, helpers, integration)
- `tests/test_georgia_comprehensive.py` - Complete Georgia license plate validation
- `tests/test_florida_comprehensive.py` - Complete Florida license plate validation
- `tests/test_tennessee_comprehensive.py` - Complete Tennessee license plate validation
- `tests/test_state_comparison.py` - Cross-state validation and comparison tests
- `tests/test_tennessee_recognition.py` - Tennessee pattern recognition tests
- `tests/unit/ui/controllers/` - UI controller unit tests (ModeController, SearchController, StateDataManager)
- `tests/unit/ui/widgets/` - UI widget unit tests (StateButton, FlowLayout)

All test files use research-backed data from Wikipedia and LicensePlates.cc to ensure accuracy.

## File Structure

```
LicensePlateInformation/
├── main.py                 # Application entry point (PySide6)
├── main.py                 # Legacy entry point
├── run_tests.py           # Test runner utility
├── requirements.txt        # Python dependencies
├── build_pyside.bat       # Build script for PySide6 executable
├── README.md              # This file
├── src/                   # Source code
│   ├── database/          # Database management
│   ├── gui/              # Legacy UI (Tkinter)
│   ├── ui/               # Modern UI (PySide6)
│   │   ├── controllers/  # Application logic controllers
│   │   ├── panels/       # Content panels
│   │   ├── widgets/      # Reusable UI components
│   │   └── main_window.py # Main application window
│   ├── models/           # Data models
│   └── utils/            # Utility functions
├── data/                 # Application data
│   ├── database/         # SQLite database
│   ├── images/           # Plate and character images
│   └── states/           # State configuration files
└── tests/                # Unit tests and validation suites
    ├── unit/ui/                       # UI component tests
    ├── test_all.py                    # Core system tests
    ├── test_georgia_comprehensive.py # Georgia validation (15 plate types)
    ├── test_florida_comprehensive.py # Florida validation (16 plate types)
    ├── test_tennessee_comprehensive.py # Tennessee validation (11 plate types)
    ├── test_state_comparison.py      # Cross-state comparison
    └── test_tennessee_recognition.py # Pattern recognition tests
```

## State Data Format

Each state has a JSON configuration file with:
- Basic info (name, abbreviation, slogan)
- Character rules (0/O usage, ambiguous characters)
- Plate types and formats
- Visual information (colors, logos)
- Image references

## Development

- **Database**: SQLite with automatic schema management
- **GUI**: Tkinter for native Windows performance
- **Data**: JSON configuration files for easy editing
- **Images**: Organized by state and type for quick access

## Toll Reading Optimization

Designed specifically for toll plaza usage:
- One-second state lookup
- Clear character disambiguation
- High-contrast visual references
- Keyboard shortcuts for efficiency
- Florida-centric with out-of-state support