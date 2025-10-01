# License Plate Information System

A desktop application for quickly identifying license plate details for toll reading, optimized for Florida with support for out-of-state plates.

## Features

- **Fast State Lookup**: Quickly find state-specific plate information
- **Character Disambiguation**: Identify whether plates use 0 vs O, and other ambiguous characters  
- **Plate Type Support**: Handle different plate types (passenger, commercial, specialty, etc.)
- **Visual References**: Support for plate images, logos, and character examples
- **Offline Operation**: No internet required - all data stored locally
- **Easy Data Management**: Simple structure for adding new states, plate types, and images

## Quick Start

1. Install Python 3.8+ if not already installed
2. Install required packages: `pip install -r requirements.txt`
3. Run the application: `python main.py`

## Usage

### Main Interface
- **State Search**: Type state name or abbreviation to quickly find information
- **Quick Info Panel**: Shows key details like 0/O usage, colors, logos
- **Plate Types**: Browse different plate formats for each state
- **Character Reference**: View state-specific character examples

### Adding Data
- **Images**: Place in `data/images/[state]/` folders
- **State Data**: Edit JSON files in `data/states/` 
- **Database**: Automatic SQLite database creation and updates

## Testing

The project includes comprehensive test suites for all states and functionality:

### Running Tests

```bash
# Run all tests
python run_tests.py

# Run specific test suite
python run_tests.py georgia_comprehensive
python run_tests.py florida_comprehensive 
python run_tests.py tennessee_comprehensive
python run_tests.py state_comparison

# Or use pytest directly
python -m pytest tests/ -v
```

### Test Organization

- `tests/test_all.py` - Core system tests (database, helpers, integration)
- `tests/test_georgia_comprehensive.py` - Complete Georgia license plate validation
- `tests/test_florida_comprehensive.py` - Complete Florida license plate validation
- `tests/test_tennessee_comprehensive.py` - Complete Tennessee license plate validation
- `tests/test_state_comparison.py` - Cross-state validation and comparison tests
- `tests/test_tennessee_recognition.py` - Tennessee pattern recognition tests

All test files use research-backed data from Wikipedia and LicensePlates.cc to ensure accuracy.

## File Structure

```
LicensePlateInformation/
├── main.py                 # Application entry point
├── run_tests.py           # Test runner utility
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── src/                   # Source code
│   ├── database/          # Database management
│   ├── gui/              # User interface
│   ├── models/           # Data models
│   └── utils/            # Utility functions
├── data/                 # Application data
│   ├── database/         # SQLite database
│   ├── images/           # Plate and character images
│   └── states/           # State configuration files
└── tests/                # Unit tests and validation suites
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