# Tests Directory

This directory contains the complete test suite for the License Plate Information System.

## Structure

```
tests/
├── conftest.py                    # Shared fixtures and pytest configuration
├── fixtures/                      # Test data and sample files
│   ├── sample_state.json         # Sample state data
│   └── sample_plate_types.json   # Sample plate type definitions
├── unit/                          # Unit tests
│   ├── models/
│   │   └── test_plate_models.py  # Tests for State, PlateType, etc.
│   ├── utils/
│   │   ├── test_helpers.py       # Tests for utility functions
│   │   └── test_image_manager.py # Tests for image management
│   ├── database/
│   │   └── test_db_manager.py    # Tests for database operations
│   └── gui/
│       └── utils/
│           └── test_json_search_engine.py  # Tests for search engine
└── integration/
    └── test_data_integrity.py    # Data validation tests
```

## Running Tests

### Run all tests:
```bash
pytest
```

### Run with coverage:
```bash
pytest --cov=src --cov-report=html
```

### Run specific test file:
```bash
pytest tests/unit/models/test_plate_models.py
```

### Run specific test class:
```bash
pytest tests/unit/models/test_plate_models.py::TestStateModel
```

### Run specific test:
```bash
pytest tests/unit/models/test_plate_models.py::TestStateModel::test_state_creation_with_all_fields
```

### Run tests by marker:
```bash
pytest -m unit          # Run only unit tests
pytest -m integration   # Run only integration tests
pytest -m database      # Run only database tests
```

### Run with verbose output:
```bash
pytest -v
```

### Run and show print statements:
```bash
pytest -s
```

## Test Categories

### Unit Tests (~220 tests)
- **Models** (25 tests): Data model creation, validation, and serialization
- **Helpers** (40 tests): Utility functions for plate text processing, validation, file I/O
- **Database** (45 tests): Database operations, CRUD, schema validation
- **Image Manager** (20 tests): Image import, organization, metadata
- **JSON Search Engine** (30 tests): Search functionality, state data loading

### Integration Tests (~20 tests)
- **Data Integrity**: Validate all JSON files, schema compliance, color codes

## Coverage Goals

- **Overall Target**: 80%+
- **Critical Modules**: 90%+
  - src/utils/helpers.py
  - src/models/plate_models.py
  - src/database/db_manager.py

## Writing New Tests

### Test Naming Convention
- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`

### Example Test:
```python
import pytest

class TestMyFeature:
    def test_basic_functionality(self):
        """Test basic feature behavior"""
        result = my_function()
        assert result == expected_value
    
    def test_edge_case(self):
        """Test edge case handling"""
        with pytest.raises(ValueError):
            my_function(invalid_input)
```

### Using Fixtures:
```python
def test_with_database(db_manager):
    """Test using database fixture from conftest.py"""
    result = db_manager.get_all_states()
    assert isinstance(result, list)
```

## Continuous Integration

Tests are designed to run in CI/CD pipelines. Key features:
- Fast execution (most unit tests < 1ms)
- No external dependencies (uses in-memory databases)
- Comprehensive coverage reports
- Clear failure messages

## Troubleshooting

### Import Errors
Ensure the src directory is in your Python path. The conftest.py handles this automatically.

### Database Errors
Tests use temporary in-memory databases. If you see database errors, check that SQLite is properly installed.

### Missing Dependencies
Install test dependencies:
```bash
pip install -r requirements.txt
```

## Contributing

When adding new features:
1. Write tests first (TDD approach)
2. Ensure tests pass: `pytest`
3. Check coverage: `pytest --cov=src`
4. Aim for 80%+ coverage on new code
5. Update this README if adding new test categories
