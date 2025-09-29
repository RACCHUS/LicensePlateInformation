# License Plate Information System - User Guide

## Quick Start for Toll Operators

### Starting the Application
1. Double-click `main.py` or run `python main.py` from command line
2. The application will automatically create the database and load sample data
3. Search box is ready for immediate use

### Basic Usage

#### Fast State Lookup
- **Type state abbreviation**: `FL`, `GA`, `AL`, `SC`, `NC`
- **Type state name**: `Florida`, `Georgia`, etc.
- **Use quick buttons**: Click FL, GA, AL, SC, NC buttons for instant lookup

#### Reading the Information

**Left Panel - State Information:**
- **Uses 0 (zero)**: Does this state use digit 0 in plates?
- **Uses O (letter)**: Does this state use letter O in plates?  
- **Zero is slashed**: Does the zero have a slash through it?
- **Colors**: Primary plate colors for visual identification
- **Notes**: Important details specific to this state

**Middle Panel - Plate Types:**
- Shows different plate formats (Passenger, Commercial, Motorcycle, etc.)
- Pattern shows expected character layout (ABC-123, etc.)
- Stickers column indicates if validation stickers are present
- Click any row to see detailed information below

**Right Panel - Character Reference:**
- Click character buttons (0, O, 1, I, etc.) for disambiguation help
- Shows state-specific character information
- Explains which characters are commonly confused

### Common Toll Reading Scenarios

#### Scenario 1: Distinguishing 0 vs O
1. Search for the state (e.g., type "FL")
2. Check "Uses 0" and "Uses O" in left panel
3. For Florida: Uses 0 = Yes, Uses O = No
4. **Result**: If you see this character in a Florida plate, it's a zero (0)

#### Scenario 2: Georgia Plate with Slashed Character
1. Search "GA" 
2. Check "Zero is slashed" = Yes
3. Click "0" button in character reference
4. **Result**: Slashed character is zero (0), unslashed round character is letter O

#### Scenario 3: Identifying Plate Type
1. Search for state
2. Look at plate types in middle panel  
3. Match the pattern you see (ABC-123, 12A-34BC, etc.)
4. Check sticker information
5. **Result**: Know what validation stickers to expect

#### Scenario 4: Hard to Read Characters
1. Search for state
2. Click suspected character in right panel (1, I, L, 8, B, etc.)
3. Read state-specific guidance
4. **Result**: Make informed decision on character identification

### Keyboard Shortcuts
- **Enter**: Search and select first result
- **Escape**: Clear search and start over
- **F1**: Show help dialog
- **Tab**: Navigate between fields

### Quick Reference Card

**Florida (Primary State):**
- Uses: 0 (zero), NO letter O
- Zero: Not slashed
- Format: ABC-123D (most common)
- Stickers: Top-left registration

**Georgia (Common Out-of-State):**
- Uses: Both 0 and O
- Zero: Slashed (has line through it)
- Format: ABC-1234
- Stickers: County name at top

**Alabama:**
- Uses: Letter O, less common 0
- Zero: Not slashed
- Format: 12A-34BC
- Stickers: Usually no county sticker

### Tips for Fast Operation

1. **Memorize common state rules** for FL, GA, AL (most frequent)
2. **Use quick buttons** instead of typing for speed
3. **Focus on character rules** - most important for toll reading
4. **Learn plate patterns** to validate what you're seeing
5. **Check sticker locations** to confirm state identification

### Troubleshooting

**Problem**: No search results
- **Solution**: Check spelling, try abbreviation instead of full name

**Problem**: Multiple states found
- **Solution**: Be more specific or press Enter to select first match

**Problem**: Character still unclear
- **Solution**: Check multiple character references, use context of surrounding characters

**Problem**: Unusual plate format
- **Solution**: Check all plate types for that state, may be specialty or older format

### Adding New States/Data

1. Create JSON file in `data/states/` directory
2. Follow format of existing files (florida.json, georgia.json, etc.)
3. Restart application to reload data
4. Add images to `data/images/[STATE]/` folders

### Performance Notes

- Database is stored locally for fastest access
- All searches are instant (no network required)
- Application optimized for rapid repeated lookups
- Search history is tracked for analysis

---

## For System Administrators

### Installation Requirements
- Python 3.8 or higher
- Tkinter (usually included with Python)
- Pillow (PIL) for image handling: `pip install pillow`
- SQLite3 (included with Python)

### Database Location
- Default: `data/database/license_plates.db`
- Automatic backup recommended
- Can be copied between installations

### Customization
- State data: Edit JSON files in `data/states/`
- Images: Add to `data/images/[STATE]/` folders
- Colors/fonts: Modify `src/gui/main_window.py`

### Deployment
- Single folder deployment (copy entire directory)
- No registry changes required
- No administrator privileges needed
- Portable between Windows systems