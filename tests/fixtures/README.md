# Test Fixtures Directory

This directory contains sample data and test fixtures used throughout the test suite.

## Files

- `sample_state.json` - Complete sample state data with all fields
- `sample_plate_types.json` - Array of sample plate type definitions
- `sample_images/` - Directory containing test images (created dynamically in tests)

## Usage

These fixtures are used by test functions to avoid hardcoding test data and to ensure consistency across tests.

Example:
```python
import json
from pathlib import Path

def load_fixture(filename):
    fixture_path = Path(__file__).parent / 'fixtures' / filename
    with open(fixture_path, 'r') as f:
        return json.load(f)
```
