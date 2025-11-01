# Tools Test Suite

Comprehensive test suite for the trading tools in the Tachi CLI project.

## Overview

This test suite includes:
- **Unit Tests**: Fast tests with mocked dependencies
- **Integration Tests**: Tests that make real API calls to verify actual behavior
- **Performance Tests**: Tests for performance and stress testing

## Test Files

- `test_stock_data_tool.py` - Tests for stock data fetching tools
- `test_technical_indicators_tool.py` - Tests for technical analysis tools
- `test_news_sentiment_tool.py` - Tests for news and sentiment analysis tools
- `test_integration.py` - End-to-end integration tests

## Running Tests

### Install Test Dependencies

```bash
pip install -r requirements-test.txt
```

### Run All Tests

```bash
# From the tests directory
pytest

# From the project root
pytest rev2/tools/tests/
```

### Run Specific Test Types

```bash
# Run only unit tests (fast, no API calls)
pytest -m unit

# Run only integration tests (requires internet)
pytest -m integration

# Run tests for a specific tool
pytest test_stock_data_tool.py

# Run a specific test class
pytest test_stock_data_tool.py::TestGetStockPrice

# Run a specific test
pytest test_stock_data_tool.py::TestGetStockPrice::test_get_stock_price_success
```

### Run Tests with Coverage

```bash
# Generate coverage report
pytest --cov=../ --cov-report=html --cov-report=term

# View HTML coverage report
open htmlcov/index.html
```

### Run Tests in Parallel

```bash
# Run tests in parallel using multiple CPU cores
pytest -n auto
```

## Test Markers

Tests are marked with the following markers:

- `@pytest.mark.unit` - Unit tests (fast, mocked dependencies)
- `@pytest.mark.integration` - Integration tests (requires API access)
- `@pytest.mark.slow` - Slow running tests

## Writing New Tests

### Unit Test Example

```python
import pytest
from unittest.mock import patch

@patch("stock_data_tool.yf.Ticker")
def test_my_function(mock_ticker):
    mock_ticker.return_value.info = {"currentPrice": 150.0}
    result = my_function("AAPL")
    assert result["price"] == 150.0
```

### Integration Test Example

```python
@pytest.mark.integration
def test_real_api_call():
    result = get_stock_price.func("AAPL")
    assert "current_price" in result or "error" in result
```

## Test Structure

Each test file follows this structure:

1. **Imports and setup** - Import necessary modules and tools
2. **Test classes** - Group related tests together
3. **Individual tests** - Test specific functionality
4. **Integration tests** - Test real API interactions (marked with `@pytest.mark.integration`)

## Fixtures

Common fixtures are defined in `conftest.py`:

- `sample_ticker` - Returns "AAPL" for testing
- `sample_tickers` - Returns list of sample tickers
- `sample_portfolio` - Returns a sample portfolio dictionary
- `mock_stock_info` - Returns mock stock info data

## Best Practices

1. **Use mocks for unit tests** - Avoid real API calls in unit tests
2. **Mark integration tests** - Use `@pytest.mark.integration` for tests that make API calls
3. **Test error cases** - Always test error handling
4. **Test edge cases** - Test boundary conditions and unusual inputs
5. **Keep tests independent** - Each test should be able to run independently
6. **Use descriptive names** - Test names should clearly describe what they test

## CI/CD Integration

To run tests in CI/CD pipelines:

```bash
# Run only fast unit tests
pytest -m unit --tb=short

# Run all tests including integration
pytest --tb=short
```

## Troubleshooting

### API Rate Limits

If integration tests fail due to rate limits:
- Run only unit tests: `pytest -m unit`
- Reduce parallel test execution
- Add delays between API calls

### Missing Dependencies

```bash
pip install -r requirements-test.txt
```

### Import Errors

Make sure the parent directory is in your Python path:
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
```

## Coverage Goals

Target coverage metrics:
- Overall: >80%
- Critical functions: >90%
- Error handling: 100%
