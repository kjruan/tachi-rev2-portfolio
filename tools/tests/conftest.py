"""
Pytest configuration and shared fixtures
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def sample_ticker():
    """Fixture providing a sample ticker for testing"""
    return "AAPL"


@pytest.fixture
def sample_tickers():
    """Fixture providing multiple sample tickers"""
    return ["AAPL", "MSFT", "GOOGL"]


@pytest.fixture
def sample_portfolio():
    """Fixture providing a sample portfolio"""
    return {
        "AAPL": 10,
        "MSFT": 5,
        "GOOGL": 2,
    }


@pytest.fixture
def mock_stock_info():
    """Fixture providing mock stock info data"""
    return {
        "currentPrice": 150.00,
        "previousClose": 148.00,
        "regularMarketChange": 2.00,
        "regularMarketChangePercent": 1.35,
        "volume": 50000000,
        "marketCap": 2500000000000,
        "fiftyTwoWeekHigh": 180.00,
        "fiftyTwoWeekLow": 120.00,
        "trailingPE": 25.5,
        "dividendYield": 0.005,
        "beta": 1.2,
    }


def pytest_configure(config):
    """Configure pytest with custom settings"""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test (fast, mocked)"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test (slow, real API)"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically"""
    for item in items:
        # Add 'unit' marker to tests that don't have 'integration' marker
        if "integration" not in item.keywords and "slow" not in item.keywords:
            item.add_marker(pytest.mark.unit)
