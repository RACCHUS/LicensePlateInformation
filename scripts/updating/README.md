# Updating Scripts

This folder contains scripts for updating various components of the License Plate Information System.

## Scripts

### `update_plate_type_dropdown.py`
**Purpose**: Updates the GUI dropdown component with all plate types from state JSON files.

**Main Command**:
```bash
python scripts/updating/update_plate_type_dropdown.py extract
```

**When to Run**:
- After adding new states
- After adding new plate types to existing states  
- After updating plate type names or descriptions
- After making any changes to `plate_types` sections in JSON files

**Other Commands**:
- `list` - Show current plate types
- `stats` - Show statistics  
- `add "Type"` - Manually add a plate type
- `remove "Type"` - Remove a plate type

**Output**: Updates the dropdown data file that the GUI components use to populate plate type selections.

---

## Usage Workflow

1. Make changes to state JSON files (add states, update plate types, etc.)
2. Run `python scripts/updating/update_plate_type_dropdown.py extract`
3. The GUI dropdown will now include all the latest plate types
4. Test the application to verify updates

## Future Scripts

Additional updating scripts will be added here as needed for other components.